ESC_CODE       = '{}'.format( '\x1b' )

TERMINATE_CODE = '{}'.format( '[0'  )

RED_CODE       = '{}'.format( '[31' )
WHITE_CODE     = '{}'.format( '[37' )
BOLD_ON_CODE   = '{}'.format( '1'    )

RED            = '{}{}m'.format(    ESC_CODE, RED_CODE                 )
RED_BOLD       = '{}{};{}m'.format( ESC_CODE, RED_CODE,   BOLD_ON_CODE )
WHITE_BOLD     = '{}{};{}m'.format( ESC_CODE, WHITE_CODE, BOLD_ON_CODE )

OFF            = '{}{}m'.format(    ESC_CODE, TERMINATE_CODE           )
#############################################################################
