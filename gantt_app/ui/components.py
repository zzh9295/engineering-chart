"""UI 组件：任务面板与横道图画布"""
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import timedelta

from gantt_app.config import (
    MIN_ZOOM, MAX_ZOOM, ZOOM_STEP, TASK_COLORS, SAMPLE_TASKS,
    THEME, FONTS, SPACING
)
from gantt_app.models import TaskRow, parse_task_rows, calculate_duration
from gantt_app.utils import compute_layout, prepare_task_data


class TaskPanel:
    """任务清单面板，负责任务行的增删改查"""

    def __init__(self, app, parent):
        self.app = app
        self.parent = parent
        self.frame = ttk.LabelFrame(parent, text="任务清单", padding=SPACING['md'])
        self.frame.pack(fill='x', padx=SPACING['md'], pady=SPACING['sm'])

        headers = ["序号", "任务名称", "开始日期", "结束日期", "工期(天)", "任务类型", "操作"]
        for i, h in enumerate(headers):
            ttk.Label(
                self.frame, text=h,
                font=FONTS['bold'],
                foreground=THEME['header_text']
            ).grid(row=0, column=i, padx=SPACING['sm'], pady=SPACING['sm'])

        self.app.task_rows = []
        self.add_row()

    def add_row(self, name="", start="2026-01-01", end="2026-01-10", task_type="normal"):
        """添加一行任务输入控件"""
        row_num = len(self.app.task_rows) + 1
        row_index = len(self.app.task_rows)

        idx_label = ttk.Label(self.frame, text=str(row_num), width=4, anchor='center')
        idx_label.grid(row=row_num, column=0, padx=SPACING['sm'], pady=SPACING['xs'])

        name_entry = ttk.Entry(self.frame, width=25)
        name_entry.grid(row=row_num, column=1, padx=SPACING['sm'], pady=SPACING['xs'])
        name_entry.insert(0, name)

        start_entry = ttk.Entry(self.frame, width=12)
        start_entry.grid(row=row_num, column=2, padx=SPACING['sm'], pady=SPACING['xs'])
        start_entry.insert(0, start)

        end_entry = ttk.Entry(self.frame, width=12)
        end_entry.grid(row=row_num, column=3, padx=SPACING['sm'], pady=SPACING['xs'])
        end_entry.insert(0, end)

        duration_label = ttk.Label(self.frame, text="--", width=8, anchor='center')
        duration_label.grid(row=row_num, column=4, padx=SPACING['sm'], pady=SPACING['xs'])

        type_var = tk.StringVar(value=task_type)
        type_combo = ttk.Combobox(
            self.frame, textvariable=type_var,
            values=["normal", "critical", "completed"], width=10, state='readonly'
        )
        type_combo.grid(row=row_num, column=5, padx=SPACING['sm'], pady=SPACING['xs'])

        def calc_duration(*args):
            days = calculate_duration(start_entry.get(), end_entry.get())
            duration_label.config(text=str(days) if days is not None else "--")

        start_entry.bind('<KeyRelease>', calc_duration)
        end_entry.bind('<KeyRelease>', calc_duration)

        widgets = [idx_label, name_entry, start_entry, end_entry, duration_label, type_combo]

        def delete():
            for w in widgets:
                w.destroy()
            self.app.task_rows = [r for r in self.app.task_rows if r.index != row_index]
            self._refresh_indices()

        delete_btn = ttk.Button(self.frame, text="删除", command=delete, width=6, style='Danger.TButton')
        delete_btn.grid(row=row_num, column=6, padx=SPACING['sm'], pady=SPACING['xs'])
        widgets.append(delete_btn)

        task_row = TaskRow(row_index, name_entry, start_entry, end_entry, duration_label, type_var, widgets)
        self.app.task_rows.append(task_row)
        calc_duration()
        return task_row

    def _refresh_indices(self):
        """删除行后刷新序号显示"""
        for i, row in enumerate(self.app.task_rows):
            row.index = i
            row.widgets[0].config(text=str(i + 1))

    def clear(self):
        """清空所有任务行并保留一个空行"""
        if not messagebox.askyesno("确认", "清空所有任务？"):
            return
        for row in self.app.task_rows:
            row.destroy()
        self.app.task_rows.clear()
        self.add_row()
        self.app.canvas.delete('all')

    def load_sample(self):
        """加载示例任务数据"""
        self.app.project_name.delete(0, 'end')
        self.app.project_name.insert(0, self.app.sample_project_name)
        self.app.project_code.delete(0, 'end')
        self.app.project_code.insert(0, self.app.sample_project_code)

        for row in list(self.app.task_rows):
            row.destroy()
        self.app.task_rows.clear()

        for name, start, end, task_type in SAMPLE_TASKS:
            task_row = self.add_row(name, start, end, task_type)
            days = calculate_duration(start, end)
            if days is not None:
                task_row.duration.config(text=str(days))


class ChartCanvas:
    """横道图画布，负责渲染与缩放"""

    def __init__(self, app, parent):
        self.app = app
        self.frame = ttk.LabelFrame(parent, text="横道图预览", padding=SPACING['md'])
        self.frame.pack(fill='both', expand=True, padx=SPACING['md'], pady=SPACING['sm'])

        self.app.canvas = tk.Canvas(
            self.frame, bg=THEME['bg_card'],
            scrollregion=(0, 0, 2000, 1000),
            highlightthickness=0
        )
        hbar = ttk.Scrollbar(self.frame, orient='horizontal', command=self.app.canvas.xview)
        vbar = ttk.Scrollbar(self.frame, orient='vertical', command=self.app.canvas.yview)
        self.app.canvas.configure(xscrollcommand=hbar.set, yscrollcommand=vbar.set)

        self.app.canvas.grid(row=0, column=0, sticky='nsew')
        vbar.grid(row=0, column=1, sticky='ns')
        hbar.grid(row=1, column=0, sticky='ew')
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

    def render(self):
        """根据当前任务数据和缩放级别绘制横道图"""
        canvas = self.app.canvas
        canvas.delete('all')

        tasks = parse_task_rows(self.app.task_rows)
        if not tasks:
            messagebox.showwarning("提示", "请输入有效的任务数据")
            return

        try:
            layout = compute_layout(tasks, self.app.zoom_level)
        except ValueError as e:
            messagebox.showwarning("提示", str(e))
            return

        prepared = prepare_task_data(tasks, layout.min_date)

        # 表头：任务名称
        canvas.create_rectangle(
            0, 0, layout.left_width, layout.header_height,
            fill=THEME['header_bg'], outline=THEME['border']
        )
        canvas.create_text(
            layout.left_width / 2, layout.header_height / 2,
            text="任务名称", font=('微软雅黑', layout.header_font_size, 'bold'),
            fill=THEME['header_text']
        )

        # 表头：日期
        current = layout.min_date
        x = layout.left_width
        while current <= layout.max_date:
            canvas.create_rectangle(
                x, 0, x + layout.day_width, layout.header_height,
                fill='#f9fafb', outline=THEME['border']
            )
            canvas.create_text(
                x + layout.day_width / 2, layout.header_height / 2,
                text=current.strftime("%m/%d"), font=('微软雅黑', layout.day_font_size),
                fill=THEME['text_secondary']
            )
            current += timedelta(days=1)
            x += layout.day_width

        # 任务行
        for i, task in enumerate(prepared):
            y = layout.header_height + i * layout.row_height

            canvas.create_rectangle(
                0, y, layout.left_width, y + layout.row_height,
                fill=THEME['bg_card'], outline=THEME['border']
            )
            canvas.create_text(
                10, y + layout.row_height / 2,
                text=task['name'], anchor='w',
                font=('微软雅黑', layout.task_font_size),
                fill=THEME['text_primary']
            )

            bar_x = layout.left_width + task['start_offset'] * layout.day_width
            bar_width = task['duration'] * layout.day_width
            bar_width = max(1, bar_width)

            color = TASK_COLORS.get(task['type'], TASK_COLORS['normal'])
            bar_top = y + layout.bar_margin
            bar_bottom = y + layout.row_height - layout.bar_margin
            canvas.create_rectangle(
                bar_x, bar_top, bar_x + bar_width, bar_bottom,
                fill=color, outline='', width=0
            )

            if bar_width >= max(20, layout.day_width):
                canvas.create_text(
                    bar_x + bar_width / 2, y + layout.row_height / 2,
                    text=f"{task['duration']}天", fill='white',
                    font=('微软雅黑', layout.day_font_size)
                )

        canvas.config(scrollregion=(
            0, 0,
            layout.left_width + layout.total_days * layout.day_width,
            layout.header_height + len(tasks) * layout.row_height
        ))

    def zoom_in(self):
        self.app.zoom_level = min(MAX_ZOOM, self.app.zoom_level + ZOOM_STEP)
        self.render()

    def zoom_out(self):
        self.app.zoom_level = max(MIN_ZOOM, self.app.zoom_level - ZOOM_STEP)
        self.render()

    def zoom_reset(self):
        self.app.zoom_level = 1.0
        self.render()
