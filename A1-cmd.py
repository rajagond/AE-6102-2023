import argparse

# Create the parser
parser = argparse.ArgumentParser(prog="cmd", description="AE6102-A1")


# function to perform the operation
def perform_operation(action, arg1, arg2):
    if action == "add":
        return arg1 + arg2
    elif action == "mul":
        return arg1 * arg2
    elif action == "sub":
        return arg1 - arg2
    elif action == "exp":
        return arg1**arg2
    else:
        raise ValueError("Invalid action: {}".format(action))


# function to print the output
def print_output(args):
    result = perform_operation(args.action, args.arg1, args.arg2)
    if not args.quiet:
        print(result)
    if args.output:
        with open(args.output, "w") as f:
            f.write(str(result) + '\n')


# main function
if __name__ == "__main__":
    # Add the arguments
    arg1 = "first argument (default: 5.0)"
    parser.add_argument("-a", "--arg1", type=float, default=5.0, help=arg1)
    arg2 = "second argument (default: 2.0)"
    parser.add_argument("-b", "--arg2", type=float, default=2.0, help=arg2)
    act = "operation to perform on arguments (default: add)"
    choices = ["add", "mul", "sub", "exp"]
    parser.add_argument("--action", choices=choices, default="add", help=act)
    out = "output filename"
    parser.add_argument("-o", "--output", help=out, required=False)
    quite = "suppress output"
    parser.add_argument("-q", "--quiet", action="store_true", help=quite)

    # Parse the arguments
    args = parser.parse_args()

    # Call the function to perform the operation
    print_output(args)
