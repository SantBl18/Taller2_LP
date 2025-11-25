// Código generado por FunLang Compiler
// Lenguaje funcional -> C++

#include <algorithm>
#include <cmath>
#include <functional>
#include <iostream>
#include <string>
#include <vector>

using namespace std;

// ============= Runtime de FunLang =============

// Tipo para listas/arreglos dinámicos
template<typename T>
using List = vector<T>;

// Tipo para matrices
template<typename T>
using Matrix = vector<vector<T>>;

// Funciones de lista
template<typename T>
int length(const List<T>& xs) { return xs.size(); }

template<typename T>
T head(const List<T>& xs) { return xs.front(); }

template<typename T>
List<T> tail(const List<T>& xs) { return List<T>(xs.begin()+1, xs.end()); }

template<typename T>
T last(const List<T>& xs) { return xs.back(); }

template<typename T>
List<T> init(const List<T>& xs) { return List<T>(xs.begin(), xs.end()-1); }

template<typename T>
List<T> take(int n, const List<T>& xs) {
    return List<T>(xs.begin(), xs.begin() + min((size_t)n, xs.size()));
}

template<typename T>
List<T> drop(int n, const List<T>& xs) {
    return List<T>(xs.begin() + min((size_t)n, xs.size()), xs.end());
}

template<typename T>
List<T> reverse_list(const List<T>& xs) {
    List<T> result(xs.rbegin(), xs.rend());
    return result;
}

template<typename T>
List<T> concat(const List<T>& xs, const List<T>& ys) {
    List<T> result = xs;
    result.insert(result.end(), ys.begin(), ys.end());
    return result;
}

template<typename T>
T sum(const List<T>& xs) {
    T result = 0;
    for (const auto& x : xs) result += x;
    return result;
}

template<typename T>
T product(const List<T>& xs) {
    T result = 1;
    for (const auto& x : xs) result *= x;
    return result;
}

template<typename T>
bool elem(const T& x, const List<T>& xs) {
    return find(xs.begin(), xs.end(), x) != xs.end();
}

// Función range [a..b]
List<int> range(int start, int end) {
    List<int> result;
    for (int i = start; i <= end; i++) result.push_back(i);
    return result;
}

// Función range con paso [a,b..c]
List<int> range_step(int start, int next, int end) {
    List<int> result;
    int step = next - start;
    if (step > 0) {
        for (int i = start; i <= end; i += step) result.push_back(i);
    } else if (step < 0) {
        for (int i = start; i >= end; i += step) result.push_back(i);
    }
    return result;
}

// Map
template<typename T, typename F>
auto map_list(F f, const List<T>& xs) {
    List<decltype(f(xs[0]))> result;
    for (const auto& x : xs) result.push_back(f(x));
    return result;
}

// Filter
template<typename T, typename F>
List<T> filter_list(F f, const List<T>& xs) {
    List<T> result;
    for (const auto& x : xs) if (f(x)) result.push_back(x);
    return result;
}

// Foldl
template<typename T, typename R, typename F>
R foldl(F f, R acc, const List<T>& xs) {
    for (const auto& x : xs) acc = f(acc, x);
    return acc;
}

// Funciones de I/O
template<typename T>
void print(const T& x) { cout << x; }

template<typename T>
void println(const T& x) { cout << x << endl; }

string readLine() { string s; getline(cin, s); return s; }
int readInt() { int x; cin >> x; return x; }
double readFloat() { double x; cin >> x; return x; }

// Conversiones
int toInt(double x) { return (int)x; }
int toInt(const string& s) { return stoi(s); }
double toFloat(int x) { return (double)x; }
double toFloat(const string& s) { return stod(s); }
string toString(int x) { return to_string(x); }
string toString(double x) { return to_string(x); }

// Funciones matemáticas adicionales
template<typename T>
T min_val(T a, T b) { return a < b ? a : b; }

template<typename T>
T max_val(T a, T b) { return a > b ? a : b; }

// ============= Fin Runtime =============

// Variables globales
auto pi = 3.14159265359;

// Funciones
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
    [&]() { println("=== Aritmetica de Punto Flotante ==="); print("PI = "); println(pi); print("Area de circulo (r=5): "); println(areaCirculo(5.0)); print("Hipotenusa (3,4): "); println(hipotenusa(3.0, 4.0)); println(""); println("Funciones matematicas:"); print("sqrt(2) = "); println(sqrt(2.0)); print("sqrt(16) = "); println(sqrt(16.0)); print("pow(2, 10) = "); println(pow(2.0, 10.0)); print("abs(-5.5) = "); println(abs((-5.5))); println(""); println("Funcion cuadratica f(x) = 2x^2 - 3x + 1:"); print("f(0) = "); println(cuadratica(2.0, (-3.0), 1.0, 0.0)); print("f(1) = "); println(cuadratica(2.0, (-3.0), 1.0, 1.0)); print("f(2) = "); println(cuadratica(2.0, (-3.0), 1.0, 2.0)); return 0; }();
    return 0;
}