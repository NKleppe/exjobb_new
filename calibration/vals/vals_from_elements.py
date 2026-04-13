# Nelly Kleppe 13/4 2026
import numpy as np
import scipy as sp
import pandas as pd


# global constants
n = 3.21
N_A = sp.constants.N_A # Avogadro's number
dens_w = 1
Ng_w = N_A*(0.111894*1/1.008 + 0.888106*8/15.999)  # fractions from nist, water. A from CT calibration sheet
rho_e_w = dens_w*Ng_w  # electron density of water
m_e = sp.constants.m_e
c = sp.constants.c
eV = sp.constants.electron_volt
m_p = sp.constants.physical_constants["proton mass energy equivalent in MeV"][0]


def Zeff(w, Z, A):
    sum1 = 0
    sum2 = 0
    for i in range(len(w)):
        temp = w[i]*Z[i]/A[i]
        sum1 += temp*np.power(Z[i], n)
        sum2 += temp
    return np.power(sum1/sum2, (1/n))


def ED(rho, w, Z, A):
    sum_ = 0
    for i in range(len(w)):
        sum_ += w[i] * Z[i] / A[i]
    return rho*N_A*sum_


def I_vals(w, Z, A, I):
    sum1 = 0
    sum2 = 0
    for i in range(len(w)):
        temp = w[i] * Z[i] / A[i]
        sum1 += temp * np.log(I[i])
        sum2 += temp
    return sum1/sum2


import numpy as np
import scipy as sp

def spr_calc(red, I, I_w=78.73, proton_energy_MeV=100.0):
    # proton beta from kinetic energy T
    T = proton_energy_MeV
    gamma = 1.0 + T / m_p
    beta2 = 1.0 - 1.0 / (gamma ** 2)

    # 2 m_e c^2 beta^2 in eV
    K_eV = 2.0 * m_e * c**2 * beta2 / eV

    # Bethe-log term
    term_mat = np.log(K_eV / I) - beta2
    term_w = np.log(K_eV / I_w) - beta2

    spr = red * (term_mat / term_w)
    return spr


# read in elemental info (originally from CT calibration sheet)
file_path_elements = r"C:\Users\Nelly Kleppe\PycharmProjects\exjobb\calibration\vals\elements.xlsx"
elements_df = pd.read_excel(file_path_elements)
for col in ["Ai", "Ii"]:
    elements_df[col] = (
        elements_df[col]
        .astype(str)
        .str.replace(",", ".", regex=False)
        .astype(float)
    )
elements_df["Zi"] = elements_df["Zi"].astype(int)


# read in insert info
file_path_inserts = r"C:\Users\Nelly Kleppe\PycharmProjects\exjobb\calibration\vals\inserts.xlsx"
insert_df = pd.read_excel(file_path_inserts)
# clean insert table
insert_df.columns = insert_df.columns.str.strip()
insert_df["Tissue type"] = insert_df["Tissue type"].ffill()

# keep only what you need
element_cols = elements_df["Element"].tolist()
keep_cols = ["Insert name", "Density (g/cm3)"] + element_cols
insert_df = insert_df[keep_cols]

# convert decimal commas to floats
for col in ["Density (g/cm3)"] + element_cols:
    insert_df[col] = (
        insert_df[col]
        .astype(str)
        .str.replace(",", ".", regex=False)
        .replace("", "0")
        .astype(float)
    )

# lookup tables for element data
Z_map = dict(zip(elements_df["Element"], elements_df["Zi"]))
A_map = dict(zip(elements_df["Element"], elements_df["Ai"]))
I_map = dict(zip(elements_df["Element"], elements_df["Ii"]))

rows = []

for _, row in insert_df.iterrows():
    rho = row["Density (g/cm3)"]
    w = row[element_cols].to_numpy(dtype=float)

    # keep only nonzero weights
    mask = w > 0
    w = w[mask]
    elems = np.array(element_cols)[mask]

    Z = np.array([Z_map[e] for e in elems], dtype=float)
    A = np.array([A_map[e] for e in elems], dtype=float)
    I = np.array([I_map[e] for e in elems], dtype=float)

    zeff = Zeff(w, Z, A)
    ed = ED(rho, w, Z, A)
    red = ed/rho_e_w
    I_val = np.exp(I_vals(w, Z, A, I))
    spr = spr_calc(red, zeff, n)

    rows.append({
        "insert": row["Insert name"],
        "density": rho,
        "ean_ref": zeff,
        "ed_ref": ed,
        "red_ref": red,
        "spr_ref": spr
    })

result_df = pd.DataFrame(rows)
print(result_df.head())

output_path = r"C:\Users\Nelly Kleppe\PycharmProjects\exjobb\calibration\lutpy_main\src\lutpy\resources\nelly_constants_output.xlsx"
result_df.to_excel(output_path, index=False)
