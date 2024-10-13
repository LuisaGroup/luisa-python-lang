
using i8 = char;
using u8 = unsigned char;
using i16 = short;
using u16 = unsigned short;
using i32 = int;
using u32 = unsigned int;
using i64 = long long;
using u64 = unsigned long long;
using f32 = float;
using f64 = double;

template<class T, class U>
constexpr bool is_same_v = false;

template<class T>
constexpr bool is_same_v<T, T> = true;

template<class T, int N>
constexpr int compute_alignment() noexcept {

    if constexpr (is_same_v<T, i8> && N == 3) {
        return alignof(i8) * 4;
    }
    if constexpr (is_same_v<T, u8> && N == 3) {
        return alignof(u8) * 4;
    }
    if constexpr (is_same_v<T, i16> && N == 3) {
        return alignof(i16) * 4;
    }
    if constexpr (is_same_v<T, u16> && N == 3) {
        return alignof(u16) * 4;
    }
    if constexpr (is_same_v<T, i32> && N == 3) {
        return alignof(i32) * 4;
    }
    if constexpr (is_same_v<T, u32> && N == 3) {
        return alignof(u32) * 4;
    }
    if constexpr (is_same_v<T, i64> && N == 3) {
        return alignof(i64) * 4;
    }
    if constexpr (is_same_v<T, u64> && N == 3) {
        return alignof(u64) * 4;
    }
    if constexpr (is_same_v<T, f32> && N == 3) {
        return alignof(f32) * 4;
    }
    if constexpr (is_same_v<T, f64> && N == 3) {
        return alignof(f64) * 4;
    }
return alignof(T) * N;
}

template<class T, int N>
struct alignas(compute_alignment<T, N>()) vec {
    T data[N]{};
    vec() noexcept = default;
    explicit vec(T value) noexcept {
        for (int i = 0; i < N; ++i) {
            data[i] = value;
        }
    }
    T& operator[](int i) noexcept {
        return data[i];
    }
    T operator[](int i) const noexcept{
        return data[i];
    }
#define VEC_OP(op, op_assign) \
    vec<T, N> operator op(const vec<T, N>& other) const noexcept \
       requires requires(T a, T b) { a op b; } { \
        vec<T, N> result{}; \
        for (int i = 0; i < N; ++i) { \
            result[i] = data[i] op other.data[i]; \
        } \
        return result; \
    } \
    vec<T, N> operator op(T scalar) const noexcept \
        requires requires(T a, T b) { a op b; } { \
        vec<T, N> result{}; \
        for (int i = 0; i < N; ++i) { \
            result[i] = data[i] op scalar; \
        } \
        return result; \
    } \
    friend vec<T, N> operator op(T scalar, const vec<T, N>& v) noexcept \
        requires requires(T a, T b) { a op b; } { \
        return vec<T, N>{scalar} op v; \
    } \
    vec<T, N> operator op_assign(const vec<T, N>& other) noexcept \
        requires requires(T a, T b) { a op_assign b; } { \
        for (int i = 0; i < N; ++i) { \
            data[i] op_assign other.data[i]; \
        } \
        return *this; \
    } \
    vec<T, N> operator op_assign(T scalar) noexcept \
        requires requires(T a, T b) { a op_assign b; }{ \
        for (int i = 0; i < N; ++i) { \
            data[i] op_assign scalar; \
        } \
        return *this; \
    }
    VEC_OP(+, +=)
    VEC_OP(-, -=)
    VEC_OP(*, *=)
    VEC_OP(/, /=)
    VEC_OP(%, %=)
      
};

template<class T>
requires requires(T a, T b) { a + b; }
T __builtin____add__(T x, T y)
{
    return x + y;
}
template<class T>
requires requires(T a, T b) { a - b; }
T __builtin____sub__(T x, T y)
{
    return x - y;
}
template<class T>
requires requires(T a, T b) { a * b; }
T __builtin____mul__(T x, T y)
{
    return x * y;
}
template<class T>
requires requires(T a, T b) { a / b; }
T __builtin____truediv__(T x, T y)
{
    return x / y;
}
