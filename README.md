# 🐭 Mouse Polling Rate Pro Tester
🌍 **Language**
- [English](README.md)
- [简体中文](README.zh-CN.md)

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)](https://github.com/yourusername/mouse-polling-rate-tester)
[![Release](https://img.shields.io/github/v/release/yourusername/mouse-polling-rate-tester)](https://github.com/yourusername/mouse-polling-rate-tester/releases)

**专业级鼠标真实USB轮询率测试工具** - 突破浏览器限制，直接测量系统级原始输入数据

![软件界面](image/MousePollingRoateTool.png)
*专业GUI界面，实时显示轮询率数据与波形图*

---

## 📋 目录
- [✨ 核心特性](#-核心特性)
- [🎯 为什么需要这个工具？](#-为什么需要这个工具？)
- [📊 技术规格](#-技术规格)
- [🚀 快速开始](#-快速开始)
- [🔧 使用方法](#-使用方法)
- [📈 测试指标详解](#-测试指标详解)
- [🖥️ 系统要求](#️-系统要求)
- [📁 项目结构](#-项目结构)
- [🤝 贡献指南](#-贡献指南)
- [📄 许可证](#-许可证)
- [🙏 致谢](#-致谢)

---

## ✨ 核心特性

### 🎯 精确测量
- **真实USB轮询率检测** - 绕过浏览器限制，直接访问系统HID层
- **纳秒级时间精度** - 使用`time.perf_counter_ns()`实现高精度计时
- **智能数据过滤** - 自动过滤异常值，确保结果准确性

### 📊 专业分析
- **自动档位识别** - 智能识别125/250/500/1000/2000/4000/8000Hz标准档位
- **稳定性评分系统** - 综合评估轮询率稳定性（优秀/良好/一般/差）
- **多维度指标** - 平均值、最小值、最大值、标准差、P95值、抖动分析

### 🎨 现代界面
- **实时波形图** - 直观显示轮询率变化趋势
- **多语言支持** - 中英文界面一键切换
- **暗色主题** - 专业电竞风格UI设计
- **详细帮助** - 每个参数都有详细解释说明

### 🔧 高级功能
- **原始输入捕获** - 使用系统级API获取鼠标数据
- **600数据点采样窗口** - 大容量数据缓存，分析更准确
- **150点波形显示** - 实时可视化轮询率变化
- **200ms更新频率** - 平衡性能与实时性

---

## 🎯 为什么需要这个工具？

### 🔍 网页测试的局限性
普通网页鼠标测试工具受限于：
- **浏览器事件节流** - 事件触发与屏幕刷新率同步
- **操作系统限制** - 无法访问USB HID层原始数据
- **最高频率受限** - 通常不超过显示器刷新率（60-240Hz）

### 🚀 桌面工具的优势
本工具提供：
- **真实硬件数据** - 直接测量USB Polling Rate
- **支持高轮询率** - 最高可测8000Hz超采样鼠标
- **系统级访问** - 绕过所有软件层限制
- **专业分析** - 电竞级性能评估标准

### 📊 对比表
| 特性 | 网页测试工具 | 本桌面工具 |
|------|--------------|------------|
| **数据源** | 浏览器事件 (mousemove) | 系统原始输入 (Raw Input) |
| **最高精度** | ≈ 显示器刷新率 | USB 真实轮询率 |
| **支持档位** | 60-240Hz | 125-8000Hz |
| **延迟测量** | 无法测量 | 精确到纳秒级 |
| **稳定性分析** | 基础统计 | 专业评分系统 |

---

## 📊 技术规格

### 🎛️ 采样参数
| 参数 | 规格 | 说明 |
|------|------|------|
| 采样窗口 | 600个数据点 | 提供充足的历史数据 |
| 波形显示 | 150个平均值点 | 实时可视化变化趋势 |
| 更新频率 | 200ms | 平衡性能与实时性 |
| 时间精度 | 纳秒级 | 使用`perf_counter_ns()` |

### 📈 支持轮询率
| 轮询率 | 典型设备 | 报告延迟 | 适用场景 |
|--------|----------|----------|----------|
| 125Hz | 普通办公鼠标 | 8ms | 日常办公 |
| 250Hz | 入门游戏鼠标 | 4ms | 休闲游戏 |
| 500Hz | 中端游戏鼠标 | 2ms | 普通游戏 |
| 1000Hz | 高端电竞鼠标 | 1ms | 竞技游戏 |
| 2000Hz | 高级电竞鼠标 | 0.5ms | 专业电竞 |
| 4000Hz | 顶级电竞鼠标 | 0.25ms | 职业电竞 |
| 8000Hz | 极致电竞鼠标 | 0.125ms | 极限电竞 |

### 📊 评估指标
1. **平均值** - 轮询率的算术平均
2. **最小值** - 测试期间最低轮询率
3. **最大值** - 测试期间最高轮询率
4. **标准差** - 轮询率波动程度
5. **P95值** - 95%时间高于此值
6. **稳定性评分** - 综合评分（0-100）
7. **等级评定** - 优秀/良好/一般/差

---

## 🚀 快速开始

### 前提条件
- Python 3.8 或更高版本
- pip 包管理工具

### 安装步骤
```bash
# 1. 克隆仓库
git clone https://github.com/yourusername/mouse-polling-rate-tester.git
cd mouse-polling-rate-tester

# 2. 安装依赖
pip install -r requirements.txt

# 3. 运行工具
python mouse_polling_gui_pro.py

### 打包步骤

# 1. 安装 auto-py-to-exe tool
pip install auto-py-to-exe

# 2. 启动打包工具窗口
python -m auto_py_to_exe


