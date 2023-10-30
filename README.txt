We have several files which we used to run our program:

python3 Manual_Classify.py
  This was used to create the useful.txt and discard.txt files which we
  later used to train BERT

python3 Manual_Sentiment.py
  This was used to split useful.txt into positives.txt and
  negatives.txt, which made it easier to do sentiment analysis with BERT
  and lexicon

python3 Lexicon_Classifier.py
  This was used to parse the tweets from the database and classify them
  based on the lexicon approach

python3 Bert_Sentiment.py
  This was used to parse the tweets from the database and classify them
  based on the BERT approach: warning, this tends to crash or get killed

We also scripted with python to transform the outputs of these programs
into our neg_sums and pos_sums for lexicon and bert. We do not have the
code for this as it was done manually from the command line, but is
relatively trivial. We have supplied these csvs so that you can look at
them for yourself.
The dataset and all our files are stored on google drive at:
https://drive.google.com/drive/folders/1pakv4S9zo1yloFLH03U-tmutugvun7Ao?usp=sharing
