from src.lutpy.run import ge
from src.lutpy.run import siemens
from src.lutpy.test.ge_test import ge_test
from src.lutpy.test.siemens_test import siemens_test




def main():
    ##################################
    # GE
    #################################

    # GE SPR maps #
    # Choose whether to create SPR maps for the both phantoms, one phantom, or a specific dose level on one phantom

    '''
    # ge.ge_both_phantoms()
    # ge.ge_one_phantom()


    ge.ge_specific(
        dose="10 mGy",
        kernel_and_recon="Standard Asir 40",
        study_UID="1.2.826.0.1.3680043.8.971.23977955880321717476897101177049934397"
    )


    ge.ge_specific_dose_and_kernel(dose="10 mGy", kernel_and_noise_red="Soft Asir 0")

    # ge.ge_one_phantom_and_dose()

    # GE SPR map test
    # Test the SPR map creation using a test set of VMIs in the project input folder
    '''
    ge_test()
    # ge.ge_ptcog()

    ##################################
    # Siemens
    #################################
    # run these scripts first to properly sort the siemens images.
    # root_dir = r"C:\Users\torbj\OneDrive\Desktop\Arbete 2 - mätningar\505 - Skarpt läge 2022-05\1 Bilder\Siemens mono"
    # sort_siemens(root_dir)

    # siemens_test()

    # siemens.siemens_both_phantoms()

    print("The END")
    return


if __name__ == "__main__":
    main()
