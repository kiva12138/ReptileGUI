import tkinter as tk
import tkinter.messagebox
from io import BytesIO
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter.filedialog import askdirectory

import requests
from lxml import etree
import time
import os

title = "健康生活"
textSiteSelect = "网站选择:"
textClassSelect = "图片分类:"
textSearchHint = "精准搜索:"
textSearchButton = " 查找 "
textDonateButton = "点开看看？"
textNotOpen = "该功能暂未开放"
textGetFailure = "获取失败"
sleepTime = 1


class MainWindow:

    def __init__(self):
        self.sourceList = []
        self.classList = []

        self.window = tk.Tk()
        self.window.title(title)
        # self.window.geometry('820x600')
        # self.window.resizable(0, 0)

        self.labelSite = tk.Label(self.window, text=textSiteSelect, font=(None, 12))
        self.listBoxSite = ttk.Combobox(self.window)

        self.labelClass = tk.Label(self.window, text=textClassSelect, font=(None, 12))
        self.listBoxClass = ttk.Combobox(self.window)
        self.listBoxClass.bind('<<ComboboxSelected>>', self.handleClassChange)

        self.labelSearch = tk.Label(self.window, text=textSearchHint, font=(None, 12))
        self.searchInput = tk.Entry(self.window, show=None, font=(None, 12))
        self.searchButton = tk.Button(self.window, text=textSearchButton, font=(None, 12), command=self.handleSearch)

        self.labelLength = tk.Label(self.window, text="暂未进行搜索", font=(None, 12))

        self.donateButton = tk.Button(self.window, text=textDonateButton, font=(None, 12), command=self.handleDonate)

        self.labelSite.grid(row=0, column=0, rowspan=2, columnspan=2, sticky=tk.E + tk.N + tk.S, padx=5, pady=10)
        self.listBoxSite.grid(row=0, column=2, rowspan=2, columnspan=3, sticky=tk.W + tk.E + tk.N + tk.S, padx=5,
                              pady=10)
        self.labelClass.grid(row=0, column=5, rowspan=2, columnspan=2, sticky=tk.E + tk.N + tk.S, padx=5, pady=10)
        self.listBoxClass.grid(row=0, column=7, rowspan=2, columnspan=3, sticky=tk.W + tk.E + tk.N + tk.S, padx=5,
                               pady=10)

        self.labelSearch.grid(row=2, column=0, rowspan=2, columnspan=2, sticky=tk.E + tk.N + tk.S, padx=5, pady=10)
        self.searchInput.grid(row=2, column=2, rowspan=2, columnspan=3, sticky=tk.W + tk.E + tk.N + tk.S, padx=5,
                              pady=10)
        self.searchButton.grid(row=2, column=5, rowspan=2, columnspan=2, sticky=tk.W + tk.N + tk.S, padx=5, pady=10)
        self.labelLength.grid(row=2, column=6, rowspan=2, columnspan=3, sticky=tk.E + tk.N + tk.S + tk.W, padx=5, pady=10)
        self.donateButton.grid(row=2, column=7, rowspan=2, columnspan=3, sticky=tk.E + tk.N + tk.S, padx=5, pady=10)

        # 主要数据展示区
        self.pictureFrame = tk.Frame(self.window, width=800, height=500, background='white')
        self.pictureCanvas = tk.Canvas(self.pictureFrame, width=800, height=500, background='white')
        self.pictureFrame.pack_propagate(0)
        self.pictureCanvas.pack_propagate(0)

        self.pictureScrollH = tk.Scrollbar(self.pictureFrame, orient=tk.HORIZONTAL, command=self.pictureCanvas.xview)
        self.pictureScrollV = tk.Scrollbar(self.pictureFrame, orient=tk.VERTICAL, command=self.pictureCanvas.yview)

        self.pictureCanvas.config(xscrollcommand=self.pictureScrollH.set, yscrollcommand=self.pictureScrollV.set)

        self.pictureScrollH.pack(side=tk.BOTTOM, fill=tk.X)
        self.pictureScrollV.pack(side=tk.RIGHT, fill=tk.Y)

        self.pictureFrame.grid(row=4, column=0, columnspan=11, padx=10, pady=10, sticky=tk.W + tk.N + tk.S)
        self.pictureCanvas.pack(side=tk.TOP, expand=True, fill=tk.BOTH)

    def getClassAndSite(self):
        self.sourceList = ["美图录"]
        self.listBoxSite['value'] = self.sourceList
        self.listBoxSite.current(0)

        # 如果获取失败，那么需要禁用该多选框，或者选项设置为“获取失败”
        self.classList = ["日本", "国内", "动漫", "其他"]
        self.listBoxClass['value'] = self.classList

    def handleSearch(self):
        if self.searchInput.get().strip() is "":
            self.alert(message='请先输入搜索内容')
        elif self.listBoxSite.get().strip() is "":
            self.alert(message='请先选择搜索的网站')
        else:
            self.window.title(self.searchInput.get().strip() + '-' + title)
            self.pictureCanvas.delete(tk.ALL)
            if self.listBoxSite.get().strip() == '美图录':
                self.searchFromMeiTuLu(self.searchInput.get().strip())

    def handleClassChange(self, event):
        # tk.messagebox.showinfo(title='WTF？', message=self.classList[self.listBoxClass.current()])
        self.alert(textNotOpen)

    def handleDonate(self):
        top = tk.Toplevel()
        top.resizable(0, 0)
        top.title('捐赠')
        lable1 = tk.Label(top, text="制作不易，请多多支持", font=(None, 12))
        lable1.grid(row=0, column=0, rowspan=2, columnspan=5, sticky=tk.W + tk.E + tk.N + tk.S, padx=5, pady=10)
        lable2 = tk.Label(top, text="如果你爽了，不妨请我喝杯咖啡", font=(None, 12))
        lable2.grid(row=2, column=0, rowspan=2, columnspan=5, sticky=tk.W + tk.E + tk.N + tk.S, padx=5, pady=10)

        photo = tk.PhotoImage(file="AliPay3.gif")
        theLabel = tk.Label(top, image=photo)
        theLabel.grid(row=4, column=0, rowspan=5, columnspan=5, sticky=tk.W + tk.E + tk.N + tk.S, padx=5, pady=10)
        top.mainloop()

    def writeToFile(self, content, number, context_name, path):
        if not os.path.isdir(str(path) + '\\' + str(context_name)):
            os.mkdir(str(path) + '\\' + str(context_name))
        with open(str(path) + '\\' + str(context_name) + '\\' + str(number) + '.jpg', 'wb') as f:
            try:
                f.write(content)
            except:
                print('淦!鬼知道为什么文件写入失败！可能搜的东西有问题或者网站改了。')

    def resizeImage(self, w_box, h_box, pil_image):
        w, h = pil_image.size
        f1 = 1.0 * w_box / w
        f2 = 1.0 * h_box / h
        factor = min([f1, f2])
        width = int(w * factor)
        height = int(h * factor)
        return pil_image.resize((width, height), Image.ANTIALIAS)

    def searchFromMeiTuLu(self, input_content):
        search_url = 'https://www.meitulu.com/search/'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/27.0.1453.94 '
                          'Safari/537.36 '}
        search_html = requests.get(search_url + str(input_content), headers=headers)
        search_html.encoding = 'utf-8'
        search_selector = etree.HTML(search_html.text)
        dataList = search_selector.xpath('/html/body/div[2]/div[2]/ul/li')
        if len(dataList) == 0:
            self.alert("未发现任何结果")
        self.labelLength['text'] = '一共'+str(len(dataList))+'个图集'
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
            if len(picTitle) >= 16:
                picTitle = picTitle[:16] + '...'

            singleCollection = tk.Canvas(self.pictureCanvas, width=singleWidth, height=singleHeight, background="white")
            singleCollection.grid_propagate(0)
            self.pictureCanvas.create_window(column * 200, row * 350, anchor=tk.NW, window=singleCollection)
            img = Image.open(BytesIO(requests.get(picUrl, headers=headers).content))
            img_resized = self.resizeImage(singleWidth, singleHeight - 50, img)
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

            self.pictureCanvas.create_window(column * 200, row * 350, anchor=tk.NW, window=singleCollection)
            labelPhoto.bind("<Button-1>",
                            lambda event: self.handleDownloadFromMeitulu(linkUrl=linkUrl, picTitle=picTitle))
            column += 1
            if column == 4:
                column = 0
                row += 1
        if len(dataList) % 4 == 0:
            row -= 1
        self.pictureCanvas.pack()
        self.pictureFrame.grid()
        self.pictureCanvas.config(scrollregion=(0, 0, 800, (row + 1) * 350))
        self.pictureFrame.mainloop()

    def handleDownloadFromMeitulu(self, linkUrl, picTitle):
        path = askdirectory()
        site_prefix = 'https://www.meitulu.com'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/27.0.1453.94 '
                          'Safari/537.36 '}
        last_page_url = ''
        current_page_url = linkUrl
        number = 0
        while current_page_url != last_page_url:
            time.sleep(sleepTime)
            content_html = requests.get(current_page_url, headers=headers)
            content_html.encoding = 'utf-8'
            content_selector = etree.HTML(content_html.text)
            content_dataList = content_selector.xpath('/html/body/div[4]/center/img')
            for img_data in content_dataList:
                time.sleep(sleepTime / 2)
                img_src = img_data.xpath('@src')[0]
                img = requests.get(img_src, headers=headers)
                self.writeToFile(img.content, number, picTitle, path)
                number += 1
            last_page_url = current_page_url
            current_page_url = site_prefix + content_selector.xpath('/html/body/center/div/a')[-1].xpath('@href')[0]

    def alert(self, message):
        tk.messagebox.showinfo(title='WTF？', message=message)


def main():
    window = MainWindow()
    window.getClassAndSite()
    tk.mainloop()


if __name__ == '__main__':
    main()
