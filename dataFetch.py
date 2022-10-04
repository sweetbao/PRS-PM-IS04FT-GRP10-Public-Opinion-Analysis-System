import requests
from bs4 import BeautifulSoup
import re
import os
import json

bearer_token = 'AAAAAAAAAAAAAAAAAAAAAH6%2FhgEAAAAAC174stDAGI%2FLK7FVJCUdZNIXdr8%3DBddrVjoAkoV2erXv1tZCFWSM7oBYsotbCWWa56AmkVKADFnGHQ'

search_url = "https://api.twitter.com/2/tweets/counts/recent"

# Optional params: start_time,end_time,since_id,until_id,next_token,granularity
query_params = {'query': 'from:twitterdev','granularity': 'day'}

def is_contains_english(str):
    my_re = re.compile(r'[A-Za-z]', re.S)
    res = re.findall(my_re, str)
    if len(res):
        return True
    else:
        return False


def get_latestTopic():
    res = requests.get('https://twitter-trends.iamrohit.in/singapore')
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')

    topic_list = []
    count = 1
    while len(topic_list) < 10:
        print(len(topic_list) + 1)
        a = soup.find('a', class_="tweet", rank=count).text
        count = count + 1
        if is_contains_english(a):
            topic_list.append(a)
            print(a)

    return topic_list


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2FilteredStreamPython"
    return r


def get_rules():
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream/rules", auth=bearer_oauth
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot get rules (HTTP {}): {}".format(response.status_code, response.text)
        )
    print(json.dumps(response.json()))
    return response.json()


def delete_all_rules(rules):
    if rules is None or "data" not in rules:
        return None

    ids = list(map(lambda rule: rule["id"], rules["data"]))
    payload = {"delete": {"ids": ids}}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        auth=bearer_oauth,
        json=payload
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot delete rules (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )
    print(json.dumps(response.json()))


def set_rules(delete):
    # You can adjust the rules if needed
    trendings = get_latestTopic()
    sample_rules = [
        # {"value": "dog has:images", "tag": "dog pictures"},
        {"value": trendings[0], "tag": trendings[0]},

    ]
    payload = {"add": sample_rules}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        auth=bearer_oauth,
        json=payload,
    )
    if response.status_code != 201:
        raise Exception(
            "Cannot add rules (HTTP {}): {}".format(response.status_code, response.text)
        )
    print(json.dumps(response.json()))


def get_stream(set):
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream", auth=bearer_oauth, stream=True,
    )
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Cannot get stream (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )
    for response_line in response.iter_lines():
        if response_line:
            json_response = json.loads(response_line)
            print(json.dumps(json_response, indent=4, sort_keys=True))


def main():
    rules = get_rules()
    delete = delete_all_rules(rules)
    set = set_rules(delete)
    get_stream(set)


if __name__ == "__main__":
    main()