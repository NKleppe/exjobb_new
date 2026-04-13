from src.lutpy.spr_calc.hu_to_spr import hu_to_spr_cal
from src.lutpy.spr_lut.get_data_for_mp_spr_calc import get_lst_of_tuples_from_df
import numpy as np
import pandas as pd
import src.lutpy.constants as con
import multiprocessing as mp


def get_spr_optimization(opt_data_df) -> list:
    """
    This script:
        - checks the number of cpus on the computer running the script
        - splits opt_data_df into (number of cpus) equal chunks in a list of DataFrames
        - as a vectorized function can't take DataFrames as input, transform the list of DataFrames into a list of
        tuples, where each tuple element is a DataFrame column (Series)
        - vectorize the script hu_to_spr_cal
        - calculate EAN, RED and SPR using multiprocessing to run the split data through the vectorized function
        hu_to_spr_cal
        - merge the results from all instances of hu_to_spr_cal and append to opt_data_df

    then uses multiprocessing to speed up the EAN, RED and SPR calculations
    :param opt_data_df:
    :return opt_data_df:
    """

    # count cpus
    cpus = mp.cpu_count()
    pool = mp.Pool(processes=cpus)
    # split data into equal chunks
    opt_data_df_split = np.array_split(opt_data_df, cpus, 0)
    # turn the list of DataFrames to a list of tuples
    data = get_lst_of_tuples_from_df(cpus, opt_data_df_split)

    # the script hu_to_spr_cal is used to calculate EAN, RED and SPR for each row in the input data.
    # Here we use multiprocessing to speed up the EAN, RED and SPR calculations.

    # vectorize the function hu_to_spr_cal
    hu_to_spr_vectorized = np.vectorize(hu_to_spr_cal)

    # run the vectorized hu_to_spr_cal with multiprocessing to speed up the calculations
    multi_proc_results = pool.starmap(hu_to_spr_vectorized, data)

    # merge the results from each instance of the vectorized hu_to_spr and append to opt_data_df
    opt_data_df = add_mp_results_to_opt_data(opt_data_df, multi_proc_results, cpus)

    # calculate relative spr deviation from ground truth
    # TODO: varna om inte referensdata går att hitta för alla inserts
    opt_data_df = get_relative_spr_deviation(opt_data_df)

    # to prepare for the root mean square error calculation, removes unnecessary columns,
    # transform from a DataFrame with one "insert" and one "spr_dev"-column, to a DataFrame with
    # multiple insert-specific "spr_dev" columns.
    opt_data_df = prepare_df_for_rmse_calculation(opt_data_df)

    # calculate the root-mean-square-error for different tissue types (lung, soft, bone)
    # TODO: varna för (eller ta bort) rader utan RMSE
    rmse_dict = get_rmse(opt_data_df)

    return rmse_dict

def get_rmse(opt_data_df):
    # split data on tissue type
    opt_data_df_lung, opt_data_df_soft, opt_data_df_bone = split_df_on_tissue_type(
        opt_data_df
    )

    # calculate rmse
    df_rmse_lung = rmse_calculator(opt_data_df_lung)
    df_rmse_soft = rmse_calculator(opt_data_df_soft)
    df_rmse_bone = rmse_calculator(opt_data_df_bone)

    # sort based on rmse
    df_rmse_lung = df_rmse_lung.sort_values(by=con.RMSE)
    df_rmse_soft = df_rmse_soft.sort_values(by=con.RMSE)
    df_rmse_bone = df_rmse_bone.sort_values(by=con.RMSE)

    # read reference data set
    df_rmse_lung_ww = pd.read_excel(
        open("src/lutpy/resources/woodard_white_energy_pairs.xlsx", "rb"),
        sheet_name="ww_lung",
    )
    df_rmse_soft_ww = pd.read_excel(
        open("src/lutpy/resources/woodard_white_energy_pairs.xlsx", "rb"),
        sheet_name="ww_soft",
    )
    df_rmse_bone_ww = pd.read_excel(
        open("src/lutpy/resources/woodard_white_energy_pairs.xlsx", "rb"),
        sheet_name="ww_bone",
    )

    # merge reference data with optimization data
    df_rmse_lung_ww = pd.merge(df_rmse_lung_ww, df_rmse_lung, how="left")
    df_rmse_soft_ww = pd.merge(df_rmse_soft_ww, df_rmse_soft, how="left")
    df_rmse_bone_ww = pd.merge(df_rmse_bone_ww, df_rmse_bone, how="left")

    # sort by rmse
    df_rmse_lung_ww = df_rmse_lung_ww.sort_values(by=con.RMSE).reset_index(drop=True)
    df_rmse_soft_ww = df_rmse_soft_ww.sort_values(by=con.RMSE).reset_index(drop=True)
    df_rmse_bone_ww = df_rmse_bone_ww.sort_values(by=con.RMSE).reset_index(drop=True)

    # create a df with the optimal VMI pairs for lung tissue, soft tissue, and bone
    df_optimal_pairs = pd.DataFrame([
        df_rmse_lung_ww.loc[0, [con.KEV_LOW, con.KEV_HIGH, con.RMSE]].to_dict(),
        df_rmse_soft_ww.loc[0, [con.KEV_LOW, con.KEV_HIGH, con.RMSE]].to_dict(),
        df_rmse_bone_ww.loc[0, [con.KEV_LOW, con.KEV_HIGH, con.RMSE]].to_dict(),
    ], index=[con.LUNG, con.SOFT, con.BONE])

    # optional: keep tissue type as a normal column instead of index
    df_optimal_pairs = df_optimal_pairs.reset_index().rename(columns={"index": "tissue_type"})

    rmse_dict = {
        con.LUNG: df_rmse_lung,
        con.SOFT: df_rmse_soft,
        con.BONE: df_rmse_bone,
        con.LUNG_COMPLIANT_WITH_REF: df_rmse_lung_ww,
        con.SOFT_COMPLIANT_WITH_REF: df_rmse_soft_ww,
        con.BONE_COMPLIANT_WITH_REF: df_rmse_bone_ww,
        con.OPTIMAL_VMI: df_optimal_pairs,
    }
    return rmse_dict
def get_rmse_old(opt_data_df):

    # split data on tissue type
    opt_data_df_lung, opt_data_df_soft, opt_data_df_bone = split_df_on_tissue_type(
        opt_data_df
    )

    # calculate rmse
    df_rmse_lung = rmse_calculator(opt_data_df_lung)
    df_rmse_soft = rmse_calculator(opt_data_df_soft)
    df_rmse_bone = rmse_calculator(opt_data_df_bone)

    # sort based on rmse
    df_rmse_lung = df_rmse_lung.sort_values(by=con.RMSE)
    df_rmse_soft = df_rmse_soft.sort_values(by=con.RMSE)
    df_rmse_bone = df_rmse_bone.sort_values(by=con.RMSE)

    # TODO: stämmer <1%?
    # read reference data set (woodard and white). This data set contains only the VMI pairs
    # that yield acceptable SPR root mean square errors within a certain threshold (<1%)
    df_rmse_lung_ww = pd.read_excel(
        open("src/lutpy/resources/woodard_white_energy_pairs.xlsx", "rb"),
        sheet_name="ww_lung",
    )
    df_rmse_soft_ww = pd.read_excel(
        open("src/lutpy/resources/woodard_white_energy_pairs.xlsx", "rb"),
        sheet_name="ww_soft",
    )
    df_rmse_bone_ww = pd.read_excel(
        open("src/lutpy/resources/woodard_white_energy_pairs.xlsx", "rb"),
        sheet_name="ww_bone",
    )

    # merge reference data with optimization data, --> excluding VMI pairs that yield
    # SPR root mean square errors above a certain threshold (<1%)
    df_rmse_lung_ww = pd.merge(df_rmse_lung_ww, df_rmse_lung, how="left")
    df_rmse_soft_ww = pd.merge(df_rmse_soft_ww, df_rmse_soft, how="left")
    df_rmse_bone_ww = pd.merge(df_rmse_bone_ww, df_rmse_bone, how="left")

    # sort by rmse
    df_rmse_lung_ww = df_rmse_lung_ww.sort_values(by=con.RMSE)
    df_rmse_soft_ww = df_rmse_soft_ww.sort_values(by=con.RMSE)
    df_rmse_bone_ww = df_rmse_bone_ww.sort_values(by=con.RMSE)

    # reset index
    df_rmse_lung_ww = df_rmse_lung_ww.reset_index(drop=True)
    df_rmse_soft_ww = df_rmse_soft_ww.reset_index(drop=True)
    df_rmse_bone_ww = df_rmse_bone_ww.reset_index(drop=True)

    # create a df with the optimal VMI pairs for lung tissue, soft tissue, and bone
    df_optimal_pairs = df_rmse_lung_ww.loc[0, [con.KEV_LOW, con.KEV_HIGH, con.RMSE]]
    df_optimal_pairs = df_optimal_pairs.append(
        df_rmse_soft_ww.loc[0, [con.KEV_LOW, con.KEV_HIGH, con.RMSE]]
    )
    df_optimal_pairs = df_optimal_pairs.append(
        df_rmse_bone_ww.loc[0, [con.KEV_LOW, con.KEV_HIGH, con.RMSE]]
    )

    # store the DataFrames in a dict
    rmse_dict = {
        con.LUNG: df_rmse_lung,
        con.SOFT: df_rmse_soft,
        con.BONE: df_rmse_bone,
        con.LUNG_COMPLIANT_WITH_REF: df_rmse_lung_ww,
        con.SOFT_COMPLIANT_WITH_REF: df_rmse_soft_ww,
        con.BONE_COMPLIANT_WITH_REF: df_rmse_bone_ww,
        con.OPTIMAL_VMI: df_optimal_pairs,
    }
    return rmse_dict


def rmse_calculator(opt_data_df):

    opt_data_df[con.RMSE] = opt_data_df.loc[
        :, opt_data_df.columns.str.contains(con.SPR_DEV)
    ].pow(2).mean(axis=1) ** (1 / 2)

    df_rmse = opt_data_df.loc[:, [con.KEV_LOW, con.KEV_HIGH, con.RMSE]]

    return df_rmse


def prepare_df_for_rmse_calculation(opt_data_df):
    """
    This function removes uneccesary columns from the DataFrame and transforms it from one DataFrame
    with one "insert" column and a "spr_dev" column, to a DataFrame with multiple insert-specific
    "spr_dev" columns.
    :param opt_data_df:
    :return opt_data_df:
    """

    #
    # removes unnecessary columns
    opt_data_df = opt_data_df.loc[
        :, [con.KEV_LOW, con.KEV_HIGH, con.INSERT, con.SPR_DEV]
    ]
    # create a dict of DataFrames, one for each
    grouped_by_insert = opt_data_df.groupby(opt_data_df[con.INSERT])

    # Get a list of all inserts (the keys in the dict "grouped_by_insert")
    insert_lst = [insert for insert, df in grouped_by_insert]

    # Pick one group, get the keV-columns and reset the index.
    opt_data_df = grouped_by_insert.get_group(insert_lst[0])
    opt_data_df = opt_data_df.loc[:, [con.KEV_LOW, con.KEV_HIGH]]
    opt_data_df = opt_data_df.reset_index(drop=True)

    # Add one spr_dev column to opt_data_df for each insert in the input data
    for key in grouped_by_insert.groups.keys():
        new_column_name = con.SPR_DEV + " ({})".format(key)
        df_temp = grouped_by_insert.get_group(key).rename(
            columns={con.SPR_DEV: new_column_name}
        )
        df_temp = df_temp.reset_index(drop=True)
        new_column = df_temp[new_column_name]
        opt_data_df = opt_data_df.join(new_column)

    return opt_data_df


def get_relative_spr_deviation(opt_data_df):
    """
    This function returns calculates the relative EAN, ED, and SPR deviation from the
    the ground truth (ean_ref, ed_ref, spr_ref).
    :return:
    """

    # adds columns with relative deviation from ground truth for EAN, RED, and SPR
    opt_data_df[con.EAN_DEV] = opt_data_df[con.EAN] / opt_data_df[con.EAN_REF] - 1
    opt_data_df[con.ED_DEV] = opt_data_df[con.ED] / opt_data_df[con.ED_REF] - 1
    opt_data_df[con.SPR_DEV] = opt_data_df[con.SPR] / opt_data_df[con.SPR_REF] - 1

    return opt_data_df


def split_df_on_tissue_type(df):
    """
    This script splits the input DataFrame into three DataFrames, one for each tissue type (lung, soft, bone)
    The returned dataframes contain the columns kev_low and kev_high and the relevant spr_dev columns.
    :param df:
    :return:
    """
    # if column name is kev_low, kev_high or contains 'lung'
    df_lung = df.loc[
        :, df.columns.str.contains(con.KEV_LOW + "|" + con.KEV_HIGH + "|" + con.LUNG)
    ]
    # if column name does not contain 'lung' or 'bone'
    df_soft = df.loc[:, ~df.columns.str.contains(con.LUNG + "|" + con.BONE)]
    # if column name is kev_low, kev_high or contains 'bone'
    df_bone = df.loc[
        :, df.columns.str.contains(con.KEV_LOW + "|" + con.KEV_HIGH + "|" + con.BONE)
    ]

    return df_lung, df_soft, df_bone


def add_mp_results_to_opt_data(opt_data_df, multi_proc_results, cpus):
    """
    This function returns a DataFrame
    :return:
    """

    ean_array = multi_proc_results[0][0]
    ed_array = multi_proc_results[0][1]
    spr_array = multi_proc_results[0][2]

    for c in range(1, cpus):
        ean_array = np.concatenate([ean_array, multi_proc_results[c][0]], axis=0)
        ed_array = np.concatenate([ed_array, multi_proc_results[c][1]], axis=0)
        spr_array = np.concatenate([spr_array, multi_proc_results[c][2]], axis=0)


    opt_data_df[con.EAN] = ean_array
    opt_data_df[con.ED] = ed_array
    opt_data_df[con.SPR] = spr_array

    return opt_data_df
