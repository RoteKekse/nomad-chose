import pandas as pd
import numpy as np
from datetime import datetime
import chardet
# import glob

from baseclasses.solar_energy.mpp_tracking import MPPTrackingProperties


def get_parameter(d, key):
    return d[key] if key in d else None


def get_mpp_data(filename, encoding='utf-8'):

    df = pd.read_csv(
        filename,
        skiprows=42,
        sep='\t',
        # index_col=0,
        encoding=encoding,
        engine='python')
    header_dict = {}

    return header_dict, df


def get_mpp_archive(header_dict, df, mpp_entitiy, mainfile=None):

    mpp_entitiy.time = np.array(df["Time (hours) "])
    mpp_entitiy.power_density = np.array(df["P (mWcm-2)"])
    mpp_entitiy.voltage = np.array(df["V (V)"])
    mpp_entitiy.current_density = np.array(df["J (mAcm-2)"])
    # mpp_entitiy.efficiency = np.array(df["PCE"])
    if mainfile is not None:
        mpp_entitiy.data_file = mainfile

    datetime_str = get_parameter(header_dict, "datetime")
    datetime_object = datetime.strptime(
        datetime_str, '%Y-%m-%d %I:%M %p')
    mpp_entitiy.datetime = datetime_object.strftime(
        "%Y-%m-%d %H:%M:%S.%f")

    properties = MPPTrackingProperties()
    properties.start_voltage_manually = get_parameter(
        header_dict, "start_voltage_manually") == "true"
    properties.perturbation_frequency = get_parameter(
        header_dict, "perturbation_frequency_[s]")
    properties.sampling = get_parameter(header_dict, "sampling")
    properties.perturbation_voltage = get_parameter(
        header_dict, "perturbation_voltage_[v]")
    properties.perturbation_delay = get_parameter(
        header_dict, "perturbation_delay_[s]")
    properties.time = get_parameter(header_dict, "time_[s]")
    properties.status = get_parameter(header_dict, "status")
    properties.last_pce = get_parameter(header_dict, "last_pce_[%]")
    properties.last_vmpp = get_parameter(header_dict, "last_vmpp_[v]")

    mpp_entitiy.properties = properties


# file = "/home/a2853/Documents/Projects/nomad/chose/18.33.10/000_2023_10_19_18.33.10_1A_3C_C1_1_Tracking.txt"
# with open(file, "br") as f:
#     encoding = chardet.detect(f.read())["encoding"]
# print(encoding)
# get_mpp_data(file, encoding)
