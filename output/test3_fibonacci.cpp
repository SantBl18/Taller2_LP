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
T0 fib(T0 n) {
    return ((n <= 0) ? 0 : ((n == 1) ? 1 : (fib((n - 1)) + fib((n - 2)))));
}

template<typename T0, typename T1, typename T2>
T0 fibAcc(T0 n, T1 a, T2 b) {
    return ((n <= 0) ? a : fibAcc((n - 1), b, (a + b)));
}

template<typename T0>
auto fibFast(T0 n) {
    return fibAcc(n, 0, 1);
}


int main() {
    println("=== Serie de Fibonacci ===");
    println("Primeros números de Fibonacci:");
    print("F(0) = ");
    println(fibFast(0));
    print("F(1) = ");
    println(fibFast(1));
    print("F(5) = ");
    println(fibFast(5));
    print("F(10) = ");
    println(fibFast(10));
    print("F(15) = ");
    println(fibFast(15));
    print("F(20) = ");
    println(fibFast(20));
    return 0;
}