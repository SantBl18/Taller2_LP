-- ============================================================
-- Test 4: Manejo de Listas y Operaciones
-- ============================================================
-- Este programa demuestra el manejo de listas,
-- incluyendo operaciones funcionales
-- Demuestra: listas, lambdas, funciones de orden superior
-- ============================================================

-- Función para calcular cuadrado
cuadrado x = x * x

-- Función para verificar si es par
esPar x = x % 2 == 0

-- Función principal
main = do
    println("=== Manejo de Listas ===")
    
    let n1 = 1
    let n2 = 2
    let n3 = 3
    let n4 = 4
    let n5 = 5
    
    print("Valores: ")
    print(n1)
    print(" ")
    print(n2)
    print(" ")
    print(n3)
    print(" ")
    print(n4)
    print(" ")
    println(n5)
    
    print("Suma manual: ")
    let suma = n1 + n2 + n3 + n4 + n5
    println(suma)
    
    print("Producto manual: ")
    let prod = n1 * n2 * n3 * n4 * n5
    println(prod)
    
    println("")
    println("Operaciones con rangos:")
    
    let rango = [1..10]
    print("Suma de rango [1..10]: ")
    println(sum(rango))
    
    print("Producto de rango [1..5]: ")
    let r5 = [1..5]
    println(product(r5))
    
    return 0
end
