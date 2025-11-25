-- ============================================================
-- Test 2: Factorial Recursivo
-- ============================================================
-- Este programa calcula el factorial de un número usando
-- recursión. Demuestra: recursión, if-then-else, expresiones
-- ============================================================

-- Implementación recursiva con if-then-else
factorial n = if n <= 1 then 1 else n * factorial(n - 1)

-- Función principal
main = do
    println("=== Cálculo de Factorial ===")
    
    print("5! = ")
    println(factorial(5))
    
    print("10! = ")
    println(factorial(10))
    
    print("7! = ")
    println(factorial(7))
    
    print("0! = ")
    println(factorial(0))
    
    print("1! = ")
    println(factorial(1))
    
    return 0
end
