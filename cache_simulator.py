import sys
import math 
import time

sim = []
linesInCache = 0
numSlots = 0
linesPerSlot = 0
hit = 0
miss = 0

#Cache creation method
def cacheCreate(sizeOfCache, lineSize, Mways):
    lC = 0
    slotNum = 0
    ways = 0

    global numSlots
    global linesPerSlot
    global linesInCache
    
    #set total number of lines in cache
    linesInCache = sizeOfCache//lineSize

    #set number of slots
    numSlots = linesInCache//Mways

    #set number of lines per slot
    linesPerSlot = linesInCache//numSlots

    for i in range(linesInCache):
        sim.append([0,0,0,0,0,-1])

    for i in range(linesInCache):
        if (lC == linesPerSlot):
            lC = 0
            slotNum = slotNum + 1
            ways = 0
        sim[i][0] = slotNum
        sim[i][1] = ways
        sim[i][2] = "-1"
        sim[i][4] = "-1"
        lC = lC + 1
        ways = ways + 1

#check for required number of parameters and throw error message if the input is wrong
if (len(sys.argv) < 4):
    print("Incorrect input command. Please use the following syntax to key in the commands:")
    print("\t" + "\"sh run_sim.sh <traceFile> <sizeOfCacheBytes> <lineSizeBytes> <numberOfWays>\"")
    sys.exit()

#format input to int
sizeOfCache = int(sys.argv[2])
lineSize = int(sys.argv[3])
Mways = int(sys.argv[4])

cacheCreate(sizeOfCache, lineSize, Mways)

#read file
file = open(sys.argv[1], "r")
while True:
    line = file.readline()
    if line == "" or line == "#eof":
        break
    
    fields = line.split()
    if (len(fields) != 3):
        continue

    hit = hit + 1
    addr = int(fields[2], 16)
    offset = addr & (lineSize - 1)
    setIndex = addr >> int(math.log(lineSize, 2)) & (numSlots - 1)
    tag = addr >> (int(math.log(numSlots, 2)) + int(math.log(lineSize, 2)))

    flag = 0
    fsCounter = 0;
    if(fields[1] == "R"):
        fRow = linesPerSlot * int(setIndex)
        for i in range(fRow, fRow + linesPerSlot):
            if (sim[i][2] == tag):
                flag = 1
                sim[i][5] = time.time()
                break

        fFalg = 1
        oldestTime = 100000000000000000000  #set to a high value for LRU algorithm to work 
        oldestRow = -1

        if (flag == 0):
            miss = miss + 1
            for i in range(fRow, fRow + linesPerSlot):
                if (sim[i][3] == 0):
                    fFalg = 0
                    break
                if (sim[i][5] < oldestTime):
                    oldestTime = sim[i][5]
                    oldestRow = i
            if (fFalg == 0):
                sim[i][2] = tag
                sim[i][4] = "data"
                sim[i][3] = 1
                sim[i][5] = time.time()
            else:
                sim[oldestRow][2] = tag
                sim[oldestRow][4] = "data"
                sim[oldestRow][3] = 1
                sim[oldestRow][5] = time.time()
	
    elif(fields[1] == "W"):
        fRow = linesPerSlot * int(setIndex)
        for i in range(fRow, fRow + linesPerSlot):
            if (sim[i][2] == tag):
                sim[i][2] = tag
                sim[i][4] = "dataUpdated"
                sim[i][3] = 1
                sim[i][5] = time.time()
                flag = 1
                break

        fFalg = 1
        oldestTime = 100000000000000000000
        oldestRow = -1

        if (flag == 0):
            miss = miss + 1
            for i in range(fRow, fRow + linesPerSlot):
                if (sim[i][3] == 0):
                    fFalg = 0
                    break
                if (sim[i][5] < oldestTime):
                    oldestTime = sim[i][5]
                    oldestRow = i
            if (fFalg == 0):
                sim[i][2] = tag
                sim[i][4] = "data"
                sim[i][3] = 1
                sim[i][5] = time.time()
            else:
                sim[oldestRow][2] = tag
                sim[oldestRow][4] = "data"
                sim[oldestRow][3] = 1
                sim[oldestRow][5] = time.time()
missRate = (miss/hit) * 100
print ("Cache miss rate: {:0.2f}%".format(missRate, 3))
file.close()