##############################################################################
# General settings
##############################################################################

# Choose the value for the exponent n (from the Bethe equation).
N_EXP = 3.21

# Set the proton energy
PROTON_ENERGY = 1.60 * 10 ** (-11)  # [J] ( 100 MeV, normal for proton therapy).


##############################################################################
# Settings for find_optimal_vmi
##############################################################################

# where to find the optimization input data
#OPT_DATA_FILE_PATH = r"input/mice export/input_iungo_all_final.xlsx"
#OPT_DATA_FILE_PATH = "input/mice export/nelly_full_vols.xlsx"
OPT_DATA_FILE_PATH = "input/mice export/nelly_full_test_qnoise.xlsx"


PHANTOM_REFERENCE_SHEET_FILE_PATH = "src/lutpy/resources/gammex_new_karin_truth_modifierade_namn.xlsx"
#PHANTOM_REFERENCE_SHEET_FILE_PATH = r"C:\Users\Nelly Kleppe\PycharmProjects\exjobb\calibration\lutpy_main\src\lutpy\resources\nelly_schneider_gammex.xlsx"


# the minimum and maximum kev available on the scanner
KEV_MIN = 40
KEV_MAX = 140


##############################################################################
# Settings for create_spr_maps
##############################################################################

### GE Energy Pairs ###
# Choose the energy pairs (expressed in eV)
KEV_LUNG_LOW = 115000
KEV_LUNG_HIGH = 116000
KEV_SOFT_LOW = 51000
KEV_SOFT_HIGH = 52000
KEV_BONE_LOW = 50000
KEV_BONE_HIGH = 64000


# Name the images that will be imported
"""VMI_REF = "74 kev"
VMI_LUNG_LOW = "115 kev"
VMI_LUNG_HIGH = "116 kev"
VMI_SOFT_LOW = "51 kev"
VMI_SOFT_HIGH = "52 kev"
VMI_BONE_LOW = "50 kev"
VMI_BONE_HIGH = "64 kev"""


# karins catsim head
VMI_REF = "74 kev"
VMI_LUNG_LOW = "135 kev"
VMI_LUNG_HIGH = "136 kev"
VMI_SOFT_LOW = "46 kev"
VMI_SOFT_HIGH = "51 kev"
VMI_BONE_LOW = "55 kev"
VMI_BONE_HIGH = "61 kev"

# Set the boundaries for the segmentation of the image volume
HU_AIR = -3024
HU_SOFT_LOWER_BOUNDRY = -200
HU_SOFT_UPPER_BOUNDRY = 150

AIR_SEGMENT = -4000
LUNG_SEGMENT = -201
SOFT_SEGMENT = 1
BONE_SEGMENT = 151

##############################################################################
###  string definitions###
##############################################################################
KEV = "kev"
KEV_LOW = "kev_low"
KEV_HIGH = "kev_high"

MEAN_HU = "mean_hu"
HU_LOW = "hu_low"
HU_HIGH = "hu_high"


MU = "mu"
MU_LOW = "mu_low"
MU_HIGH = "mu_high"
MU_H2O = "mu_h2o"

ED = "ed"
EAN = "ean"
RED = "red"
SPR = "spr"

EAN_REF = "ean_ref"
ED_REF = "ed_ref"
SPR_REF = "spr_ref"

EAN_DEV = "ean_dev"
ED_DEV = "ed_dev"
SPR_DEV = "spr_dev"
RMSE = "rmse"

INSERT = "insert"
OPTIMAL_VMI = "optimal_vmis"

REF_KEV = "ref_kev"
REF_COPY = "ref_kev_copy"
LUNG_LOW = "lung_low"
LUNG_HIGH = "lung_high"
SOFT_LOW = "soft_low"
SOFT_HIGH = "soft_high"
BONE_LOW = "bone_low"
BONE_HIGH = "bone_high"

LUNG = "lung"
SOFT = "soft"
BONE = "bone"

LUNG_COMPLIANT_WITH_REF = "lung_ww"
SOFT_COMPLIANT_WITH_REF = "soft_ww"
BONE_COMPLIANT_WITH_REF = "bone_ww"

##############################################################################
### Tables from Jackson & Hawkes ###
##############################################################################

JACK_HAWK_Z_REF = (6, 8, 10, 13, 26, 54)

SCOFIELD_TAB2A_KL_SHELL_HV_REF = [
    10 * 10 ** 3,
    30 * 10 ** 3,
    50 * 10 ** 3,
    80 * 10 ** 3,
    100 * 10 ** 3,
    150 * 10 ** 3,
    200 * 10 ** 3,
    400 * 10 ** 3,
]
SCOFIELD_TAB2A_KL_SHELL_Z_REF = [6, 8, 10, 13, 20, 26, 36, 54]
SCOFIELD_TAB2A_KL_SHELL_TABLE_VALUES = (
    [
        [3.9348 * 10 ** (-27), 2.0570 * 10 ** (-28)],
        [1.0807 * 10 ** (-28), 5.7194 * 10 ** (-30)],  # Z=6
        [1.9741 * 10 ** (-29), 1.0479 * 10 ** (-30)],
        [4.1092 * 10 ** (-30), 2.1859 * 10 ** (-31)],
        [1.9538 * 10 ** (-30), 1.0401 * 10 ** (-31)],
        [5.1244 * 10 ** (-31), 2.7255 * 10 ** (-32)],
        [2.0138 * 10 ** (-31), 1.0711 * 10 ** (-32)],
        [2.4075 * 10 ** (-32), 1.2799 * 10 ** (-33)],
    ],
    [
        [1.4004 * 10 ** (-26), 7.8278 * 10 ** (-28)],
        [4.1264 * 10 ** (-28), 2.3354 * 10 ** (-29)],  # Z=8
        [7.7129 * 10 ** (-29), 4.3797 * 10 ** (-30)],
        [1.6332 * 10 ** (-29), 9.2942 * 10 ** (-31)],
        [7.8182 * 10 ** (-30), 4.4529 * 10 ** (-31)],
        [2.0678 * 10 ** (-30), 1.1794 * 10 ** (-31)],
        [8.1707 * 10 ** (-31), 4.6649 * 10 ** (-32)],
        [9.8899 * 10 ** (-32), 5.6376 * 10 ** (-33)],
    ],
    [
        [3.6260 * 10 ** (-26), 2.1089 * 10 ** (-27)],
        [1.1380 * 10 ** (-27), 6.6344 * 10 ** (-29)],  # Z=10
        [2.1739 * 10 ** (-28), 1.2701 * 10 ** (-29)],
        [4.6784 * 10 ** (-29), 2.7375 * 10 ** (-30)],
        [2.2543 * 10 ** (-29), 1.3199 * 10 ** (-30)],
        [6.0244 * 10 ** (-30), 3.5312 * 10 ** (-31)],
        [2.3952 * 10 ** (-30), 1.4050 * 10 ** (-31)],
        [2.9269 * 10 ** (-31), 1.7160 * 10 ** (-32)],
    ],
    [
        [1.0657 * 10 ** (-25), 7.5168 * 10 ** (-27)],
        [3.6371 * 10 ** (-27), 2.5344 * 10 ** (-28)],  # Z=13
        [7.1628 * 10 ** (-28), 4.9903 * 10 ** (-29)],
        [1.5773 * 10 ** (-28), 1.1001 * 10 ** (-29)],
        [7.6715 * 10 ** (-29), 5.3532 * 10 ** (-30)],
        [2.0806 * 10 ** (-29), 1.4531 * 10 ** (-30)],
        [8.3457 * 10 ** (-30), 5.8323 * 10 ** (-31)],
        [1.0340 * 10 ** (-30), 7.2350 * 10 ** (-32)],
    ],
    [
        [5.5596 * 10 ** (-25), 5.2041 * 10 ** (-26)],
        [2.2574 * 10 ** (-26), 1.9769 * 10 ** (-27)],  # Z=20
        [4.7234 * 10 ** (-27), 4.1005 * 10 ** (-28)],
        [1.0906 * 10 ** (-27), 9.4356 * 10 ** (-29)],
        [5.4104 * 10 ** (-28), 4.6779 * 10 ** (-29)],
        [1.5145 * 10 ** (-28), 1.3090 * 10 ** (-29)],
        [6.1921 * 10 ** (-29), 5.3552 * 10 ** (-30)],
        [7.9436 * 10 ** (-30), 6.8750 * 10 ** (-31)],
    ],
    [
        [1.3889 * 10 ** (-24), 1.5859 * 10 ** (-25)],
        [6.4603 * 10 ** (-26), 6.4153 * 10 ** (-27)],  # Z=26
        [1.4160 * 10 ** (-26), 1.3764 * 10 ** (-27)],
        [3.3885 * 10 ** (-27), 3.2632 * 10 ** (-28)],
        [1.7064 * 10 ** (-27), 1.6395 * 10 ** (-28)],
        [4.8937 * 10 ** (-28), 4.6914 * 10 ** (-29)],
        [2.0311 * 10 ** (-28), 1.9460 * 10 ** (-29)],
        [2.6798 * 10 ** (-29), 2.5673 * 10 ** (-30)],
    ],
    [
        [0, 5.9923 * 10 ** (-25)],
        [2.1955 * 10 ** (-25), 2.6005 * 10 ** (-26)],  # Z=36
        [5.1685 * 10 ** (-26), 5.8025 * 10 ** (-27)],
        [1.3059 * 10 ** (-26), 1.4295 * 10 ** (-27)],
        [6.7277 * 10 ** (-27), 7.3139 * 10 ** (-28)],
        [2.0019 * 10 ** (-27), 2.1606 * 10 ** (-28)],
        [8.5013 * 10 ** (-28), 9.1520 * 10 ** (-29)],
        [1.1722 * 10 ** (-28), 1.2579 * 10 ** (-29)],
    ],
    [
        [0, 2.8919 * 10 ** (-24)],
        [0, 1.4087 * 10 ** (-25)],  # Z=54
        [2.2619 * 10 ** (-25), 3.3004 * 10 ** (-26)],
        [6.2631 * 10 ** (-26), 8.5341 * 10 ** (-27)],
        [3.3508 * 10 ** (-26), 4.4724 * 10 ** (-27)],
        [1.0595 * 10 ** (-26), 1.3813 * 10 ** (-27)],
        [4.6742 * 10 ** (-27), 6.0362 * 10 ** (-28)],
        [6.9539 * 10 ** (-28), 8.8655 * 10 ** (-29)],
    ],
)
