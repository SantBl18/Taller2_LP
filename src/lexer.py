"""
FunLang - Analizador Léxico
Implementado con PLY (Python Lex-Yacc)
"""

import ply.lex as lex
from typing import List, Tuple


class FunLangLexer:
    """Analizador léxico para FunLang"""
    
    # Palabras reservadas
    reserved = {
        'if': 'IF',
        'then': 'THEN',
        'else': 'ELSE',
        'let': 'LET',
        'in': 'IN',
        'do': 'DO',
        'end': 'END',
        'return': 'RETURN',
        'True': 'TRUE',
        'False': 'FALSE',
    }
    
    # Lista de tokens
    tokens = [
        # Literales
        'INTEGER',
        'FLOAT',
        'STRING',
        'IDENTIFIER',
        
        # Operadores aritméticos
        'PLUS',
        'MINUS',
        'TIMES',
        'DIVIDE',
        'MOD',
        
        # Operadores de comparación
        'EQ',
        'NEQ',
        'LT',
        'GT',
        'LE',
        'GE',
        
        # Operadores lógicos
        'AND',
        'OR',
        'NOT',
        
        # Delimitadores
        'LPAREN',
        'RPAREN',
        'LBRACKET',
        'RBRACKET',
        'COMMA',
        'ASSIGN',
        'DOTDOT',
    ] + list(reserved.values())
    
    # Reglas de tokens simples
    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_TIMES = r'\*'
    t_DIVIDE = r'/'
    t_MOD = r'%'
    t_EQ = r'=='
    t_NEQ = r'!='
    t_LE = r'<='
    t_GE = r'>='
    t_LT = r'<'
    t_GT = r'>'
    t_AND = r'&&'
    t_OR = r'\|\|'
    t_NOT = r'!'
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_LBRACKET = r'\['
    t_RBRACKET = r'\]'
    t_COMMA = r','
    t_ASSIGN = r'='
    t_DOTDOT = r'\.\.'
    
    # Ignorar espacios y tabs
    t_ignore = ' \t'
    
    def __init__(self):
        self.lexer = None
        self.errors: List[str] = []
        self.lexdata = ""
    
    def t_COMMENT(self, t):
        r'--[^\n]*'
        pass  # Ignorar comentarios
    
    def t_FLOAT(self, t):
        r'\d+\.\d+'
        t.value = float(t.value)
        return t
    
    def t_INTEGER(self, t):
        r'\d+'
        t.value = int(t.value)
        return t
    
    def t_STRING(self, t):
        r'"([^"\\]|\\.)*"'
        t.value = t.value[1:-1]  # Quitar comillas
        return t
    
    def t_IDENTIFIER(self, t):
        r'[a-zA-Z_][a-zA-Z0-9_]*'
        t.type = self.reserved.get(t.value, 'IDENTIFIER')
        return t
    
    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)
    
    def t_error(self, t):
        self.errors.append(f"Carácter ilegal '{t.value[0]}' en línea {t.lineno}")
        t.lexer.skip(1)
    
    def build(self, **kwargs):
        """Construye el lexer"""
        self.lexer = lex.lex(module=self, **kwargs)
        return self.lexer
    
    def input(self, data: str):
        """Proporciona entrada al lexer"""
        self.lexdata = data
        self.lexer.input(data)
    
    def token(self):
        """Obtiene el siguiente token"""
        return self.lexer.token()
    
    def tokenize(self, data: str) -> List[Tuple]:
        """Tokeniza una cadena completa"""
        self.input(data)
        tokens = []
        while True:
            tok = self.token()
            if tok is None:
                break
            tokens.append((tok.type, tok.value, tok.lineno, tok.lexpos))
        return tokens
    
    def find_column(self, token):
        """Encuentra la columna de un token"""
        line_start = self.lexdata.rfind('\n', 0, token.lexpos) + 1
        return (token.lexpos - line_start) + 1


def create_lexer() -> FunLangLexer:
    """Factory function para crear un lexer"""
    lexer = FunLangLexer()
    lexer.build()
    return lexer
