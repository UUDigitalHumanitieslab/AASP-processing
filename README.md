AASP-processing
===============================================================================
This reposistory contains scripts to train speech prosody classifiers, to be used in the [Automatic Analysis of Speech Prosody](https://github.com/UUDigitalHumanitieslab/AASP) application. The scripts collected here can be used to use audio features extracted with the speech prosody analysis tool [AuToBI](https://github.com/AndrewRosenberg/AuToBI) to predict human annotations in .TextGrid format.

For more documentation about the file types:
- [arff](https://www.cs.waikato.ac.nz/ml/weka/arff.html) format, as used by the machine learning library Weka. These files are a specialized version of a csv, in which each feature name is listed as @ATTRIBUTE on top of the file, and the feature value is a cell in a comma-separated grid
- [TextGrid](https://www.fon.hum.uva.nl/praat/manual/TextGrid.html) format, as used by audio annotation and analysis software Praat.

## Prerequesites
1. Make sure you have Python 3.6 installed (e.g. via [Anaconda](https://www.anaconda.com/distribution/))
2. If you do not want to install the required libraries globally, make a conda environment (see instructions [here](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html))
3. Navigate to this directory and run `pip install -r requirements.txt`

## Running
The repository contains two scripts:
1. `process_arff` can be used to combine audio features computed by [AuToBI](https://github.com/AndrewRosenberg/AuToBI) (in arff format) with human annotations (in TextGrid format). `python process_arff.py -a PATH/TO/YOUR/ARFF/FEATURE/FILES -t PATH/TO/YOUR/TEXTGRID/FILES` will:
    - adjust the headers (`@ATTRIBUTE`s) of the arff feature files and write new files into a directory. By default, this will be subdirectory called 'processed' in the source file directory, you can set another directory with the -c flag.
    - step through the directory with TextGrid files (including subdirectories) and collect the annotated intonations, and combine them with the features from the arff files in a large output file. By default, the complete table is written to  `combined.arff`, and a table with only numerical parameters will be written to `combined_nostring.arff` in this directory. You can set another filename with the -o flag.
    -  For help with the script, call `python process_arff.py --help`
2. As a next step, `train_classifiers` documents how to train a new classifier using Python's [scikit-learn](https://scikit-learn.org/stable/), in which the features extracted from the .arff file will be use to predict the annotations extracted from the `.TextGrid` file. It shows how to achieve train / test split, and suggests that a random forest classifier may achieve around 0.9 accuracy for prediction of tone and accent, which were the annotated features in data used for making a proof of concept.
