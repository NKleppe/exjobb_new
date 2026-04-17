import os
import re
import pydicom

# --- paths ---
src_root = r"C:\Users\Nelly Kleppe\PycharmProjects\exjobb\calibration\lutpy_main\input\mono ge\head_test\4.9 mGy\Soft Asir 0"
ref_root = r"C:\Users\Nelly Kleppe\PycharmProjects\exjobb\calibration\lutpy_main\input\mono ge\ge head\5 mGy\Soft Asir 0\1.2.826.0.1.3680043.8.971.25283424576306668811460400804025227384"

print("SOURCE:", src_root)
print("REFERENCE:", ref_root)

# --- helper: find matching series by energy ---
def extract_energy(name):
    m = re.search(r"(\d+)\s*keV", name)
    return int(m.group(1)) if m else None

# map reference series by energy
ref_series_map = {}

for series_name in os.listdir(ref_root):
    series_path = os.path.join(ref_root, series_name)
    if not os.path.isdir(series_path):
        continue

    kev = extract_energy(series_name)
    if kev is None:
        continue

    ref_series_map[kev] = series_path

print("Reference energies found:", sorted(ref_series_map.keys()))

# --- process your data ---
for study_name in os.listdir(src_root):
    study_path = os.path.join(src_root, study_name)
    if not os.path.isdir(study_path):
        continue

    print("\nSTUDY:", study_path)

    for series_name in os.listdir(study_path):
        series_path = os.path.join(study_path, series_name)
        if not os.path.isdir(series_path):
            continue

        kev = extract_energy(series_name)
        if kev not in ref_series_map:
            print("Skipping (no ref match):", series_name)
            continue

        ref_series_path = ref_series_map[kev]

        print("\nMATCHED SERIES:", series_name, "→", os.path.basename(ref_series_path))

        src_files = sorted([
            os.path.join(series_path, f)
            for f in os.listdir(series_path)
            if os.path.isfile(os.path.join(series_path, f))
        ])

        ref_files = sorted([
            os.path.join(ref_series_path, f)
            for f in os.listdir(ref_series_path)
            if os.path.isfile(os.path.join(ref_series_path, f))
        ])

        if len(src_files) != len(ref_files):
            print("WARNING: different number of slices")

        for i, (src_file, ref_file) in enumerate(zip(src_files, ref_files)):
            try:
                src_ds = pydicom.dcmread(src_file)
                ref_ds = pydicom.dcmread(ref_file)

                # --- keep pixel data from your file ---
                pixel_data = src_ds.PixelData

                # --- copy full reference dataset ---
                new_ds = ref_ds.copy()

                # --- restore your image data ---
                new_ds.PixelData = pixel_data

                new_ds.Rows = src_ds.Rows
                new_ds.Columns = src_ds.Columns
                new_ds.BitsAllocated = src_ds.BitsAllocated
                new_ds.BitsStored = src_ds.BitsStored
                new_ds.HighBit = src_ds.HighBit
                new_ds.PixelRepresentation = src_ds.PixelRepresentation

                # --- keep instance number order ---
                new_ds.InstanceNumber = i + 1

                # optional: preserve UID uniqueness
                new_ds.SOPInstanceUID = pydicom.uid.generate_uid()

                # --- save ---
                new_ds.save_as(src_file, write_like_original=False)

                print("OK:", src_file)

            except Exception as e:
                print("FAILED:", src_file)
                print("Reason:", e)

print("\nDONE")