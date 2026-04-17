from src.lutpy import constants as con
import pandas as pd


def get_spr_map(image_volume_dict: dict, spr_lut_df):
    """
    This function takes image_volume_dict and creates a DataFrame (image_volume_df) containing the columns
    ["Ref 140 keV", "Low HU", "High HU"]. Then it merges the DataFrame with the SPR Look-Up Table DataFrame (spr_lut_df),
    thereby mapping a SPR value for every row in image_volume_df. Finally, it extracts the newly created
    SPR column from image_volume_df and reshapes to the same shape as the original image volume.

    :param image_volume_dict: dict
    :param spr_lut_df: DataFrame
    :return: spr_map:  ndarray
    """

    spr_dict = {con.REF_KEV: spr_lut_df[:, 0], con.HU_LOW: spr_lut_df[:, 5], con.HU_HIGH: spr_lut_df[:, 6],
                con.SPR: spr_lut_df[:, 7]}
    spr_df = pd.DataFrame(data=spr_dict)

    ref_140kev_arr = image_volume_dict[con.REF_KEV].flatten()
    hu_low_arr = image_volume_dict[con.HU_LOW].flatten()
    hu_high_arr = image_volume_dict[con.HU_HIGH].flatten()

    flattened_dict = {con.REF_KEV: ref_140kev_arr, con.HU_LOW: hu_low_arr, con.HU_HIGH: hu_high_arr}
    image_volume_df = pd.DataFrame(data=flattened_dict)

    merged = pd.merge(image_volume_df, spr_df, how="left", on=[con.REF_KEV, con.HU_LOW, con.HU_HIGH], sort=False)

    spr_map = merged[con.SPR].values
    spr_map = spr_map.reshape(image_volume_dict[con.REF_KEV].shape)


    return spr_map
