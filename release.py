from pathlib   import Path

import datetime as dt
import pprint   as pp         # pylint: disable=W0611
import sys
import os
import re

import moveOrCopyFiles as mcf # pylint: disable=W0611
import fileLstCreator  as flc
import runTerminalCmd  as rtc
import printRoutines   as pr
import asciiColorCodes as ACC
import compareFiles    as cf
import getVerNums      as gvn

VER = 'v4.4.0 - 23-Mar-2026'
#############################################################################

def makeSingleDictContainingMetaDataOnAllProjects():

    fileBase = Path(r'C:\01-home\14-python\gitTrackedCode')
    webBase  = 'https://github.com/sgarrow/'

    prjDict  = {
        'spiClock':
            {'dir'     : fileBase / Path(r'spiClock'),
             'url'     : webBase  + 'spiClock.git',
             'verFile' : 'cmdVectors.py', 
             'active'  : False },
        'sprinkler2':
            {'dir'     : fileBase / Path(r'sprinkler2'),
             'url'     : webBase  + 'sprinkler2.git',
             'verFile' : 'cmdVectors.py',
              'active' : False },
        'shared':
            {'dir'     : fileBase / Path(r'sharedClientServerCode'),
             'url'     : webBase  + 'sharedClientServerCode.git',
             'verFile' : 'fileIO.py',
             'active'  : False },
        'soduko':
            {'dir'     : fileBase / Path(r'soduko'),
             'url'     : webBase  + 'soduko.git',
             'verFile' : 'soduko.py',
             'active'  : False },
        'multiCore':
            {'dir'     : fileBase / Path(r'multicore'),
             'url'     : webBase  + 'multiCore.git',
             'verFile' : 'main.py',
             'active'  : False },
        'clientServer':
            {'dir'     : fileBase / Path(r'clientServer'),
             'url'     : webBase  + 'clientServer.git',
             'verFile' : 'server.py',
             'active'  : False },
        'releaser':
            {'dir'     : fileBase / Path( r'releaser'),
             'url'     : webBase  + 'releaser.git',
             'verFile' : 'release.py',
             'active'  : False },
    }
    return prjDict
#############################################################################

def getDsrdPrjDictKey(prjDict):

    print( '\n Which project do you want to release.' )
    keyLst = list(prjDict.keys())
    for idx,ky in enumerate(keyLst):
        print( '  {} - {}'.format( idx, ky ) )

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
            if choiceInt not in range(0,len(prjDict)):
                print( '  Invalid choice integer' )
                continue
        break
    return keyLst[choiceInt]
#############################################################################

def exitOnError(errorFlag):
    if errorFlag:
        print( ' Exiting, RE: Error.\n' )
        sys.exit()
#############################################################################

def exitOnNoGoOn(inGoOn):
    if inGoOn != 'y':
        sys.exit()
#############################################################################

if __name__ == '__main__':

    print( '\n Releaser verion: {} '.format(VER))

    # Get Command Line Args (verbose PRiNt ENable).
    arguments  = sys.argv
    scriptName = arguments[0]
    userArgs   = arguments[1:]
    prnEn      = (len(userArgs) > 0 and '/p' in userArgs)

    # Make a dict that contains meta data on ALL releaseable projects.
    projDict = makeSingleDictContainingMetaDataOnAllProjects()

    # Prompt user to select (from the "keys" in the projDict)
    # the name (key) of the project to be released.
    dsrdPrjDictKey = getDsrdPrjDictKey(projDict)
    if dsrdPrjDictKey == 'quit':
        sys.exit()

    # Set the user selected project as "Active" in projDict, then
    # set the local "Working Variables" and finally, set the cwd.
    projDict[dsrdPrjDictKey]['active'] = True
    projFileWithVerNumInIt = projDict[dsrdPrjDictKey]['verFile']
    projGithubUrl          = projDict[dsrdPrjDictKey]['url']
    projDir                = projDict[dsrdPrjDictKey]['dir']
    os.chdir(projDir)
    #pr.printPathInfo(projDir)
    print( '\n Releasing {}\n'.format(projDir) )
    print( ' Current working directory: {}'.format(Path.cwd() ))

    # Make a dict containing a seperate list for tracked, changed, untracked,
    # etc, files for the "Active" project.  There are now 2 dicts:
    # projDict containing meta data for ALL projects and fLstDict containing
    # lists of various types of files for the "Active" project.
    print( '\n Getting changed and untracked files.' )
    fLstDict = flc.makeFileLstDict(projDict)
    pr.printFileLstDict( fLstDict, prnEn )

    # Exit if there were problems making fLstDict.
    errFound, funcRspMsg = flc.lookForErrorsInFileLstDict( fLstDict )
    if errFound:
        print( '{}{}{}'.format( ACC.RED_BOLD, funcRspMsg, ACC.OFF ))
        sys.exit()

    # Exit, if desired, if there are unexpected-untracked files
    # present or there are no tracked/changed files present.
    if fLstDict['unexpectedUntrackedFs']['len'] > 0:
        print( '\n unexpected/untracked files present.')
        print( '   Continuing will not add them.')
        print( '   Add from cmd line like this <git add fName>')
        goOn = input( '   Continue (y/n)? -> ' )
        exitOnNoGoOn(goOn)

    if fLstDict['changedTrackedFs']['len'] == 0:
        print( '\n No tracked/changed files present.' )
        goOn = input( '   Continue (y/n)? -> ' )
        exitOnNoGoOn(goOn)

    # Look for diffs in shared files if appropriate.
    thereAreDiffs = False # pylint: disable=C0103
    if dsrdPrjDictKey in ['spiClock', 'sprinkler2', 'shared']:
        dirsToCmpLst = [
            projDict['shared']['dir'],
            projDict['spiClock']['dir'],
            projDict['sprinkler2']['dir']
        ]
        thereAreDiffs= cf.lookForDiffs( dirsToCmpLst, # pylint: disable=C0103
            [ 'cfg.cfg',   'cfg.py',    'client.py',   'gui.py',
              'fileIO.py', 'server.py', 'swUpdate.py', 'utils.py' ])

    # Exit, if desired, if diffs in shared files are problematic.
    if thereAreDiffs:
        print( '\n There are diffs in shared files.' )
        goOn = input( '   Continue (y/n)? -> ' )
        exitOnNoGoOn(goOn)

    # Get the current ver num, calculate the new ver, and get the date.
    print( '\n Getting curr/new Version Number and Date' )

    curVerStr, pcntChanged, newVerStr = \
    gvn.getVerNums( projFileWithVerNumInIt,
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

    # Exit if there was a problem getting/calculating version numbers.
    if pcntChanged < 0:
        print( ' Exiting, RE: Error.\n' )
        sys.exit()

    # Last chance to exit before changing ver num in source and releasing.
    print( '\n About to Update app Ver and Date in {}'.\
        format(projFileWithVerNumInIt) )
    goOn = input( '   Continue (y/n)? -> ' )
    exitOnNoGoOn(goOn)

    # Write new ver num and date into source, add file
    # that contains ver num to fLstDict if appropriate.
    print( '\n Updating app Ver and Date in {}'.format(projFileWithVerNumInIt))
    fileToChangeVerNumIn = Path( projFileWithVerNumInIt )
    text = fileToChangeVerNumIn.read_text(encoding='utf-8')
    new_text=re.sub(r"VER = .*", f"VER = '{newVerStr} - {date}'",text,count=1) # pylint: disable=W1405
    fileToChangeVerNumIn.write_text(new_text, encoding='utf-8')

    if projFileWithVerNumInIt not in fLstDict['changedTrackedFs']['fLst']:
        print( '   Adding {} to changedTrackedFs'.format(projFileWithVerNumInIt))
        fLstDict['changedTrackedFs']['fLst'].append(projFileWithVerNumInIt)

        fLstDict['changedTrackedFs']['len'] = \
            fLstDict['changedTrackedFs']['len'] + 1

    #@rem only needed on first push
    #@rem git branch -M main
    #@rem git remote add origin https://github.com/sgarrow/spiClock.git

    # Get commit message.
    commitTxt = input( '\n Enter GIT commit message -> ' )
    cmtTxtQuotes = r'"{}. {}"'.format( newVerStr, commitTxt )

    gitCmdDict = {
        0: { 'msg'   : '\n GIT Adding appropriate files.',
             'cmdLst': [ ['git', 'add', f] \
                         for f in fLstDict['changedTrackedFs']['fLst'] ]     },
        1: { 'msg'   : '\n GIT Committing.',
             'cmdLst': [['git', 'commit', '--no-verify', '-m',cmtTxtQuotes]] },
        2: { 'msg'   : '\n GIT Setting GitHub URL.',
             'cmdLst': [['git', 'remote', 'set-url', 'origin',projGithubUrl]]},
        3: { 'msg'   : ' GIT Pushing to GitHub.',
             'cmdLst': [['git', 'push', '-u', 'origin', 'main']]             }
    }
    for k in range(len(gitCmdDict)):
        print(gitCmdDict[k]['msg'])
        for cmd in gitCmdDict[k]['cmdLst']:
            hasErr, stdO, stdE = rtc.runCommand(cmd)
            pr.printStdOutOrStdErr( hasErr, stdO, stdE )
            exitOnError( hasErr )

    # Exit or release?
    print( '\n Successfully pushed {} to GitHub.'.format(newVerStr) )
    goOn = input( '   Do you want to "Release" it (y/n)? -> ' )  # <-- EXIT ?
    exitOnNoGoOn(goOn)

    # Release.
    releaseTxt = input( '\n   Enter release message -> ' )
    releaseTxtWithQuotes = r'"{}."'.format( releaseTxt )

    print( '\n gh Releasing on GitHub.' )
    cmd = ['gh', 'release', 'create', newVerStr, '--notes', releaseTxtWithQuotes]
    hasErr, stdO, stdE = rtc.runCommand(cmd)
    pr.printStdOutOrStdErr( hasErr, stdO, stdE )
    exitOnError( hasErr )
    print( '\n Successfully released {} on GitHub.'.format(newVerStr) )
    print()
