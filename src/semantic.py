"""
FunLang - Analizador Semántico
Incluye tabla de símbolos y verificación de tipos
"""

from typing import Dict, List, Optional, Set, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum
from .ast_nodes import *


# ============================================================================
# TABLA DE SÍMBOLOS
# ============================================================================

@dataclass
class Symbol:
    """Representa un símbolo en la tabla de símbolos"""
    name: str
    symbol_type: TypeNode
    kind: str  # 'variable', 'function', 'parameter', 'type', 'constructor'
    is_mutable: bool = False
    scope_level: int = 0
    lineno: int = 0
    value: Any = None  # Para constantes
    params: List['Symbol'] = field(default_factory=list)  # Para funciones


class SymbolTable:
    """Tabla de símbolos con manejo de scopes"""
    
    def __init__(self):
        self.scopes: List[Dict[str, Symbol]] = [{}]
        self.current_scope = 0
        self.type_registry: Dict[str, TypeNode] = {}
        self._init_builtins()
    
    def _init_builtins(self):
        """Inicializa funciones y tipos built-in"""
        # Tipos básicos
        self.type_registry['Int'] = TypeNode(kind=TypeKind.INT)
        self.type_registry['Float'] = TypeNode(kind=TypeKind.FLOAT)
        self.type_registry['Double'] = TypeNode(kind=TypeKind.DOUBLE)
        self.type_registry['Bool'] = TypeNode(kind=TypeKind.BOOL)
        self.type_registry['Char'] = TypeNode(kind=TypeKind.CHAR)
        self.type_registry['String'] = TypeNode(kind=TypeKind.STRING)
        self.type_registry['Void'] = TypeNode(kind=TypeKind.VOID)
        
        # Funciones built-in
        builtins = [
            # I/O
            ('print', TypeNode(kind=TypeKind.FUNCTION), 'function'),
            ('println', TypeNode(kind=TypeKind.FUNCTION), 'function'),
            ('read', TypeNode(kind=TypeKind.FUNCTION), 'function'),
            ('readLine', TypeNode(kind=TypeKind.FUNCTION), 'function'),
            ('readInt', TypeNode(kind=TypeKind.FUNCTION), 'function'),
            ('readFloat', TypeNode(kind=TypeKind.FUNCTION), 'function'),
            
            # Matemáticas
            ('abs', TypeNode(kind=TypeKind.FUNCTION), 'function'),
            ('sqrt', TypeNode(kind=TypeKind.FUNCTION), 'function'),
            ('sin', TypeNode(kind=TypeKind.FUNCTION), 'function'),
            ('cos', TypeNode(kind=TypeKind.FUNCTION), 'function'),
            ('tan', TypeNode(kind=TypeKind.FUNCTION), 'function'),
            ('log', TypeNode(kind=TypeKind.FUNCTION), 'function'),
            ('exp', TypeNode(kind=TypeKind.FUNCTION), 'function'),
            ('floor', TypeNode(kind=TypeKind.FUNCTION), 'function'),
            ('ceil', TypeNode(kind=TypeKind.FUNCTION), 'function'),
            ('round', TypeNode(kind=TypeKind.FUNCTION), 'function'),
            ('pow', TypeNode(kind=TypeKind.FUNCTION), 'function'),
            ('min', TypeNode(kind=TypeKind.FUNCTION), 'function'),
            ('max', TypeNode(kind=TypeKind.FUNCTION), 'function'),
            
            # Conversiones
            ('toInt', TypeNode(kind=TypeKind.FUNCTION), 'function'),
            ('toFloat', TypeNode(kind=TypeKind.FUNCTION), 'function'),
            ('toDouble', TypeNode(kind=TypeKind.FUNCTION), 'function'),
            ('toString', TypeNode(kind=TypeKind.FUNCTION), 'function'),
            ('toChar', TypeNode(kind=TypeKind.FUNCTION), 'function'),
            
            # Listas
            ('length', TypeNode(kind=TypeKind.FUNCTION), 'function'),
            ('head', TypeNode(kind=TypeKind.FUNCTION), 'function'),
            ('tail', TypeNode(kind=TypeKind.FUNCTION), 'function'),
            ('init', TypeNode(kind=TypeKind.FUNCTION), 'function'),
            ('last', TypeNode(kind=TypeKind.FUNCTION), 'function'),
            ('take', TypeNode(kind=TypeKind.FUNCTION), 'function'),
            ('drop', TypeNode(kind=TypeKind.FUNCTION), 'function'),
            ('reverse', TypeNode(kind=TypeKind.FUNCTION), 'function'),
            ('concat', TypeNode(kind=TypeKind.FUNCTION), 'function'),
            ('map', TypeNode(kind=TypeKind.FUNCTION), 'function'),
            ('filter', TypeNode(kind=TypeKind.FUNCTION), 'function'),
            ('foldl', TypeNode(kind=TypeKind.FUNCTION), 'function'),
            ('foldr', TypeNode(kind=TypeKind.FUNCTION), 'function'),
            ('sum', TypeNode(kind=TypeKind.FUNCTION), 'function'),
            ('product', TypeNode(kind=TypeKind.FUNCTION), 'function'),
            ('elem', TypeNode(kind=TypeKind.FUNCTION), 'function'),
            ('zip', TypeNode(kind=TypeKind.FUNCTION), 'function'),
            ('enumerate', TypeNode(kind=TypeKind.FUNCTION), 'function'),
            
            # Arreglos y Matrices
            ('arrayNew', TypeNode(kind=TypeKind.FUNCTION), 'function'),
            ('arrayGet', TypeNode(kind=TypeKind.FUNCTION), 'function'),
            ('arraySet', TypeNode(kind=TypeKind.FUNCTION), 'function'),
            ('arrayLength', TypeNode(kind=TypeKind.FUNCTION), 'function'),
            ('matrixNew', TypeNode(kind=TypeKind.FUNCTION), 'function'),
            ('matrixGet', TypeNode(kind=TypeKind.FUNCTION), 'function'),
            ('matrixSet', TypeNode(kind=TypeKind.FUNCTION), 'function'),
            ('matrixRows', TypeNode(kind=TypeKind.FUNCTION), 'function'),
            ('matrixCols', TypeNode(kind=TypeKind.FUNCTION), 'function'),
        ]
        
        for name, sym_type, kind in builtins:
            self.define(Symbol(name=name, symbol_type=sym_type, kind=kind, scope_level=0))
    
    def enter_scope(self):
        """Entra a un nuevo scope"""
        self.current_scope += 1
        self.scopes.append({})
    
    def exit_scope(self):
        """Sale del scope actual"""
        if self.current_scope > 0:
            self.scopes.pop()
            self.current_scope -= 1
    
    def define(self, symbol: Symbol) -> bool:
        """Define un nuevo símbolo en el scope actual"""
        if symbol.name in self.scopes[self.current_scope]:
            return False  # Ya existe en el scope actual
        symbol.scope_level = self.current_scope
        self.scopes[self.current_scope][symbol.name] = symbol
        return True
    
    def lookup(self, name: str) -> Optional[Symbol]:
        """Busca un símbolo en todos los scopes"""
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        return None
    
    def lookup_current(self, name: str) -> Optional[Symbol]:
        """Busca un símbolo solo en el scope actual"""
        return self.scopes[self.current_scope].get(name)
    
    def update(self, name: str, value: Any) -> bool:
        """Actualiza el valor de un símbolo"""
        for scope in reversed(self.scopes):
            if name in scope:
                scope[name].value = value
                return True
        return False
    
    def register_type(self, name: str, type_node: TypeNode):
        """Registra un tipo definido por el usuario"""
        self.type_registry[name] = type_node
    
    def get_type(self, name: str) -> Optional[TypeNode]:
        """Obtiene un tipo registrado"""
        return self.type_registry.get(name)


# ============================================================================
# ERRORES SEMÁNTICOS
# ============================================================================

@dataclass
class SemanticError:
    """Representa un error semántico"""
    message: str
    lineno: int
    column: int = 0
    severity: str = "error"  # "error", "warning"
    
    def __str__(self):
        return f"[{self.severity.upper()}] Línea {self.lineno}: {self.message}"


# ============================================================================
# ANALIZADOR SEMÁNTICO
# ============================================================================

class SemanticAnalyzer(ASTVisitor):
    """Analizador semántico para FunLang"""
    
    def __init__(self):
        self.symbol_table = SymbolTable()
        self.errors: List[SemanticError] = []
        self.warnings: List[SemanticError] = []
        self.current_function: Optional[str] = None
        self.function_signatures: Dict[str, TypeNode] = {}
    
    def analyze(self, ast: Program) -> Tuple[bool, List[SemanticError]]:
        """Analiza el AST y retorna si es válido"""
        self.errors = []
        self.warnings = []
        
        # Primera pasada: recoger firmas de tipo
        self._collect_signatures(ast)
        
        # Segunda pasada: análisis completo
        self.visit(ast)
        
        return len(self.errors) == 0, self.errors + self.warnings
    
    def _collect_signatures(self, ast: Program):
        """Recoge las firmas de tipo de las funciones"""
        for decl in ast.declarations:
            if isinstance(decl, TypeSignature):
                self.function_signatures[decl.name] = decl.type_expr
    
    def error(self, message: str, node: ASTNode):
        """Registra un error semántico"""
        self.errors.append(SemanticError(
            message=message,
            lineno=node.lineno if hasattr(node, 'lineno') else 0,
            severity="error"
        ))
    
    def warning(self, message: str, node: ASTNode):
        """Registra una advertencia"""
        self.warnings.append(SemanticError(
            message=message,
            lineno=node.lineno if hasattr(node, 'lineno') else 0,
            severity="warning"
        ))
    
    # ========================================================================
    # VISITORS
    # ========================================================================
    
    def visit_Program(self, node: Program):
        """Visita el programa principal"""
        for imp in node.imports:
            self.visit(imp)
        
        for decl in node.declarations:
            self.visit(decl)
        
        # Verificar que existe main
        main = self.symbol_table.lookup('main')
        if not main:
            self.warning("No se encontró la función 'main'", node)
    
    def visit_Import(self, node: Import):
        """Visita una declaración de importación"""
        # Por ahora solo registramos el módulo
        pass
    
    def visit_TypeSignature(self, node: TypeSignature):
        """Visita una firma de tipo"""
        # Las firmas se procesan en _collect_signatures
        pass
    
    def visit_FunctionDecl(self, node: FunctionDecl):
        """Visita una declaración de función"""
        # Obtener tipo de la firma si existe
        func_type = self.function_signatures.get(node.name, TypeNode(kind=TypeKind.INFERRED))
        
        # Verificar si ya existe
        existing = self.symbol_table.lookup_current(node.name)
        if existing and existing.kind == 'function':
            # Podría ser una definición múltiple (pattern matching)
            pass
        else:
            # Definir la función
            symbol = Symbol(
                name=node.name,
                symbol_type=func_type,
                kind='function',
                lineno=node.lineno
            )
            if not self.symbol_table.define(symbol):
                self.error(f"Función '{node.name}' ya definida en este scope", node)
        
        # Entrar al scope de la función
        self.symbol_table.enter_scope()
        self.current_function = node.name
        
        # Procesar parámetros
        for param in node.params:
            self._process_pattern(param)
        
        # Procesar cuerpo o guardas
        if node.body:
            result_type = self.visit(node.body)
        elif node.guards:
            for guard in node.guards:
                self.visit(guard)
        
        # Salir del scope
        self.current_function = None
        self.symbol_table.exit_scope()
    
    def _process_pattern(self, pattern: Pattern):
        """Procesa un patrón y define variables"""
        if isinstance(pattern, VarPattern):
            symbol = Symbol(
                name=pattern.name,
                symbol_type=TypeNode(kind=TypeKind.INFERRED),
                kind='parameter',
                lineno=pattern.lineno
            )
            self.symbol_table.define(symbol)
        elif isinstance(pattern, ConsPattern):
            self._process_pattern(pattern.head)
            self._process_pattern(pattern.tail)
        elif isinstance(pattern, ListPattern):
            for elem in pattern.elements:
                self._process_pattern(elem)
        elif isinstance(pattern, TuplePattern):
            for elem in pattern.elements:
                self._process_pattern(elem)
    
    def visit_GuardedExpr(self, node: GuardedExpr):
        """Visita una expresión con guarda"""
        guard_type = self.visit(node.guard)
        if guard_type and guard_type.kind != TypeKind.BOOL:
            self.error("La guarda debe ser de tipo Bool", node)
        return self.visit(node.body)
    
    def visit_VarDecl(self, node: VarDecl):
        """Visita una declaración de variable"""
        # Verificar el valor
        value_type = self.visit(node.value)
        
        # Determinar el tipo
        if node.var_type:
            var_type = node.var_type
            # Verificar compatibilidad
            if value_type and not self._types_compatible(var_type, value_type):
                self.error(f"Tipo incompatible: se esperaba {var_type} pero se obtuvo {value_type}", node)
        else:
            var_type = value_type or TypeNode(kind=TypeKind.INFERRED)
        
        # Definir la variable
        symbol = Symbol(
            name=node.name,
            symbol_type=var_type,
            kind='variable',
            is_mutable=node.is_mutable,
            lineno=node.lineno
        )
        
        if not self.symbol_table.define(symbol):
            self.error(f"Variable '{node.name}' ya definida en este scope", node)
    
    def visit_ConstDecl(self, node: ConstDecl):
        """Visita una declaración de constante"""
        value_type = self.visit(node.value)
        
        if node.const_type:
            const_type = node.const_type
        else:
            const_type = value_type or TypeNode(kind=TypeKind.INFERRED)
        
        symbol = Symbol(
            name=node.name,
            symbol_type=const_type,
            kind='variable',
            is_mutable=False,
            lineno=node.lineno
        )
        
        if not self.symbol_table.define(symbol):
            self.error(f"Constante '{node.name}' ya definida en este scope", node)
    
    def visit_TypeDecl(self, node: TypeDecl):
        """Visita una declaración de tipo"""
        self.symbol_table.register_type(node.name, node.body)
    
    def visit_DataDecl(self, node: DataDecl):
        """Visita una declaración de tipo de dato algebraico"""
        # Registrar el tipo
        data_type = TypeNode(kind=TypeKind.CUSTOM, name=node.name)
        self.symbol_table.register_type(node.name, data_type)
        
        # Registrar constructores
        for constr in node.constructors:
            symbol = Symbol(
                name=constr.name,
                symbol_type=data_type,
                kind='constructor',
                lineno=node.lineno
            )
            self.symbol_table.define(symbol)
    
    def visit_IfExpr(self, node: IfExpr) -> Optional[TypeNode]:
        """Visita una expresión if"""
        cond_type = self.visit(node.condition)
        if cond_type and cond_type.kind != TypeKind.BOOL:
            self.error("La condición del if debe ser de tipo Bool", node)
        
        then_type = self.visit(node.then_branch)
        else_type = self.visit(node.else_branch)
        
        # Las ramas deben tener tipos compatibles
        if then_type and else_type and not self._types_compatible(then_type, else_type):
            self.warning("Las ramas del if tienen tipos diferentes", node)
        
        return then_type or else_type
    
    def visit_LetExpr(self, node: LetExpr) -> Optional[TypeNode]:
        """Visita una expresión let"""
        self.symbol_table.enter_scope()
        
        for binding in node.bindings:
            value_type = self.visit(binding.value)
            symbol = Symbol(
                name=binding.name,
                symbol_type=value_type or TypeNode(kind=TypeKind.INFERRED),
                kind='variable',
                is_mutable=False,
                lineno=binding.lineno
            )
            self.symbol_table.define(symbol)
        
        result_type = self.visit(node.body)
        self.symbol_table.exit_scope()
        return result_type
    
    def visit_CaseExpr(self, node: CaseExpr) -> Optional[TypeNode]:
        """Visita una expresión case"""
        expr_type = self.visit(node.expr)
        
        result_type = None
        for alt in node.alternatives:
            self.symbol_table.enter_scope()
            self._process_pattern(alt.pattern)
            alt_type = self.visit(alt.body)
            if result_type is None:
                result_type = alt_type
            self.symbol_table.exit_scope()
        
        return result_type
    
    def visit_LambdaExpr(self, node: LambdaExpr) -> Optional[TypeNode]:
        """Visita una expresión lambda"""
        self.symbol_table.enter_scope()
        
        for param in node.params:
            self._process_pattern(param)
        
        body_type = self.visit(node.body)
        self.symbol_table.exit_scope()
        
        return TypeNode(kind=TypeKind.FUNCTION)
    
    def visit_WhileExpr(self, node: WhileExpr) -> Optional[TypeNode]:
        """Visita una expresión while"""
        cond_type = self.visit(node.condition)
        if cond_type and cond_type.kind != TypeKind.BOOL:
            self.error("La condición del while debe ser de tipo Bool", node)
        
        self.symbol_table.enter_scope()
        self.visit(node.body)
        self.symbol_table.exit_scope()
        
        return TypeNode(kind=TypeKind.VOID)
    
    def visit_ForExpr(self, node: ForExpr) -> Optional[TypeNode]:
        """Visita una expresión for"""
        self.symbol_table.enter_scope()
        
        # Definir variable de iteración
        symbol = Symbol(
            name=node.var,
            symbol_type=TypeNode(kind=TypeKind.INT),
            kind='variable',
            lineno=node.lineno
        )
        self.symbol_table.define(symbol)
        
        if node.start:
            self.visit(node.start)
        if node.end:
            self.visit(node.end)
        if node.collection:
            self.visit(node.collection)
        
        self.visit(node.body)
        self.symbol_table.exit_scope()
        
        return TypeNode(kind=TypeKind.VOID)
    
    def visit_DoBlock(self, node: DoBlock) -> Optional[TypeNode]:
        """Visita un bloque do"""
        self.symbol_table.enter_scope()
        
        result_type = None
        for stmt in node.statements:
            result_type = self.visit(stmt)
        
        self.symbol_table.exit_scope()
        return result_type
    
    def visit_DoExprStmt(self, node: DoExprStmt) -> Optional[TypeNode]:
        return self.visit(node.expr)
    
    def visit_DoBindStmt(self, node: DoBindStmt) -> Optional[TypeNode]:
        expr_type = self.visit(node.expr)
        symbol = Symbol(
            name=node.name,
            symbol_type=expr_type or TypeNode(kind=TypeKind.INFERRED),
            kind='variable',
            lineno=node.lineno
        )
        self.symbol_table.define(symbol)
        return expr_type
    
    def visit_DoLetStmt(self, node: DoLetStmt) -> Optional[TypeNode]:
        expr_type = self.visit(node.expr)
        symbol = Symbol(
            name=node.name,
            symbol_type=expr_type or TypeNode(kind=TypeKind.INFERRED),
            kind='variable',
            lineno=node.lineno
        )
        self.symbol_table.define(symbol)
        return expr_type
    
    def visit_DoReturnStmt(self, node: DoReturnStmt) -> Optional[TypeNode]:
        return self.visit(node.expr)
    
    def visit_BinaryExpr(self, node: BinaryExpr) -> Optional[TypeNode]:
        """Visita una expresión binaria"""
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)
        
        # Determinar el tipo resultado según el operador
        if node.op in (BinaryOp.ADD, BinaryOp.SUB, BinaryOp.MUL, BinaryOp.DIV, BinaryOp.POW):
            # Operadores aritméticos
            if left_type and right_type:
                if left_type.kind == TypeKind.FLOAT or right_type.kind == TypeKind.FLOAT:
                    return TypeNode(kind=TypeKind.FLOAT)
                elif left_type.kind == TypeKind.DOUBLE or right_type.kind == TypeKind.DOUBLE:
                    return TypeNode(kind=TypeKind.DOUBLE)
            return TypeNode(kind=TypeKind.INT)
        
        elif node.op == BinaryOp.MOD:
            return TypeNode(kind=TypeKind.INT)
        
        elif node.op in (BinaryOp.EQ, BinaryOp.NEQ, BinaryOp.LT, BinaryOp.GT, BinaryOp.LE, BinaryOp.GE):
            return TypeNode(kind=TypeKind.BOOL)
        
        elif node.op in (BinaryOp.AND, BinaryOp.OR):
            if left_type and left_type.kind != TypeKind.BOOL:
                self.error("Operando izquierdo de operador lógico debe ser Bool", node)
            if right_type and right_type.kind != TypeKind.BOOL:
                self.error("Operando derecho de operador lógico debe ser Bool", node)
            return TypeNode(kind=TypeKind.BOOL)
        
        elif node.op == BinaryOp.CONS:
            return TypeNode(kind=TypeKind.ARRAY, params=[left_type] if left_type else [])
        
        return TypeNode(kind=TypeKind.INFERRED)
    
    def visit_UnaryExpr(self, node: UnaryExpr) -> Optional[TypeNode]:
        """Visita una expresión unaria"""
        operand_type = self.visit(node.operand)
        
        if node.op == UnaryOp.NEG:
            return operand_type
        elif node.op == UnaryOp.NOT:
            if operand_type and operand_type.kind != TypeKind.BOOL:
                self.error("Operando de 'not' debe ser Bool", node)
            return TypeNode(kind=TypeKind.BOOL)
        
        return operand_type
    
    def visit_FunctionCall(self, node: FunctionCall) -> Optional[TypeNode]:
        """Visita una llamada a función"""
        func_type = self.visit(node.func)
        
        # Verificar argumentos
        for arg in node.args:
            self.visit(arg)
        
        # El tipo de retorno depende de la función
        if isinstance(node.func, Identifier):
            symbol = self.symbol_table.lookup(node.func.name)
            if symbol and isinstance(symbol.symbol_type, FunctionType):
                return symbol.symbol_type.return_type
        
        return TypeNode(kind=TypeKind.INFERRED)
    
    def visit_IndexExpr(self, node: IndexExpr) -> Optional[TypeNode]:
        """Visita un acceso por índice"""
        array_type = self.visit(node.array)
        index_type = self.visit(node.index)
        
        if index_type and index_type.kind != TypeKind.INT:
            self.error("El índice debe ser de tipo Int", node)
        
        if array_type and array_type.kind == TypeKind.ARRAY and array_type.params:
            return array_type.params[0]
        
        return TypeNode(kind=TypeKind.INFERRED)
    
    def visit_MatrixIndexExpr(self, node: MatrixIndexExpr) -> Optional[TypeNode]:
        """Visita un acceso a matriz"""
        self.visit(node.matrix)
        row_type = self.visit(node.row)
        col_type = self.visit(node.col)
        
        if row_type and row_type.kind != TypeKind.INT:
            self.error("El índice de fila debe ser de tipo Int", node)
        if col_type and col_type.kind != TypeKind.INT:
            self.error("El índice de columna debe ser de tipo Int", node)
        
        return TypeNode(kind=TypeKind.INFERRED)
    
    def visit_Identifier(self, node: Identifier) -> Optional[TypeNode]:
        """Visita un identificador"""
        symbol = self.symbol_table.lookup(node.name)
        if symbol is None:
            self.error(f"Identificador '{node.name}' no definido", node)
            return None
        return symbol.symbol_type
    
    def visit_Constructor(self, node: Constructor) -> Optional[TypeNode]:
        """Visita un constructor"""
        symbol = self.symbol_table.lookup(node.name)
        if symbol is None:
            self.error(f"Constructor '{node.name}' no definido", node)
            return None
        return symbol.symbol_type
    
    def visit_IntLiteral(self, node: IntLiteral) -> TypeNode:
        return TypeNode(kind=TypeKind.INT)
    
    def visit_FloatLiteral(self, node: FloatLiteral) -> TypeNode:
        return TypeNode(kind=TypeKind.FLOAT)
    
    def visit_BoolLiteral(self, node: BoolLiteral) -> TypeNode:
        return TypeNode(kind=TypeKind.BOOL)
    
    def visit_CharLiteral(self, node: CharLiteral) -> TypeNode:
        return TypeNode(kind=TypeKind.CHAR)
    
    def visit_StringLiteral(self, node: StringLiteral) -> TypeNode:
        return TypeNode(kind=TypeKind.STRING)
    
    def visit_ListExpr(self, node: ListExpr) -> TypeNode:
        elem_type = None
        for elem in node.elements:
            t = self.visit(elem)
            if elem_type is None:
                elem_type = t
        return TypeNode(kind=TypeKind.ARRAY, params=[elem_type] if elem_type else [])
    
    def visit_ArrayExpr(self, node: ArrayExpr) -> TypeNode:
        elem_type = None
        for elem in node.elements:
            t = self.visit(elem)
            if elem_type is None:
                elem_type = t
        return TypeNode(kind=TypeKind.ARRAY, params=[elem_type] if elem_type else [])
    
    def visit_MatrixExpr(self, node: MatrixExpr) -> TypeNode:
        for row in node.rows:
            for elem in row:
                self.visit(elem)
        return TypeNode(kind=TypeKind.MATRIX)
    
    def visit_TupleExpr(self, node: TupleExpr) -> TypeNode:
        elem_types = [self.visit(elem) for elem in node.elements]
        return TypeNode(kind=TypeKind.CUSTOM, name="Tuple", params=elem_types)
    
    def visit_RangeExpr(self, node: RangeExpr) -> TypeNode:
        self.visit(node.start)
        self.visit(node.end)
        if node.step:
            self.visit(node.step)
        return TypeNode(kind=TypeKind.ARRAY, params=[TypeNode(kind=TypeKind.INT)])
    
    def visit_ListComprehension(self, node: ListComprehension) -> TypeNode:
        self.symbol_table.enter_scope()
        
        for qual in node.qualifiers:
            if isinstance(qual, GeneratorQual):
                self.visit(qual.expr)
                symbol = Symbol(
                    name=qual.var,
                    symbol_type=TypeNode(kind=TypeKind.INFERRED),
                    kind='variable',
                    lineno=qual.lineno
                )
                self.symbol_table.define(symbol)
            elif isinstance(qual, FilterQual):
                filter_type = self.visit(qual.condition)
                if filter_type and filter_type.kind != TypeKind.BOOL:
                    self.error("El filtro debe ser de tipo Bool", qual)
        
        elem_type = self.visit(node.expr)
        self.symbol_table.exit_scope()
        
        return TypeNode(kind=TypeKind.ARRAY, params=[elem_type] if elem_type else [])
    
    def generic_visit(self, node: ASTNode):
        """Visita genérica para nodos no manejados"""
        return None
    
    # ========================================================================
    # UTILIDADES
    # ========================================================================
    
    def _types_compatible(self, t1: TypeNode, t2: TypeNode) -> bool:
        """Verifica si dos tipos son compatibles"""
        if t1 is None or t2 is None:
            return True
        if t1.kind == TypeKind.INFERRED or t2.kind == TypeKind.INFERRED:
            return True
        if t1.kind != t2.kind:
            # Permitir promoción numérica
            numeric = {TypeKind.INT, TypeKind.FLOAT, TypeKind.DOUBLE}
            if t1.kind in numeric and t2.kind in numeric:
                return True
            return False
        return True


def create_analyzer():
    """Factory function para crear un analizador semántico"""
    return SemanticAnalyzer()
