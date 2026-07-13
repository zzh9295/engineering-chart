import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime, timedelta
import csv

class GanttChartApp:
    def __init__(self, root):
        self.root = root
        self.root.title("工程横道图生成器 v1.0")
        self.root.geometry("1200x800")
        self.tasks = []
        
        self.setup_ui()
    
    def setup_ui(self):
        # 顶部项目信息
        info_frame = ttk.LabelFrame(self.root, text="项目信息", padding=10)
        info_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(info_frame, text="项目名称:").grid(row=0, column=0, sticky='w')
        self.project_name = ttk.Entry(info_frame, width=40)
        self.project_name.grid(row=0, column=1, padx=5)
        
        ttk.Label(info_frame, text="项目编号:").grid(row=0, column=2, sticky='w', padx=(20,0))
        self.project_code = ttk.Entry(info_frame, width=20)
        self.project_code.grid(row=0, column=3, padx=5)
        
        # 任务输入区
        task_frame = ttk.LabelFrame(self.root, text="任务清单", padding=10)
        task_frame.pack(fill='x', padx=10, pady=5)
        
        # 表头
        headers = ["序号", "任务名称", "开始日期", "结束日期", "工期(天)", "任务类型", "操作"]
        for i, h in enumerate(headers):
            ttk.Label(task_frame, text=h, font=('微软雅黑', 9, 'bold')).grid(row=0, column=i, padx=5, pady=5)
        
        self.task_rows = []
        self.add_task_row(task_frame, 1)
        
        # 按钮区
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(btn_frame, text="➕ 添加任务", command=lambda: self.add_task_row(task_frame, len(self.task_rows)+1)).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="🗑️ 清空", command=self.clear_tasks).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="📋 示例数据", command=self.load_sample).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="🚀 生成横道图", command=self.generate_chart).pack(side='left', padx=20)
        ttk.Button(btn_frame, text="💾 导出CSV", command=self.export_csv).pack(side='right', padx=5)
        
        # 图表显示区（Canvas）
        chart_frame = ttk.LabelFrame(self.root, text="横道图预览", padding=10)
        chart_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.canvas = tk.Canvas(chart_frame, bg='white', scrollregion=(0, 0, 2000, 1000))
        hbar = ttk.Scrollbar(chart_frame, orient='horizontal', command=self.canvas.xview)
        vbar = ttk.Scrollbar(chart_frame, orient='vertical', command=self.canvas.yview)
        self.canvas.configure(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
        
        self.canvas.grid(row=0, column=0, sticky='nsew')
        vbar.grid(row=0, column=1, sticky='ns')
        hbar.grid(row=1, column=0, sticky='ew')
        chart_frame.grid_rowconfigure(0, weight=1)
        chart_frame.grid_columnconfigure(0, weight=1)
    
    def add_task_row(self, parent, row_num):
        row = len(self.task_rows)
        idx_label = ttk.Label(parent, text=str(row_num))
        idx_label.grid(row=row_num, column=0, padx=5)
        
        name = ttk.Entry(parent, width=25)
        name.grid(row=row_num, column=1, padx=5)
        
        start = ttk.Entry(parent, width=12)
        start.grid(row=row_num, column=2, padx=5)
        start.insert(0, "2026-01-01")
        
        end = ttk.Entry(parent, width=12)
        end.grid(row=row_num, column=3, padx=5)
        end.insert(0, "2026-01-10")
        
        duration = ttk.Label(parent, text="--", width=8)
        duration.grid(row=row_num, column=4, padx=5)
        
        type_var = tk.StringVar(value="normal")
        type_combo = ttk.Combobox(parent, textvariable=type_var, values=["normal", "critical", "completed"], width=10, state='readonly')
        type_combo.grid(row=row_num, column=5, padx=5)
        
        def calc_duration(*args):
            try:
                s = datetime.strptime(start.get(), "%Y-%m-%d")
                e = datetime.strptime(end.get(), "%Y-%m-%d")
                days = (e - s).days + 1
                duration.config(text=str(days))
            except:
                pass
        
        start.bind('<KeyRelease>', calc_duration)
        end.bind('<KeyRelease>', calc_duration)
        
        def delete():
            for w in [idx_label, name, start, end, duration, type_combo]:
                w.destroy()
            self.task_rows = [r for r in self.task_rows if r[0] != row]
        
        ttk.Button(parent, text="删除", command=delete, width=6).grid(row=row_num, column=6, padx=5)
        
        self.task_rows.append((row, name, start, end, duration, type_var))
    
    def clear_tasks(self):
        if messagebox.askyesno("确认", "清空所有任务？"):
            self.task_rows.clear()
            # 重新构建UI...
    
    def load_sample(self):
        self.project_name.delete(0, 'end')
        self.project_name.insert(0, "示例工程")
        # 填充示例任务...
    
    def generate_chart(self):
        self.canvas.delete('all')
        
        # 收集任务数据
        tasks = []
        for _, name, start, end, _, type_var in self.task_rows:
            try:
                s = datetime.strptime(start.get(), "%Y-%m-%d")
                e = datetime.strptime(end.get(), "%Y-%m-%d")
                tasks.append({
                    'name': name.get(),
                    'start': s,
                    'end': e,
                    'type': type_var.get()
                })
            except:
                continue
        
        if not tasks:
            messagebox.showwarning("提示", "请输入有效的任务数据")
            return
        
        # 计算时间范围
        min_date = min(t['start'] for t in tasks)
        max_date = max(t['end'] for t in tasks)
        total_days = (max_date - min_date).days + 1
        
        # 绘图参数
        left_width = 200
        day_width = 30
        row_height = 40
        header_height = 60
        colors = {
            'normal': '#3b82f6',
            'critical': '#ef4444', 
            'completed': '#10b981'
        }
        
        # 绘制表头
        self.canvas.create_rectangle(0, 0, left_width, header_height, fill='#f3f4f6', outline='#d1d5db')
        self.canvas.create_text(left_width/2, header_height/2, text="任务名称", font=('微软雅黑', 10, 'bold'))
        
        # 绘制日期轴
        current = min_date
        x = left_width
        while current <= max_date:
            self.canvas.create_rectangle(x, 0, x+day_width, header_height, fill='#f9fafb', outline='#e5e7eb')
            self.canvas.create_text(x+day_width/2, 20, text=current.strftime("%m/%d"), font=('微软雅黑', 8))
            current += timedelta(days=1)
            x += day_width
        
        # 绘制任务条
        for i, task in enumerate(tasks):
            y = header_height + i * row_height
            
            # 任务名
            self.canvas.create_rectangle(0, y, left_width, y+row_height, fill='white', outline='#e5e7eb')
            self.canvas.create_text(10, y+row_height/2, text=task['name'], anchor='w', font=('微软雅黑', 9))
            
            # 横道
            start_offset = (task['start'] - min_date).days
            duration = (task['end'] - task['start']).days + 1
            bar_x = left_width + start_offset * day_width
            bar_width = duration * day_width
            
            color = colors.get(task['type'], '#3b82f6')
            self.canvas.create_rectangle(bar_x, y+10, bar_x+bar_width, y+30, fill=color, outline='', width=0)
            self.canvas.create_text(bar_x+bar_width/2, y+20, text=f"{duration}天", fill='white', font=('微软雅黑', 8))
        
        self.canvas.config(scrollregion=(0, 0, left_width + total_days*day_width, header_height + len(tasks)*row_height))
    
    def export_csv(self):
        # CSV导出逻辑...
        pass

if __name__ == '__main__':
    root = tk.Tk()
    app = GanttChartApp(root)
    root.mainloop()