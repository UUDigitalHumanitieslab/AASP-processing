AASP-processing
===============================================================================
Custom scripts for processing arff and TextGrid files to be used in the Automatic Analysis of Speech Prosody project

To run:
1. Make sure you have Python 3.6 installed (e.g. via [Anaconda](https://www.anaconda.com/distribution/))
2. If you do not want to install the required libraries globally, make a conda environment (see instructions [here](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html))
3. Navigate to this directory and run `pip install -r requirements.txt`
4. In this directory, run the script: `python process.arff.py -a PATH/TO/YOUR/ARFF/FEATURE/FILES -t PATH/TO/YOUR/TEXTGRID/FILES` This will
- adjust the headers of the arff feature files and write new files into a directory. By default, subdirectory 'processed' in the source files, you can set another directory with the -c flag.
- step through the directory with TextGrid files (including subdirectories) and collect the annotated intonations, and combine them with the features from the arff files in a large output file. By default, the complete table is written to  `combined.arff`, and a table without string parameters will be written to `combined_nostring.arff` in this directory. You can set another filename with the -o flag.
- For help with the script, you can pass `python process.py --help`