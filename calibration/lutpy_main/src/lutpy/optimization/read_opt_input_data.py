from src.lutpy import constants as con
import pandas as pd
import itertools


def get_opt_data():
    """
    This function reads the optimization data into a pandas dataframe (path specified in the constants-file),
    generates permutations of every possible keV combination, and returns the DataFrame.
    :return: list
    """

    opt_data_df = pd.read_excel(con.OPT_DATA_FILE_PATH)

    # TODO: fyller det här någon funktion?
    opt_data_df.name = r"opt_data_df"

    opt_data_df = get_kev_permutations_and_ground_truth_data(opt_data_df)

    return opt_data_df


def get_kev_permutations_and_ground_truth_data(opt_data_df):
    """
    This function returns a DataFrame
    :return:
    """

    # TODO: tror den här raden är onödig numera
    # opt_data_df["keV"] = opt_data_df["keV"].astype(int)

    # read "linear attenuation for water"-data into a pandas DataFrame, merge with opt_data_df on the "kev"-column and
    # calculate linear attenuation coefficients from the 'mean_hu'-column in opt_data_df
    df_h2o_att = pd.read_excel(
        "src/lutpy/resources/nist_mass_attenuation_h2o.xlsx", sheet_name="Blad2"
    )
    opt_data_df = pd.merge(opt_data_df, df_h2o_att, how="left")
    opt_data_df[con.MU] = (opt_data_df[con.MEAN_HU] / 1000 + 1) * opt_data_df[
        con.MU_H2O
    ]

    # Read ground truth EAN, ED and SPR for the optimization data
    df_ed_ean_spr = pd.read_excel(con.PHANTOM_REFERENCE_SHEET_FILE_PATH)
    opt_data_df = pd.merge(opt_data_df, df_ed_ean_spr, how="left")

    # Create a keV-dataframe with all possible permutations between kev_min and kev_max (assigned in the constants-file)
    # TODO: ändra så att den skapar permutationer av keV som finns i input data istälelt för alla mellan min och max
    lst_kev_range = list(range(con.KEV_MIN, con.KEV_MAX + 1))
    lst_kev_iterations = list(itertools.combinations(lst_kev_range, 2))
    df_keV = pd.DataFrame(lst_kev_iterations, columns=[con.KEV_LOW, con.KEV_HIGH])

    # merge keV-dataframe with mice-export Dataframe
    df_temp = opt_data_df.copy()
    df_temp = df_temp.rename(
        columns={con.KEV: con.KEV_LOW, con.MEAN_HU: con.HU_LOW, con.MU: con.MU_LOW}
    )
    df_temp_result = pd.merge(df_keV, df_temp, how="left")

    df_temp = opt_data_df.copy()
    df_temp = df_temp.rename(
        columns={con.KEV: con.KEV_HIGH, con.MEAN_HU: con.HU_HIGH, con.MU: con.MU_HIGH}
    )
    df_temp = df_temp.loc[:, [con.INSERT, con.HU_HIGH, con.KEV_HIGH, con.MU_HIGH]]

    opt_data_df_formatted = pd.merge(df_temp_result, df_temp, how="left")
    opt_data_df_formatted = opt_data_df_formatted.sort_values(
        [con.KEV_LOW, con.KEV_HIGH]
    )
    opt_data_df_formatted = opt_data_df_formatted.reset_index(drop=True)
    column_names = [
        con.KEV_LOW,
        con.KEV_HIGH,
        con.INSERT,
        con.HU_LOW,
        con.HU_HIGH,
        con.MU_LOW,
        con.MU_HIGH,
        con.EAN_REF,
        con.ED_REF,
        con.SPR_REF,
    ]
    opt_data_df_formatted = opt_data_df_formatted.reindex(columns=column_names)

    return opt_data_df_formatted
