from tkinter.filedialog import askdirectory
import time
import threading
import CurrentScript.CurrentSite as CurrentSite

from Interface import StaticString
from UtilOperations import WriteToFile


class DownloadThread(threading.Thread):

    def __init__(self, linkUrl, picTitle, labelDownload):
        super(DownloadThread, self).__init__()
        self.linkUrl = linkUrl
        self.picTitle = picTitle
        self.labelDownload = labelDownload
        self.path = ""

    def saveDownloadData(self, downloadData):
        number = 0
        while True:
            try:
                time.sleep(StaticString.sleepTime)
                WriteToFile.writeToFile(next(downloadData).content, number, self.picTitle, self.path)
                number += 1
                self.labelDownload['text'] = StaticString.textDownloadingPrefix + str(number) + \
                                             StaticString.textDownloadingSuffix
            except StopIteration:
                break
        self.labelDownload['text'] = StaticString.textDownloadComplete

    def run(self) -> None:
        self.path = ""
        self.path = askdirectory()
        if self.path == "":
            return
        downloadData = CurrentSite.downloadData(self.linkUrl)
        self.saveDownloadData(downloadData)
