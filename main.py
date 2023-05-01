import praw
import pandas as pd
import re
import gensim
import nltk
from nltk import TreebankWordDetokenizer
from num2words import num2words
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import logging
import sys
from io import StringIO

def send_email(send_to, subject, crash_message):
    email = 'kcford26@gmail.com'
    send_to_email = send_to #'fordcb@lafayette.edu'
    subject = subject
    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = send_to_email
    msg['Subject'] = subject
    message = crash_message
    msg.attach(MIMEText(message, 'plain'))
    # Send the message via SMTP server.
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('kcford26@gmail.com', 'tjajkllenxbvmzgk')
    text = msg.as_string()
    server.sendmail(email, send_to_email, text)
    server.quit()
    print('email sent to ' + str(send_to_email))
    return True

def depure_data(data):
    # Removing URLs with a regular expression
    url_pattern = re.compile(r'https?://\S+|www\.\S+')
    data = url_pattern.sub(r'', data)

    # Remove Emails
    data = re.sub('\S*@\S*\s?', '', data)

    # Remove new line characters
    data = re.sub('\s+', ' ', data)
    data = re.sub('\n', ' ', data)

    # Remove distracting single quotes
    data = re.sub("\'", "", data)

    # Remove jargon with regular expression
    data = re.sub(r'aita', 'am I the asshole', data, flags=re.IGNORECASE)
    data = re.sub(r'nta', 'not the asshole', data, flags=re.IGNORECASE)
    data = re.sub(r'yta', 'you\'re the asshole', data, flags=re.IGNORECASE)
    data = re.sub(r'esh', 'everyone sucks here', data, flags=re.IGNORECASE)
    data = re.sub(r'nah', 'no assholes here', data, flags=re.IGNORECASE)
    data = re.sub(r'ta', 'the asshole', data, flags=re.IGNORECASE)

    # Removing jargon of gender + age identifier like 35m 45F
    match1 = re.findall(r"\d+\s*[mM]", data)
    match2 = re.findall(r"\d+\s*[fF]", data)

    for match in match1:
        num1 = int(re.findall(r"\d+", match)[0])  # extract the number from the matched string
        word = num2words(num1)  # convert the number to its word form
        data = data.replace(match, f"{word} male")  # replace the matched string with the word plus "male"

    for match in match2:
        num2 = int(re.findall(r"\d+", match)[0])  # extract the number from the matched string
        word = num2words(num2)  # convert the number to its word form
        data = data.replace(match, f"{word} female")  # replace the matched string with the word plus "female"

    return data


def sent_to_words(sentences):
    for sentence in sentences:
        yield (gensim.utils.simple_preprocess(str(sentence), deacc=True))


def detokenize(text):
    return TreebankWordDetokenizer().detokenize(text)


def clean_text(inData):
    temp = inData

    depured = depure_data(temp)
    data_words = sent_to_words(depured)
    detokenized = detokenize(data_words)

    return detokenized


try:
    # Read-only instance
    reddit = praw.Reddit(client_id="iKq7bmcsBuF0aH2C3uUmPA",  # your client id
                         client_secret="WlB5uVd2GP1wPlL1xrEbhnRnjNUz2w",  # your client secret
                         user_agent="Berryhill_",  # your user agent
                         check_for_async=False)

    subreddit = reddit.subreddit("AmITheAsshole")

    # Scraping the top posts of all time
    posts = subreddit.top(time_filter="all")


    posts_dict = {"Post Text": [], "Label": [],
                  "ID": [], "Post URL": []
                  }
    # time_dict = {"post times": [], "regex times": []}

    cnt = 0
    limit = 10000

    for post in posts:
        if len(post.comments) >= 2:
            top_comment = post.comments[1].body

            nta_label = re.search("NTA", top_comment)
            yta_label = re.search("YTA", top_comment)
            label = ""

            if nta_label != None:
                label = "nta"
            elif yta_label != None:
                label = "yta"

            # check that top comment includes a label
            if label != "":
                # Text inside a post
                post_text = post.selftext
                cleaned = clean_text(post_text)
                posts_dict["Post Text"].append(post.selftext)

                # label associated with top comment
                posts_dict["Label"].append(label)

                # Unique ID of each post
                posts_dict["ID"].append(post.id)

                # URL of each post
                posts_dict["Post URL"].append(post.url)
                cnt += 1
                if cnt % 100==0:
                    top_posts = pd.DataFrame(posts_dict)
                    top_posts.to_csv(f"Posts_{cnt}.csv", index=True)
                if cnt % 1000==0:
                    send_email('fordcb@lafayette.edu', "REDDIT SCRAPER: +1000", ":)")
                    send_email('naiks@lafayette.edu', "REDDIT SCRAPER: +1000", ":)")
                    send_email('lansingk@lafayette.edu', "REDDIT SCRAPER: +1000", ":)")
                if cnt >= limit:
                    break

    # Saving the data in a pandas dataframe
    top_posts = pd.DataFrame(posts_dict)
    top_posts.to_csv("All_Posts.csv", index=True)
except Exception as e:
    log_stream = StringIO()
    logging.basicConfig(stream=log_stream, level=logging.INFO)
    logging.error("Exception occurred", exc_info=True)
    send_email('fordcb@lafayette.edu', "CRASHED: REDDIT SCRAPER", f":( {log_stream.getvalue()}")
    send_email('naiks@lafayette.edu', "CRASHED: REDDIT SCRAPER", f":( {log_stream.getvalue()}")
    send_email('lansingk@lafayette.edu', "CRASHED: REDDIT SCRAPER", f":( {log_stream.getvalue()}")
