import requests
from lxml import etree

searchURL = 'https://www.meitulu.com/search/'
sitePrefix = 'https://www.meitulu.com'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/27.0.1453.94 '
                         'Safari/537.36 '}
classes = {'女神': 'https://www.meitulu.com/t/meishaonv/',
           '极品': 'https://www.meitulu.com/t/jipin/',
           '嫩模': 'https://www.meitulu.com/t/nenmo/',
           '网络红人': 'https://www.meitulu.com/t/wangluohongren/',
           '风俗娘': 'https://www.meitulu.com/t/fengsuniang/',
           '气质': 'https://www.meitulu.com/t/qizhi/',
           '尤物': 'https://www.meitulu.com/t/youwu/',
           '爆乳': 'https://www.meitulu.com/t/baoru/',
           '性感': 'https://www.meitulu.com/t/xinggan/',
           '诱惑': 'https://www.meitulu.com/t/youhuo/',
           '美胸': 'https://www.meitulu.com/t/meixiong/',
           '少妇': 'https://www.meitulu.com/t/shaofu/',
           '长腿': 'https://www.meitulu.com/t/changtui/',
           '萌妹子': 'https://www.meitulu.com/t/mengmeizi/',
           '萝莉': 'https://www.meitulu.com/t/luoli/',
           '可爱': 'https://www.meitulu.com/t/keai/',
           '户外': 'https://www.meitulu.com/t/huwai/',
           '比基尼': 'https://www.meitulu.com/t/bijini/',
           '青春': 'https://www.meitulu.com/t/qingchun/',
           '唯美': 'https://www.meitulu.com/t/weimei/',
           '清新': 'https://www.meitulu.com/t/qingxin/'}


def searchData(content):
    result = []
    search_url = searchURL
    search_html = requests.get(search_url + str(content), headers=headers)
    search_html.encoding = 'utf-8'
    search_selector = etree.HTML(search_html.text)
    dataList = search_selector.xpath('/html/body/div[2]/div[2]/ul/li')
    for data in dataList:
        singleResult = {'picUrl': data.xpath('a/img/@src')[0], 'number': data.xpath('p[1]/text()')[0],
                        'picTitleReal': data.xpath('p[2]/a/text()')[0], 'linkUrl': data.xpath('a/@href')[0]}
        if len(singleResult['picTitleReal']) >= 16:
            singleResult['picTitle'] = singleResult['picTitleReal'][:16] + '...'
        else:
            singleResult['picTitle'] = singleResult['picTitleReal']
        result.append(singleResult)
    return result


def downloadData(linkUrl):
    site_prefix = sitePrefix
    last_page_url = ''
    current_page_url = linkUrl
    while current_page_url != last_page_url:
        content_html = requests.get(current_page_url, headers=headers)
        content_html.encoding = 'utf-8'
        content_selector = etree.HTML(content_html.text)
        content_dataList = content_selector.xpath('/html/body/div[4]/center/img')
        for img_data in content_dataList:
            img_src = img_data.xpath('@src')[0]
            img = requests.get(img_src, headers=headers)
            yield img
        last_page_url = current_page_url
        current_page_url = site_prefix + content_selector.xpath('/html/body/center/div/a')[-1].xpath('@href')[0]


def searchFromClass(className):
    result = []
    class_url = classes[className]
    class_html = requests.get(class_url, headers=headers)
    class_html.encoding = 'utf-8'
    class_selector = etree.HTML(class_html.text)
    dataList = class_selector.xpath('/html/body/div[2]/div[4]/ul/li')
    for data in dataList:
        singleResult = {'picUrl': data.xpath('a/img/@src')[0], 'number': data.xpath('p[1]/text()')[0],
                        'picTitleReal': data.xpath('p[5]/a/text()')[0], 'linkUrl': data.xpath('a/@href')[0]}
        if len(singleResult['picTitleReal']) >= 16:
            singleResult['picTitle'] = singleResult['picTitleReal'][:16] + '...'
        else:
            singleResult['picTitle'] = singleResult['picTitleReal']
        result.append(singleResult)
    return result


def isSearchable():
    return True


def getClasses():
    return list(classes.keys())
