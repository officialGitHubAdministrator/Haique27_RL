# 虚实接口契约规范 (Interface Contract)

## 1. 坐标系转换约定

* **ROS 2 & Isaac Lab**: **FLU 坐标系** (X-前, Y-左, Z-上)。
* **PX4 原生内部**: **FRD 坐标系** (X-前, Y-右, Z-下)。

### 转换公式
对于机体角速度向量 $\boldsymbol{\omega} = [\omega_x, \omega_y, \omega_z]^T$：
$$\boldsymbol{\omega}_{FRD} = \begin{bmatrix} 1 & 0 & 0 \\ 0 & -1 & 0 \\ 0 & 0 & -1 \end{bmatrix} \boldsymbol{\omega}_{FLU} = [\omega_x, -\omega_y, -\omega_z]^T$$

对于归一化推力 $\tau_{cmd} \in [0, 1]$：
* PX4 `vehicle_rates_setpoint` 的 `thrust_body` 向量定义在 FRD 体系下（推力向上指向负 Z 轴）：
  $$\mathbf{F}_{FRD} = [0.0, 0.0, -\tau_{cmd}]^T$$

---

## 2. 四元数姿态标准

所有姿态四元数（不论在仿真、网络通信还是机载模型输入中）一律遵循 **Hamilton 约定，实部在前**：
$$\mathbf{q} = [w, x, y, z]^T, \quad \|\mathbf{q}\| = 1$$

---

## 3. ONNX 强化学习策略接口规范

* **模型导出参数**:
  * 框架: PyTorch $\to$ ONNX
  * Opset Version: **16**
* **输入张量 (Input Tensor)**:
  * 名字: `obs`
  * 形状: `[batch_size, 17]`
  * 字段构成（全部在机体系 FLU 下标定归一化）：
    1. `q_body` (4维): 当前姿态四元数 $[w, x, y, z]$
    2. `v_body` (3维): 当前机体系线速度 $[v_x, v_y, v_z]$
    3. `w_body` (3维): 当前机体系角速度 $[\omega_x, \omega_y, \omega_z]$
    4. `pos_err_body` (3维): 目标路点在当前机体系下的相对位置偏差 $[\Delta x, \Delta y, \Delta z]$
    5. `last_act` (4维): 上一步执行的控制动作 $[\omega_{x, cmd}, \omega_{y, cmd}, \omega_{z, cmd}, \tau_{cmd}]$
* **输出张量 (Output Tensor)**:
  * 名字: `action`
  * 形状: `[batch_size, 4]`
  * 字段构成:
    1. `roll_rate_cmd`: 期望横滚角速度 (rad/s)
    2. `pitch_rate_cmd`: 期望俯仰角速度 (rad/s)
    3. `yaw_rate_cmd`: 期望偏航角速度 (rad/s)
    4. `collective_thrust`: 归一化总推力 $\tau_{cmd} \in [0, 1]$
