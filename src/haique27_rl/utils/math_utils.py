"""Coordinate frame and quaternion math utilities for Haique27 RL."""

from typing import Tuple
import torch


def flu_to_frd_rates(rates_flu: torch.Tensor) -> torch.Tensor:
    """Convert body angular rates from FLU (Forward-Left-Up) to FRD (Forward-Right-Down).

    Args:
        rates_flu: Tensor of shape (..., 3) containing [roll_rate, pitch_rate, yaw_rate] in FLU.

    Returns:
        Tensor of shape (..., 3) containing [roll_rate, -pitch_rate, -yaw_rate] in FRD.
    """
    scale = torch.tensor([1.0, -1.0, -1.0], dtype=rates_flu.dtype, device=rates_flu.device)
    return rates_flu * scale


def frd_to_flu_rates(rates_frd: torch.Tensor) -> torch.Tensor:
    """Convert body angular rates from FRD (Forward-Right-Down) to FLU (Forward-Left-Up).

    Args:
        rates_frd: Tensor of shape (..., 3) containing [roll_rate, pitch_rate, yaw_rate] in FRD.

    Returns:
        Tensor of shape (..., 3) in FLU.
    """
    return flu_to_frd_rates(rates_frd)


def normalize_quaternion(quat: torch.Tensor) -> torch.Tensor:
    """Ensure quaternion [w, x, y, z] is normalized to unit length.

    Args:
        quat: Tensor of shape (..., 4) where index 0 is scalar 'w'.

    Returns:
        Normalized quaternion tensor of shape (..., 4).
    """
    norm = torch.linalg.norm(quat, dim=-1, keepdim=True)
    return quat / torch.clamp(norm, min=1e-8)
