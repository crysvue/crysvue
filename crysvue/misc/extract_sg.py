#  SPDX-FileCopyrightText: 2023 easyCrystallography contributors <crystallography@easyscience.software>
#  SPDX-License-Identifier: BSD-3-Clause
#  © 2022-2023  Contributors to the easyCore project <https://github.com/easyScience/easyCrystallography>

__author__ = "github.com/wardsimon"
__version__ = "0.1.0"

substr ='static const Spacegroup ALL_SPACEGROUPS[] = {'


def remove_quotes(input_str: str):
    tokens = input_str.split('"')
    return tokens[1] if len(tokens[1]) > 0 else None

def generate_entry(input_str: str):
    tokens = input_str.split(',')
    IT_number = int(tokens[0])
    SchoenfliesSymbol = remove_quotes(tokens[1])
    HallSymbol = remove_quotes(tokens[2])
    IT_SG_Name = remove_quotes(tokens[3])
    HM_SG_Name = remove_quotes(tokens[4])
    C_IT_SG_Name = remove_quotes(tokens[5])
    Choice = remove_quotes(tokens[6])
    Centering = tokens[7][tokens[7].find(':')+2:]  # In the form "' Bravais::X'" where we are interested in X
    PointGroupNumber = int(tokens[8])
    HallNumber = int(tokens[9])


with open('spg_database.cpp', 'r') as f:
    data = f.read()
data = data[data.find(substr)+len(substr):].split('\n')[1:]
data = [generate_entry(dat[3:-2]) for dat in data]



