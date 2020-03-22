import requests
import xmltodict
from dealabs.deal import Deal

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36\''
}

url = "https://www.dealabs.com/rssx/keyword-alarm/"
token = "l1O2vYj_HbIT3ja9sfD779D7_qv0LFr8vJtEwce_GTc."


def request_xml():
    join_url = url + token;
    return requests.request(method='GET', url=join_url, headers=headers).text.encode('utf8')


def format_to_json(data):
    return xmltodict.parse(data)


deals = Deal.getAll(request_xml())

for d in deals:
    print(d.title)
