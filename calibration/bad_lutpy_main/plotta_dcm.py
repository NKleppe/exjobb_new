import pydicom
import matplotlib.pyplot as plt
import os

# choose a slice
slice = 40
slice = "Image (0001)"

path_in = r"C:\Users\Nelly Kleppe\PycharmProjects\exjobb\calibration\lutpy_main\output\mono ge\ge head test\5 mGy\Soft Asir 0\1.2.826.0.1.3680043.8.971.25283424576306668811460400804025227384"
path_out = r"C:\Users\Nelly Kleppe\PycharmProjects\exjobb\calibration\bilder"
path_in = r"C:\Users\Nelly Kleppe\PycharmProjects\exjobb\calibration\lutpy_main\input\mono ge\head_test\4.9 mGy\Soft Asir 0\1.2.826.0.1.3680043.8.971.25283424576306668811460400804025227384\49"
filename = str(slice)+".dcm"
save_filename = str(slice)+".png"
full_out = os.path.join(path_out, save_filename)
full_in = os.path.join(path_in, filename)

ds = pydicom.dcmread(full_in)
img = ds.pixel_array

plt.imshow(img, cmap="gray")
plt.axis("off")
plt.savefig(full_out, bbox_inches="tight", pad_inches=0)
plt.close()

print("Saved to:", full_out)