"""应用配置常量"""

# 窗口配置
WINDOW_TITLE = "工程横道图生成器 v1.0"
WINDOW_SIZE = "1200x800"

# 横道图基础尺寸
BASE_DAY_WIDTH = 30
BASE_ROW_HEIGHT = 40
BASE_HEADER_HEIGHT = 60
BASE_LEFT_WIDTH = 200

# 缩放限制
MIN_ZOOM = 0.3
MAX_ZOOM = 3.0
ZOOM_STEP = 0.2

# 图片导出安全限制
MAX_IMAGE_WIDTH = 8000
MAX_IMAGE_HEIGHT = 8000

# Excel 列数限制
MAX_EXCEL_COLUMNS = 16384

# 任务类型颜色（Canvas / 图片）
TASK_COLORS = {
    'normal': '#3b82f6',
    'critical': '#ef4444',
    'completed': '#10b981'
}

# Excel 填充颜色
EXCEL_FILLS = {
    'normal': '3B82F6',
    'critical': 'EF4444',
    'completed': '10B981'
}

# 字体候选列表
FONT_CANDIDATES = ['msyh.ttc', 'msyhbd.ttc', 'simhei.ttf', 'simsun.ttc', 'arial.ttf']

# 主题配色（现代浅色风格）
THEME = {
    'bg_primary': '#f8fafc',
    'bg_secondary': '#ffffff',
    'bg_card': '#ffffff',
    'border': '#e2e8f0',
    'text_primary': '#1e293b',
    'text_secondary': '#64748b',
    'accent': '#3b82f6',
    'accent_hover': '#2563eb',
    'danger': '#ef4444',
    'success': '#10b981',
    'warning': '#f59e0b',
    'header_bg': '#f1f5f9',
    'header_text': '#475569',
}

# 字体配置
FONTS = {
    'default': ('微软雅黑', 10),
    'title': ('微软雅黑', 12, 'bold'),
    'small': ('微软雅黑', 9),
    'button': ('微软雅黑', 9),
    'bold': ('微软雅黑', 9, 'bold'),
}

# 间距配置
SPACING = {
    'xs': 2,
    'sm': 5,
    'md': 10,
    'lg': 15,
    'xl': 20,
}

# 示例数据
SAMPLE_PROJECT_NAME = "城市商业综合体建设项目"
SAMPLE_PROJECT_CODE = "CS-2026-001"
SAMPLE_TASKS = [
    ("基础施工", "2026-01-01", "2026-01-15", "normal"),
    ("主体结构", "2026-01-16", "2026-03-15", "critical"),
    ("装饰装修", "2026-03-16", "2026-05-15", "normal"),
    ("竣工验收", "2026-05-16", "2026-05-31", "completed"),
]
