# PX4 飞控配置与 EdgeTX 遥控安全通道指南

## 1. MicoAir743 飞控固件烧录

1. **固件获取**:
   * MicoAir 官方开源维护了 PX4 适配代码，固件文件名：`micoair_h743-v1.14.3.px4`。
2. **烧录步骤 (QGroundControl)**:
   * 启动 QGroundControl (QGC)；
   * 用 USB-C 数据线连接 MicoAir743 至电脑；
   * 进入 `Vehicle Setup` $\to$ `Firmware`；
   * 勾选 `Advanced settings`，下拉选择 `Custom firmware file`；
   * 载入 `micoair_h743-v1.14.3.px4`，等待烧录与自动重启；
   * 完成传感器校准（陀螺仪、加速度计、磁力计、水平校准）。

---

## 2. EdgeTX 遥控通道与安全开关映射规范

在 EdgeTX 遥控器（TX12 MKII 或 Pocket）中，必须建立以下标准模型通道映射：

| 通道 | 映射功能 | 物理按键 / 摇杆 | 逻辑与触发定义 |
| :---: | :---: | :---: | :--- |
| **CH1** | 横滚 (Roll) | 右摇杆左右 (Mode 2) | 控制机体横滚姿态 / 角速度 |
| **CH2** | 俯仰 (Pitch) | 右摇杆上下 (Mode 2) | 控制机体俯仰姿态 / 角速度 |
| **CH3** | 油门 (Throttle) | 左摇杆上下 (Mode 2) | 归一化推力输入 |
| **CH4** | 偏航 (Yaw) | 左摇杆左右 (Mode 2) | 控制偏航角速度 |
| **CH5** | **解锁 (Arm)** | 独立两档开关 (如 SA) | 上拨: Disarmed (锁定) / 下拨: Armed (解锁) |
| **CH6** | **模式切换 (Flight Mode)** | **独立三档开关 (如 SB)** | **上档 (UP)**: 纯手动自稳 (Stabilized)<br>**中档 (MID)**: GPS 定点悬停 (Position)<br>**下档 (DOWN)**: 算法离板接管 (Offboard Mode) |
| **CH7** | **急停锁死 (Kill Switch)** | **独立高敏两档/自复位开关 (如 SF/SH)** | **全系统最高优先级**。无论处于何种模式，拨下立即瞬时切断 4 电机动力（防止失控与姿态翻转割伤）。 |
| **CH8** | 一键返航 (RTL) | 独立两档开关 (如 SC) | 触发自动返航悬停 |

---

## 3. PX4 Offboard 模式安全看门狗机制

PX4 原生具备严格的离板失联保护。当无人机切入 Offboard（CH6 下档）由机载算法控制时：
1. **心跳超时保护**:
   * PX4 参数 `COM_OF_LOSS_T` 默认设置为 `0.5s`（500ms）。
   * 若 ROS 2 节点或机载电脑崩溃超过 500ms 未发送有效指令，飞控将自动降级为定点（Position）或降落（Land），绝不乱窜。
2. **操作手一键接管**:
   * 操作手只要将 CH6 从【下档】拨回【中档】或【上档】，控制权在 $\le 5\text{ms}$ 内立刻切回人工操纵。
