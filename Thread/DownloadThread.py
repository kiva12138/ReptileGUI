from tkinter.filedialog import askdirectory
import time
import threading
import requests
from lxml import etree
from Interface import StaticString
from UtilOperations import WriteToFile


class DownloadThread(threading.Thread):
    def __init__(self, site, linkUrl, picTitle, labelDownload):
        super(DownloadThread, self).__init__()
        self.site = site
        self.linkUrl = linkUrl
        self.picTitle = picTitle
        self.labelDownload = labelDownload

    def handleDownloadFromMeitulu(self):
        path = askdirectory()
        if path == "":
            return
        site_prefix = 'https://www.meitulu.com'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/27.0.1453.94 '
                          'Safari/537.36 '}
        last_page_url = ''
        current_page_url = self.linkUrl
        number = 0
        while current_page_url != last_page_url:
            time.sleep(StaticString.sleepTime)
            content_html = requests.get(current_page_url, headers=headers)
            content_html.encoding = 'utf-8'
            content_selector = etree.HTML(content_html.text)
            content_dataList = content_selector.xpath('/html/body/div[4]/center/img')
            for img_data in content_dataList:
                time.sleep(StaticString.sleepTime / 2)
                img_src = img_data.xpath('@src')[0]
                img = requests.get(img_src, headers=headers)
                WriteToFile.writeToFile(img.content, number, self.picTitle, path)
                number += 1
                self.labelDownload['text'] = '正在下载第' + str(number) + '张图片'
            last_page_url = current_page_url
            current_page_url = site_prefix + content_selector.xpath('/html/body/center/div/a')[-1].xpath('@href')[0]
        self.labelDownload['text'] = '下载完成'

    def run(self) -> None:
        if self.site == '美图录':
            self.handleDownloadFromMeitulu()
