"""现代主题配置与 ttk 样式应用"""
import tkinter as tk
from tkinter import ttk

from gantt_app.config import THEME, FONTS


def setup_theme(root):
    """配置现代浅色主题样式"""
    style = ttk.Style(root)

    # 使用 clam 主题作为可定制基础
    try:
        style.theme_use('clam')
    except tk.TclError:
        pass

    # 全局字体
    root.option_add('*Font', FONTS['default'])
    root.option_add('*TLabel.Font', FONTS['default'])
    root.option_add('*TButton.Font', FONTS['button'])
    root.option_add('*TEntry.Font', FONTS['default'])
    root.option_add('*TCombobox.Font', FONTS['default'])

    # 主背景
    root.configure(background=THEME['bg_primary'])

    # Frame
    style.configure('TFrame', background=THEME['bg_primary'])

    # LabelFrame
    style.configure(
        'TLabelframe',
        background=THEME['bg_card'],
        borderwidth=1,
        relief='solid'
    )
    style.configure(
        'TLabelframe.Label',
        background=THEME['bg_card'],
        foreground=THEME['header_text'],
        font=FONTS['bold']
    )

    # Label
    style.configure('TLabel', background=THEME['bg_primary'], foreground=THEME['text_primary'])
    style.configure('Header.TLabel', font=FONTS['title'], foreground=THEME['text_primary'])
    style.configure('Muted.TLabel', foreground=THEME['text_secondary'])

    # Entry
    style.configure(
        'TEntry',
        fieldbackground=THEME['bg_secondary'],
        foreground=THEME['text_primary'],
        bordercolor=THEME['border'],
        lightcolor=THEME['border'],
        darkcolor=THEME['border']
    )

    # Combobox
    style.configure(
        'TCombobox',
        fieldbackground=THEME['bg_secondary'],
        background=THEME['bg_secondary'],
        foreground=THEME['text_primary']
    )

    # 普通按钮
    style.configure(
        'TButton',
        background=THEME['bg_secondary'],
        foreground=THEME['text_primary'],
        bordercolor=THEME['border'],
        font=FONTS['button'],
        padding=(8, 4)
    )
    style.map(
        'TButton',
        background=[('active', THEME['header_bg']), ('pressed', '#e2e8f0')],
        foreground=[('active', THEME['text_primary'])]
    )

    # 主操作按钮（强调色）
    style.configure(
        'Accent.TButton',
        background=THEME['accent'],
        foreground='white',
        bordercolor=THEME['accent'],
        font=FONTS['button'],
        padding=(8, 4)
    )
    style.map(
        'Accent.TButton',
        background=[('active', THEME['accent_hover']), ('pressed', '#1d4ed8')],
        foreground=[('active', 'white'), ('pressed', 'white')]
    )

    # 危险按钮
    style.configure(
        'Danger.TButton',
        background=THEME['bg_secondary'],
        foreground=THEME['danger'],
        bordercolor=THEME['danger'],
        font=FONTS['button'],
        padding=(8, 4)
    )
    style.map(
        'Danger.TButton',
        background=[('active', '#fef2f2'), ('pressed', '#fee2e2')],
        foreground=[('active', THEME['danger']), ('pressed', THEME['danger'])]
    )

    # 成功按钮
    style.configure(
        'Success.TButton',
        background=THEME['success'],
        foreground='white',
        bordercolor=THEME['success'],
        font=FONTS['button'],
        padding=(8, 4)
    )
    style.map(
        'Success.TButton',
        background=[('active', '#059669'), ('pressed', '#047857')],
        foreground=[('active', 'white'), ('pressed', 'white')]
    )

    # Scrollbar
    style.configure(
        'TScrollbar',
        background=THEME['border'],
        troughcolor=THEME['bg_primary'],
        bordercolor=THEME['bg_primary'],
        arrowcolor=THEME['text_secondary']
    )
    style.map('TScrollbar', background=[('active', '#cbd5e1'), ('pressed', '#94a3b8')])

    # Progressbar
    style.configure(
        'TProgressbar',
        background=THEME['accent'],
        troughcolor=THEME['border'],
        bordercolor=THEME['border']
    )

    return style
