import os

import numpy as np
import time

from src.lutpy.run.patient import single_patient
import dicom_image_tools as dit
from pathlib import Path
from src.lutpy.time.get_time import get_time


def ge_both_phantoms():
    """
    This script reads a folder containing multiple monoenergetic DICOM-series from multiple acquisition and returns
    SPR-map DICOM-series. DICOM tags are inherited from the original monoenergetic series.

    :return: SPR map DICOM Series
    """
    start = time.time()
    print("Go!\n")

    # input_folder = r"input/mono ge/GE Head/4.9 mGy/Soft Asir 0"
    # output_folder = input_folder.replace("input", "output")

    root_dir = r"C:\Users\torbj\OneDrive\Desktop\Arbete 2 - mätningar\505 - Skarpt läge 2022-05\07 Bilder sorterade\\"

    #spr_lut = np.zeros((1, 9))
    spr_lut = np.array([[-4000, 0, 0, 0, 0, -3024, -3024, 0, 0]])
    print("test")

    for phantom in os.listdir(root_dir):
        phantom_dir = root_dir + phantom
        for dose_level in os.listdir(phantom_dir):
            dose_dir = phantom_dir + r"\\" + dose_level
            for recon in os.listdir(dose_dir):
                if "Bone" in recon or "QR66" in recon:
                    print("Skipping bone.")
                    continue
                recon_dir = dose_dir + r"\\" + recon

                print("Phantom: ", phantom, ", Dose: ", dose_level, ", Recon: ", recon)

                all_dicom = dit.import_dicom_from_folder(folder=Path(recon_dir))

                m, s = get_time(start)
                print("Importing dicom from folder took ", m, "minutes and ", s, "seconds to run")

                for patient in all_dicom:
                    patient_dir = recon_dir + r"\\" + patient
                    output_dir = patient_dir.replace(r"7 Bilder sorterade", r"8 SPR maps")
                    print("The patient is: ", patient)
                    spr_lut = single_patient(output_dir, all_dicom[patient].Series, spr_lut, start)

    print("End of script")
    print("The end")


def ge_one_phantom():
    """
    This script reads a folder containing multiple monoenergetic DICOM-series from 1 acquisition and returns a new
    SPR-map DICOM-series. DICOM tags are inherited from the original monoenergetic series.

    :return: SPR map DICOM Series
    """
    start = time.time()
    print("Go!\n")

    # root_dir = r"input/mono ge/GE Head/4.9 mGy/Soft Asir 0"
    # output_folder = input_folder.replace("input", "output")

    root_dir = r"C:\Users\torbj\OneDrive\Desktop\Arbete 2 - mätningar\505 - Skarpt läge 2022-05\07 Bilder sorterade\GE Body\\"
    root_dir = r"C:\Users\Nelly Kleppe\PycharmProjects\exjobb\calibration\lutpy_main\input\mono ge\head_test"
    spr_lut = np.zeros((1, 9))

    for dose_level in os.listdir(root_dir):
        if "05 mGy" in dose_level:
            print("Skipping {}.".format(dose_level))
            continue
        dose_dir = root_dir + r"\\" + dose_level
        for recon in os.listdir(dose_dir):
            if "Bone" in recon:
                print("Skipping {}.".format(recon))
                continue
            recon_dir = dose_dir + r"\\" + recon

            print("Dose ", dose_level, ", Recon: ", recon)

            all_dicom = dit.import_dicom_from_folder(folder=Path(recon_dir))

            m, s = get_time(start)
            print("Importing dicom from folder took ", m, "minutes and ", s, "seconds to run")

            for patient in all_dicom:
                patient_dir = recon_dir + r"\\" + patient
                output_dir = patient_dir.replace(r"7 Bilder sorterade", r"8 SPR maps")
                print("The patient is: ", patient)
                spr_lut = single_patient(output_dir, all_dicom[patient].Series, spr_lut, start)

    print("End of script")
    print("The end")


def ge_one_phantom_and_dose():
    """
    This script reads a folder containing multiple monoenergetic DICOM-series from 1 acquisition and returns a new
    SPR-map DICOM-series. DICOM tags are inherited from the original monoenergetic series.

    :return: SPR map DICOM Series
    """
    start = time.time()
    print("Go!\n")

    # input_folder = r"input/mono ge/GE Head/4.9 mGy/Soft Asir 0"
    # output_folder = input_folder.replace("input", "output")

    root_dir = r"C:\Users\torbj\OneDrive\Desktop\Arbete 2 - mätningar\505 - Skarpt läge 2022-05\07 Bilder sorterade\GE Body\5 mGy\\"

    spr_lut = np.array([-4000, 0, 0, 0, 0, -3024, -3024, 0, 0])

    for recon in os.listdir(root_dir):
        if "Bone" in recon or "QR66" in recon:
            print("Skipping bone.")
            continue
        recon_dir = root_dir + r"\\" + recon

        print("Recon: ", recon)

        all_dicom = dit.import_dicom_from_folder(folder=Path(recon_dir))

        m, s = get_time(start)
        print("Importing dicom from folder took ", m, "minutes and ", s, "seconds to run")

        for patient in all_dicom:
            patient_dir = recon_dir + r"\\" + patient
            output_dir = patient_dir.replace(r"7 Bilder sorterade", r"8 SPR maps")
            print("The patient is: ", patient)
            spr_lut = single_patient(output_dir, all_dicom[patient].Series, spr_lut, start)

    print("End of script")
    print("The end")

def ge_specific(dose, kernel_and_recon, study_UID):
    """
    This script reads a folder containing multiple monoenergetic DICOM-series from 1 acquisition and returns a new
    SPR-map DICOM-series. DICOM tags are inherited from the original monoenergetic series.

    :return: SPR map DICOM Series
    """
    start = time.time()
    print("Go!\n")

    # root_dir = r"input/mono ge/GE Head/4.9 mGy/Soft Asir 0"
    # output_folder = input_folder.replace("input", "output")

    root_dir = r"C:\Users\torbj\OneDrive\Desktop\Arbete 2 - mätningar\505 - Skarpt läge 2022-05\07 Bilder sorterade\GE Body\\"

    spr_lut = np.zeros((1, 9))

    for dose_level in os.listdir(root_dir):
        if dose in dose_level:
            print("found {}.".format(dose_level))
            dose_dir = root_dir + r"\\" + dose_level
            for recon in os.listdir(dose_dir):
                if kernel_and_recon in recon:
                    print("found {}.".format(recon))
                    recon_dir = dose_dir + r"\\" + recon

                    print("Dose ", dose_level, ", Recon: ", recon)

                    all_dicom = dit.import_dicom_from_folder(folder=Path(recon_dir))

                    m, s = get_time(start)
                    print("Importing dicom from folder took ", m, "minutes and ", s, "seconds to run")

                    for patient in all_dicom:
                        if study_UID in patient:
                            print("found {}.".format(recon))
                            patient_dir = recon_dir + r"\\" + patient
                            output_dir = patient_dir.replace(r"7 Bilder sorterade", r"8 SPR maps (spec)")
                            print("The patient is: ", patient)
                            spr_lut = single_patient(output_dir, all_dicom[patient].Series, spr_lut, start)

    print("End of script")
    print("The end")


def ge_specific_dose_and_kernel(dose, kernel_and_noise_red):
    """
    This script reads a folder containing multiple monoenergetic DICOM-series from 1 acquisition and returns a new
    SPR-map DICOM-series. DICOM tags are inherited from the original monoenergetic series.

    :return: SPR map DICOM Series
    """
    start = time.time()
    print("Go!\n")

    # input_folder = r"input/mono ge/GE Head/4.9 mGy/Soft Asir 0"
    # output_folder = input_folder.replace("input", "output")
    root_dir = r"C:\Users\torbj\OneDrive\Desktop\Arbete 2 - mätningar\505 - Skarpt läge 2022-05\07 Bilder sorterade\GE Body\\"

    spr_lut = np.zeros((1, 9))

    for dose_level in os.listdir(root_dir):
        if dose in dose_level:
            print("found {}.".format(dose_level))
            dose_dir = root_dir + r"\\" + dose_level
            for recon in os.listdir(dose_dir):
                if kernel_and_noise_red in recon:
                    print("found {}.".format(recon))
                    recon_dir = dose_dir + r"\\" + recon

                    print("Dose ", dose_level, ", Recon: ", recon)

                    all_dicom = dit.import_dicom_from_folder(folder=Path(recon_dir))

                    m, s = get_time(start)
                    print("Importing dicom from folder took ", m, "minutes and ", s, "seconds to run")

                    for patient in all_dicom:
                        patient_dir = recon_dir + r"\\" + patient
                        output_dir = patient_dir.replace(r"7 Bilder sorterade", r"8 SPR maps (spec)")
                        print("The patient is: ", patient)
                        spr_lut = single_patient(output_dir, all_dicom[patient].Series, spr_lut, start)

    print("End of script")
    print("The end")


