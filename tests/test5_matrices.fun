-- ============================================================
-- Test 5: Aritmética de Punto Flotante
-- ============================================================
-- Este programa demuestra operaciones con punto flotante.
-- Demuestra: float, funciones matemáticas
-- ============================================================

-- Constantes
let pi = 3.14159265359

-- Función para calcular área de círculo
areaCirculo r = pi * r * r

-- Función para calcular hipotenusa
hipotenusa a b = sqrt(a * a + b * b)

-- Función cuadrática f(x) = ax^2 + bx + c
cuadratica a b c x = a * x * x + b * x + c

-- Función principal
main = do
    println("=== Aritmetica de Punto Flotante ===")
    
    print("PI = ")
    println(pi)
    
    print("Area de circulo (r=5): ")
    println(areaCirculo(5.0))
    
    print("Hipotenusa (3,4): ")
    println(hipotenusa(3.0, 4.0))
    
    println("")
    println("Funciones matematicas:")
    
    print("sqrt(2) = ")
    println(sqrt(2.0))
    
    print("sqrt(16) = ")
    println(sqrt(16.0))
    
    print("pow(2, 10) = ")
    println(pow(2.0, 10.0))
    
    print("abs(-5.5) = ")
    println(abs(-5.5))
    
    println("")
    println("Funcion cuadratica f(x) = 2x^2 - 3x + 1:")
    
    print("f(0) = ")
    println(cuadratica(2.0, -3.0, 1.0, 0.0))
    
    print("f(1) = ")
    println(cuadratica(2.0, -3.0, 1.0, 1.0))
    
    print("f(2) = ")
    println(cuadratica(2.0, -3.0, 1.0, 2.0))
    
    return 0
end
