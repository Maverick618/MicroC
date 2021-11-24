> time: 2021/11/22 \
> 短路原则有感而发
```python
    # 致，因前期的工程导致无法实现的《短路原则》
    # Expr : Expr OR Expr
    #      | Expr AND Expr
    # 在归约逻辑运算语句时，产生体中的两个Expr已经打印了中间代码，无法进行短路
    # 要想短路，要将几乎全部Expr运算语句改写
def p_Expr_3(p):   
    # 逻辑运算：短路原则
    '''
        Expr : Expr OR Expr
             | Expr AND Expr
    '''
    global temp, l_or_and
    temp_ = 'temp_' + str(temp)
    temp += 1
    ic = [temp_, int]
    if p[2] == '||':
        print('if ' + p[1][2][0] + ' == 0 Goto label_' + str(l_or_and))
        print(temp_ + ' = ' + p[1][2][0])
        print('Goto label_' + str(l_or_and + 1)) # 短路原则的体现

        print('label_' + str(l_or_and) + ':')
        l_or_and += 1
        print(temp_ + ' = ' + p[3][2][0])

        print('label_' + str(l_or_and) + ':')
        l_or_and += 1

    else:
        print('if ' + p[1][2][0] + ' != 0 Goto label_' + str(l_or_and))
        print(temp_ + ' = 0')  # 短路原则的体现
        print('Goto label_' + str(l_or_and + 1))
        print('label_' + str(l_or_and) + ':')
        l_or_and += 1
        print(temp_ + ' = ' + p[3][2][0] + ' != 0')  # 短路原则的体现
        print('label_' + str(l_or_and) + ':')
        l_or_and += 1
    p[0] = ['Expr', p[1:], ic]
```