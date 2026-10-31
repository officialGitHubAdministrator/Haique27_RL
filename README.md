# Haique27_RL (海雀27多旋翼强化学习控制系统)

Haique 27 是一套面向多旋翼无人机高机动飞行与自主控制的具身智能强化学习全栈系统。项目依托 NVIDIA Isaac Lab 高保真物理仿真器进行策略训练，并通过标准 ONNX 运行时闭环部署于机载嵌入式计算平台与 PX4 开源飞控。

> 📖 **项目文档与规格指南**：
> - 核心项目全景规格说明书：[docs/PROJECT_SPEC.md](docs/PROJECT_SPEC.md)
> - AI 助手协同上下文规范：[AGENTS.md](AGENTS.md)
> - 硬件电气清单与实测推力：[docs/HARDWARE_ARCHITECTURE.md](docs/HARDWARE_ARCHITECTURE.md)
> - PX4 飞控刷机与安全遥控通道：[docs/FLIGHT_CONTROL_PX4.md](docs/FLIGHT_CONTROL_PX4.md)
> - 虚实坐标系与数据通信契约：[docs/INTERFACE_CONTRACT.md](docs/INTERFACE_CONTRACT.md)

---

## 软件版本

- **操作系统**: Ubuntu 24.04 LTS (x86_64)
- **Python 运行时**: Python 3.12 (`.python-version` 锁定)
- **包管理器**: `uv`
- **仿真底座**: Isaac Sim 6.2.0.0 + Isaac Lab 3.0.0
- **深度学习核心**: PyTorch 2.11.0 + CUDA 13.0
- **并行物理计算**: NVIDIA Warp 1.17.0
- **RL 算法库**: RSL-RL (PPO)
- **飞控固件**: PX4 Autopilot v1.14.3 (运行于 MicoAir743)
- **通信中间件**: ROS 2 Humble + Micro-XRCE-DDS-Agent v2.4.1

---

## 环境同步与激活

### 1. 安装包管理器 uv
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

### 3. 激活开发环境
```bash
source /home/wang/IsaacLab/.venv/bin/activate
uv pip list
```

---

## 工作区目录结构

```text
Haique27_RL/
├── AGENTS.md                          # AI 协同上下文与项目规范
├── README.md                          # 仓库主页说明
├── docs/                              # 工程与算法规格文档
├── configs/                           # Isaac Lab 与 PX4 配置文件
├── assets/                            # 资产与测量数据 (包含测功台推力曲线)
├── scripts/                           # 训练与评估脚本入口
└── src/haique27_rl/                   # 核心 Python 算法源码包
```
