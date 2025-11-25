# Manual Técnico - FunLang Compiler

## Sistema de Procesamiento del Lenguaje (SPL)

### Taller #2 - Lenguajes de Programación

---

## Tabla de Contenidos

1. [Introducción](#1-introducción)
2. [Arquitectura del Compilador](#2-arquitectura-del-compilador)
3. [Gramática E-BNF](#3-gramática-e-bnf)
4. [Análisis Léxico](#4-análisis-léxico)
5. [Análisis Sintáctico](#5-análisis-sintáctico)
6. [Análisis Semántico](#6-análisis-semántico)
7. [Generación de Código](#7-generación-de-código)
8. [Descripción Semántica de Producciones](#8-descripción-semántica-de-producciones)
9. [Tipos de Datos](#9-tipos-de-datos)
10. [Ejemplos y Pruebas](#10-ejemplos-y-pruebas)
11. [Guía de Uso](#11-guía-de-uso)

---

## 1. Introducción

### 1.1 Descripción del Proyecto

FunLang es un lenguaje de programación con paradigma funcional inspirado en Haskell, que compila a código C++ ejecutable. El compilador implementa un Sistema de Procesamiento del Lenguaje completo incluyendo:

- **Preprocesador**: Manejo de módulos e imports
- **Compilador**: Análisis léxico, sintáctico, semántico y generación de código
- **Enlazador**: El código C++ generado puede ser compilado con g++

### 1.2 Características del Lenguaje

- **Paradigma**: Funcional con soporte imperativo
- **Tipos de datos**: Int, Float, Double, Bool, Char, String, Array, Matrix
- **Estructuras de control**: Secuencia, selección (if-then-else), iteración (for, while)
- **Funciones**: Primera clase, recursión, guardas, pattern matching
- **TDA**: Soporte para tipos de datos algebraicos (data)
- **Aritmética**: Soporte completo de punto flotante

### 1.3 Herramientas Utilizadas

- **Python 3.8+**: Lenguaje de implementación
- **PLY (Python Lex-Yacc)**: Equivalente a Flex/Bison para Python
- **G++**: Compilador de C++ para el código generado

---

## 2. Arquitectura del Compilador

```
┌─────────────────────────────────────────────────────────────┐
│                    CÓDIGO FUENTE (.fun)                      │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                   ANALIZADOR LÉXICO                          │
│                      (lexer.py)                              │
│  - Tokenización                                              │
│  - Reconocimiento de palabras reservadas                     │
│  - Manejo de comentarios                                     │
└─────────────────────────┬───────────────────────────────────┘
                          │ Tokens
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                  ANALIZADOR SINTÁCTICO                       │
│                      (parser.py)                             │
│  - Análisis de gramática libre de contexto                   │
│  - Construcción del AST                                      │
│  - Detección de errores sintácticos                          │
└─────────────────────────┬───────────────────────────────────┘
                          │ AST
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                  ANALIZADOR SEMÁNTICO                        │
│                     (semantic.py)                            │
│  - Tabla de símbolos                                         │
│  - Verificación de tipos                                     │
│  - Detección de variables no declaradas                      │
└─────────────────────────┬───────────────────────────────────┘
                          │ AST anotado
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                  GENERADOR DE CÓDIGO                         │
│                      (codegen.py)                            │
│  - Traducción a C++                                          │
│  - Runtime de FunLang                                        │
│  - Optimizaciones básicas                                    │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                    CÓDIGO C++ (.cpp)                         │
└─────────────────────────┬───────────────────────────────────┘
                          │ g++
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                    EJECUTABLE (.exe)                         │
└─────────────────────────────────────────────────────────────┘
```

### 2.1 Módulos del Sistema

| Módulo | Archivo | Descripción |
|--------|---------|-------------|
| Lexer | `src/lexer.py` | Analizador léxico con PLY Lex |
| Parser | `src/parser.py` | Analizador sintáctico con PLY Yacc |
| AST | `src/ast_nodes.py` | Definición de nodos del árbol sintáctico |
| Semantic | `src/semantic.py` | Analizador semántico y tabla de símbolos |
| Codegen | `src/codegen.py` | Generador de código C++ |
| Compiler | `src/compiler.py` | Integración de todos los módulos |

---

## 3. Gramática E-BNF

La gramática completa está definida en `grammar/funlang.ebnf`. A continuación se presenta un resumen:

### 3.1 Estructura del Programa

```ebnf
Program       ::= ModuleDecl? ImportList? DeclList
ModuleDecl    ::= 'module' IDENTIFIER 'where'
ImportList    ::= Import+
Import        ::= 'import' IDENTIFIER ('as' IDENTIFIER)?
```

### 3.2 Declaraciones

```ebnf
Declaration   ::= FunctionDecl | TypeDecl | VarDecl | ConstDecl | DataDecl

FunctionDecl  ::= FunctionSig? FunctionDef
FunctionSig   ::= IDENTIFIER '::' TypeExpr
FunctionDef   ::= IDENTIFIER ParamList? '=' Expression
                | IDENTIFIER ParamList? GuardedExpr+

VarDecl       ::= 'let' IDENTIFIER (':' TypeExpr)? '=' Expression
                | 'var' IDENTIFIER (':' TypeExpr)? '=' Expression
```

### 3.3 Expresiones

```ebnf
Expression    ::= LetExpr | IfExpr | CaseExpr | LambdaExpr 
                | WhileExpr | ForExpr | DoBlock | LogicalOrExpr

IfExpr        ::= 'if' Expression 'then' Expression 'else' Expression
LambdaExpr    ::= '\' ParamList '->' Expression
DoBlock       ::= 'do' DoStatements 'end'
```

### 3.4 Tipos

```ebnf
TypeExpr      ::= BaseType | TypeExpr '->' TypeExpr | '[' TypeExpr ']'
BaseType      ::= 'Int' | 'Float' | 'Double' | 'Bool' | 'Char' | 'String' | 'Void'
```

---

## 4. Análisis Léxico

### 4.1 Tokens Reconocidos

#### Palabras Reservadas
```
module, where, import, as, let, in, var, const, type, data,
if, then, else, case, of, while, for, do, end, return, fn,
Int, Float, Double, Bool, Char, String, Void, array, matrix,
True, False, and, or, not, mod, div
```

#### Operadores
```
+ - * / % ^ ** == != /= < > <= >= && || ! -> <- :: .. !! : .
```

#### Delimitadores
```
( ) [ ] { } , ; | _ \
```

### 4.2 Expresiones Regulares

| Token | Expresión Regular |
|-------|-------------------|
| IDENTIFIER | `[a-z_][a-zA-Z0-9_']*` |
| CONSTRUCTOR | `[A-Z][a-zA-Z0-9_]*` |
| INTEGER | `[0-9]+` o `0x[0-9a-fA-F]+` o `0b[01]+` |
| FLOAT | `[0-9]+\.[0-9]+([eE][+-]?[0-9]+)?` |
| STRING | `"([^"\\]|\\[ntr\\'"0])*"` |
| CHAR | `'([^'\\]|\\[ntr\\'"0])'` |
| COMMENT | `--[^\n]*` o `{-.*-}` |

---

## 5. Análisis Sintáctico

### 5.1 Precedencia de Operadores

```python
precedence = (
    ('left', 'OR_OP', 'OR'),           # ||, or
    ('left', 'AND_OP', 'AND'),         # &&, and
    ('left', 'NOT_OP', 'NOT'),         # !, not
    ('nonassoc', 'EQ', 'NEQ'),         # ==, !=, /=
    ('nonassoc', 'LT', 'GT', 'LE', 'GE'),  # <, >, <=, >=
    ('right', 'CONS'),                  # :
    ('left', 'PLUS', 'MINUS'),         # +, -
    ('left', 'TIMES', 'DIVIDE', 'MODULO'),  # *, /, %
    ('right', 'POWER'),                 # ^, **
    ('right', 'UMINUS'),               # - unario
)
```

### 5.2 Reglas de Producción Principales

```python
# Programa
def p_program(p):
    '''program : module_decl import_list decl_list
               | decl_list'''

# Función con guardas
def p_function_decl(p):
    '''function_decl : IDENTIFIER param_list ASSIGN expression
                     | IDENTIFIER param_list guarded_exprs'''

# If-Then-Else
def p_if_expr(p):
    '''if_expr : IF expression THEN expression ELSE expression'''

# Lambda
def p_lambda_expr(p):
    '''lambda_expr : BACKSLASH param_list ARROW expression'''
```

---

## 6. Análisis Semántico

### 6.1 Tabla de Símbolos

La tabla de símbolos maneja:
- **Scopes anidados**: Permite variables locales en funciones y bloques
- **Tipos de símbolos**: Variables, funciones, parámetros, tipos, constructores
- **Información de tipo**: Tipo inferido o declarado

```python
@dataclass
class Symbol:
    name: str
    symbol_type: TypeNode
    kind: str  # 'variable', 'function', 'parameter', 'type', 'constructor'
    is_mutable: bool = False
    scope_level: int = 0
```

### 6.2 Verificaciones Semánticas

1. **Variables no declaradas**: Error si se usa una variable sin definir
2. **Tipos incompatibles**: Advertencia si los tipos no coinciden
3. **Redefinición**: Error si se redefine en el mismo scope
4. **Guardas no booleanas**: Error si la condición no es Bool
5. **Función main**: Advertencia si no existe

### 6.3 Funciones Built-in

El analizador reconoce funciones predefinidas:
- I/O: `print`, `println`, `readInt`, `readFloat`, `readLine`
- Matemáticas: `abs`, `sqrt`, `sin`, `cos`, `tan`, `log`, `exp`, `pow`
- Listas: `length`, `head`, `tail`, `take`, `drop`, `map`, `filter`, `foldl`
- Conversiones: `toInt`, `toFloat`, `toString`

---

## 7. Generación de Código

### 7.1 Mapeo de Tipos

| FunLang | C++ |
|---------|-----|
| Int | int |
| Float | double |
| Double | double |
| Bool | bool |
| Char | char |
| String | string |
| [T] | vector<T> |
| Matrix T | vector<vector<T>> |

### 7.2 Traducción de Construcciones

#### If-Then-Else
```haskell
-- FunLang
if x > 0 then x else -x
```
```cpp
// C++
(x > 0 ? x : -x)
```

#### Let-In
```haskell
-- FunLang
let x = 5 in x * 2
```
```cpp
// C++
[&]() { auto x = 5; return x * 2; }()
```

#### Lambda
```haskell
-- FunLang
\x -> x * 2
```
```cpp
// C++
[&](auto x) { return x * 2; }
```

#### Do-Block
```haskell
-- FunLang
do
    let x = 5
    println(x)
    return x
end
```
```cpp
// C++
[&]() {
    auto x = 5;
    println(x);
    return x;
}()
```

---

## 8. Descripción Semántica de Producciones

### 8.1 Program → ModuleDecl? ImportList? DeclList

**Acción Semántica**: 
- Crea el nodo raíz del AST
- Registra el nombre del módulo si existe
- Procesa las importaciones
- Analiza todas las declaraciones

**En C++**: Genera el archivo completo con includes, runtime y función main.

### 8.2 FunctionDecl → IDENTIFIER ParamList '=' Expression

**Acción Semántica**:
- Registra la función en la tabla de símbolos
- Crea nuevo scope para parámetros
- Verifica tipos de parámetros con la firma si existe
- Analiza el cuerpo en el nuevo scope

**En C++**: 
```cpp
auto nombre(auto param1, auto param2) {
    return expresion;
}
```

### 8.3 IfExpr → 'if' Expression 'then' Expression 'else' Expression

**Acción Semántica**:
- Verifica que la condición sea de tipo Bool
- Verifica que ambas ramas tengan tipos compatibles
- Retorna el tipo común de las ramas

**En C++**: Usa el operador ternario `(cond ? then : else)`

### 8.4 GuardedExpr → '|' Expression '=' Expression

**Acción Semántica**:
- Verifica que la guarda sea de tipo Bool
- Asocia la guarda con su expresión resultado

**En C++**: Genera `if (guarda) return expresion;`

### 8.5 LetExpr → 'let' LetBindings 'in' Expression

**Acción Semántica**:
- Crea nuevo scope
- Procesa cada binding secuencialmente
- Evalúa el cuerpo en el scope extendido
- Retorna el tipo del cuerpo

**En C++**: Lambda inmediatamente invocada (IIFE)

### 8.6 LambdaExpr → '\' ParamList '->' Expression

**Acción Semántica**:
- Crea nuevo scope para parámetros
- Registra parámetros como variables
- Analiza el cuerpo
- Retorna tipo función

**En C++**: Lambda de C++ `[&](auto params) { return body; }`

### 8.7 WhileExpr → 'while' Expression 'do' Expression 'end'

**Acción Semántica**:
- Verifica que la condición sea Bool
- Analiza el cuerpo
- Retorna tipo Void

**En C++**: 
```cpp
[&]() { while (cond) { body; } }()
```

### 8.8 ForExpr → 'for' IDENTIFIER 'in' Expression '..' Expression 'do' Expression 'end'

**Acción Semántica**:
- Crea scope con variable de iteración (tipo Int)
- Verifica que inicio y fin sean Int
- Analiza el cuerpo
- Retorna tipo Void

**En C++**:
```cpp
[&]() { for (int i = start; i <= end; i++) { body; } }()
```

### 8.9 DoBlock → 'do' DoStatements 'end'

**Acción Semántica**:
- Crea nuevo scope
- Procesa cada sentencia en orden
- El tipo es el de la última expresión o return

**En C++**: Lambda con secuencia de sentencias

### 8.10 BinaryExpr → Expression OP Expression

**Acción Semántica** (según operador):
- Aritméticos (+, -, *, /): Promoción numérica, retorna Float si alguno es Float
- Comparación (<, >, ==, etc.): Retorna Bool
- Lógicos (&&, ||): Verifica operandos Bool, retorna Bool
- Potencia (^, **): Usa pow() para Float

### 8.11 ListExpr → '[' ExpressionList ']'

**Acción Semántica**:
- Verifica que todos los elementos tengan tipos compatibles
- Retorna tipo [T] donde T es el tipo de elementos

**En C++**: `vector<T>{elem1, elem2, ...}`

### 8.12 ListComprehension → '[' Expression '|' Qualifiers ']'

**Acción Semántica**:
- Procesa generadores (var <- lista)
- Procesa filtros (condición booleana)
- Analiza la expresión de resultado
- Retorna tipo lista del tipo de la expresión

**En C++**: Combinación de filter_list y map_list

---

## 9. Tipos de Datos

### 9.1 Tipos Básicos

| Tipo | Descripción | Ejemplo |
|------|-------------|---------|
| Int | Entero de 32 bits | `42`, `-17`, `0xFF` |
| Float | Punto flotante | `3.14`, `2.5e-3` |
| Double | Doble precisión | `3.14159265359` |
| Bool | Booleano | `True`, `False` |
| Char | Caracter | `'a'`, `'\n'` |
| String | Cadena de texto | `"Hola mundo"` |

### 9.2 Tipos Compuestos

| Tipo | Sintaxis | Ejemplo |
|------|----------|---------|
| Lista | `[T]` | `[1, 2, 3]`, `[1..10]` |
| Arreglo | `array[T]` | `#[1, 2, 3]` |
| Matriz | `Matrix T` | `matrix [1,2; 3,4]` |
| Tupla | `(T1, T2, ...)` | `(1, "hola", True)` |
| Función | `T1 -> T2` | `Int -> Int -> Int` |

### 9.3 Tipos Definidos por Usuario

```haskell
-- Alias de tipo
type Punto = (Float, Float)

-- Tipo algebraico
data Maybe a = Nothing | Just a
data List a = Nil | Cons a (List a)
```

---

## 10. Ejemplos y Pruebas

### 10.1 Test 1: Algoritmo de Euclides

```haskell
-- Máximo Común Divisor
gcd :: Int -> Int -> Int
gcd a b
    | b == 0 = a
    | b > 0 = gcd b (a mod b)

main = do
    let resultado = gcd(48, 18)
    println(resultado)  -- Imprime: 6
    return 0
end
```

### 10.2 Test 2: Factorial Recursivo

```haskell
factorial :: Int -> Int
factorial n = if n <= 1 then 1 else n * factorial(n - 1)

main = do
    println(factorial(5))  -- Imprime: 120
    return 0
end
```

### 10.3 Test 3: Fibonacci

```haskell
fib :: Int -> Int
fib n
    | n <= 0 = 0
    | n == 1 = 1
    | n > 1 = fib(n-1) + fib(n-2)
```

### 10.4 Test 4: Operaciones con Listas

```haskell
main = do
    let nums = [1..10]
    let cuadrados = map(\x -> x * x, nums)
    let pares = filter(\x -> x mod 2 == 0, nums)
    let suma = foldl(\acc x -> acc + x, 0, nums)
    println(suma)  -- Imprime: 55
    return 0
end
```

### 10.5 Test 5: Matrices y Punto Flotante

```haskell
main = do
    let mat = matrix [1.0, 2.0; 3.0, 4.0]
    let det = mat[0,0] * mat[1,1] - mat[0,1] * mat[1,0]
    println(det)  -- Imprime: -2.0
    println(sqrt(2.0))  -- Imprime: 1.41421...
    return 0
end
```

---

## 11. Guía de Uso

### 11.1 Instalación

```bash
# Clonar o descargar el proyecto
cd Taller2_LP

# Crear entorno virtual (opcional)
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Instalar dependencias
pip install ply
```

### 11.2 Compilar un Programa

```bash
# Compilar a C++
python main.py archivo.fun

# Compilar con salida específica
python main.py archivo.fun -o salida.cpp

# Compilar y ejecutar (requiere g++)
python main.py archivo.fun -r

# Modo verbose (muestra todas las fases)
python main.py archivo.fun -v

# Solo mostrar tokens
python main.py archivo.fun --tokens

# Solo mostrar AST
python main.py archivo.fun --ast
```

### 11.3 Ejecutar Demo

```bash
# Sin argumentos ejecuta una demo
python main.py

# Ejecutar todas las pruebas
python main.py --test
```

### 11.4 Compilar el C++ Generado

```bash
# Compilar con g++
g++ -std=c++17 -O2 output/programa.cpp -o output/programa

# Ejecutar
./output/programa  # Linux/Mac
output\programa.exe  # Windows
```

---

## Apéndice A: Diagramas UML

Los diagramas de sintaxis pueden generarse en https://www.bottlecaps.de/rr/ui usando el archivo `grammar/funlang.ebnf`.

### A.1 Diagrama de Clases del AST

```
                    ┌─────────────┐
                    │   ASTNode   │
                    └──────┬──────┘
                           │
         ┌─────────────────┼─────────────────┐
         │                 │                 │
    ┌────┴────┐      ┌────┴────┐      ┌─────┴─────┐
    │ Program │      │Expression│      │Declaration│
    └─────────┘      └────┬────┘      └─────┬─────┘
                          │                  │
              ┌───────────┼───────────┐      │
              │           │           │      │
         ┌────┴───┐  ┌────┴───┐  ┌───┴───┐ ┌───┴───┐
         │BinaryOp│  │ IfExpr │  │LetExpr│ │FuncDecl│
         └────────┘  └────────┘  └───────┘ └───────┘
```

---

## Apéndice B: Código C++ Generado de Ejemplo

Para el programa de Euclides, el compilador genera:

```cpp
// Código generado por FunLang Compiler
#include <iostream>
#include <vector>
#include <cmath>
#include <functional>

using namespace std;

// Runtime de FunLang...

auto gcd(auto a, auto b) {
    if ((b == 0)) return a;
    if ((b > 0)) return gcd(b, (a % b));
    throw runtime_error("No matching guard");
}

int main() {
    [&]() { 
        auto x = 48; 
        auto y = 18; 
        println("Calculando MCD de 48 y 18:");
        auto resultado = gcd(x, y);
        print("MCD = ");
        println(resultado);
        return resultado; 
    }();
    return 0;
}
```

---

## Referencias

1. PLY (Python Lex-Yacc) Documentation: https://www.dabeaz.com/ply/
2. Haskell Language Report: https://www.haskell.org/onlinereport/
3. C++17 Standard: https://isocpp.org/std/the-standard
4. Railroad Diagram Generator: https://www.bottlecaps.de/rr/ui

---

**Fecha**: Noviembre 2024  
**Versión**: 1.0.0  
**Taller #2 - Lenguajes de Programación**
