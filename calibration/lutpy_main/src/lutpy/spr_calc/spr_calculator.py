import numpy
import numpy as np
import scipy as sp
import scipy.constants

from src.lutpy import constants as con


def spr_calc(ed: float, ean: float) -> float:
    """
    This function takes electron density (ED) and the effective atomic number (EAN)
    and the exponent "n" used for Z_eff to calculate the stopping power ratio (SPR)

    Torbjörn Näsmark, 2020-04-06

    :return:
    """

    # Constants
    m_e = sp.constants.m_e  # [kg]
    c = sp.constants.c  # [m/s]
    m_p = sp.constants.m_p  # [kg] , protonens massa
    i_h20 = 78.73  # [eV], from Bär et al. (2018)
    n = con.N_EXP
    # I_H20 = 75

    # Calculate ln(I_x) with the parametrization given by Yang et al (2010). One parametrization is used for soft tissue
    # (Z<=8.5) and one for bone (Z>8.5). The constants a1, a2, b1, b2 are calculated from elemental I-values taken from
    # Bär 2018 och ICRU 37

    if n == 3.0:
        a1 = 0.1324
        b1 = 3.3577
        a2 = 0.1025
        b2 = 3.3805

    elif n == 3.1:
        a1 = 0.1315
        b1 = 3.3601
        a2 = 0.1028
        b2 = 3.3639

    elif n == 3.21:
        a1 = 0.1305
        b1 = 3.3634
        a2 = 0.1032
        b2 = 3.3448

    elif n == 3.3:
        a1 = 0.1296
        b1 = 3.3666
        a2 = 0.1036
        b2 = 3.3285

    elif n == 3.4:
        a1 = 0.1285
        b1 = 3.3709
        a2 = 0.1041
        b2 = 3.3098

    elif n == 3.5:
        a1 = 0.1274
        b1 = 3.3758
        a2 = 0.1047
        b2 = 3.2904

    if ean <= 8.5:
        ln_ix = a1 * ean + b1
    else:
        ln_ix = a2 * ean + b2

    # Logarithm of the mean ionization value for water
    ln_i_h20 = numpy.log(i_h20)

    # Proton velocity.
    energy = con.PROTON_ENERGY  # [J]
    v = numpy.sqrt(2 * energy / m_p)  # [m/s]
    beta2 = v / c

    # Relative electron density
    ed_h2o = 3.343 * 10 ** 23  # [cm^-3]
    red = ed / ed_h2o

    # SPR calculated with the Bethe equation.

    if np.isnan(red):
        spr = np.NAN
    else:
        spr = red * (
                (numpy.log(2 * m_e * c ** 2 * beta2 ** 2 / ((1 - beta2 ** 2) * 1.602 * 10 ** (-19))) - beta2 ** 2 - ln_ix)
                / (numpy.log(2 * m_e * c ** 2 * beta2 ** 2 / ((1 - beta2 ** 2) * 1.602 * 10 ** (-19))) - beta2 ** 2 - ln_i_h20)
        )

    return spr
