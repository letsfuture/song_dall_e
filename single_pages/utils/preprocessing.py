# -*- coding: utf-8 -*-
"""preprocessing.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1SSrjWaoPc3nSlXRcpQ044-656MOcQRQx
"""

# pip install soynlp

# pip install pykospacing

import soynlp
from soynlp.normalizer import *
# from pykospacing import Spacing # 코랩에서만 실행됨
import pandas as pd
import re

def __init__(self, lyrics):
    '''초기화'''
    self.lyrics = lyrics

def text_preprocessing(lyrics):
# 개행문자를 마침표(.)로 변환
    result = re.sub('\n', '. ', str(lyrics)) # 마침표 뒤에 띄어쓰기해서 교체
    result2 = result.replace(' .','')  # ' .' 없애기
    result3 = re.sub("[^’A-Za-z0-9가-힣'.]", ' ', str(result2))    # 제2외국어 및 특수문자 제거(',. 제외)

    result4 = result3.lower()                                    # 대문자를 소문자로
    #    result3 = removeDuplicates(result2)                         # 인접 중복 문자 제거
    result5 = repeat_normalize(result4, num_repeats=1) # 아아아 ---> 아
    # print(result5)
    # kpop, pop = [], []
    new_lyrics = isEnglishOrKorean(result5)
    if new_lyrics == '한국어':
        # 번역기 함수 연결
        final = result5 # 번역 돌리고 나서 변수 다르게 해줘야 함
    else:
        final = result5
    return final

# 문자열에서 인접한 중복 문자를 제거하는 기능
def removeDuplicates(s):
    chars = []
    prev = None

    if prev != s:
        chars.append(s)
        prev = s

    return ''.join(chars)

# 한국어인지 영어인지 판별하는 함수
def isEnglishOrKorean(input_s):
    k_count = 0
    e_count = 0
    for c in str(input_s):
        if ord('가') <= ord(c) <= ord('힣'): # ord ---> 하나의 문자를 인자로 받고 해당 문자에 해당하는 유니코드 정수를 반환
            k_count+=1
        elif ord('a') <= ord(c.lower()) <= ord('z'):
            e_count+=1
    return "한국어" if k_count>1 else "영어" # 한국어가 하나라도 있으면 한국어

