from contracts import contract
from times import toMS, fromMS, sToTime, toTD, fromTD, toDD, fromDD
from files import saveSplits, loadSplits, durations

@contract(returns = "int")
def getNum():
    """ Takes an integer input from the user and returns it."""
    while True:
        try:
            n = int(input("Enter the number of splits: "))
            if n > 0:
                return n
            else:
                print("Number must be a positive integer.")
        except:
            print("You must have a whole number of splits.")

@contract(n = "int, >0", returns = "list[n]")
def getTime(n):
    """Gets n split times in order from the user"""
    current = 1
    splits = []
    while current < n + 1:
        try:
            outtime = ""
            intime = input("Enter time for split {a}: ".format(a=current))
            mss = intime.split(".")
            ss = mss[0].split(":")
            ls = len(ss)
            if ls > 3:
                print("Only intervals up to hours are accepted. \
Time must be input in format 'hh:mm:ss.mis' (hours, \
minutes, and milliseconds may be omitted)")
            else:
                if len(mss) > 1:
                    ms = toTD(fromTD(mss[1]))
                else:
                    ms = "000"
                if ss[-1] == "": #Checking if seconds were given
                    print("Please specify the seconds.")
                else:
                    for i in range(3, 1, -1):
                        if ls < i:
                            outtime += "00:"
                    for i in range(len(ss)):
                        outtime += toDD(fromDD(ss[i]))
                        if i < len(ss)-1:
                            outtime += ":"
                        else:
                            outtime += "."
                    outtime += ms
                    print(outtime)
                    if current > 1: #Checking that splits are in order
                        if toMS(sToTime(outtime)) > \
                        toMS(sToTime(splits[current-2])):
                            splits.append(outtime)
                            print(splits)
                            current += 1
                        else:
                            print("Your time for split {b} cannot be before \
your time for split {a}.".format(b=current, a=current-1))
                    else:
                        splits.append(outtime)
                        print(splits)
                        current += 1
        except:
            print("Time must be input in format 'hh:mm:ss.mis' (hours, \
minutes, and milliseconds may be omitted)")
    return splits

@contract(returns = "tuple")
def enterSplits():
    numSplits = getNum()
    name1 = getNewName(1)
    print("~~~~Inputting times for {}~~~~".format(name1))
    sp1 = getTime(numSplits)
    name2 = getNewName(2)
    print("~~~~Inputting times for {}~~~~".format(name2))
    sp2 = getTime(numSplits)
    saveSplits(name1, sp1)
    saveSplits(name2, sp2)
    return name1, name2

@contract(i = "int, >0", returns = "str")
def getNewName(i):
    name = input("Enter the name for runner {}'s splits: ".format(i))
    return name

@contract(i = "int, >0", returns = "tuple")
def getExistingName(i):
    print("~~File number {}~~".format(i))
    while True:
        try:
            name = input("Enter the name of the file to read from (txt): ")
            splits, durs = loadSplits(name)
            if splits == []:
                print("File is not properly formatted.")
            else:
                return splits, durs
        except:
            print("Invalid file name given. Please ensure that the file name \
you enter exists in this directory.")

@contract(returns = "str")
def getChoice():
    valid = ["q", "l", "n", "s", "new", "save", "load", "quit"]
    while True:
        choice = input("Would you like to load splits or enter new ones? " )
        c = choice.lower()
        if c in valid:
            return c
        else:
            print("Invalid input. Please enter quit, new, save, or load.")

@contract(returns = "str")
def getSecondChoice():
    valid = ["losses", "l", "all", "saves", "s", "1", "2", "3", "q", "quit", \
             "4"]
    while True:
        choice = input("Which comparison would you like to see? \n\
1. All Splits (all) \n2. The splits with the biggest time saves (you can \
choose how many to view) (s) \n3. The splits with the biggest time \
losses (you can choose how many to view) (l)\n4. Quit (q)\n")
        c = choice.lower()
        if c in valid:
            return c
        else:
            print("Invalid input. Please enter either big, all, small, 1, 2, \
or 3.")

@contract(message = "str", returns = "int, >0")
def getN(message):
    while True:
        try:
            n = int(input("How many of the biggest time {} would you like to \
see? ".format(message)))
            if n > 0:
                return n
            else:
                print("Must input a positive integer.")
        except:
            print("Invalid input. Please input a positive integer.")

@contract(comptups = "list")
def showComps(comptups):
    print("Split # \tTime Difference (+ means slower, - means faster)")
    for tup in comptups:
        i = tup[1]
        ms = tup[0]
        if ms < 0:
            m = "-" + fromMS(abs(ms))
        else:
            m = "+" + fromMS(ms)
        print("Split {a}:\t{b}".format(a = i, b = m))

def main():
    print("~" * 12 + "Welcome to SplitsComp!" + "~" * 12)
    choice = ""
    while choice != "q":
        choice = getChoice() #Either load splits or make new ones
        if choice in ["q", "quit"]:
            choice = "q"
            break
        elif choice in ["n", "s", "new", "save"]:
            name1, name2 = enterSplits()
            splits1, durs1 = loadSplits(name1)
            splits2, durs2 = loadSplits(name2)
        elif choice in ["l", "load"]:
            splits1, durs1 = getExistingName(1)
            splits2, durs2 = getExistingName(2)
        #COMPARE TIME
        if len(durs2) != len(durs1):
            print("Files given do not have the same number of splits.")
        else:
            comps = [durs1[i] - durs2[i] for i in range(len(durs2))]
            compTuples = [(comps[i], i+1) for i in range(len(comps))]
            while True:
                ct = compTuples.copy()
                choice = getSecondChoice()
                if choice in ["q", "quit", "4"]:
                    choice = "q"
                    break
                elif choice in ["1", "all"]:
                    showComps(ct)
                elif choice in ["2", "l", "losses"]:
                    n = getN("losses")
                    n = min([n, len(comps)])
                    ct.sort()
                    ct.reverse() #Getting the BIGGEST n differences
                    use = ct[:n]
                    showComps(use)
                elif choice in ["3", "s", "saves"]:
                    n = getN("saves")
                    n = min([n, len(comps)])
                    ct.sort()
                    use = ct[:n]
                    showComps(use)
    print("Thank you for using SplitsComp! Goodbye!")

if __name__ == "__main__":
    main()
