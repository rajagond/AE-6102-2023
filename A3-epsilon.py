import numpy as np


# epsilon function
def print_epsilon():
    print("{},{}".format(np.finfo(float).eps, np.finfo(np.float32).eps))


# main function
if __name__ == "__main__":
    print_epsilon()
