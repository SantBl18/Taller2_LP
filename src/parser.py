"""
FunLang - Analizador Sintáctico
Implementado con PLY (Python Lex-Yacc)
"""

import ply.yacc as yacc
from .lexer import FunLangLexer
from .ast_nodes import *


class FunLangParser:
    """Analizador sintáctico para FunLang"""
    
    def __init__(self):
        self.lexer = FunLangLexer()
        self.lexer.build()
        self.tokens = self.lexer.tokens
        self.parser = None
        self.errors = []
    
    # ========================================================================
    # PRECEDENCIA DE OPERADORES
    # ========================================================================
    
    precedence = (
        ('left', 'OR'),
        ('left', 'AND'),
        ('left', 'EQ', 'NEQ'),
        ('left', 'LT', 'GT', 'LE', 'GE'),
        ('left', 'PLUS', 'MINUS'),
        ('left', 'TIMES', 'DIVIDE', 'MOD'),
        ('right', 'NOT', 'UMINUS'),
    )
    
    # ========================================================================
    # REGLAS GRAMATICALES
    # ========================================================================
    
    def p_program(self, p):
        '''program : declarations'''
        p[0] = Program(declarations=p[1])
    
    def p_declarations(self, p):
        '''declarations : declarations declaration
                        | declaration'''
        if len(p) == 3:
            p[0] = p[1] + [p[2]]
        else:
            p[0] = [p[1]]
    
    def p_declaration(self, p):
        '''declaration : function_decl
                       | var_decl'''
        p[0] = p[1]
    
    # Variable global: let nombre = valor
    def p_var_decl(self, p):
        '''var_decl : LET IDENTIFIER ASSIGN expression'''
        p[0] = VarDecl(name=p[2], value=p[4])
    
    # Función: nombre params = cuerpo
    def p_function_decl(self, p):
        '''function_decl : IDENTIFIER params ASSIGN expression'''
        p[0] = FunctionDecl(name=p[1], params=p[2], body=p[4])
    
    def p_params(self, p):
        '''params : params IDENTIFIER
                  | empty'''
        if len(p) == 3:
            p[0] = p[1] + [p[2]]
        else:
            p[0] = []
    
    # ========================================================================
    # EXPRESIONES
    # ========================================================================
    
    def p_expression(self, p):
        '''expression : if_expr
                      | do_block
                      | or_expr'''
        p[0] = p[1]
    
    # If-then-else
    def p_if_expr(self, p):
        '''if_expr : IF expression THEN expression ELSE expression'''
        p[0] = IfExpr(condition=p[2], then_branch=p[4], else_branch=p[6])
    
    # Bloque do...end
    def p_do_block(self, p):
        '''do_block : DO statements END'''
        p[0] = DoBlock(statements=p[2])
    
    def p_statements(self, p):
        '''statements : statements statement
                      | statement'''
        if len(p) == 3:
            p[0] = p[1] + [p[2]]
        else:
            p[0] = [p[1]]
    
    def p_statement(self, p):
        '''statement : let_stmt
                     | return_stmt
                     | expr_stmt'''
        p[0] = p[1]
    
    def p_let_stmt(self, p):
        '''let_stmt : LET IDENTIFIER ASSIGN expression'''
        p[0] = LetStmt(name=p[2], value=p[4])
    
    def p_return_stmt(self, p):
        '''return_stmt : RETURN expression'''
        p[0] = ReturnStmt(value=p[2])
    
    def p_expr_stmt(self, p):
        '''expr_stmt : or_expr'''
        p[0] = ExprStmt(expr=p[1])
    
    # ========================================================================
    # OPERADORES (por precedencia)
    # ========================================================================
    
    def p_or_expr(self, p):
        '''or_expr : or_expr OR and_expr
                   | and_expr'''
        if len(p) == 4:
            p[0] = BinaryExpr(op=BinaryOp.OR, left=p[1], right=p[3])
        else:
            p[0] = p[1]
    
    def p_and_expr(self, p):
        '''and_expr : and_expr AND comparison
                    | comparison'''
        if len(p) == 4:
            p[0] = BinaryExpr(op=BinaryOp.AND, left=p[1], right=p[3])
        else:
            p[0] = p[1]
    
    def p_comparison(self, p):
        '''comparison : comparison EQ additive
                      | comparison NEQ additive
                      | comparison LT additive
                      | comparison GT additive
                      | comparison LE additive
                      | comparison GE additive
                      | additive'''
        if len(p) == 4:
            ops = {'==': BinaryOp.EQ, '!=': BinaryOp.NEQ, '<': BinaryOp.LT,
                   '>': BinaryOp.GT, '<=': BinaryOp.LE, '>=': BinaryOp.GE}
            p[0] = BinaryExpr(op=ops[p[2]], left=p[1], right=p[3])
        else:
            p[0] = p[1]
    
    def p_additive(self, p):
        '''additive : additive PLUS multiplicative
                    | additive MINUS multiplicative
                    | multiplicative'''
        if len(p) == 4:
            op = BinaryOp.ADD if p[2] == '+' else BinaryOp.SUB
            p[0] = BinaryExpr(op=op, left=p[1], right=p[3])
        else:
            p[0] = p[1]
    
    def p_multiplicative(self, p):
        '''multiplicative : multiplicative TIMES unary
                          | multiplicative DIVIDE unary
                          | multiplicative MOD unary
                          | unary'''
        if len(p) == 4:
            ops = {'*': BinaryOp.MUL, '/': BinaryOp.DIV, '%': BinaryOp.MOD}
            p[0] = BinaryExpr(op=ops[p[2]], left=p[1], right=p[3])
        else:
            p[0] = p[1]
    
    def p_unary(self, p):
        '''unary : MINUS unary %prec UMINUS
                 | NOT unary
                 | call'''
        if len(p) == 3:
            if p[1] == '-':
                p[0] = UnaryExpr(op=UnaryOp.NEG, operand=p[2])
            else:
                p[0] = UnaryExpr(op=UnaryOp.NOT, operand=p[2])
        else:
            p[0] = p[1]
    
    # ========================================================================
    # LLAMADAS Y PRIMARIOS
    # ========================================================================
    
    def p_call(self, p):
        '''call : IDENTIFIER LPAREN args RPAREN
                | primary'''
        if len(p) == 5:
            p[0] = FunctionCall(name=p[1], args=p[3])
        else:
            p[0] = p[1]
    
    def p_args(self, p):
        '''args : arg_list
                | empty'''
        p[0] = p[1] if p[1] else []
    
    def p_arg_list(self, p):
        '''arg_list : arg_list COMMA expression
                    | expression'''
        if len(p) == 4:
            p[0] = p[1] + [p[3]]
        else:
            p[0] = [p[1]]
    
    def p_primary(self, p):
        '''primary : INTEGER
                   | FLOAT
                   | STRING
                   | TRUE
                   | FALSE
                   | IDENTIFIER
                   | range_expr
                   | LPAREN expression RPAREN'''
        if len(p) == 2:
            if isinstance(p[1], int):
                p[0] = IntLiteral(value=p[1])
            elif isinstance(p[1], float):
                p[0] = FloatLiteral(value=p[1])
            elif p[1] == 'True':
                p[0] = BoolLiteral(value=True)
            elif p[1] == 'False':
                p[0] = BoolLiteral(value=False)
            elif isinstance(p[1], str) and p.slice[1].type == 'STRING':
                p[0] = StringLiteral(value=p[1])
            elif isinstance(p[1], str):
                p[0] = Identifier(name=p[1])
            else:
                p[0] = p[1]
        else:
            p[0] = p[2]
    
    # Rango [a..b]
    def p_range_expr(self, p):
        '''range_expr : LBRACKET expression DOTDOT expression RBRACKET'''
        p[0] = RangeExpr(start=p[2], end=p[4])
    
    def p_empty(self, p):
        '''empty :'''
        p[0] = None
    
    def p_error(self, p):
        if p:
            self.errors.append(f"Error de sintaxis en '{p.value}' (línea {p.lineno})")
        else:
            self.errors.append("Error de sintaxis: fin de archivo inesperado")
    
    # ========================================================================
    # MÉTODOS PÚBLICOS
    # ========================================================================
    
    def build(self, **kwargs):
        """Construye el parser"""
        self.parser = yacc.yacc(module=self, **kwargs)
        return self.parser
    
    def parse(self, data: str):
        """Parsea código fuente"""
        self.errors = []
        self.lexer.errors = []
        self.lexer.input(data)
        result = self.parser.parse(lexer=self.lexer.lexer)
        return result


def create_parser() -> FunLangParser:
    """Factory function para crear un parser"""
    parser = FunLangParser()
    parser.build(debug=False, write_tables=False)
    return parser
