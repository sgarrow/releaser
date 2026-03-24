# Setup codes for building things that can be put in print strings
ESC_CODE       = '{}'.format( '\x1b' )

TERMINATE_CODE = '{}'.format( '[0'  )

RED_CODE       = '{}'.format( '[31' )
WHITE_CODE     = '{}'.format( '[37' )
BOLD_ON_CODE   = '{}'.format( '1'    )

# Things that can be put in print strings.  
# e.g., print('{}{}{}'.format(RED,'hello',OFF)) # print hello in red.
RED            = '{}{}m'.format(    ESC_CODE, RED_CODE                 )
RED_BOLD       = '{}{};{}m'.format( ESC_CODE, RED_CODE,   BOLD_ON_CODE )
WHITE_BOLD     = '{}{};{}m'.format( ESC_CODE, WHITE_CODE, BOLD_ON_CODE )

OFF            = '{}{}m'.format(    ESC_CODE, TERMINATE_CODE           )
#############################################################################
