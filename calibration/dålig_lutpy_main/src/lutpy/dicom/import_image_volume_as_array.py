from pathlib import Path

import dicom_image_tools as dit
import numpy as np

from src.lutpy import constants as con
from src.lutpy.spr_lut.get_water_attenuation import get_water_attenuation


def dicom_to_array(dicom_series):
    """
    This function imports multiple DICOM series from a chosen folder, segments the image into AIR, LUNG, SOFT TISSUE and
    BONE, and assigns water attenuation coefficients corresponding to the optimal energy for the tissue type.
    It expects to find the following series:
    - reference VMI
    - lung low VMI
    - lung high VMI
    - soft low VMI
    - soft high VMI
    - bone low VMI
    - bone high VMI

    In order for the script to correctly identify the series, the images must be named in the constants.py file

    This function returns a dict containing the following image volumes as numpy arrays:
        - reference image
        - keV low
        - keV high
        - mu low
        - mu high
        - HU low
        - HU high
        - SPR (empty)

    :rtype: dict
    """
    ### debug nelly
    print(dicom_series)
    dicom_image_volume_dict = {}

    print("Number of series:", len(dicom_series))

    for i, ct_series in enumerate(dicom_series):
        print(f"\n--- SERIES {i} ---")
        print("SeriesDescription:", getattr(ct_series, "SeriesDescription", "MISSING"))
        print("Before import, ImageVolume exists:", hasattr(ct_series, "ImageVolume"))

        ct_series.import_image_volume()

        print("After import, ImageVolume type:", type(getattr(ct_series, "ImageVolume", None)))
        print("After import, ImageVolume is None:", getattr(ct_series, "ImageVolume", None) is None)

        dicom_image_volume_dict[ct_series.SeriesDescription] = ct_series.ImageVolume

    print("\nRaw dict keys:", list(dicom_image_volume_dict.keys()))

    dicom_image_volume_dict = {key.lower(): val for key, val in dicom_image_volume_dict.items()}

    print("Lowercase dict keys:", list(dicom_image_volume_dict.keys()))
    ### debug

    # Import images

    dicom_image_volume_dict = {}

    for ct_series in dicom_series:
        ct_series.import_image_volume()
        dicom_image_volume_dict[ct_series.SeriesDescription] = ct_series.ImageVolume

    dicom_image_volume_dict = {key.lower(): val for key, val in dicom_image_volume_dict.items()}

    for ct_series in dicom_series:
        if con.VMI_REF in ct_series.SeriesDescription.casefold():
            ref_kev = dicom_image_volume_dict.get(ct_series.SeriesDescription.casefold())
        if con.VMI_LUNG_LOW in ct_series.SeriesDescription.casefold():
            lung_low = dicom_image_volume_dict.get(ct_series.SeriesDescription.casefold())
        if con.VMI_LUNG_HIGH in ct_series.SeriesDescription.casefold():
            lung_high = dicom_image_volume_dict.get(ct_series.SeriesDescription.casefold())
        if con.VMI_SOFT_LOW in ct_series.SeriesDescription.casefold():
            soft_low = dicom_image_volume_dict.get(ct_series.SeriesDescription.casefold())
        if con.VMI_SOFT_HIGH in ct_series.SeriesDescription.casefold():
            soft_high = dicom_image_volume_dict.get(ct_series.SeriesDescription.casefold())
        if con.VMI_BONE_LOW in ct_series.SeriesDescription.casefold():
            bone_low = dicom_image_volume_dict.get(ct_series.SeriesDescription.casefold())
        if con.VMI_BONE_HIGH in ct_series.SeriesDescription.casefold():
            bone_high = dicom_image_volume_dict.get(ct_series.SeriesDescription.casefold())

    #ref_kev = dicom_image_volume_dict.get(con.VMI_REF)
    #lung_low = dicom_image_volume_dict.get(con.VMI_LUNG_LOW)
    #lung_high = dicom_image_volume_dict.get(con.VMI_LUNG_HIGH)
    #soft_low = dicom_image_volume_dict.get(con.VMI_SOFT_LOW)
    #soft_high = dicom_image_volume_dict.get(con.VMI_SOFT_HIGH)
    #bone_low = dicom_image_volume_dict.get(con.VMI_BONE_LOW)
    #bone_high = dicom_image_volume_dict.get(con.VMI_BONE_HIGH)

    # Get water attenuation coefficients
    water_attenuation = get_water_attenuation()

    # Create a copy of the reference image
    ref_kev_copy = ref_kev.copy()

    # Segment reference image, assign water attenuation coefficients, assemble low and high HU images.
    ref_kev[ref_kev <= con.HU_AIR] = con.AIR_SEGMENT
    ref_kev[(ref_kev > con.HU_AIR) & (ref_kev < con.HU_SOFT_LOWER_BOUNDRY)] = con.LUNG_SEGMENT
    ref_kev[(ref_kev >= con.HU_SOFT_LOWER_BOUNDRY) & (ref_kev <= con.HU_SOFT_UPPER_BOUNDRY)] = con.SOFT_SEGMENT
    ref_kev[ref_kev > con.HU_SOFT_UPPER_BOUNDRY] = con.BONE_SEGMENT

    kev_low = np.empty(ref_kev.shape)
    kev_low[ref_kev == con.LUNG_SEGMENT] = con.KEV_LUNG_LOW
    kev_low[ref_kev == con.SOFT_SEGMENT] = con.KEV_SOFT_LOW
    kev_low[ref_kev == con.BONE_SEGMENT] = con.KEV_BONE_LOW

    kev_high = np.empty(ref_kev.shape)
    kev_high[ref_kev == con.LUNG_SEGMENT] = con.KEV_LUNG_HIGH
    kev_high[ref_kev == con.SOFT_SEGMENT] = con.KEV_SOFT_HIGH
    kev_high[ref_kev == con.BONE_SEGMENT] = con.KEV_BONE_HIGH

    mu_low = np.empty(ref_kev.shape)
    mu_low[ref_kev == con.LUNG_SEGMENT] = water_attenuation[con.LUNG_LOW]
    mu_low[ref_kev == con.SOFT_SEGMENT] = water_attenuation[con.SOFT_LOW]
    mu_low[ref_kev == con.BONE_SEGMENT] = water_attenuation[con.BONE_LOW]

    mu_high = np.empty(ref_kev.shape)
    mu_high[ref_kev == con.LUNG_SEGMENT] = water_attenuation[con.LUNG_HIGH]
    mu_high[ref_kev == con.SOFT_SEGMENT] = water_attenuation[con.SOFT_HIGH]
    mu_high[ref_kev == con.BONE_SEGMENT] = water_attenuation[con.BONE_HIGH]

    hu_low = np.empty(ref_kev.shape)
    hu_low[ref_kev == con.AIR_SEGMENT] = -3024
    hu_low[ref_kev == con.LUNG_SEGMENT] = lung_low[ref_kev == con.LUNG_SEGMENT]
    hu_low[ref_kev == con.SOFT_SEGMENT] = soft_low[ref_kev == con.SOFT_SEGMENT]
    hu_low[ref_kev == con.BONE_SEGMENT] = bone_low[ref_kev == con.BONE_SEGMENT]

    hu_high = np.empty(ref_kev.shape)
    hu_high[ref_kev == con.AIR_SEGMENT] = -3024
    hu_high[ref_kev == con.LUNG_SEGMENT] = lung_high[ref_kev == con.LUNG_SEGMENT]
    hu_high[ref_kev == con.SOFT_SEGMENT] = soft_high[ref_kev == con.SOFT_SEGMENT]
    hu_high[ref_kev == con.BONE_SEGMENT] = bone_high[ref_kev == con.BONE_SEGMENT]

    result_volume = np.empty(ref_kev.shape)

    result_dict = {
        con.REF_KEV: ref_kev,
        con.KEV_LOW: kev_low,
        con.KEV_HIGH: kev_high,
        con.MU_LOW: mu_low,
        con.MU_HIGH: mu_high,
        con.HU_LOW: hu_low,
        con.HU_HIGH: hu_high,
        con.SPR: result_volume,
        con.REF_COPY: ref_kev_copy
    }

    return result_dict, dicom_series[0]


