import numpy as np
from pathlib import Path
import pydicom
from dicom_image_tools.dicom_handlers import CtSeries
import shutil
import os


# -> tuple[np.ndarray, float(RescaleIntercept), float(RescaleSlope)]
def rescale_image(image_volume: np.ndarray):
    """
    This function takes an image volume (np-array) and returns the rescale intercept and slope
    :param image_volume:
    :return: image_volume, rescale_intercept, rescale_slope
    """
    # rescale_intercept = float(np.min(image_volume))
    # rescale_slope = (np.max(image_volume) - np.min(image_volume)) / 2 ** 16

    # image_volume = (image_volume - rescale_intercept) / rescale_slope
    rescale_intercept = 0
    rescale_slope = 1
    image_volume = (image_volume*1000-1000)
    image_volume = np.rint(image_volume)
    image_volume = image_volume.astype(np.int16)

    return image_volume, rescale_intercept, rescale_slope


def save_new_slice(image_slice: np.ndarray, metadata: pydicom.FileDataset, output_path: Path,
                   rescale_intercept, rescale_slope):
    """
    Changes relevant metadata attributes and saves the slice as a DICOM-image at Path.

    :param image_slice:
    :param metadata:
    :param output_path:
    :param rescale_intercept:
    :param rescale_slope:
    :return:
    """

    metadata.RescaleIntercept = rescale_intercept
    metadata.RescaleSlope = rescale_slope

    # write pixeldata
    metadata.PixelData = image_slice.tobytes()
    metadata['PixelData'].VR = "OW"
    # Mer parametrar som måste ändras t ex StudyDescription

    metadata.save_as(output_path)


def save_volume_as_dcm(ct_series: CtSeries, output_dir: Path):
    """
    Loops through each slice of the image volume, changes relevant metadata andsa
    :param ct_series:
    :param output_dir:
    :return:
    """
    image_volume, rescale_intercept, rescale_slope = rescale_image(ct_series.ImageVolume)

    _ = [
        save_new_slice(
            image_slice=image_volume[:, :, ind],
            metadata=metadata,
            rescale_intercept=rescale_intercept,
            rescale_slope=rescale_slope,
            output_path=output_dir / f"{ind}.dcm"

        ) for ind, metadata in enumerate(ct_series.CompleteMetadata)
    ]




