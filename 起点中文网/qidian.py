# -*- coding: utf-8 -*-
# @Time    : 2020/3/18 21:12
# @Author  : Key-lei
# @File    : qidian.py


# -*- coding: utf-8 -*-
# @Time    : 2020/3/12 12:34
# @Author  : Key-lei
# @File    : 01.py

# 1.下载字体文件
# 2.找出映射规则
# 3.替换
import requests
import re
from fontTools.ttLib import TTFont
import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gb18030')


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
}

# 映射规则是不变了
eng_2_num = {
    'period': ".", 'two': '2', 'zero': '0', 'five': '5', 'nine': "9", 'seven': '7', 'one': '1', 'three': '3',
    'six': '6', 'four': '4', 'eight': '8'
}


def get_response(url):
    response = requests.get(url, headers=headers)
    return response


def get_font(html):
    """下载字体文件保存到本地"""
    # 获取font相关信息
    font_link = re.findall("format\('eot'\); src: url\('(.*?)'\) format\('woff'\)", html)
    print(font_link)
    font_link = font_link[0]
    response_woff = requests.get(font_link)
    filename = font_link.split('/')[-1]
    with open(filename, "wb") as f:
        f.write(response_woff.content)
    return filename


def get_map_url(font_name):
    # 把字体文件读取为python能理解的对象
    base_font = TTFont(font_name)
    base_font.saveXML('font.xml')
    # 获取映射规则
    map_list = base_font.getBestCmap()
    print(map_list)
    for key in map_list.keys():
        map_list[key] = eng_2_num[map_list[key]]
    return map_list


if __name__ == '__main__':
    # 1. 下载html
    response = get_response('https://book.qidian.com/info/1016965825')
    old_html = response.text
    with open('替换之前的.html', mode='w', encoding='utf-8') as f:
        f.write(old_html)
    # 2. 下载字体
    font_name = get_font(response.text)
    # 3. 获取字体的映射规则
    map_list = get_map_url(font_name)
    print(map_list)
    # 4. 用映射规则替换旧文本
    new_html = old_html
    for key, value in map_list.items():
        # &#100177;
        new_html = new_html.replace('&#' + str(key) + ';', value)
        print(key, value)
    with open('替换之后的.html', mode='w', encoding='utf-8') as f:
        f.write(new_html)

