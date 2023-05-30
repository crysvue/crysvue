#  SPDX-FileCopyrightText: 2023 easyCrystallography contributors <crystallography@easyscience.software>
#  SPDX-License-Identifier: BSD-3-Clause
#  © 2022-2023  Contributors to the easyCore project <https://github.com/easyScience/easyCrystallography>

from __future__ import annotations

__author__ = "github.com/wardsimon"
__version__ = "0.1.0"


def rgb_to_hex(rgb: tuple) -> str:
    """
    Convert an RGB tuple to a hex string

    :param rgb: RGB tuple
    :return: Hex string
    """
    return '#%02x%02x%02x' % rgb


def hex_to_rgb(hex_str: str) -> tuple:
    """
    Convert a hex string to an RGB tuple

    :param hex_str: Hex string
    :return: RGB tuple
    """
    hex_str = hex_str.lstrip('#')
    return tuple(int(hex_str[i:i + 2], 16) for i in (0, 2, 4))
