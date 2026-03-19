from itertools import combinations
from pathlib   import Path
import datetime   as dt
import pprint     as pp       # pylint: disable=W0611
import sys
import os
import re

import moveOrCopyFiles as mcf # pylint: disable=W0611
import asciiColorCodes as ACC
import runTerminalCmd  as rtc
import printRoutines   as pr

VER = 'v4.1.0 - 18-Mar-2026'
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

def getAllTrackedFs():
    allTrackedFiles = []
    cmdLst = [ 'git', 'ls-files' ]
    #cmdLst = [ 'git', 'ls-file' ] # shg
    err, stdOut,stdErr = rtc.runCommand(cmdLst)
    if not err:
        stdOutLines = stdOut.split('\n')
        allTrackedFiles = [line.split()[0] for line in stdOutLines]
    return err, stdOut, stdErr, allTrackedFiles
    #################################

def getChangedTrackedFs():
    changedTrackedFiles = []
    cmdLst = [ 'git', 'status', '--porcelain' ]
    #cmdLst = [ 'gi', 'status', '--porcelain' ] # shg
    err, stdOut,stdErr = rtc.runCommand(cmdLst)
    if not err:
        stdOutLines = stdOut.split('\n')
        changedTrackedFiles = \
            [line.split()[1] for line in stdOutLines if line.split()[0]=='M']
    return err, stdOut, stdErr, changedTrackedFiles
    #################################

def getUntrackedFs():
    untrackedFiles = []
    cmdLst = [ 'git', 'status', '--porcelain' ]
    err, stdOut,stdErr = rtc.runCommand(cmdLst)
    if not err:
        stdOutLines = stdOut.split('\n')
        untrackedFiles = \
            [line.split()[1] for line in stdOutLines if line.split()[0]=='??']
    return err, stdOut, stdErr, untrackedFiles
    #################################

def getExpectedUntrackedFs(projectsDict):
    err, stdOut, stdErr = True, '', ' Active Project not Found.'

    kk = ''
    for kk,v in projectsDict.items():
        if v['active']:
            err = False
            stdErr = ''
            break

    if kk == 'spiClock':
        expectedUntrackedFiles   = \
            [ 'cfg.cfg',   'cfg.py',    'client.py',   'gui.py',
              'fileIO.py', 'server.py', 'swUpdate.py', 'utils.py' ]
    elif kk == 'sprinkler2':
        expectedUntrackedFiles   = \
            [ 'cfg.cfg',   'cfg.py',    'client.py',   'gui.py',
              'fileIO.py', 'server.py', 'swUpdate.py', 'utils.py' ]
    elif kk == 'shared':
        expectedUntrackedFiles = []
    else:
        expectedUntrackedFiles = []

    return err, stdOut, stdErr, expectedUntrackedFiles
    #################################

def getUnexpectedUntrackedFs( untracked, expectedUntracked ):
    err, stdOut, stdErr = False, '', ''
    unexpectedUntrackedFiles = list(set(untracked) - set(expectedUntracked))
    if '__pycache__/' in unexpectedUntrackedFiles:
        unexpectedUntrackedFiles.remove('__pycache__/')
    return err, stdOut, stdErr, unexpectedUntrackedFiles
#############################################################################

def getFileLstDict(projectsDict):
    fDict = {
        'trackedFs'            : 
        { 'sts' : None, 'stdO':None, 'stdE':None, 'fLst':[], 'len':None,
          'func': getAllTrackedFs         },

        'changedTrackedFs'     :
        { 'sts' : None, 'stdO':None, 'stdE':None, 'fLst':[], 'len':None,
          'func': getChangedTrackedFs     },

        'untrackedFs'          :
        { 'sts' : None, 'stdO':None, 'stdE':None, 'fLst':[], 'len':None,
          'func': getUntrackedFs          },

        'expectedUntrackedFs'  :
        { 'sts' : None, 'stdO':None, 'stdE':None, 'fLst':[], 'len':None,
          'func': getExpectedUntrackedFs  },

        'unexpectedUntrackedFs':
        { 'sts' : None, 'stdO':None, 'stdE':None, 'fLst':[], 'len':None,
          'func': getUnexpectedUntrackedFs},

        'trackedPyFs'          :
        { 'sts' : None, 'stdO':None, 'stdE':None, 'fLst':[], 'len':None,
          'func': None                    },

        'changedTrackedPyFs'   :
        { 'sts' : None, 'stdO':None, 'stdE':None, 'fLst':[], 'len':None,
          'func': None                    },
    }

    for kk,v in fDict.items():
        if kk in ['unexpectedUntrackedFs','trackedPyFs','changedTrackedPyFs']:
            continue
        if kk in [ 'expectedUntrackedFs' ]:
            s,o,e,l = v['func'](projectsDict)
        else:
            s,o,e,l = v['func']()
        v['sts' ] = s
        v['stdO'] = o
        v['stdE'] = e
        v['fLst'] = l

    kk = 'unexpectedUntrackedFs'
    s,o,e,l = fDict[kk]['func'](fDict['untrackedFs'       ]['fLst'],
                              fDict['expectedUntrackedFs']['fLst'])
    fDict[kk]['sts' ] = s
    fDict[kk]['stdO'] = o
    fDict[kk]['stdE'] = e
    fDict[kk]['fLst'] = l

    fDict['trackedPyFs']['fLst']        = \
        [x for x in fDict['trackedFs'][       'fLst'] if x.endswith('.py')]
    fDict['changedTrackedPyFs']['fLst'] = \
        [x for x in fDict['changedTrackedFs']['fLst'] if x.endswith('.py')]

    for kk,v in fDict.items():
        v['len'] = len(v['fLst'])
    return fDict
#############################################################################

def lookForErrorsInFileLstDict(inFileListDict):
    rspMsg = ''
    errorsPresent = False
    for kk,v in inFileListDict.items():
        if v['sts']:
            if rspMsg == '':
                rspMsg += '\n Exiting, RE: Error(s) in fileLstDict.\n'
            rspMsg += '\n   {:23} error = {}\n'.format(kk, v['sts'])
            erMsgLines = v['stdE'].split('\n')
            for errLine in  erMsgLines:
                rspMsg += '     {}\n'.format(errLine)
            errorsPresent = True
    return errorsPresent, rspMsg
#############################################################################

def lookForDiffs( dirsToComp, fLstStr ):
    print( '\n Looking for diffs among shared files.\n' )
    print( fLstStr )

    differencesExist = False
    fLstPath = [ Path(x) for x in fLstStr ]
    combSet  = combinations(dirsToComp, 2)
    width    = 37
    slash    = '\\'

    for comb in combSet:

        combAsStr0   = str(comb[0])
        combAsStr1   = str(comb[1])

        slashIndeces0= [idx for idx,ch in enumerate(combAsStr0) if ch==slash]
        slashIndeces1= [idx for idx,ch in enumerate(combAsStr1) if ch==slash]

        comb0Root    = combAsStr0[ slashIndeces0[-1]: ]
        comb1Root    = combAsStr1[ slashIndeces1[-1]: ]

        for file in fLstPath:

            f0 =  comb[0] / file  # A Path join. All 3 vars type Path.
            f1 =  comb[1] / file  # A Path join. All 3 vars type Path.

            text0 = f0.read_text( encoding='utf-8' )
            text1 = f1.read_text( encoding='utf-8' )
            equal = text0 == text1

            pStr0 = '   {}\\{}{}'.format( comb0Root, file,
                        (width-len(comb0Root)-len(str(file))) * ' ' )

            pStr1 = '   {}\\{}'.format(   comb1Root, file )

            print(pStr0, end ='')
            if equal:
                print( '==',end = '' )
            else:
                print( '!=', end = '' )
                differencesExist = True
            print(pStr1, end ='')

            print()
        print('  ##########')
    return differencesExist
#############################################################################

def buildProjectDict():
    prjDict = {
    'spiClock':
        {'dir' :Path( r'C:\01-home\14-python\gitTrackedCode\spiClock'),
         'verNumFile':'cmdVectors.py',
         'active'    :False,
         'url'       :'https://github.com/sgarrow/spiClock.git'
        },
    'sprinkler2':
        {'dir' :Path( r'C:\01-home\14-python\gitTrackedCode\sprinkler2'),
         'verNumFile':'cmdVectors.py',
         'active'    :False,
         'url'       :'https://github.com/sgarrow/sprinkler2.git'
        },
    'shared':
        {'dir' : Path( r'C:\01-home\14-python\gitTrackedCode\sharedClientServerCode'),
         'verNumFile':'fileIO.py',
         'active'    :False,
         'url'       :'https://github.com/sgarrow/sharedClientServerCode.git'
        },
    'soduko':
        {'dir' : Path( r'C:\01-home\14-python\gitTrackedCode\soduko'),
         'verNumFile':'soduko.py',
         'active'    :False,
         'url'       :'https://github.com/sgarrow/soduko.git'
        },
    'multiCore':
        {'dir' : Path( r'C:\01-home\14-python\gitTrackedCode\multicore'),
         'verNumFile':'main.py',
         'active'    :False,
         'url'       :'https://github.com/sgarrow/multiCore.git'
        },
    'clientServer':
        {'dir' : Path( r'C:\01-home\14-python\gitTrackedCode\clientServer'),
         'verNumFile':'server.py',
         'active'    :False,
         'url'       :'https://github.com/sgarrow/clientServer.git'
        },
    'releaser':
        {'dir' : Path( r'C:\01-home\14-python\gitTrackedCode\releaser'),
         'verNumFile':'release.py',
         'active'    :False,
         'url'       :'https://github.com/sgarrow/releaser.git'
        },
    }
    return prjDict
#############################################################################
def getDsrdPrjDictKey(prjDict):

    print( '\n Which project do you want to release.' )
    keyLst = list(projDict.keys())
    for idx,k in enumerate(keyLst):
        print( '  {} - {}'.format( idx, k ) )
    
    while True:
        choice = input( '  Enter project number (or q (quit)) --> ' )
        if choice == 'q':
            return 'quit'
        try:
            choiceInt = int(choice)
        except ValueError:
            print( '  Must enter an integer' )
            continue
        else:
            if choiceInt not in range(0,len(projDict)):
                print( '  Invalid choice integer' )
                continue
        break
    return keyLst[choiceInt]
#############################################################################

if __name__ == '__main__':

    print( '\n Releaser verion: {} '.format(VER))

    ### Get Command Line Args.
    arguments  = sys.argv
    scriptName = arguments[0]
    userArgs   = arguments[1:]
    prnEn      = (len(userArgs) > 0 and '/p' in userArgs)
    #########################################

    ### Build Project Dictionary.
    projDict = buildProjectDict()
    #########################################

    ### Get Desired Project To Release.
    dsrdPrjDictKey = getDsrdPrjDictKey(projDict)
    if dsrdPrjDictKey == 'quit':
        sys.exit()
    #########################################

    ### Set "Working Variables" (from proj dict) and set cwd.
    projDict[dsrdPrjDictKey]['active'] = True
    projFileWithVerNumInIt = projDict[dsrdPrjDictKey]['verNumFile']
    projGithubUrl          = projDict[dsrdPrjDictKey]['url']
    projDir                = projDict[dsrdPrjDictKey]['dir']
    os.chdir(projDir)
    #pr.printPathInfo(projDir)
    print( '\n Releasing {}\n'.format(projDir) )
    print( ' Current working directory: {}'.format(Path.cwd() ))
    #########################################

    ### Get changed,untracked,etc files of selected project.
    print( '\n Getting changed and untracked files.' )
    fLstDict = getFileLstDict(projDict)
    pr.printFileLstDict( fLstDict, prnEn )
    #########################################

    ### Exit if problems getting changed/untracked files.
    errFound, funcRspMsg = lookForErrorsInFileLstDict( fLstDict )
    if errFound:
        print( '{}{}{}'.format( ACC.RED_BOLD, funcRspMsg, ACC.OFF ))
        sys.exit()
    #########################################

    ### Exit, if desired, if unexpected/untracked files present or 
    ### no tracked/changed files present.
    if fLstDict['unexpectedUntrackedFs']['len'] > 0:
        print( '\n unexpected/untracked files present.')
        print( '   Continuing will not add them.')
        print( '   Add from cmd line like this <git add fName>')
        goOn = input( '   Continue (y/n)? -> ' )      # <-- EXIT ?
        if goOn != 'y':
            sys.exit()

    if fLstDict['changedTrackedFs']['len'] == 0:
        print( '\n No tracked/changed files present.' )
        print( '   Continue will bump rev and thus {} will change.'.\
            format(projFileWithVerNumInIt))
        goOn = input( '   Continue (y/n)? -> ' )      # <-- EXIT ?
        if goOn != 'y':
            sys.exit()
    #########################################

    ### Look for diffs in shared files if appropriate.
    thereAreDiffs = False
    if dsrdPrjDictKey in ['spiClock', 'sprinkler2', 'shared']:
        dirsToCmpLst = [
            projDict['shared']['dir'],
            projDict['spiClock']['dir'],
            projDict['sprinkler2']['dir']
        ]
        thereAreDiffs = lookForDiffs( dirsToCmpLst,
            [ 'cfg.cfg',   'cfg.py',    'client.py',   'gui.py',
              'fileIO.py', 'server.py', 'swUpdate.py', 'utils.py' ])
    #########################################

    ### Exit, if desired, if diffs in shared files are problematic.
    if thereAreDiffs:
        print( '\n There are diffs in shared files.' )
        goOn = input( '   Continue (y/n)? -> ' )  # <-- EXIT ?
        if goOn != 'y':
            sys.exit()
    #########################################

    #### Get current ver num, calc new version, get date.
    print( '\n Getting curr/new Version Number and Date' )

    curVerStr, pcntChanged, newVerStr = \
    getVerNums( projFileWithVerNumInIt,
                fLstDict['changedTrackedPyFs']['len'],
                fLstDict['trackedPyFs']['len']
    )
    date = dt.datetime.now().strftime( '%d-%b-%Y' )
    print('   Percent of tracked .py files changed = {}%'.format(pcntChanged))
    print('   Old/New Version Numbers = {}/{}'.format(curVerStr, newVerStr))

    if pcntChanged == -1:
        print( '\n   Error getting ver num (divide by zero).\n')
    if pcntChanged == -2:
        print( '\n   Error getting ver num (file not found).\n')
    if pcntChanged == -3:
        print( '\n   Error getting ver num (search string not found).\n')
    #########################################

    #### Exit if there was a problem getting/calculating version numbers.
    if pcntChanged < 0:
        print( ' Exiting, RE: Error.\n' )
        sys.exit()  # <-- AUTO-EXIT ON ERROR !!
    #########################################

    #### Last chance to exit before changing ver num in source and releasing.
    print( '\n About to Update app Ver and Date in {}'.format(projFileWithVerNumInIt) )
    goOn = input( '   Continue (y/n)? -> ' )      # <-- EXIT ?
    if goOn != 'y':
        sys.exit()
    #########################################

    #### Write new ver num and date into source, 
    ###  add file that contains ver num to fLst if appropriate.
    print( '\n Updating app Ver and Date in {}'.format(projFileWithVerNumInIt) )
    fileToChangeVerNumIn = Path( projFileWithVerNumInIt )
    text = fileToChangeVerNumIn.read_text(encoding='utf-8')
    new_text=re.sub(r"VER = .*", f"VER = '{newVerStr} - {date}'",text,count=1) # pylint: disable=W1405
    fileToChangeVerNumIn.write_text(new_text, encoding='utf-8')

    if projFileWithVerNumInIt not in fLstDict['changedTrackedFs']['fLst']:
        print( '   Adding {} to changedTrackedFs'.format(projFileWithVerNumInIt))
        fLstDict['changedTrackedFs']['fLst'].append(projFileWithVerNumInIt)

        fLstDict['changedTrackedFs']['len'] = \
            fLstDict['changedTrackedFs']['len'] + 1
    #########################################

    #@rem only needed on first push
    #@rem git branch -M main
    #@rem git remote add origin https://github.com/sgarrow/spiClock.git
    #########################################

    #### Get commit message.
    commitTxt = input( '\n Enter GIT commit message -> ' )
    commitTxtWithQuotes = r'"{}. {}"'.format( newVerStr, commitTxt )
    #########################################

    #### git add
    print( '\n GIT Adding appropriate files.' )
    cmdBaseLst = [ 'git', 'add' ]
    for f in fLstDict['changedTrackedFs']['fLst']:
        cmd = cmdBaseLst + [f]
        hasErr, stdO, stdE = rtc.runCommand(cmd)
        pr.printStdOutOrStdErr( hasErr, stdO, stdE )
        if hasErr:
            print( ' Exiting, RE: Error.\n' )
            sys.exit()
    #########################################

    #### git commit
    print( '\n GIT Committing.' )
    cmd = [ 'git', 'commit', '--no-verify', '-m', commitTxtWithQuotes  ]
    hasErr, stdO, stdE = rtc.runCommand(cmd)
    pr.printStdOutOrStdErr( hasErr, stdO, stdE )
    if hasErr:
        print( ' Exiting, RE: Error.\n' )
        sys.exit()
    #########################################

    #### git set url
    print( '\n GIT Setting GitHub URL.' )
    cmd = [ 'git', 'remote', 'set-url', 'origin', projGithubUrl ]
    hasErr, stdO, stdE = rtc.runCommand(cmd)
    pr.printStdOutOrStdErr( hasErr, stdO, stdE )
    if hasErr:
        print( ' Exiting, RE: Error.\n' )
        sys.exit()
    #########################################

    #### git push
    print( ' GIT Pushing to GitHub.' )
    cmd = ['git', 'push', '-u', 'origin', 'main']
    hasErr, stdO, stdE = rtc.runCommand(cmd)
    pr.printStdOutOrStdErr( hasErr, stdO, stdE )
    if hasErr:
        print( ' Exiting, RE: Error.\n' )
        sys.exit()
    #########################################

    #### Exit or release?
    print( '\n Successfully pushed {} to GitHub.'.format(newVerStr) )
    goOn = input( '   Do you want to "Release" it (y/n)? -> ' )  # <-- EXIT ?
    if goOn != 'y':
        print()
        sys.exit()
    #########################################

    #### Release.
    releaseTxt = input( '\n   Enter release message -> ' )
    releaseTxtWithQuotes = r'"{}."'.format( releaseTxt )

    print( '\n gh Releasing on GitHub.' )
    cmd = ['gh', 'release', 'create', newVerStr, '--notes', releaseTxtWithQuotes]
    hasErr, stdO, stdE = rtc.runCommand(cmd)
    pr.printStdOutOrStdErr( hasErr, stdO, stdE )
    if hasErr:
        print( ' Exiting, RE: Error.\n' )
        sys.exit()
    print()
    #########################################
