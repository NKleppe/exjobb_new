#%%
import os
import h5py
import numpy as np
import matplotlib.pyplot as plt
from gecatsim.pyfiles.GetMu import GetMu

#%%
mat_folder = r"C:\Users\Nelly Kleppe\PycharmProjects\exjobb\calibration\matfiles"

files = [
    "body1_265927_200419.mat",
    "body2_260227_220418.mat",
    "body3_260427_230435.mat",
    "body4_260728_000402.mat",
    "body5_260928_010451.mat",
    "head1_260628_020405.mat",
    "head2_260228_030426.mat",
    "head3_265828_030443.mat",
    "head4_265528_040408.mat",
    "head5_265128_050412.mat"
]

kev = 74
slice_idx = 6
r_mm = 10

body_rois = [
    ("corner", 0, 190),
    ("between_inserts", -75, 50),
]

head_rois = [
    ("corner", -150, 150),
    ("between_inserts", -45, 20),
]

#%%
def mm2px(cx, cy, r, shape, fov):
    px = fov / 1024
    x0 = (shape[1] - 1) / 2
    y0 = (shape[0] - 1) / 2

    x = int(round(x0 + cx / px))
    y = int(round(y0 - cy / px))
    r = r / px

    return x, y, r


def get_roi(img, cx, cy, r, fov):
    x, y, r = mm2px(cx, cy, r, img.shape, fov)

    yy, xx = np.ogrid[:img.shape[0], :img.shape[1]]
    mask = (xx - x) ** 2 + (yy - y) ** 2 <= r ** 2

    return img[mask], x, y, r


def get_HU(file_path):
    with h5py.File(file_path, "r") as f:
        pe = 10 * np.array(f["Image_PE"])
        pvc = 10 * np.array(f["Image_PVC"])

    pe = pe[slice_idx]
    pvc = pvc[slice_idx]

    mu_pe = GetMu("polyethylene", kev)[0]
    mu_pvc = GetMu("pvc_legacy", kev)[0]
    mu_w = GetMu("water", kev)[0]
    mu_a = GetMu("air", kev)[0]

    mu = mu_pe * pe + mu_pvc * pvc
    HU = 1000 * (mu - mu_w) / (mu_w - mu_a)

    return HU

#%%
# print mean and variance

for file in files:
    HU = get_HU(os.path.join(mat_folder, file))

    if file.startswith("body"):
        fov = 420
        rois = body_rois
    else:
        fov = 350
        rois = head_rois

    print(f"\n{file}")

    for name, cx, cy in rois:
        vals, _, _, _ = get_roi(HU, cx, cy, r_mm, fov)
        print(f"{name}: mean={vals.mean():.2f}, var={vals.var():.2f}")

#%%
# plot one body and one head

plot_files = [files[0], files[6]]

for file in plot_files:
    HU = get_HU(os.path.join(mat_folder, file))

    if file.startswith("body"):
        fov = 420
        rois = body_rois
    else:
        fov = 350
        rois = head_rois

    plt.figure(figsize=(7, 7))
    plt.imshow(HU, cmap="gray")
    plt.title(file)

    for name, cx, cy in rois:
        _, x, y, r = get_roi(HU, cx, cy, r_mm, fov)
        plt.gca().add_patch(plt.Circle((x, y), r, color="red", fill=False))
        plt.text(x + 5, y, name, color="yellow")

    plt.axis("off")

    outname = file.replace(".mat", "_roi_check.png")
    plt.savefig(outname, dpi=200, bbox_inches="tight")
    plt.close()

    print(f"Saved {outname}")