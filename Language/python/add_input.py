import getopt
import sys

#Get user input and run related function
def Usage():
    """
       echo "Usage: Input_list [options]"
       echo "Available options:"
       echo "  -d      download a repo"
       echo "  -h      help message"
       echo "  -b      build repo"
    """

def Get_option():
    try:
        options, args = getopt.getopt(sys.argv[1:], "d:hb", ["download", "help", "build"])
        if len(options):
            for option, value in options:
                if option in ("-d", "--download"):
                    if (value == "abc") or (value == "Abc"):
                        # Add a function to download abc repo
                        print "Add a function to download abc repo"
                    elif (value == "def") or (value == "Def"):
                        # Add a function to download def repo
                        print "Add a function to download def repo"
                    else:
                        print "Please input a valid repo name"
                elif option in ("-h", "--help"):
                     # print usage list
                     print Usage.__doc__
                elif option in ("-b", "--build"):
                    # Add a function to build repo
                    print "Add a function to build repo"
                else:
                    print "Wrong input"
                    sys.exit()
        else:
            print Usage.__doc__
    except getopt.GetoptError as err:
        print str(err)
        print Usage.__doc__
        sys.exit(1)
if __name__=='__main__':
    Get_option()
