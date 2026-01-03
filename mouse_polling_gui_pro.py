import time
import threading
import statistics
import tkinter as tk
from tkinter import ttk, font, messagebox
from collections import deque
from pynput import mouse

# ================= 配置 =================
WINDOW_SIZE = 600
AVG_HISTORY = 150
UPDATE_INTERVAL = 200  # ms
STANDARD_RATES = [125, 250, 500, 1000, 2000, 4000, 8000]

# ================= 状态 =================
intervals = deque(maxlen=WINDOW_SIZE)
avg_wave = deque(maxlen=AVG_HISTORY)
last_time_ns = None
listening = False
current_lang = "zh"  # 默认中文
current_help = None  # 当前显示的帮助窗口

# ================= 颜色主题 =================
COLORS = {
    "bg_primary": "#0f172a",
    "bg_secondary": "#1e293b",
    "bg_card": "#334155",
    "text_primary": "#f1f5f9",
    "text_secondary": "#94a3b8",
    "accent": "#3b82f6",
    "accent_hover": "#2563eb",
    "success": "#10b981",
    "warning": "#f59e0b",
    "danger": "#ef4444",
    "graph_line": "#60a5fa",
    "graph_bg": "#1e293b",
    "grid_lines": "#475569",
    "info": "#0ea5e9",
    "info_hover": "#0284c7",
    "help_bg": "#1e293b",
    "help_btn": "#0ea5e9",
    "help_btn_hover": "#0284c7"
}

# ================= 多语言文本 =================
LANGUAGES = {
    "zh": {
        "app_title": "鼠标轮询率专业测试工具",
        "status_ready": "● 准备就绪",
        "status_running": "● 运行中",
        "status_stopped": "● 已停止",
        "start_test": "开始测试",
        "stop_test": "停止测试",
        "avg_polling_rate": "平均轮询率",
        "min_polling_rate": "最低轮询率",
        "max_polling_rate": "最高轮询率",
        "std_dev": "标准差",
        "p95_rate": "P95 轮询率",
        "detected_rate": "检测到的轮询率",
        "stability_score": "稳定性评分",
        "grade": "等级",
        "waveform_title": "平均轮询率实时变化",
        "stability_progress": "稳定性进度:",
        "instruction": "测试说明：持续移动鼠标以获得准确的轮询率测试结果",
        "hz": "Hz",
        "excellent": "优秀",
        "good": "良好",
        "fair": "一般",
        "poor": "差",
        "unknown": "未知",
        "language": "语言",
        "chinese": "english",
        "english": "英文",
        "rate_125": "125Hz (普通鼠标)",
        "rate_250": "250Hz (游戏鼠标)",
        "rate_500": "500Hz (高性能)",
        "rate_1000": "1000Hz (电竞级)",
        "rate_2000": "2000Hz (高级电竞)",
        "rate_4000": "4000Hz (顶级电竞)",
        "rate_8000": "8000Hz (极致电竞)",
        "test_tips": "测试时请持续匀速移动鼠标",
        "help": "帮助",
        "about": "关于",
        "close": "关闭",
        
        # 参数解释
        "avg_explanation": "平均轮询率\n\n鼠标向计算机报告位置的频率平均值。\n\n• 125Hz: 普通办公鼠标\n• 250Hz: 入门游戏鼠标\n• 500Hz: 中端游戏鼠标\n• 1000Hz: 高端电竞鼠标\n• 2000Hz: 高级电竞鼠标\n• 4000Hz: 顶级电竞鼠标\n• 8000Hz: 极致电竞鼠标\n\n更高的轮询率意味着更流畅的指针移动和更低的延迟。",
        "min_explanation": "最低轮询率\n\n测试期间记录到的最低轮询率数值。\n\n• 指示系统在最差情况下的性能\n• 过低的值可能表示系统卡顿或干扰\n• 理想情况下应接近平均值",
        "max_explanation": "最高轮询率\n\n测试期间记录到的最高轮询率数值。\n\n• 指示系统在最佳情况下的性能\n• 远高于标称值可能表示测量误差\n• 应该接近平均值且稳定",
        "std_explanation": "标准差\n\n衡量轮询率波动程度的统计指标。\n\n• 值越小表示轮询率越稳定\n• 值越大表示波动越大\n• 优秀: < 5 Hz\n• 良好: 5-15 Hz\n• 一般: 15-30 Hz\n• 差: > 30 Hz",
        "p95_explanation": "P95 轮询率\n\n95% 的时间轮询率高于此值。\n\n• 比平均值更能反映实际体验\n• 表示在最差5%情况下的性能\n• 数值越接近平均值越好",
        "detected_explanation": "检测到的轮询率\n\n根据测试结果自动识别的标准轮询率档位。\n\n• 125Hz: 标准USB轮询率\n• 250Hz: 常见游戏鼠标设置\n• 500Hz: 高性能模式\n• 1000Hz: 电竞级低延迟模式\n• 2000Hz: 高级低延迟模式\n• 4000Hz: 顶级低延迟模式\n• 8000Hz: 极致低延迟模式\n• 未知: 无法匹配标准档位",
        "score_explanation": "稳定性评分\n\n综合评估鼠标轮询率的稳定性。\n\n评分因素：\n• 抖动程度 (40%)\n• 尖峰数量 (30%)\n• 下降次数 (20%)\n• 偏移程度 (10%)\n\n评分等级：\n• 90-100: 优秀\n• 75-89: 良好\n• 60-74: 一般\n• 0-59: 差",
        "grade_explanation": "等级\n\n根据稳定性评分的文字评级。\n\n• 优秀: 性能稳定，适合竞技游戏\n• 良好: 性能良好，适合一般游戏\n• 一般: 存在波动，适合日常使用\n• 差: 性能不稳定，建议检查设备"
    },
    "en": {
        "app_title": "Mouse Polling Rate Pro Tester",
        "status_ready": "● Ready",
        "status_running": "● Running",
        "status_stopped": "● Stopped",
        "start_test": "Start Test",
        "stop_test": "Stop Test",
        "avg_polling_rate": "Average Polling Rate",
        "min_polling_rate": "Minimum Polling Rate",
        "max_polling_rate": "Maximum Polling Rate",
        "std_dev": "Standard Deviation",
        "p95_rate": "P95 Polling Rate",
        "detected_rate": "Detected Rate",
        "stability_score": "Stability Score",
        "grade": "Grade",
        "waveform_title": "Average Polling Rate Waveform",
        "stability_progress": "Stability Progress:",
        "instruction": "Instruction: Move mouse continuously to get accurate polling rate results",
        "hz": "Hz",
        "excellent": "Excellent",
        "good": "Good",
        "fair": "Fair",
        "poor": "Poor",
        "unknown": "Unknown",
        "language": "Language",
        "chinese": "Chinese",
        "english": "中文",
        "rate_125": "125Hz (Standard)",
        "rate_250": "250Hz (Gaming)",
        "rate_500": "500Hz (High Performance)",
        "rate_1000": "1000Hz (E-Sports)",
        "rate_2000": "2000Hz (Advanced Esports)",
        "rate_4000": "4000Hz (Top Esports)",
        "rate_8000": "8000Hz (Ultimate Esports)",
        "test_tips": "Move mouse steadily and continuously during testing",
        "help": "Help",
        "about": "About",
        "close": "Close",
        
        # 参数解释
        "avg_explanation": "Average Polling Rate\n\nAverage frequency at which the mouse reports its position to the computer.\n\n• 125Hz: Standard office mouse\n• 250Hz: Entry-level gaming mouse\n• 500Hz: Mid-range gaming mouse\n• 1000Hz: High-end esports mouse\n• 2000Hz: Advanced esports mouse\n• 4000Hz: Top esports mouse\n• 8000Hz: Ultimate esports mouse\n\nHigher polling rate means smoother cursor movement and lower latency.",
        "min_explanation": "Minimum Polling Rate\n\nLowest polling rate recorded during the test.\n\n• Indicates worst-case performance\n• Very low values may indicate system stutter or interference\n• Ideally should be close to the average",
        "max_explanation": "Maximum Polling Rate\n\nHighest polling rate recorded during the test.\n\n• Indicates best-case performance\n• Values far above nominal may indicate measurement errors\n• Should be close to average and stable",
        "std_explanation": "Standard Deviation\n\nStatistical measure of polling rate variability.\n\n• Lower values indicate more stable polling\n• Higher values indicate more fluctuation\n• Excellent: < 5 Hz\n• Good: 5-15 Hz\n• Fair: 15-30 Hz\n• Poor: > 30 Hz",
        "p95_explanation": "P95 Polling Rate\n\n95% of the time, polling rate is above this value.\n\n• Better reflects actual experience than average\n• Indicates performance in worst 5% of cases\n• Closer to average is better",
        "detected_explanation": "Detected Polling Rate\n\nAutomatically identified standard polling rate based on test results.\n\n• 125Hz: Standard USB polling rate\n• 250Hz: Common gaming mouse setting\n• 500Hz: High performance mode\n• 1000Hz: Esports low-latency mode\n• 2000Hz: Advanced low-latency mode\n• 4000Hz: Top low-latency mode\n• 8000Hz: Ultimate low-latency mode\n• Unknown: Cannot match standard rate",
        "score_explanation": "Stability Score\n\nComprehensive assessment of mouse polling rate stability.\n\nScoring factors:\n• Jitter level (40%)\n• Spike count (30%)\n• Drop count (20%)\n• Offset level (10%)\n\nScore levels:\n• 90-100: Excellent\n• 75-89: Good\n• 60-74: Fair\n• 0-59: Poor",
        "grade_explanation": "Grade\n\nText rating based on stability score.\n\n• Excellent: Stable performance, suitable for competitive gaming\n• Good: Good performance, suitable for general gaming\n• Fair: Some fluctuation, suitable for daily use\n• Poor: Unstable performance, check your device"
    }
}

def t(key):
    """获取当前语言的文本"""
    return LANGUAGES[current_lang].get(key, key)

# ================= 鼠标事件 =================
def on_move(x, y):
    global last_time_ns
    if not listening:
        return
    now = time.perf_counter_ns()
    if last_time_ns:
        dt = now - last_time_ns
        if dt < 50_000_000:  # 过滤 >50ms 异常
            intervals.append(dt)
    last_time_ns = now

# ================= 工具函数 =================
def clamp(v, a, b): return max(a, min(b, v))

def hz_list():
    return [1e9 / d for d in intervals if d > 0]

# ================= 档位识别 =================
def detect_rate(avg_hz):
    for r in STANDARD_RATES:
        if abs(avg_hz - r) / r < 0.12:
            return r
    return None

# ================= 稳定性评分 =================
def stability_score(hz, avg_hz, target):
    if len(hz) < 30:
        return None

    std = statistics.stdev(hz) if len(hz) > 1 else 0
    jitter_ratio = std / avg_hz
    jitter_score = clamp(100 - jitter_ratio * 400, 0, 100)

    spike_cnt = sum(1 for h in hz if h < avg_hz * 0.6)
    spike_score = clamp(100 - (spike_cnt / len(hz)) * 500, 0, 100)

    drop_cnt = sum(1 for h in hz if h < avg_hz * 0.8)
    drop_score = clamp(100 - (drop_cnt / len(hz)) * 300, 0, 100)

    if target:
        offset = abs(avg_hz - target) / target
        offset_score = clamp(100 - offset * 300, 0, 100)
    else:
        offset_score = 60

    final = (
        jitter_score * 0.4 +
        spike_score * 0.3 +
        drop_score * 0.2 +
        offset_score * 0.1
    )

    return round(final), jitter_score, spike_score

# ================= 创建现代按钮 =================
class ModernButton(ttk.Frame):
    def __init__(self, parent, text_key, command, color=COLORS["accent"], width=120):
        super().__init__(parent)
        self.command = command
        self.color = color
        self.text_key = text_key
        
        self.btn_canvas = tk.Canvas(
            self, width=width, height=42, 
            bg=COLORS["bg_secondary"], highlightthickness=0
        )
        self.btn_canvas.pack()
        
        self.btn_id = self.btn_canvas.create_rectangle(
            2, 2, width-2, 40, 
            fill=color, outline=color, width=2, 
            tags="btn"
        )
        
        self.text_id = self.btn_canvas.create_text(
            width//2, 21, 
            text=t(text_key), 
            fill=COLORS["text_primary"],
            font=("Segoe UI", 10, "bold"),
            tags="text"
        )
        
        self.btn_canvas.tag_bind("btn", "<Button-1>", self._on_click)
        self.btn_canvas.tag_bind("text", "<Button-1>", self._on_click)
        
        self.btn_canvas.bind("<Enter>", self._on_hover)
        self.btn_canvas.bind("<Leave>", self._on_leave)
        
    def _on_click(self, event):
        self.btn_canvas.itemconfig("btn", fill=COLORS["accent_hover"])
        self.after(100, self.command)
        
    def _on_hover(self, event):
        self.btn_canvas.itemconfig("btn", fill=COLORS["accent_hover"])
        
    def _on_leave(self, event):
        self.btn_canvas.itemconfig("btn", fill=self.color)
    
    def update_text(self):
        """更新按钮文本"""
        self.btn_canvas.itemconfig(self.text_id, text=t(self.text_key))

# ================= 创建增强的帮助按钮 =================
class EnhancedHelpButton(tk.Canvas):
    def __init__(self, parent, explanation_key, size=28):
        super().__init__(
            parent, 
            width=size, 
            height=size, 
            bg=COLORS["bg_card"], 
            highlightthickness=0
        )
        self.explanation_key = explanation_key
        self.size = size
        self.is_hovered = False
        
        # 绘制圆形背景
        self.bg_circle = self.create_oval(
            2, 2, size-2, size-2,
            fill=COLORS["help_btn"],
            outline=COLORS["help_btn"],
            width=2,
            tags="btn"
        )
        
        # 绘制问号
        self.text_id = self.create_text(
            size//2, size//2,
            text="?",
            fill=COLORS["text_primary"],
            font=("Segoe UI", 14, "bold"),
            tags="text"
        )
        
        # 绑定事件
        self.tag_bind("btn", "<Button-1>", self.show_help)
        self.tag_bind("text", "<Button-1>", self.show_help)
        self.bind("<Enter>", self._on_hover)
        self.bind("<Leave>", self._on_leave)
    
    def show_help(self, event=None):
        """显示帮助信息"""
        global current_help
        
        # 关闭现有的帮助窗口
        if current_help:
            try:
                current_help.destroy()
            except:
                pass
        
        # 创建新的帮助窗口
        help_window = tk.Toplevel(root)
        help_window.title(f"{t('help')} - {t(self.explanation_key.replace('_explanation', ''))}")
        help_window.geometry("450x400")
        help_window.configure(bg=COLORS["help_bg"])
        help_window.resizable(False, False)
        
        # 设置窗口位置（在鼠标位置附近）
        x = root.winfo_x() + 100
        y = root.winfo_y() + 100
        help_window.geometry(f"+{x}+{y}")
        
        # 使帮助窗口始终在最前面
        help_window.attributes('-topmost', True)
        
        # 创建文本框显示帮助内容
        help_text = tk.Text(
            help_window,
            wrap="word",
            font=("Segoe UI", 10),
            bg=COLORS["help_bg"],
            fg=COLORS["text_primary"],
            borderwidth=0,
            padx=20,
            pady=20,
            relief="flat"
        )
        help_text.pack(fill="both", expand=True, padx=1, pady=1)
        
        # 插入帮助文本
        help_text.insert("1.0", t(self.explanation_key))
        help_text.configure(state="disabled")
        
        # 关闭按钮
        close_frame = ttk.Frame(help_window, style="Card.TFrame")
        close_frame.pack(fill="x", pady=(0, 15))
        
        close_btn = ModernButton(close_frame, "close", help_window.destroy, COLORS["accent"], 120)
        close_btn.pack()
        
        # 保存当前帮助窗口引用
        current_help = help_window
        
        # 绑定关闭事件
        help_window.protocol("WM_DELETE_WINDOW", lambda: self.close_help(help_window))
    
    def close_help(self, window):
        """关闭帮助窗口"""
        global current_help
        window.destroy()
        current_help = None
    
    def _on_hover(self, event):
        """鼠标悬停在帮助按钮上"""
        self.is_hovered = True
        self.itemconfig(self.bg_circle, fill=COLORS["help_btn_hover"], outline=COLORS["help_btn_hover"])
        
        # 添加轻微放大效果
        self.scale("all", self.size//2, self.size//2, 1.1, 1.1)
    
    def _on_leave(self, event):
        """鼠标离开帮助按钮"""
        self.is_hovered = False
        self.itemconfig(self.bg_circle, fill=COLORS["help_btn"], outline=COLORS["help_btn"])
        
        # 恢复原始大小
        self.scale("all", self.size//2, self.size//2, 1/1.1, 1/1.1)

# ================= 创建指标卡片（带增强的帮助按钮）=================
class MetricCard(ttk.Frame):
    def __init__(self, parent, title_key, value="---", unit_key="", width=140, explanation_key=""):
        super().__init__(parent, width=width)
        self.config(style="Card.TFrame")
        self.title_key = title_key
        self.unit_key = unit_key
        self.explanation_key = explanation_key
        
        # 卡片内容容器
        self.content_frame = ttk.Frame(self, style="Card.TFrame")
        self.content_frame.pack(fill="both", expand=True, padx=12, pady=10)
        
        # 标题和帮助按钮容器
        title_container = ttk.Frame(self.content_frame, style="Card.TFrame")
        title_container.pack(fill="x", pady=(0, 8))
        
        # 标题
        self.title_label = ttk.Label(
            title_container, text=t(title_key), 
            font=("Segoe UI", 10, "bold"),
            foreground=COLORS["text_secondary"],
            background=COLORS["bg_card"]
        )
        self.title_label.pack(side="left", anchor="w")
        
        # 帮助按钮
        if explanation_key:
            self.help_btn = EnhancedHelpButton(title_container, explanation_key, size=28)
            self.help_btn.pack(side="right", padx=(5, 0))
        
        # 数值
        self.value_label = ttk.Label(
            self.content_frame, text=value, 
            font=("Segoe UI", 20, "bold"),
            foreground=COLORS["text_primary"],
            background=COLORS["bg_card"]
        )
        self.value_label.pack(pady=(8, 4))
        
        # 单位
        if unit_key:
            self.unit_label = ttk.Label(
                self.content_frame, text=t(unit_key), 
                font=("Segoe UI", 10),
                foreground=COLORS["text_secondary"],
                background=COLORS["bg_card"]
            )
            self.unit_label.pack(pady=(0, 8))
        else:
            # 如果没有单位，添加一些底部间距
            ttk.Frame(self.content_frame, height=12, style="Card.TFrame").pack()
    
    def update_title(self):
        """更新标题文本"""
        self.title_label.config(text=t(self.title_key))
        if hasattr(self, 'unit_label'):
            self.unit_label.config(text=t(self.unit_key))

# ================= 创建语言切换按钮 =================
class LanguageButton(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.config(style="Card.TFrame")
        
        # 语言按钮
        self.btn_canvas = tk.Canvas(
            self, width=100, height=40, 
            bg=COLORS["bg_secondary"], highlightthickness=0
        )
        self.btn_canvas.pack()
        
        # 绘制语言图标和文本
        self.bg_rect = self.btn_canvas.create_rectangle(
            2, 2, 98, 38,
            fill=COLORS["accent"],
            outline=COLORS["accent"],
            width=2,
            tags="btn"
        )
        
        self.text_id = self.btn_canvas.create_text(
            50, 20, 
            text=f"🌐 {t('chinese' if current_lang == 'zh' else 'english')}", 
            font=("Segoe UI", 10, "bold"),
            fill=COLORS["text_primary"],
            tags="text"
        )
        
        self.btn_canvas.tag_bind("btn", "<Button-1>", self.toggle_language)
        self.btn_canvas.tag_bind("text", "<Button-1>", self.toggle_language)
        self.btn_canvas.bind("<Enter>", self._on_hover)
        self.btn_canvas.bind("<Leave>", self._on_leave)
    
    def toggle_language(self, event=None):
        """切换语言"""
        global current_lang
        current_lang = "en" if current_lang == "zh" else "zh"
        update_ui_texts()
        
    def _on_hover(self, event):
        self.btn_canvas.itemconfig(self.bg_rect, fill=COLORS["accent_hover"], outline=COLORS["accent_hover"])
    
    def _on_leave(self, event):
        self.btn_canvas.itemconfig(self.bg_rect, fill=COLORS["accent"], outline=COLORS["accent"])
    
    def update_text(self):
        """更新按钮文本"""
        self.btn_canvas.itemconfig(
            self.text_id, 
            text=f"🌐 {t('chinese' if current_lang == 'zh' else 'english')}"
        )

# ================= 创建关于按钮 =================
class AboutButton(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.config(style="Card.TFrame")
        
        # 关于按钮
        self.btn_canvas = tk.Canvas(
            self, width=100, height=40, 
            bg=COLORS["bg_secondary"], highlightthickness=0
        )
        self.btn_canvas.pack()
        
        # 绘制问号图标和文本
        self.bg_rect = self.btn_canvas.create_rectangle(
            2, 2, 98, 38,
            fill=COLORS["info"],
            outline=COLORS["info"],
            width=2,
            tags="btn"
        )
        
        self.text_id = self.btn_canvas.create_text(
            50, 20, 
            text=f"ℹ️ {t('about')}", 
            font=("Segoe UI", 10, "bold"),
            fill=COLORS["text_primary"],
            tags="text"
        )
        
        self.btn_canvas.tag_bind("btn", "<Button-1>", self.show_about)
        self.btn_canvas.tag_bind("text", "<Button-1>", self.show_about)
        self.btn_canvas.bind("<Enter>", self._on_hover)
        self.btn_canvas.bind("<Leave>", self._on_leave)
    
    def show_about(self, event=None):
        """显示关于信息"""
        about_text = {
            "zh": """鼠标轮询率专业测试工具 v2.0

功能说明：
• 实时测试鼠标轮询率
• 自动识别标准轮询率档位
• 评估轮询率稳定性
• 提供详细参数解释

技术指标：
• 采样窗口：600个数据点
• 波形显示：150个平均值点
• 更新频率：200ms
• 支持轮询率：125Hz, 250Hz, 500Hz, 1000Hz, 2000Hz, 4000Hz, 8000Hz

使用方法：
1. 点击"开始测试"按钮
2. 持续移动鼠标
3. 观察测试结果
4. 点击"停止测试"结束

提示：
• 测试时请保持鼠标匀速移动
• 建议测试时间不少于10秒
• 稳定的系统环境可获得更准确结果""",
            
            "en": """Mouse Polling Rate Pro Tester v2.0

Features:
• Real-time mouse polling rate testing
• Automatic standard rate detection
• Polling rate stability assessment
• Detailed parameter explanations

Technical Specifications:
• Sampling window: 600 data points
• Waveform display: 150 average points
• Update frequency: 200ms
• Supported rates: 125Hz, 250Hz, 500Hz, 1000Hz, 2000Hz, 4000Hz, 8000Hz

Usage:
1. Click "Start Test" button
2. Move mouse continuously
3. Observe test results
4. Click "Stop Test" to end

Tips:
• Keep mouse moving steadily during testing
• Recommended test duration: at least 10 seconds
• Stable system environment for accurate results"""
        }
        
        messagebox.showinfo(t("about"), about_text[current_lang])
        
    def _on_hover(self, event):
        self.btn_canvas.itemconfig(self.bg_rect, fill=COLORS["info_hover"], outline=COLORS["info_hover"])
    
    def _on_leave(self, event):
        self.btn_canvas.itemconfig(self.bg_rect, fill=COLORS["info"], outline=COLORS["info"])
    
    def update_text(self):
        """更新按钮文本"""
        self.btn_canvas.itemconfig(
            self.text_id, 
            text=f"ℹ️ {t('about')}"
        )

# ================= 创建标准轮询率标签 =================
class RateTags(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.config(style="Card.TFrame")
        
        # 标题
        title = ttk.Label(
            self, 
            text="标准轮询率档位" if current_lang == "zh" else "Standard Polling Rates",
            font=("Segoe UI", 10, "bold"),
            foreground=COLORS["text_secondary"],
            background=COLORS["bg_primary"]
        )
        title.pack(anchor="w", pady=(0, 8))
        
        self.tags_frame1 = ttk.Frame(self, style="Card.TFrame")
        self.tags_frame1.pack(fill="x", pady=(0, 2))
        self.tags_frame2 = ttk.Frame(self, style="Card.TFrame")
        self.tags_frame2.pack(fill="x", pady=(0, 5))
        
        # 创建7个轮询率标签
        self.rate_tags = []
        rate_keys = ["rate_125", "rate_250", "rate_500", "rate_1000", "rate_2000", "rate_4000", "rate_8000"]
        colors = [COLORS["text_secondary"], COLORS["warning"], COLORS["accent"], COLORS["success"], COLORS["success"], COLORS["success"], COLORS["success"]]
        
        for i, (key, color) in enumerate(zip(rate_keys, colors)):
            if i < 4:
                parent_frame = self.tags_frame1
            else:
                parent_frame = self.tags_frame2
            tag_frame = ttk.Frame(parent_frame, style="Card.TFrame")
            tag_frame.pack(side="left", padx=(0, 10))
            
            # 标签点 - 更大的圆点
            tk.Canvas(tag_frame, width=14, height=14, bg=color, 
                     highlightthickness=0).pack(side="left", padx=(0, 8))
            
            # 标签文本
            tag_label = ttk.Label(tag_frame, text=t(key), 
                                 font=("Segoe UI", 10),
                                 foreground=COLORS["text_secondary"],
                                 background=COLORS["bg_primary"])
            tag_label.pack(side="left")
            
            self.rate_tags.append(tag_label)
    
    def update_texts(self):
        """更新所有标签文本"""
        # 更新标题
        for widget in self.winfo_children():
            if isinstance(widget, ttk.Label):
                widget.config(text="标准轮询率档位" if current_lang == "zh" else "Standard Polling Rates")
                break
        
        # 更新标签
        rate_keys = ["rate_125", "rate_250", "rate_500", "rate_1000", "rate_2000", "rate_4000", "rate_8000"]
        for i, label in enumerate(self.rate_tags):
            label.config(text=t(rate_keys[i]))

# ================= UI 更新 =================
def update_ui():
    if len(intervals) < 20:
        root.after(UPDATE_INTERVAL, update_ui)
        return

    hz = hz_list()
    avg = statistics.mean(hz)
    mn, mx = min(hz), max(hz)
    std = statistics.stdev(hz) if len(hz) > 1 else 0
    p95 = sorted(hz)[int(len(hz) * 0.95)]

    avg_wave.append(avg)

    # 更新指标卡片数值
    card_avg.value_label.config(text=f"{avg:7.1f}")
    card_min.value_label.config(text=f"{mn:7.1f}")
    card_max.value_label.config(text=f"{mx:7.1f}")
    card_std.value_label.config(text=f"{std:6.1f}")
    card_p95.value_label.config(text=f"{p95:7.1f}")

    # 检测轮询率
    rate = detect_rate(avg)
    if rate:
        card_rate.value_label.config(text=f"{rate}")
        # 根据检测到的轮询率设置颜色
        if rate >= 1000:
            color = COLORS["success"]
        elif rate >= 500:
            color = COLORS["accent"]
        elif rate >= 250:
            color = COLORS["warning"]
        else:
            color = COLORS["text_secondary"]
        card_rate.value_label.config(foreground=color)
    else:
        card_rate.value_label.config(text=t("unknown"), foreground=COLORS["text_secondary"])

    # 稳定性评分
    score = stability_score(hz, avg, rate)
    if score:
        final, _, _ = score
        card_score.value_label.config(text=f"{final}")
        
        # 根据评分设置等级
        if final >= 90:
            grade_key = "excellent"
            color = COLORS["success"]
        elif final >= 75:
            grade_key = "good"
            color = COLORS["accent"]
        elif final >= 60:
            grade_key = "fair"
            color = COLORS["warning"]
        else:
            grade_key = "poor"
            color = COLORS["danger"]
            
        card_grade.value_label.config(text=t(grade_key), foreground=color)
        
        # 更新进度条
        progress_bar["value"] = final

    draw_wave()
    root.after(UPDATE_INTERVAL, update_ui)

# ================= 更新所有UI文本 =================
def update_ui_texts():
    """更新所有UI文本为当前语言"""
    # 更新窗口标题
    root.title(t("app_title"))
    
    # 更新标题标签
    title_label.config(text=t("app_title"))
    
    # 更新状态标签
    if listening:
        status_label.config(text=t("status_running"))
    else:
        status_label.config(text=t("status_ready"))
    
    # 更新指标卡片标题
    for card in [card_avg, card_min, card_max, card_std, card_p95, 
                 card_rate, card_score, card_grade]:
        card.update_title()
    
    # 更新波形图标题
    graph_title.config(text=t("waveform_title"))
    
    # 更新进度条标签
    progress_label.config(text=t("stability_progress"))
    
    # 更新底部说明
    footer.config(text=t("instruction"))
    tips_label.config(text=t("test_tips"))
    
    # 更新语言按钮
    lang_btn.update_text()
    
    # 更新关于按钮
    about_btn.update_text()
    
    # 更新轮询率标签
    rate_tags.update_texts()
    
    # 更新图形框架标签
    graph_frame.config(text=t("waveform_title"))

# ================= 波形绘制 =================
def draw_wave():
    canvas.delete("all")
    if len(avg_wave) < 2:
        return
    
    w, h = canvas.winfo_width(), canvas.winfo_height()
    
    # 绘制网格背景
    grid_size = 40
    for x in range(0, w, grid_size):
        canvas.create_line(x, 0, x, h, fill=COLORS["grid_lines"], width=1)
    for y in range(0, h, grid_size):
        canvas.create_line(0, y, w, y, fill=COLORS["grid_lines"], width=1)
    
    # 计算坐标范围
    hi, lo = max(avg_wave), min(avg_wave)
    span = max(hi - lo, 1)
    
    # 绘制Y轴标签
    y_values = [hi, (hi + lo) / 2, lo]
    for val in y_values:
        y = h - (val - lo) / span * (h - 40) - 20
        canvas.create_text(8, y, anchor="w", fill=COLORS["text_secondary"], 
                          font=("Segoe UI", 8), text=f"{int(val)} {t('hz')}")

# 生成波形点
    pts = []
    for i, v in enumerate(avg_wave):
        x = 60 + i * (w - 80) / (AVG_HISTORY - 1)
        y = h - (v - lo) / span * (h - 40) - 20
        pts.append((x, y))
    
    # 绘制波形线
    for i in range(len(pts) - 1):
        canvas.create_line(*pts[i], *pts[i + 1], 
                          fill=COLORS["graph_line"], width=3, 
                          capstyle=tk.ROUND, joinstyle=tk.ROUND)
    
    # 绘制当前点
    if pts:
        last_x, last_y = pts[-1]
        canvas.create_oval(last_x-4, last_y-4, last_x+4, last_y+4, 
                          fill=COLORS["graph_line"], outline=COLORS["graph_line"])
        
        # 显示当前值
        canvas.create_text(last_x+10, last_y, anchor="w", 
                          fill=COLORS["text_primary"], 
                          font=("Segoe UI", 9, "bold"),
                          text=f"{avg_wave[-1]:.1f} {t('hz')}")

# ================= 控制函数 =================
def start():
    global listening, last_time_ns
    intervals.clear()
    avg_wave.clear()
    last_time_ns = None
    listening = True
    status_label.config(text=t("status_running"), foreground=COLORS["success"])

# ================= GUI 设置 =================
root = tk.Tk()
root.title(t("app_title"))
root.geometry("920x820")
root.resizable(False, False)
root.configure(bg=COLORS["bg_primary"])

# 设置ttk样式
style = ttk.Style()
style.theme_use("clam")

# 配置样式
style.configure("Title.TLabel", 
                font=("Segoe UI", 22, "bold"),
                foreground=COLORS["text_primary"],
                background=COLORS["bg_primary"])

style.configure("Subtitle.TLabel", 
                font=("Segoe UI", 11),
                foreground=COLORS["text_secondary"],
                background=COLORS["bg_primary"])

style.configure("Card.TFrame", 
                background=COLORS["bg_card"],
                relief="flat",
                borderwidth=0)

style.configure("Card.TLabelframe", 
                background=COLORS["bg_primary"],
                foreground=COLORS["text_primary"],
                borderwidth=0)

style.configure("TProgressbar",
                troughcolor=COLORS["bg_card"],
                background=COLORS["accent"],
                borderwidth=0,
                lightcolor=COLORS["accent"],
                darkcolor=COLORS["accent"])

# ================= 主界面布局 =================
# 标题区域
title_frame = ttk.Frame(root, style="Card.TFrame")
title_frame.pack(fill="x", padx=25, pady=(25, 15))

# 应用标题
title_label = ttk.Label(title_frame, text=t("app_title"), style="Title.TLabel")
title_label.pack(side="left", anchor="w", expand=True)

# 状态和按钮区域
status_btn_frame = ttk.Frame(title_frame, style="Card.TFrame")
status_btn_frame.pack(side="right", anchor="e")

# 状态标签
status_label = ttk.Label(status_btn_frame, text=t("status_ready"), 
                        font=("Segoe UI", 11, "bold"),
                        foreground=COLORS["text_secondary"], 
                        background=COLORS["bg_primary"])
status_label.pack(side="top", anchor="e", pady=(0, 8))

# 按钮容器
btn_container_frame = ttk.Frame(status_btn_frame, style="Card.TFrame")
btn_container_frame.pack(side="top", anchor="e")

# 关于按钮
about_btn = AboutButton(btn_container_frame)
about_btn.pack(side="left", padx=(0, 12))

# 语言切换按钮
lang_btn = LanguageButton(btn_container_frame)
lang_btn.pack(side="left")

# 标准轮询率标签区域
rate_tags = RateTags(root)
rate_tags.pack(fill="x", padx=25, pady=(0, 15))

# 指标卡片区域
metrics_frame = ttk.Frame(root, style="Card.TFrame")
metrics_frame.pack(fill="x", padx=25, pady=(10, 20))

# 第一行指标卡片
row1 = ttk.Frame(metrics_frame, style="Card.TFrame")
row1.pack(fill="x", pady=(0, 15))

card_avg = MetricCard(row1, "avg_polling_rate", "---", "hz", width=150, explanation_key="avg_explanation")
card_avg.pack(side="left", padx=(0, 15), expand=True, fill="both")

card_min = MetricCard(row1, "min_polling_rate", "---", "hz", width=150, explanation_key="min_explanation")
card_min.pack(side="left", padx=(0, 15), expand=True, fill="both")

card_max = MetricCard(row1, "max_polling_rate", "---", "hz", width=150, explanation_key="max_explanation")
card_max.pack(side="left", padx=(0, 15), expand=True, fill="both")

card_std = MetricCard(row1, "std_dev", "---", "", width=150, explanation_key="std_explanation")
card_std.pack(side="left", expand=True, fill="both")

# 第二行指标卡片
row2 = ttk.Frame(metrics_frame, style="Card.TFrame")
row2.pack(fill="x", pady=(0, 15))

card_p95 = MetricCard(row2, "p95_rate", "---", "hz", width=150, explanation_key="p95_explanation")
card_p95.pack(side="left", padx=(0, 15), expand=True, fill="both")

card_rate = MetricCard(row2, "detected_rate", "---", "", width=150, explanation_key="detected_explanation")
card_rate.pack(side="left", padx=(0, 15), expand=True, fill="both")

card_score = MetricCard(row2, "stability_score", "---", "", width=150, explanation_key="score_explanation")
card_score.pack(side="left", padx=(0, 15), expand=True, fill="both")

card_grade = MetricCard(row2, "grade", "---", "", width=150, explanation_key="grade_explanation")
card_grade.pack(side="left", expand=True, fill="both")

# 波形图区域
graph_frame = ttk.LabelFrame(root, text=t("waveform_title"), style="Card.TLabelframe")
graph_frame.pack(fill="both", expand=True, padx=25, pady=(0, 20))

graph_title = ttk.Label(graph_frame, text=t("waveform_title"), 
                       font=("Segoe UI", 11, "bold"),
                       foreground=COLORS["text_secondary"],
                       background=COLORS["bg_primary"])
graph_title.pack(pady=(12, 8))

canvas = tk.Canvas(graph_frame, height=220, bg=COLORS["graph_bg"], 
                   highlightthickness=0, borderwidth=0)
canvas.pack(fill="both", expand=True, padx=15, pady=(0, 15))

# 稳定性进度条
stability_frame = ttk.Frame(root, style="Card.TFrame")
stability_frame.pack(fill="x", padx=25, pady=(0, 20))

progress_label = ttk.Label(stability_frame, text=t("stability_progress"), 
                          font=("Segoe UI", 11),
                          foreground=COLORS["text_secondary"],
                          background=COLORS["bg_primary"])
progress_label.pack(side="left", padx=(0, 12))

progress_bar = ttk.Progressbar(stability_frame, length=650, maximum=100, 
                              style="TProgressbar", mode="determinate")
progress_bar.pack(side="left", fill="x", expand=True, padx=(0, 12))
progress_bar["value"] = 0

# 测试提示
tips_frame = ttk.Frame(root, style="Card.TFrame")
tips_frame.pack(fill="x", padx=25, pady=(0, 12))

tips_label = ttk.Label(tips_frame, text=t("test_tips"), 
                      font=("Segoe UI", 10, "italic"),
                      foreground=COLORS["warning"],
                      background=COLORS["bg_primary"])
tips_label.pack()

# 底部说明
footer = ttk.Label(root, text=t("instruction"), 
                  font=("Segoe UI", 9),
                  foreground=COLORS["text_secondary"],
                  background=COLORS["bg_primary"])
footer.pack(pady=(0, 25))

# ================= 启动 =================
# 启动鼠标监听线程
threading.Thread(target=lambda: mouse.Listener(on_move=on_move).run(), daemon=True).start()

# 开始UI更新循环
root.after(UPDATE_INTERVAL, update_ui)

# 自动开始测试
start()

# 启动主循环
root.mainloop()