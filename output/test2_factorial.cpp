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
T0 factorial(T0 n) {
    return ((n <= 1) ? 1 : (n * factorial((n - 1))));
}


int main() {
    println("=== Cálculo de Factorial ===");
    print("5! = ");
    println(factorial(5));
    print("10! = ");
    println(factorial(10));
    print("7! = ");
    println(factorial(7));
    print("0! = ");
    println(factorial(0));
    print("1! = ");
    println(factorial(1));
    return 0;
}