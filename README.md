# FunLang Compiler

Compilador de un lenguaje funcional simple que genera código C++ ejecutable.
Proyecto del Taller #2 de Lenguajes de Programación.

## Estructura del Proyecto

```
Taller2_LP/
├── src/
│   ├── lexer.py          # Analizador Léxico (PLY)
│   ├── parser.py         # Analizador Sintáctico (PLY)
│   ├── ast_nodes.py      # Nodos del AST
│   ├── semantic.py       # Analizador Semántico
│   ├── codegen.py        # Generador de Código C++
│   └── compiler.py       # Compilador integrado
├── grammar/
│   └── funlang.ebnf      # Gramática E-BNF
├── tests/
│   ├── test1_euclides.fun
│   ├── test2_factorial.fun
│   ├── test3_fibonacci.fun
│   ├── test4_arrays.fun
│   └── test5_matrices.fun
├── output/               # Código C++ generado
├── docs/
│   └── manual_tecnico.md
├── compile_all.ps1       # Script para compilar C++
└── main.py
```

## Características del Lenguaje

- Funciones recursivas
- Expresiones `if-then-else`
- Bloques `do...end` con `let` y `return`
- Operadores aritméticos: `+`, `-`, `*`, `/`, `%`
- Operadores de comparación: `==`, `!=`, `<`, `>`, `<=`, `>=`
- Rangos: `[1..10]`
- Funciones built-in: `print`, `println`, `sum`, `product`, `sqrt`, `abs`, `pow`
- Comentarios: `-- comentario`

## Requisitos

- Python 3.8+
- PLY (`pip install ply`)
- G++ (para compilar el código generado)

## Uso

```bash
# Demo
python main.py

# Compilar archivo
python main.py tests/test1_euclides.fun

# Ejecutar todas las pruebas
python main.py --test

# Compilar todos los C++ generados
.\compile_all.ps1
```

## Ejemplo

```
-- Factorial recursivo
factorial n = if n <= 1 then 1 else n * factorial(n - 1)

main = do
    println("5! = ")
    println(factorial(5))
    return 0
end
```

## Autores

Taller #2 - Lenguajes de Programación
