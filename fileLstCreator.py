import runTerminalCmd  as rtc
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
#############################################################################

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
#############################################################################

def getUntrackedFs():
    untrackedFiles = []
    cmdLst = [ 'git', 'status', '--porcelain' ]
    err, stdOut,stdErr = rtc.runCommand(cmdLst)
    if not err:
        stdOutLines = stdOut.split('\n')
        untrackedFiles = \
            [line.split()[1] for line in stdOutLines if line.split()[0]=='??']
    return err, stdOut, stdErr, untrackedFiles
#############################################################################

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
#############################################################################

def getUnexpectedUntrackedFs( untracked, expectedUntracked ):
    err, stdOut, stdErr = False, '', ''
    unexpectedUntrackedFiles = list(set(untracked) - set(expectedUntracked))
    if '__pycache__/' in unexpectedUntrackedFiles:
        unexpectedUntrackedFiles.remove('__pycache__/')
    return err, stdOut, stdErr, unexpectedUntrackedFiles
#############################################################################

def makeFileLstDict(projectsDict):
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
