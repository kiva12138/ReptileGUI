import threading
import requests
import tkinter as tk
from io import BytesIO
from PIL import Image, ImageTk
from lxml import etree

import Thread.DownloadThread as DownloadThread
import Interface.Alert as Alert
import UtilOperations.ImageOperation as ImageOperation
import Thread.StopThread as StopThread


class SearchThread(threading.Thread):
    def __init__(self, site, content, canvas, frame, labelLength, labelDownload):
        super(SearchThread, self).__init__()
        self.currentDownloadThread = None
        self.site = site
        self.content = content
        self.canvas = canvas
        self.frame = frame
        self.labelLength = labelLength
        self.labelDownload = labelDownload

    def stopDownload(self):
        if self.currentDownloadThread is not None and self.currentDownloadThread.is_alive():
            StopThread.stop_thread(self.currentDownloadThread)
            self.labelDownload['text'] = '下载完成'

    def handleDownloadFromMeitulu(self, linkUrl, picTitleReal):
        if self.currentDownloadThread is None or not self.currentDownloadThread.is_alive():
            self.labelDownload.bind("<Button-1>", lambda event: self.stopDownload())
            downloadThread = DownloadThread.DownloadThread(self.site, linkUrl, picTitleReal, self.labelDownload)
            downloadThread.setDaemon(True)
            downloadThread.start()
            self.currentDownloadThread = downloadThread
        else:
            Alert.alert('当前正在下载，请等待下载完成')

    def searchFromMeiTuLu(self):
        search_url = 'https://www.meitulu.com/search/'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/27.0.1453.94 '
                          'Safari/537.36 '}
        search_html = requests.get(search_url + str(self.content), headers=headers)
        search_html.encoding = 'utf-8'
        search_selector = etree.HTML(search_html.text)
        dataList = search_selector.xpath('/html/body/div[2]/div[2]/ul/li')
        if len(dataList) == 0:
            Alert.alert("未发现任何结果")
        self.labelLength['text'] = '一共' + str(len(dataList)) + '个图集'
        row = 0
        column = 0
        singleWidth = 200
        singleHeight = 350
        picturesData = []
        for data in dataList:
            picUrl = data.xpath('a/img/@src')[0]
            number = data.xpath('p[1]/text()')[0]
            picTitle = data.xpath('p[2]/a/text()')[0]
            linkUrl = data.xpath('a/@href')[0]
            picTitleReal = picTitle
            if len(picTitle) >= 16:
                picTitle = picTitle[:16] + '...'

            singleCollection = tk.Canvas(self.canvas, width=singleWidth, height=singleHeight, background="white")
            singleCollection.grid_propagate(0)
            self.canvas.create_window(column * 200, row * 350, anchor=tk.NW, window=singleCollection)
            img = Image.open(BytesIO(requests.get(picUrl, headers=headers).content))
            img_resized = ImageOperation.resizeImage(singleWidth, singleHeight - 50, img)
            photo = ImageTk.PhotoImage(img_resized)
            labelPhoto = tk.Label(singleCollection, image=photo)
            picturesData.append(photo)
            labelPhoto.grid(row=0, column=0, rowspan=3, columnspan=1, sticky=tk.W + tk.E + tk.N + tk.S, padx=5, pady=5)

            lableName = tk.Label(singleCollection, text=picTitle, font=(None, 12), background="white", width=10,
                                 height=1)
            lableName.grid(row=3, column=0, rowspan=1, columnspan=1, sticky=tk.W + tk.E + tk.N + tk.S, padx=5)
            lableNumber = tk.Label(singleCollection, text=number, font=(None, 12), background="white", width=10,
                                   height=1)
            lableNumber.grid(row=4, column=0, rowspan=1, columnspan=1, sticky=tk.W + tk.E + tk.N + tk.S, padx=5)

            self.canvas.create_window(column * 200, row * 350, anchor=tk.NW, window=singleCollection)
            labelPhoto.bind("<Button-1>",
                            lambda event, linkUrl1=linkUrl, picTitleReal1=picTitleReal:
                            self.handleDownloadFromMeitulu(linkUrl1, picTitleReal1))
            column += 1
            if column == 4:
                column = 0
                row += 1
        if len(dataList) % 4 == 0:
            row -= 1
        self.canvas.pack()
        self.frame.grid()
        self.canvas.config(scrollregion=(0, 0, 800, (row + 1) * 350))

    def run(self) -> None:
        if self.site == '美图录':
            self.searchFromMeiTuLu()