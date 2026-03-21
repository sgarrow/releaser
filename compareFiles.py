from itertools import combinations
from pathlib   import Path
#############################################################################

def lookForDiffs( dirsToComp, fLstStr ):

    print( '\n Looking for diffs among shared files.\n' )

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
