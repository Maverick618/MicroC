from microC_lexer import tokens
import ply.yacc as yacc
import collections
from microC_stack import Stack  # 特殊栈

scope_st = Stack()  # 作用域栈
static_global = collections.OrderedDict()  # 静态全局作用域
static_global['input'] = ('Func', 'int', [])
static_global['print'] = ('Func', 'void', [])
scope_st.push(static_global)  # 全局域入栈

temp = 0
func_tail = 0

l_while = 0
label = 0  # for if end then
while_flag = False  # true is while stmt, false is if stmt
while_scope = False  # while 域内标签
# l_or_and = 0  # for or, and
# 错误信息
error_meg = []


def error(code, var=None):
    if code == 0:
        return error_meg
    elif code == 1:
        # 试图定义 Void 类型变量
        error_meg.append('Error: Trying To Definite a Void Variable.\n Warning: rejected the void and set it as int.')
    elif code == 2:
        # 使用未定义的变量
        error_meg.append('Error: Undefined Variable' + '[' + var + ']')
    elif code == 3:
        # 变量的重复定义
        error_meg.append('Error: Redefined Variable' + '[' + var + ']')
    elif code == 4:
        # 存在重复的函数参数声明
        error_meg.append('Error: Existing The Same Function Parameter Declarations[' + var + ']')
    elif code == 5:
        # 存在隐式类型转换
        error_meg.append('Warning: implicit type conversions exist.')
    elif code == 6:
        # 调用函数时参数数量有误
        error_meg.append('Error: Function Call With Incorrect Number of Arguments. ')
    elif code == 7:
        # 尝试调用未定义的函数
        error_meg.append('Error: Trying to Call an Undefined Function [' + var + '()]')
    elif code == 8:
        # 调用函数时参数类型不对
        error_meg.append('Warning: wrong parameter type when calling function')
    elif code == 9:
        # 程序没有 main 函数入口
        error_meg.append('Error: Undefined Reference To \'main\'.\n Warning: the program must have a \'main\' '
                         'function as its entry point.')
    elif code == 10:
        # 函数的重复定义
        error_meg.append('Error: redefined function' + '[' + var + ']')


# 运算符优先级
precedence = (
    ('left', 'ASSIGN'),
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'LT', 'GT', 'LE', 'GE'),
    ('left', 'EQ', 'NE'),
    ('left', 'LSHIFT', 'RSHIFT'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('right', 'UMINUS', 'NOT'),  # Unary minus operator
)


def p_Start(p):
    'Start : Program'
    # main函数查找检测
    if scope_st.find('main', 'Func'):
        print('\nCALL main')
    else:
        error(9)
    p[0] = ('Start', p[1:])  # 最后一行生成树节点, tuple三元素分别是 结点名，孩子结点，属性和中间代码


def p_Program(p):
    '''
    Program : Program GlobalDecl
            |'''
    ic = []
    if len(p) == 3:
        ic = p[2][-1][0]
    p[0] = ('Program', p[1:], ic)


def p_GlobalDecl(p):
    '''
    GlobalDecl : FuncDecl
               | VarDecl SEMI
    '''

    ic = p[1][-1][0]

    p[0] = ('GlobalDecl', p[1:], [ic])


def p_FuncDecl(p):
    'FuncDecl : FuncHead FuncBody'
    global func_tail
    print('Func_tail_' + str(func_tail) + ':')
    func_tail += 1
    p[0] = ('FuncDecl', p[1:])


def p_FuncHead(p):
    'FuncHead : Type FuncName LPAREN newScope Args RPAREN'
    # 函数入域
    name = p[2][1][0]
    # p[1][1][0] 为返回类型， p[5][2]为参数列表
    args = p[5][2]
    scope_st.get_static_scope()[name] = ('Func', p[1][1][0], args)
    p[0] = ('FuncHead', p[1:], args)


def p_FuncBody(p):
    'FuncBody : LBRACE Stmts RBRACE'
    # 分析完成，退出域
    scope_st.pop()
    p[0] = ('FuncBody', p[1:])


def p_newScope(p):
    'newScope :'
    # 新的域空间建立
    cur_scope = collections.OrderedDict()
    scope_st.push(cur_scope)


def p_FuncName(p):
    'FuncName : ID'
    # 略过函数定义体
    print('GOTO Func_tail_' + str(func_tail))
    # 函数静态域查找
    name = p[1]
    if scope_st.find(name, 'Func') is not False:
        error(10, name)
        exit(-1)
    # 函数体标签
    print()
    print(p[1] + ':')
    p[0] = ('FuncName', p[1:])


def p_Args(p):
    '''
    Args : Arg
         |'''
    # 参数属性传递， p[1][2]为参数列表
    args = [] if len(p) == 1 else p[1][2]
    p[0] = ('Args', p[1:], args)


def p_Type(p):
    '''
    Type : INT
         | CHAR
         | VOID
    '''
    p[0] = ('Type', p[1:])


def p_Arg(p):
    '''
    Arg : Type ID
        | Arg COMMA Type ID
    '''
    # 形式参数声明获取类型和名字
    ic = [p[1][1][0], p[2]] if len(p) == 3 else [p[3][1][0], p[4]]
    args = [] if len(p) == 3 else p[1][2]
    # 域内检测： 参数的重复声明
    if scope_st.findInCurScope(ic[1]):
        error(4, ic[1])
        print('skip by[delete the repeated arg]')
    else:
        scope_st.top()[ic[1]] = ('Var', ic[0], None)
        args.append(ic[0])  # 实际只需类型即可

    print('PARAM ' + ic[0] + ' ' + ic[1])
    p[0] = ('Arg', p[1:], args)


def p_VarDeclStmt(p):
    'VarDeclStmt : VarDecl SEMI'
    p[0] = ('ValDecls', p[1:])


def p_VarDecl(p):
    '''
    VarDecl : Type ID
            | VarDecl COMMA ID
    '''
    ic = []
    if len(p) == 3:
        if p[1][1][0] == 'VOID':
            error(1)
            p[1][1][0] = 'INT'
    # 变量声明
    ic.append(p[1][-1][0])  # 类型
    ic.append(p[2 if len(p) == 3 else 3])  # 名字

    # 变量检测入域
    if scope_st.findInCurScope(ic[1]):
        error(3, ic[1])
    else:
        scope_st.top()[ic[1]] = ('Var', ic[0], None)

    # 中间代码打印
    for s in ic:
        print(s, end=' ')
    print()

    p[0] = ('VarDecl', p[1:], ic)


def p_Stmts(p):
    '''
    Stmts : Stmts Stmt
         |'''
    p[0] = ('Stmts', p[1:])


def p_Stmt(p):
    '''
    Stmt : AssignStmt
         | PrintStmt
         | CallStmt
         | ReturnStmt
         | IfStmt
         | WhileStmt
         | BreakStmt
         | ContinueStmt
         | VarDeclStmt
    '''
    p[0] = ('Stmt', p[1:])


def p_AssignStmt(p):
    'AssignStmt : ID ASSIGN Expr SEMI'

    # 变量查找
    global temp
    name = p[1]
    # 优先在域内查找
    var_info = scope_st.find(name, 'Var')
    t = ''  # 变量id的类型
    if var_info is False:
        error(2, name)
        # 缺省的变量以及缺省变量类型
        t = 'int'
        print('skip_by[int ' + name + ';] ')
        # 缺省的变量入域
        scope_st.top()[name] = ('Var', 'int', 0)
    else:
        t = var_info[1]  # 获取变量类型

    if t != p[3][2][1]:
        error(5)
        if t == 'int':
            temp_ = 'temp_' + str(temp)
            temp += 1
            print(temp_ + ' = ctoi(' + p[3][2][0] + ')')
            print(name + ' = ' + temp_)
        else:
            temp_ = 'temp_' + str(temp)
            temp += 1
            print(temp_ + ' = itoc(' + p[3][2][0] + ')')
            print(name + ' = ' + temp_)
    # 打印中间代码
    else:
        print(name + ' = ' + p[3][2][0])

    p[0] = ('AssignStmt', p[1:])


def p_PrintStmt(p):
    'PrintStmt : PRINT LPAREN Actuals RPAREN SEMI'
    args = p[3][2]
    for arg in args:
        print('ARG ' + arg[1])
    print('CALL print')
    p[0] = ('PrintStmt', p[1:])


def p_PActuals(p):
    '''
    PActuals : PActuals COMMA Expr
             |'''
    args = []
    if len(p) == 4:
        # print('ARG ' + p[3][2][0])
        args = p[1][2]
        # 类型，名字
        args.append([p[3][2][1], p[3][2][0]])

    p[0] = ('PActuals', p[1:], args)


def p_CallStmt(p):
    'CallStmt : CallExpr SEMI'
    p[0] = ('CallStmt', p[1:])


def p_CallExpr(p):
    'CallExpr : ID LPAREN Actuals RPAREN'
    # 查找函数, 获取返回值
    global temp
    func = scope_st.find(p[1], 'Func')
    ic = []
    args = p[3][2]
    if func is False:
        error(7, p[1])
        print('skip_by[return 0 as call null.]')
        if not args:
            print('Warning: discard parameters')
        ic = ['0', 'int']
    else:
        # func[1]是返回类型, func[2]是参数类型表
        if len(args) != len(func[2]):
            error(6)
            print('CALL Failed.\nskip_by[return 0]')
            ic = ['0', 'int']
        else:
            # print(func[2], args)
            for i in range(len(func[2])):
                if func[2][-(i + 1)] != args[i][0]:
                    error(8)
                    error(5)
                    # 类型转换
                    temp_ = 'temp_' + str(temp)
                    temp += 1
                    if func[2][-(i + 1)] == 'int':
                        print(temp_ + ' = ctoi(' + args[i][1] + ')')
                        args[i][1] = temp_
                    else:
                        print(temp_ + ' = itoc(' + args[i][1] + ')')
                        args[i][1] = temp_
                    print('ARG ' + temp_)
                else:
                    print('ARG ' + args[i][1])
            # 打印的参数信息
            arg_str = ''
            for [t, n] in args:
                if arg_str == '':
                    arg_str += n
                else:
                    arg_str += ', ' + n
            # 打印中间代码
            if func[1] == 'void':
                ic = [p[1] + '(' + arg_str + ')', 'int']
            else:
                ic = [p[1] + '(' + arg_str + ')', func[1]]
            print('CALL ' + p[1])

    p[0] = ('CallExpr', p[1:], ic)


def p_Actuals(p):
    '''
    Actuals : Expr PActuals
            |'''
    args = []
    if len(p) == 3:
        args = p[2][2]
        args.append([p[1][2][1], p[1][2][0]])

    p[0] = ('Actuals', p[1:], args)


def p_ReturnStmt(p):
    '''
    ReturnStmt : RETURN Expr SEMI
               | RETURN SEMI
    '''

    print('RETURN ' + p[2][2][0] if len(p) == 4 else '')
    p[0] = ('ReturnStmt', p[1:])


def p_IfStmt(p):
    '''
    IfStmt : If TestExpr Then StmtsBlock EndThen EndIf
           | If TestExpr Then StmtsBlock EndThen Else StmtsBlock EndIf
    '''
    p[0] = ('IfStmt', p[1:])


def p_TestExpr(p):
    'TestExpr : LPAREN Expr RPAREN'
    global while_flag, l_while, label
    if while_flag:  # while 中的 Test 语句
        #  中间代码
        print("if " + p[2][2][0] + ' == 0 Goto end_while_' + str(l_while - 1))
        while_flag = False
    else:  # if 中的 Test 语句
        #  中间代码
        print("if " + p[2][2][0] + ' == 0 Goto label_' + str(label))
        label += 1
    p[0] = ('TestExpr', p[1:])


def p_StmtsBlock(p):
    'StmtsBlock : LBRACE newScope Stmts RBRACE '
    p[0] = ('StmtsBlock', p[1:])


def p_If(p):
    'If : IF'
    p[0] = ('If', p[1:])


def p_Else(p):
    'Else : ELSE'

    p[0] = ('Else', p[1:])


def p_Then(p):
    'Then :'
    p[0] = ('Then', p[1:])


def p_EndThen(p):
    'EndThen :'
    # 打上标签
    global label
    print('label_' + str(label - 1) + ':')
    p[0] = ('EndThen', p[1:])


def p_EndIf(p):
    'EndIf :'
    p[0] = ('EndIf', p[1:])


def p_WhileStmt(p):
    '''
    WhileStmt : While TestExpr Do StmtsBlock EndWhile
    '''
    # todo WhileStmt 是否需要完善？
    # while 域结束
    global while_scope
    while_scope = False
    p[0] = ('WhileStmt', p[1:])


def p_While(p):
    'While : WHILE'
    # 开始标签，while状态
    global l_while, while_flag
    while_flag = True
    print('start_while_' + str(l_while) + ':')
    l_while += 1
    p[0] = ('While', p[1:])


def p_Do(p):
    'Do :'
    # 即将进入while域内
    global while_scope
    while_scope = True
    p[0] = ('Do', p[1:])


def p_EndWhile(p):
    'EndWhile :'
    global l_while
    print('Goto start_while_' + str(l_while - 1))
    print('end_while_' + str(l_while - 1) + ':')
    p[0] = ('EndWhile', p[1:])


def p_BreakStmt(p):
    '''
    BreakStmt : BREAK SEMI
    '''
    # 如果在 while 域内直接跳转到 end_while 处，否则忽略该语句
    global while_scope
    if while_scope:
        print('Goto end_while_' + str(l_while - 1))
    p[0] = ('BreakStmt', p[1:])


def p_ContinueStmt(p):
    '''
    ContinueStmt : CONTINUE SEMI
    '''
    # 如果在 while 域内直接跳转到 start_while 处，否则忽略该语句
    global while_scope
    if while_scope:
        print('Goto start_while_' + str(l_while - 1))
    p[0] = ('ContinueStmt', p[1:])


def p_Expr_1(p):
    '''
    Expr : Expr PLUS Expr
         | Expr MINUS Expr
         | Expr TIMES Expr
         | Expr DIVIDE Expr
         | Expr LSHIFT Expr
         | Expr RSHIFT Expr
         | Expr LT Expr
         | Expr GT Expr
         | Expr EQ Expr
         | Expr NE Expr
         | Expr LE Expr
         | Expr GE Expr
         | Expr OR Expr
         | Expr AND Expr
    '''
    global temp
    t_1 = p[1][2][1]
    t_2 = p[3][2][1]
    if t_1 == t_2:
        # 不需要类型转换
        ic = ['temp_' + str(temp)]
        temp += 1
        ic.append(t_1)
        print(ic[0] + ' = ' + p[1][2][0] + ' ' + p[2] + ' ' + p[3][2][0])
    else:
        # 存在向上转型, 默认向上转型
        error(5)
        temp_ = 'temp_' + str(temp)
        temp += 1
        ic = ['temp_' + str(temp), 'int']
        temp += 1
        if t_1 == 'char':
            print(temp_ + ' = ctoi(' + p[1][2][0] + ')')
            print(ic[0] + ' = ' + temp_ + ' ' + p[2] + ' ' + p[3][2][0])
        else:
            print(temp_ + ' = ctoi(' + p[3][2][0] + ')')
            print(ic[0] + ' = ' + p[1][2][0] + ' ' + p[2] + ' ' + temp_)

    p[0] = ('Expr', p[1:], ic)

def p_Expr_2(p):
    '''
    Expr : NOT Expr
         | MINUS Expr %prec UMINUS
    '''
    global temp
    ic = ['temp_' + str(temp), p[2][2][1]]
    temp += 1
    print(ic[0] + ' = ' + p[1] + p[2][2][0])
    p[0] = ('Expr', p[1:], ic)

def p_Expr_3(p):
    '''
    Expr : NUMBER
         | LPAREN Expr RPAREN
    '''
    if len(p) == 2:
        ic = [str(p[1]), 'int']
    else:
        ic = p[2][2]
    p[0] = ('Expr', p[1:], ic)


def p_Expr_4(p):
    'Expr : CallExpr'
    ic = p[1][2]
    p[0] = ('Expr', p[1:], ic)


def p_Expr_5(p):
    'Expr : ID'
    ic = [p[1]]
    var = scope_st.find(ic[0], 'Var')
    # 查找id
    if var is False:
        error(2, ic[0])
        ic.append('int')
        # 缺省的变量以及缺省变量类型
        print('skip_by[' + ic[1] + ' ' + ic[0] + ';] ')
        # 缺省的变量入域
        scope_st.top()[ic[0]] = ('Var', 'int', 0)
    else:
        ic.append(var[1])
    p[0] = ('Expr', p[1:], ic)

# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")

# Build the parser
parse = yacc.yacc(debug=True)

def parser(p):
    return parse.parse(p)
