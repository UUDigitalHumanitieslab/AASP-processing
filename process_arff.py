import os.path as op
import os
import glob
import re

import click
import arff # liac-arff for arff processing
import pympi # pympi-ling for textgrid processing


PROBLEMATIC_ATTRS = [
    'nominal_PitchAccent', 
    'hyp_pitch_accent_type',
    'nominal_PitchAccentType',
    'hyp_pitch_accent_location'
    ]


def parse_files(directory, output_dir):
    ''' given a directory of .arff files, rewrite them to a format
    which can be read by libraries such as R and Weka.
    '''
    files  = glob.glob('{}/*.arff'.format(directory))
    for arff_file in files:        
        output_file = op.join(output_dir, (op.splitext(op.split(arff_file)[1])[0] + '_fixed_header.arff'))
        adjust_header(arff_file, output_file)


def adjust_header(in_file, out_file):
    ''' write out a new file as output_file, with the header adjusted
    such that categorical variables are labeled as "string"
    '''
    with open(in_file) as f:
        text = f.readlines()
    with open(out_file, 'w') as f:
        for row in text:
            content = row.split()
            if len(content)<3:
                row_cleaned = re.sub(r'\?', 'NaN', row)
                f.write(row_cleaned)
                continue
            if content[1] in PROBLEMATIC_ATTRS:
                row = "{} {} {}\n".format(content[0], content[1], 'string')
            f.write(row)


def get_feature_data(filename):
    ''' find the information under the @data header 
    and return that part of the file 
    '''
    with open(filename) as f:
        text = f.read()
    seek = text.rfind('@data')+5
    return text[seek:-1]


def combine_textgrid_data(
                        textgrid_dir,
                        arff_dir,
                        output_file,
                        suppress_strings=False,):
    ''' given a directory containing arff files with feature data,
    look for the relevant tones in corresponding textgrid files.
    If suppress_strings is True, no string attributes will be written.
    '''
    textgrid_files = glob.glob('{}/**/*.TextGrid'.format(textgrid_dir), recursive=True)
    arff_files = glob.glob('{}/*.arff'.format(arff_dir))
    intonations = set()
    boundaries = set()
    all_data = []
    for tg in textgrid_files:
        counter = -1
        tg_data = pympi.Praat.TextGrid(tg)
        try:
            words = tg_data.get_tier('segment').get_all_intervals()
            tones = tg_data.get_tier('intonation').get_all_intervals()
        except Exception as e:
            continue
        arff_file = next((
            af for af in arff_files if op.split(af)[1].startswith(
                op.splitext(op.split(tg)[1])[0]
            )
            ), None)
        if not arff_file:
            continue
        arff_data = arff.load(open(arff_file, 'r'))
        arff_attributes = arff_data['attributes']
        string_ind = [
            i for i, a in enumerate(arff_attributes) 
            if a[0] in PROBLEMATIC_ATTRS
        ]
        # word is a tuple of mintime, maxtime, and the word
        for word in words:
            if word[-1]!='':
                counter += 1
                feature_row = arff_data['data'][counter]
                tone = next((t[1] for t in tones if t[0]>word[0] and t[0]<word[1]), None)
                boundary = next((
                    t[1] for t in tones if t[0]==word[0] or t[0]==word[1]), None)
                if tone:
                    if '%' in tone:
                        # % is a boundary sign
                        boundary = tone
                        tone = None
                        feature_row.append('unaccented')
                    else:
                        intonations.add(tone)
                        feature_row.append('accented')
                else:
                    feature_row.append('unaccented')
                if boundary:
                    boundaries.add(boundary)
                feature_row.append(boundary) # add boundary, second to last column
                feature_row.append(tone) # add tone, as last column
                if not suppress_strings:
                    feature_row.append(op.split(tg)[1]) # add filename
                    feature_row.append(word[-1]) # add word in question
                    # move autobi predictions to end of file
                    for ind in string_ind:
                        feature_row.append(feature_row[ind])
                new_row = [f for i, f in enumerate(feature_row) if 
                            i not in string_ind]
                all_data.append(new_row)
    arff_output = arff.load(open(arff_files[0], 'r'))
    output_attrs = arff_output['attributes']
    output_attrs.extend([
        ('accent', ['accented', 'unaccented']),
        ('boundary', list(boundaries)),
        ('tone', list(intonations))
    ])
    if not suppress_strings:
        output_attrs.extend([
            ('file_name', 'STRING'), 
            ('word', 'STRING')
        ])
        output_attrs.extend([
            output_attrs[i] for i in string_ind
        ])
    arff_output['attributes'] = [
        attr for i, attr in enumerate(output_attrs) if 
        i not in string_ind
    ]
    arff_output['data'] = all_data
    with open(output_file, "w") as f:
        f.write(arff.dumps(arff_output))


@click.command()
@click.option('--arff_dir', '-a', 'source_arff_dir',
              help='The source directory of arff files.',
              type=click.Path(exists=True),
              required=True)
@click.option('--textgrid', '-t', 'textgrid_dir',
              help='The source directory of TextGrid files.',
              type=click.Path(exists=True),
              required=True)
@click.option('--clean', '-c', 'cleaned_arff_dir',
              help='The directory where to write processed arff files.',
              default='processed',
              show_default=True)
@click.option('--out', '-o', 'output_file',
              help='The file name of the output file.',
              default='combined.arff',
              show_default=True
              )
def main(source_arff_dir, textgrid_dir, cleaned_arff_dir, output_file):
    if cleaned_arff_dir=='processed':
        cleaned_arff_dir = op.join(source_arff_dir, cleaned_arff_dir)
    if not op.exists(cleaned_arff_dir):
        os.makedirs(cleaned_arff_dir)
    parse_files(source_arff_dir, cleaned_arff_dir)
    combine_textgrid_data(textgrid_dir, cleaned_arff_dir, output_file)
    out_nostring = "{}_nostring.{}".format(*output_file.split("."))
    combine_textgrid_data(textgrid_dir, cleaned_arff_dir, out_nostring, suppress_strings=True)


if __name__ == '__main__':
    main()



    
