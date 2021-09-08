# Set of colors that can be used for printing on Terminal
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


# Class that defines getting the parameters
class Params:

    # Initialiser takes in a parameter on whether to use defaults at all
    def __init__(self, *args):
        args = args[0]

        # Print out a name of the script
        print("------------------------------")
        print(args[0][:-3].upper() + " PARAMETERS")
        print("------------------------------")

        # Set any default values
        self.use_defaults = False

        # Look for arguments
        for arg in args:
            if arg == "-defaults":
                self.use_defaults = True
        


    # Asks the user for a value and performs some checking on the input
    def ask (self, name, default, values=[]):

        # Check for using default values
        if self.use_defaults:
            val = ""

        # Ask the user for a value
        else:
            val = input("\nEnter a value for %s%s%s [default = %s%s%s]: " % \
                (col.OKGREEN, name, col.ENDC, col.OKCYAN, str(default), col.ENDC))

        # Determine the output based on type
        if val == "":
            output = default
        elif val.lower() in ("true", "false"):
            output = val.lower() == "true"
        elif type(default) is int:
            output = int(val)
        elif type(default) is float:
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
        print("Selected %s%s%s for %s%s%s." % (col.OKCYAN, output, col.ENDC, col.OKGREEN, name, col.ENDC))

        # Return the parameter
        return output