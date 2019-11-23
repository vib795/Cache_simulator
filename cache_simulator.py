import sys, math, time

simulator = []
cacheLines = 0
numSets = 0
linesPerSet = 0
hitCount = 0
missCount = 0

def cacheCreate(cacheSize, cacheLineSize, ways):
    lineCount = 0
    setNum = 0
    waysNum = 0

    global cacheLines
    global numSets
    global linesPerSet

    cacheLines = cacheSize//cacheLineSize
    numSets = cacheLines//ways
    linesPerSet = cacheLines//numSets

    for i in range(cacheLines):
        simulator.append([0,0,0,0,0,-1])

    for i in range(cacheLines):
        if (lineCount == linesPerSet):
            lineCount = 0
            setNum = setNum + 1
            waysNum = 0
        simulator[i][0] = setNum
        simulator[i][1] = waysNum
        simulator[i][2] = "-1"
        simulator[i][4] = "-1"
        lineCount = lineCount + 1
        waysNum = waysNum + 1

if (len(sys.argv) < 4):
    print("Correct usage: sh run_sim.sh [traceFile] [cacheSizeBytes] [cacheLineSizeBytes] [numberOfWays]")
    sys.exit()

cacheSize = int(sys.argv[2])
cacheLineSize = int(sys.argv[3])
ways = int(sys.argv[4])

cacheCreate(cacheSize, cacheLineSize, ways)

file = open(sys.argv[1], "r")
while True:
    readLine = file.readline()
    if readLine == "" or readLine == "#eof":
        break
    
    accessFields = readLine.split()
    if (len(accessFields) != 3):
        continue

    hitCount = hitCount + 1
    addr = int(accessFields[2], 16)
    memOffet = addr & (cacheLineSize - 1)
    memSetIndex = addr >> int(math.log(cacheLineSize, 2)) & (numSets - 1)
    memTag = addr >> (int(math.log(numSets, 2)) + int(math.log(cacheLineSize, 2)))

    hitFlag = 0
    fullSetCounter = 0;
    if(accessFields[1] == "R"):
        startingRow = linesPerSet * int(memSetIndex)
        for i in range(startingRow, startingRow + linesPerSet):
            if (simulator[i][2] == memTag):
                hitFlag = 1
                simulator[i][5] = time.time()
                break

        fullFlag = 1
        oldestTime = 1000000000000000000000000  #use a large time value by default for LRU comparison
        oldestRow = -1

        if (hitFlag == 0):
            missCount = missCount + 1
            for i in range(startingRow, startingRow + linesPerSet):
                if (simulator[i][3] == 0):
                    fullFlag = 0
                    break
                if (simulator[i][5] < oldestTime):
                    oldestTime = simulator[i][5]
                    oldestRow = i
            if (fullFlag == 0):
                simulator[i][2] = memTag
                simulator[i][4] = "data"
                simulator[i][3] = 1
                simulator[i][5] = time.time()
            else:
                simulator[oldestRow][2] = memTag
                simulator[oldestRow][4] = "data"
                simulator[oldestRow][3] = 1
                simulator[oldestRow][5] = time.time()
	
    elif(accessFields[1] == "W"):
        startingRow = linesPerSet * int(memSetIndex)
        for i in range(startingRow, startingRow + linesPerSet):
            if (simulator[i][2] == memTag):
                simulator[i][2] = memTag
                simulator[i][4] = "dataUpdated"
                simulator[i][3] = 1
                simulator[i][5] = time.time()
                hitFlag = 1
                break

        fullFlag = 1
        oldestTime = 1000000000000000000000000
        oldestRow = -1

        if (hitFlag == 0):
            missCount = missCount + 1
            for i in range(startingRow, startingRow + linesPerSet):
                if (simulator[i][3] == 0):
                    fullFlag = 0
                    break
                if (simulator[i][5] < oldestTime):
                    oldestTime = simulator[i][5]
                    oldestRow = i
            if (fullFlag == 0):
                simulator[i][2] = memTag
                simulator[i][4] = "data"
                simulator[i][3] = 1
                simulator[i][5] = time.time()
            else:
                simulator[oldestRow][2] = memTag
                simulator[oldestRow][4] = "data"
                simulator[oldestRow][3] = 1
                simulator[oldestRow][5] = time.time()
missRate = (missCount/hitCount) * 100
print ("Cache miss rate: {:0.2f}%".format(missRate, 3))
