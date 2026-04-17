import pandas as pd

from src.lutpy.time.get_time import get_time
from src.lutpy import constants as con


def write_result(rmse_dict, start, file_name):

    # write rmse_dict to xlsx-file.
    with pd.ExcelWriter(file_name, engine="openpyxl") as writer:
        rmse_dict[con.LUNG].to_excel(writer, sheet_name=con.LUNG)
        rmse_dict[con.SOFT].to_excel(writer, sheet_name=con.SOFT)
        rmse_dict[con.BONE].to_excel(writer, sheet_name=con.BONE)

        rmse_dict[con.LUNG_COMPLIANT_WITH_REF].to_excel(
            writer, sheet_name=con.LUNG_COMPLIANT_WITH_REF
        )
        rmse_dict[con.SOFT_COMPLIANT_WITH_REF].to_excel(
            writer, sheet_name=con.SOFT_COMPLIANT_WITH_REF
        )
        rmse_dict[con.BONE_COMPLIANT_WITH_REF].to_excel(
            writer, sheet_name=con.BONE_COMPLIANT_WITH_REF
        )
        rmse_dict[con.OPTIMAL_VMI].to_excel(writer, sheet_name=con.OPTIMAL_VMI)

    m, s = get_time(start)

    print(
        "finished writing results to excel at ", m, "minutes and ", s, "seconds to run"
    )

    # print the optimal vmi pairs in the console window
    print_optimal_vmi_pairs(rmse_dict)

    return


def print_optimal_vmi_pairs(rmse_dict):

    print("The optimal energy pairs are: ")
    print(
        "{} / {} keV for lung tissue".format(
            rmse_dict[con.LUNG_COMPLIANT_WITH_REF][con.KEV_LOW][0],
            rmse_dict[con.LUNG_COMPLIANT_WITH_REF][con.KEV_HIGH][0],
        )
    )
    print(
        "{} / {} keV for soft tissue".format(
            rmse_dict[con.SOFT_COMPLIANT_WITH_REF][con.KEV_LOW][0],
            rmse_dict[con.SOFT_COMPLIANT_WITH_REF][con.KEV_HIGH][0],
        )
    )
    print(
        "{} / {} keV for bone tissue".format(
            rmse_dict[con.BONE_COMPLIANT_WITH_REF][con.KEV_LOW][0],
            rmse_dict[con.BONE_COMPLIANT_WITH_REF][con.KEV_HIGH][0],
        )
    )

    print("\n \n")
    return
