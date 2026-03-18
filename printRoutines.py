import sys
#############################################################################
ESC_CODE       = '{}'.format( '\x1b' )

TERMINATE_CODE = '{}'.format( '[0'  )

RED_CODE       = '{}'.format( '[31' )
WHITE_CODE     = '{}'.format( '[37' )
BOLD_ON_CODE   = '{}'.format( '1'    )

RED        = '{}{}m'.format(    ESC_CODE, RED_CODE                 )
RED_BOLD   = '{}{};{}m'.format( ESC_CODE, RED_CODE,   BOLD_ON_CODE )
WHITE_BOLD = '{}{};{}m'.format( ESC_CODE, WHITE_CODE, BOLD_ON_CODE )

OFF        = '{}{}m'.format(    ESC_CODE, TERMINATE_CODE           )
#############################################################################


def mapTo2D(  flatList, numCols ):
    # mapTo2D( [1,2,3,4,5,6,7,8], 2 ) = [[1,2],[3,4],[5,6],[7,8]]
    twoD = [flatList[ii:ii+numCols] for ii in range(0,len(flatList),numCols)]
    return twoD
#############################################################################

def printPathInfo(inPathInfo):
    print()
    print( ' inPathInfo   = {}'.format(inPathInfo   ))
    print( '   inPathInfo.name   = {}'.format(inPathInfo.name   ))
    print( '   inPathInfo.stem   = {}'.format(inPathInfo.stem   ))
    print( '   inPathInfo.suffix = {}'.format(inPathInfo.suffix ))
    print( '   inPathInfo.anchor = {}'.format(inPathInfo.anchor ))
    print( '   inPathInfo.parent = {}'.format(inPathInfo.parent ))
    print()
#############################################################################


def printFileLstDict(inFileListDict, pEn):
    #pp.pprint(inFileListDict)
    printOrder = [
        'trackedFs',    'trackedPyFs',         'changedTrackedPyFs',
        'untrackedFs',  'expectedUntrackedFs', 'changedTrackedFs',
        'unexpectedUntrackedFs'
    ]
    groupSize = 2  if pEn else 3
    width     = 50 if pEn else 25

    for el in printOrder:

        print( '\n   {}{}{} (len  = {}) = '.\
            format( WHITE_BOLD,el,OFF, inFileListDict[el]['len']))

        if el == 'trackedFs' and not pEn:
            print( '   Not printed.  Use /p cmd line arg.')
            continue
        #pp.pprint(inFileListDict[el]['fLst'])
        d2FileList = mapTo2D( inFileListDict[el]['fLst'], groupSize )
        pStr = ''
        for group in d2FileList:
            pStr = [ '{}{}'.format((width-len(x))*' ',x) for x in group ]
            [print(x,end = '') for x in pStr] # pylint: disable=W0106
            print()
#############################################################################

def printStdOutOrStdErr( hasError, stdOut, stdErr ):

    if hasError:
        print( '   error = {}'.format(hasError))
        msgLines = stdErr.split('\n')
    else:
        msgLines = stdOut.split('\n')

    for theLine in  msgLines:
        if theLine != '\n':  # Don't print blank lines.
            print('     {}'.format(theLine))

    if hasError:
        print( ' Exiting, RE: Error.\n' )
        sys.exit()
#############################################################################
