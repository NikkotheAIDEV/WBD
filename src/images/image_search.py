from typing import Dict
import requests
import re
import json
import time
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def search(keywords: str, max_results = None) -> Dict:
    url = 'https://duckduckgo.com/'
    params = {
    	'q': keywords
    }

    logger.debug("Hitting DuckDuckGo for Token")

    res = requests.post(url, data=params)
    searchObj = re.search(r'vqd=([\d-]+)\&', res.text, re.M|re.I)

    if not searchObj:
        logger.error("Token Parsing Failed !")
        return -1

    logger.debug("Obtained Token")

    headers = {
        'authority': 'duckduckgo.com',
        'accept': 'application/json, text/javascript, */* q=0.01',
        'sec-fetch-dest': 'empty',
        'x-requested-with': 'XMLHttpRequest',
        'user-agent': 'Mozilla/5.0 (Macintosh Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'referer': 'https://duckduckgo.com/',
        'accept-language': 'en-US,enq=0.9',
    }

    params = (
        ('l', 'us-en'),
        ('o', 'json'),
        ('q', keywords),
        ('vqd', searchObj.group(1)),
        ('f', ',,,'),
        ('p', '1'),
        ('v7exp', 'a'),
    )

    requestUrl = url + "i.js"

    logger.debug("1, Hitting Url : %s", requestUrl)

    while True:
        try:
            res = requests.get(requestUrl, headers=headers, params=params)
            data = json.loads(res.text)
            break
        except ValueError as e:
            logger.debug("Hitting Url Failure - Sleep and Retry: %s", requestUrl)
            time.sleep(4)
            continue

    return data
    # response = requests.get(requestUrl, headers=headers, params=params)
    # data = json.loads(response.text)
    # return data

def search_museum(name: str, num_results = 5) -> dict:
        
        results = search(name)
        result = results["results"]

        data: dict = {}
        for i in range(num_results):
            key_image = "image_" + str(i+1)
            data[key_image] = result[i]["image"]
            key_thumb = "thumbnail_" + str(i+1)
            data[key_thumb] = result[i]["thumbnail"]
        return data


if __name__ == "__main__":
    search("test")