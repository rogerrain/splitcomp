from contracts import contract

@contract(s = "str", returns = "list[4]")
def sToTime(s):
    """Takes a time string hh:mm:ss.mis and returns a corresponding list
        [hh, mm, ss, mis] with integer values"""
    timelist = []
    split1 = s.split(".")
    split2 = split1[0].split(":")
    timelist.append(int(split2[0]))
    timelist.append(int(split2[1]))
    timelist.append(int(split2[2]))
    timelist.append(fromTD(split1[1]))
    return timelist

@contract(oldtime = "list[4]", returns = "int")
def toMS(oldtime):
    time = oldtime.copy()
    time.reverse() #Lining up the time segments with the conversion order
    conversions = [1, 1000, 60000, 3600000]
    ms = 0
    for i in range(0, len(time)):
        ms += int(time[i])*conversions[i]
    return ms

@contract(ms = "int", returns = "str[12]")
def fromMS(ms):
    conversions = [3600000, 60000, 1000, 1]
    t = []
    for i in range(0, len(conversions)):
        current = ms // conversions[i]
        ms -= current * conversions[i]
        t.append(current)
    timeString = "{}:{}:{}.{}".format(toDD(t[0]), toDD(t[1]), \
                                      toDD(t[2]), toTD(t[3]))
    return timeString

@contract(n = "int, >= 0, <100", returns = "str[<=2]")
def toDD(n):
    """Takes an integer and returns a string of length 2 corresponding to it"""
    if n // 10 > 0:
        return str(n)
    else:
        return "0" + str(n)

@contract(n = "int, >=0, <1000", returns = "str[<=3]")
def toTD(n):
    """Takes an integer and returns a string of length 3 corresponding to it"""
    if n // 100 > 0:
        return str(n)
    elif n // 10 > 0:
        return "0" + str(n)
    else:
        return "00" + str(n)

@contract(s = "str", returns = "int, <1000, >= 0")
def fromTD(s):
    """Takes a string of any number of digits and returns a positive number <
        1000"""
    temp = int(s)
    if len(s) >= 3:
        return int(s[0:3])
    elif temp // 10 > 0:
        if s[0] == "0":
            return temp
        else:
            return temp * 10
    else:
        if s[0] != "0" or temp == 0:
            return temp * 100
        elif s[1] != "0":
            return temp * 10

@contract(s = "str[n], n > 0", returns = "int, <100")
def fromDD(s):
    """Takes a string of 2 digits and returns a number with up to 2 digits"""
    if len(s) <= 2:
        return int(s)
    else:
        return int(s[0:2])
