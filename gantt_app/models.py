"""数据模型与任务解析"""
from dataclasses import dataclass
from datetime import datetime
from tkinter import ttk
import tkinter as tk


@dataclass
class TaskRow:
    """表示界面中的一行任务输入控件"""
    index: int
    name: ttk.Entry
    start: ttk.Entry
    end: ttk.Entry
    duration: ttk.Label
    type_var: tk.StringVar
    widgets: list

    def destroy(self):
        """销毁该行所有控件"""
        for w in self.widgets:
            w.destroy()


def parse_task_rows(task_rows):
    """从 TaskRow 列表解析出有效任务数据，供渲染和导出使用。

    返回列表，每项为 dict：name, start(datetime), end(datetime), type
    """
    tasks = []
    for row in task_rows:
        try:
            s = datetime.strptime(row.start.get(), "%Y-%m-%d")
            e = datetime.strptime(row.end.get(), "%Y-%m-%d")
            tasks.append({
                'name': row.name.get(),
                'start': s,
                'end': e,
                'type': row.type_var.get()
            })
        except Exception:
            continue
    return tasks


def parse_tasks_for_export(task_rows):
    """解析用于导出的任务数据，包含序号、工期等展示字段。

    返回列表，每项为 dict：序号、任务名称、开始日期、结束日期、工期(天)、任务类型、start_dt、end_dt
    """
    tasks = []
    for i, row in enumerate(task_rows, 1):
        try:
            s = datetime.strptime(row.start.get(), "%Y-%m-%d")
            e = datetime.strptime(row.end.get(), "%Y-%m-%d")
            days = (e - s).days + 1
            tasks.append({
                '序号': i,
                '任务名称': row.name.get(),
                '开始日期': row.start.get(),
                '结束日期': row.end.get(),
                '工期(天)': days,
                '任务类型': row.type_var.get(),
                'start_dt': s,
                'end_dt': e
            })
        except Exception:
            continue
    return tasks


def calculate_duration(start_text, end_text):
    """计算两个日期字符串之间的工期（包含首尾）"""
    try:
        s = datetime.strptime(start_text, "%Y-%m-%d")
        e = datetime.strptime(end_text, "%Y-%m-%d")
        return (e - s).days + 1
    except Exception:
        return None
