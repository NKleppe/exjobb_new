from src.lutpy.spr_calc.ean_solver import ean_solv
from src.lutpy.spr_calc.ed_solver import ed_calc
from src.lutpy.spr_calc.spr_calculator import spr_calc

from src.lutpy import constants as con
import numpy as np

def hu_to_spr(
        hu_low: float,
        hu_high: float,
        n_exp,
        kev_low,
        kev_high,
        water_attenuation_low,
        water_attenuation_high
):
    """
     By Torbjörn Näsmark, 2021-10-05

     This file contains the function hu_to_spr which takes as argument:
       - two HU values as input (hu_low, hu_high),
       - the exponent n from the Bethe equation,
       - two energy levels (kev_low, kev_high)
       - two attenuation coefficients for water corresponding
           to the two energies (water_attenuation_low, water_attenuation_high)

     The script decides which tissue pair to use and then determines proton stopping power ratio (SPR) using the method
     described in Näsmark and Andersson (2021). The function output is the SPR value.

     The functions ean_solver, ed_calc, and spr, are used to determine the effective atomic number (EAN), the electron
     density (ED), and SPR.  photon as inout and returns:

     Näsmark and Andersson (2021): Proton stopping power prediction based on dual-energy ct-generated virtual
     monoenergetic images. Torbjörn Näsmark, Jonas Andersson. Med Phys. 2021 Jul 2. doi: 10.1002/mp.15066

    :param hu_low: int
    :param hu_high: int
    :param n_exp: float
    :param kev_low: int
    :param kev_high: int
    :param water_attenuation_low: float
    :param water_attenuation_high: float
    :return: spr: float
    """

    # calculate attenuation coefficients from the HU-values
    mu_low = (hu_low / 1000 + 1) * water_attenuation_low
    mu_high = (hu_high / 1000 + 1) * water_attenuation_high

    # Determine the EAN, ED, and SPR
    ean = ean_solv(mu_low, mu_high, kev_low, kev_high)
    ed = ed_calc(mu_low, mu_high, ean, kev_low, kev_high)
    spr = spr_calc(ed, ean)

    return spr


def hu_to_spr_cal(
        kev_low,
        kev_high,
        mu_low,
        mu_high
):
    """
     By Torbjörn Näsmark, 2023-09-19

     This script takes as argument:
       - two energy levels (kev_low, kev_high)
       - two attenuation coefficients for water corresponding
           to the two energies (water_attenuation_low, water_attenuation_high)

     The functions ean_solver, ed_calc, and spr, are used to determine the effective atomic number (EAN), the electron
     density (ED), and SPR.  photon as inout and returns:

     Näsmark and Andersson (2021): Proton stopping power prediction based on dual-energy ct-generated virtual
     monoenergetic images. Torbjörn Näsmark, Jonas Andersson. Med Phys. 2021 Jul 2. doi: 10.1002/mp.15066

    :param kev_low: int
    :param kev_high: int
    :param water_attenuation_low: float
    :param water_attenuation_high: float
    :return: spr: float
    """

    # Determine the EAN, ED, and SPR
    ean = ean_solv(mu_low, mu_high, kev_low, kev_high)
    ed = ed_calc(mu_low, mu_high, ean, kev_low, kev_high)
    spr = spr_calc(ed, ean)

    ean = float(np.asarray(ean).squeeze())
    ed = float(np.asarray(ed).squeeze())
    spr = float(np.asarray(spr).squeeze())

    return ean, ed, spr

def hu_to_spr_3(
        kev_low,
        kev_high,
        mu_low,
        mu_high
):
    """
     By Torbjörn Näsmark, 2021-10-05

     This file contains the function hu_to_spr which takes as argument:
       - two HU values as input (hu_low, hu_high),
       - the exponent n from the Bethe equation,
       - two energy levels (kev_low, kev_high)
       - two attenuation coefficients for water corresponding
           to the two energies (water_attenuation_low, water_attenuation_high)

     The script decides which tissue pair to use and then determines proton stopping power ratio (SPR) using the method
     described in Näsmark and Andersson (2021). The function output is the SPR value.

     The functions ean_solver, ed_calc, and spr, are used to determine the effective atomic number (EAN), the electron
     density (ED), and SPR.  photon as inout and returns:

     Näsmark and Andersson (2021): Proton stopping power prediction based on dual-energy ct-generated virtual
     monoenergetic images. Torbjörn Näsmark, Jonas Andersson. Med Phys. 2021 Jul 2. doi: 10.1002/mp.15066

    :param hu_low: int
    :param hu_high: int
    :param n_exp: float
    :param kev_low: int
    :param kev_high: int
    :param water_attenuation_low: float
    :param water_attenuation_high: float
    :return: spr: float
    """

    # Determine the EAN, ED, and SPR
    ean = ean_solv(mu_low, mu_high, kev_low, kev_high)
    ed = ed_calc(mu_low, mu_high, ean, kev_low, kev_high)
    spr = spr_calc(ed, ean, con.N_EXP)

    return ean, ed, spr
if __name__ == "__main__":
    spr = hu_to_spr_cal(51000, 61000, 0.8010180812370546, 0.5952612884916816)
    print(spr)