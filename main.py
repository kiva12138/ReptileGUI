import tkinter as tk
import tkinter.messagebox
from tkinter import ttk

title = "健康生活"
textSiteSelect = "网站选择:"
textClassSelect = "图片分类:"
textSearchHint = "精准搜索:"
textSearchButton = " 查找 "
textDonateButton = "点开看看？"
textGetFailure = "获取失败"


class MainWindow:

    def __init__(self):
        self.sourceList = []
        self.classList = []

        self.window = tk.Tk()
        self.window.title(title)
        # self.window.geometry('800x600')
        self.window.resizable(0, 0)

        self.labelSite = tk.Label(self.window, text=textSiteSelect, font=(None, 12))
        self.listBoxSite = ttk.Combobox(self.window)

        self.labelClass = tk.Label(self.window, text=textClassSelect, font=(None, 12))
        self.listBoxClass = ttk.Combobox(self.window)
        self.listBoxClass.bind('<<ComboboxSelected>>', self.handleClassChange)

        self.labelSearch = tk.Label(self.window, text=textSearchHint, font=(None, 12))
        self.searchInput = tk.Entry(self.window, show=None, font=(None, 12))
        self.searchButton = tk.Button(self.window, text=textSearchButton, font=(None, 12), command=self.handleSearch)

        self.donateButton = tk.Button(self.window, text=textDonateButton, font=(None, 12), command=self.handleDonate)

        self.pictureFrame = tk.Frame(self.window, width=800, height=500, background="white")

    def guiBuild(self):
        self.labelSite.grid(row=0, column=0, rowspan=2, columnspan=2, sticky=tk.E+tk.N+tk.S, padx=5, pady=10)
        self.listBoxSite.grid(row=0, column=2, rowspan=2, columnspan=3, sticky=tk.W+tk.E+tk.N+tk.S, padx=5, pady=10)
        self.labelClass.grid(row=0, column=5, rowspan=2, columnspan=2, sticky=tk.E+tk.N+tk.S, padx=5, pady=10)
        self.listBoxClass.grid(row=0, column=7, rowspan=2, columnspan=3, sticky=tk.W+tk.E+tk.N+tk.S, padx=5, pady=10)

        self.labelSearch.grid(row=2, column=0, rowspan=2, columnspan=2, sticky=tk.E+tk.N+tk.S, padx=5, pady=10)
        self.searchInput.grid(row=2, column=2, rowspan=2, columnspan=3, sticky=tk.W+tk.E+tk.N+tk.S, padx=5, pady=10)
        self.searchButton.grid(row=2, column=5, rowspan=2, columnspan=2, sticky=tk.W+tk.N+tk.S, padx=5, pady=10)
        self.donateButton.grid(row=2, column=7, rowspan=2, columnspan=3, sticky=tk.E+tk.N+tk.S, padx=5, pady=10)

        self.pictureFrame.grid(row=4, column=0, columnspan=11, padx=10, pady=10)

    def getClassAndSite(self):
        self.sourceList = ["美图录", "秀人网", "推女郎"]
        self.listBoxSite['value'] = self.sourceList

        # 如果获取失败，那么需要禁用该多选框，或者选项设置为“获取失败”
        self.classList = ["日本", "国内", "动漫", "其他"]
        self.listBoxClass['value'] = self.classList

    def handleSearch(self):
        if self.searchInput.get().strip() is "":
            tk.messagebox.showinfo(title='WTF？', message='请先输入搜索内容')
        elif self.listBoxSite.get().strip() is "":
            tk.messagebox.showinfo(title='WTF？', message='请先选择搜索的网站')
        else:
            self.window.title(self.searchInput.get().strip() + '-' + title)

    def handleClassChange(self, event):
        tk.messagebox.showinfo(title='WTF？', message=self.classList[self.listBoxClass.current()])

    def handleDonate(self):
        top = tk.Toplevel()
        top.resizable(0, 0)
        top.title('捐赠')
        lable1 = tk.Label(top, text="制作不易，请多多支持", font=(None, 12))
        lable1.grid(row=0, column=0, rowspan=2, columnspan=5, sticky=tk.W+tk.E+tk.N+tk.S, padx=5, pady=10)
        lable2 = tk.Label(top, text="如果你爽了，不妨请我喝杯咖啡", font=(None, 12))
        lable2.grid(row=2, column=0, rowspan=2, columnspan=5, sticky=tk.W+tk.E+tk.N+tk.S, padx=5, pady=10)

        photo = tk.PhotoImage(file="AliPay3.gif")
        theLabel = tk.Label(top, image=photo)
        theLabel.grid(row=4, column=0, rowspan=5, columnspan=5, sticky=tk.W+tk.E+tk.N+tk.S, padx=5, pady=10)
        top.mainloop()


def main():
    window = MainWindow()
    window.guiBuild()
    window.getClassAndSite()
    tk.mainloop()


if __name__ == '__main__':
    main()
