from __future__ import annotations

from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import numpy.typing as npt

import numpy as np
import brille
from vispy.visuals.markers import MarkersVisual
from vispy.color import Color


class AtomsVisual(MarkersVisual):
    def __init__(self, atoms: List[List[int, npt.ArrayLike]],
                 spacegroup_str: str, extent: npt.ArrayLike = (1, 1, 1),
                 center: Optional[npt.ArrayLike] = None, **kwargs):

        if center is None:
            center = np.asarray(extent) / 2
        center = np.asarray(center)

        self.symmetry = brille.Symmetry(spacegroup_str)

        colors = []
        positions = []
        sizes = []
        self.atoms = {}
        ind = 0
        for atomic_numer, atom_fractional_coords in atoms:
            orbits, generators = self.generate_positions(np.asarray(atom_fractional_coords), extent)
            colors = colors + [Color('#' + COLOR_DATA[atomic_numer - 1])] * orbits.shape[0]
            self.atoms[ind] = {'positions': orbits, 'generators': generators}
            positions.append(orbits)
            sizes.append(RADIUS_DATA[atomic_numer - 1] * np.ones_like(orbits[:, 0]))
            ind += 1
        positions = np.vstack(positions) - center
        sizes = np.hstack(sizes)
        super().__init__(pos=positions,
                         size=sizes,
                         face_color=colors,
                         antialias=0,
                         spherical=True,
                         edge_color='white',
                         edge_width=0,
                         scaling=True,
                         **kwargs)

    def generate_positions(self, atom, extent):
        all_positions = []
        generators = []
        for z in np.arange(-1, extent[2] + 1):
            for y in np.arange(-1, extent[1] + 1):
                for x in np.arange(-1, extent[0] + 1):
                    for rot, trans in zip(self.symmetry.W, self.symmetry.w):
                        all_positions.append(np.matmul(rot, atom + [x, y, z]) + trans)
                        generators.append([rot, np.array([x, y, z]), trans])
        positions, indices = np.unique(np.array(all_positions), axis=0, return_index=True)
        generators = [generators[idx] for idx in indices]
        logic = np.all(positions <= extent, axis=1) & np.all(positions >= 0, axis=1)
        positions = positions[logic]
        generators = [generators[index] for index in np.where(logic)[0]]
        return positions, generators


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
