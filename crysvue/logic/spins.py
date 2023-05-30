#  SPDX-FileCopyrightText: 2023 easyCrystallography contributors <crystallography@easyscience.software>
#  SPDX-License-Identifier: BSD-3-Clause
#  © 2022-2023  Contributors to the easyCore project <https://github.com/easyScience/easyCrystallography>

__author__ = "github.com/wardsimon"
__version__ = "0.1.0"

from typing import Optional

import numpy as np


class SpinLogic:
    def __init__(self, vector: np.ndarray):
        self._spin_base_vector = vector

    @property
    def arrow_base_position(self):
        return - np.linalg.norm(self._spin_base_vector) / 2
