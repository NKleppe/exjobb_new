from src.lutpy import constants as con


def get_data_for_mp_spr_calc(cpus: int, df_temp_split) -> list:
    """
    This function splits the dataframe into a number of chunks equal to the variable cpus.
    :return: list
    """
    list_of_chunks = []

    for cpu in range(cpus):
        list_of_chunks.append(
            (
                df_temp_split[cpu][con.HU_LOW],
                df_temp_split[cpu][con.HU_HIGH],
                con.N_EXP,
                df_temp_split[cpu][con.KEV_LOW],
                df_temp_split[cpu][con.KEV_HIGH],
                df_temp_split[cpu][con.MU_LOW],
                df_temp_split[cpu][con.MU_HIGH],
            )
        )

    return list_of_chunks


def get_lst_of_tuples_from_df_old(cpus: int, df_temp_split) -> list:
    """
    This function turns the df_temp_split from a list of DataFrames into a list of tuples.
    :return: list
    """
    list_of_chunks = []

    for cpu in range(cpus):
        list_of_chunks.append(
            (
                df_temp_split[cpu]["kev_low"]*1000,
                df_temp_split[cpu]["kev_high"]*1000,
                df_temp_split[cpu]["mu_low"],
                df_temp_split[cpu]["mu_high"],
            )
        )

    return list_of_chunks


def get_lst_of_tuples_from_df(cpus: int, df_temp_split) -> list:
    """
    This function turns the df_temp_split from a list of DataFrames into a list of tuples.
    :return: list
    """
    list_of_chunks = []

    for cpu in range(cpus):
        list_of_chunks.append(
            (
                (df_temp_split[cpu]["kev_low"] * 1000).to_numpy(),
                (df_temp_split[cpu]["kev_high"] * 1000).to_numpy(),
                df_temp_split[cpu]["mu_low"].to_numpy(),
                df_temp_split[cpu]["mu_high"].to_numpy(),
            )
        )

    return list_of_chunks

