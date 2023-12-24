# Lexer
import ply.lex as lex

tokens = ('VAR', 'IDENTIFIER', 'NUMBER', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'LPAREN', 'RPAREN', 'EQUALS', 'SEMICOLON')

t_VAR = r'var'
t_IDENTIFIER = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_NUMBER = r'\d+'
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_EQUALS = r'='
t_SEMICOLON = r';'

t_ignore = ' \t'

def t_error(t):
    print(f"Illegal character {t.value[0]!r}")
    t.lexer.skip(1)

lexer = lex.lex()

# Parser
import ply.yacc as yacc

def p_program(p):
    '''program : statements'''
    p[0] = p[1]

def p_statements(p):
    '''statements : statement SEMICOLON statements
                  | statement SEMICOLON'''
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = [p[1]]

def p_statement(p):
    '''statement : variable_declaration
                 | assignment
                 | expression'''
    p[0] = p[1]

def p_variable_declaration(p):
    '''variable_declaration : VAR IDENTIFIER'''
    p[0] = ('VAR_DECL', p[2])

def p_assignment(p):
    '''assignment : IDENTIFIER EQUALS expression'''
    p[0] = ('ASSIGN', p[1], p[3])

def p_expression(p):
    '''expression : term
                  | term PLUS term
                  | term MINUS term'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = (p[2], p[1], p[3])

def p_term(p):
    '''term : factor
            | factor TIMES factor
            | factor DIVIDE factor'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = (p[2], p[1], p[3])

def p_factor(p):
    '''factor : NUMBER
              | IDENTIFIER
              | LPAREN expression RPAREN'''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 4:
        p[0] = p[2]

def p_error(p):
    print("Syntax error")

parser = yacc.yacc()

# Semantic Analysis
symbol_table = {}

def check_variable_declaration(identifier):
    if identifier in symbol_table:
        print(f"Error: Variable '{identifier}' already declared.")
        return False
    else:
        symbol_table[identifier] = True
        return True

def check_variable_assignment(identifier):
    if identifier not in symbol_table:
        print(f"Error: Variable '{identifier}' not declared.")
        return False
    else:
        return True

def semantic_analysis(node):
    if isinstance(node, tuple):
        if node[0] == 'VAR_DECL':
            return check_variable_declaration(node[1])
        elif node[0] == 'ASSIGN':
            return check_variable_assignment(node[1])
    elif isinstance(node, list):
        for statement in node:
            if not semantic_analysis(statement):
                return False
    return True

# Test the parser and perform semantic analysis
input_code = "var x; var y; x = 10; y = (x + 5) * 2;"
parsed_result = parser.parse(input_code, lexer=lexer)
if semantic_analysis(parsed_result):
    print("Semantic analysis passed.")
else:
    print("Semantic analysis failed.")
