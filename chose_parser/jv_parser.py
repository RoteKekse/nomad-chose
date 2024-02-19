#
# Copyright The NOMAD Authors.
#
# This file is part of NOMAD. See https://nomad-lab.eu for further info.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import chardet
import pandas as pd
import numpy as np
import ast


def get_jv_data(filename, encoding='utf-8'):
    # Block to clean up some bad characters found in the file which gives
    # trouble reading.

    df = pd.read_csv(
        filename,
        skiprows=42,
        header=[0, 1],
        nrows=2,
        sep='\t',
        index_col=0,
        engine='python',
        encoding=encoding)

    df_header = pd.read_csv(
        filename,
        skiprows=11,
        nrows=8,
        header=None,
        sep='\t',
        index_col=0,
        encoding=encoding,
        engine='python')

    df_curves = pd.read_csv(
        filename,
        skiprows=46,
        on_bad_lines='skip',
        sep='\t',
        encoding=encoding,
        engine='python')
    df_curves = df_curves.dropna(how='all', axis=1)

    df_header.replace([np.inf, -np.inf, np.nan], 0, inplace=True)
    df.replace([np.inf, -np.inf, np.nan], 0, inplace=True)

    jv_dict = {}
    jv_dict['active_area'] = float(df_header.iloc[7, 0])

    jv_dict['J_sc'] = list(df["Jsc"]["mA/cm²"])
    jv_dict['V_oc'] = list(df["Voc"]["V"])
    jv_dict['Fill_factor'] = list(df["FF"]["%"])
    jv_dict['Efficiency'] = list(df["Eff"]["%"])
    jv_dict['P_MPP'] = list(df["P_MPP"]["mW/cm²"])
    jv_dict['J_MPP'] = list(df["J_MPP"]["mA/cm²"])
    jv_dict['U_MPP'] = list(df["V_MPP"]["V"])
    jv_dict['R_ser'] = list(df["Rs"]["Ohm"])
    jv_dict['R_par'] = list(df["R//"]["Ohm"])

    jv_dict['jv_curve'] = []

    scan_direction = ["FW", "RV"] if str(df_header.iloc[3, 0]).strip() == "FW->RV" else ["RV", "FW"]
    for column in range(0, len(df_curves.columns), 2):
        jv_dict['jv_curve'].append({'name': scan_direction[int(column/2) % 2] + " " + df_curves.columns[column],
                                    'voltage': df_curves[df_curves.columns[column]].values,
                                    'current_density': df_curves[df_curves.columns[column+1]].values})

    return jv_dict


# file = "/home/a2853/Documents/Projects/nomad/chose/18.33.10/001_2023_10_19_18.33.25_1A_3C_C1_1_JV.txt"
# with open(file, "br") as f:
#     encoding = chardet.detect(f.read())["encoding"]
# print(encoding)
# get_jv_data(file, encoding)
