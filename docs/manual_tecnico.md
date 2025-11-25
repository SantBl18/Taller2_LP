# Manual Técnico - FunLang Compiler

## 1. Introducción

FunLang es un lenguaje de programación funcional simple que compila a código C++ ejecutable.
Este compilador fue desarrollado usando PLY (Python Lex-Yacc).

## 2. Arquitectura del Compilador

```
Código Fuente (.fun)
        │
        ▼
┌───────────────┐
│ Lexer (PLY)   │  → Tokens
└───────────────┘
        │
        ▼
┌───────────────┐
│ Parser (PLY)  │  → AST
└───────────────┘
        │
        ▼
┌───────────────┐
│ Semántico     │  → AST validado
└───────────────┘
        │
        ▼
┌───────────────┐
│ Codegen       │  → Código C++
└───────────────┘
        │
        ▼
  Archivo .cpp
```

## 3. Componentes

### 3.1 Analizador Léxico (`lexer.py`)

Tokeniza el código fuente en:
- **Palabras reservadas**: `if`, `then`, `else`, `let`, `do`, `end`, `return`, `True`, `False`
- **Identificadores**: nombres de variables y funciones
- **Literales**: enteros, flotantes, strings
- **Operadores**: `+`, `-`, `*`, `/`, `%`, `==`, `!=`, `<`, `>`, `<=`, `>=`, `&&`, `||`
- **Delimitadores**: `(`, `)`, `[`, `]`, `,`, `=`, `..`

### 3.2 Analizador Sintáctico (`parser.py`)

Implementa la gramática E-BNF del lenguaje usando reglas de producción PLY.

**Precedencia de operadores** (menor a mayor):
1. `||` (OR lógico)
2. `&&` (AND lógico)
3. `==`, `!=`, `<`, `>`, `<=`, `>=` (comparación)
4. `+`, `-` (aditivos)
5. `*`, `/`, `%` (multiplicativos)
6. `-`, `!` (unarios)

### 3.3 Nodos AST (`ast_nodes.py`)

Nodos principales:
- `Program` - Nodo raíz
- `FunctionDecl` - Declaración de función
- `VarDecl` - Declaración de variable
- `IfExpr` - Expresión if-then-else
- `DoBlock` - Bloque do...end
- `BinaryExpr` - Operación binaria
- `FunctionCall` - Llamada a función
- `IntLiteral`, `FloatLiteral`, `StringLiteral` - Literales
- `RangeExpr` - Expresión de rango [a..b]

### 3.4 Analizador Semántico (`semantic.py`)

Verifica:
- Variables definidas antes de uso
- Funciones definidas antes de llamada
- Manejo de ámbitos (global, función, bloque)

### 3.5 Generador de Código (`codegen.py`)

Genera código C++ incluyendo:
- Runtime mínimo (print, println, range, sum, product)
- Funciones como templates para polimorfismo
- Detección de recursión para tipos explícitos

## 4. Sintaxis del Lenguaje

### 4.1 Comentarios
```
-- Esto es un comentario
```

### 4.2 Variables Globales
```
let pi = 3.14159
```

### 4.3 Funciones
```
-- Función simple
doble x = x * 2

-- Función con múltiples parámetros
suma a b = a + b

-- Función recursiva
factorial n = if n <= 1 then 1 else n * factorial(n - 1)
```

### 4.4 Bloques Do
```
main = do
    let x = 10
    println("Hola")
    print(x)
    return 0
end
```

### 4.5 If-Then-Else
```
max a b = if a > b then a else b
```

### 4.6 Rangos
```
let numeros = [1..10]    -- Lista del 1 al 10
println(sum(numeros))    -- Imprime 55
```

## 5. Funciones Built-in

| Función | Descripción |
|---------|-------------|
| `print(x)` | Imprime sin salto de línea |
| `println(x)` | Imprime con salto de línea |
| `sum(lista)` | Suma elementos de lista |
| `product(lista)` | Producto de elementos |
| `sqrt(x)` | Raíz cuadrada |
| `abs(x)` | Valor absoluto |
| `pow(x, y)` | Potencia x^y |

## 6. Compilación

```bash
# 1. Compilar .fun a .cpp
python main.py archivo.fun

# 2. Compilar .cpp a ejecutable
g++ -std=c++14 -O2 -static output/archivo.cpp -o output/archivo.exe

# 3. Ejecutar
./output/archivo.exe
```

## 7. Ejemplos

Ver carpeta `tests/` para 5 programas de ejemplo:
1. Algoritmo de Euclides (MCD)
2. Factorial recursivo
3. Serie de Fibonacci
4. Operaciones con listas
5. Aritmética de punto flotante
