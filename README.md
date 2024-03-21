AASP-processing
===============================================================================
Custom scripts for processing two kinds of file types:
- [arff](https://www.cs.waikato.ac.nz/ml/weka/arff.html) format, as used by the machine learning library Weka. These files are a specialized version of a csv, in which the column headers are listed as @ATTRIBUTE on top of the file
- [TextGrid](https://www.fon.hum.uva.nl/praat/manual/TextGrid.html) format, as used by audio annotation and analysis software Praat.

The purpose of the scripts in this repository is to produce files compatible for use in the [Automatic Analysis of Speech Prosody](https://github.com/UUDigitalHumanitieslab/AASP) application.

## Prerequesites
1. Make sure you have Python 3.6 installed (e.g. via [Anaconda](https://www.anaconda.com/distribution/))
2. If you do not want to install the required libraries globally, make a conda environment (see instructions [here](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html))
3. Navigate to this directory and run `pip install -r requirements.txt`

## Running
Run the script: `python process_arff.py -a PATH/TO/YOUR/ARFF/FEATURE/FILES -t PATH/TO/YOUR/TEXTGRID/FILES` This will:
- adjust the headers (`@ATTRIBUTE`s) of the arff feature files and write new files into a directory. By default, this will be subdirectory called 'processed' in the source file directory, you can set another directory with the -c flag.
- step through the directory with TextGrid files (including subdirectories) and collect the annotated intonations, and combine them with the features from the arff files in a large output file. By default, the complete table is written to  `combined.arff`, and a table with only numerical parameters will be written to `combined_nostring.arff` in this directory. You can set another filename with the -o flag.
- For help with the script, call `python process_arff.py --help`
