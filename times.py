def getTime():
    time = input("Please enter a time in the format 'hh:mm:ss.mis': ")
    mss = time.split(".")
    ss = mss[0].split(":")
    if len(mss) > 1:
        ss.append(mss[1])
    return ss

def toMS(time):
    assert len(time) <= 5
    conversions = [1, 1000, 60000, 3600000, 86400000]
    ms = 0
    for i in range(0, len(time)):
        ms += time[i]*conversions[i]
    return ms

def main():
    timeList = getTime()
    for time in timeList:
        print(time)

'''
if __name__ == "__main__":
    main()
'''
