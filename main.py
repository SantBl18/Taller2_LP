#!/usr/bin/env python3
"""
FunLang Compiler - Punto de entrada principal
Lenguaje funcional que compila a C++ ejecutable
"""

import sys
import os
from pathlib import Path

# Agregar src al path
sys.path.insert(0, str(Path(__file__).parent))

from src.compiler import create_compiler
from src.ast_nodes import ASTPrinter


def print_header():
    print("=" * 60)
    print("  FunLang Compiler")
    print("  Lenguaje funcional -> C++ ejecutable")
    print("=" * 60)
    print()


def run_demo():
    """Ejecuta una demostración del compilador"""
    demo_code = '''-- Ejemplo: Factorial recursivo
factorial n = if n <= 1 then 1 else n * factorial(n - 1)

main = do
    println("Calculando factorial de 5:")
    let resultado = factorial(5)
    print("5! = ")
    println(resultado)
    return 0
end
'''
    
    print_header()
    print("[CÓDIGO FUENTE]")
    print("-" * 40)
    print(demo_code)
    print("-" * 40)
    print()
    
    compiler = create_compiler()
    result = compiler.compile(demo_code, "demo")
    
    if result['success']:
        print("[COMPILACIÓN EXITOSA]")
        print(f"Archivo generado: {result['output_file']}")
        print()
        print("[CÓDIGO C++ GENERADO]")
        print("-" * 40)
        print(result['cpp_code'])
    else:
        print("[ERRORES]")
        for error in result['errors']:
            print(f"  - {error}")


def run_tests():
    """Ejecuta todos los programas de prueba"""
    print_header()
    print("Ejecutando programas de prueba...")
    print()
    
    tests_dir = Path(__file__).parent / "tests"
    compiler = create_compiler()
    
    results = {'passed': 0, 'failed': 0}
    
    for test_file in sorted(tests_dir.glob("*.fun")):
        name = test_file.stem
        print(f"[{test_file.name}] ", end="")
        
        result = compiler.compile_file(str(test_file))
        
        if result['success']:
            print(f"✓ -> {name}.cpp")
            results['passed'] += 1
        else:
            print("✗ Error")
            for error in result['errors']:
                print(f"    {error}")
            results['failed'] += 1
    
    print()
    print("-" * 40)
    print(f"Resultados: {results['passed']} exitosos, {results['failed']} fallidos")


def compile_file(filepath: str):
    """Compila un archivo específico"""
    print_header()
    
    compiler = create_compiler()
    result = compiler.compile_file(filepath)
    
    if result['success']:
        print(f"[OK] Compilado: {result['output_file']}")
    else:
        print("[ERROR]")
        for error in result['errors']:
            print(f"  - {error}")


def main():
    if len(sys.argv) < 2:
        run_demo()
    elif sys.argv[1] == "--test":
        run_tests()
    elif sys.argv[1] == "--help":
        print("Uso: python main.py [archivo.fun] [--test]")
        print()
        print("Opciones:")
        print("  (sin args)    Ejecuta demo")
        print("  archivo.fun   Compila el archivo")
        print("  --test        Ejecuta todos los tests")
    else:
        compile_file(sys.argv[1])


if __name__ == "__main__":
    main()
