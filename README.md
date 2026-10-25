# Haique27_RL (海雀27多旋翼强化学习控制系统)

Haique 27 是一套面向多旋翼无人机高机动飞行与自主控制的具身智能强化学习全栈系统。项目采用**“虚实结合、双轨并行”**的开发模式，依托 NVIDIA Isaac Lab 高保真物理仿真器进行策略训练，并通过标准 ONNX 运行时闭环部署于机载嵌入式平台与 PX4 开源飞控。

---

## 团队四组协同架构

| 组别简称 | 组别全称 | 核心成员 | 核心交付物 |
| :---: | :--- | :--- | :--- |
| **【机体组】** | 机体结构与工装工程组 | 结构/机械 | 零共振碳纤机架、减震安装座、单轴/系留防炸测试工装 |
| **【电气组】** | 动力电气与硬件系统组 | 电路/电源 | 宽压防掉电供电系统、动力测功台推力/延迟标定数据 |
| **【航电组】** | 机载系统与航电组 | 嵌入式/电控 | PX4底层角速度闭环、ROS 2通信链路、ONNX机载推理、一键遥控安全救援 |
| **【策略组】** | 飞行控制律与智能策略组 | 算法/仿真 | Isaac Lab数字孪生模型、PPO策略训练、Sim-to-Real域随机化、ONNX模型 |

---

## 全队软硬件版本基准线 (Baseline v1.0)

为了杜绝版本冲突导致的通信故障或实机炸机，全队开发严格锚定以下版本：

### 1. 策略与仿真端（以主工作站为基准）
- **操作系统**: Ubuntu 24.04 LTS (x86_64)
- **Python 运行时**: `Python 3.12.x` (锁死于 `.python-version`)
- **包管理器**: `uv`
- **仿真底座**: Isaac Sim 6.2.0.0 + Isaac Lab 3.0.0
- **深度学习核心**: PyTorch 2.11.0 + CUDA 13.0
- **并行物理计算**: NVIDIA Warp 1.17.0
- **RL 算法库**: RSL-RL (PPO)

### 2. 机载与飞控端（Jetson Orin Nano / PX4）
- **机载系统**: JetPack 6.0 / 6.1 (Ubuntu 22.04 aarch64)
- **机载 Python**: `Python 3.10.x` (Ubuntu 22.04 默认)
- **机载中间件**: ROS 2 Humble Hawksbill (LTS)
- **模型推理**: ONNX Runtime (GPU) 1.17.x
- **飞控固件**: PX4 Autopilot `v1.14.3` (Release Tag)
- **微通信代理**: Micro-XRCE-DDS-Agent `v2.4.1`
- **ROS 2 消息包**: `px4_msgs` (`release/1.14` 分支)
- **遥控链路**: ExpressLRS (ELRS) `v3.3.x`
- **电调协议**: DShot600 (启用双向 RPM 回传)

---

## 虚实接口契约规范 (Interface Contract)

全链路严格遵循以下数据协议：
1. **机体坐标系**: 统一采用 ROS 标准 **FLU（前-左-上）**，进飞控前由航电组负责转为 PX4 原生 **FRD（前-右-下）**。
2. **四元数姿态顺序**: 所有跨进程/网络传输统一遵循 **`[w, x, y, z]`**（实部在首位）。
3. **模型导出参数**: 策略组导出 ONNX 时必须显式声明 **`opset_version = 16`**。
4. **控制频率**: 策略回环与飞控下发频率统一固定为 **50Hz** (20ms 周期)。

---

## 快速上手与环境同步

### 1. 安装极速包管理器 uv
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. 克隆仓库并同步环境
```bash
git clone git@github.com:officialGitHubAdministrator/Haique27_RL.git
cd Haique27_RL

# 依赖与环境锁文件完全就绪后，直接同步
uv sync
```
