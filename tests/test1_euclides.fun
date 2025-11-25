-- ============================================================
-- Test 1: Algoritmo de Euclides (MCD - Máximo Común Divisor)
-- ============================================================
-- Este programa implementa el algoritmo de Euclides para
-- calcular el máximo común divisor de dos números.
-- Demuestra: recursión, if-then-else, funciones
-- ============================================================

-- Implementación recursiva con if-then-else
gcd a b = if b == 0 then a else gcd(b, a % b)

-- Función principal
main = do
    println("=== Algoritmo de Euclides ===")
    
    let a1 = 48
    let b1 = 18
    print("MCD(48, 18) = ")
    let r1 = gcd(a1, b1)
    println(r1)
    
    let a2 = 56
    let b2 = 98
    print("MCD(56, 98) = ")
    let r2 = gcd(a2, b2)
    println(r2)
    
    let a3 = 270
    let b3 = 192
    print("MCD(270, 192) = ")
    let r3 = gcd(a3, b3)
    println(r3)
    
    return 0
end
