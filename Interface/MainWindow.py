import tkinter as tk
from importlib import reload
from tkinter import ttk
import os
from shutil import copyfile

import Interface.StaticString as StaticString
import Interface.Alert as Alert
import Thread.SearchThread as SearchThread
import CurrentScript.CurrentSite as CurrentSite
import Thread.ClassGetThread as ClassGetThread


class MainWindow:

    def __init__(self):
        self.sourceList = []
        self.classList = []
        self.currentScript = None

        self.window = tk.Tk()
        self.window.title(StaticString.title)
        # self.window.geometry('820x600')
        self.window.resizable(0, 0)

        self.labelSite = tk.Label(self.window, text=StaticString.textSiteSelect, font=(None, 12))
        self.listBoxSite = ttk.Combobox(self.window)
        self.listBoxSite.bind('<<ComboboxSelected>>', self.handleSiteChange)

        self.labelClass = tk.Label(self.window, text=StaticString.textClassSelect, font=(None, 12))
        self.listBoxClass = ttk.Combobox(self.window)
        self.listBoxClass.bind('<<ComboboxSelected>>', self.handleClassChange)

        self.labelSearch = tk.Label(self.window, text=StaticString.textSearchHint, font=(None, 12))
        self.searchInput = tk.Entry(self.window, show=None, font=(None, 12))
        self.searchButton = tk.Button(self.window, text=StaticString.textSearchButton, font=(None, 12),
                                      command=self.handleSearch)

        self.labelLength = tk.Label(self.window, text=StaticString.textNotSearch, font=(None, 12))
        self.labelDownload = tk.Label(self.window, text=StaticString.textNotDownload, font=(None, 12))

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

        Alert.alert(message=StaticString.textStart)

    # 读取文件
    def getSite(self):
        self.sourceList.clear()
        path = "./Scripts"
        files = os.listdir(path)
        for file in files:
            if not os.path.isdir(file):
                fileFormat = os.path.splitext(file)[-1]
                fileName = os.path.splitext(file)[0]
                if fileFormat != StaticString.scriptFileFormat:
                    continue
                self.sourceList.append(fileName)
        self.listBoxSite['value'] = self.sourceList

    # 文件改变
    def handleSiteChange(self, event):
        self.currentScript = self.listBoxSite.get().strip()
        copyfile('./Scripts/' + self.listBoxSite.get().strip() + StaticString.scriptFileFormat,
                 './CurrentScript/' + 'CurrentSite.py')
        self.getClassAndSearch()

    # 更新图片
    def handleClassChange(self, event):
        if self.listBoxSite.get().strip() is "":
            Alert.alert(message=StaticString.textSearchEmptySite)
        else:
            self.window.title(self.searchInput.get().strip() + '-' + StaticString.title)
            self.pictureCanvas.delete(tk.ALL)
            threadClassGet = ClassGetThread.ClassGetThread(self.listBoxClass.get().strip(),
                                                           self.pictureCanvas, self.pictureFrame, self.labelDownload)
            threadClassGet.setDaemon(True)
            threadClassGet.start()

    # 获取分类与搜索的有效性
    def getClassAndSearch(self):
        reload(CurrentSite)
        if CurrentSite.isSearchable():
            self.searchButton.config(state='active')
        else:
            self.searchButton.config(state='disabled')
        self.classList = CurrentSite.getClasses()
        self.listBoxClass['value'] = self.classList
        if len(self.classList) == 0:
            self.listBoxClass.config(state='disabled')
        else:
            self.listBoxClass.config(state='active')

    def handleSearch(self):
        if self.searchInput.get().strip() is "":
            Alert.alert(message=StaticString.textSearchEmptyInput)
        elif self.listBoxSite.get().strip() is "":
            Alert.alert(message=StaticString.textSearchEmptySite)
        else:
            self.window.title(self.searchInput.get().strip() + '-' + StaticString.title)
            self.pictureCanvas.delete(tk.ALL)
            threadSearch = SearchThread.SearchThread(self.searchInput.get().strip(),
                                                     self.pictureCanvas, self.pictureFrame, self.labelLength,
                                                     self.labelDownload)
            threadSearch.setDaemon(True)
            threadSearch.start()

    def handleDonate(self):
        top = tk.Toplevel(self.window)
        top.resizable(0, 0)
        top.title(StaticString.textDonate)
        tk.Label(top, text=StaticString.textDonate1, font=(None, 12)) \
            .grid(row=0, column=0, rowspan=2, columnspan=5, sticky=tk.W + tk.E + tk.N + tk.S, padx=5, pady=10)
        tk.Label(top, text=StaticString.textDonate2, font=(None, 12)) \
            .grid(row=2, column=0, rowspan=2, columnspan=5, sticky=tk.W + tk.E + tk.N + tk.S, padx=5, pady=10)

        photo = tk.PhotoImage(file="StaticPictures/AliPay3.gif")
        theLabel = tk.Label(top, image=photo)
        theLabel.grid(row=4, column=0, rowspan=5, columnspan=5, sticky=tk.W + tk.E + tk.N + tk.S, padx=5, pady=10)
        top.mainloop()
