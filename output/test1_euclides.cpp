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

template<typename T0, typename T1>
T0 gcd(T0 a, T1 b) {
    return ((b == 0) ? a : gcd(b, (a % b)));
}


int main() {
    println("=== Algoritmo de Euclides ===");
    auto a1 = 48;
    auto b1 = 18;
    print("MCD(48, 18) = ");
    auto r1 = gcd(a1, b1);
    println(r1);
    auto a2 = 56;
    auto b2 = 98;
    print("MCD(56, 98) = ");
    auto r2 = gcd(a2, b2);
    println(r2);
    auto a3 = 270;
    auto b3 = 192;
    print("MCD(270, 192) = ");
    auto r3 = gcd(a3, b3);
    println(r3);
    return 0;
}