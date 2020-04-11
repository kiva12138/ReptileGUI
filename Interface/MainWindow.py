import tkinter as tk
from tkinter import ttk

import Interface.StaticString as StaticString
import Interface.Alert as Alert
import Thread.SearchThread as SearchThread


class MainWindow:

    def __init__(self):
        self.sourceList = []
        self.classList = []

        self.window = tk.Tk()
        self.window.title(StaticString.title)
        # self.window.geometry('820x600')
        self.window.resizable(0, 0)

        self.labelSite = tk.Label(self.window, text=StaticString.textSiteSelect, font=(None, 12))
        self.listBoxSite = ttk.Combobox(self.window)

        self.labelClass = tk.Label(self.window, text=StaticString.textClassSelect, font=(None, 12))
        self.listBoxClass = ttk.Combobox(self.window)
        self.listBoxClass.bind('<<ComboboxSelected>>', self.handleClassChange)

        self.labelSearch = tk.Label(self.window, text=StaticString.textSearchHint, font=(None, 12))
        self.searchInput = tk.Entry(self.window, show=None, font=(None, 12))
        self.searchButton = tk.Button(self.window, text=StaticString.textSearchButton, font=(None, 12),
                                      command=self.handleSearch)

        self.labelLength = tk.Label(self.window, text="暂未进行搜索", font=(None, 12))
        self.labelDownload = tk.Label(self.window, text="暂未下载", font=(None, 12))

        self.donateButton = tk.Button(self.window, text=StaticString.textDonateButton, font=(None, 12),
                                      command=self.handleDonate)

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
        self.labelLength.grid(row=2, column=6, rowspan=2, columnspan=2, sticky=tk.E + tk.N + tk.S + tk.W, padx=5,
                              pady=10)
        self.labelDownload.grid(row=5, column=0, rowspan=1, columnspan=11, sticky=tk.E + tk.N + tk.S + tk.W)
        self.donateButton.grid(row=2, column=9, rowspan=2, columnspan=2, sticky=tk.E + tk.N + tk.S, padx=5, pady=10)

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
            Alert.alert(message='请先输入搜索内容')
        elif self.listBoxSite.get().strip() is "":
            Alert.alert(message='请先选择搜索的网站')
        else:
            self.window.title(self.searchInput.get().strip() + '-' + StaticString.title)
            self.pictureCanvas.delete(tk.ALL)
            threadSearch = SearchThread.SearchThread(self.listBoxSite.get().strip(), self.searchInput.get().strip(),
                                                     self.pictureCanvas, self.pictureFrame, self.labelLength,
                                                     self.labelDownload)
            threadSearch.setDaemon(True)
            threadSearch.start()

    def handleClassChange(self):
        print(self.listBoxClass.get().strip())
        Alert.alert(StaticString.textNotOpen)

    def handleDonate(self):
        top = tk.Toplevel(self.window)
        top.resizable(0, 0)
        top.title('捐赠')
        tk.Label(top, text="制作不易，请多多支持", font=(None, 12))\
            .grid(row=0, column=0, rowspan=2, columnspan=5, sticky=tk.W + tk.E + tk.N + tk.S, padx=5, pady=10)
        tk.Label(top, text="如果你爽了，不妨请我喝杯咖啡", font=(None, 12))\
            .grid(row=2, column=0, rowspan=2, columnspan=5, sticky=tk.W + tk.E + tk.N + tk.S, padx=5, pady=10)

        photo = tk.PhotoImage(file="StaticPictures/AliPay3.gif")
        theLabel = tk.Label(top, image=photo)
        theLabel.grid(row=4, column=0, rowspan=5, columnspan=5, sticky=tk.W + tk.E + tk.N + tk.S, padx=5, pady=10)
        top.mainloop()
