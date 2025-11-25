"""
FunLang - Generador de Código C++
Genera código C++ ejecutable desde el AST
"""

from typing import List, Set
from .ast_nodes import *


class CppCodeGenerator(ASTVisitor):
    """Genera código C++ desde el AST de FunLang"""
    
    def __init__(self):
        self.functions: List[str] = []
        self.global_vars: List[str] = []
        self.main_code: List[str] = []
        self.includes: Set[str] = {"iostream", "vector", "string", "cmath"}
    
    def generate(self, ast: Program) -> str:
        """Genera código C++ desde el AST"""
        self.functions = []
        self.global_vars = []
        self.main_code = []
        
        self.visit(ast)
        
        return self._build_output()
    
    def _build_output(self) -> str:
        """Construye el código C++ final"""
        lines = []
        
        # Header
        lines.append("// Código generado por FunLang Compiler")
        lines.append("")
        
        # Includes
        for inc in sorted(self.includes):
            lines.append(f"#include <{inc}>")
        lines.append("")
        lines.append("using namespace std;")
        lines.append("")
        
        # Runtime mínimo
        lines.extend(self._generate_runtime())
        lines.append("")
        
        # Variables globales
        if self.global_vars:
            for var in self.global_vars:
                lines.append(var)
            lines.append("")
        
        # Funciones
        if self.functions:
            for func in self.functions:
                lines.append(func)
            lines.append("")
        
        # Main
        lines.append("int main() {")
        for line in self.main_code:
            lines.append("    " + line)
        lines.append("    return 0;")
        lines.append("}")
        
        return "\n".join(lines)
    
    def _generate_runtime(self) -> List[str]:
        """Genera funciones de runtime mínimas"""
        return [
            "// === Runtime ===",
            "template<typename T> void print(const T& x) { cout << x; }",
            "template<typename T> void println(const T& x) { cout << x << endl; }",
            "",
            "vector<int> range(int start, int end) {",
            "    vector<int> result;",
            "    for (int i = start; i <= end; i++) result.push_back(i);",
            "    return result;",
            "}",
            "",
            "template<typename T> T sum(const vector<T>& xs) {",
            "    T result = 0;",
            "    for (const auto& x : xs) result += x;",
            "    return result;",
            "}",
            "",
            "template<typename T> T product(const vector<T>& xs) {",
            "    T result = 1;",
            "    for (const auto& x : xs) result *= x;",
            "    return result;",
            "}",
            "// === Fin Runtime ===",
        ]
    
    # ========================================================================
    # VISITORS
    # ========================================================================
    
    def visit_Program(self, node: Program):
        for decl in node.declarations:
            if isinstance(decl, FunctionDecl):
                if decl.name == "main":
                    self._generate_main(decl)
                else:
                    self._generate_function(decl)
            elif isinstance(decl, VarDecl):
                value = self.visit(decl.value)
                self.global_vars.append(f"auto {decl.name} = {value};")
    
    def _generate_main(self, node: FunctionDecl):
        """Genera el código de main"""
        if isinstance(node.body, DoBlock):
            for stmt in node.body.statements:
                code = self._generate_statement(stmt)
                if code:
                    self.main_code.append(code)
    
    def _generate_function(self, node: FunctionDecl):
        """Genera una función"""
        params = node.params
        is_recursive = self._is_recursive(node.name, node.body)
        
        if params:
            # Template para funciones con parámetros
            tparams = ", ".join([f"typename T{i}" for i in range(len(params))])
            plist = ", ".join([f"T{i} {p}" for i, p in enumerate(params)])
            
            # Tipo de retorno explícito para recursivas
            ret_type = "T0" if is_recursive else "auto"
            
            self.functions.append(f"template<{tparams}>")
            self.functions.append(f"{ret_type} {node.name}({plist}) {{")
        else:
            self.functions.append(f"auto {node.name}() {{")
        
        body = self.visit(node.body)
        self.functions.append(f"    return {body};")
        self.functions.append("}")
        self.functions.append("")
    
    def _is_recursive(self, func_name: str, node) -> bool:
        """Detecta si una función es recursiva"""
        if node is None:
            return False
        if isinstance(node, FunctionCall) and node.name == func_name:
            return True
        if isinstance(node, BinaryExpr):
            return self._is_recursive(func_name, node.left) or self._is_recursive(func_name, node.right)
        if isinstance(node, IfExpr):
            return (self._is_recursive(func_name, node.condition) or
                    self._is_recursive(func_name, node.then_branch) or
                    self._is_recursive(func_name, node.else_branch))
        if isinstance(node, UnaryExpr):
            return self._is_recursive(func_name, node.operand)
        return False
    
    def _generate_statement(self, stmt) -> str:
        """Genera un statement"""
        if isinstance(stmt, LetStmt):
            value = self.visit(stmt.value)
            return f"auto {stmt.name} = {value};"
        elif isinstance(stmt, ExprStmt):
            return self.visit(stmt.expr) + ";"
        elif isinstance(stmt, ReturnStmt):
            return ""  # Ignoramos return en main
        return ""
    
    def visit_IfExpr(self, node: IfExpr) -> str:
        cond = self.visit(node.condition)
        then_code = self.visit(node.then_branch)
        else_code = self.visit(node.else_branch)
        return f"({cond} ? {then_code} : {else_code})"
    
    def visit_DoBlock(self, node: DoBlock) -> str:
        # Para do blocks en expresiones (no main)
        stmts = []
        last = "0"
        for stmt in node.statements:
            if isinstance(stmt, LetStmt):
                value = self.visit(stmt.value)
                stmts.append(f"auto {stmt.name} = {value};")
            elif isinstance(stmt, ExprStmt):
                code = self.visit(stmt.expr)
                stmts.append(f"{code};")
                last = code
            elif isinstance(stmt, ReturnStmt):
                last = self.visit(stmt.value)
        
        stmts_str = " ".join(stmts)
        return f"[&]() {{ {stmts_str} return {last}; }}()"
    
    def visit_BinaryExpr(self, node: BinaryExpr) -> str:
        left = self.visit(node.left)
        right = self.visit(node.right)
        
        op_map = {
            BinaryOp.ADD: "+", BinaryOp.SUB: "-", BinaryOp.MUL: "*",
            BinaryOp.DIV: "/", BinaryOp.MOD: "%",
            BinaryOp.EQ: "==", BinaryOp.NEQ: "!=",
            BinaryOp.LT: "<", BinaryOp.GT: ">",
            BinaryOp.LE: "<=", BinaryOp.GE: ">=",
            BinaryOp.AND: "&&", BinaryOp.OR: "||",
        }
        
        return f"({left} {op_map[node.op]} {right})"
    
    def visit_UnaryExpr(self, node: UnaryExpr) -> str:
        operand = self.visit(node.operand)
        if node.op == UnaryOp.NEG:
            return f"(-{operand})"
        elif node.op == UnaryOp.NOT:
            return f"(!{operand})"
        return operand
    
    def visit_FunctionCall(self, node: FunctionCall) -> str:
        args = ", ".join(self.visit(arg) for arg in node.args)
        return f"{node.name}({args})"
    
    def visit_Identifier(self, node: Identifier) -> str:
        return node.name
    
    def visit_IntLiteral(self, node: IntLiteral) -> str:
        return str(node.value)
    
    def visit_FloatLiteral(self, node: FloatLiteral) -> str:
        return str(node.value)
    
    def visit_BoolLiteral(self, node: BoolLiteral) -> str:
        return "true" if node.value else "false"
    
    def visit_StringLiteral(self, node: StringLiteral) -> str:
        escaped = node.value.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
        return f'"{escaped}"'
    
    def visit_RangeExpr(self, node: RangeExpr) -> str:
        start = self.visit(node.start)
        end = self.visit(node.end)
        return f"range({start}, {end})"


def create_generator() -> CppCodeGenerator:
    """Factory function para crear un generador"""
    return CppCodeGenerator()
