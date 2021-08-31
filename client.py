# -*- coding: utf-8 -*-
import base64
import requests


class Client:
    def __init__(self, email, key):
        self.email = email
        self.key = key
        self.base_url = "https://fofa.so"
        self.search_api_url = "/api/v1/search/all"
        self.login_api_url = "/api/v1/info/my"
        self.get_userinfo()  # check email and key

    def get_userinfo(self):
        api_full_url = "%s%s" % (self.base_url, self.login_api_url)
        param = {"email": self.email, "key": self.key}
        res = self.__http_get(api_full_url, param)
        return res

    def get_data(self, query_str, page=1, fields=""):
        res = self.get_json_data(query_str, page, fields)
        return res

    def get_json_data(self, query_str, page=1, fields=""):
        api_full_url = "%s%s" % (self.base_url, self.search_api_url)
        param = {"qbase64": base64.b64encode(query_str.encode('utf-8')).decode('utf-8'), "email": self.email,
                 "key": self.key, "page": str(page),
                 "fields": fields}
        res = self.__http_get(api_full_url, param)
        return res

    def __http_get(self, url, param):
        param = param
        url = url + "?"

        for keys in param.keys():
            url += keys + "=" + param[keys] + "&"

        url = url[:-1]

        try:
            req = requests.get(url=url)
            if "errmsg" in req.json():
                raise RuntimeError(req.json())
        except Exception as e:
            raise e
        return req.json()
