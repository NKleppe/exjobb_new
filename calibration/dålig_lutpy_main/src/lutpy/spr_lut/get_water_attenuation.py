import pandas as pd
from src.lutpy import constants as con


def get_water_attenuation() -> dict:
    """
    This function loads the attenuation coefficients for water and convert the keV-column to strings
    so that specific coefficients can be found with df.loc using keV as index, then calculates the
    linear attenuation coefficient of water corresponding to the optimal energy pairs defined in
    the file constants.py

    The function returns a dict containing the water attenuation coefficients for the different energy pairs
    corresponding to LUNG TISSUE, SOFT TISSUE, and BONE.
    :return: dict
    """

    df_h2o_att = pd.read_excel("src/lutpy/resources/nist_mass_attenuation_h2o.xlsx", sheet_name="Blad1", index_col=0)
    df_h2o_att.index = df_h2o_att.index.astype(int, copy=False)
    df_h2o_att.index = df_h2o_att.index.astype(str, copy=False)


    water_attenuation = {
        con.LUNG_LOW: df_h2o_att.loc[[str(con.KEV_LUNG_LOW)], ["mu"]].values[0][0],
        con.LUNG_HIGH: df_h2o_att.loc[[str(con.KEV_LUNG_HIGH)], ["mu"]].values[0][0],
        con.SOFT_LOW: df_h2o_att.loc[[str(con.KEV_SOFT_LOW)], ["mu"]].values[0][0],
        con.SOFT_HIGH: df_h2o_att.loc[[str(con.KEV_SOFT_HIGH)], ["mu"]].values[0][0],
        con.BONE_LOW: df_h2o_att.loc[[str(con.KEV_BONE_LOW)], ["mu"]].values[0][0],
        con.BONE_HIGH: df_h2o_att.loc[[str(con.KEV_BONE_HIGH)], ["mu"]].values[0][0],
    }

    return water_attenuation

