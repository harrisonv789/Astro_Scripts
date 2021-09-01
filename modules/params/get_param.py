class col:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# Asks the user for a value and performs some checking on the input
def ask (name, default, values=[]):
    
    # Ask the user for a value
    val = input("\nEnter a value for %s%s%s [default = %s%s%s]: " % \
        (col.OKGREEN, name, col.ENDC, col.OKCYAN, str(default), col.ENDC))

    # Determine the output based on type
    if val == "":
        output = default
    elif val.lower() in ("true", "false"):
        output = val.lower() == "true"
    elif type(default) is type(int):
        output = int(val)
    elif type(default) is type(float):
        output = float(val)
    else:
        output = val

    # Make sure value in values
    if len(values) > 0 and val != "":
        # If invalid value, then use the default
        if output not in values:
            print("Invalid input. Possible values are %s%s%s." % (col.OKCYAN, values, col.ENDC))
            output = default

    # Print the selected value
    print("Selected %s%s%s." % (col.OKCYAN, output, col.ENDC))

    # Return the parameter
    return output