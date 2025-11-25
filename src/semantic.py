"""
FunLang - Analizador Semántico
Verificación básica de tipos y símbolos
"""

from typing import Dict, Set, Optional
from .ast_nodes import *


class SymbolTable:
    """Tabla de símbolos simple"""
    
    def __init__(self, parent=None):
        self.symbols: Dict[str, str] = {}  # nombre -> tipo
        self.parent = parent
    
    def define(self, name: str, symbol_type: str = "any"):
        """Define un símbolo"""
        self.symbols[name] = symbol_type
    
    def lookup(self, name: str) -> Optional[str]:
        """Busca un símbolo"""
        if name in self.symbols:
            return self.symbols[name]
        if self.parent:
            return self.parent.lookup(name)
        return None
    
    def exists(self, name: str) -> bool:
        """Verifica si existe un símbolo"""
        return self.lookup(name) is not None


class SemanticAnalyzer(ASTVisitor):
    """Analizador semántico básico"""
    
    # Funciones built-in
    BUILTINS = {
        'print', 'println', 'sum', 'product', 'length',
        'sqrt', 'abs', 'pow', 'sin', 'cos', 'tan', 'log', 'exp',
        'floor', 'ceil', 'round', 'min', 'max',
        'head', 'tail', 'take', 'drop', 'reverse', 'concat',
        'readInt', 'readLine', 'readFloat',
        'toInt', 'toFloat', 'toString'
    }
    
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.global_scope = SymbolTable()
        self.current_scope = self.global_scope
        
        # Registrar built-ins
        for fn in self.BUILTINS:
            self.global_scope.define(fn, "builtin")
    
    def analyze(self, ast: Program) -> bool:
        """Analiza el AST"""
        self.errors = []
        self.warnings = []
        self.visit(ast)
        return len(self.errors) == 0
    
    def error(self, message: str, node: ASTNode = None):
        """Registra un error"""
        if node:
            self.errors.append(f"Error: {message} (línea {node.line})")
        else:
            self.errors.append(f"Error: {message}")
    
    def warning(self, message: str):
        """Registra una advertencia"""
        self.warnings.append(f"Advertencia: {message}")
    
    # ========================================================================
    # VISITORS
    # ========================================================================
    
    def visit_Program(self, node: Program):
        # Primera pasada: registrar todas las funciones
        for decl in node.declarations:
            if isinstance(decl, FunctionDecl):
                self.global_scope.define(decl.name, "function")
            elif isinstance(decl, VarDecl):
                self.global_scope.define(decl.name, "variable")
        
        # Segunda pasada: analizar cuerpos
        for decl in node.declarations:
            self.visit(decl)
    
    def visit_FunctionDecl(self, node: FunctionDecl):
        # Crear scope para la función
        func_scope = SymbolTable(self.global_scope)
        
        # Registrar parámetros
        for param in node.params:
            func_scope.define(param, "param")
        
        # Analizar cuerpo
        old_scope = self.current_scope
        self.current_scope = func_scope
        
        if node.body:
            self.visit(node.body)
        
        self.current_scope = old_scope
    
    def visit_VarDecl(self, node: VarDecl):
        if node.value:
            self.visit(node.value)
    
    def visit_IfExpr(self, node: IfExpr):
        self.visit(node.condition)
        self.visit(node.then_branch)
        self.visit(node.else_branch)
    
    def visit_DoBlock(self, node: DoBlock):
        # Crear scope local
        block_scope = SymbolTable(self.current_scope)
        old_scope = self.current_scope
        self.current_scope = block_scope
        
        for stmt in node.statements:
            self.visit(stmt)
        
        self.current_scope = old_scope
    
    def visit_LetStmt(self, node: LetStmt):
        self.visit(node.value)
        self.current_scope.define(node.name, "variable")
    
    def visit_ExprStmt(self, node: ExprStmt):
        self.visit(node.expr)
    
    def visit_ReturnStmt(self, node: ReturnStmt):
        self.visit(node.value)
    
    def visit_BinaryExpr(self, node: BinaryExpr):
        self.visit(node.left)
        self.visit(node.right)
    
    def visit_UnaryExpr(self, node: UnaryExpr):
        self.visit(node.operand)
    
    def visit_FunctionCall(self, node: FunctionCall):
        # Verificar que la función existe
        if not self.current_scope.exists(node.name):
            self.error(f"Función no definida: '{node.name}'", node)
        
        # Analizar argumentos
        for arg in node.args:
            self.visit(arg)
    
    def visit_Identifier(self, node: Identifier):
        if not self.current_scope.exists(node.name):
            self.error(f"Variable no definida: '{node.name}'", node)
    
    def visit_RangeExpr(self, node: RangeExpr):
        self.visit(node.start)
        self.visit(node.end)
    
    # Literales - no necesitan análisis
    def visit_IntLiteral(self, node): pass
    def visit_FloatLiteral(self, node): pass
    def visit_BoolLiteral(self, node): pass
    def visit_StringLiteral(self, node): pass


def create_analyzer() -> SemanticAnalyzer:
    """Factory function para crear un analizador"""
    return SemanticAnalyzer()
