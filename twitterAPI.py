# -*- coding: utf-8 -*-
import requests
import json
import re
import traceback


def twitter_auth(func):
    def set_headers(*args, **kwargs):
        bearer_token = kwargs['bearer_token']
        headers = {"Authorization": "Bearer {}".format(bearer_token)}
        kwargs['headers'] = headers
        return func(*args, **kwargs)
    return set_headers


@twitter_auth
def post_rule(rule,tag, **kwargs):
    url = 'https://api.twitter.com/2/tweets/search/stream/rules'
    post_headers = kwargs['headers']
    post_headers['Content-type'] = "application/json"
    body =  {"add": [{"value": rule, "tag":tag}]}
    post_response = requests.request("POST", url, headers=post_headers, data=json.dumps(body))
    if post_response.status_code != 201:
        raise Exception(post_response.status_code, post_response.text)
    check_response = requests.request("GET", url, headers=kwargs['headers'])
    if check_response.status_code != 200:
        raise Exception(post_response.status_code, post_response.text)
    if re.search(rule, check_response.text) is None:
        raise Exception(check_response.status_code, "post rule failed")


@twitter_auth
def delete_rule(ids, **kwargs):
    url = 'https://api.twitter.com/2/tweets/search/stream/rules'
    post_headers = kwargs['headers']
    post_headers['Content-type'] = "application/json"
    body = {"delete": {"ids": ids}}
    post_response = requests.request("POST", url, headers=post_headers, data=json.dumps(body))
    if post_response.status_code != 200:
        raise Exception(post_response.status_code, post_response.text)


@twitter_auth
def start_stream(**kwargs):
    url = "https://api.twitter.com/2/tweets/search/stream?tweet.fields={}&expansions={}&user.fields={}".format(
        kwargs['tweet_fields'], kwargs['expansions'], kwargs['user_fields']
    )
    steam_r = requests.get(url, headers=kwargs['headers'], stream=True)
    raw_set = set()
    for line in steam_r.iter_lines():
        try:
            raw_data = line.decode('utf-8')
            if len(raw_data) == 0:
                continue
            raw_set.add(raw_data)
            r_dict = json.loads(raw_data)
            r_body = r_dict['data']
            if 'en' != r_body['lang']:
                if r_body['id'] not in raw_set:
                    raw_set.add(r_body['id'])
                    yield r_body['id'], r_body['text'], raw_data
        except json.decoder.JSONDecodeError as e:
            print('traceback.print_exc(), with raw:')
            traceback.print_exc()
        except KeyError:
            print('failed to stream data, please check the token')
            traceback.print_exc()
#
# if __name__ == "__main__":
#     delete_rule([1387335211394940932],bearer_token = 'AAAAAAAAAAAAAAAAAAAAAIHdOwEAAAAAeEv2s7uvNJU%2FQO3GXIZnVG34Aa8%3DuHn6yORO254J7WpW07h22aZmymez1pHKp0b3YG1aKmGqGN2Xne')