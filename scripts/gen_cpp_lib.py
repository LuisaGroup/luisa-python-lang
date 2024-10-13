import bz2
import base64
import io
from typing import Dict


def compress(s: str) -> str:
    data = s.encode('utf-8')
    return base64.b64encode(bz2.compress(data)).decode('utf-8')


CPP_LIB_SRC = io.StringIO()
print("""
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
""", file=CPP_LIB_SRC)

TYPES = ['i8', 'u8', 'i16', 'u16', 'i32', 'u32', 'i64', 'u64', 'f32', 'f64']


def gen_alignment(ty: str, c: int, a: int):
    print(f'''    if constexpr (is_same_v<T, {ty}> && N == {c}) {{
        return alignof({ty}) * {a};
    }}''', file=CPP_LIB_SRC)


for t in TYPES:
    for c in [3]:
        gen_alignment(t, c, 4)

print('return alignof(T) * N;\n}', file=CPP_LIB_SRC)


print("""
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
#define VEC_OP(op, op_assign) \\
    vec<T, N> operator op(const vec<T, N>& other) const noexcept \\
       requires requires(T a, T b) { a op b; } { \\
        vec<T, N> result{}; \\
        for (int i = 0; i < N; ++i) { \\
            result[i] = data[i] op other.data[i]; \\
        } \\
        return result; \\
    } \\
    vec<T, N> operator op(T scalar) const noexcept \\
        requires requires(T a, T b) { a op b; } { \\
        vec<T, N> result{}; \\
        for (int i = 0; i < N; ++i) { \\
            result[i] = data[i] op scalar; \\
        } \\
        return result; \\
    } \\
    friend vec<T, N> operator op(T scalar, const vec<T, N>& v) noexcept \\
        requires requires(T a, T b) { a op b; } { \\
        return vec<T, N>{scalar} op v; \\
    } \\
    vec<T, N> operator op_assign(const vec<T, N>& other) noexcept \\
        requires requires(T a, T b) { a op_assign b; } { \\
        for (int i = 0; i < N; ++i) { \\
            data[i] op_assign other.data[i]; \\
        } \\
        return *this; \\
    } \\
    vec<T, N> operator op_assign(T scalar) noexcept \\
        requires requires(T a, T b) { a op_assign b; }{ \\
        for (int i = 0; i < N; ++i) { \\
            data[i] op_assign scalar; \\
        } \\
        return *this; \\
    }
    VEC_OP(+, +=)
    VEC_OP(-, -=)
    VEC_OP(*, *=)
    VEC_OP(/, /=)
    VEC_OP(%, %=)
      
};
""", file=CPP_LIB_SRC)

_OPERATORS: Dict[str, str] = {
    '__add__': '+',
    '__sub__': '-',
    '__mul__': '*',
    '__truediv__': '/',
}
for op, cpp_op in _OPERATORS.items():
    print(f"""template<class T>
requires requires(T a, T b) {{ a {cpp_op} b; }}
T __builtin__{op}(T x, T y)
{{
    return x {cpp_op} y;
}}""", file=CPP_LIB_SRC)
with open('scripts/cpp_lib.hpp', 'w') as f:
    f.write(CPP_LIB_SRC.getvalue())

