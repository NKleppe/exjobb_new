from src.lutpy import constants as con
import pandas as pd
import itertools


def get_opt_data(file_path = con.OPT_DATA_FILE_PATH):
    """
    This function reads the optimization data into a pandas dataframe (path specified in the constants-file),
    generates permutations of every possible keV combination, and returns the DataFrame.
    :return: list
    """

    opt_data_df = pd.read_excel(file_path)
    # TODO: fyller det här någon funktion?
    opt_data_df.name = r"opt_data_df"
    opt_data_df = get_insert_names(opt_data_df)
    opt_data_df = create_kev_column(opt_data_df)
    opt_data_df = rename_mean_column(opt_data_df)
    opt_data_df = get_ground_truth_data(opt_data_df)
    opt_data_df = create_kev_permutations(opt_data_df)
    #opt_data_df = get_kev_permutations_and_ground_truth_data(opt_data_df)

    return opt_data_df

"""def get_insert_names(opt_data_df) -> pd.DataFrame:"""
"""
    This function checks if a column named 'insert' exists in the given dataframe. If it doesn't exist,
    the function creates this column and fills it with values looked up from another Excel file
    ('cirs062m.xlsx') based on the values in the 'Mask Name' column of the input dataframe.

    :param opt_data_df: pandas.DataFrame
        The input dataframe that contains the data to be updated. It must have a column named 'Mask Name'.

    :return: pandas.DataFrame
        The updated dataframe with the 'insert' column filled with the corresponding values from the lookup table.
    """
"""
    if 'insert' not in opt_data_df.columns:
        opt_data_df['insert'] = None
    temp_df = pd.read_excel('src/lutpy/resources/cirs062m.xlsx', sheet_name='inserts')

    # Create a dictionary for fast lookup from temp_df
    lookup_dict = pd.Series(temp_df['insert'].values, index=temp_df['Mask Name']).to_dict()

    opt_data_df['insert'] = opt_data_df['Mask Name'].map(lookup_dict)

    return opt_data_df"""

def get_insert_names(opt_data_df) -> pd.DataFrame:
    # Case 1: already processed → do nothing
    if 'insert' in opt_data_df.columns and opt_data_df['insert'].notna().all():
        return opt_data_df

    # Case 2: raw data → map from Mask Name
    if 'Mask Name' not in opt_data_df.columns:
        raise ValueError("No 'Mask Name' column and no valid 'insert' column found")

    #temp_df = pd.read_excel('src/lutpy/resources/cirs062m.xlsx', sheet_name='inserts')
    temp_df = pd.read_excel('src/lutpy/resources/nelly_constants_output.xlsx', sheet_name='inserts')


    lookup_dict = pd.Series(
        temp_df['insert'].values,
        index=temp_df['Mask Name']
    ).to_dict()

    opt_data_df['insert'] = opt_data_df['Mask Name'].map(lookup_dict)

    return opt_data_df

def create_kev_column(opt_data_df):
    """
    Adds a 'kev' column to the DataFrame by extracting the substring preceding 'keV'
    from the 'Image Name' column.

    This function checks if a column named 'kev' exists in the DataFrame. If it does not
    exist, it creates the 'kev' column by extracting the substring immediately preceding
    the substring 'keV' from the 'Image Name' column, which is assumed to contain multiple
    substrings separated by spaces.

    Parameters:
    df (pd.DataFrame): The input DataFrame that must contain a column named 'Image Name'.

    Returns:
    pd.DataFrame: The DataFrame with the added 'kev' column, if it was not already present.
    """

    if "kev" not in opt_data_df.columns:
        # function to extract the desired substring from "Image Name"
        def extract_kev(image_name):
            # split the string by spaces
            parts = image_name.split()
            # iterate over the parts and find the one that is "keV"
            for i in range(len(parts)):
                if parts[i] == 'keV':
                    # return the preceding substring if it exists
                    return parts[i-1] if i > 0 else None
                # return None if no part is "keV"
            return None
        # Apply the function to the "image Name" column to create the "kev" column
        opt_data_df["kev"] = opt_data_df["Image Name"].apply(extract_kev)
        opt_data_df["kev"] = opt_data_df["kev"].astype('int64')
    return opt_data_df

def rename_mean_column(opt_data_df: pd.DataFrame) -> pd.DataFrame:
    """
    This function checks if there is a column named 'Mean' in the given DataFrame and renames it to 'mean_hu'.

    :param opt_data_df: pandas.DataFrame
        The input DataFrame that may contain a column named 'Mean'.

    :return: pandas.DataFrame
        The DataFrame with the 'Mean' column renamed to 'mean_hu', if it exists.
    """
    if 'Mean' in opt_data_df.columns:
        opt_data_df.rename(columns={'Mean': 'mean_hu'}, inplace=True)
    return opt_data_df


def get_ground_truth_data(opt_data_df):
    """
    This function returns a DataFrame with ground truth data merged with the input DataFrame.
    """
    # Read "linear attenuation for water"-data into a pandas DataFrame
    df_h2o_att = pd.read_excel("src/lutpy/resources/nist_mass_attenuation_h2o.xlsx", sheet_name="Blad2")

    # Merge with opt_data_df on the "kev"-column and calculate linear attenuation coefficients
    opt_data_df = pd.merge(opt_data_df, df_h2o_att, how="left")
    opt_data_df[con.MU] = (opt_data_df[con.MEAN_HU] / 1000 + 1) * opt_data_df[con.MU_H2O]

    # Read ground truth EAN, ED and SPR for the optimization data
    df_ed_ean_spr = pd.read_excel(con.PHANTOM_REFERENCE_SHEET_FILE_PATH)
    opt_data_df = pd.merge(opt_data_df, df_ed_ean_spr, how="left")

    return opt_data_df


def create_kev_permutations(opt_data_df):
    """
    Returns a DataFrame with keV permutations merged with the input DataFrame.
    """
    kev_permutations_df = generate_kev_permutations(opt_data_df)
    opt_data_df_formatted = merge_kev_permutations_with_data(opt_data_df, kev_permutations_df)
    opt_data_df_formatted = sort_and_reset_index(opt_data_df_formatted)
    opt_data_df_formatted = reorder_columns(opt_data_df_formatted)

    return opt_data_df_formatted

def generate_kev_permutations(opt_data_df):
    """
    Generates DataFrame with all possible permutations of keV values.
    """
    # Extract unique keV values from the DataFrame
    kev_values = opt_data_df[con.KEV].unique()
    # Generate all possible combinations of keV values
    kev_permutations = itertools.combinations(kev_values, 2)
    # Create a DataFrame with keV permutations
    df_keV = pd.DataFrame(kev_permutations, columns=[con.KEV_LOW, con.KEV_HIGH])
    return df_keV

def merge_kev_permutations_with_data_old(opt_data_df, kev_permutations_df):
    """
      Merges DataFrame of keV permutations with opt_data_df for both low and high keV values.

      Parameters:
          opt_data_df (DataFrame): DataFrame containing the data to merge.
          kev_permutations_df (DataFrame): DataFrame containing keV permutations.

      Returns:
          DataFrame: Merged DataFrame containing the keV permutations and corresponding data.
      """
    # Merge on 'kev_low' column
    merged_df_low = pd.merge(kev_permutations_df, opt_data_df, how="left", left_on=con.KEV_LOW, right_on=con.KEV)
    merged_df_low = merged_df_low.rename(columns={con.MEAN_HU: con.HU_LOW, con.MU: con.MU_LOW})

    # Prepare opt_data_df for high values
    opt_data_df_high = opt_data_df.rename(columns={con.KEV: con.KEV_HIGH, con.MEAN_HU: con.HU_HIGH, con.MU: con.MU_HIGH})
    opt_data_df_high = opt_data_df_high.loc[:, [con.MASK_NAME, con.HU_HIGH, con.KEV_HIGH, con.MU_HIGH]]

    # Merge on 'kev_high' column
    merged_df = pd.merge(merged_df_low, opt_data_df_high, how="left", on=[con.KEV_HIGH, con.MASK_NAME])
    return merged_df

def merge_kev_permutations_with_data(opt_data_df, kev_permutations_df):
    # Merge low-energy data
    merged_df_low = pd.merge(
        kev_permutations_df,
        opt_data_df,
        how="left",
        left_on=con.KEV_LOW,
        right_on=con.KEV
    )
    merged_df_low = merged_df_low.rename(columns={
        con.MEAN_HU: con.HU_LOW,
        con.MU: con.MU_LOW
    })

    # Prepare high-energy data
    opt_data_df_high = opt_data_df.rename(columns={
        con.KEV: con.KEV_HIGH,
        con.MEAN_HU: con.HU_HIGH,
        con.MU: con.MU_HIGH
    })
    opt_data_df_high = opt_data_df_high.loc[:, [con.INSERT, con.HU_HIGH, con.KEV_HIGH, con.MU_HIGH]]

    # Merge low + high on energy pair and insert name
    merged_df = pd.merge(
        merged_df_low,
        opt_data_df_high,
        how="left",
        on=[con.KEV_HIGH, con.INSERT]
    )

    return merged_df

def sort_and_reset_index(df):
    """
    Sorts DataFrame by keV_low and keV_high and resets index.
    """
    df = df.sort_values([con.KEV_LOW, con.KEV_HIGH])
    df = df.reset_index(drop=True)
    return df

def reorder_columns(df):
    """
    Reorders DataFrame columns.
    """
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
    df = df.reindex(columns=column_names)
    return df



