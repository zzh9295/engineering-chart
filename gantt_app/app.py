"""应用控制器：负责主窗口、工具栏与模块协调"""
import tkinter as tk
from tkinter import ttk

from gantt_app.config import WINDOW_TITLE, WINDOW_SIZE, SAMPLE_PROJECT_NAME, SAMPLE_PROJECT_CODE, SPACING
from gantt_app.ui import TaskPanel, ChartCanvas, setup_theme
from gantt_app.exporters import ExportManager


class GanttChartApp:
    """工程横道图生成器主应用"""

    def __init__(self, root):
        self.root = root
        self.root.title(WINDOW_TITLE)
        self.root.geometry(WINDOW_SIZE)

        # 状态变量
        self.tasks = []
        self.task_rows = []
        self.zoom_level = 1.0
        self.sample_project_name = SAMPLE_PROJECT_NAME
        self.sample_project_code = SAMPLE_PROJECT_CODE

        # 子模块
        self.exporter = ExportManager(self)

        # 应用主题
        setup_theme(self.root)

        self.setup_ui()

    def setup_ui(self):
        """构建主界面"""
        self._setup_info_frame()
        self.task_panel = TaskPanel(self, self.root)
        self.chart_canvas = ChartCanvas(self, self.root)
        self._setup_button_frame()

    def _setup_info_frame(self):
        """项目信息输入区"""
        info_frame = ttk.LabelFrame(self.root, text="项目信息", padding=SPACING['md'])
        info_frame.pack(fill='x', padx=SPACING['md'], pady=SPACING['sm'])

        ttk.Label(info_frame, text="项目名称:").grid(row=0, column=0, sticky='w')
        self.project_name = ttk.Entry(info_frame, width=40)
        self.project_name.grid(row=0, column=1, padx=SPACING['sm'])

        ttk.Label(info_frame, text="项目编号:").grid(row=0, column=2, sticky='w', padx=(SPACING['lg'], 0))
        self.project_code = ttk.Entry(info_frame, width=20)
        self.project_code.grid(row=0, column=3, padx=SPACING['sm'])

    def _setup_button_frame(self):
        """工具按钮区：按功能分组显示"""
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(fill='x', padx=SPACING['md'], pady=SPACING['sm'])

        # 任务管理组
        task_group = ttk.Frame(btn_frame)
        task_group.pack(side='left', padx=(0, SPACING['lg']))
        ttk.Button(task_group, text="➕ 添加任务", command=self.task_panel.add_row).pack(side='left', padx=SPACING['xs'])
        ttk.Button(task_group, text="🗑️ 清空", command=self.task_panel.clear, style='Danger.TButton').pack(side='left', padx=SPACING['xs'])
        ttk.Button(task_group, text="📋 示例数据", command=self.task_panel.load_sample).pack(side='left', padx=SPACING['xs'])

        # 渲染控制组
        render_group = ttk.Frame(btn_frame)
        render_group.pack(side='left', padx=(0, SPACING['lg']))
        ttk.Button(render_group, text="🚀 生成横道图", command=self.chart_canvas.render, style='Accent.TButton').pack(side='left', padx=SPACING['xs'])

        # 缩放控制组
        zoom_group = ttk.Frame(btn_frame)
        zoom_group.pack(side='left')
        ttk.Button(zoom_group, text="➕ 放大", command=self.chart_canvas.zoom_in).pack(side='left', padx=SPACING['xs'])
        ttk.Button(zoom_group, text="➖ 缩小", command=self.chart_canvas.zoom_out).pack(side='left', padx=SPACING['xs'])
        ttk.Button(zoom_group, text="↺ 重置", command=self.chart_canvas.zoom_reset).pack(side='left', padx=SPACING['xs'])

        # 导出组
        export_group = ttk.Frame(btn_frame)
        export_group.pack(side='right')
        ttk.Button(export_group, text="📄 导出CSV", command=self.exporter.export_csv).pack(side='left', padx=SPACING['xs'])
        ttk.Button(export_group, text="🖼️ 导出图片", command=self.exporter.export_image).pack(side='left', padx=SPACING['xs'])
        ttk.Button(export_group, text="📊 导出Excel", command=self.exporter.export_excel).pack(side='left', padx=SPACING['xs'])
        ttk.Button(export_group, text="📊 导出JSON", command=self.exporter.export_json, style='Success.TButton').pack(side='left', padx=SPACING['xs'])
