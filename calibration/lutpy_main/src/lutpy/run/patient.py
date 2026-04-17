import time

from pathlib import Path
import numpy as np
import os
import time

from src.lutpy.dicom.import_image_volume_as_array import dicom_to_array
from src.lutpy.spr_lut.get_spr_lut import get_spr_lut
from src.lutpy.spr_map.get_spr_map import get_spr_map
from src.lutpy.time.get_time import get_time
from src.lutpy.dicom.save_dicom import save_volume_as_dcm


def single_patient(output_dir, dicom_series, spr_lut, start):
    """
    This script reads a folder containing multiple monoenergetic DICOM-series from 1 acquisition and returns a new
    SPR-map DICOM-series. DICOM tags are inherited from the original monoenergetic series.

    :return: spr_lut in the form of a Pandas Dataframe
    """
    patient_start_time = time.time()
    # Import the image volumes as a dict of numpy arrays
    image_volume_dict, ref_dcm = dicom_to_array(dicom_series)

    m, s = get_time(patient_start_time)
    print("Dicom to array took ", m, "minutes and ", s, "seconds to run")

    # calculate the spr_lut
    print("Let's calculate the LUT")
    spr_lut = get_spr_lut(image_volume_dict, spr_lut)
    # TODO: Find out why some SPR values are negative. Is it a problem?
    # spr_lut_temp[:, 7][spr_lut_temp[:, 7] < 0.0000001] = 0
    # spr_lut_temp = np.append(spr_lut_temp, np.array([[-4000, 0, 0, 0, 0, -3024, -3024, 0, 0]]), axis=0)
    # spr_lut = np.append(spr_lut, spr_lut_temp, axis=0)

    # spr_lut = spr_lut.drop_duplicates(
    #    subset=[con.REF_KEV, con.HU_LOW, con.HU_HIGH], keep='first'
    # )
    print("The LUT dimensions are: ", spr_lut.shape[0], " by ", spr_lut.shape[1])

    m, s = get_time(patient_start_time)
    print("Calculating the LUT took ", m, "minutes and ", s, "seconds to run")

    #  map the volume
    spr_map = get_spr_map(image_volume_dict, spr_lut)

    is_exist = os.path.exists(output_dir)
    if not is_exist:
        os.makedirs(output_dir)

    ref_dcm.ImageVolume = spr_map
    save_volume_as_dcm(ref_dcm, Path(output_dir))

    m, s = get_time(start)
    print("The total time is ", m, "minutes and ", s, "seconds to run\n ")
    m, s = get_time(patient_start_time)
    print("This patient took ", m, "minutes and ", s, "seconds to run\n ")

    #if spr_lut.shape[0] > 55000:
    #    spr_lut = np.zeros((1, 9))
    #    print("The spr LUT has been reset")

    return spr_lut
