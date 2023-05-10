# AmITheAsshole_ML
Given a text post on the subreddit r/AmITheAsshole, we trained a model to predict whether or not the Reddit community thinks that the poster of an AITA post is or is not the asshole. 

# Files

### Every_Post.csv

This csv file contains all the posts that were scraped from Reddit and used as our data set.

### bert_model.h5

This is the model, containing the weights. The fine-tuning step of the project had to be run on a PC, outside of the Google Colab due to the computational requirements 
which is why the model was saved as an h5 and uploaded separetly here. It is loaded into the self-sustained notebook for the evaluation step.

### main.py

This is the code that was used to run scrape the data from Reddit.

### pretrained_bert_model.py

This is the code used to fine-tune the model, outside of the Google Colab.

### tensorboard_data

Contains the tensorboards that were run outside of the Google Colab. They are imported into the Colab and rendered there.
