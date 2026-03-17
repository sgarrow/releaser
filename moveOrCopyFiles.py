from pathlib   import Path
#############################################################################

def moveOrCopyFiles( src, dst, fLst, moveOrCopy ):

    if moveOrCopy not in ['Mov','Copy']:
        print(' moveOrCopy has invalid value.')
        return
    print('   {}ing from \n     {} to \n     {}.'.format(moveOrCopy,src,dst))

    for file in fLst:
        s =  src / file  # A Path join. All 3 vars type Path.
        d =  dst / file  # A Path join. All 3 vars type Path.
        # Move/Copy if source exists and is a file.
        try:
            if not s.exists():
                raise FileNotFoundError( ' {} not found.'.format(s) )
            if not s.is_file():
                raise IsADirectoryError( ' {} is not a file.'.format(s) )
        except Exception as e:
            print( ' Error: {}'.format(e) )
        else:
            if moveOrCopy == 'Mov':
                s.replace(d)
                print( '       Moved {}.'.format(file))
            elif moveOrCopy == 'Copy':
                d.write_bytes(s.read_bytes())
                print( '       Copied {}.'.format( file))
#############################################################################

def tstMoveOrCopyFiles():
    clkDir   = Path( r'C:\01-home\14-python\temp\tstClkDir' )
    sprDir   = Path( r'C:\01-home\14-python\temp\tstSprDir' )
    shrDir   = Path( r'C:\01-home\14-python\temp\tstShrDir' )
    dsts     = [clkDir, sprDir]
    fLstStr  = [ 'd1.txt', 'd2.txt', 'd3.txt' ]
    fLstPath = [ Path(x) for x in fLstStr ]

    print( '\n Moving files.' )
    #                src     dst     fLst       cmd
    moveOrCopyFiles( clkDir, shrDir, fLstPath, 'Mov' )

    x = input( 'Press Return to Continue.' )

    print( '\n Copying files.' )
    for dstn in dsts:
        #                src      dst   fLst       cmd
        moveOrCopyFiles( shrDir,  dstn, fLstPath, 'Copy' )
#############################################################################

