#  SPDX-FileCopyrightText: 2023 easyCrystallography contributors <crystallography@easyscience.software>
#  SPDX-License-Identifier: BSD-3-Clause
#  © 2022-2023  Contributors to the easyCore project <https://github.com/easyScience/easyCrystallography>
from __future__ import annotations

__author__ = "github.com/wardsimon"
__version__ = "0.1.0"

from typing import List, Optional, Dict

import numpy as np
from crysvue.visual.vispy.components import Arrow3D
from crysvue.logic.spins import SpinLogic

class Spin(Arrow3D, SpinLogic):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
