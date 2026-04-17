import numpy as np
import scipy as sp
import scipy.constants

from src.lutpy.jack_hawk import tables


def jack_hawk_g(ean, hv):
    """
     By Torbjörn Näsmark, 2020-02-20

    This file contains the function G which takes the energy of the incident
    photon as inout and returns the expression G from Torikoshi (2001)
    :param ean:
    :param hv:
    :return:
    """
    ########################################
    # Constants
    ########################################
    e = sp.constants.e  # [C]
    c = sp.constants.c  # [m/s]
    m_e = sp.constants.m_e
    ep0 = sp.constants.epsilon_0
    energy_0 = m_e * c ** 2 / sp.constants.eV  # [J*C = eV]
    energy_0_joules = m_e * c ** 2
    pi = np.pi
    b = 0.5  # according to page 199 in Jackson & Hawkes

    # Oxygen is chosen as the reference material (Z_ref=8) since it is the most important element in tissue
    # and the reference energy is calculated according to eq 3.28
    ean_ref = 8
    hv_ref = (ean_ref / ean) ** (1 / 3) * hv

    # The coherent cross section of the reference material (Oxygen) interpolated using cubic splines from
    # table 2 in Hubbel (1975)

    sigma_ref = tables.Hubbel_tab2_ref(hv_ref)

    # The Klein Nishina Cross Section (equation 3.6a) from
    # the Lecture Note on Photon Interactions and Cross Sections by H. Hirayama (2000), KEK internal
    k = hv / energy_0  # [dimensionless]
    sigma_klein_nishina = (
        2
        * pi
        * (1 / (4 * pi * ep0) * (e ** 2 / energy_0_joules)) ** 2
        * (
            (1 + k) / k ** 2 * (2 * (1 + k) / (1 + 2 * k) - np.log(1 + 2 * k) / k)
            + np.log(1 + 2 * k) / (2 * k)
            - (1 + 3 * k) / (1 + 2 * k) ** 2
        )
    )

    # The expression G(hv,Z) given by Torikoshi et al. (july 2001), Journal of Biomedical Optics 6(3), 371-377
    torikoshi_g = sigma_klein_nishina + (1 - ean ** (b - 1)) * ean / (ean_ref ** 2) * sigma_ref

    # return the expression G from Torikoshi (2001)
    return torikoshi_g
