import os
import time
import datetime

from src.lutpy.optimization.read_opt_input_data import get_opt_data
from src.lutpy.optimization.get_spr_optimization import get_spr_optimization
from src.lutpy.optimization.write_opt_results import write_result
from src.lutpy.time.get_time import get_time


def main():
    """
    This script reads unformatted excel files exported from mice and performs an optimization of the Näsmark Andersson
    -method for mapping stopping power. If the excel files contain data from more than one acquisition, the script will
    run the optimization and output the results in an Excel document for each acquisition.

    The script expects both Siemens and GE data, for both Head and Body, and VMIs in the range 40-101 keV.
    :return: Excel-document
    """

    start = time.time()
    print("Go!\n")

    input_dir = r'C:\Users\Nelly Kleppe\PycharmProjects\exjobb\calibration\lutpy_main\input\mice export'

    #for filename in os.listdir(input_dir):
    #if filename.endswith('xlsx'):
    # den bryr sig inte om filen här, utan den som är i constants?
    filename = 'nelly_full2.xlsx'
    #filename = "input_testkarin.xlsx"
    file_path = os.path.join(input_dir, filename)
    opt_data_df = get_opt_data(file_path)

    m, s = get_time(start)
    print("Importing and formatting optimization_data took", m, "minutes and ", s, "seconds to run",)

    # Calculate EAN, RED and SPR for every row in opt_data_df
    rmse_dict = get_spr_optimization(opt_data_df)
    m, s = get_time(start)


    current_datetime = datetime.datetime.now()
    str_date = current_datetime.strftime("%d-%m-%Y")
    output_file_name = f"Output\Optimal_energy\Optimal energy {os.path.splitext(filename)[0]} ({str_date}).xlsx"
    write_result(rmse_dict, start, output_file_name)

    m, s = get_time(start)
    print(f"The script finished running for {filename} at", m, "minutes and", s, "seconds")
    print("All files processed")
    return


if __name__ == "__main__":

    main()
