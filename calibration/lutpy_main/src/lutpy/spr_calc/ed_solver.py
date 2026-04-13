from src.lutpy.jack_hawk.jack_hawk_compton import jack_hawk_g
from src.lutpy.jack_hawk.jack_hawk_photoelectric import jack_hawk_f


def ed_calc(mu_1: float, mu_2: float, ean: float, hv_low: int, hv_high: int) -> float:
    """
    This function is used to solve for ED given the attenuation coefficients and EAN

    :return: ed: float
    """

    g1 = jack_hawk_g(ean, hv_low)[0]  # m^2
    g2 = jack_hawk_g(ean, hv_high)[0]  # m^2
    f1 = jack_hawk_f(ean, hv_low)[0]  # m^2
    f2 = jack_hawk_f(ean, hv_high)[0]  # m^2

    return ((mu_1 * f2 - mu_2 * f1) / (f2 * g1 - f1 * g2)) / 10000  # [m^(-3)]
