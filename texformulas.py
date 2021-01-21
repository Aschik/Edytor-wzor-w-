
#--------------------Functions--------------------
getBeginStr = lambda x: r'\begin{%s}' %x
getEndStr = lambda x: r'\end{%s}' %x


#--------Get string for matrix inner lines--------
def getMatrixInner(nrow,ncol,add_dummy):
    if not add_dummy:
        line_str='&'.join([' ']*ncol)
        inner_str=(r' \\'+'\n').join([line_str,]*nrow)
    else:
        inner_str=[]
        for ii in range(nrow):
            line_ii=['a_{%d%d}' %(ii+1,jj+1) for jj in range(ncol)]
            line_ii=' & '.join(line_ii)
            inner_str.append(line_ii)
        inner_str=(r' \\'+'\n').join(inner_str)

    return inner_str


#--Get string for matrix with left and right brackets--
def getDoubleMatrix(nrow,ncol,matrix_type,add_dummy=True):
    assert matrix_type in ['matrix','bmatrix','pmatrix','vmatrix',
            'Bmatrix','Vmatrix'], "<matrix_type> not included."

    matrix_str=getMatrixInner(nrow,ncol,add_dummy)
    begin_matrix=getBeginStr(matrix_type)
    end_matrix=getEndStr(matrix_type)
    ret_str='''\
%s
%s
%s
''' %(begin_matrix, matrix_str, end_matrix)

    return ret_str


#---------Get string for cases inner lines---------
def getCasesInner(nrow,add_dummy):
    inner_str=[]
    for ii in range(nrow):
        if not add_dummy:
            line_ii=r' & \text{ if }'
        else:
            line_ii=r' y_%d & \text{ if } x_%d' %(ii,ii)
        inner_str.append(line_ii)
    line_str=(r' \\'+'\n').join(inner_str)

    return line_str


#-----------Get string for cases matrix-----------
def getCasesMatrix(nrow,add_dummy=True):
    begin_matrix=getBeginStr('cases')
    end_matrix=getEndStr('cases')
    matrix_str=getCasesInner(nrow,add_dummy)
    ret_str='''\
%s
%s
%s
''' %(begin_matrix,matrix_str,end_matrix)
    return ret_str


#-----Get string for matrix with left bracket-----
def getLeftMatrix(nrow,ncol,bracket_str,add_dummy=True):
    bracket_dict={
            '(': r'(',
            '[': r'[',
            '{': r'\{',
            '<': r'<',
            '|': r'|'}
    assert bracket_str in bracket_dict.keys(), "<matrix_type> not included."

    matrix_str=getMatrixInner(nrow,ncol,add_dummy)
    begin_matrix=r'\left%s%s' %(bracket_dict[bracket_str],getBeginStr('matrix'))
    end_matrix=r'%s\right.' %getEndStr('matrix')
    ret_str='''\
%s
%s
%s
''' %(begin_matrix, matrix_str, end_matrix)

    return ret_str



#-----Get string for matrix with right bracket-----
def getRightMatrix(nrow,ncol,bracket_str,add_dummy=True):
    bracket_dict={
            ')': r')',
            ']': r']',
            '}': r'\}',
            '>': r'>',
            '|': r'|'}
    assert bracket_str in bracket_dict.keys(), "<matrix_type> not included."

    matrix_str=getMatrixInner(nrow,ncol,add_dummy)
    begin_matrix=r'\left.%s' %getBeginStr('matrix')
    end_matrix=r'%s\right%s' %(getEndStr('matrix'),bracket_dict[bracket_str])
    ret_str='''\
%s
%s
%s
''' %(begin_matrix, matrix_str, end_matrix)

    return ret_str
