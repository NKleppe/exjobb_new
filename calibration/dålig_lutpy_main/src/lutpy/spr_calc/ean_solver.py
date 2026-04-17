from scipy.optimize import minimize
from src.lutpy.jack_hawk.jack_hawk_compton import jack_hawk_g
from src.lutpy.jack_hawk.jack_hawk_photoelectric import jack_hawk_f
import numpy as np
from scipy.optimize import root_scalar

def ean_solv(mu_1: float, mu_2: float, hv_low: int, hv_high: int) -> float:
    """
    This function is used to iteratively solve for the EAN given two attenuation coefficients
    and two energies as arguments

    :rtype: object
    """

    def objective(ean):
        g1 = jack_hawk_g(ean, hv_low)[0]   # m^2
        g2 = jack_hawk_g(ean, hv_high)[0]  # m^2
        f1 = jack_hawk_f(ean, hv_low)[0]   # m^2
        f2 = jack_hawk_f(ean, hv_high)[0]  # m^2
        return abs(((mu_2*g1-mu_1*g2) / (mu_1*f2-mu_2*f1)) - ean ** 4)
    #
    # Boundry
    bnds = [(4, 54)]

    # initial guess for the effective atomic number. Starting guess depends on the attenuation coefficient
    # from the low energy image
    #z0 = 7 if mu_1 < 0.3 else 12

    if mu_1 < 0.3:
        z0 = 5
    else:
        z0 = 12

    # solve iteratively for the effective atomic number by minimizing the objective function
    # and return the value
    sol = minimize(objective, np.array(z0), method='SLSQP', bounds=bnds)
    return sol.x



