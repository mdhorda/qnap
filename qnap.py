import json
import logging
import re
import requests
import xml.etree.ElementTree as ET

from get_sid import ezEncode
from utils import jsonprint

class Qnap():
    def __init__(self, host, user, passwd, port='8080'):
        self.host = host
        self.port = port
        self.sid = None
        self.logged_in = self.login(user, passwd)

    def login(self, user, passwd):
        login_endpoint = self.endpoint(
            'authLogin.cgi',
            params={
                'user' : user.replace('\\', '+'),
                'pwd' : ezEncode(passwd)
            }
        )
        xml_response = self.req(login_endpoint, is_xml=True)
        if xml_response is not None:
            xml_root = ET.fromstring(xml_response)
            if xml_root is not None:
                auth_passed = xml_root.find('authPassed').text
                if auth_passed == '1':
                    self.sid = xml_root.find('authSid').text
                    return True
        return False

    def base_endpoint(self, cgi='filemanager/utilRequest.cgi'):
        ret = 'http://' + self.host + ':' + self.port + '/cgi-bin/' + cgi
        return ret

    def endpoint(self, cgi='filemanager/utilRequest.cgi', func=None, params={}):
        ret = self.base_endpoint(cgi) + '?'

        if func:
            ret = self.add_param(ret, 'func', func)

        if self.sid:
            ret = self.add_param(ret, 'sid', self.sid)

        for key, value in params.items():
            ret = self.add_param(ret, key, str(value))

        return ret

    def req(self, endpoint, is_xml=False):
        logging.info('GET: ' + endpoint)
        try:
            r = requests.get(endpoint)
            return self.get_response_data(r, is_xml)
        except:
            logging.error('GET error: ' + endpoint)
            return None

    def req_binary(self, endpoint):
        logging.info('GET: ' + endpoint)
        try:
            r = requests.get(endpoint)
        except:
            logging.error('GET error: ' + endpoint)
            return None
        if self.is_response_binary(r):
            return r.content
        self.get_response_data(r)
        return None

    def req_post(self, endpoint, files):
        logging.info('url: ' + endpoint)
        try:
            r = requests.post(endpoint, files=files)
        except:
            logging.error('POST error: ' + endpoint)
            return None
        return self.get_response_data(r)

    def get_response_data(self, response, is_xml=False):
        if response.status_code != 200:
            logging.error('http status: ' + str(response.status_code))

        if is_xml:
            return response.text.strip()

        try:
            response_text = response.text.strip()
            # Some responses contain extra content-type header
            response_text = response_text.strip('Content-type: text/html; charset="UTF-8"')
            # Get only first line of output (some responses contain same JSON on 2 different lines)
            match = re.match('.*', response_text)
            if match is not None:
                response_text = match.group(0)
            response_json = json.loads(response_text)
        except:
            return response.content

        return response_json

    def is_response_binary(self, response):
        return 'text/plain' not in response.headers['content-type']

    def add_param(self, base_url, param, value):
        ret_value = base_url
        if not base_url.endswith('?'):
            ret_value += '&'
        return ret_value + param + '=' + value