import os
import re
import pydicom
from pydicom.uid import ExplicitVRLittleEndian, generate_uid

root_folder = r"C:\Users\Nelly Kleppe\PycharmProjects\exjobb\calibration\lutpy_main\input\mono ge\head_test\4.9 mGy\Soft Asir 0"

print("PATCHING:", root_folder)

for study_name in os.listdir(root_folder):
    study_path = os.path.join(root_folder, study_name)
    if not os.path.isdir(study_path):
        continue

    # One StudyInstanceUID for the whole study folder
    study_uid = generate_uid()
    print("\nSTUDY FOLDER:", study_path)
    print("Study UID:", study_uid)

    for series_folder_name in os.listdir(study_path):
        series_path = os.path.join(study_path, series_folder_name)
        if not os.path.isdir(series_path):
            continue

        # Parse folder name like: Mono 49 keV_Series0301
        m = re.match(r"(.+)_Series(\d+)$", series_folder_name)
        if m:
            series_description = m.group(1).strip()   # "Mono 49 keV"
            series_number = int(m.group(2))           # 301
        else:
            series_description = series_folder_name
            series_number = 1

        series_uid = generate_uid()

        print("\n  SERIES FOLDER:", series_path)
        print("  SeriesDescription:", series_description)
        print("  SeriesNumber:", series_number)
        print("  Series UID:", series_uid)

        # collect files
        dcm_files = []
        for f in os.listdir(series_path):
            full_path = os.path.join(series_path, f)
            if os.path.isfile(full_path):
                dcm_files.append(full_path)

        dcm_files.sort()

        for i, full_path in enumerate(dcm_files, start=1):
            try:
                ds = pydicom.dcmread(full_path)

                # --- CT identity ---
                ds.SOPClassUID = "1.2.840.10008.5.1.4.1.1.2"   # CT Image Storage
                ds.Modality = "CT"
                ds.Manufacturer = "GE MEDICAL SYSTEMS"
                ds.ManufacturerModelName = "Revolution CT"

                # --- study / series / instance ---
                ds.StudyInstanceUID = study_uid
                ds.SeriesInstanceUID = series_uid
                ds.SeriesDescription = series_description
                ds.SeriesNumber = series_number
                ds.InstanceNumber = i

                # --- minimal geometry ---
                ds.ImagePositionPatient = [0.0, 0.0, float(i - 1)]
                ds.ImageOrientationPatient = [1.0, 0.0, 0.0, 0.0, 1.0, 0.0]
                ds.PixelSpacing = [1.0, 1.0]
                ds.SliceThickness = 1.0

                # --- common CT scaling ---
                ds.RescaleIntercept = 0
                ds.RescaleSlope = 1

                # --- file meta ---
                if not hasattr(ds, "file_meta") or ds.file_meta is None:
                    ds.file_meta = pydicom.dataset.FileMetaDataset()

                ds.file_meta.MediaStorageSOPClassUID = ds.SOPClassUID
                ds.file_meta.MediaStorageSOPInstanceUID = ds.SOPInstanceUID
                ds.file_meta.TransferSyntaxUID = ExplicitVRLittleEndian

                ds.is_little_endian = True
                ds.is_implicit_VR = False

                ds.save_as(full_path, write_like_original=False)

                # verify
                check = pydicom.dcmread(full_path, stop_before_pixels=True)
                print(f"    OK: {os.path.basename(full_path)}")
                print(f"       SeriesDescription: {getattr(check, 'SeriesDescription', 'MISSING')}")
                print(f"       SeriesNumber: {getattr(check, 'SeriesNumber', 'MISSING')}")
                print(f"       Modality: {getattr(check, 'Modality', 'MISSING')}")

            except Exception as e:
                print("    FAILED:", full_path)
                print("    Reason:", e)

print("\nDONE")