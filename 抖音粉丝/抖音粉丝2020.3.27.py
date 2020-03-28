# -*- coding: utf-8 -*-
# @Time    : 2020/3/27 23:43
# @Author  : Key-lei
# @File    : 抖音粉丝2020.3.27.py
import requests
from fontTools.ttLib import TTFont
from parsel import Selector

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
}
# 分析得到得字体文件
url = 'https://s3.pstatp.com/ies/resource/falcon/douyin_falcon/static/font/iconfont_9eb9a50.woff'

# 这些映射关系是再  当前文件夹下xml中找到得
real_2_map = {
    'x': '',
    'num_': '1', 'num_1': '0', 'num_2': '3', 'num_3': '2', 'num_4': '4', 'num_5': '5', 'num_6': '6', 'num_7': '9',
    'num_8': '7',
    'num_9': '8'
}

two_2_sixteenn = {
    "&#xe602": "num_",
    "&#xe603": "num_1",
    "&#xe604": "num_2",
    "&#xe605": "num_3",
    "&#xe606": "num_4",
    "&#xe607": "num_5",
    "&#xe608": "num_6",
    "&#xe609": "num_7",
    "&#xe60a": "num_8",
    "&#xe60b": "num_9",
    "&#xe60c": "num_4",
    "&#xe60d": "num_1",
    "&#xe60e": "num_",
    "&#xe60f": "num_5",
    "&#xe610": "num_3",
    "&#xe611": "num_2",
    "&#xe612": "num_6",
    "&#xe613": "num_8",
    "&#xe614": "num_9",
    "&#xe615": "num_7",
    "&#xe616": "num_1",
    "&#xe617": "num_3",
    "&#xe618": "num_",
    "&#xe619": "num_4",
    "&#xe61a": "num_2",
    "&#xe61b": "num_5",
    "&#xe61c": "num_8",
    "&#xe61d": "num_9",
    "&#xe61e": "num_7",
    "&#xe61f": "num_6",
}


# 拿到字体文件
def get_font(url):
    response_woff = requests.get(url)
    filename = url.split('/')[-1]
    with open(filename, "wb") as f:
        f.write(response_woff.content)
    return filename


def get_map_url(font_name):
    # 把字体文件读取为python能理解的对象
    base_font = TTFont(font_name)
    base_font.saveXML('font.xml')
    # 获取映射规则
    for key in two_2_sixteenn.keys():
        two_2_sixteenn[key] = real_2_map[two_2_sixteenn[key]]
    return two_2_sixteenn


# 格式化输出
def format_str(character):
    character = [x.replace(" ", '') for x in character]
    character = "".join(character)
    character = character.replace(";", '')
    return character


if __name__ == '__main__':
    font_name = get_font(url)
    two_2_sixteenn = get_map_url(font_name)
    # 得到请求页面
    response = requests.get(
        'https://v.douyin.com/77hwgS/',
        headers=headers)
    with open('替换之前的.html', mode='w', encoding='utf-8') as f:
        f.write(response.text)
    new_html = response.text
    # 替换html中得字体
    for key, value in two_2_sixteenn.items():
        new_html = new_html.replace(str(key).lower(), value)
    with open('替换之后的.html', mode='w', encoding='utf-8') as f:
        f.write(new_html)
    # 提取粉丝数量
    selector = Selector(new_html)
    fans_num = format_str(selector.xpath('//span[@class="follower block"]//span[@class="num"]//text()').getall())
    star_num = format_str(selector.xpath('//span[@class="focus block"]//span[@class="num"]//text()').getall())
    like_num = format_str(selector.xpath('//span[@class="liked-num block"]//span[@class="num"]//text()').getall()
    print('粉丝的数量:', fans_num)
    print('关注的数量:', star_num)
    print('赞的数量:', like_num)
