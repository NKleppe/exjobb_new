import pydicom
import matplotlib.pyplot as plt
import os

# choose a slice
slice = 6

path_out = r"C:\Users\Nelly Kleppe\PycharmProjects\exjobb\calibration\test"

path_in = r"C:\Users\Nelly Kleppe\PycharmProjects\exjobb\calibration\lutpy_main\output\mono ge\ge head test\5 mGy\Soft Asir 0\1.2.826.0.1.3680043.8.971.25283424576306668811460400804025227384"
path_in = r'C:\Users\Nelly Kleppe\PycharmProjects\exjobb\calibration\bilder\70_body3'
path_in = r'C:\Users\Nelly Kleppe\PycharmProjects\exjobb\calibration\bilder\70_head4'
path_in = r"C:\Users\Nelly Kleppe\PycharmProjects\exjobb\calibration\matfiles\head4\265528_040408\70"
path_in = r'C:\Users\Nelly Kleppe\PycharmProjects\exjobb\calibration\matfiles\body2\260227_220418\70'

filename = "im.000" + str(slice)+".dcm"
save_filename = "slice"+str(slice)+"_"+str(path_in[-5:])+".png"
save_filename = "slice"+str(slice)+"_"+str(path_in[-22:-17])+"_with_qnoise.png"
full_out = os.path.join(path_out, save_filename)
full_in = os.path.join(path_in, filename)

ds = pydicom.dcmread(full_in)
img = ds.pixel_array

plt.imshow(img, cmap="gray")
plt.axis("off")
plt.savefig(full_out, bbox_inches="tight", pad_inches=0)
plt.close()

print("Saved to:", full_out)