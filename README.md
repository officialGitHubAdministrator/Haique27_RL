# Haique27_RL (海雀27多旋翼强化学习控制系统)

Haique 27 是一套面向多旋翼无人机高机动飞行与自主控制的强化学习控制系统。

---

## 软件版本

- **操作系统**: Ubuntu 24.04 LTS
- **Python 运行时**: `Python 3.12
- **包管理器**: `uv`
- **仿真底座**: Isaac Sim 6.2.0.0 + Isaac Lab 3.0.0
- **深度学习核心**: PyTorch 2.11.0 + CUDA 13.0
- **并行物理计算**: NVIDIA Warp 1.17.0
- **RL 算法库**: RSL-RL (PPO)

---

## 环境同步

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
