import os
import re
import shutil


def sort_siemens(root_dir):
    """
    This script takes a root directory containing Siemens VMIs and returns a directory with the Dicom-files sorted into
    the following structure:

    root_dir --> kernel + safir --> Acquisition --> keV-level

    The root directory must first be sorted using DicomSort on the property 'study description" and the files must be
    renamed using the properties "SOP instance UID", "


    """
    i = 0
    for root, dirs, files in os.walk(root_dir):
        print("in the loop")
        print(root, dirs)
        for f_name in files:
            new_dose_dir = root.partition(r"mGy")[0]
            new_dose_dir = new_dose_dir.partition("Siemens mono\\")[2]
            new_phantom_dir = new_dose_dir.partition("\\")[0]
            new_dose_dir = new_dose_dir.partition("\\")[2] + " mGy"

            new_recon_dir = root.partition(r"\22.")[0]
            new_recon_dir = new_recon_dir.partition(r"QR")[2]
            new_recon_dir = "QR" + new_recon_dir
            new_recon_dir = new_recon_dir.strip()

            new_kev_dir = root.partition("Monoenergetic Plus")[2]
            new_kev_dir = new_kev_dir.partition(" keV")[0]
            new_kev_dir = new_kev_dir + " keV"
            new_kev_dir = new_kev_dir.strip()

            new_acq_dir = root.partition("22.")[2]
            new_acq_dir = new_acq_dir.partition("\DE")[0]
            new_acq_dir = "22." + new_acq_dir
            new_file_name = f_name.partition("(")[2]
            new_file_name = new_file_name.partition(")")[0]
            new_file_name = new_file_name[-4:]

            source = root + r"/" + f_name
            destination = root_dir.replace(r"1 Bilder", r"7 Bilder sorterade")
            destination = destination + "/" + new_phantom_dir + "/" + new_dose_dir + "/" + new_recon_dir + "/" + new_acq_dir + "/" + new_kev_dir

            is_exist = os.path.exists(destination)
            if not is_exist:
                print("It does not exist!")
                print(destination)
                os.makedirs(destination)

            destination = destination + "/" + new_file_name + ".dcm"
            shutil.move(source, destination)

    return
