"""横道图布局计算工具

将 Canvas 渲染与图片导出共用的尺寸、位置计算逻辑集中到这里，
消除两处绘制代码的重复。
"""
from dataclasses import dataclass
from datetime import datetime

from gantt_app.config import (
    BASE_DAY_WIDTH, BASE_ROW_HEIGHT, BASE_HEADER_HEIGHT, BASE_LEFT_WIDTH,
    MAX_IMAGE_WIDTH, MAX_IMAGE_HEIGHT
)


@dataclass
class ChartLayout:
    """横道图布局参数"""
    min_date: datetime
    max_date: datetime
    total_days: int
    left_width: int
    day_width: int
    row_height: int
    header_height: int
    width: int
    height: int
    padding: int
    bar_margin: int
    header_font_size: int
    day_font_size: int
    task_font_size: int


def prepare_task_data(tasks, min_date):
    """为每个任务计算起始偏移和工期"""
    result = []
    for task in tasks:
        start_offset = (task['start'] - min_date).days
        duration = (task['end'] - task['start']).days + 1
        result.append({
            **task,
            'start_offset': start_offset,
            'duration': duration
        })
    return result


def compute_layout(
    tasks,
    zoom_level=1.0,
    max_width=MAX_IMAGE_WIDTH,
    max_height=MAX_IMAGE_HEIGHT,
    base_day_width=BASE_DAY_WIDTH,
    base_row_height=BASE_ROW_HEIGHT,
    base_header_height=BASE_HEADER_HEIGHT,
    base_left_width=BASE_LEFT_WIDTH,
    padding=20
):
    """根据任务数据和缩放级别计算横道图完整布局。

    返回 ChartLayout 对象，若尺寸超出限制则抛出 ValueError。
    """
    if not tasks:
        raise ValueError("没有有效的任务数据")

    min_date = min(t['start'] for t in tasks)
    max_date = max(t['end'] for t in tasks)
    total_days = (max_date - min_date).days + 1

    left_width = int(base_left_width * zoom_level)
    day_width = int(base_day_width * zoom_level)
    row_height = int(base_row_height * zoom_level)
    header_height = int(base_header_height * zoom_level)

    day_width = max(4, day_width)
    row_height = max(10, row_height)
    header_height = max(20, header_height)
    left_width = max(100, left_width)

    # 宽度超出时自动压缩日期列宽
    if total_days > 0:
        calculated_width = left_width + total_days * day_width + padding * 2
        if calculated_width > max_width:
            day_width = (max_width - left_width - padding * 2) // total_days
            day_width = max(4, day_width)

    width = left_width + total_days * day_width + padding * 2
    height = header_height + len(tasks) * row_height + padding * 2

    # 高度超出时自动压缩行高
    if height > max_height:
        row_height = (max_height - header_height - padding * 2) // len(tasks)
        row_height = max(16, row_height)
        height = header_height + len(tasks) * row_height + padding * 2

    width = max(100, width)
    height = max(100, height)

    if width > max_width or height > max_height:
        raise ValueError(f"图片尺寸({width}x{height})超出安全限制")

    header_font_size = max(8, int(10 * zoom_level))
    day_font_size = max(6, int(8 * zoom_level))
    task_font_size = max(7, int(9 * zoom_level))
    bar_margin = max(2, int(10 * zoom_level))

    return ChartLayout(
        min_date=min_date,
        max_date=max_date,
        total_days=total_days,
        left_width=left_width,
        day_width=day_width,
        row_height=row_height,
        header_height=header_height,
        width=width,
        height=height,
        padding=padding,
        bar_margin=bar_margin,
        header_font_size=header_font_size,
        day_font_size=day_font_size,
        task_font_size=task_font_size
    )
