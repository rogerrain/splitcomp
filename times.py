def getTime():
    time = input("Please enter a time in the format 'hh:mm:ss.mis': ")
    mss = time.split(".")
    ss = mss[0].split(":")
    if len(mss) > 1:
        ss.append(mss[1])
    return ss

def toMS(time):
    assert len(time) <= 4
    time.reverse() #Lining up the time segments with the conversion order
    conversions = [1, 1000, 60000, 3600000]
    ms = 0
    for i in range(0, len(time)):
        ms += int(time[i])*conversions[i]
    return ms

def fromMS(ms):
    conversions = [3600000, 60000, 1000, 1]
    t = []
    for i in range(0, len(conversions)):
        current = ms // conversions[i]
        ms -= current * conversions[i]
        t.append(current)
    timeString = "{}:{}:{}.{}".format(t[0], t[1], t[2], t[3])
    return timeString

def main():
    timeList = getTime()
    for time in timeList:
        print(time)
    ms = toMS(timeList)
    print(ms)
    timeList2 = getTime()
    for time in timeList2:
        print(time)
    ms2 = toMS(timeList2)
    print(ms2)
    total = abs(ms - ms2)
    print(total)
    time = fromMS(total)
    print(time)

if __name__ == "__main__":
    main()
