from contracts import contract
from times import toMS, fromMS, sToTime, toTD, fromTD, toDD

@contract(returns = "int")
def getNum():
    """ Takes an integer input from the user and returns it."""
    while True:
        try:
            n = int(input("Enter the number of splits: "))
            break
        except:
            print("You must have a whole number of splits.")
    return n

@contract(s = "str[n], n > 0", returns = "int, <100")
def fromDD(s):
    """Takes a string of 2 digits and returns a number with up to 2 digits"""
    if len(s) <= 2:
        return int(s)
    else:
        return int(s[0:2])

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
    
def durations(splits):
    """Given a list of splits, returns a list of the durations of each split"""
    d = []
    prev = 0
    for i in range(len(splits)):
        current = toMS(sToTime(splits[i]))
        d.append(current - prev)
        prev = current
    return d

def main():
    numSplits = getNum()
    print("~~~~Inputting times for runner 1's splits~~~~")
    sp1 = getTime(numSplits)
    print("~~~~Inputting times for runner 2's splits~~~~")
    sp2 = getTime(numSplits)
    d1 = durations(sp1)
    d2 = durations(sp2)
    for dur in d1:
        print("- " + fromMS(dur))
    for dur in d2:
        print("~ " + fromMS(dur))

if __name__ == "__main__":
    main()
