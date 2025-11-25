-- ============================================================
-- Test 3: Serie de Fibonacci
-- ============================================================
-- Este programa calcula números de la serie de Fibonacci.
-- Demuestra: recursión, condicionales
-- ============================================================

-- Fibonacci recursivo simple
fib n = if n <= 0 then 0 else if n == 1 then 1 else fib(n - 1) + fib(n - 2)

-- Fibonacci eficiente con acumuladores
fibAcc n a b = if n <= 0 then a else fibAcc(n - 1, b, a + b)

-- Wrapper para fibonacci eficiente
fibFast n = fibAcc(n, 0, 1)

-- Función principal
main = do
    println("=== Serie de Fibonacci ===")
    
    println("Primeros números de Fibonacci:")
    
    print("F(0) = ")
    println(fibFast(0))
    
    print("F(1) = ")
    println(fibFast(1))
    
    print("F(5) = ")
    println(fibFast(5))
    
    print("F(10) = ")
    println(fibFast(10))
    
    print("F(15) = ")
    println(fibFast(15))
    
    print("F(20) = ")
    println(fibFast(20))
    
    return 0
end
