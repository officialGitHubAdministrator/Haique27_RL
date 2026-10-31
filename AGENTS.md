# AGENTS.md - Haique27_RL AI Assistant Context & Guidelines

> **重要提示（致后续新开会话的 AI 助手 / Pair Programmer）**：
> 本文件为 **Haique27_RL（海雀27多旋翼强化学习自主控制系统）** 的核心上下文规范。
> 当用户在此工作区开启新会话时，**必须首先读取并严格遵循本文件定义的技术基准、硬件参数与控制架构约束**。

---

## 1. 项目核心愿景与任务定义

- **项目名称**：海雀27（Haique 27）
- **核心任务**：基于 **NVIDIA Isaac Lab (PPO)** 训练具备高动态敏捷性、抗扰动能力的四旋翼无人机姿态与轨迹跟踪智能策略，通过标准 **ONNX** 离线导出，闭环部署至机载嵌入式计算平台（Jetson Orin Nano / RK3588），并通过 **PX4 (v1.14.3)** 开源飞控控制 7 寸碳纤实机实现稳定自主飞行。
- **开发策略（两阶段战略，切勿激进跨越）**：
  - **阶段一（第 1 ~ 2 个月）**：**纯 PX4 传统飞控实体验证**。不上 ROS 2，不跑神经网络。先使用 EdgeTX 遥控器验证手动自稳（Stabilized）、定高（Altitude）、GPS 定点（Position）、动力系统匹配度与结构减震健康度。
  - **阶段二（第 2 个月后）**：**离板闭环与策略部署**。硬件健康度 100% 确认后，接入机载计算机、启动 Micro-XRCE-DDS 通信链路、加载 ONNX 模型进行 Offboard 接管飞行。

---

## 2. 严禁逾越的技术红线 (Non-negotiable Architectural Constraints)

1. **严禁端到端直接输出电机 PWM（禁止输出 4 电机原始占空比）**：
   - 团队必须采用 **“分层控制架构（Hierarchical Control）”**：
     - **上层（RL 策略网络）**：运行在机载端（50Hz），输出期望机体角速度（Desired Angular Rates $\boldsymbol{\omega}_{cmd}$）或期望滚转/俯仰角 + 偏航角速度，以及归一化总推力（Normalized Collective Thrust $\tau_{cmd} \in [0, 1]$）。
     - **下层（PX4 飞控内环）**：运行在 MicoAir743 飞控端（250Hz~400Hz），负责微秒级陀螺仪滤波、PID 姿态角速度闭环及 DShot600 电机混控。
2. **遥控器安全生命线红线**：
   - 必须使用运行 **EdgeTX** 系统的遥控器（如 RadioMaster TX12 MKII 或 Pocket，内置 ELRS 2.4G）。
   - 严禁使用玩具级无屏控（如 T8L）。
   - 遥控器必须配置：
     - 独立瞬时/两档 **急停锁电机开关（Kill Switch / Emergency Motor Cutoff）**；
     - 独立三档 **飞行模式开关（Stabilized $\to$ Position $\to$ Offboard RL）**；
     - 一旦策略发散或发生姿态倾覆，操作手必须在 0.2 秒内切回手动或打下急停。
3. **坐标系与四元数契约**：
   - 仿真、ROS 2 与机载端统一使用 **FLU（前-左-上，Forward-Left-Up）**。
   - PX4 原生为 **FRD（前-右-下，Forward-Right-Down）**，下发与接收时必须做轴系反转变换。
   - 所有四元数传输统一遵循 **`[w, x, y, z]`**（实部在首位）。
4. **控制频率与时间延迟**：
   - 策略控制回环固定为 **50Hz**（周期 20ms）。
   - Isaac Lab 仿真中必须引入 **20ms ~ 45ms** 的物理时延缓冲（Domain Randomization: Action Delay Buffer），以覆盖机载推理、ROS 2 序列化及 UART/DDS 通信开销。

---

## 3. 软硬件系统全景基准线 (Baseline v1.0)

### 3.1 训练与仿真宿主机（Host Workstation）
- **操作系统**: Ubuntu 24.04 LTS (x86_64)
- **Python**: `3.12.x`（环境由 `uv` 管理，已锁定在 `uv.lock` 和 `.python-version`）
- **仿真环境**: NVIDIA Isaac Lab 3.0.0 (Isaac Sim 6.2.0.0)
- **核心计算栈**: PyTorch 2.11.0 + CUDA 13.0, NVIDIA Warp 1.17.0
- **算法依赖**: RSL-RL (PPO 实现)

### 3.2 实机机体与电气系统（Hardware & Power）
- **机架**: GEPRC 7 英寸碳纤穿越机机架（轴距约 295~320mm，机臂厚度 5~6mm）
- **电机与桨叶**: 2807 或 T-Motor F90 1300KV 无刷电机 + HQProp 70403 / Gemfan 7042 3叶桨
- **电池组**: 6S 22.2V LiPo (3000mAh~4000mAh, 100C 放电率)
- **实测动力学数据（HQ 70403 + F90 1300KV）**:
  - 单发最大推力：$2360\text{g}$，四发总推力：$9440\text{g}$
  - 整机估算全备重量 (AUW)：约 $1200\text{g}$（含电池与机载电脑）
  - **整机推重比 (TWR)**：$7.87 : 1$（极高机动动力，切记悬停油门仅约 **28%**，推力拟合度 $R^2 = 0.9957$）
- **电调 (ESC)**: 55A ~ 60A 四合一电调，支持 DShot600 及双向 RPM 遥测回传
- **降压供电**: 6S 宽压转 5V/5A 或 12V/5A 独立 DC-DC 稳压模块（严禁机载电脑与电调共用同一未经滤波的电源线路）

### 3.3 飞控与机载系统（Avionics & Onboard）
- **主飞控 (FC)**: **MicoAir743 v1.3**（基于 STM32H743VIT6，30.5×30.5mm 飞塔安装位，原生支持 PX4 `micoair_h743-v1.14.3.px4`）
  - UART1: 机载电脑伴随计算机通信（TELEM1 / Micro-XRCE-DDS）
  - UART3: M9N GPS + 磁罗盘模块
  - UART6: ELRS 接收机（CRSF 协议）
- **机载电脑**: Jetson Orin Nano (8GB) 或 Orange Pi 5 (RK3588 8GB)
  - 存储: SK Hynix PC601 256GB NVMe SSD
  - 网络: Intel AX200/AX210 WiFi 6 网卡
- **通信与中间件**: ROS 2 Humble LTS + Micro-XRCE-DDS-Agent `v2.4.1` + `px4_msgs` (`release/1.14` 分支)
- **遥控接收**: ExpressLRS (ELRS 2.4G) v3.3.x

---

## 4. 团队四组协同分工与核心交付物

| 组别 | 核心交付物 | 当前状态与近期任务 |
| :--- | :--- | :--- |
| **【机体组】** | 7寸碳纤整机装配、TPU 减震打印件、单轴/双轴防炸实物测试台架 | 选定 GEPRC 7寸机架，制作电机防震垫与单轴拉力架 |
| **【电气组】** | 6S 动力分配、独立降压滤波、MT10PRO 测功台电机推力/电流标定曲线 | 标定 F90+70403 数据（悬停点 28%），制作防掉电供电线路 |
| **【航电组】** | MicoAir743 刷入 PX4 1.14.3、QGC 调参、DShot600 配置、EdgeTX 遥控安全通道配置 | 刷机验证、飞控接线、传统模式试飞，待硬件稳定后接 ROS 2 |
| **【策略组】** | Isaac Lab 数字孪生环境、PPO 控制律训练、时延/推力域随机化、ONNX 导出 | 基于测功台推力曲线构建 MDP，训练角速度闭环策略，导出 opset 16 |

---

## 5. 项目工作区目录规范

```text
Haique27_RL/
├── AGENTS.md                          # [本文件] AI 协同与项目全局上下文规范
├── README.md                          # 仓库主页与团队快速上手指南
├── pyproject.toml / uv.lock           # 依赖与环境锁文件 (Python 3.12)
├── docs/                              # 工程与算法规格文档
│   ├── PROJECT_SPEC.md                # 详尽项目规格说明与两阶段开发规划
│   ├── HARDWARE_ARCHITECTURE.md       # 硬件电气清单、引脚定义与测功曲线
│   ├── FLIGHT_CONTROL_PX4.md          # MicoAir743 刷机、接线与 QGC 参数指南
│   └── INTERFACE_CONTRACT.md          # 坐标系、四元数、ROS 2 与 ONNX 通信契约
├── configs/                           # 配置文件
│   ├── env/                           # Isaac Lab 环境与 PPO 奖励超参数配置
│   └── px4/                           # PX4 飞控参数导出与备份
├── assets/                            # 资产与测量数据
│   └── thrust_bench/                  # MT10PRO 动力测功实测 JSON 数据
├── scripts/                           # 脚本入口
│   ├── train.py                       # PPO 训练主入口
│   ├── eval.py                        # 策略评估与实时渲染
│   └── export_onnx.py                 # ONNX 标准模型导出脚本
└── src/haique27_rl/                   # 核心 Python 算法源码
    ├── envs/                          # Isaac Lab MDP 强化学习环境定义
    ├── models/                        # 策略网络架构定义
    └── utils/                         # 坐标系转换、滤波与数学工具库
```

---

## 6. 新开会话的开发者自检与问答指引

当用户在新的会话中提出以下方向的问题时，优先调取对应文档：
1. **飞控与遥控问题** $\to$ 参考 `docs/FLIGHT_CONTROL_PX4.md`，重点检查急停开关与 UART 引脚分配；
2. **硬件与动力选型** $\to$ 参考 `docs/HARDWARE_ARCHITECTURE.md`，牢记推重比接近 8:1，悬停油门 28%；
3. **算法训练与仿真** $\to$ 参考 `docs/PROJECT_SPEC.md` 与 `configs/env/`，必须加 $20\sim 45\text{ms}$ 时延域随机化；
4. **通信与部署问题** $\to$ 参考 `docs/INTERFACE_CONTRACT.md`，坚守 FLU/FRD 转换与 `[w,x,y,z]` 四元数格式。
