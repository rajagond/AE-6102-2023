import numpy as np
import argparse

# compare two npz files
def compare_npz(file1, file2):
    with np.load(file1) as data1:
        with np.load(file2) as data2:
            if np.all(data1['arr_0'] == data2['arr_0']):
                return True
            for key in data1.files:
                if not np.allclose(data1[key], data2[key]):
                    return False
    return False

if __name__ == "__main__":
    # Create the parser
    parser = argparse.ArgumentParser(prog="program_verifier", description="AE6102-A4")
    # Add the arguments
    parser.add_argument("--input-file1", type=str, help="Input file 1")
    parser.add_argument("--input-file2", type=str, help="Input file 2")

    # Parse the arguments
    args = parser.parse_args()

    # Compare the two files
    if compare_npz(args.input_file1, args.input_file2):
        print("Files are identical")
    else:
        print("Files are different")