"""命令行入口：python -m gantt_app"""
import tkinter as tk
from gantt_app import GanttChartApp


def main():
    root = tk.Tk()
    app = GanttChartApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()
