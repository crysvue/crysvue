#  SPDX-FileCopyrightText: 2023 easyCrystallography contributors <crystallography@easyscience.software>
#  SPDX-License-Identifier: BSD-3-Clause
#  © 2022-2023  Contributors to the easyCore project <https://github.com/easyScience/easyCrystallography>

from __future__ import annotations

__author__ = "github.com/wardsimon"
__version__ = "0.1.0"

import brille
import numpy as np

from crysvue.misc.color import rgb_to_hex
from typing import List, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    import numpy.typing as npt


class AtomLogic:
    def __init__(self, position, size, color, symmetry_str):
        self._symmetry = brille.Symmetry(symmetry_str)
        self._color = color
        self._size = size
        self._position = np.asarray(position)
        self._dataset = {
            'positions':  [],
            'generators': [],
            'colors':     [],
            'sizes':      []
        }
        self._generate_full_data()

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value: Union[str, tuple]):
        if not isinstance(value, str):
            value = rgb_to_hex(value)
        self._color = value
        self._dataset['colors'] = [value] * len(self._dataset['positions'])

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        self._size = value
        self._dataset['sizes'] = [value] * len(self._dataset['positions'])

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value: npt.ArrayLike):
        self._position = np.asarray(value)
        self._generate_full_data()

    @property
    def symmetry(self):
        return self._symmetry

    @symmetry.setter
    def symmetry(self, symmetry_str: str):
        self._symmetry = brille.Symmetry(symmetry_str)

    @property
    def positions(self):
        return self._dataset['positions']

    @property
    def generators(self):
        return self._dataset['generators']

    @property
    def colors(self):
        return self._dataset['colors']

    @property
    def sizes(self):
        return self._dataset['sizes']

    def generate_full_data(self, extent):
        return self._generate_full_data(extent, set_data=False)

    def _generate_full_data(self, extent=(1, 1, 1), set_data=True):

        positions, generators = self.generate_positions(self._position, extent)

        dataset = {
            'positions':  positions,
            'generators': generators,
            'colors':     [self._color] * len(positions),
            'sizes':      [self._size] * len(positions)
        }
        if set_data:
            self._dataset = dataset
        else:
            return dataset

    def generate_positions(self, atom, extent):
        all_positions = []
        generators = []
        for z in np.arange(-1, extent[2] + 1):
            for y in np.arange(-1, extent[1] + 1):
                for x in np.arange(-1, extent[0] + 1):
                    for rot, trans in zip(self._symmetry.W, self._symmetry.w):
                        all_positions.append(np.matmul(rot, atom + [x, y, z]) + trans)
                        generators.append([rot, np.array([x, y, z]), trans])
        positions, indices = np.unique(np.array(all_positions), axis=0, return_index=True)
        generators = [generators[idx] for idx in indices]
        logic = np.all(positions <= extent, axis=1) & np.all(positions >= 0, axis=1)
        positions = positions[logic]
        generators = [generators[index] for index in np.where(logic)[0]]
        return positions, generators


class AtomsLogic:

    def __init__(self, position, size, color, symmetry_str):
        self._atoms = []
        for pos, sz, c in zip(position, size, color):
            self._atoms.append(AtomLogic(pos, sz, c, symmetry_str))

    @staticmethod
    def _from_atom_name(positions, atom_label, symmetry_str):
        sizes = []
        colors = []
        for atom_str in atom_label:
            if atom_str in ELEMENT_DATA:
                idx = ELEMENT_DATA.index(atom_str)
                sizes.append(RADIUS_DATA[idx])
                colors.append('#' + COLOR_DATA[idx])
            else:
                raise ValueError(f"Atom {atom_str} not found in ELEMENT_DATA")
        return positions, sizes, colors, symmetry_str

    @classmethod
    def from_atom_name(cls, positions, atom_label, symmetry_str, **kwargs):
        positions, sizes, colors, symmetry_str = cls._from_atom_name(positions, atom_label, symmetry_str)
        return cls(positions, sizes, colors, symmetry_str, **kwargs)

    @staticmethod
    def _from_atom_number(positions, atom_number, symmetry_str):
        sizes = []
        colors = []
        for atom_num in atom_number:
            if atom_num < len(ELEMENT_DATA):
                sizes.append(RADIUS_DATA[atom_num - 1])
                colors.append('#' + COLOR_DATA[atom_num - 1])
            else:
                raise ValueError(f"Atom {atom_num} is not valid")
        return positions, sizes, colors, symmetry_str

    @classmethod
    def from_atom_number(cls, positions, atom_number, symmetry_str, **kwargs):
        positions, sizes, colors, symmetry_str = cls._from_atom_number(positions, atom_number, symmetry_str)
        return cls(positions, sizes, colors, symmetry_str, **kwargs)

    @property
    def atoms(self):
        return self._atoms

    @property
    def positions(self):
        return np.concatenate([atom.positions for atom in self._atoms])

    @property
    def generators(self):
        return np.concatenate([atom.generators for atom in self._atoms])

    @property
    def colors(self):
        return np.concatenate([atom.colors for atom in self._atoms])

    @property
    def sizes(self):
        return np.concatenate([atom.sizes for atom in self._atoms])

    def generate_full_dataset(self, extent):
        dataset = self._atoms[0].generate_full_data(extent)
        for atom in self._atoms[1:]:
            this_dataset = atom.generate_full_data(extent)
            dataset['sizes'] += this_dataset['sizes']
            dataset['colors'] += this_dataset['colors']
            dataset['positions'] = np.concatenate([dataset['positions'], this_dataset['positions']])
            dataset['generators'] += this_dataset['generators']
        return dataset


COLOR_DATA = '#FFFFFF#D9FFFF#CC80FF#C2FF00#FFB5B5#909090#3050F8#FF0D0D#90E050#B3E3F5#AB5CF2#8AFF00#BFA6A6#F0C8A0' \
             '#FF8000#FFFF30#1FF01F#80D1E3#8F40D4#3DFF00#E6E6E6#BFC2C7#A6A6AB#8A99C7#9C7AC7#E06633#F090A0#50D050' \
             '#C88033#7D80B0#C28F8F#668F8F#BD80E3#FFA100#A62929#5CB8D1#702EB0#00FF00#94FFFF#94E0E0#73C2C9#54B5B5' \
             '#3B9E9E#248F8F#0A7D8C#006985#C0C0C0#FFD98F#A67573#668080#9E63B5#D47A00#940094#429EB0#57178F#00C900' \
             '#70D4FF#FFFFC7#D9FFC7#C7FFC7#A3FFC7#8FFFC7#61FFC7#45FFC7#30FFC7#1FFFC7#00FF9C#00E675#00D452#00BF38' \
             '#00AB24#4DC2FF#4DA6FF#2194D6#267DAB#266696#175487#D0D0E0#FFD123#B8B8D0#A6544D#575961#9E4FB5#AB5C00' \
             '#754F45#428296#420066#007D00#70ABFA#00BAFF#00A1FF#008FFF#0080FF#006BFF#545CF2#785CE3#8A4FE3#A136D4' \
             '#B31FD4#B31FBA#B30DA6#BD0D87#C70066#CC0059#D1004F#D90045#E00038#E6002E#EB0026#000000#000000#000000' \
             '#000000#000000#000000#000000#000000#000000'.split(
    '#')[1:]

RADIUS_DATA = [0.37,
               0.32,
               0.90,
               0.50,
               0.32,
               0.77,
               0.75,
               1.26,
               1.18,
               0.38,
               1.21,
               0.86,
               0.60,
               1.11,
               1.06,
               1.84,
               1.67,
               0.71,
               1.52,
               1.20,
               0.95,
               0.74,
               0.81,
               0.75,
               0.81,
               0.75,
               0.78,
               0.70,
               0.70,
               0.88,
               0.69,
               1.22,
               1.19,
               1.98,
               1.95,
               0.88,
               1.70,
               1.35,
               1.09,
               0.86,
               0.82,
               0.78,
               0.72,
               0.76,
               0.74,
               0.90,
               1.08,
               1.09,
               0.94,
               1.41,
               1.38,
               2.21,
               2.06,
               1.08,
               1.85,
               1.52,
               1.40,
               1.30,
               1.20,
               1.18,
               1.17,
               1.15,
               1.25,
               1.13,
               1.12,
               1.10,
               1.10,
               1.08,
               1.07,
               1.15,
               1.05,
               0.85,
               0.83,
               0.76,
               0.72,
               0.70,
               0.76,
               0.82,
               1.00,
               1.16,
               1.48,
               1.33,
               1.46,
               1.08,
               0.76,
               1.20,
               1.00,
               1.00,
               1.00,
               1.00,
               1.00,
               1.00,
               1.00,
               1.00,
               1.00,
               1.00,
               1.00,
               1.00,
               1.00,
               1.00,
               1.00,
               1.00,
               1.00,
               1.00,
               1.00,
               1.00,
               1.00,
               1.00,
               1.00,
               1.00,
               1.00,
               1.00,
               1.00]

ELEMENT_DATA = ["H",
                "He",
                "Li",
                "Be",
                "B",
                "C",
                "N",
                "O",
                "F",
                "Ne",
                "Na",
                "Mg",
                "Al",
                "Si",
                "P",
                "S",
                "Cl",
                "Ar",
                "K",
                "Ca",
                "Sc",
                "Ti",
                "V",
                "Cr",
                "Mn",
                "Fe",
                "Co",
                "Ni",
                "Cu",
                "Zn",
                "Ga",
                "Ge",
                "As",
                "Se",
                "Br",
                "Kr",
                "Rb",
                "Sr",
                "Y",
                "Zr",
                "Nb",
                "Mo",
                "Tc",
                "Ru",
                "Rh",
                "Pd",
                "Ag",
                "Cd",
                "In",
                "Sn",
                "Sb",
                "Te",
                "I",
                "Xe",
                "Cs",
                "Ba",
                "La",
                "Ce",
                "Pr",
                "Nd",
                "Pm",
                "Sm",
                "Eu",
                "Gd",
                "Tb",
                "Dy",
                "Ho",
                "Er",
                "Tm",
                "Yb",
                "Lu",
                "Hf",
                "Ta",
                "W",
                "Re",
                "Os",
                "Ir",
                "Pt",
                "Au",
                "Hg",
                "Tl",
                "Pb",
                "Bi",
                "Po",
                "At",
                "Rn",
                "Fr",
                "Ra",
                "Ac",
                "Th",
                "Pa",
                "U",
                "Np",
                "Pu",
                "Am",
                "Cm",
                "Bk",
                "Cf",
                "Es",
                "Fm",
                "Md",
                "No",
                "Lr",
                "Rf",
                "Db",
                "Sg",
                "Bh",
                "Hs",
                "Mt",
                "Ds",
                "Rg",
                "Cn",
                "Nh",
                "Fl",
                ]
