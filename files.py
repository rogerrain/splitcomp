from contracts import contract
from times import fromMS, toMS, sToTime

@contract(name = "str", splits = "list")
def saveSplits(name, splits):
    """Saves splits to a txt file for later"""
    durationz = durations(splits)
    durs = [fromMS(d) for d in durationz]
    if not name.endswith(".txt"):
        name += ".txt"
    outfile = open(name, "w")
    outfile.write("#\tSplit Time\tDuration\n" + "-"*36 + "\n")
    for i in range(len(splits)):
        outfile.write("{a}.\t{b}\t{c}\n".format(a = i+1, b = splits[i], \
                                              c = durs[i]))
    outfile.close()

@contract(name = "str", returns = "tuple")
def loadSplits(name):
    """Loads splits from a txt file in the same format as demonstrated in the
        saveSplits function"""
    if not name.endswith(".txt"):
        name += ".txt"
    infile = open(name, "r")
    lines = infile.readlines()
    infile.close()
    if len(lines) < 3:
        print("No splits were found in the given file. Please note the format \
for the split files in the default ones (if the default files are gone, save \
new splits and note the format they are written in).")
        return [], [0]
    lines = lines[2:]
    splits = []
    for line in lines:
        parts = line.split("\t")
        splits.append(parts[1])
    durs = durations(splits)
    for dur in durs:
        if dur < 0:
            print("Splits in the given file are not in order.")
            return [], [0]
    return splits, durs

@contract(splits = "list", returns = "list")
def durations(splits):
    """Given a list of splits, returns a list of the durations of each split"""
    d = []
    prev = 0
    for i in range(len(splits)):
        current = toMS(sToTime(splits[i]))
        d.append(current - prev)
        prev = current
    return d
