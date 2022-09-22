# -*- coding: utf-8 -*-
"""papago.py

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Qj-N3eVuuljgHPcnukT0gr7UtyupXHQp
"""

import os
import sys
import time
import requests

client_id = "Y5XGw8WTFwB6v1Tt4iRp"
client_secret = "vWIsd2WL9P"
time0 = time.time()   

def get_translate(text):
    a='error'
    b = "error"
    if text.encode().isalpha():
        a = 'en'
        b = 'ko'
    else:
        a = 'ko'
        b = 'en'
    data = {'text' : text,#inputtext
            'source' : a,#input lan
            'target': b}#output lan

    url = "https://openapi.naver.com/v1/papago/n2mt"

    header = {"X-Naver-Client-Id":client_id,
              "X-Naver-Client-Secret":client_secret}

    response = requests.post(url, headers=header, data= data)
    rescode = response.status_code

    if(rescode==200):
        t_data = response.json()
        return str.lower(response.json()['message']['result']['translatedText'])
    else:
        print("Error Code:" , rescode)
        return 0
