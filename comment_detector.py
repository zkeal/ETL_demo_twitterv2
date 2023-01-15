# -*- coding: utf-8 -*-
import json
import twitterAPI
from textblob import TextBlob
from classify_sentences import classify
from collections import Counter


class detector():
    def __init__(self, config_path='config.json', max_count = 100):
        self.query, self.bearer_token = self.load_config(config_path)
        self.exclude_language = 'en'
        self.max_count = 100

    def load_config(self, config_path):
        with open(config_path, 'r') as load_f:
            load_dict = json.load(load_f)
        return load_dict['query'], load_dict['BearerToken']

    def detect_streaming(self, max_iter = 100):

        #collection for storage data
        raw_json = []
        sentiments_json = []
        meta_json = []

        twitterAPI.post_rule(self.query, hash(str(self.query)), bearer_token = self.bearer_token)

        for id, content, raw_data in twitterAPI.start_stream(tweet_fields ='lang', expansions = 'author_id', user_fields = 'id', bearer_token = self.bearer_token):
            try:
                trans_text = content
                prediction = classify(trans_text)

                sentiment = dict()
                sentiment['id'] = id
                sentiment['sentiment'] = prediction
                sentiments_json.append(json.dumps(sentiment))

                raw_json.append(raw_data)
                meta_json.append(prediction)

                meta_dict = dict(Counter(meta_json))
                self.storage_data('meta.json', json.dumps(meta_dict))
            except Exception as e:
                print('error dealing with raw')

            if len(raw_json) >= max_iter:
                self.storage_data('raw.json', raw_json)
                self.storage_data('sentiments.json', sentiments_json)

                raw_json.clear()
                sentiments_json.clear()
                break


    @staticmethod
    def storage_data(file_name, datalist):
        f = open(file_name, 'w')
        f.writelines(datalist)
        f.close()

