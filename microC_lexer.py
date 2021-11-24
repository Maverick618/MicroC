# ------------------------------------------------------------
# lexer.py
#
# ------------------------------------------------------------
import ply.lex as lex

reserved = {
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'int': 'INT',
    'void': 'VOID',
    'char' : 'CHAR',
    'break': 'BREAK',
    'continue': 'CONTINUE',
    'return': 'RETURN',
    'print': 'PRINT',
}

# List of token names.   This is always required
tokens = [
     # int const
     'NUMBER',
     # operators
     # 'INC',
     # 'SUB',

     'PLUS',
     'MINUS',
     'TIMES',
     'DIVIDE',
     'LSHIFT',
     'RSHIFT',
     # divided char
     'COMMA',
     'SEMI',
     # compare operators
     'GT',
     'LT',
     'EQ',
     'NE',
     'GE',
     'LE',
     'AND',
     'OR',
     'NOT',

     # assignment
     'ASSIGN',
     # region
     'LBRACE',
     'RBRACE',
     'LPAREN',
     'RPAREN',

     'ID',
     'COMMENT'
    ] + list(reserved.values())

# Regular expression rules for simple tokens
# t_INC = r'[+][+]'
# t_SUB = r'[-][-]'

t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LSHIFT = r'[<][<]'
t_RSHIFT = r'[>][>]'

t_SEMI = r';'
t_COMMA = r','

t_GT = r'>'
t_LT = r'<'
t_EQ = r'=\='
t_NE = r'!\='
t_GE = r'>='
t_LE = r'<='
t_AND = r'[&][&]'
t_OR  = r'[|][|]'
t_NOT = r'[!]'

t_ASSIGN = r'\='

t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_LPAREN = r'\('
t_RPAREN = r'\)'

# t_STRCONST = r'\"([^\\\n]|(\\.))*?\"'

# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t\x0c'

def t_COMMENT(t):
    r'([/][/]([^\n]*))|(/\*(.|\n)*?\*/)'
    t.lexer.lineno += t.value.count('\n')
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')  # Check for reserved words
    return t


# A regular expression rule with some action code
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t


# Define a rule so we can track li ne numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# # Build the lexer
lexer = lex.lex()

# Test it out
# data = '''
# int a, b; # test
# # test
# int main(){
#    a = 1;
#    b = readint();
#    if (!a || b << 1){
#         print(a + b);
#    }
#    print("Hello World!");
#    return 0;
# }
# '''

# Give the lexer some input
# lexer.input(data)

# Tokenize
#
# for tok in lexer:
#     print(tok)

# while True:
#     tok = lexer.token()
#     if not tok:
#         break      # No more input
#     print(tok)
