
import os
import subprocess
import tempfile
import texformulas
import json

RESO=[200,200]

CURRENT_DIR     = os.path.dirname(os.path.abspath(__file__))
RELATIVE_OUTDIR = 'tab_icons'
OUTPUTDIR       = os.path.join(CURRENT_DIR,RELATIVE_OUTDIR)
ICON_META_FILE  = os.path.join(CURRENT_DIR,'icon_paths.txt')

#Renderowanie macierzy
def renderMatrix(nrow,ncol,matrix_type,bracket_str,add_dummy,
        filename,subdir,outdir):

    assert matrix_type in ['left','right','cases','matrix','bmatrix',
            'pmatrix','vmatrix','Bmatrix','Vmatrix'],\
        "<matrix_type> should be one in ['left','right','cases','matrix','bmatrix', 'pmatrix','vmatrix','Bmatrix','Vmatrix']."

    return_list=[]

    if matrix_type=='left':
        tex_str=texformulas.getLeftMatrix(nrow,ncol,bracket_str,add_dummy)
    elif matrix_type=='right':
        tex_str=texformulas.getRightMatrix(nrow,ncol,bracket_str,add_dummy)
    elif matrix_type=='cases':
        tex_str=texformulas.getCasesMatrix(nrow,add_dummy)
    else:
        tex_str=texformulas.getDoubleMatrix(nrow,ncol,matrix_type,add_dummy)
    return return_list




FORMULAE_LISTS=[
    ('asdasd'            , texformulas.GREEK_LETTERS)      ,
    ('Set symbol'       , texformulas.MATH_SET_SYMBOLS)   ,
    ('Set operator'     , texformulas.MATH_SET_OPERATORS) ,
    ('Math operator'    , texformulas.MATH_OPERATORS)     ,
    ('Text format'      , texformulas.TEXT_FORMATTING)    ,
    ('Spacing'          , texformulas.SPACING)            ,
    ('Decoration'       , texformulas.DECOREATIONS)       ,
    ('Arrow'            , texformulas.ARROWS)             ,
    ('Sub-super script' , texformulas.SUB_SUPER_SCRIPTS)  ,
    ('Fraction'         , texformulas.FRACTIONS)          ,
    ('Integration'      , texformulas.INTEGRATIONS)       ,
    ('Cap/cup'          , texformulas.CAP_CUPS)           ,
    ('Sum'              , texformulas.SUM_PRODUCT)        ,
    ('Bracket'          , texformulas.BRACKETS)           ,
    ('Comparison'       , texformulas.COMPARE_OPERATORS)
]

MATRIX_LISTS=[
        (2 , 2 , 'left'    , '(' , True) ,
        (2 , 2 , 'left'    , '[' , True) ,
        (2 , 2 , 'left'    , '{' , True) ,
        (2 , 2 , 'left'    , '<' , True) ,
        (2 , 2 , 'left'    , '|' , True) ,
        (2 , 2 , 'right'   , ')' , True) ,
        (2 , 2 , 'right'   , ']' , True) ,
        (2 , 2 , 'right'   , '}' , True) ,
        (2 , 2 , 'right'   , '>' , True) ,
        (2 , 2 , 'right'   , '|' , True) ,
        (2 , 2 , 'matrix'  , ''  , True) ,
        (2 , 2 , 'bmatrix' , ''  , True) ,
        (2 , 2 , 'pmatrix' , ''  , True) ,
        (2 , 2 , 'vmatrix' , ''  , True) ,
        (2 , 2 , 'Bmatrix' , ''  , True) ,
        (2 , 2 , 'Vmatrix' , ''  , True) ,
        (2 , 2 , 'cases'   , ''  , True)
]





if __name__=='__main__':

    #Renderuj ikony macierzy
    outdirii=os.path.join(OUTPUTDIR,'tab_matrix')
    print ('save list to'),outdirii
    outdirii=os.path.expanduser(outdirii)

    if not os.path.exists(outdirii):
        os.makedirs(outdirii)

    matrix_icon_meta_list=[]
    for ii,mii in enumerate(MATRIX_LISTS):
        subdir='tab_matrix'
        outdirii=os.path.join(OUTPUTDIR,subdir)

        fileii=str(ii+1).rjust(len(str(len(MATRIX_LISTS))),'0')+'.png'
        print ('save matrix img')
        argsii=mii+(fileii,subdir,outdirii)

        try:
            meta_listii=renderMatrix(*argsii)
            matrix_icon_meta_list.extend(meta_listii)
        except:
            matrix_icon_meta_list.extend([])





