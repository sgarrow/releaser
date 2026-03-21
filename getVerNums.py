from pathlib   import Path
#############################################################################

def getVerNums( fName, numChangedPy, numTrackedPy ):

    curVStr   = None
    newVStrwV = None

    try:
        pcntChange = int((numChangedPy/numTrackedPy) * 100.0)
    except ZeroDivisionError:
        return curVStr, -1, newVStrwV

    fileWithVerNum = Path( fName )

    try:
        txt = fileWithVerNum.read_text(encoding='utf-8').split('\n')
    except (FileNotFoundError, IsADirectoryError):
        return curVStr, -2, newVStrwV

    verFound = False
    for line in txt:
        if 'VER =' in line:
            curVStr     = \
            line.split('=')[1].split('-')[0].replace('\'','').strip() #v1.6.4
            curVLstwV   = [ x.strip() for x in curVStr.split('.') ]
            curVLstwoV  = [curVLstwV[0][1:]] + curVLstwV[1:]
            curVIntLst  = [int(x) for x in curVLstwoV]
            verFound    = True
            break

    if not verFound:
        return curVStr, -3, newVStrwV

    newVIntLst = curVIntLst[:]

    if numTrackedPy > 4:
        if pcntChange > 66:
            newVIntLst[0] = newVIntLst[0]+1
            newVIntLst[1] = 0
            newVIntLst[2] = 0
        elif pcntChange > 33:
            newVIntLst[1] = newVIntLst[1]+1
            newVIntLst[2] = 0
        else:
            newVIntLst[2] = newVIntLst[2]+1
    else:
        newVIntLst[2] = newVIntLst[2]+1
        if newVIntLst[2] > 9:
            newVIntLst[2] = 0
            newVIntLst[1] = newVIntLst[1]+1
            if newVIntLst[1] > 9:
                newVIntLst[1] = 0
                newVIntLst[0] = newVIntLst[0]+1

    newVStrLst = [ str(x) for x in newVIntLst ]
    newVStr    = '.'.join(newVStrLst)
    newVStrwV = 'v' + newVStr

    return curVStr, pcntChange, newVStrwV
#############################################################################
