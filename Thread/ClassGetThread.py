import threading
import requests
import tkinter as tk
from io import BytesIO
from PIL import Image, ImageTk
import CurrentScript.CurrentSite as CurrentSite

import UtilOperations.ImageOperation as ImageOperation
import Thread.StopThread as StopThread
import Thread.DownloadThread as DownloadThread
import Interface.StaticString as StaticString
import Interface.Alert as Alert
import RequestNeededData.BrowserData as BrowserData


class ClassGetThread(threading.Thread):

    def __init__(self, className, canvas, frame, labelDownload):
        super(ClassGetThread, self).__init__()
        self.currentDownloadThread = None
        self.className = className
        self.canvas = canvas
        self.frame = frame
        self.labelDownload = labelDownload

    def stopDownload(self):
        if self.currentDownloadThread is not None and self.currentDownloadThread.is_alive():
            StopThread.stop_thread(self.currentDownloadThread)
            self.labelDownload['text'] = StaticString.textDownloadComplete

    def handleDownload(self, linkUrl, picTitleReal):
        if self.currentDownloadThread is None or not self.currentDownloadThread.is_alive():
            self.labelDownload.bind("<Button-1>", lambda event: self.stopDownload())
            downloadThread = DownloadThread.DownloadThread(linkUrl, picTitleReal, self.labelDownload)
            downloadThread.setDaemon(True)
            downloadThread.start()
            self.currentDownloadThread = downloadThread
        else:
            Alert.alert(StaticString.textAlreadyDownloading)

    def searchDataDisplay(self, result):
        if len(result) == 0:
            Alert.alert(StaticString.textSearchNotFound)
        row = 0
        column = 0
        singleWidth = 200
        singleHeight = 350
        picturesData = []
        for data in result:
            singleCollection = tk.Canvas(self.canvas, width=singleWidth, height=singleHeight, background="white")
            singleCollection.grid_propagate(0)
            self.canvas.create_window(column * 200, row * 350, anchor=tk.NW, window=singleCollection)
            img = Image.open(BytesIO(requests.get(data['picUrl'], headers=BrowserData.headers).content))
            img_resized = ImageOperation.resizeImage(singleWidth, singleHeight - 50, img)
            photo = ImageTk.PhotoImage(img_resized)
            picturesData.append(photo)
            labelPhoto = tk.Label(singleCollection, image=photo)
            labelPhoto.grid(row=0, column=0, rowspan=3, columnspan=1, sticky=tk.W + tk.E + tk.N + tk.S, padx=5, pady=5)

            lableName = tk.Label(singleCollection, text=data['picTitle'], font=(None, 12), background="white",
                                 width=10, height=1)
            lableName.grid(row=3, column=0, rowspan=1, columnspan=1, sticky=tk.W + tk.E + tk.N + tk.S, padx=5)
            lableNumber = tk.Label(singleCollection, text=data['number'], font=(None, 12), background="white", width=10,
                                   height=1)
            lableNumber.grid(row=4, column=0, rowspan=1, columnspan=1, sticky=tk.W + tk.E + tk.N + tk.S, padx=5)

            self.canvas.create_window(column * 200, row * 350, anchor=tk.NW, window=singleCollection)
            labelPhoto.bind("<Button-1>",
                            lambda event, linkUrl1=data['linkUrl'], picTitleReal1=data['picTitleReal']:
                            self.handleDownload(linkUrl1, picTitleReal1))
            column += 1
            if column == 4:
                column = 0
                row += 1

        if len(result) % 4 == 0:
            row -= 1
        self.canvas.pack()
        self.frame.grid()
        self.canvas.config(scrollregion=(0, 0, 800, (row + 1) * 350))

    def run(self) -> None:
        result = CurrentSite.searchFromClass(self.className)
        self.searchDataDisplay(result)
