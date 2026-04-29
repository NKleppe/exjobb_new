import pandas as pd
import numpy as np
import multiprocessing as mp

from src.lutpy import constants as con
from src.lutpy.spr_calc.hu_to_spr import hu_to_spr
from src.lutpy.spr_lut.get_data_for_mp_spr_calc import get_data_for_mp_spr_calc

def hu_to_spr_chunk(
    hu_low,
    hu_high,
    n_exp,
    kev_low,
    kev_high,
    mu_low,
    mu_high,
):
    results = []

    for h_low, h_high, k_low, k_high, m_low, m_high in zip(
        hu_low,
        hu_high,
        kev_low,
        kev_high,
        mu_low,
        mu_high,
    ):
        spr = hu_to_spr(
            h_low,
            h_high,
            n_exp,
            k_low,
            k_high,
            m_low,
            m_high,
        )

        results.append(spr)

    return results

def get_spr_lut(image_dict: dict, spr_lut) -> list:
    """
    This function takes a dict containing DICOM image volumes (numpy arrays), then creates a pandas DataFrame containing
    all unique combinations of tissue type, HU Low, and HU High, then calculates SPR for each combination.

    The function expects the input dict to contain the following arrays:
    - reference image
    - keV low
    - keV high
    - mu low
    - mu high
    - HU low
    - HU high
    - SPR (empty)

     The function returns a SPR Look-Up Table in the form of a Pandas DataFrame.

    :return: DataFrame
    """

    pandas_array = np.array(
        [
            image_dict[con.REF_KEV].flatten(),
            image_dict[con.KEV_LOW].flatten(),
            image_dict[con.KEV_HIGH].flatten(),
            image_dict[con.MU_LOW].flatten(),
            image_dict[con.MU_HIGH].flatten(),
            image_dict[con.HU_LOW].flatten(),
            image_dict[con.HU_HIGH].flatten(),
            image_dict[con.SPR].flatten(),
            image_dict[con.REF_COPY].flatten()
        ]
    )

    column_names = [
        con.REF_KEV,
        con.KEV_LOW,
        con.KEV_HIGH,
        con.MU_LOW,
        con.MU_HIGH,
        con.HU_LOW,
        con.HU_HIGH,
        con.SPR,
        con.REF_COPY]

    images_df = pd.DataFrame(
        pandas_array.transpose(),
        columns=column_names,
    )

    spr_lut = pd.DataFrame(
        spr_lut,
        columns=column_names)

    # remove duplicates from the images_df dataframe
    images_df = images_df.drop_duplicates(
        subset=[con.REF_KEV, con.HU_LOW, con.HU_HIGH], keep='first'
    )
    # Remove air_segment
    df_temp = pd.concat([spr_lut, images_df])
    df_temp = df_temp[df_temp[con.REF_KEV] > con.AIR_SEGMENT]
    # removes the all zero row that was used to initialize spr_lut
    df_temp = df_temp.loc[(df_temp != 0).any(axis=1)]

    # If spr_lut contains more than the initial all-zero row, do not keep any duplicates.
    if spr_lut.shape[0] != 1:
        df_temp = df_temp.drop_duplicates(
            subset=[con.REF_KEV, con.HU_LOW, con.HU_HIGH], keep=False)

    # Remove any rows that have already been assigned a SPR value
    df_temp = df_temp.loc[df_temp["spr"] == 0]

    #print(df_temp.shape[0], " were added to the LUT")

    cpus = mp.cpu_count()
    if df_temp.shape[0] < cpus:
        cpus = 1
    if df_temp.shape[0] == 0:
        return df_temp.to_numpy()

    #pool = mp.Pool(processes=cpus)

    #df_temp_split = np.array_split(df_temp, cpus, 0)
    df_temp_split = [
        df_temp.iloc[start:end]
        for start, end in zip(
            np.linspace(0, len(df_temp), cpus, endpoint=False, dtype=int),
            np.linspace(0, len(df_temp), cpus + 1, dtype=int)[1:]
        )
    ]
    """hu_to_spr_vectorized = np.vectorize(hu_to_spr)



    data = get_data_for_mp_spr_calc(cpus, df_temp_split)

    multi_proc_results = pool.starmap(
        hu_to_spr_vectorized,
        data
    )"""
    data = get_data_for_mp_spr_calc(cpus, df_temp_split)

    """    multi_proc_results = pool.starmap(
        hu_to_spr_chunk,
        data
    )"""

    with mp.Pool(processes=cpus) as pool:
        multi_proc_results = pool.starmap(
            hu_to_spr_chunk,
            data
        )


    #df_temp[con.SPR] = [item for sublist in multi_proc_results for item in sublist]

    #df_temp[con.SPR][df_temp[con.SPR] < 0.0000001] = 0

    df_temp[con.SPR] = [item for sublist in multi_proc_results for item in sublist]

    df_temp.loc[df_temp[con.SPR] < 0.0000001, con.SPR] = 0

    # If spr_lut contains more than the initial all-zero row, do not keep any duplicates.

    # TODO: this drop_duplicates in probably not necessary
    df_temp = df_temp.drop_duplicates(
        subset=[con.REF_KEV, con.HU_LOW, con.HU_HIGH], keep='first')

    # join the old and new SPR, then remove duplicates between them.
    df_temp = pd.concat([spr_lut, df_temp])
    df_temp = df_temp.drop_duplicates(
        subset=[con.REF_KEV, con.HU_LOW, con.HU_HIGH], keep='first'
    )

    new_spr_lut = df_temp.to_numpy()



    return new_spr_lut
