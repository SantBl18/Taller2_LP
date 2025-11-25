"""
FunLang - Nodos del Árbol de Sintaxis Abstracta (AST)
Definición simplificada de nodos para el lenguaje
"""

from dataclasses import dataclass, field
from typing import List, Optional, Any
from enum import Enum, auto


# ============================================================================
# ENUMERACIONES
# ============================================================================

class BinaryOp(Enum):
    """Operadores binarios"""
    ADD = auto()   # +
    SUB = auto()   # -
    MUL = auto()   # *
    DIV = auto()   # /
    MOD = auto()   # %
    EQ = auto()    # ==
    NEQ = auto()   # !=
    LT = auto()    # <
    GT = auto()    # >
    LE = auto()    # <=
    GE = auto()    # >=
    AND = auto()   # &&
    OR = auto()    # ||


class UnaryOp(Enum):
    """Operadores unarios"""
    NEG = auto()   # -
    NOT = auto()   # !


# ============================================================================
# CLASE BASE
# ============================================================================

@dataclass
class ASTNode:
    """Clase base para todos los nodos del AST"""
    line: int = 0
    column: int = 0


# ============================================================================
# PROGRAMA Y DECLARACIONES
# ============================================================================

@dataclass
class Program(ASTNode):
    """Nodo raíz del programa"""
    declarations: List['Declaration'] = field(default_factory=list)


@dataclass
class FunctionDecl(ASTNode):
    """Declaración de función"""
    name: str = ""
    params: List[str] = field(default_factory=list)
    body: Optional['Expression'] = None


@dataclass
class VarDecl(ASTNode):
    """Declaración de variable con let (global)"""
    name: str = ""
    value: Optional['Expression'] = None


# ============================================================================
# EXPRESIONES
# ============================================================================

@dataclass
class IfExpr(ASTNode):
    """Expresión if-then-else"""
    condition: 'Expression' = None
    then_branch: 'Expression' = None
    else_branch: 'Expression' = None


@dataclass
class DoBlock(ASTNode):
    """Bloque do...end"""
    statements: List['Statement'] = field(default_factory=list)


@dataclass
class LetStmt(ASTNode):
    """Declaración let dentro de do"""
    name: str = ""
    value: 'Expression' = None


@dataclass
class ExprStmt(ASTNode):
    """Expresión como statement"""
    expr: 'Expression' = None


@dataclass
class ReturnStmt(ASTNode):
    """Statement return"""
    value: 'Expression' = None


@dataclass
class BinaryExpr(ASTNode):
    """Expresión binaria"""
    op: BinaryOp = None
    left: 'Expression' = None
    right: 'Expression' = None


@dataclass
class UnaryExpr(ASTNode):
    """Expresión unaria"""
    op: UnaryOp = None
    operand: 'Expression' = None


@dataclass
class FunctionCall(ASTNode):
    """Llamada a función"""
    name: str = ""
    args: List['Expression'] = field(default_factory=list)


@dataclass
class Identifier(ASTNode):
    """Identificador/variable"""
    name: str = ""


@dataclass
class IntLiteral(ASTNode):
    """Literal entero"""
    value: int = 0


@dataclass
class FloatLiteral(ASTNode):
    """Literal flotante"""
    value: float = 0.0


@dataclass
class BoolLiteral(ASTNode):
    """Literal booleano"""
    value: bool = False


@dataclass
class StringLiteral(ASTNode):
    """Literal string"""
    value: str = ""


@dataclass
class RangeExpr(ASTNode):
    """Expresión de rango [a..b]"""
    start: 'Expression' = None
    end: 'Expression' = None


# ============================================================================
# TIPOS ALIAS
# ============================================================================

Expression = Any
Statement = Any
Declaration = Any


# ============================================================================
# VISITOR PATTERN (SIMPLIFICADO)
# ============================================================================

class ASTVisitor:
    """Visitor base para recorrer el AST"""
    
    def visit(self, node):
        if node is None:
            return None
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.generic_visit)
        return method(node)
    
    def generic_visit(self, node):
        return None


class ASTPrinter(ASTVisitor):
    """Imprime el AST de forma legible"""
    
    def __init__(self):
        self.indent = 0
    
    def _print(self, text):
        print("  " * self.indent + text)
    
    def visit_Program(self, node):
        self._print("Program")
        self.indent += 1
        for decl in node.declarations:
            self.visit(decl)
        self.indent -= 1
    
    def visit_FunctionDecl(self, node):
        self._print(f"FunctionDecl: {node.name}({', '.join(node.params)})")
        if node.body:
            self.indent += 1
            self.visit(node.body)
            self.indent -= 1
    
    def visit_VarDecl(self, node):
        self._print(f"VarDecl: {node.name}")
        if node.value:
            self.indent += 1
            self.visit(node.value)
            self.indent -= 1
    
    def visit_IfExpr(self, node):
        self._print("IfExpr")
        self.indent += 1
        self._print("condition:")
        self.indent += 1
        self.visit(node.condition)
        self.indent -= 1
        self._print("then:")
        self.indent += 1
        self.visit(node.then_branch)
        self.indent -= 1
        self._print("else:")
        self.indent += 1
        self.visit(node.else_branch)
        self.indent -= 1
        self.indent -= 1
    
    def visit_DoBlock(self, node):
        self._print("DoBlock")
        self.indent += 1
        for stmt in node.statements:
            self.visit(stmt)
        self.indent -= 1
    
    def visit_LetStmt(self, node):
        self._print(f"LetStmt: {node.name}")
        self.indent += 1
        self.visit(node.value)
        self.indent -= 1
    
    def visit_ExprStmt(self, node):
        self._print("ExprStmt")
        self.indent += 1
        self.visit(node.expr)
        self.indent -= 1
    
    def visit_ReturnStmt(self, node):
        self._print("ReturnStmt")
        self.indent += 1
        self.visit(node.value)
        self.indent -= 1
    
    def visit_BinaryExpr(self, node):
        self._print(f"BinaryExpr: {node.op.name}")
        self.indent += 1
        self.visit(node.left)
        self.visit(node.right)
        self.indent -= 1
    
    def visit_UnaryExpr(self, node):
        self._print(f"UnaryExpr: {node.op.name}")
        self.indent += 1
        self.visit(node.operand)
        self.indent -= 1
    
    def visit_FunctionCall(self, node):
        self._print(f"FunctionCall: {node.name}")
        self.indent += 1
        for arg in node.args:
            self.visit(arg)
        self.indent -= 1
    
    def visit_Identifier(self, node):
        self._print(f"Identifier: {node.name}")
    
    def visit_IntLiteral(self, node):
        self._print(f"IntLiteral: {node.value}")
    
    def visit_FloatLiteral(self, node):
        self._print(f"FloatLiteral: {node.value}")
    
    def visit_BoolLiteral(self, node):
        self._print(f"BoolLiteral: {node.value}")
    
    def visit_StringLiteral(self, node):
        self._print(f"StringLiteral: \"{node.value}\"")
    
    def visit_RangeExpr(self, node):
        self._print("RangeExpr")
        self.indent += 1
        self.visit(node.start)
        self.visit(node.end)
        self.indent -= 1
