import logging
import traceback
from json.decoder import JSONDecodeError
from time import sleep

import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import xmltodict
import json as json_func
from bs4 import BeautifulSoup
from requests import ReadTimeout, ConnectTimeout
import ssl

logger = logging.getLogger("app")


class CustomHttpAdapter (requests.adapters.HTTPAdapter):
    # "Transport adapter" that allows us to use custom ssl_context.

    def __init__(self, ssl_context=None, **kwargs):
        self.ssl_context = ssl_context
        super().__init__(**kwargs)

    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = urllib3.poolmanager.PoolManager(
            num_pools=connections, maxsize=maxsize,
            block=block, ssl_context=self.ssl_context)


def get_legacy_session():
    ctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    ctx.options |= 0x4  # OP_LEGACY_SERVER_CONNECT
    session = requests.session()
    session.mount('https://', CustomHttpAdapter(ctx))
    return session


def request_func(url, method='GET', params=None, headers=None, json=None, data=None, timeout=3, http=False, body=None, verify=True, need_400=False, to_dict=True, try_count=5):
    response = None
    headers = {"Content-Type": "application/json"} if headers is None else headers
    for _ in range(try_count):
        try:
            if http:
                http = urllib3.PoolManager()
                if method == 'GET':
                    response = get_legacy_session().get(url)
                    return response.json()
                elif body:
                    response = http.request('POST', url, headers=headers, body=body)
                    return json_func.loads(response.data)
                else:
                    response = http.request('POST', url, headers=headers, body=body)
                    return BeautifulSoup(response.data, 'lxml')
            else:
                if method == 'GET':
                    if params:
                        response = requests.get(url=url, params=params, headers=headers, timeout=timeout, verify=False)
                    elif data:
                        response = requests.get(url=url, data=params, headers=headers, timeout=timeout, verify=False)
                    else:
                        response = requests.get(url=url, timeout=timeout, headers=headers, verify=False)
                elif method == 'POST':
                    if params:
                        response = requests.post(url=url, params=params, headers=headers, timeout=timeout)
                    elif json:
                        response = requests.post(url=url, json=json, headers=headers, timeout=timeout)
                    elif data:
                        response = requests.post(url=url, data=data, headers=headers, timeout=timeout, verify=verify)
                    elif body:
                        response = requests.post(url=url, json=body, headers=headers, timeout=timeout, verify=verify)
                    else:
                        response = requests.post(url=url, headers=headers, timeout=timeout, verify=False)
                if response:
                    if to_dict:
                        try:
                            response = response.json()
                        except JSONDecodeError:
                            response = xmltodict.parse(response.content)
                    return response
                elif need_400 and response.status_code == 400:
                    return response.json()
                elif _ == 3:
                    sleep(5)
        except ReadTimeout:
            print(1)
        except ConnectTimeout:
            print(2)
        except:
            print(traceback.format_exc())
            print(3)
    # logger.error(f'Request return zero! {url}')
