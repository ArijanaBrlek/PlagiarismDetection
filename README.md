# Plagiarism detection

A plagiarism detection classifier built as part of the Text Analysis and Retrieval course project.

## Running

Prerequisites:
Download word2vec pre-trained vectors trained on Google News dataset. The archive is available at:
https://code.google.com/archive/p/word2vec/

Right now the dataset needs to be present in the root folder of the project.

Command to run the classifier:

$ python src/baseline.py data/pairs data/src/ data/susp/ data/out/
