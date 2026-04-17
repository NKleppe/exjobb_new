import os

import numpy as np
import time

from src.lutpy.run.patient import single_patient
import dicom_image_tools as dit
from pathlib import Path
from src.lutpy.time.get_time import get_time



def siemens_test():
    """
    This script reads a folder containing multiple monoenergetic DICOM-series from 1 acquisition and returns a new
    SPR-map DICOM-series. DICOM tags are inherited from the original monoenergetic series.

    :return: SPR map DICOM Series
    """
    start = time.time()
    print("Go!\n")
    #TODO: set right keV for the Siemens images. 
    root_dir = r"input/mono_siemens/"

    spr_lut = np.zeros((1, 9))

    for dose_level in os.listdir(root_dir):
        dose_dir = root_dir + r"\\" + dose_level
        for recon in os.listdir(dose_dir):
            recon_dir = dose_dir + r"\\" + recon

            print("Dose ", dose_level, ", Recon: ", recon)

            all_dicom = dit.import_dicom_from_folder(folder=Path(recon_dir))

            m, s = get_time(start)
            print("Importing dicom from folder took ", m, "minutes and ", s, "seconds to run")

            for patient in all_dicom:
                patient_dir = recon_dir + r"\\" + patient
                output_dir = patient_dir.replace(r"input", r"output")
                print("The patient is: ", patient)
                spr_lut = single_patient(output_dir, all_dicom[patient].Series, spr_lut, start)

    print("End of script")
    print("The end")



if __name__ == "__main__":
    main()