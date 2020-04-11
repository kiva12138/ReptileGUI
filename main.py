import tkinter as tk
import Interface.MainWindow as MainWindow


def main():
    window = MainWindow.MainWindow()
    window.getSite()
    tk.mainloop()


if __name__ == '__main__':
    main()
