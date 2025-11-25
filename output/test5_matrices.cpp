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

auto pi = 3.14159265359;

template<typename T0>
auto areaCirculo(T0 r) {
    return ((pi * r) * r);
}

template<typename T0, typename T1>
auto hipotenusa(T0 a, T1 b) {
    return sqrt(((a * a) + (b * b)));
}

template<typename T0, typename T1, typename T2, typename T3>
auto cuadratica(T0 a, T1 b, T2 c, T3 x) {
    return ((((a * x) * x) + (b * x)) + c);
}


int main() {
    println("=== Aritmetica de Punto Flotante ===");
    print("PI = ");
    println(pi);
    print("Area de circulo (r=5): ");
    println(areaCirculo(5.0));
    print("Hipotenusa (3,4): ");
    println(hipotenusa(3.0, 4.0));
    println("");
    println("Funciones matematicas:");
    print("sqrt(2) = ");
    println(sqrt(2.0));
    print("sqrt(16) = ");
    println(sqrt(16.0));
    print("pow(2, 10) = ");
    println(pow(2.0, 10.0));
    print("abs(-5.5) = ");
    println(abs((-5.5)));
    println("");
    println("Funcion cuadratica f(x) = 2x^2 - 3x + 1:");
    print("f(0) = ");
    println(cuadratica(2.0, (-3.0), 1.0, 0.0));
    print("f(1) = ");
    println(cuadratica(2.0, (-3.0), 1.0, 1.0));
    print("f(2) = ");
    println(cuadratica(2.0, (-3.0), 1.0, 2.0));
    return 0;
}