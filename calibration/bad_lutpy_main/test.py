import os
import pydicom

folder_52 = r"C:\Users\Nelly Kleppe\PycharmProjects\exjobb\calibration\lutpy_main\input\mono ge\head_test\4.9 mGy\Soft Asir 0\1.2.826.0.1.3680043.8.971.25283424576306668811460400804025227384\Mono 52 kev_Series0349"

for f in sorted(os.listdir(folder_52)):
    path = os.path.join(folder_52, f)
    if os.path.isfile(path):
        ds = pydicom.dcmread(path, stop_before_pixels=True)
        print("FILE:", path)
        print("KVP:", getattr(ds, "KVP", "MISSING"))
        print("SeriesDescription:", getattr(ds, "SeriesDescription", "MISSING"))
        break