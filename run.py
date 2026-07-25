"""工程横道图生成器启动入口"""
import tkinter as tk
from gantt_app import GanttChartApp


def main():
    root = tk.Tk()
    app = GanttChartApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()
