#!/usr/bin/env python

# Twitter Bot: Responding Bot

# This bot listens to the account @QuinOcellEs.

import os
import pathlib
import requests
import tensorflow as tf
import time
import tweepy

from io import BytesIO
from keys import keys
import numpy as np
from PIL import Image
from species import species
from tensorflow import keras
from tensorflow.keras.models import load_model

CONSUMER_KEY = keys['api_key']
CONSUMER_KEY_SECRET = keys['api_secret_key']

ACCESS_TOKEN = keys['access_token']
ACCESS_TOKEN_SECRET = keys['access_token_secret']

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_KEY_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth, wait_on_rate_limit=True)
since_id = 1

image_classification_model = load_model('./bird_classification_v2.h5')
img_height = 180
img_width = 180

def process_image(filename, i):
    image_path = pathlib.Path(filename)

    # Pre-process image
    preprocessed_image = keras.preprocessing.image.load_img(
        image_path, target_size=(img_height, img_width)
    )

    img_array = keras.preprocessing.image.img_to_array(preprocessed_image)
    img_array = tf.expand_dims(img_array, 0)

    # Predict bird specie
    predictions = image_classification_model.predict(img_array)
    score = tf.nn.softmax(predictions[0])
    
    return "Imatge {}: {} amb {:.2f} % probabilitat.".format(i, species[np.argmax(score)], 100 * np.max(score))


def check_mentions(api, since_id):
    new_since_id = since_id
    for tweet in tweepy.Cursor(api.mentions_timeline, since_id=since_id).items():
        new_since_id = max(tweet.id, new_since_id)

        # Mention found, replying...
        replyUsername = tweet.user.screen_name
        replyMessage = "@%s Hello!" % (replyUsername)
        api.update_status(replyMessage, tweet.id)

    return new_since_id

def download_image(url):
    response = requests.get(url)
    filename = url.split("/")[-1]
    with open(filename, "wb") as file:
        file.write(response.content)

    return filename


def find_tweets(api):
    # fetching tweets
    tweets = api.user_timeline(count = 1)
      
    for tweet in tweets:
        # get all the images for each tweet
        try:
            images = tweet.extended_entities['media']

            reply_message = "@" + tweet.user.screen_name
            
            for i, img in enumerate(images, start = 1):
                # Download image
                filename = download_image(img['media_url'])

                # Process image
                prediction_message = process_image(filename, i)
                reply_message = reply_message + "\n" + prediction_message

                # Delete downloaded image
                os.remove(filename)

            # Reply
            print(reply_message)
            api.update_status(reply_message, tweet.id)
        except Exception as e:
            print(e)


#while True:
    #since_id = check_mentions(api, since_id)
find_tweets(api)
    #time.sleep(5)