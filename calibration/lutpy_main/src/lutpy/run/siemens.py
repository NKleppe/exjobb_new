import os

import numpy as np
import time

from src.lutpy.run.patient import single_patient
import dicom_image_tools as dit
from pathlib import Path
from src.lutpy.time.get_time import get_time


def siemens_both_phantoms():
    """
    This script reads a folder containing multiple monoenergetic DICOM-series from multiple acquisition and returns
    SPR-map DICOM-series. DICOM tags are inherited from the original monoenergetic series.

    :return: SPR map DICOM Series
    """
    start = time.time()
    print("Go!\n")

    # input_folder = r"input/mono ge/GE Head/5 mGy/Soft Asir 0"
    # output_folder = input_folder.replace("input", "output")

    root_dir = r"C:\Users\torbj\OneDrive\Desktop\Arbete 2 - mätningar\505 - Skarpt läge 2022-05\07 Bilder sorterade\\"
    # root_dir = r"input/mono_siemens"

    # spr_lut = np.zeros((1, 9))
    spr_lut = np.array([[-4000, 0, 0, 0, 0, -3024, -3024, 0, 0]])
    print("test")

    for phantom in os.listdir(root_dir):
        if "GE" in phantom or "AB" in phantom or "Body" in phantom:
            print("Skipping {}.".format(phantom))
            continue
        phantom_dir = root_dir + phantom
        for dose_level in os.listdir(phantom_dir):
            dose_dir = phantom_dir + r"\\" + dose_level
            for recon in os.listdir(dose_dir):
                if "QR66" in recon:
                    print("Skipping bone.")
                    continue
                recon_dir = dose_dir + r"\\" + recon

                print("Phantom: ", phantom, ", Dose: ", dose_level, ", Recon: ", recon)

                all_dicom = dit.import_dicom_from_folder(folder=Path(recon_dir))

                m, s = get_time(start)
                print(
                    "Importing dicom from folder took ",
                    m,
                    "minutes and ",
                    s,
                    "seconds to run",
                )

                for patient in all_dicom:
                    patient_dir = recon_dir + r"\\" + patient
                    output_dir = patient_dir.replace(
                        r"7 Bilder sorterade\Siemens mono", r"8 SPR maps\Siemens mono"
                    )
                    # output_dir = r"output/mono siemens"
                    print("The patient is: ", patient)
                    spr_lut = single_patient(
                        output_dir, all_dicom[patient].Series, spr_lut, start
                    )

    print("End of script")
    print("The end")
