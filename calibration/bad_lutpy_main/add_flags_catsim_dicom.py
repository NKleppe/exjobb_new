import os
import pydicom
from pydicom.uid import ExplicitVRLittleEndian
from pydicom.dataelem import DataElement


root_folder = r"C:\Users\Nelly Kleppe\PycharmProjects\exjobb\calibration\lutpy_main\input\mono ge\head_test\4.9 mGy\Soft Asir 0"

print("PATCHING FOLDER:", root_folder)

total = 0
missing_after = 0

for folder_path, _, file_names in os.walk(root_folder):
    for file_name in file_names:
        if not file_name.lower().endswith(".dcm"):
            continue

        full_path = os.path.join(folder_path, file_name)

        try:
            # --- PATCH ---
            ds = pydicom.dcmread(full_path)

            ds[(0x0008, 0x0070)] = DataElement((0x0008, 0x0070), "LO", "GE MEDICAL SYSTEMS")
            ds[(0x0008, 0x1090)] = DataElement((0x0008, 0x1090), "LO", "Revolution CT")

            ds.Manufacturer = "GE MEDICAL SYSTEMS"
            ds.Modality = "CT"
            #ds.SOPClassUID = "1.2.840.10008.5.1.4.1.1.2"

            #if not hasattr(ds, "file_meta") or ds.file_meta is None:
            #    ds.file_meta = pydicom.dataset.FileMetaDataset()

            #ds.file_meta.MediaStorageSOPClassUID = ds.SOPClassUID
            #ds.file_meta.TransferSyntaxUID = ExplicitVRLittleEndian

            #ds.is_little_endian = True
            #ds.is_implicit_VR = False

            ds.save_as(full_path, write_like_original=False)

            # --- CHECK ---
            check = pydicom.dcmread(full_path, stop_before_pixels=True)

            manufacturer_attr = getattr(check, "Manufacturer", "MISSING")
            manufacturer_tag = check.get((0x0008, 0x0070), "TAG NOT FOUND")

            print("\nFILE:", full_path)
            print("  Manufacturer (attr):", manufacturer_attr)
            print("  Manufacturer (tag):", manufacturer_tag)
            print("  Modality:", getattr(check, "Modality", "MISSING"))

            if manufacturer_attr == "MISSING":
                missing_after += 1
                print("  >>> STILL MISSING <<<")

            total += 1

        except Exception as e:
            print("FAILED:", full_path)
            print("Reason:", e)

print("\nDONE")
print("Total files checked:", total)
print("Still missing Manufacturer:", missing_after)