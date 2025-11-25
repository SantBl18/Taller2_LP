"""
FunLang - Punto de entrada principal
Sistema de Procesamiento de Lenguaje (SPL)

Uso:
    python main.py <archivo.fun>           # Compilar a C++
    python main.py <archivo.fun> -r        # Compilar y ejecutar
    python main.py <archivo.fun> -v        # Modo verbose
    python main.py <archivo.fun> --tokens  # Solo mostrar tokens
    python main.py <archivo.fun> --ast     # Solo mostrar AST
"""

import sys
import os

# Agregar el directorio src al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.compiler import main as compiler_main, create_compiler


def demo():
    """Demostración del compilador con un programa simple"""
    
    print("=" * 70)
    print("  FunLang Compiler - Demostración")
    print("  Lenguaje Funcional -> C++ Ejecutable")
    print("=" * 70)
    
    # Programa de ejemplo: Algoritmo de Euclides
    demo_code = '''
-- Algoritmo de Euclides para MCD
-- Ejemplo de programa en FunLang

-- Función factorial recursiva
factorial n = if n <= 1 then 1 else n * factorial(n - 1)

-- Función principal
main = do
    let x = 5
    println("Calculando factorial de 5:")
    let resultado = factorial(x)
    print("5! = ")
    println(resultado)
    return resultado
end
'''
    
    print("\n[CÓDIGO FUENTE FunLang]")
    print("-" * 40)
    print(demo_code)
    print("-" * 40)
    
    # Compilar
    compiler = create_compiler(verbose=True)
    
    output_dir = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(output_dir, exist_ok=True)
    
    cpp_path = os.path.join(output_dir, "demo.cpp")
    result = compiler.compile(demo_code, cpp_path)
    
    if result.success:
        print("\n" + "=" * 70)
        print("[CÓDIGO C++ GENERADO]")
        print("=" * 70)
        print(result.cpp_code)
        
        print("\n" + "=" * 70)
        print(f"Archivo guardado: {cpp_path}")
        print("=" * 70)
        
        # Intentar compilar y ejecutar con g++
        print("\n¿Desea compilar y ejecutar el código C++? (requiere g++)")
        print("Para compilar manualmente:")
        print(f"  g++ -std=c++17 -O2 {cpp_path} -o {output_dir}/demo")
    else:
        print("\n[ERRORES DE COMPILACIÓN]")
        for err in result.errors:
            print(f"  {err}")


def run_tests():
    """Ejecuta los programas de prueba"""
    tests_dir = os.path.join(os.path.dirname(__file__), "tests")
    output_dir = os.path.join(os.path.dirname(__file__), "output")
    
    if not os.path.exists(tests_dir):
        print(f"Directorio de pruebas no encontrado: {tests_dir}")
        return
    
    os.makedirs(output_dir, exist_ok=True)
    
    compiler = create_compiler(verbose=False)
    
    test_files = [f for f in os.listdir(tests_dir) if f.endswith('.fun')]
    
    print("=" * 70)
    print("  Ejecutando programas de prueba")
    print("=" * 70)
    
    for test_file in sorted(test_files):
        input_path = os.path.join(tests_dir, test_file)
        output_path = os.path.join(output_dir, test_file.replace('.fun', '.cpp'))
        
        print(f"\n[{test_file}]")
        
        result = compiler.compile_file(input_path, output_path)
        
        if result.success:
            print(f"  ✓ Compilado exitosamente -> {os.path.basename(output_path)}")
            if result.warnings:
                for w in result.warnings:
                    print(f"  ⚠ {w}")
        else:
            print(f"  ✗ Error de compilación")
            for e in result.errors:
                print(f"    {e}")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        # Sin argumentos: ejecutar demo
        demo()
    elif sys.argv[1] == "--test":
        # Ejecutar pruebas
        run_tests()
    else:
        # Usar el CLI del compilador
        compiler_main()