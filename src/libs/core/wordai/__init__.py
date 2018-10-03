"""
WordAI
"""

import json, re, urllib, requests

from .constants import Quality
from flask import current_app

class WordAI(object):
    """WordAI class
    """
    URL = 'http://wordai.com/users/turing-api.php'
    ACCOUNT_URL = 'http://wordai.com/users/account-api.php'
    DEFAULT_PARAMS = {
        "quality": Quality.reqular,
        "output": "json"
    }

    def __init__(self, **kwargs):
        """Initializes WordAI API object
        """
        self._username = kwargs.get('username', current_app.config.get('WORDAI_API_EMAIL', None))
        self._password = kwargs.get('password', current_app.config.get('WORDAI_API_PASSWORD', None))
        self._hash = kwargs.get('hash', current_app.config.get('WORDAI_API_KEY', None))

    def _check_auth(self):
        return self._username is not None and (self._password is not None or self._hash is not None)

    def _stripslashes(self, s):
        return re.sub(r'\\', '', s)

    def set_auth(self, **kwargs):
        self._username = kwargs.get('username', None)
        self._password = kwargs.get('password', None)
        self._hash = kwargs.get('hash', None)

    def _send_request(self, url, text=None, params=None):
        """ Invoke Word Ai API with given parameters and return its response.
        :param params: parameters to pass along with the request
        :type params: dictionary
        :return: API's response
        :rtype: dict
        """
        if params is not None:
            for k, v in params.items():
                params[k] = v.encode("utf-8")
        else:
            params = {}

        params['email'] = self._username

        if self._password:
            params['pass'] = self._password

        if self._hash:
            params['hash'] = self._hash

        if text is not None:
            params['s'] = self._stripslashes(text)


        try:
            response = requests.post(url, data=params)
        except Exception as e:
            print(str(e))

        result = response.content.decode('utf-8')
        

        try:
            json_data = json.loads(result)
        except ValueError as e:
            print(str(e))

        if json_data['status'] == "Success":
            return json_data
        elif json_data['status'] == "Failure":
            if json_data['error'].startswith("Error Authenticating."):
                print(json_data['error'])
            else:
                print(json_data['error'])
        else:
            print(json_data)
        
    
    def account_info(self):
        """Return account info.
        :return: account info
        :rtype: dict
        :Example: {u'Standard Limit': 2500000, u'Status': u'Success',
            u'Turing Limit': 150000, u'Standard Usage': 0, u'Turing Usage': 0}
        """
        return self._send_request(self.ACCOUNT_URL)

    def text_with_spintax(self, text, params=None):
        """ Return processed spun text with spintax.
        :param text: original text that needs to be changed
        :type text: string
        :param params: parameters to pass along with the request
        :type params: dictionary
        :return: processed text in spintax format
        :rtype: string
        """

        if not params:
            params = self.DEFAULT_PARAMS.copy()

        params['returnspin'] = 'false'

        result = self._send_request(
            url=self.URL,
            text=text,
            params=params
        )['text']

        if result is None:
            return ""
        else:
            result = re.sub("<p>", "", result)
            return re.sub("</p>", "", result).strip()

    def unique_variation(self, text, params=None):
        """ Return a unique variation of the given text.
        :param text: original text that needs to be changed
        :type text: string
        :param params: parameters to pass along with the request
        :type params: dictionary
        :return: processed text
        :rtype: string
        """

        if not params:
            params = self.DEFAULT_PARAMS.copy()

        params['returnspin'] = 'true'

        result = self._send_request(
            url=self.URL,
            text=text,
            params=params
        )['text']

        if result is None:
            return ""
        else:
            result = re.sub("<p>", "", result)
            return re.sub("</p>", "", result).strip()

if __name__ == "__main__":
    print("Something went wrong...")
