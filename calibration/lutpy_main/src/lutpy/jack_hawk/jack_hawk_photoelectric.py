# jack_hawk_photoelectric.py
#
# By Torbjörn Näsmark, 2020-02-05
#
# This file contains the function F which takes Z (ranging from 6 to 54)
# and hv (ranging from 10 keV to 400 keV), and returns:
# 0 - The expression F(hv, Z) as given by Torikoshi et al (2001)
#
#
# (D.F Jackson and D.J. Hawkes, "X-ray attenuation coefficients of elements and mixture",
#      Phys Rep. 70 (1981), 169-233)
#
import numpy as np
import scipy as sp
import scipy.constants

from src.lutpy.jack_hawk import tables


def jack_hawk_f(ean, hv):

    ########################################
    # Constants
    ########################################
    m_e = sp.constants.m_e
    c = sp.constants.c
    energy_0 = m_e * c ** 2 / sp.constants.eV
    energy_0_joules = m_e * c ** 2
    e = sp.constants.e
    alpha = sp.constants.alpha
    ep0 = sp.constants.epsilon_0
    pi = np.pi

    ########################################
    # Binding Energies and derivatives
    ########################################

    # (eq. 2.9 and 2.)
    eps_k = 0.5 * (ean * alpha) ** 2 * energy_0
    eps_l = eps_k / 4

    # (eq. 2.12 and 2.22)
    n1 = np.sqrt(eps_k / (hv - eps_k))
    n2 = 2 * np.sqrt(eps_l / (hv - eps_l))

    # (eq. 2.13 and 2.23)
    f_n1 = np.exp(-4 * n1 * np.arctan(1 / n1)) / (1 - np.exp(-2 * pi * n1))
    f_n2 = np.exp(-4 * n2 * np.arctan(2 / n2)) / (1 - np.exp(-2 * pi * n2))

    ########################################
    # The Velocity of the Electron
    ########################################

    # The kinetic energy of the electron
    t_k = (hv - eps_k) * e
    t_l = (hv - eps_l) * e

    # The relativistic velocity of the electron
    v_k_rel = c * np.sqrt(1 - (energy_0_joules / (t_k + energy_0_joules)) ** 2)
    v_l_rel = c * np.sqrt(1 - (energy_0_joules / (t_l + energy_0_joules)) ** 2)

    # Ratio between relativistic velocity of electron and
    # the speed of light
    beta_k = v_k_rel / c
    beta_l = v_l_rel / c

    ########################################
    # The Shell Ratios
    ########################################

    # (eq. 2.19 and 2.20)
    shell_ratio_2_s = 8 * (eps_l / eps_k) ** 3 * (1 + 3 * eps_l / hv) * f_n2 / f_n1
    shell_ratio_2_p = 8 * eps_l ** 4 / (hv * eps_k ** 3) * (3 + 8 * eps_l / hv) * f_n2 / f_n1

    ########################################
    # The correction term N
    ########################################

    # Interpolated from table A1 in Scofield
    n1_s = tables.Scofield_N_interpolation(ean, 1)
    n2_s = tables.Scofield_N_interpolation(ean, 2)
    n2_p_m = tables.Scofield_N_interpolation(ean, 3)
    n2_p_p = tables.Scofield_N_interpolation(ean, 4)

    ########################################
    # The correction term O
    ########################################

    # (eq. 2.52)
    o1s = 1
    o2s = 1
    o2_pmin = 1 / 9
    o2_pplus = 8 / 9

    ########################################
    # The Correction term G
    ########################################

    # (equation in text, between eq. 2.54 and 2.55). The Vk-values are
    # found by interpolation in table 2 from Mcellan et al.
    # (Physical Review A, 1976)
    lambda2 = tables.McEllan_Vk_interpolation(ean, 1) * (1.13 * ean ** (-2 / 3)) ** 2
    lambda3 = tables.McEllan_Vk_interpolation(ean, 2) * (1.13 * ean ** (-2 / 3)) ** 3

    # (eq. 2.55 a-d)
    q1s = n1 ** 2 * (
        (3 + 2 * n1 ** 2) / (1 + n1 ** 2) - 2 * n1 * np.arctan(1 / n1) - pi * n1 / (np.exp(2 * pi * n1) - 1)
    )
    q2s = n2 ** 2 * (
        (3 + 4 * n2 ** 2) / (1 + n2 ** 2) - 2 * n2 * np.arctan(2 / n2) - pi * n2 / (np.exp(2 * pi * n2) - 1)
    )
    q2_pplus = n2 ** 2 * (
        (16 + 23 * n2 ** 2 + 4 * n2 ** 4) / ((4 + n2 ** 2) * (1 + n2 ** 2))
        - 2 * n2 * np.arctan(2 / n2)
        - pi * n2 / (np.exp(2 * pi * n2) - 1)
    )
    q2_pmin = n2 ** 2 * (4 - 2 * n2 * np.arctan(2 / n2) - pi * n2 / (np.exp(2 * pi * n2) - 1))

    # (eq. 2.54 a-d)
    g1s = lambda2 * (q1s * (3 * n1 ** 2 + 5) - 8 * n1 ** 2 / (1 + n1 ** 2) * (2 + n1 ** 2) + 3 * n1 ** 2) - lambda3 * (
        q1s * (5 * n1 ** 2 * (1 + n1 ** 2) - 6)
        + 4 / 3 * n1 ** 2 / (1 + n1 ** 2) ** 2 * (6 + 7 * n1 ** 2 - 21 * n1 ** 4 - 10 * n1 ** 6)
        + 5 * n1 ** 4
    )
    g2s = lambda2 * (
        q2s * (3 * n2 ** 2 + 14) - 16 * n2 ** 2 / (4 + n2 ** 2) * (7 + n2 ** 2) + 3 * n2 ** 2
    ) - lambda3 * (
        q2s * (5 * n2 ** 2 * (1 + n2 ** 2) - 84)
        + 32 * n2 ** 2 / (4 + n2 ** 2) ** 2 * (56 + 40 * n2 ** 2 / 3 - 11 * n2 ** 4 / 2 - 5 * n2 ** 6 / 6)
        + 5 * n2 ** 4
    )
    g2_pplus = lambda2 * (
        q2_pplus * (3 * n2 ** 2 + 16) - 8 * n2 ** 2 / (4 + n2 ** 2) * (5 * n2 ** 2 + 28) + 15 * n2 ** 2
    ) - lambda3 * (
        q2_pplus * (n2 ** 2 * (5 * n2 + 17) - 60)
        - 8 * n2 ** 2 / (3 * (4 + n2 ** 2) ** 2) * (25 * n2 ** 6 + 210 * n2 ** 4 + 200 * n2 ** 2 - 432)
        + 25 * n2 ** 4
    )

    g2_pmin = lambda2 * (q2_pmin * (3 * n2 ** 2 + 10) - 2 * n2 ** 2 / (4 + n2 ** 2) * (8 * n2 ** 2 + 40)) - lambda3 * (
        q2_pmin * (n2 ** 2 * (5 * n2 ** 2 - 1) - 60)
        - 16 * n2 ** 2 / (3 * (4 + n2 ** 2) ** 2) * (5 * n2 ** 6 + 27 * n2 ** 4 - 128 * n2 ** 2 - 432)
    )

    ########################################
    # The F+1 correction term
    ########################################

    # (eq. 2.61)
    f_plus_one_1_s = 1 + 0.143 * beta_k ** 2 + 1.667 * beta_k ** 8
    f_plus_one_2_s = 1 + 0.143 * beta_l ** 2 + 1.667 * beta_l ** 8

    ########################################
    # %% The Tabulated values of Scofield
    ########################################
    # Sco_K, Sco_L = Tables.Scofield_tabA2_kl_shell(Z,hv)
    # Sco_KL = (Sco_K + Sco_L)

    ########################################
    # %% The Cross Sections
    ########################################

    # The Thompson Cross Section
    # (eq. 2.6)
    phi_0 = (8 / 3) * pi * (1 / (4 * pi * ep0) * (e ** 2 / energy_0_joules)) ** 2  # [m^2/electron]

    # The Born approximation
    # (eq. 2.5) [m^2/electron]
    born = 4 * np.sqrt(2) * ean ** 5 * alpha ** 4 * (energy_0 / hv) ** 3.5 * phi_0

    # The Stobbe Cross Section
    # (eq. 2.11)
    stobbe = born * 2 * pi * np.sqrt(eps_k / hv) * f_n1

    ########################################
    # Final expression for the Photoelectric cross section
    ########################################

    # (eq. 2.62) [m^2/electron]
    eq_262 = stobbe * (
        n1_s * o1s * (1 + g1s) * f_plus_one_1_s
        + shell_ratio_2_s * n2_s * o2s * (1 + g2s) * f_plus_one_2_s
        + shell_ratio_2_p * n2_p_m * o2_pmin * (1 + g2_pmin) * f_plus_one_2_s
        + shell_ratio_2_p * n2_p_p * o2_pplus * (1 + g2_pplus) * f_plus_one_2_s
    )

    # The expression F(hv,Z) given by
    # Torikoshi et al. (july 2001), Journal of Biomedical Optics 6(3), 371-377
    # [m^2/electron]
    torikoshi_f = eq_262 / (ean ** 5)

    return torikoshi_f
