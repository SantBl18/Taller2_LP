// Código generado por FunLang Compiler

#include <cmath>
#include <iostream>
#include <string>
#include <vector>

using namespace std;

// === Runtime ===
template<typename T> void print(const T& x) { cout << x; }
template<typename T> void println(const T& x) { cout << x << endl; }

vector<int> range(int start, int end) {
    vector<int> result;
    for (int i = start; i <= end; i++) result.push_back(i);
    return result;
}

template<typename T> T sum(const vector<T>& xs) {
    T result = 0;
    for (const auto& x : xs) result += x;
    return result;
}

template<typename T> T product(const vector<T>& xs) {
    T result = 1;
    for (const auto& x : xs) result *= x;
    return result;
}
// === Fin Runtime ===

template<typename T0>
auto cuadrado(T0 x) {
    return (x * x);
}

template<typename T0>
auto esPar(T0 x) {
    return ((x % 2) == 0);
}


int main() {
    println("=== Manejo de Listas ===");
    auto n1 = 1;
    auto n2 = 2;
    auto n3 = 3;
    auto n4 = 4;
    auto n5 = 5;
    print("Valores: ");
    print(n1);
    print(" ");
    print(n2);
    print(" ");
    print(n3);
    print(" ");
    print(n4);
    print(" ");
    println(n5);
    print("Suma manual: ");
    auto suma = ((((n1 + n2) + n3) + n4) + n5);
    println(suma);
    print("Producto manual: ");
    auto prod = ((((n1 * n2) * n3) * n4) * n5);
    println(prod);
    println("");
    println("Operaciones con rangos:");
    auto rango = range(1, 10);
    print("Suma de rango [1..10]: ");
    println(sum(rango));
    print("Producto de rango [1..5]: ");
    auto r5 = range(1, 5);
    println(product(r5));
    return 0;
}