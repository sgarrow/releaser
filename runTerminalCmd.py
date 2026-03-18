import subprocess as sp
#############################################################################

def runCommand( cmdLst ):

    # If check is true, and the process exits with a non-zero exit code,
    # a CalledProcessError exception will be raised. Attributes of that
    # exception hold the arguments, the exit code, and stdout and stderr
    # if they were captured.

    print('   Terminal Cmd: {}'.format(' '.join(cmdLst)))
    error = False
    try:
        result = sp.run(
            cmdLst,
            capture_output = True,
            text           = True,
            shell          = False,
            check          = True,
        )
        return error, result.stdout.strip(), result.stderr.strip()
    except sp.CalledProcessError as e:
        error = True
        return error, e.stdout.strip(),      e.stderr.strip()
    except FileNotFoundError as e:
        error = True
        return error, '', e
#############################################################################

def runCommandTst():
    cmdLst = [ 'gi', 'ls-files' ]
    cmdLst = [ 'cmd', '/c', 'dir' ]
    err, stdOut, stdErr = runCommand(cmdLst)
    print( '\nerr = \n\n', err, '\n\nstdout = \n\n', stdOut, '\n\nstderr = \n\n',stdErr )
    print()
    return err, stdOut, stdErr
#############################################################################

if __name__ == '__main__':
    runCommandTst()
