
#define __device__
#include <cmath>
#include <bit>
          
// inline directives
          // if msvc
#ifdef _MSC_VER
#define __lc_always_inline__ __forceinline
#define __lc_never_inline__ __declspec(noinline)
#else
#define __lc_always_inline__ __attribute__((always_inline))
#define __lc_never_inline__ __attribute__((noinline))
#endif

          
inline int __float_as_int(float x) noexcept { return std::bit_cast<int>(x); }
inline float __int_as_float(int x) noexcept { return std::bit_cast<float>(x); }
inline float exp10f(float x) noexcept { return std::pow(10.0f, x); }
inline float rsqrtf(float x) noexcept { return 1.0f / std::sqrt(x); }
inline int __clz(unsigned int x) {
    return __builtin_clz(x);
}
inline int __ctz(unsigned int x) {
    return __builtin_ctz(x);
}
inline int __clzll(unsigned long long x) {
    return __builtin_clzll(x);
}
inline int __ctzll(unsigned long long x) {
    return __builtin_ctzll(x);
}
inline int __ffs(unsigned int x) {
    return __builtin_ffs(x);
}
inline int __ffsll(unsigned long long x) {
    return __builtin_ffsll(x);
}
inline int __popc(unsigned int x) {
    return __builtin_popcount(x);
}
inline int __brev(unsigned int x) {
    return __builtin_bswap32(x);
}
inline int __popcll(unsigned long long x) {
    return __builtin_popcountll(x);
}
inline int __brevll(unsigned long long x) {
    return __builtin_bswap64(x);
}

using lc_byte = char;
using lc_ubyte = unsigned char;
using lc_short = short;
using lc_ushort = unsigned short;
using lc_int = int;
using lc_uint = unsigned int;
using lc_float = float;
using lc_bool = bool;
using lc_long = long long;
using lc_ulong = unsigned long long;

[[nodiscard]] __device__ inline bool isinf_impl(lc_float x) noexcept {
auto u = __float_as_int(x);
return u == 0x7f800000u | u == 0xff800000u;
}
[[nodiscard]] __device__ inline bool isnan_impl(lc_float x) noexcept {
auto u = __float_as_int(x);
return ((u & 0x7F800000u) == 0x7F800000u) & ((u & 0x7FFFFFu) != 0u);
}
[[nodiscard]] __device__ inline lc_float powi_impl(lc_float x, lc_int y) noexcept {
lc_float r = 1.0f;
auto is_y_neg = y < 0;
auto y_abs = is_y_neg ? -y : y;

while (y_abs) {
    if (y_abs & 1) r *= x;
    x *= x;
    y_abs >>= 1;
}
return is_y_neg ? 1.0f / r : r;
}
[[nodiscard]] __device__ inline lc_float powf_impl(lc_float x, lc_float y) noexcept {
auto y_int = static_cast<lc_int>(y);
return y_int == y ? powi_impl(x, y_int) : powf(x, y);
}



struct lc_half {
private:
    union U { __fp16 h; lc_ushort bits; };
public:
    lc_ushort bits;
    inline constexpr lc_half() noexcept : bits{0} {}
    [[nodiscard]] static inline constexpr auto from_bits(lc_ushort bits) noexcept {
        lc_half h;
        h.bits = bits;
        return h;
    }
    inline constexpr lc_half(float x) noexcept {
        U u;
        u.h = x;
        bits = u.bits;
    }
    template<typename T>
    inline constexpr operator T() const noexcept {
        U u;
        u.bits = bits;
        return static_cast<T>(static_cast<float>(u.h));
    }
    inline constexpr auto operator-() const noexcept { return from_bits(bits ^ 0x8000u); }
    inline constexpr auto operator+() const noexcept { return *this; }
    inline constexpr auto operator!() const noexcept { return bits == 0u || bits == 0x8000u; }
#define IMPL_HALF_BINOP(op)                                             inline constexpr auto operator op(lc_half rhs) const noexcept {         U u_lhs; u_lhs.bits = bits;                                         U u_rhs; u_rhs.bits = rhs.bits;                                     return lc_half{lc_float(u_lhs.h op u_rhs.h)};                   }
    IMPL_HALF_BINOP(+)
    IMPL_HALF_BINOP(-)
    IMPL_HALF_BINOP(*)
    IMPL_HALF_BINOP(/)
#undef IMPL_HALF_BINOP
#define IMPL_HALF_CMP(op) inline constexpr auto operator op(lc_half rhs) const noexcept { return float(*this) op float(rhs); }
    IMPL_HALF_CMP(==)
    IMPL_HALF_CMP(!=)
    IMPL_HALF_CMP(<)
    IMPL_HALF_CMP(<=)
    IMPL_HALF_CMP(>)
    IMPL_HALF_CMP(>=)

};
static_assert(sizeof(lc_half) == 2);
[[nodiscard]] inline lc_short __half_as_short(lc_half x) noexcept { 
    return x.bits;
}
[[nodiscard]] inline lc_half __short_as_half(lc_short x) noexcept {
    return lc_half::from_bits(x);
}
[[nodiscard]] inline lc_half __hmax(lc_half x, lc_half y) noexcept { return lc_half{lc_float(x) > lc_float(y) ? x : y}; }
[[nodiscard]] inline lc_half __hmin(lc_half x, lc_half y) noexcept { return lc_half{lc_float(x) < lc_float(y) ? x : y}; }
[[nodiscard]] inline lc_half __habs(lc_half x) noexcept { return lc_half{lc_float(x) < 0.0f ? -x : x}; }
[[nodiscard]] inline lc_half hexp2(lc_half x) noexcept { return lc_half{exp2f(lc_float(x))}; }
[[nodiscard]] inline lc_half hceil(lc_half x) noexcept { return lc_half{ceilf(lc_float(x))}; }
[[nodiscard]] inline lc_half hfloor(lc_half x) noexcept { return lc_half{floorf(lc_float(x))}; }
[[nodiscard]] inline lc_half htrunc(lc_half x) noexcept { return lc_half{truncf(lc_float(x))}; }
[[nodiscard]] inline lc_half hround(lc_half x) noexcept { return lc_half{roundf(lc_float(x))}; }
[[nodiscard]] inline lc_half hsqrt(lc_half x) noexcept { return lc_half{sqrtf(lc_float(x))}; }
[[nodiscard]] inline lc_half hrsqrt(lc_half x) noexcept { return lc_half{rsqrtf(lc_float(x))}; }
[[nodiscard]] inline lc_half __hfma(lc_half x, lc_half y, lc_half z) noexcept { return lc_half{fmaf(lc_float(x), lc_float(y), lc_float(z))}; }
[[nodiscard]] inline bool __hisnan(lc_half x) noexcept { return isnan_impl(lc_float(x)); }
[[nodiscard]] inline bool __hisinf(lc_half x) noexcept { return isinf_impl(lc_float(x)); }
    
struct alignas(2) lc_byte2 {
lc_byte x, y;
__device__ inline constexpr lc_byte2() noexcept
    : x{}, y{} {}
__device__ inline constexpr static auto zero() noexcept { return lc_byte2{}; }
__device__ inline constexpr static auto one() noexcept { return lc_byte2{1, 1}; }
__device__ inline explicit constexpr lc_byte2(lc_byte s) noexcept
    : x{s}, y{s} {}
__device__ inline constexpr lc_byte2(lc_byte x, lc_byte y) noexcept
    : x{x}, y{y} {}
__device__ inline constexpr auto &operator[](lc_uint i) noexcept { return (&x)[i]; }
__device__ inline constexpr auto operator[](lc_uint i) const noexcept { return (&x)[i]; }
};

struct alignas(4) lc_byte3 {
lc_byte x, y, z;
__device__ inline constexpr lc_byte3() noexcept
    : x{}, y{}, z{} {}
__device__ inline constexpr static auto zero() noexcept { return lc_byte3{}; }
__device__ inline constexpr static auto one() noexcept { return lc_byte3{1, 1, 1}; }
__device__ inline explicit constexpr lc_byte3(lc_byte s) noexcept
    : x{s}, y{s}, z{s} {}
__device__ inline constexpr lc_byte3(lc_byte x, lc_byte y, lc_byte z) noexcept
    : x{x}, y{y}, z{z} {}
__device__ inline constexpr auto &operator[](lc_uint i) noexcept { return (&x)[i]; }
__device__ inline constexpr auto operator[](lc_uint i) const noexcept { return (&x)[i]; }
};

struct alignas(4) lc_byte4 {
lc_byte x, y, z, w;
__device__ inline constexpr lc_byte4() noexcept
    : x{}, y{}, z{}, w{} {}
__device__ inline constexpr static auto zero() noexcept { return lc_byte4{}; }
__device__ inline constexpr static auto one() noexcept { return lc_byte4{1, 1, 1, 1}; }
__device__ inline explicit constexpr lc_byte4(lc_byte s) noexcept
    : x{s}, y{s}, z{s}, w{s} {}
__device__ inline constexpr lc_byte4(lc_byte x, lc_byte y, lc_byte z, lc_byte w) noexcept
    : x{x}, y{y}, z{z}, w{w} {}
__device__ inline constexpr auto &operator[](lc_uint i) noexcept { return (&x)[i]; }
__device__ inline constexpr auto operator[](lc_uint i) const noexcept { return (&x)[i]; }
};

struct alignas(2) lc_ubyte2 {
lc_ubyte x, y;
__device__ inline constexpr lc_ubyte2() noexcept
    : x{}, y{} {}
__device__ inline constexpr static auto zero() noexcept { return lc_ubyte2{}; }
__device__ inline constexpr static auto one() noexcept { return lc_ubyte2{1, 1}; }
__device__ inline explicit constexpr lc_ubyte2(lc_ubyte s) noexcept
    : x{s}, y{s} {}
__device__ inline constexpr lc_ubyte2(lc_ubyte x, lc_ubyte y) noexcept
    : x{x}, y{y} {}
__device__ inline constexpr auto &operator[](lc_uint i) noexcept { return (&x)[i]; }
__device__ inline constexpr auto operator[](lc_uint i) const noexcept { return (&x)[i]; }
};

struct alignas(4) lc_ubyte3 {
lc_ubyte x, y, z;
__device__ inline constexpr lc_ubyte3() noexcept
    : x{}, y{}, z{} {}
__device__ inline constexpr static auto zero() noexcept { return lc_ubyte3{}; }
__device__ inline constexpr static auto one() noexcept { return lc_ubyte3{1, 1, 1}; }
__device__ inline explicit constexpr lc_ubyte3(lc_ubyte s) noexcept
    : x{s}, y{s}, z{s} {}
__device__ inline constexpr lc_ubyte3(lc_ubyte x, lc_ubyte y, lc_ubyte z) noexcept
    : x{x}, y{y}, z{z} {}
__device__ inline constexpr auto &operator[](lc_uint i) noexcept { return (&x)[i]; }
__device__ inline constexpr auto operator[](lc_uint i) const noexcept { return (&x)[i]; }
};

struct alignas(4) lc_ubyte4 {
lc_ubyte x, y, z, w;
__device__ inline constexpr lc_ubyte4() noexcept
    : x{}, y{}, z{}, w{} {}
__device__ inline constexpr static auto zero() noexcept { return lc_ubyte4{}; }
__device__ inline constexpr static auto one() noexcept { return lc_ubyte4{1, 1, 1, 1}; }
__device__ inline explicit constexpr lc_ubyte4(lc_ubyte s) noexcept
    : x{s}, y{s}, z{s}, w{s} {}
__device__ inline constexpr lc_ubyte4(lc_ubyte x, lc_ubyte y, lc_ubyte z, lc_ubyte w) noexcept
    : x{x}, y{y}, z{z}, w{w} {}
__device__ inline constexpr auto &operator[](lc_uint i) noexcept { return (&x)[i]; }
__device__ inline constexpr auto operator[](lc_uint i) const noexcept { return (&x)[i]; }
};

struct alignas(4) lc_short2 {
lc_short x, y;
__device__ inline constexpr lc_short2() noexcept
    : x{}, y{} {}
__device__ inline constexpr static auto zero() noexcept { return lc_short2{}; }
__device__ inline constexpr static auto one() noexcept { return lc_short2{1, 1}; }
__device__ inline explicit constexpr lc_short2(lc_short s) noexcept
    : x{s}, y{s} {}
__device__ inline constexpr lc_short2(lc_short x, lc_short y) noexcept
    : x{x}, y{y} {}
__device__ inline constexpr auto &operator[](lc_uint i) noexcept { return (&x)[i]; }
__device__ inline constexpr auto operator[](lc_uint i) const noexcept { return (&x)[i]; }
};

struct alignas(8) lc_short3 {
lc_short x, y, z;
__device__ inline constexpr lc_short3() noexcept
    : x{}, y{}, z{} {}
__device__ inline constexpr static auto zero() noexcept { return lc_short3{}; }
__device__ inline constexpr static auto one() noexcept { return lc_short3{1, 1, 1}; }
__device__ inline explicit constexpr lc_short3(lc_short s) noexcept
    : x{s}, y{s}, z{s} {}
__device__ inline constexpr lc_short3(lc_short x, lc_short y, lc_short z) noexcept
    : x{x}, y{y}, z{z} {}
__device__ inline constexpr auto &operator[](lc_uint i) noexcept { return (&x)[i]; }
__device__ inline constexpr auto operator[](lc_uint i) const noexcept { return (&x)[i]; }
};

struct alignas(8) lc_short4 {
lc_short x, y, z, w;
__device__ inline constexpr lc_short4() noexcept
    : x{}, y{}, z{}, w{} {}
__device__ inline constexpr static auto zero() noexcept { return lc_short4{}; }
__device__ inline constexpr static auto one() noexcept { return lc_short4{1, 1, 1, 1}; }
__device__ inline explicit constexpr lc_short4(lc_short s) noexcept
    : x{s}, y{s}, z{s}, w{s} {}
__device__ inline constexpr lc_short4(lc_short x, lc_short y, lc_short z, lc_short w) noexcept
    : x{x}, y{y}, z{z}, w{w} {}
__device__ inline constexpr auto &operator[](lc_uint i) noexcept { return (&x)[i]; }
__device__ inline constexpr auto operator[](lc_uint i) const noexcept { return (&x)[i]; }
};

struct alignas(4) lc_ushort2 {
lc_ushort x, y;
__device__ inline constexpr lc_ushort2() noexcept
    : x{}, y{} {}
__device__ inline constexpr static auto zero() noexcept { return lc_ushort2{}; }
__device__ inline constexpr static auto one() noexcept { return lc_ushort2{1, 1}; }
__device__ inline explicit constexpr lc_ushort2(lc_ushort s) noexcept
    : x{s}, y{s} {}
__device__ inline constexpr lc_ushort2(lc_ushort x, lc_ushort y) noexcept
    : x{x}, y{y} {}
__device__ inline constexpr auto &operator[](lc_uint i) noexcept { return (&x)[i]; }
__device__ inline constexpr auto operator[](lc_uint i) const noexcept { return (&x)[i]; }
};

struct alignas(8) lc_ushort3 {
lc_ushort x, y, z;
__device__ inline constexpr lc_ushort3() noexcept
    : x{}, y{}, z{} {}
__device__ inline constexpr static auto zero() noexcept { return lc_ushort3{}; }
__device__ inline constexpr static auto one() noexcept { return lc_ushort3{1, 1, 1}; }
__device__ inline explicit constexpr lc_ushort3(lc_ushort s) noexcept
    : x{s}, y{s}, z{s} {}
__device__ inline constexpr lc_ushort3(lc_ushort x, lc_ushort y, lc_ushort z) noexcept
    : x{x}, y{y}, z{z} {}
__device__ inline constexpr auto &operator[](lc_uint i) noexcept { return (&x)[i]; }
__device__ inline constexpr auto operator[](lc_uint i) const noexcept { return (&x)[i]; }
};

struct alignas(8) lc_ushort4 {
lc_ushort x, y, z, w;
__device__ inline constexpr lc_ushort4() noexcept
    : x{}, y{}, z{}, w{} {}
__device__ inline constexpr static auto zero() noexcept { return lc_ushort4{}; }
__device__ inline constexpr static auto one() noexcept { return lc_ushort4{1, 1, 1, 1}; }
__device__ inline explicit constexpr lc_ushort4(lc_ushort s) noexcept
    : x{s}, y{s}, z{s}, w{s} {}
__device__ inline constexpr lc_ushort4(lc_ushort x, lc_ushort y, lc_ushort z, lc_ushort w) noexcept
    : x{x}, y{y}, z{z}, w{w} {}
__device__ inline constexpr auto &operator[](lc_uint i) noexcept { return (&x)[i]; }
__device__ inline constexpr auto operator[](lc_uint i) const noexcept { return (&x)[i]; }
};

struct alignas(8) lc_int2 {
lc_int x, y;
__device__ inline constexpr lc_int2() noexcept
    : x{}, y{} {}
__device__ inline constexpr static auto zero() noexcept { return lc_int2{}; }
__device__ inline constexpr static auto one() noexcept { return lc_int2{1, 1}; }
__device__ inline explicit constexpr lc_int2(lc_int s) noexcept
    : x{s}, y{s} {}
__device__ inline constexpr lc_int2(lc_int x, lc_int y) noexcept
    : x{x}, y{y} {}
__device__ inline constexpr auto &operator[](lc_uint i) noexcept { return (&x)[i]; }
__device__ inline constexpr auto operator[](lc_uint i) const noexcept { return (&x)[i]; }
};

struct alignas(16) lc_int3 {
lc_int x, y, z;
__device__ inline constexpr lc_int3() noexcept
    : x{}, y{}, z{} {}
__device__ inline constexpr static auto zero() noexcept { return lc_int3{}; }
__device__ inline constexpr static auto one() noexcept { return lc_int3{1, 1, 1}; }
__device__ inline explicit constexpr lc_int3(lc_int s) noexcept
    : x{s}, y{s}, z{s} {}
__device__ inline constexpr lc_int3(lc_int x, lc_int y, lc_int z) noexcept
    : x{x}, y{y}, z{z} {}
__device__ inline constexpr auto &operator[](lc_uint i) noexcept { return (&x)[i]; }
__device__ inline constexpr auto operator[](lc_uint i) const noexcept { return (&x)[i]; }
};

struct alignas(16) lc_int4 {
lc_int x, y, z, w;
__device__ inline constexpr lc_int4() noexcept
    : x{}, y{}, z{}, w{} {}
__device__ inline constexpr static auto zero() noexcept { return lc_int4{}; }
__device__ inline constexpr static auto one() noexcept { return lc_int4{1, 1, 1, 1}; }
__device__ inline explicit constexpr lc_int4(lc_int s) noexcept
    : x{s}, y{s}, z{s}, w{s} {}
__device__ inline constexpr lc_int4(lc_int x, lc_int y, lc_int z, lc_int w) noexcept
    : x{x}, y{y}, z{z}, w{w} {}
__device__ inline constexpr auto &operator[](lc_uint i) noexcept { return (&x)[i]; }
__device__ inline constexpr auto operator[](lc_uint i) const noexcept { return (&x)[i]; }
};

struct alignas(8) lc_uint2 {
lc_uint x, y;
__device__ inline constexpr lc_uint2() noexcept
    : x{}, y{} {}
__device__ inline constexpr static auto zero() noexcept { return lc_uint2{}; }
__device__ inline constexpr static auto one() noexcept { return lc_uint2{1, 1}; }
__device__ inline explicit constexpr lc_uint2(lc_uint s) noexcept
    : x{s}, y{s} {}
__device__ inline constexpr lc_uint2(lc_uint x, lc_uint y) noexcept
    : x{x}, y{y} {}
__device__ inline constexpr auto &operator[](lc_uint i) noexcept { return (&x)[i]; }
__device__ inline constexpr auto operator[](lc_uint i) const noexcept { return (&x)[i]; }
};

struct alignas(16) lc_uint3 {
lc_uint x, y, z;
__device__ inline constexpr lc_uint3() noexcept
    : x{}, y{}, z{} {}
__device__ inline constexpr static auto zero() noexcept { return lc_uint3{}; }
__device__ inline constexpr static auto one() noexcept { return lc_uint3{1, 1, 1}; }
__device__ inline explicit constexpr lc_uint3(lc_uint s) noexcept
    : x{s}, y{s}, z{s} {}
__device__ inline constexpr lc_uint3(lc_uint x, lc_uint y, lc_uint z) noexcept
    : x{x}, y{y}, z{z} {}
__device__ inline constexpr auto &operator[](lc_uint i) noexcept { return (&x)[i]; }
__device__ inline constexpr auto operator[](lc_uint i) const noexcept { return (&x)[i]; }
};

struct alignas(16) lc_uint4 {
lc_uint x, y, z, w;
__device__ inline constexpr lc_uint4() noexcept
    : x{}, y{}, z{}, w{} {}
__device__ inline constexpr static auto zero() noexcept { return lc_uint4{}; }
__device__ inline constexpr static auto one() noexcept { return lc_uint4{1, 1, 1, 1}; }
__device__ inline explicit constexpr lc_uint4(lc_uint s) noexcept
    : x{s}, y{s}, z{s}, w{s} {}
__device__ inline constexpr lc_uint4(lc_uint x, lc_uint y, lc_uint z, lc_uint w) noexcept
    : x{x}, y{y}, z{z}, w{w} {}
__device__ inline constexpr auto &operator[](lc_uint i) noexcept { return (&x)[i]; }
__device__ inline constexpr auto operator[](lc_uint i) const noexcept { return (&x)[i]; }
};

struct alignas(4) lc_half2 {
lc_half x, y;
__device__ inline constexpr lc_half2() noexcept
    : x{}, y{} {}
__device__ inline constexpr static auto zero() noexcept { return lc_half2{}; }
__device__ inline constexpr static auto one() noexcept { return lc_half2{1, 1}; }
__device__ inline explicit constexpr lc_half2(lc_half s) noexcept
    : x{s}, y{s} {}
__device__ inline constexpr lc_half2(lc_half x, lc_half y) noexcept
    : x{x}, y{y} {}
__device__ inline constexpr auto &operator[](lc_uint i) noexcept { return (&x)[i]; }
__device__ inline constexpr auto operator[](lc_uint i) const noexcept { return (&x)[i]; }
};

struct alignas(8) lc_half3 {
lc_half x, y, z;
__device__ inline constexpr lc_half3() noexcept
    : x{}, y{}, z{} {}
__device__ inline constexpr static auto zero() noexcept { return lc_half3{}; }
__device__ inline constexpr static auto one() noexcept { return lc_half3{1, 1, 1}; }
__device__ inline explicit constexpr lc_half3(lc_half s) noexcept
    : x{s}, y{s}, z{s} {}
__device__ inline constexpr lc_half3(lc_half x, lc_half y, lc_half z) noexcept
    : x{x}, y{y}, z{z} {}
__device__ inline constexpr auto &operator[](lc_uint i) noexcept { return (&x)[i]; }
__device__ inline constexpr auto operator[](lc_uint i) const noexcept { return (&x)[i]; }
};

struct alignas(8) lc_half4 {
lc_half x, y, z, w;
__device__ inline constexpr lc_half4() noexcept
    : x{}, y{}, z{}, w{} {}
__device__ inline constexpr static auto zero() noexcept { return lc_half4{}; }
__device__ inline constexpr static auto one() noexcept { return lc_half4{1, 1, 1, 1}; }
__device__ inline explicit constexpr lc_half4(lc_half s) noexcept
    : x{s}, y{s}, z{s}, w{s} {}
__device__ inline constexpr lc_half4(lc_half x, lc_half y, lc_half z, lc_half w) noexcept
    : x{x}, y{y}, z{z}, w{w} {}
__device__ inline constexpr auto &operator[](lc_uint i) noexcept { return (&x)[i]; }
__device__ inline constexpr auto operator[](lc_uint i) const noexcept { return (&x)[i]; }
};

struct alignas(8) lc_float2 {
lc_float x, y;
__device__ inline constexpr lc_float2() noexcept
    : x{}, y{} {}
__device__ inline constexpr static auto zero() noexcept { return lc_float2{}; }
__device__ inline constexpr static auto one() noexcept { return lc_float2{1, 1}; }
__device__ inline explicit constexpr lc_float2(lc_float s) noexcept
    : x{s}, y{s} {}
__device__ inline constexpr lc_float2(lc_float x, lc_float y) noexcept
    : x{x}, y{y} {}
__device__ inline constexpr auto &operator[](lc_uint i) noexcept { return (&x)[i]; }
__device__ inline constexpr auto operator[](lc_uint i) const noexcept { return (&x)[i]; }
};

struct alignas(16) lc_float3 {
lc_float x, y, z;
__device__ inline constexpr lc_float3() noexcept
    : x{}, y{}, z{} {}
__device__ inline constexpr static auto zero() noexcept { return lc_float3{}; }
__device__ inline constexpr static auto one() noexcept { return lc_float3{1, 1, 1}; }
__device__ inline explicit constexpr lc_float3(lc_float s) noexcept
    : x{s}, y{s}, z{s} {}
__device__ inline constexpr lc_float3(lc_float x, lc_float y, lc_float z) noexcept
    : x{x}, y{y}, z{z} {}
__device__ inline constexpr auto &operator[](lc_uint i) noexcept { return (&x)[i]; }
__device__ inline constexpr auto operator[](lc_uint i) const noexcept { return (&x)[i]; }
};

struct alignas(16) lc_float4 {
lc_float x, y, z, w;
__device__ inline constexpr lc_float4() noexcept
    : x{}, y{}, z{}, w{} {}
__device__ inline constexpr static auto zero() noexcept { return lc_float4{}; }
__device__ inline constexpr static auto one() noexcept { return lc_float4{1, 1, 1, 1}; }
__device__ inline explicit constexpr lc_float4(lc_float s) noexcept
    : x{s}, y{s}, z{s}, w{s} {}
__device__ inline constexpr lc_float4(lc_float x, lc_float y, lc_float z, lc_float w) noexcept
    : x{x}, y{y}, z{z}, w{w} {}
__device__ inline constexpr auto &operator[](lc_uint i) noexcept { return (&x)[i]; }
__device__ inline constexpr auto operator[](lc_uint i) const noexcept { return (&x)[i]; }
};

struct alignas(2) lc_bool2 {
lc_bool x, y;
__device__ inline constexpr lc_bool2() noexcept
    : x{}, y{} {}
__device__ inline constexpr static auto zero() noexcept { return lc_bool2{}; }
__device__ inline constexpr static auto one() noexcept { return lc_bool2{1, 1}; }
__device__ inline explicit constexpr lc_bool2(lc_bool s) noexcept
    : x{s}, y{s} {}
__device__ inline constexpr lc_bool2(lc_bool x, lc_bool y) noexcept
    : x{x}, y{y} {}
__device__ inline constexpr auto &operator[](lc_uint i) noexcept { return (&x)[i]; }
__device__ inline constexpr auto operator[](lc_uint i) const noexcept { return (&x)[i]; }
};

struct alignas(4) lc_bool3 {
lc_bool x, y, z;
__device__ inline constexpr lc_bool3() noexcept
    : x{}, y{}, z{} {}
__device__ inline constexpr static auto zero() noexcept { return lc_bool3{}; }
__device__ inline constexpr static auto one() noexcept { return lc_bool3{1, 1, 1}; }
__device__ inline explicit constexpr lc_bool3(lc_bool s) noexcept
    : x{s}, y{s}, z{s} {}
__device__ inline constexpr lc_bool3(lc_bool x, lc_bool y, lc_bool z) noexcept
    : x{x}, y{y}, z{z} {}
__device__ inline constexpr auto &operator[](lc_uint i) noexcept { return (&x)[i]; }
__device__ inline constexpr auto operator[](lc_uint i) const noexcept { return (&x)[i]; }
};

struct alignas(4) lc_bool4 {
lc_bool x, y, z, w;
__device__ inline constexpr lc_bool4() noexcept
    : x{}, y{}, z{}, w{} {}
__device__ inline constexpr static auto zero() noexcept { return lc_bool4{}; }
__device__ inline constexpr static auto one() noexcept { return lc_bool4{1, 1, 1, 1}; }
__device__ inline explicit constexpr lc_bool4(lc_bool s) noexcept
    : x{s}, y{s}, z{s}, w{s} {}
__device__ inline constexpr lc_bool4(lc_bool x, lc_bool y, lc_bool z, lc_bool w) noexcept
    : x{x}, y{y}, z{z}, w{w} {}
__device__ inline constexpr auto &operator[](lc_uint i) noexcept { return (&x)[i]; }
__device__ inline constexpr auto operator[](lc_uint i) const noexcept { return (&x)[i]; }
};

struct alignas(16) lc_long2 {
lc_long x, y;
__device__ inline constexpr lc_long2() noexcept
    : x{}, y{} {}
__device__ inline constexpr static auto zero() noexcept { return lc_long2{}; }
__device__ inline constexpr static auto one() noexcept { return lc_long2{1, 1}; }
__device__ inline explicit constexpr lc_long2(lc_long s) noexcept
    : x{s}, y{s} {}
__device__ inline constexpr lc_long2(lc_long x, lc_long y) noexcept
    : x{x}, y{y} {}
__device__ inline constexpr auto &operator[](lc_uint i) noexcept { return (&x)[i]; }
__device__ inline constexpr auto operator[](lc_uint i) const noexcept { return (&x)[i]; }
};

struct alignas(16) lc_long3 {
lc_long x, y, z;
__device__ inline constexpr lc_long3() noexcept
    : x{}, y{}, z{} {}
__device__ inline constexpr static auto zero() noexcept { return lc_long3{}; }
__device__ inline constexpr static auto one() noexcept { return lc_long3{1, 1, 1}; }
__device__ inline explicit constexpr lc_long3(lc_long s) noexcept
    : x{s}, y{s}, z{s} {}
__device__ inline constexpr lc_long3(lc_long x, lc_long y, lc_long z) noexcept
    : x{x}, y{y}, z{z} {}
__device__ inline constexpr auto &operator[](lc_uint i) noexcept { return (&x)[i]; }
__device__ inline constexpr auto operator[](lc_uint i) const noexcept { return (&x)[i]; }
};

struct alignas(16) lc_long4 {
lc_long x, y, z, w;
__device__ inline constexpr lc_long4() noexcept
    : x{}, y{}, z{}, w{} {}
__device__ inline constexpr static auto zero() noexcept { return lc_long4{}; }
__device__ inline constexpr static auto one() noexcept { return lc_long4{1, 1, 1, 1}; }
__device__ inline explicit constexpr lc_long4(lc_long s) noexcept
    : x{s}, y{s}, z{s}, w{s} {}
__device__ inline constexpr lc_long4(lc_long x, lc_long y, lc_long z, lc_long w) noexcept
    : x{x}, y{y}, z{z}, w{w} {}
__device__ inline constexpr auto &operator[](lc_uint i) noexcept { return (&x)[i]; }
__device__ inline constexpr auto operator[](lc_uint i) const noexcept { return (&x)[i]; }
};

struct alignas(16) lc_ulong2 {
lc_ulong x, y;
__device__ inline constexpr lc_ulong2() noexcept
    : x{}, y{} {}
__device__ inline constexpr static auto zero() noexcept { return lc_ulong2{}; }
__device__ inline constexpr static auto one() noexcept { return lc_ulong2{1, 1}; }
__device__ inline explicit constexpr lc_ulong2(lc_ulong s) noexcept
    : x{s}, y{s} {}
__device__ inline constexpr lc_ulong2(lc_ulong x, lc_ulong y) noexcept
    : x{x}, y{y} {}
__device__ inline constexpr auto &operator[](lc_uint i) noexcept { return (&x)[i]; }
__device__ inline constexpr auto operator[](lc_uint i) const noexcept { return (&x)[i]; }
};

struct alignas(16) lc_ulong3 {
lc_ulong x, y, z;
__device__ inline constexpr lc_ulong3() noexcept
    : x{}, y{}, z{} {}
__device__ inline constexpr static auto zero() noexcept { return lc_ulong3{}; }
__device__ inline constexpr static auto one() noexcept { return lc_ulong3{1, 1, 1}; }
__device__ inline explicit constexpr lc_ulong3(lc_ulong s) noexcept
    : x{s}, y{s}, z{s} {}
__device__ inline constexpr lc_ulong3(lc_ulong x, lc_ulong y, lc_ulong z) noexcept
    : x{x}, y{y}, z{z} {}
__device__ inline constexpr auto &operator[](lc_uint i) noexcept { return (&x)[i]; }
__device__ inline constexpr auto operator[](lc_uint i) const noexcept { return (&x)[i]; }
};

struct alignas(16) lc_ulong4 {
lc_ulong x, y, z, w;
__device__ inline constexpr lc_ulong4() noexcept
    : x{}, y{}, z{}, w{} {}
__device__ inline constexpr static auto zero() noexcept { return lc_ulong4{}; }
__device__ inline constexpr static auto one() noexcept { return lc_ulong4{1, 1, 1, 1}; }
__device__ inline explicit constexpr lc_ulong4(lc_ulong s) noexcept
    : x{s}, y{s}, z{s}, w{s} {}
__device__ inline constexpr lc_ulong4(lc_ulong x, lc_ulong y, lc_ulong z, lc_ulong w) noexcept
    : x{x}, y{y}, z{z}, w{w} {}
__device__ inline constexpr auto &operator[](lc_uint i) noexcept { return (&x)[i]; }
__device__ inline constexpr auto operator[](lc_uint i) const noexcept { return (&x)[i]; }
};

[[nodiscard]] __device__ inline constexpr auto lc_make_byte2(lc_byte s = 0) noexcept { return lc_byte2{s, s}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_byte2(lc_byte x, lc_byte y) noexcept { return lc_byte2{x, y}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_byte2(lc_byte2 v) noexcept { return lc_byte2{static_cast<lc_byte>(v.x), static_cast<lc_byte>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_byte2(lc_byte3 v) noexcept { return lc_byte2{static_cast<lc_byte>(v.x), static_cast<lc_byte>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_byte2(lc_byte4 v) noexcept { return lc_byte2{static_cast<lc_byte>(v.x), static_cast<lc_byte>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_byte2(lc_ubyte2 v) noexcept { return lc_byte2{static_cast<lc_byte>(v.x), static_cast<lc_byte>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_byte2(lc_ubyte3 v) noexcept { return lc_byte2{static_cast<lc_byte>(v.x), static_cast<lc_byte>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_byte2(lc_ubyte4 v) noexcept { return lc_byte2{static_cast<lc_byte>(v.x), static_cast<lc_byte>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_byte2(lc_short2 v) noexcept { return lc_byte2{static_cast<lc_byte>(v.x), static_cast<lc_byte>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_byte2(lc_short3 v) noexcept { return lc_byte2{static_cast<lc_byte>(v.x), static_cast<lc_byte>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_byte2(lc_short4 v) noexcept { return lc_byte2{static_cast<lc_byte>(v.x), static_cast<lc_byte>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_byte2(lc_ushort2 v) noexcept { return lc_byte2{static_cast<lc_byte>(v.x), static_cast<lc_byte>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_byte2(lc_ushort3 v) noexcept { return lc_byte2{static_cast<lc_byte>(v.x), static_cast<lc_byte>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_byte2(lc_ushort4 v) noexcept { return lc_byte2{static_cast<lc_byte>(v.x), static_cast<lc_byte>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_byte2(lc_int2 v) noexcept { return lc_byte2{static_cast<lc_byte>(v.x), static_cast<lc_byte>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_byte2(lc_int3 v) noexcept { return lc_byte2{static_cast<lc_byte>(v.x), static_cast<lc_byte>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_byte2(lc_int4 v) noexcept { return lc_byte2{static_cast<lc_byte>(v.x), static_cast<lc_byte>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_byte2(lc_uint2 v) noexcept { return lc_byte2{static_cast<lc_byte>(v.x), static_cast<lc_byte>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_byte2(lc_uint3 v) noexcept { return lc_byte2{static_cast<lc_byte>(v.x), static_cast<lc_byte>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_byte2(lc_uint4 v) noexcept { return lc_byte2{static_cast<lc_byte>(v.x), static_cast<lc_byte>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_byte2(lc_half2 v) noexcept { return lc_byte2{static_cast<lc_byte>(v.x), static_cast<lc_byte>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_byte2(lc_half3 v) noexcept { return lc_byte2{static_cast<lc_byte>(v.x), static_cast<lc_byte>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_byte2(lc_half4 v) noexcept { return lc_byte2{static_cast<lc_byte>(v.x), static_cast<lc_byte>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_byte2(lc_float2 v) noexcept { return lc_byte2{static_cast<lc_byte>(v.x), static_cast<lc_byte>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_byte2(lc_float3 v) noexcept { return lc_byte2{static_cast<lc_byte>(v.x), static_cast<lc_byte>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_byte2(lc_float4 v) noexcept { return lc_byte2{static_cast<lc_byte>(v.x), static_cast<lc_byte>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_byte2(lc_bool2 v) noexcept { return lc_byte2{static_cast<lc_byte>(v.x), static_cast<lc_byte>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_byte2(lc_bool3 v) noexcept { return lc_byte2{static_cast<lc_byte>(v.x), static_cast<lc_byte>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_byte2(lc_bool4 v) noexcept { return lc_byte2{static_cast<lc_byte>(v.x), static_cast<lc_byte>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_byte2(lc_long2 v) noexcept { return lc_byte2{static_cast<lc_byte>(v.x), static_cast<lc_byte>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_byte2(lc_long3 v) noexcept { return lc_byte2{static_cast<lc_byte>(v.x), static_cast<lc_byte>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_byte2(lc_long4 v) noexcept { return lc_byte2{static_cast<lc_byte>(v.x), static_cast<lc_byte>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_byte2(lc_ulong2 v) noexcept { return lc_byte2{static_cast<lc_byte>(v.x), static_cast<lc_byte>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_byte2(lc_ulong3 v) noexcept { return lc_byte2{static_cast<lc_byte>(v.x), static_cast<lc_byte>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_byte2(lc_ulong4 v) noexcept { return lc_byte2{static_cast<lc_byte>(v.x), static_cast<lc_byte>(v.y)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_byte3(lc_byte s = 0) noexcept { return lc_byte3{s, s, s}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_byte3(lc_byte x, lc_byte y, lc_byte z) noexcept { return lc_byte3{x, y, z}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_byte3(lc_byte x, lc_byte2 yz) noexcept { return lc_byte3{x, yz.x, yz.y}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_byte3(lc_byte2 xy, lc_byte z) noexcept { return lc_byte3{xy.x, xy.y, z}; }
[[nodiscard]] __device__ constexpr auto lc_make_byte3(lc_byte3 v) noexcept { return lc_byte3{static_cast<lc_byte>(v.x), static_cast<lc_byte>(v.y), static_cast<lc_byte>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_byte3(lc_byte4 v) noexcept { return lc_byte3{static_cast<lc_byte>(v.x), static_cast<lc_byte>(v.y), static_cast<lc_byte>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_byte3(lc_ubyte3 v) noexcept { return lc_byte3{static_cast<lc_byte>(v.x), static_cast<lc_byte>(v.y), static_cast<lc_byte>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_byte3(lc_ubyte4 v) noexcept { return lc_byte3{static_cast<lc_byte>(v.x), static_cast<lc_byte>(v.y), static_cast<lc_byte>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_byte3(lc_short3 v) noexcept { return lc_byte3{static_cast<lc_byte>(v.x), static_cast<lc_byte>(v.y), static_cast<lc_byte>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_byte3(lc_short4 v) noexcept { return lc_byte3{static_cast<lc_byte>(v.x), static_cast<lc_byte>(v.y), static_cast<lc_byte>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_byte3(lc_ushort3 v) noexcept { return lc_byte3{static_cast<lc_byte>(v.x), static_cast<lc_byte>(v.y), static_cast<lc_byte>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_byte3(lc_ushort4 v) noexcept { return lc_byte3{static_cast<lc_byte>(v.x), static_cast<lc_byte>(v.y), static_cast<lc_byte>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_byte3(lc_int3 v) noexcept { return lc_byte3{static_cast<lc_byte>(v.x), static_cast<lc_byte>(v.y), static_cast<lc_byte>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_byte3(lc_int4 v) noexcept { return lc_byte3{static_cast<lc_byte>(v.x), static_cast<lc_byte>(v.y), static_cast<lc_byte>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_byte3(lc_uint3 v) noexcept { return lc_byte3{static_cast<lc_byte>(v.x), static_cast<lc_byte>(v.y), static_cast<lc_byte>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_byte3(lc_uint4 v) noexcept { return lc_byte3{static_cast<lc_byte>(v.x), static_cast<lc_byte>(v.y), static_cast<lc_byte>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_byte3(lc_half3 v) noexcept { return lc_byte3{static_cast<lc_byte>(v.x), static_cast<lc_byte>(v.y), static_cast<lc_byte>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_byte3(lc_half4 v) noexcept { return lc_byte3{static_cast<lc_byte>(v.x), static_cast<lc_byte>(v.y), static_cast<lc_byte>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_byte3(lc_float3 v) noexcept { return lc_byte3{static_cast<lc_byte>(v.x), static_cast<lc_byte>(v.y), static_cast<lc_byte>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_byte3(lc_float4 v) noexcept { return lc_byte3{static_cast<lc_byte>(v.x), static_cast<lc_byte>(v.y), static_cast<lc_byte>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_byte3(lc_bool3 v) noexcept { return lc_byte3{static_cast<lc_byte>(v.x), static_cast<lc_byte>(v.y), static_cast<lc_byte>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_byte3(lc_bool4 v) noexcept { return lc_byte3{static_cast<lc_byte>(v.x), static_cast<lc_byte>(v.y), static_cast<lc_byte>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_byte3(lc_long3 v) noexcept { return lc_byte3{static_cast<lc_byte>(v.x), static_cast<lc_byte>(v.y), static_cast<lc_byte>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_byte3(lc_long4 v) noexcept { return lc_byte3{static_cast<lc_byte>(v.x), static_cast<lc_byte>(v.y), static_cast<lc_byte>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_byte3(lc_ulong3 v) noexcept { return lc_byte3{static_cast<lc_byte>(v.x), static_cast<lc_byte>(v.y), static_cast<lc_byte>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_byte3(lc_ulong4 v) noexcept { return lc_byte3{static_cast<lc_byte>(v.x), static_cast<lc_byte>(v.y), static_cast<lc_byte>(v.z)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_byte4(lc_byte s = 0) noexcept { return lc_byte4{s, s, s, s}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_byte4(lc_byte x, lc_byte y, lc_byte z, lc_byte w) noexcept { return lc_byte4{x, y, z, w}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_byte4(lc_byte x, lc_byte y, lc_byte2 zw) noexcept { return lc_byte4{x, y, zw.x, zw.y}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_byte4(lc_byte x, lc_byte2 yz, lc_byte w) noexcept { return lc_byte4{x, yz.x, yz.y, w}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_byte4(lc_byte2 xy, lc_byte z, lc_byte w) noexcept { return lc_byte4{xy.x, xy.y, z, w}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_byte4(lc_byte2 xy, lc_byte2 zw) noexcept { return lc_byte4{xy.x, xy.y, zw.x, zw.y}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_byte4(lc_byte x, lc_byte3 yzw) noexcept { return lc_byte4{x, yzw.x, yzw.y, yzw.z}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_byte4(lc_byte3 xyz, lc_byte w) noexcept { return lc_byte4{xyz.x, xyz.y, xyz.z, w}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_byte4(lc_byte4 v) noexcept { return lc_byte4{static_cast<lc_byte>(v.x), static_cast<lc_byte>(v.y), static_cast<lc_byte>(v.z), static_cast<lc_byte>(v.w)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_byte4(lc_ubyte4 v) noexcept { return lc_byte4{static_cast<lc_byte>(v.x), static_cast<lc_byte>(v.y), static_cast<lc_byte>(v.z), static_cast<lc_byte>(v.w)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_byte4(lc_short4 v) noexcept { return lc_byte4{static_cast<lc_byte>(v.x), static_cast<lc_byte>(v.y), static_cast<lc_byte>(v.z), static_cast<lc_byte>(v.w)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_byte4(lc_ushort4 v) noexcept { return lc_byte4{static_cast<lc_byte>(v.x), static_cast<lc_byte>(v.y), static_cast<lc_byte>(v.z), static_cast<lc_byte>(v.w)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_byte4(lc_int4 v) noexcept { return lc_byte4{static_cast<lc_byte>(v.x), static_cast<lc_byte>(v.y), static_cast<lc_byte>(v.z), static_cast<lc_byte>(v.w)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_byte4(lc_uint4 v) noexcept { return lc_byte4{static_cast<lc_byte>(v.x), static_cast<lc_byte>(v.y), static_cast<lc_byte>(v.z), static_cast<lc_byte>(v.w)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_byte4(lc_half4 v) noexcept { return lc_byte4{static_cast<lc_byte>(v.x), static_cast<lc_byte>(v.y), static_cast<lc_byte>(v.z), static_cast<lc_byte>(v.w)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_byte4(lc_float4 v) noexcept { return lc_byte4{static_cast<lc_byte>(v.x), static_cast<lc_byte>(v.y), static_cast<lc_byte>(v.z), static_cast<lc_byte>(v.w)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_byte4(lc_bool4 v) noexcept { return lc_byte4{static_cast<lc_byte>(v.x), static_cast<lc_byte>(v.y), static_cast<lc_byte>(v.z), static_cast<lc_byte>(v.w)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_byte4(lc_long4 v) noexcept { return lc_byte4{static_cast<lc_byte>(v.x), static_cast<lc_byte>(v.y), static_cast<lc_byte>(v.z), static_cast<lc_byte>(v.w)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_byte4(lc_ulong4 v) noexcept { return lc_byte4{static_cast<lc_byte>(v.x), static_cast<lc_byte>(v.y), static_cast<lc_byte>(v.z), static_cast<lc_byte>(v.w)}; }

[[nodiscard]] __device__ inline constexpr auto lc_make_ubyte2(lc_ubyte s = 0) noexcept { return lc_ubyte2{s, s}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ubyte2(lc_ubyte x, lc_ubyte y) noexcept { return lc_ubyte2{x, y}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ubyte2(lc_byte2 v) noexcept { return lc_ubyte2{static_cast<lc_ubyte>(v.x), static_cast<lc_ubyte>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ubyte2(lc_byte3 v) noexcept { return lc_ubyte2{static_cast<lc_ubyte>(v.x), static_cast<lc_ubyte>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ubyte2(lc_byte4 v) noexcept { return lc_ubyte2{static_cast<lc_ubyte>(v.x), static_cast<lc_ubyte>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ubyte2(lc_ubyte2 v) noexcept { return lc_ubyte2{static_cast<lc_ubyte>(v.x), static_cast<lc_ubyte>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ubyte2(lc_ubyte3 v) noexcept { return lc_ubyte2{static_cast<lc_ubyte>(v.x), static_cast<lc_ubyte>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ubyte2(lc_ubyte4 v) noexcept { return lc_ubyte2{static_cast<lc_ubyte>(v.x), static_cast<lc_ubyte>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ubyte2(lc_short2 v) noexcept { return lc_ubyte2{static_cast<lc_ubyte>(v.x), static_cast<lc_ubyte>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ubyte2(lc_short3 v) noexcept { return lc_ubyte2{static_cast<lc_ubyte>(v.x), static_cast<lc_ubyte>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ubyte2(lc_short4 v) noexcept { return lc_ubyte2{static_cast<lc_ubyte>(v.x), static_cast<lc_ubyte>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ubyte2(lc_ushort2 v) noexcept { return lc_ubyte2{static_cast<lc_ubyte>(v.x), static_cast<lc_ubyte>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ubyte2(lc_ushort3 v) noexcept { return lc_ubyte2{static_cast<lc_ubyte>(v.x), static_cast<lc_ubyte>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ubyte2(lc_ushort4 v) noexcept { return lc_ubyte2{static_cast<lc_ubyte>(v.x), static_cast<lc_ubyte>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ubyte2(lc_int2 v) noexcept { return lc_ubyte2{static_cast<lc_ubyte>(v.x), static_cast<lc_ubyte>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ubyte2(lc_int3 v) noexcept { return lc_ubyte2{static_cast<lc_ubyte>(v.x), static_cast<lc_ubyte>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ubyte2(lc_int4 v) noexcept { return lc_ubyte2{static_cast<lc_ubyte>(v.x), static_cast<lc_ubyte>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ubyte2(lc_uint2 v) noexcept { return lc_ubyte2{static_cast<lc_ubyte>(v.x), static_cast<lc_ubyte>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ubyte2(lc_uint3 v) noexcept { return lc_ubyte2{static_cast<lc_ubyte>(v.x), static_cast<lc_ubyte>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ubyte2(lc_uint4 v) noexcept { return lc_ubyte2{static_cast<lc_ubyte>(v.x), static_cast<lc_ubyte>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ubyte2(lc_half2 v) noexcept { return lc_ubyte2{static_cast<lc_ubyte>(v.x), static_cast<lc_ubyte>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ubyte2(lc_half3 v) noexcept { return lc_ubyte2{static_cast<lc_ubyte>(v.x), static_cast<lc_ubyte>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ubyte2(lc_half4 v) noexcept { return lc_ubyte2{static_cast<lc_ubyte>(v.x), static_cast<lc_ubyte>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ubyte2(lc_float2 v) noexcept { return lc_ubyte2{static_cast<lc_ubyte>(v.x), static_cast<lc_ubyte>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ubyte2(lc_float3 v) noexcept { return lc_ubyte2{static_cast<lc_ubyte>(v.x), static_cast<lc_ubyte>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ubyte2(lc_float4 v) noexcept { return lc_ubyte2{static_cast<lc_ubyte>(v.x), static_cast<lc_ubyte>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ubyte2(lc_bool2 v) noexcept { return lc_ubyte2{static_cast<lc_ubyte>(v.x), static_cast<lc_ubyte>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ubyte2(lc_bool3 v) noexcept { return lc_ubyte2{static_cast<lc_ubyte>(v.x), static_cast<lc_ubyte>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ubyte2(lc_bool4 v) noexcept { return lc_ubyte2{static_cast<lc_ubyte>(v.x), static_cast<lc_ubyte>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ubyte2(lc_long2 v) noexcept { return lc_ubyte2{static_cast<lc_ubyte>(v.x), static_cast<lc_ubyte>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ubyte2(lc_long3 v) noexcept { return lc_ubyte2{static_cast<lc_ubyte>(v.x), static_cast<lc_ubyte>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ubyte2(lc_long4 v) noexcept { return lc_ubyte2{static_cast<lc_ubyte>(v.x), static_cast<lc_ubyte>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ubyte2(lc_ulong2 v) noexcept { return lc_ubyte2{static_cast<lc_ubyte>(v.x), static_cast<lc_ubyte>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ubyte2(lc_ulong3 v) noexcept { return lc_ubyte2{static_cast<lc_ubyte>(v.x), static_cast<lc_ubyte>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ubyte2(lc_ulong4 v) noexcept { return lc_ubyte2{static_cast<lc_ubyte>(v.x), static_cast<lc_ubyte>(v.y)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_ubyte3(lc_ubyte s = 0) noexcept { return lc_ubyte3{s, s, s}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ubyte3(lc_ubyte x, lc_ubyte y, lc_ubyte z) noexcept { return lc_ubyte3{x, y, z}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ubyte3(lc_ubyte x, lc_ubyte2 yz) noexcept { return lc_ubyte3{x, yz.x, yz.y}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ubyte3(lc_ubyte2 xy, lc_ubyte z) noexcept { return lc_ubyte3{xy.x, xy.y, z}; }
[[nodiscard]] __device__ constexpr auto lc_make_ubyte3(lc_byte3 v) noexcept { return lc_ubyte3{static_cast<lc_ubyte>(v.x), static_cast<lc_ubyte>(v.y), static_cast<lc_ubyte>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_ubyte3(lc_byte4 v) noexcept { return lc_ubyte3{static_cast<lc_ubyte>(v.x), static_cast<lc_ubyte>(v.y), static_cast<lc_ubyte>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_ubyte3(lc_ubyte3 v) noexcept { return lc_ubyte3{static_cast<lc_ubyte>(v.x), static_cast<lc_ubyte>(v.y), static_cast<lc_ubyte>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_ubyte3(lc_ubyte4 v) noexcept { return lc_ubyte3{static_cast<lc_ubyte>(v.x), static_cast<lc_ubyte>(v.y), static_cast<lc_ubyte>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_ubyte3(lc_short3 v) noexcept { return lc_ubyte3{static_cast<lc_ubyte>(v.x), static_cast<lc_ubyte>(v.y), static_cast<lc_ubyte>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_ubyte3(lc_short4 v) noexcept { return lc_ubyte3{static_cast<lc_ubyte>(v.x), static_cast<lc_ubyte>(v.y), static_cast<lc_ubyte>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_ubyte3(lc_ushort3 v) noexcept { return lc_ubyte3{static_cast<lc_ubyte>(v.x), static_cast<lc_ubyte>(v.y), static_cast<lc_ubyte>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_ubyte3(lc_ushort4 v) noexcept { return lc_ubyte3{static_cast<lc_ubyte>(v.x), static_cast<lc_ubyte>(v.y), static_cast<lc_ubyte>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_ubyte3(lc_int3 v) noexcept { return lc_ubyte3{static_cast<lc_ubyte>(v.x), static_cast<lc_ubyte>(v.y), static_cast<lc_ubyte>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_ubyte3(lc_int4 v) noexcept { return lc_ubyte3{static_cast<lc_ubyte>(v.x), static_cast<lc_ubyte>(v.y), static_cast<lc_ubyte>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_ubyte3(lc_uint3 v) noexcept { return lc_ubyte3{static_cast<lc_ubyte>(v.x), static_cast<lc_ubyte>(v.y), static_cast<lc_ubyte>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_ubyte3(lc_uint4 v) noexcept { return lc_ubyte3{static_cast<lc_ubyte>(v.x), static_cast<lc_ubyte>(v.y), static_cast<lc_ubyte>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_ubyte3(lc_half3 v) noexcept { return lc_ubyte3{static_cast<lc_ubyte>(v.x), static_cast<lc_ubyte>(v.y), static_cast<lc_ubyte>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_ubyte3(lc_half4 v) noexcept { return lc_ubyte3{static_cast<lc_ubyte>(v.x), static_cast<lc_ubyte>(v.y), static_cast<lc_ubyte>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_ubyte3(lc_float3 v) noexcept { return lc_ubyte3{static_cast<lc_ubyte>(v.x), static_cast<lc_ubyte>(v.y), static_cast<lc_ubyte>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_ubyte3(lc_float4 v) noexcept { return lc_ubyte3{static_cast<lc_ubyte>(v.x), static_cast<lc_ubyte>(v.y), static_cast<lc_ubyte>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_ubyte3(lc_bool3 v) noexcept { return lc_ubyte3{static_cast<lc_ubyte>(v.x), static_cast<lc_ubyte>(v.y), static_cast<lc_ubyte>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_ubyte3(lc_bool4 v) noexcept { return lc_ubyte3{static_cast<lc_ubyte>(v.x), static_cast<lc_ubyte>(v.y), static_cast<lc_ubyte>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_ubyte3(lc_long3 v) noexcept { return lc_ubyte3{static_cast<lc_ubyte>(v.x), static_cast<lc_ubyte>(v.y), static_cast<lc_ubyte>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_ubyte3(lc_long4 v) noexcept { return lc_ubyte3{static_cast<lc_ubyte>(v.x), static_cast<lc_ubyte>(v.y), static_cast<lc_ubyte>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_ubyte3(lc_ulong3 v) noexcept { return lc_ubyte3{static_cast<lc_ubyte>(v.x), static_cast<lc_ubyte>(v.y), static_cast<lc_ubyte>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_ubyte3(lc_ulong4 v) noexcept { return lc_ubyte3{static_cast<lc_ubyte>(v.x), static_cast<lc_ubyte>(v.y), static_cast<lc_ubyte>(v.z)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_ubyte4(lc_ubyte s = 0) noexcept { return lc_ubyte4{s, s, s, s}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ubyte4(lc_ubyte x, lc_ubyte y, lc_ubyte z, lc_ubyte w) noexcept { return lc_ubyte4{x, y, z, w}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ubyte4(lc_ubyte x, lc_ubyte y, lc_ubyte2 zw) noexcept { return lc_ubyte4{x, y, zw.x, zw.y}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ubyte4(lc_ubyte x, lc_ubyte2 yz, lc_ubyte w) noexcept { return lc_ubyte4{x, yz.x, yz.y, w}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ubyte4(lc_ubyte2 xy, lc_ubyte z, lc_ubyte w) noexcept { return lc_ubyte4{xy.x, xy.y, z, w}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ubyte4(lc_ubyte2 xy, lc_ubyte2 zw) noexcept { return lc_ubyte4{xy.x, xy.y, zw.x, zw.y}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ubyte4(lc_ubyte x, lc_ubyte3 yzw) noexcept { return lc_ubyte4{x, yzw.x, yzw.y, yzw.z}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ubyte4(lc_ubyte3 xyz, lc_ubyte w) noexcept { return lc_ubyte4{xyz.x, xyz.y, xyz.z, w}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_ubyte4(lc_byte4 v) noexcept { return lc_ubyte4{static_cast<lc_ubyte>(v.x), static_cast<lc_ubyte>(v.y), static_cast<lc_ubyte>(v.z), static_cast<lc_ubyte>(v.w)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_ubyte4(lc_ubyte4 v) noexcept { return lc_ubyte4{static_cast<lc_ubyte>(v.x), static_cast<lc_ubyte>(v.y), static_cast<lc_ubyte>(v.z), static_cast<lc_ubyte>(v.w)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_ubyte4(lc_short4 v) noexcept { return lc_ubyte4{static_cast<lc_ubyte>(v.x), static_cast<lc_ubyte>(v.y), static_cast<lc_ubyte>(v.z), static_cast<lc_ubyte>(v.w)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_ubyte4(lc_ushort4 v) noexcept { return lc_ubyte4{static_cast<lc_ubyte>(v.x), static_cast<lc_ubyte>(v.y), static_cast<lc_ubyte>(v.z), static_cast<lc_ubyte>(v.w)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_ubyte4(lc_int4 v) noexcept { return lc_ubyte4{static_cast<lc_ubyte>(v.x), static_cast<lc_ubyte>(v.y), static_cast<lc_ubyte>(v.z), static_cast<lc_ubyte>(v.w)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_ubyte4(lc_uint4 v) noexcept { return lc_ubyte4{static_cast<lc_ubyte>(v.x), static_cast<lc_ubyte>(v.y), static_cast<lc_ubyte>(v.z), static_cast<lc_ubyte>(v.w)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_ubyte4(lc_half4 v) noexcept { return lc_ubyte4{static_cast<lc_ubyte>(v.x), static_cast<lc_ubyte>(v.y), static_cast<lc_ubyte>(v.z), static_cast<lc_ubyte>(v.w)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_ubyte4(lc_float4 v) noexcept { return lc_ubyte4{static_cast<lc_ubyte>(v.x), static_cast<lc_ubyte>(v.y), static_cast<lc_ubyte>(v.z), static_cast<lc_ubyte>(v.w)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_ubyte4(lc_bool4 v) noexcept { return lc_ubyte4{static_cast<lc_ubyte>(v.x), static_cast<lc_ubyte>(v.y), static_cast<lc_ubyte>(v.z), static_cast<lc_ubyte>(v.w)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_ubyte4(lc_long4 v) noexcept { return lc_ubyte4{static_cast<lc_ubyte>(v.x), static_cast<lc_ubyte>(v.y), static_cast<lc_ubyte>(v.z), static_cast<lc_ubyte>(v.w)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_ubyte4(lc_ulong4 v) noexcept { return lc_ubyte4{static_cast<lc_ubyte>(v.x), static_cast<lc_ubyte>(v.y), static_cast<lc_ubyte>(v.z), static_cast<lc_ubyte>(v.w)}; }

[[nodiscard]] __device__ inline constexpr auto lc_make_short2(lc_short s = 0) noexcept { return lc_short2{s, s}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_short2(lc_short x, lc_short y) noexcept { return lc_short2{x, y}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_short2(lc_byte2 v) noexcept { return lc_short2{static_cast<lc_short>(v.x), static_cast<lc_short>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_short2(lc_byte3 v) noexcept { return lc_short2{static_cast<lc_short>(v.x), static_cast<lc_short>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_short2(lc_byte4 v) noexcept { return lc_short2{static_cast<lc_short>(v.x), static_cast<lc_short>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_short2(lc_ubyte2 v) noexcept { return lc_short2{static_cast<lc_short>(v.x), static_cast<lc_short>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_short2(lc_ubyte3 v) noexcept { return lc_short2{static_cast<lc_short>(v.x), static_cast<lc_short>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_short2(lc_ubyte4 v) noexcept { return lc_short2{static_cast<lc_short>(v.x), static_cast<lc_short>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_short2(lc_short2 v) noexcept { return lc_short2{static_cast<lc_short>(v.x), static_cast<lc_short>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_short2(lc_short3 v) noexcept { return lc_short2{static_cast<lc_short>(v.x), static_cast<lc_short>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_short2(lc_short4 v) noexcept { return lc_short2{static_cast<lc_short>(v.x), static_cast<lc_short>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_short2(lc_ushort2 v) noexcept { return lc_short2{static_cast<lc_short>(v.x), static_cast<lc_short>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_short2(lc_ushort3 v) noexcept { return lc_short2{static_cast<lc_short>(v.x), static_cast<lc_short>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_short2(lc_ushort4 v) noexcept { return lc_short2{static_cast<lc_short>(v.x), static_cast<lc_short>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_short2(lc_int2 v) noexcept { return lc_short2{static_cast<lc_short>(v.x), static_cast<lc_short>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_short2(lc_int3 v) noexcept { return lc_short2{static_cast<lc_short>(v.x), static_cast<lc_short>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_short2(lc_int4 v) noexcept { return lc_short2{static_cast<lc_short>(v.x), static_cast<lc_short>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_short2(lc_uint2 v) noexcept { return lc_short2{static_cast<lc_short>(v.x), static_cast<lc_short>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_short2(lc_uint3 v) noexcept { return lc_short2{static_cast<lc_short>(v.x), static_cast<lc_short>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_short2(lc_uint4 v) noexcept { return lc_short2{static_cast<lc_short>(v.x), static_cast<lc_short>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_short2(lc_half2 v) noexcept { return lc_short2{static_cast<lc_short>(v.x), static_cast<lc_short>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_short2(lc_half3 v) noexcept { return lc_short2{static_cast<lc_short>(v.x), static_cast<lc_short>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_short2(lc_half4 v) noexcept { return lc_short2{static_cast<lc_short>(v.x), static_cast<lc_short>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_short2(lc_float2 v) noexcept { return lc_short2{static_cast<lc_short>(v.x), static_cast<lc_short>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_short2(lc_float3 v) noexcept { return lc_short2{static_cast<lc_short>(v.x), static_cast<lc_short>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_short2(lc_float4 v) noexcept { return lc_short2{static_cast<lc_short>(v.x), static_cast<lc_short>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_short2(lc_bool2 v) noexcept { return lc_short2{static_cast<lc_short>(v.x), static_cast<lc_short>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_short2(lc_bool3 v) noexcept { return lc_short2{static_cast<lc_short>(v.x), static_cast<lc_short>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_short2(lc_bool4 v) noexcept { return lc_short2{static_cast<lc_short>(v.x), static_cast<lc_short>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_short2(lc_long2 v) noexcept { return lc_short2{static_cast<lc_short>(v.x), static_cast<lc_short>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_short2(lc_long3 v) noexcept { return lc_short2{static_cast<lc_short>(v.x), static_cast<lc_short>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_short2(lc_long4 v) noexcept { return lc_short2{static_cast<lc_short>(v.x), static_cast<lc_short>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_short2(lc_ulong2 v) noexcept { return lc_short2{static_cast<lc_short>(v.x), static_cast<lc_short>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_short2(lc_ulong3 v) noexcept { return lc_short2{static_cast<lc_short>(v.x), static_cast<lc_short>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_short2(lc_ulong4 v) noexcept { return lc_short2{static_cast<lc_short>(v.x), static_cast<lc_short>(v.y)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_short3(lc_short s = 0) noexcept { return lc_short3{s, s, s}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_short3(lc_short x, lc_short y, lc_short z) noexcept { return lc_short3{x, y, z}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_short3(lc_short x, lc_short2 yz) noexcept { return lc_short3{x, yz.x, yz.y}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_short3(lc_short2 xy, lc_short z) noexcept { return lc_short3{xy.x, xy.y, z}; }
[[nodiscard]] __device__ constexpr auto lc_make_short3(lc_byte3 v) noexcept { return lc_short3{static_cast<lc_short>(v.x), static_cast<lc_short>(v.y), static_cast<lc_short>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_short3(lc_byte4 v) noexcept { return lc_short3{static_cast<lc_short>(v.x), static_cast<lc_short>(v.y), static_cast<lc_short>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_short3(lc_ubyte3 v) noexcept { return lc_short3{static_cast<lc_short>(v.x), static_cast<lc_short>(v.y), static_cast<lc_short>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_short3(lc_ubyte4 v) noexcept { return lc_short3{static_cast<lc_short>(v.x), static_cast<lc_short>(v.y), static_cast<lc_short>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_short3(lc_short3 v) noexcept { return lc_short3{static_cast<lc_short>(v.x), static_cast<lc_short>(v.y), static_cast<lc_short>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_short3(lc_short4 v) noexcept { return lc_short3{static_cast<lc_short>(v.x), static_cast<lc_short>(v.y), static_cast<lc_short>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_short3(lc_ushort3 v) noexcept { return lc_short3{static_cast<lc_short>(v.x), static_cast<lc_short>(v.y), static_cast<lc_short>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_short3(lc_ushort4 v) noexcept { return lc_short3{static_cast<lc_short>(v.x), static_cast<lc_short>(v.y), static_cast<lc_short>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_short3(lc_int3 v) noexcept { return lc_short3{static_cast<lc_short>(v.x), static_cast<lc_short>(v.y), static_cast<lc_short>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_short3(lc_int4 v) noexcept { return lc_short3{static_cast<lc_short>(v.x), static_cast<lc_short>(v.y), static_cast<lc_short>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_short3(lc_uint3 v) noexcept { return lc_short3{static_cast<lc_short>(v.x), static_cast<lc_short>(v.y), static_cast<lc_short>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_short3(lc_uint4 v) noexcept { return lc_short3{static_cast<lc_short>(v.x), static_cast<lc_short>(v.y), static_cast<lc_short>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_short3(lc_half3 v) noexcept { return lc_short3{static_cast<lc_short>(v.x), static_cast<lc_short>(v.y), static_cast<lc_short>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_short3(lc_half4 v) noexcept { return lc_short3{static_cast<lc_short>(v.x), static_cast<lc_short>(v.y), static_cast<lc_short>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_short3(lc_float3 v) noexcept { return lc_short3{static_cast<lc_short>(v.x), static_cast<lc_short>(v.y), static_cast<lc_short>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_short3(lc_float4 v) noexcept { return lc_short3{static_cast<lc_short>(v.x), static_cast<lc_short>(v.y), static_cast<lc_short>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_short3(lc_bool3 v) noexcept { return lc_short3{static_cast<lc_short>(v.x), static_cast<lc_short>(v.y), static_cast<lc_short>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_short3(lc_bool4 v) noexcept { return lc_short3{static_cast<lc_short>(v.x), static_cast<lc_short>(v.y), static_cast<lc_short>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_short3(lc_long3 v) noexcept { return lc_short3{static_cast<lc_short>(v.x), static_cast<lc_short>(v.y), static_cast<lc_short>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_short3(lc_long4 v) noexcept { return lc_short3{static_cast<lc_short>(v.x), static_cast<lc_short>(v.y), static_cast<lc_short>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_short3(lc_ulong3 v) noexcept { return lc_short3{static_cast<lc_short>(v.x), static_cast<lc_short>(v.y), static_cast<lc_short>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_short3(lc_ulong4 v) noexcept { return lc_short3{static_cast<lc_short>(v.x), static_cast<lc_short>(v.y), static_cast<lc_short>(v.z)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_short4(lc_short s = 0) noexcept { return lc_short4{s, s, s, s}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_short4(lc_short x, lc_short y, lc_short z, lc_short w) noexcept { return lc_short4{x, y, z, w}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_short4(lc_short x, lc_short y, lc_short2 zw) noexcept { return lc_short4{x, y, zw.x, zw.y}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_short4(lc_short x, lc_short2 yz, lc_short w) noexcept { return lc_short4{x, yz.x, yz.y, w}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_short4(lc_short2 xy, lc_short z, lc_short w) noexcept { return lc_short4{xy.x, xy.y, z, w}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_short4(lc_short2 xy, lc_short2 zw) noexcept { return lc_short4{xy.x, xy.y, zw.x, zw.y}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_short4(lc_short x, lc_short3 yzw) noexcept { return lc_short4{x, yzw.x, yzw.y, yzw.z}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_short4(lc_short3 xyz, lc_short w) noexcept { return lc_short4{xyz.x, xyz.y, xyz.z, w}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_short4(lc_byte4 v) noexcept { return lc_short4{static_cast<lc_short>(v.x), static_cast<lc_short>(v.y), static_cast<lc_short>(v.z), static_cast<lc_short>(v.w)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_short4(lc_ubyte4 v) noexcept { return lc_short4{static_cast<lc_short>(v.x), static_cast<lc_short>(v.y), static_cast<lc_short>(v.z), static_cast<lc_short>(v.w)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_short4(lc_short4 v) noexcept { return lc_short4{static_cast<lc_short>(v.x), static_cast<lc_short>(v.y), static_cast<lc_short>(v.z), static_cast<lc_short>(v.w)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_short4(lc_ushort4 v) noexcept { return lc_short4{static_cast<lc_short>(v.x), static_cast<lc_short>(v.y), static_cast<lc_short>(v.z), static_cast<lc_short>(v.w)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_short4(lc_int4 v) noexcept { return lc_short4{static_cast<lc_short>(v.x), static_cast<lc_short>(v.y), static_cast<lc_short>(v.z), static_cast<lc_short>(v.w)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_short4(lc_uint4 v) noexcept { return lc_short4{static_cast<lc_short>(v.x), static_cast<lc_short>(v.y), static_cast<lc_short>(v.z), static_cast<lc_short>(v.w)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_short4(lc_half4 v) noexcept { return lc_short4{static_cast<lc_short>(v.x), static_cast<lc_short>(v.y), static_cast<lc_short>(v.z), static_cast<lc_short>(v.w)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_short4(lc_float4 v) noexcept { return lc_short4{static_cast<lc_short>(v.x), static_cast<lc_short>(v.y), static_cast<lc_short>(v.z), static_cast<lc_short>(v.w)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_short4(lc_bool4 v) noexcept { return lc_short4{static_cast<lc_short>(v.x), static_cast<lc_short>(v.y), static_cast<lc_short>(v.z), static_cast<lc_short>(v.w)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_short4(lc_long4 v) noexcept { return lc_short4{static_cast<lc_short>(v.x), static_cast<lc_short>(v.y), static_cast<lc_short>(v.z), static_cast<lc_short>(v.w)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_short4(lc_ulong4 v) noexcept { return lc_short4{static_cast<lc_short>(v.x), static_cast<lc_short>(v.y), static_cast<lc_short>(v.z), static_cast<lc_short>(v.w)}; }

[[nodiscard]] __device__ inline constexpr auto lc_make_ushort2(lc_ushort s = 0) noexcept { return lc_ushort2{s, s}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ushort2(lc_ushort x, lc_ushort y) noexcept { return lc_ushort2{x, y}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ushort2(lc_byte2 v) noexcept { return lc_ushort2{static_cast<lc_ushort>(v.x), static_cast<lc_ushort>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ushort2(lc_byte3 v) noexcept { return lc_ushort2{static_cast<lc_ushort>(v.x), static_cast<lc_ushort>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ushort2(lc_byte4 v) noexcept { return lc_ushort2{static_cast<lc_ushort>(v.x), static_cast<lc_ushort>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ushort2(lc_ubyte2 v) noexcept { return lc_ushort2{static_cast<lc_ushort>(v.x), static_cast<lc_ushort>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ushort2(lc_ubyte3 v) noexcept { return lc_ushort2{static_cast<lc_ushort>(v.x), static_cast<lc_ushort>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ushort2(lc_ubyte4 v) noexcept { return lc_ushort2{static_cast<lc_ushort>(v.x), static_cast<lc_ushort>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ushort2(lc_short2 v) noexcept { return lc_ushort2{static_cast<lc_ushort>(v.x), static_cast<lc_ushort>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ushort2(lc_short3 v) noexcept { return lc_ushort2{static_cast<lc_ushort>(v.x), static_cast<lc_ushort>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ushort2(lc_short4 v) noexcept { return lc_ushort2{static_cast<lc_ushort>(v.x), static_cast<lc_ushort>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ushort2(lc_ushort2 v) noexcept { return lc_ushort2{static_cast<lc_ushort>(v.x), static_cast<lc_ushort>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ushort2(lc_ushort3 v) noexcept { return lc_ushort2{static_cast<lc_ushort>(v.x), static_cast<lc_ushort>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ushort2(lc_ushort4 v) noexcept { return lc_ushort2{static_cast<lc_ushort>(v.x), static_cast<lc_ushort>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ushort2(lc_int2 v) noexcept { return lc_ushort2{static_cast<lc_ushort>(v.x), static_cast<lc_ushort>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ushort2(lc_int3 v) noexcept { return lc_ushort2{static_cast<lc_ushort>(v.x), static_cast<lc_ushort>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ushort2(lc_int4 v) noexcept { return lc_ushort2{static_cast<lc_ushort>(v.x), static_cast<lc_ushort>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ushort2(lc_uint2 v) noexcept { return lc_ushort2{static_cast<lc_ushort>(v.x), static_cast<lc_ushort>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ushort2(lc_uint3 v) noexcept { return lc_ushort2{static_cast<lc_ushort>(v.x), static_cast<lc_ushort>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ushort2(lc_uint4 v) noexcept { return lc_ushort2{static_cast<lc_ushort>(v.x), static_cast<lc_ushort>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ushort2(lc_half2 v) noexcept { return lc_ushort2{static_cast<lc_ushort>(v.x), static_cast<lc_ushort>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ushort2(lc_half3 v) noexcept { return lc_ushort2{static_cast<lc_ushort>(v.x), static_cast<lc_ushort>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ushort2(lc_half4 v) noexcept { return lc_ushort2{static_cast<lc_ushort>(v.x), static_cast<lc_ushort>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ushort2(lc_float2 v) noexcept { return lc_ushort2{static_cast<lc_ushort>(v.x), static_cast<lc_ushort>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ushort2(lc_float3 v) noexcept { return lc_ushort2{static_cast<lc_ushort>(v.x), static_cast<lc_ushort>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ushort2(lc_float4 v) noexcept { return lc_ushort2{static_cast<lc_ushort>(v.x), static_cast<lc_ushort>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ushort2(lc_bool2 v) noexcept { return lc_ushort2{static_cast<lc_ushort>(v.x), static_cast<lc_ushort>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ushort2(lc_bool3 v) noexcept { return lc_ushort2{static_cast<lc_ushort>(v.x), static_cast<lc_ushort>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ushort2(lc_bool4 v) noexcept { return lc_ushort2{static_cast<lc_ushort>(v.x), static_cast<lc_ushort>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ushort2(lc_long2 v) noexcept { return lc_ushort2{static_cast<lc_ushort>(v.x), static_cast<lc_ushort>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ushort2(lc_long3 v) noexcept { return lc_ushort2{static_cast<lc_ushort>(v.x), static_cast<lc_ushort>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ushort2(lc_long4 v) noexcept { return lc_ushort2{static_cast<lc_ushort>(v.x), static_cast<lc_ushort>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ushort2(lc_ulong2 v) noexcept { return lc_ushort2{static_cast<lc_ushort>(v.x), static_cast<lc_ushort>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ushort2(lc_ulong3 v) noexcept { return lc_ushort2{static_cast<lc_ushort>(v.x), static_cast<lc_ushort>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ushort2(lc_ulong4 v) noexcept { return lc_ushort2{static_cast<lc_ushort>(v.x), static_cast<lc_ushort>(v.y)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_ushort3(lc_ushort s = 0) noexcept { return lc_ushort3{s, s, s}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ushort3(lc_ushort x, lc_ushort y, lc_ushort z) noexcept { return lc_ushort3{x, y, z}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ushort3(lc_ushort x, lc_ushort2 yz) noexcept { return lc_ushort3{x, yz.x, yz.y}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ushort3(lc_ushort2 xy, lc_ushort z) noexcept { return lc_ushort3{xy.x, xy.y, z}; }
[[nodiscard]] __device__ constexpr auto lc_make_ushort3(lc_byte3 v) noexcept { return lc_ushort3{static_cast<lc_ushort>(v.x), static_cast<lc_ushort>(v.y), static_cast<lc_ushort>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_ushort3(lc_byte4 v) noexcept { return lc_ushort3{static_cast<lc_ushort>(v.x), static_cast<lc_ushort>(v.y), static_cast<lc_ushort>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_ushort3(lc_ubyte3 v) noexcept { return lc_ushort3{static_cast<lc_ushort>(v.x), static_cast<lc_ushort>(v.y), static_cast<lc_ushort>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_ushort3(lc_ubyte4 v) noexcept { return lc_ushort3{static_cast<lc_ushort>(v.x), static_cast<lc_ushort>(v.y), static_cast<lc_ushort>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_ushort3(lc_short3 v) noexcept { return lc_ushort3{static_cast<lc_ushort>(v.x), static_cast<lc_ushort>(v.y), static_cast<lc_ushort>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_ushort3(lc_short4 v) noexcept { return lc_ushort3{static_cast<lc_ushort>(v.x), static_cast<lc_ushort>(v.y), static_cast<lc_ushort>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_ushort3(lc_ushort3 v) noexcept { return lc_ushort3{static_cast<lc_ushort>(v.x), static_cast<lc_ushort>(v.y), static_cast<lc_ushort>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_ushort3(lc_ushort4 v) noexcept { return lc_ushort3{static_cast<lc_ushort>(v.x), static_cast<lc_ushort>(v.y), static_cast<lc_ushort>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_ushort3(lc_int3 v) noexcept { return lc_ushort3{static_cast<lc_ushort>(v.x), static_cast<lc_ushort>(v.y), static_cast<lc_ushort>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_ushort3(lc_int4 v) noexcept { return lc_ushort3{static_cast<lc_ushort>(v.x), static_cast<lc_ushort>(v.y), static_cast<lc_ushort>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_ushort3(lc_uint3 v) noexcept { return lc_ushort3{static_cast<lc_ushort>(v.x), static_cast<lc_ushort>(v.y), static_cast<lc_ushort>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_ushort3(lc_uint4 v) noexcept { return lc_ushort3{static_cast<lc_ushort>(v.x), static_cast<lc_ushort>(v.y), static_cast<lc_ushort>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_ushort3(lc_half3 v) noexcept { return lc_ushort3{static_cast<lc_ushort>(v.x), static_cast<lc_ushort>(v.y), static_cast<lc_ushort>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_ushort3(lc_half4 v) noexcept { return lc_ushort3{static_cast<lc_ushort>(v.x), static_cast<lc_ushort>(v.y), static_cast<lc_ushort>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_ushort3(lc_float3 v) noexcept { return lc_ushort3{static_cast<lc_ushort>(v.x), static_cast<lc_ushort>(v.y), static_cast<lc_ushort>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_ushort3(lc_float4 v) noexcept { return lc_ushort3{static_cast<lc_ushort>(v.x), static_cast<lc_ushort>(v.y), static_cast<lc_ushort>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_ushort3(lc_bool3 v) noexcept { return lc_ushort3{static_cast<lc_ushort>(v.x), static_cast<lc_ushort>(v.y), static_cast<lc_ushort>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_ushort3(lc_bool4 v) noexcept { return lc_ushort3{static_cast<lc_ushort>(v.x), static_cast<lc_ushort>(v.y), static_cast<lc_ushort>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_ushort3(lc_long3 v) noexcept { return lc_ushort3{static_cast<lc_ushort>(v.x), static_cast<lc_ushort>(v.y), static_cast<lc_ushort>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_ushort3(lc_long4 v) noexcept { return lc_ushort3{static_cast<lc_ushort>(v.x), static_cast<lc_ushort>(v.y), static_cast<lc_ushort>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_ushort3(lc_ulong3 v) noexcept { return lc_ushort3{static_cast<lc_ushort>(v.x), static_cast<lc_ushort>(v.y), static_cast<lc_ushort>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_ushort3(lc_ulong4 v) noexcept { return lc_ushort3{static_cast<lc_ushort>(v.x), static_cast<lc_ushort>(v.y), static_cast<lc_ushort>(v.z)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_ushort4(lc_ushort s = 0) noexcept { return lc_ushort4{s, s, s, s}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ushort4(lc_ushort x, lc_ushort y, lc_ushort z, lc_ushort w) noexcept { return lc_ushort4{x, y, z, w}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ushort4(lc_ushort x, lc_ushort y, lc_ushort2 zw) noexcept { return lc_ushort4{x, y, zw.x, zw.y}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ushort4(lc_ushort x, lc_ushort2 yz, lc_ushort w) noexcept { return lc_ushort4{x, yz.x, yz.y, w}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ushort4(lc_ushort2 xy, lc_ushort z, lc_ushort w) noexcept { return lc_ushort4{xy.x, xy.y, z, w}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ushort4(lc_ushort2 xy, lc_ushort2 zw) noexcept { return lc_ushort4{xy.x, xy.y, zw.x, zw.y}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ushort4(lc_ushort x, lc_ushort3 yzw) noexcept { return lc_ushort4{x, yzw.x, yzw.y, yzw.z}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ushort4(lc_ushort3 xyz, lc_ushort w) noexcept { return lc_ushort4{xyz.x, xyz.y, xyz.z, w}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_ushort4(lc_byte4 v) noexcept { return lc_ushort4{static_cast<lc_ushort>(v.x), static_cast<lc_ushort>(v.y), static_cast<lc_ushort>(v.z), static_cast<lc_ushort>(v.w)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_ushort4(lc_ubyte4 v) noexcept { return lc_ushort4{static_cast<lc_ushort>(v.x), static_cast<lc_ushort>(v.y), static_cast<lc_ushort>(v.z), static_cast<lc_ushort>(v.w)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_ushort4(lc_short4 v) noexcept { return lc_ushort4{static_cast<lc_ushort>(v.x), static_cast<lc_ushort>(v.y), static_cast<lc_ushort>(v.z), static_cast<lc_ushort>(v.w)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_ushort4(lc_ushort4 v) noexcept { return lc_ushort4{static_cast<lc_ushort>(v.x), static_cast<lc_ushort>(v.y), static_cast<lc_ushort>(v.z), static_cast<lc_ushort>(v.w)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_ushort4(lc_int4 v) noexcept { return lc_ushort4{static_cast<lc_ushort>(v.x), static_cast<lc_ushort>(v.y), static_cast<lc_ushort>(v.z), static_cast<lc_ushort>(v.w)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_ushort4(lc_uint4 v) noexcept { return lc_ushort4{static_cast<lc_ushort>(v.x), static_cast<lc_ushort>(v.y), static_cast<lc_ushort>(v.z), static_cast<lc_ushort>(v.w)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_ushort4(lc_half4 v) noexcept { return lc_ushort4{static_cast<lc_ushort>(v.x), static_cast<lc_ushort>(v.y), static_cast<lc_ushort>(v.z), static_cast<lc_ushort>(v.w)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_ushort4(lc_float4 v) noexcept { return lc_ushort4{static_cast<lc_ushort>(v.x), static_cast<lc_ushort>(v.y), static_cast<lc_ushort>(v.z), static_cast<lc_ushort>(v.w)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_ushort4(lc_bool4 v) noexcept { return lc_ushort4{static_cast<lc_ushort>(v.x), static_cast<lc_ushort>(v.y), static_cast<lc_ushort>(v.z), static_cast<lc_ushort>(v.w)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_ushort4(lc_long4 v) noexcept { return lc_ushort4{static_cast<lc_ushort>(v.x), static_cast<lc_ushort>(v.y), static_cast<lc_ushort>(v.z), static_cast<lc_ushort>(v.w)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_ushort4(lc_ulong4 v) noexcept { return lc_ushort4{static_cast<lc_ushort>(v.x), static_cast<lc_ushort>(v.y), static_cast<lc_ushort>(v.z), static_cast<lc_ushort>(v.w)}; }

[[nodiscard]] __device__ inline constexpr auto lc_make_int2(lc_int s = 0) noexcept { return lc_int2{s, s}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_int2(lc_int x, lc_int y) noexcept { return lc_int2{x, y}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_int2(lc_byte2 v) noexcept { return lc_int2{static_cast<lc_int>(v.x), static_cast<lc_int>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_int2(lc_byte3 v) noexcept { return lc_int2{static_cast<lc_int>(v.x), static_cast<lc_int>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_int2(lc_byte4 v) noexcept { return lc_int2{static_cast<lc_int>(v.x), static_cast<lc_int>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_int2(lc_ubyte2 v) noexcept { return lc_int2{static_cast<lc_int>(v.x), static_cast<lc_int>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_int2(lc_ubyte3 v) noexcept { return lc_int2{static_cast<lc_int>(v.x), static_cast<lc_int>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_int2(lc_ubyte4 v) noexcept { return lc_int2{static_cast<lc_int>(v.x), static_cast<lc_int>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_int2(lc_short2 v) noexcept { return lc_int2{static_cast<lc_int>(v.x), static_cast<lc_int>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_int2(lc_short3 v) noexcept { return lc_int2{static_cast<lc_int>(v.x), static_cast<lc_int>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_int2(lc_short4 v) noexcept { return lc_int2{static_cast<lc_int>(v.x), static_cast<lc_int>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_int2(lc_ushort2 v) noexcept { return lc_int2{static_cast<lc_int>(v.x), static_cast<lc_int>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_int2(lc_ushort3 v) noexcept { return lc_int2{static_cast<lc_int>(v.x), static_cast<lc_int>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_int2(lc_ushort4 v) noexcept { return lc_int2{static_cast<lc_int>(v.x), static_cast<lc_int>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_int2(lc_int2 v) noexcept { return lc_int2{static_cast<lc_int>(v.x), static_cast<lc_int>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_int2(lc_int3 v) noexcept { return lc_int2{static_cast<lc_int>(v.x), static_cast<lc_int>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_int2(lc_int4 v) noexcept { return lc_int2{static_cast<lc_int>(v.x), static_cast<lc_int>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_int2(lc_uint2 v) noexcept { return lc_int2{static_cast<lc_int>(v.x), static_cast<lc_int>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_int2(lc_uint3 v) noexcept { return lc_int2{static_cast<lc_int>(v.x), static_cast<lc_int>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_int2(lc_uint4 v) noexcept { return lc_int2{static_cast<lc_int>(v.x), static_cast<lc_int>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_int2(lc_half2 v) noexcept { return lc_int2{static_cast<lc_int>(v.x), static_cast<lc_int>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_int2(lc_half3 v) noexcept { return lc_int2{static_cast<lc_int>(v.x), static_cast<lc_int>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_int2(lc_half4 v) noexcept { return lc_int2{static_cast<lc_int>(v.x), static_cast<lc_int>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_int2(lc_float2 v) noexcept { return lc_int2{static_cast<lc_int>(v.x), static_cast<lc_int>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_int2(lc_float3 v) noexcept { return lc_int2{static_cast<lc_int>(v.x), static_cast<lc_int>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_int2(lc_float4 v) noexcept { return lc_int2{static_cast<lc_int>(v.x), static_cast<lc_int>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_int2(lc_bool2 v) noexcept { return lc_int2{static_cast<lc_int>(v.x), static_cast<lc_int>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_int2(lc_bool3 v) noexcept { return lc_int2{static_cast<lc_int>(v.x), static_cast<lc_int>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_int2(lc_bool4 v) noexcept { return lc_int2{static_cast<lc_int>(v.x), static_cast<lc_int>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_int2(lc_long2 v) noexcept { return lc_int2{static_cast<lc_int>(v.x), static_cast<lc_int>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_int2(lc_long3 v) noexcept { return lc_int2{static_cast<lc_int>(v.x), static_cast<lc_int>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_int2(lc_long4 v) noexcept { return lc_int2{static_cast<lc_int>(v.x), static_cast<lc_int>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_int2(lc_ulong2 v) noexcept { return lc_int2{static_cast<lc_int>(v.x), static_cast<lc_int>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_int2(lc_ulong3 v) noexcept { return lc_int2{static_cast<lc_int>(v.x), static_cast<lc_int>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_int2(lc_ulong4 v) noexcept { return lc_int2{static_cast<lc_int>(v.x), static_cast<lc_int>(v.y)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_int3(lc_int s = 0) noexcept { return lc_int3{s, s, s}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_int3(lc_int x, lc_int y, lc_int z) noexcept { return lc_int3{x, y, z}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_int3(lc_int x, lc_int2 yz) noexcept { return lc_int3{x, yz.x, yz.y}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_int3(lc_int2 xy, lc_int z) noexcept { return lc_int3{xy.x, xy.y, z}; }
[[nodiscard]] __device__ constexpr auto lc_make_int3(lc_byte3 v) noexcept { return lc_int3{static_cast<lc_int>(v.x), static_cast<lc_int>(v.y), static_cast<lc_int>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_int3(lc_byte4 v) noexcept { return lc_int3{static_cast<lc_int>(v.x), static_cast<lc_int>(v.y), static_cast<lc_int>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_int3(lc_ubyte3 v) noexcept { return lc_int3{static_cast<lc_int>(v.x), static_cast<lc_int>(v.y), static_cast<lc_int>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_int3(lc_ubyte4 v) noexcept { return lc_int3{static_cast<lc_int>(v.x), static_cast<lc_int>(v.y), static_cast<lc_int>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_int3(lc_short3 v) noexcept { return lc_int3{static_cast<lc_int>(v.x), static_cast<lc_int>(v.y), static_cast<lc_int>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_int3(lc_short4 v) noexcept { return lc_int3{static_cast<lc_int>(v.x), static_cast<lc_int>(v.y), static_cast<lc_int>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_int3(lc_ushort3 v) noexcept { return lc_int3{static_cast<lc_int>(v.x), static_cast<lc_int>(v.y), static_cast<lc_int>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_int3(lc_ushort4 v) noexcept { return lc_int3{static_cast<lc_int>(v.x), static_cast<lc_int>(v.y), static_cast<lc_int>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_int3(lc_int3 v) noexcept { return lc_int3{static_cast<lc_int>(v.x), static_cast<lc_int>(v.y), static_cast<lc_int>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_int3(lc_int4 v) noexcept { return lc_int3{static_cast<lc_int>(v.x), static_cast<lc_int>(v.y), static_cast<lc_int>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_int3(lc_uint3 v) noexcept { return lc_int3{static_cast<lc_int>(v.x), static_cast<lc_int>(v.y), static_cast<lc_int>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_int3(lc_uint4 v) noexcept { return lc_int3{static_cast<lc_int>(v.x), static_cast<lc_int>(v.y), static_cast<lc_int>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_int3(lc_half3 v) noexcept { return lc_int3{static_cast<lc_int>(v.x), static_cast<lc_int>(v.y), static_cast<lc_int>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_int3(lc_half4 v) noexcept { return lc_int3{static_cast<lc_int>(v.x), static_cast<lc_int>(v.y), static_cast<lc_int>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_int3(lc_float3 v) noexcept { return lc_int3{static_cast<lc_int>(v.x), static_cast<lc_int>(v.y), static_cast<lc_int>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_int3(lc_float4 v) noexcept { return lc_int3{static_cast<lc_int>(v.x), static_cast<lc_int>(v.y), static_cast<lc_int>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_int3(lc_bool3 v) noexcept { return lc_int3{static_cast<lc_int>(v.x), static_cast<lc_int>(v.y), static_cast<lc_int>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_int3(lc_bool4 v) noexcept { return lc_int3{static_cast<lc_int>(v.x), static_cast<lc_int>(v.y), static_cast<lc_int>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_int3(lc_long3 v) noexcept { return lc_int3{static_cast<lc_int>(v.x), static_cast<lc_int>(v.y), static_cast<lc_int>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_int3(lc_long4 v) noexcept { return lc_int3{static_cast<lc_int>(v.x), static_cast<lc_int>(v.y), static_cast<lc_int>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_int3(lc_ulong3 v) noexcept { return lc_int3{static_cast<lc_int>(v.x), static_cast<lc_int>(v.y), static_cast<lc_int>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_int3(lc_ulong4 v) noexcept { return lc_int3{static_cast<lc_int>(v.x), static_cast<lc_int>(v.y), static_cast<lc_int>(v.z)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_int4(lc_int s = 0) noexcept { return lc_int4{s, s, s, s}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_int4(lc_int x, lc_int y, lc_int z, lc_int w) noexcept { return lc_int4{x, y, z, w}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_int4(lc_int x, lc_int y, lc_int2 zw) noexcept { return lc_int4{x, y, zw.x, zw.y}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_int4(lc_int x, lc_int2 yz, lc_int w) noexcept { return lc_int4{x, yz.x, yz.y, w}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_int4(lc_int2 xy, lc_int z, lc_int w) noexcept { return lc_int4{xy.x, xy.y, z, w}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_int4(lc_int2 xy, lc_int2 zw) noexcept { return lc_int4{xy.x, xy.y, zw.x, zw.y}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_int4(lc_int x, lc_int3 yzw) noexcept { return lc_int4{x, yzw.x, yzw.y, yzw.z}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_int4(lc_int3 xyz, lc_int w) noexcept { return lc_int4{xyz.x, xyz.y, xyz.z, w}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_int4(lc_byte4 v) noexcept { return lc_int4{static_cast<lc_int>(v.x), static_cast<lc_int>(v.y), static_cast<lc_int>(v.z), static_cast<lc_int>(v.w)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_int4(lc_ubyte4 v) noexcept { return lc_int4{static_cast<lc_int>(v.x), static_cast<lc_int>(v.y), static_cast<lc_int>(v.z), static_cast<lc_int>(v.w)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_int4(lc_short4 v) noexcept { return lc_int4{static_cast<lc_int>(v.x), static_cast<lc_int>(v.y), static_cast<lc_int>(v.z), static_cast<lc_int>(v.w)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_int4(lc_ushort4 v) noexcept { return lc_int4{static_cast<lc_int>(v.x), static_cast<lc_int>(v.y), static_cast<lc_int>(v.z), static_cast<lc_int>(v.w)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_int4(lc_int4 v) noexcept { return lc_int4{static_cast<lc_int>(v.x), static_cast<lc_int>(v.y), static_cast<lc_int>(v.z), static_cast<lc_int>(v.w)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_int4(lc_uint4 v) noexcept { return lc_int4{static_cast<lc_int>(v.x), static_cast<lc_int>(v.y), static_cast<lc_int>(v.z), static_cast<lc_int>(v.w)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_int4(lc_half4 v) noexcept { return lc_int4{static_cast<lc_int>(v.x), static_cast<lc_int>(v.y), static_cast<lc_int>(v.z), static_cast<lc_int>(v.w)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_int4(lc_float4 v) noexcept { return lc_int4{static_cast<lc_int>(v.x), static_cast<lc_int>(v.y), static_cast<lc_int>(v.z), static_cast<lc_int>(v.w)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_int4(lc_bool4 v) noexcept { return lc_int4{static_cast<lc_int>(v.x), static_cast<lc_int>(v.y), static_cast<lc_int>(v.z), static_cast<lc_int>(v.w)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_int4(lc_long4 v) noexcept { return lc_int4{static_cast<lc_int>(v.x), static_cast<lc_int>(v.y), static_cast<lc_int>(v.z), static_cast<lc_int>(v.w)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_int4(lc_ulong4 v) noexcept { return lc_int4{static_cast<lc_int>(v.x), static_cast<lc_int>(v.y), static_cast<lc_int>(v.z), static_cast<lc_int>(v.w)}; }

[[nodiscard]] __device__ inline constexpr auto lc_make_uint2(lc_uint s = 0) noexcept { return lc_uint2{s, s}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_uint2(lc_uint x, lc_uint y) noexcept { return lc_uint2{x, y}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_uint2(lc_byte2 v) noexcept { return lc_uint2{static_cast<lc_uint>(v.x), static_cast<lc_uint>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_uint2(lc_byte3 v) noexcept { return lc_uint2{static_cast<lc_uint>(v.x), static_cast<lc_uint>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_uint2(lc_byte4 v) noexcept { return lc_uint2{static_cast<lc_uint>(v.x), static_cast<lc_uint>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_uint2(lc_ubyte2 v) noexcept { return lc_uint2{static_cast<lc_uint>(v.x), static_cast<lc_uint>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_uint2(lc_ubyte3 v) noexcept { return lc_uint2{static_cast<lc_uint>(v.x), static_cast<lc_uint>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_uint2(lc_ubyte4 v) noexcept { return lc_uint2{static_cast<lc_uint>(v.x), static_cast<lc_uint>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_uint2(lc_short2 v) noexcept { return lc_uint2{static_cast<lc_uint>(v.x), static_cast<lc_uint>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_uint2(lc_short3 v) noexcept { return lc_uint2{static_cast<lc_uint>(v.x), static_cast<lc_uint>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_uint2(lc_short4 v) noexcept { return lc_uint2{static_cast<lc_uint>(v.x), static_cast<lc_uint>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_uint2(lc_ushort2 v) noexcept { return lc_uint2{static_cast<lc_uint>(v.x), static_cast<lc_uint>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_uint2(lc_ushort3 v) noexcept { return lc_uint2{static_cast<lc_uint>(v.x), static_cast<lc_uint>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_uint2(lc_ushort4 v) noexcept { return lc_uint2{static_cast<lc_uint>(v.x), static_cast<lc_uint>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_uint2(lc_int2 v) noexcept { return lc_uint2{static_cast<lc_uint>(v.x), static_cast<lc_uint>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_uint2(lc_int3 v) noexcept { return lc_uint2{static_cast<lc_uint>(v.x), static_cast<lc_uint>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_uint2(lc_int4 v) noexcept { return lc_uint2{static_cast<lc_uint>(v.x), static_cast<lc_uint>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_uint2(lc_uint2 v) noexcept { return lc_uint2{static_cast<lc_uint>(v.x), static_cast<lc_uint>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_uint2(lc_uint3 v) noexcept { return lc_uint2{static_cast<lc_uint>(v.x), static_cast<lc_uint>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_uint2(lc_uint4 v) noexcept { return lc_uint2{static_cast<lc_uint>(v.x), static_cast<lc_uint>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_uint2(lc_half2 v) noexcept { return lc_uint2{static_cast<lc_uint>(v.x), static_cast<lc_uint>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_uint2(lc_half3 v) noexcept { return lc_uint2{static_cast<lc_uint>(v.x), static_cast<lc_uint>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_uint2(lc_half4 v) noexcept { return lc_uint2{static_cast<lc_uint>(v.x), static_cast<lc_uint>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_uint2(lc_float2 v) noexcept { return lc_uint2{static_cast<lc_uint>(v.x), static_cast<lc_uint>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_uint2(lc_float3 v) noexcept { return lc_uint2{static_cast<lc_uint>(v.x), static_cast<lc_uint>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_uint2(lc_float4 v) noexcept { return lc_uint2{static_cast<lc_uint>(v.x), static_cast<lc_uint>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_uint2(lc_bool2 v) noexcept { return lc_uint2{static_cast<lc_uint>(v.x), static_cast<lc_uint>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_uint2(lc_bool3 v) noexcept { return lc_uint2{static_cast<lc_uint>(v.x), static_cast<lc_uint>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_uint2(lc_bool4 v) noexcept { return lc_uint2{static_cast<lc_uint>(v.x), static_cast<lc_uint>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_uint2(lc_long2 v) noexcept { return lc_uint2{static_cast<lc_uint>(v.x), static_cast<lc_uint>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_uint2(lc_long3 v) noexcept { return lc_uint2{static_cast<lc_uint>(v.x), static_cast<lc_uint>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_uint2(lc_long4 v) noexcept { return lc_uint2{static_cast<lc_uint>(v.x), static_cast<lc_uint>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_uint2(lc_ulong2 v) noexcept { return lc_uint2{static_cast<lc_uint>(v.x), static_cast<lc_uint>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_uint2(lc_ulong3 v) noexcept { return lc_uint2{static_cast<lc_uint>(v.x), static_cast<lc_uint>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_uint2(lc_ulong4 v) noexcept { return lc_uint2{static_cast<lc_uint>(v.x), static_cast<lc_uint>(v.y)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_uint3(lc_uint s = 0) noexcept { return lc_uint3{s, s, s}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_uint3(lc_uint x, lc_uint y, lc_uint z) noexcept { return lc_uint3{x, y, z}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_uint3(lc_uint x, lc_uint2 yz) noexcept { return lc_uint3{x, yz.x, yz.y}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_uint3(lc_uint2 xy, lc_uint z) noexcept { return lc_uint3{xy.x, xy.y, z}; }
[[nodiscard]] __device__ constexpr auto lc_make_uint3(lc_byte3 v) noexcept { return lc_uint3{static_cast<lc_uint>(v.x), static_cast<lc_uint>(v.y), static_cast<lc_uint>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_uint3(lc_byte4 v) noexcept { return lc_uint3{static_cast<lc_uint>(v.x), static_cast<lc_uint>(v.y), static_cast<lc_uint>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_uint3(lc_ubyte3 v) noexcept { return lc_uint3{static_cast<lc_uint>(v.x), static_cast<lc_uint>(v.y), static_cast<lc_uint>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_uint3(lc_ubyte4 v) noexcept { return lc_uint3{static_cast<lc_uint>(v.x), static_cast<lc_uint>(v.y), static_cast<lc_uint>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_uint3(lc_short3 v) noexcept { return lc_uint3{static_cast<lc_uint>(v.x), static_cast<lc_uint>(v.y), static_cast<lc_uint>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_uint3(lc_short4 v) noexcept { return lc_uint3{static_cast<lc_uint>(v.x), static_cast<lc_uint>(v.y), static_cast<lc_uint>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_uint3(lc_ushort3 v) noexcept { return lc_uint3{static_cast<lc_uint>(v.x), static_cast<lc_uint>(v.y), static_cast<lc_uint>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_uint3(lc_ushort4 v) noexcept { return lc_uint3{static_cast<lc_uint>(v.x), static_cast<lc_uint>(v.y), static_cast<lc_uint>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_uint3(lc_int3 v) noexcept { return lc_uint3{static_cast<lc_uint>(v.x), static_cast<lc_uint>(v.y), static_cast<lc_uint>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_uint3(lc_int4 v) noexcept { return lc_uint3{static_cast<lc_uint>(v.x), static_cast<lc_uint>(v.y), static_cast<lc_uint>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_uint3(lc_uint3 v) noexcept { return lc_uint3{static_cast<lc_uint>(v.x), static_cast<lc_uint>(v.y), static_cast<lc_uint>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_uint3(lc_uint4 v) noexcept { return lc_uint3{static_cast<lc_uint>(v.x), static_cast<lc_uint>(v.y), static_cast<lc_uint>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_uint3(lc_half3 v) noexcept { return lc_uint3{static_cast<lc_uint>(v.x), static_cast<lc_uint>(v.y), static_cast<lc_uint>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_uint3(lc_half4 v) noexcept { return lc_uint3{static_cast<lc_uint>(v.x), static_cast<lc_uint>(v.y), static_cast<lc_uint>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_uint3(lc_float3 v) noexcept { return lc_uint3{static_cast<lc_uint>(v.x), static_cast<lc_uint>(v.y), static_cast<lc_uint>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_uint3(lc_float4 v) noexcept { return lc_uint3{static_cast<lc_uint>(v.x), static_cast<lc_uint>(v.y), static_cast<lc_uint>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_uint3(lc_bool3 v) noexcept { return lc_uint3{static_cast<lc_uint>(v.x), static_cast<lc_uint>(v.y), static_cast<lc_uint>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_uint3(lc_bool4 v) noexcept { return lc_uint3{static_cast<lc_uint>(v.x), static_cast<lc_uint>(v.y), static_cast<lc_uint>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_uint3(lc_long3 v) noexcept { return lc_uint3{static_cast<lc_uint>(v.x), static_cast<lc_uint>(v.y), static_cast<lc_uint>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_uint3(lc_long4 v) noexcept { return lc_uint3{static_cast<lc_uint>(v.x), static_cast<lc_uint>(v.y), static_cast<lc_uint>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_uint3(lc_ulong3 v) noexcept { return lc_uint3{static_cast<lc_uint>(v.x), static_cast<lc_uint>(v.y), static_cast<lc_uint>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_uint3(lc_ulong4 v) noexcept { return lc_uint3{static_cast<lc_uint>(v.x), static_cast<lc_uint>(v.y), static_cast<lc_uint>(v.z)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_uint4(lc_uint s = 0) noexcept { return lc_uint4{s, s, s, s}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_uint4(lc_uint x, lc_uint y, lc_uint z, lc_uint w) noexcept { return lc_uint4{x, y, z, w}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_uint4(lc_uint x, lc_uint y, lc_uint2 zw) noexcept { return lc_uint4{x, y, zw.x, zw.y}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_uint4(lc_uint x, lc_uint2 yz, lc_uint w) noexcept { return lc_uint4{x, yz.x, yz.y, w}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_uint4(lc_uint2 xy, lc_uint z, lc_uint w) noexcept { return lc_uint4{xy.x, xy.y, z, w}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_uint4(lc_uint2 xy, lc_uint2 zw) noexcept { return lc_uint4{xy.x, xy.y, zw.x, zw.y}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_uint4(lc_uint x, lc_uint3 yzw) noexcept { return lc_uint4{x, yzw.x, yzw.y, yzw.z}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_uint4(lc_uint3 xyz, lc_uint w) noexcept { return lc_uint4{xyz.x, xyz.y, xyz.z, w}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_uint4(lc_byte4 v) noexcept { return lc_uint4{static_cast<lc_uint>(v.x), static_cast<lc_uint>(v.y), static_cast<lc_uint>(v.z), static_cast<lc_uint>(v.w)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_uint4(lc_ubyte4 v) noexcept { return lc_uint4{static_cast<lc_uint>(v.x), static_cast<lc_uint>(v.y), static_cast<lc_uint>(v.z), static_cast<lc_uint>(v.w)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_uint4(lc_short4 v) noexcept { return lc_uint4{static_cast<lc_uint>(v.x), static_cast<lc_uint>(v.y), static_cast<lc_uint>(v.z), static_cast<lc_uint>(v.w)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_uint4(lc_ushort4 v) noexcept { return lc_uint4{static_cast<lc_uint>(v.x), static_cast<lc_uint>(v.y), static_cast<lc_uint>(v.z), static_cast<lc_uint>(v.w)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_uint4(lc_int4 v) noexcept { return lc_uint4{static_cast<lc_uint>(v.x), static_cast<lc_uint>(v.y), static_cast<lc_uint>(v.z), static_cast<lc_uint>(v.w)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_uint4(lc_uint4 v) noexcept { return lc_uint4{static_cast<lc_uint>(v.x), static_cast<lc_uint>(v.y), static_cast<lc_uint>(v.z), static_cast<lc_uint>(v.w)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_uint4(lc_half4 v) noexcept { return lc_uint4{static_cast<lc_uint>(v.x), static_cast<lc_uint>(v.y), static_cast<lc_uint>(v.z), static_cast<lc_uint>(v.w)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_uint4(lc_float4 v) noexcept { return lc_uint4{static_cast<lc_uint>(v.x), static_cast<lc_uint>(v.y), static_cast<lc_uint>(v.z), static_cast<lc_uint>(v.w)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_uint4(lc_bool4 v) noexcept { return lc_uint4{static_cast<lc_uint>(v.x), static_cast<lc_uint>(v.y), static_cast<lc_uint>(v.z), static_cast<lc_uint>(v.w)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_uint4(lc_long4 v) noexcept { return lc_uint4{static_cast<lc_uint>(v.x), static_cast<lc_uint>(v.y), static_cast<lc_uint>(v.z), static_cast<lc_uint>(v.w)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_uint4(lc_ulong4 v) noexcept { return lc_uint4{static_cast<lc_uint>(v.x), static_cast<lc_uint>(v.y), static_cast<lc_uint>(v.z), static_cast<lc_uint>(v.w)}; }

[[nodiscard]] __device__ inline constexpr auto lc_make_half2(lc_half s = 0) noexcept { return lc_half2{s, s}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_half2(lc_half x, lc_half y) noexcept { return lc_half2{x, y}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_half2(lc_byte2 v) noexcept { return lc_half2{static_cast<lc_half>(v.x), static_cast<lc_half>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_half2(lc_byte3 v) noexcept { return lc_half2{static_cast<lc_half>(v.x), static_cast<lc_half>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_half2(lc_byte4 v) noexcept { return lc_half2{static_cast<lc_half>(v.x), static_cast<lc_half>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_half2(lc_ubyte2 v) noexcept { return lc_half2{static_cast<lc_half>(v.x), static_cast<lc_half>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_half2(lc_ubyte3 v) noexcept { return lc_half2{static_cast<lc_half>(v.x), static_cast<lc_half>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_half2(lc_ubyte4 v) noexcept { return lc_half2{static_cast<lc_half>(v.x), static_cast<lc_half>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_half2(lc_short2 v) noexcept { return lc_half2{static_cast<lc_half>(v.x), static_cast<lc_half>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_half2(lc_short3 v) noexcept { return lc_half2{static_cast<lc_half>(v.x), static_cast<lc_half>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_half2(lc_short4 v) noexcept { return lc_half2{static_cast<lc_half>(v.x), static_cast<lc_half>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_half2(lc_ushort2 v) noexcept { return lc_half2{static_cast<lc_half>(v.x), static_cast<lc_half>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_half2(lc_ushort3 v) noexcept { return lc_half2{static_cast<lc_half>(v.x), static_cast<lc_half>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_half2(lc_ushort4 v) noexcept { return lc_half2{static_cast<lc_half>(v.x), static_cast<lc_half>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_half2(lc_int2 v) noexcept { return lc_half2{static_cast<lc_half>(v.x), static_cast<lc_half>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_half2(lc_int3 v) noexcept { return lc_half2{static_cast<lc_half>(v.x), static_cast<lc_half>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_half2(lc_int4 v) noexcept { return lc_half2{static_cast<lc_half>(v.x), static_cast<lc_half>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_half2(lc_uint2 v) noexcept { return lc_half2{static_cast<lc_half>(v.x), static_cast<lc_half>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_half2(lc_uint3 v) noexcept { return lc_half2{static_cast<lc_half>(v.x), static_cast<lc_half>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_half2(lc_uint4 v) noexcept { return lc_half2{static_cast<lc_half>(v.x), static_cast<lc_half>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_half2(lc_half2 v) noexcept { return lc_half2{static_cast<lc_half>(v.x), static_cast<lc_half>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_half2(lc_half3 v) noexcept { return lc_half2{static_cast<lc_half>(v.x), static_cast<lc_half>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_half2(lc_half4 v) noexcept { return lc_half2{static_cast<lc_half>(v.x), static_cast<lc_half>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_half2(lc_float2 v) noexcept { return lc_half2{static_cast<lc_half>(v.x), static_cast<lc_half>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_half2(lc_float3 v) noexcept { return lc_half2{static_cast<lc_half>(v.x), static_cast<lc_half>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_half2(lc_float4 v) noexcept { return lc_half2{static_cast<lc_half>(v.x), static_cast<lc_half>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_half2(lc_bool2 v) noexcept { return lc_half2{static_cast<lc_half>(v.x), static_cast<lc_half>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_half2(lc_bool3 v) noexcept { return lc_half2{static_cast<lc_half>(v.x), static_cast<lc_half>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_half2(lc_bool4 v) noexcept { return lc_half2{static_cast<lc_half>(v.x), static_cast<lc_half>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_half2(lc_long2 v) noexcept { return lc_half2{static_cast<lc_half>(v.x), static_cast<lc_half>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_half2(lc_long3 v) noexcept { return lc_half2{static_cast<lc_half>(v.x), static_cast<lc_half>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_half2(lc_long4 v) noexcept { return lc_half2{static_cast<lc_half>(v.x), static_cast<lc_half>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_half2(lc_ulong2 v) noexcept { return lc_half2{static_cast<lc_half>(v.x), static_cast<lc_half>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_half2(lc_ulong3 v) noexcept { return lc_half2{static_cast<lc_half>(v.x), static_cast<lc_half>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_half2(lc_ulong4 v) noexcept { return lc_half2{static_cast<lc_half>(v.x), static_cast<lc_half>(v.y)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_half3(lc_half s = 0) noexcept { return lc_half3{s, s, s}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_half3(lc_half x, lc_half y, lc_half z) noexcept { return lc_half3{x, y, z}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_half3(lc_half x, lc_half2 yz) noexcept { return lc_half3{x, yz.x, yz.y}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_half3(lc_half2 xy, lc_half z) noexcept { return lc_half3{xy.x, xy.y, z}; }
[[nodiscard]] __device__ constexpr auto lc_make_half3(lc_byte3 v) noexcept { return lc_half3{static_cast<lc_half>(v.x), static_cast<lc_half>(v.y), static_cast<lc_half>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_half3(lc_byte4 v) noexcept { return lc_half3{static_cast<lc_half>(v.x), static_cast<lc_half>(v.y), static_cast<lc_half>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_half3(lc_ubyte3 v) noexcept { return lc_half3{static_cast<lc_half>(v.x), static_cast<lc_half>(v.y), static_cast<lc_half>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_half3(lc_ubyte4 v) noexcept { return lc_half3{static_cast<lc_half>(v.x), static_cast<lc_half>(v.y), static_cast<lc_half>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_half3(lc_short3 v) noexcept { return lc_half3{static_cast<lc_half>(v.x), static_cast<lc_half>(v.y), static_cast<lc_half>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_half3(lc_short4 v) noexcept { return lc_half3{static_cast<lc_half>(v.x), static_cast<lc_half>(v.y), static_cast<lc_half>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_half3(lc_ushort3 v) noexcept { return lc_half3{static_cast<lc_half>(v.x), static_cast<lc_half>(v.y), static_cast<lc_half>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_half3(lc_ushort4 v) noexcept { return lc_half3{static_cast<lc_half>(v.x), static_cast<lc_half>(v.y), static_cast<lc_half>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_half3(lc_int3 v) noexcept { return lc_half3{static_cast<lc_half>(v.x), static_cast<lc_half>(v.y), static_cast<lc_half>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_half3(lc_int4 v) noexcept { return lc_half3{static_cast<lc_half>(v.x), static_cast<lc_half>(v.y), static_cast<lc_half>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_half3(lc_uint3 v) noexcept { return lc_half3{static_cast<lc_half>(v.x), static_cast<lc_half>(v.y), static_cast<lc_half>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_half3(lc_uint4 v) noexcept { return lc_half3{static_cast<lc_half>(v.x), static_cast<lc_half>(v.y), static_cast<lc_half>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_half3(lc_half3 v) noexcept { return lc_half3{static_cast<lc_half>(v.x), static_cast<lc_half>(v.y), static_cast<lc_half>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_half3(lc_half4 v) noexcept { return lc_half3{static_cast<lc_half>(v.x), static_cast<lc_half>(v.y), static_cast<lc_half>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_half3(lc_float3 v) noexcept { return lc_half3{static_cast<lc_half>(v.x), static_cast<lc_half>(v.y), static_cast<lc_half>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_half3(lc_float4 v) noexcept { return lc_half3{static_cast<lc_half>(v.x), static_cast<lc_half>(v.y), static_cast<lc_half>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_half3(lc_bool3 v) noexcept { return lc_half3{static_cast<lc_half>(v.x), static_cast<lc_half>(v.y), static_cast<lc_half>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_half3(lc_bool4 v) noexcept { return lc_half3{static_cast<lc_half>(v.x), static_cast<lc_half>(v.y), static_cast<lc_half>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_half3(lc_long3 v) noexcept { return lc_half3{static_cast<lc_half>(v.x), static_cast<lc_half>(v.y), static_cast<lc_half>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_half3(lc_long4 v) noexcept { return lc_half3{static_cast<lc_half>(v.x), static_cast<lc_half>(v.y), static_cast<lc_half>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_half3(lc_ulong3 v) noexcept { return lc_half3{static_cast<lc_half>(v.x), static_cast<lc_half>(v.y), static_cast<lc_half>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_half3(lc_ulong4 v) noexcept { return lc_half3{static_cast<lc_half>(v.x), static_cast<lc_half>(v.y), static_cast<lc_half>(v.z)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_half4(lc_half s = 0) noexcept { return lc_half4{s, s, s, s}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_half4(lc_half x, lc_half y, lc_half z, lc_half w) noexcept { return lc_half4{x, y, z, w}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_half4(lc_half x, lc_half y, lc_half2 zw) noexcept { return lc_half4{x, y, zw.x, zw.y}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_half4(lc_half x, lc_half2 yz, lc_half w) noexcept { return lc_half4{x, yz.x, yz.y, w}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_half4(lc_half2 xy, lc_half z, lc_half w) noexcept { return lc_half4{xy.x, xy.y, z, w}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_half4(lc_half2 xy, lc_half2 zw) noexcept { return lc_half4{xy.x, xy.y, zw.x, zw.y}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_half4(lc_half x, lc_half3 yzw) noexcept { return lc_half4{x, yzw.x, yzw.y, yzw.z}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_half4(lc_half3 xyz, lc_half w) noexcept { return lc_half4{xyz.x, xyz.y, xyz.z, w}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_half4(lc_byte4 v) noexcept { return lc_half4{static_cast<lc_half>(v.x), static_cast<lc_half>(v.y), static_cast<lc_half>(v.z), static_cast<lc_half>(v.w)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_half4(lc_ubyte4 v) noexcept { return lc_half4{static_cast<lc_half>(v.x), static_cast<lc_half>(v.y), static_cast<lc_half>(v.z), static_cast<lc_half>(v.w)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_half4(lc_short4 v) noexcept { return lc_half4{static_cast<lc_half>(v.x), static_cast<lc_half>(v.y), static_cast<lc_half>(v.z), static_cast<lc_half>(v.w)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_half4(lc_ushort4 v) noexcept { return lc_half4{static_cast<lc_half>(v.x), static_cast<lc_half>(v.y), static_cast<lc_half>(v.z), static_cast<lc_half>(v.w)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_half4(lc_int4 v) noexcept { return lc_half4{static_cast<lc_half>(v.x), static_cast<lc_half>(v.y), static_cast<lc_half>(v.z), static_cast<lc_half>(v.w)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_half4(lc_uint4 v) noexcept { return lc_half4{static_cast<lc_half>(v.x), static_cast<lc_half>(v.y), static_cast<lc_half>(v.z), static_cast<lc_half>(v.w)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_half4(lc_half4 v) noexcept { return lc_half4{static_cast<lc_half>(v.x), static_cast<lc_half>(v.y), static_cast<lc_half>(v.z), static_cast<lc_half>(v.w)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_half4(lc_float4 v) noexcept { return lc_half4{static_cast<lc_half>(v.x), static_cast<lc_half>(v.y), static_cast<lc_half>(v.z), static_cast<lc_half>(v.w)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_half4(lc_bool4 v) noexcept { return lc_half4{static_cast<lc_half>(v.x), static_cast<lc_half>(v.y), static_cast<lc_half>(v.z), static_cast<lc_half>(v.w)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_half4(lc_long4 v) noexcept { return lc_half4{static_cast<lc_half>(v.x), static_cast<lc_half>(v.y), static_cast<lc_half>(v.z), static_cast<lc_half>(v.w)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_half4(lc_ulong4 v) noexcept { return lc_half4{static_cast<lc_half>(v.x), static_cast<lc_half>(v.y), static_cast<lc_half>(v.z), static_cast<lc_half>(v.w)}; }

[[nodiscard]] __device__ inline constexpr auto lc_make_float2(lc_float s = 0) noexcept { return lc_float2{s, s}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_float2(lc_float x, lc_float y) noexcept { return lc_float2{x, y}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_float2(lc_byte2 v) noexcept { return lc_float2{static_cast<lc_float>(v.x), static_cast<lc_float>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_float2(lc_byte3 v) noexcept { return lc_float2{static_cast<lc_float>(v.x), static_cast<lc_float>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_float2(lc_byte4 v) noexcept { return lc_float2{static_cast<lc_float>(v.x), static_cast<lc_float>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_float2(lc_ubyte2 v) noexcept { return lc_float2{static_cast<lc_float>(v.x), static_cast<lc_float>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_float2(lc_ubyte3 v) noexcept { return lc_float2{static_cast<lc_float>(v.x), static_cast<lc_float>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_float2(lc_ubyte4 v) noexcept { return lc_float2{static_cast<lc_float>(v.x), static_cast<lc_float>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_float2(lc_short2 v) noexcept { return lc_float2{static_cast<lc_float>(v.x), static_cast<lc_float>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_float2(lc_short3 v) noexcept { return lc_float2{static_cast<lc_float>(v.x), static_cast<lc_float>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_float2(lc_short4 v) noexcept { return lc_float2{static_cast<lc_float>(v.x), static_cast<lc_float>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_float2(lc_ushort2 v) noexcept { return lc_float2{static_cast<lc_float>(v.x), static_cast<lc_float>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_float2(lc_ushort3 v) noexcept { return lc_float2{static_cast<lc_float>(v.x), static_cast<lc_float>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_float2(lc_ushort4 v) noexcept { return lc_float2{static_cast<lc_float>(v.x), static_cast<lc_float>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_float2(lc_int2 v) noexcept { return lc_float2{static_cast<lc_float>(v.x), static_cast<lc_float>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_float2(lc_int3 v) noexcept { return lc_float2{static_cast<lc_float>(v.x), static_cast<lc_float>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_float2(lc_int4 v) noexcept { return lc_float2{static_cast<lc_float>(v.x), static_cast<lc_float>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_float2(lc_uint2 v) noexcept { return lc_float2{static_cast<lc_float>(v.x), static_cast<lc_float>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_float2(lc_uint3 v) noexcept { return lc_float2{static_cast<lc_float>(v.x), static_cast<lc_float>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_float2(lc_uint4 v) noexcept { return lc_float2{static_cast<lc_float>(v.x), static_cast<lc_float>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_float2(lc_half2 v) noexcept { return lc_float2{static_cast<lc_float>(v.x), static_cast<lc_float>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_float2(lc_half3 v) noexcept { return lc_float2{static_cast<lc_float>(v.x), static_cast<lc_float>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_float2(lc_half4 v) noexcept { return lc_float2{static_cast<lc_float>(v.x), static_cast<lc_float>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_float2(lc_float2 v) noexcept { return lc_float2{static_cast<lc_float>(v.x), static_cast<lc_float>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_float2(lc_float3 v) noexcept { return lc_float2{static_cast<lc_float>(v.x), static_cast<lc_float>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_float2(lc_float4 v) noexcept { return lc_float2{static_cast<lc_float>(v.x), static_cast<lc_float>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_float2(lc_bool2 v) noexcept { return lc_float2{static_cast<lc_float>(v.x), static_cast<lc_float>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_float2(lc_bool3 v) noexcept { return lc_float2{static_cast<lc_float>(v.x), static_cast<lc_float>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_float2(lc_bool4 v) noexcept { return lc_float2{static_cast<lc_float>(v.x), static_cast<lc_float>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_float2(lc_long2 v) noexcept { return lc_float2{static_cast<lc_float>(v.x), static_cast<lc_float>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_float2(lc_long3 v) noexcept { return lc_float2{static_cast<lc_float>(v.x), static_cast<lc_float>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_float2(lc_long4 v) noexcept { return lc_float2{static_cast<lc_float>(v.x), static_cast<lc_float>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_float2(lc_ulong2 v) noexcept { return lc_float2{static_cast<lc_float>(v.x), static_cast<lc_float>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_float2(lc_ulong3 v) noexcept { return lc_float2{static_cast<lc_float>(v.x), static_cast<lc_float>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_float2(lc_ulong4 v) noexcept { return lc_float2{static_cast<lc_float>(v.x), static_cast<lc_float>(v.y)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_float3(lc_float s = 0) noexcept { return lc_float3{s, s, s}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_float3(lc_float x, lc_float y, lc_float z) noexcept { return lc_float3{x, y, z}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_float3(lc_float x, lc_float2 yz) noexcept { return lc_float3{x, yz.x, yz.y}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_float3(lc_float2 xy, lc_float z) noexcept { return lc_float3{xy.x, xy.y, z}; }
[[nodiscard]] __device__ constexpr auto lc_make_float3(lc_byte3 v) noexcept { return lc_float3{static_cast<lc_float>(v.x), static_cast<lc_float>(v.y), static_cast<lc_float>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_float3(lc_byte4 v) noexcept { return lc_float3{static_cast<lc_float>(v.x), static_cast<lc_float>(v.y), static_cast<lc_float>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_float3(lc_ubyte3 v) noexcept { return lc_float3{static_cast<lc_float>(v.x), static_cast<lc_float>(v.y), static_cast<lc_float>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_float3(lc_ubyte4 v) noexcept { return lc_float3{static_cast<lc_float>(v.x), static_cast<lc_float>(v.y), static_cast<lc_float>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_float3(lc_short3 v) noexcept { return lc_float3{static_cast<lc_float>(v.x), static_cast<lc_float>(v.y), static_cast<lc_float>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_float3(lc_short4 v) noexcept { return lc_float3{static_cast<lc_float>(v.x), static_cast<lc_float>(v.y), static_cast<lc_float>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_float3(lc_ushort3 v) noexcept { return lc_float3{static_cast<lc_float>(v.x), static_cast<lc_float>(v.y), static_cast<lc_float>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_float3(lc_ushort4 v) noexcept { return lc_float3{static_cast<lc_float>(v.x), static_cast<lc_float>(v.y), static_cast<lc_float>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_float3(lc_int3 v) noexcept { return lc_float3{static_cast<lc_float>(v.x), static_cast<lc_float>(v.y), static_cast<lc_float>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_float3(lc_int4 v) noexcept { return lc_float3{static_cast<lc_float>(v.x), static_cast<lc_float>(v.y), static_cast<lc_float>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_float3(lc_uint3 v) noexcept { return lc_float3{static_cast<lc_float>(v.x), static_cast<lc_float>(v.y), static_cast<lc_float>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_float3(lc_uint4 v) noexcept { return lc_float3{static_cast<lc_float>(v.x), static_cast<lc_float>(v.y), static_cast<lc_float>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_float3(lc_half3 v) noexcept { return lc_float3{static_cast<lc_float>(v.x), static_cast<lc_float>(v.y), static_cast<lc_float>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_float3(lc_half4 v) noexcept { return lc_float3{static_cast<lc_float>(v.x), static_cast<lc_float>(v.y), static_cast<lc_float>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_float3(lc_float3 v) noexcept { return lc_float3{static_cast<lc_float>(v.x), static_cast<lc_float>(v.y), static_cast<lc_float>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_float3(lc_float4 v) noexcept { return lc_float3{static_cast<lc_float>(v.x), static_cast<lc_float>(v.y), static_cast<lc_float>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_float3(lc_bool3 v) noexcept { return lc_float3{static_cast<lc_float>(v.x), static_cast<lc_float>(v.y), static_cast<lc_float>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_float3(lc_bool4 v) noexcept { return lc_float3{static_cast<lc_float>(v.x), static_cast<lc_float>(v.y), static_cast<lc_float>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_float3(lc_long3 v) noexcept { return lc_float3{static_cast<lc_float>(v.x), static_cast<lc_float>(v.y), static_cast<lc_float>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_float3(lc_long4 v) noexcept { return lc_float3{static_cast<lc_float>(v.x), static_cast<lc_float>(v.y), static_cast<lc_float>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_float3(lc_ulong3 v) noexcept { return lc_float3{static_cast<lc_float>(v.x), static_cast<lc_float>(v.y), static_cast<lc_float>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_float3(lc_ulong4 v) noexcept { return lc_float3{static_cast<lc_float>(v.x), static_cast<lc_float>(v.y), static_cast<lc_float>(v.z)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_float4(lc_float s = 0) noexcept { return lc_float4{s, s, s, s}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_float4(lc_float x, lc_float y, lc_float z, lc_float w) noexcept { return lc_float4{x, y, z, w}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_float4(lc_float x, lc_float y, lc_float2 zw) noexcept { return lc_float4{x, y, zw.x, zw.y}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_float4(lc_float x, lc_float2 yz, lc_float w) noexcept { return lc_float4{x, yz.x, yz.y, w}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_float4(lc_float2 xy, lc_float z, lc_float w) noexcept { return lc_float4{xy.x, xy.y, z, w}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_float4(lc_float2 xy, lc_float2 zw) noexcept { return lc_float4{xy.x, xy.y, zw.x, zw.y}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_float4(lc_float x, lc_float3 yzw) noexcept { return lc_float4{x, yzw.x, yzw.y, yzw.z}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_float4(lc_float3 xyz, lc_float w) noexcept { return lc_float4{xyz.x, xyz.y, xyz.z, w}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_float4(lc_byte4 v) noexcept { return lc_float4{static_cast<lc_float>(v.x), static_cast<lc_float>(v.y), static_cast<lc_float>(v.z), static_cast<lc_float>(v.w)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_float4(lc_ubyte4 v) noexcept { return lc_float4{static_cast<lc_float>(v.x), static_cast<lc_float>(v.y), static_cast<lc_float>(v.z), static_cast<lc_float>(v.w)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_float4(lc_short4 v) noexcept { return lc_float4{static_cast<lc_float>(v.x), static_cast<lc_float>(v.y), static_cast<lc_float>(v.z), static_cast<lc_float>(v.w)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_float4(lc_ushort4 v) noexcept { return lc_float4{static_cast<lc_float>(v.x), static_cast<lc_float>(v.y), static_cast<lc_float>(v.z), static_cast<lc_float>(v.w)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_float4(lc_int4 v) noexcept { return lc_float4{static_cast<lc_float>(v.x), static_cast<lc_float>(v.y), static_cast<lc_float>(v.z), static_cast<lc_float>(v.w)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_float4(lc_uint4 v) noexcept { return lc_float4{static_cast<lc_float>(v.x), static_cast<lc_float>(v.y), static_cast<lc_float>(v.z), static_cast<lc_float>(v.w)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_float4(lc_half4 v) noexcept { return lc_float4{static_cast<lc_float>(v.x), static_cast<lc_float>(v.y), static_cast<lc_float>(v.z), static_cast<lc_float>(v.w)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_float4(lc_float4 v) noexcept { return lc_float4{static_cast<lc_float>(v.x), static_cast<lc_float>(v.y), static_cast<lc_float>(v.z), static_cast<lc_float>(v.w)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_float4(lc_bool4 v) noexcept { return lc_float4{static_cast<lc_float>(v.x), static_cast<lc_float>(v.y), static_cast<lc_float>(v.z), static_cast<lc_float>(v.w)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_float4(lc_long4 v) noexcept { return lc_float4{static_cast<lc_float>(v.x), static_cast<lc_float>(v.y), static_cast<lc_float>(v.z), static_cast<lc_float>(v.w)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_float4(lc_ulong4 v) noexcept { return lc_float4{static_cast<lc_float>(v.x), static_cast<lc_float>(v.y), static_cast<lc_float>(v.z), static_cast<lc_float>(v.w)}; }

[[nodiscard]] __device__ inline constexpr auto lc_make_bool2(lc_bool s = 0) noexcept { return lc_bool2{s, s}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_bool2(lc_bool x, lc_bool y) noexcept { return lc_bool2{x, y}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_bool2(lc_byte2 v) noexcept { return lc_bool2{static_cast<lc_bool>(v.x), static_cast<lc_bool>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_bool2(lc_byte3 v) noexcept { return lc_bool2{static_cast<lc_bool>(v.x), static_cast<lc_bool>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_bool2(lc_byte4 v) noexcept { return lc_bool2{static_cast<lc_bool>(v.x), static_cast<lc_bool>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_bool2(lc_ubyte2 v) noexcept { return lc_bool2{static_cast<lc_bool>(v.x), static_cast<lc_bool>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_bool2(lc_ubyte3 v) noexcept { return lc_bool2{static_cast<lc_bool>(v.x), static_cast<lc_bool>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_bool2(lc_ubyte4 v) noexcept { return lc_bool2{static_cast<lc_bool>(v.x), static_cast<lc_bool>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_bool2(lc_short2 v) noexcept { return lc_bool2{static_cast<lc_bool>(v.x), static_cast<lc_bool>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_bool2(lc_short3 v) noexcept { return lc_bool2{static_cast<lc_bool>(v.x), static_cast<lc_bool>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_bool2(lc_short4 v) noexcept { return lc_bool2{static_cast<lc_bool>(v.x), static_cast<lc_bool>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_bool2(lc_ushort2 v) noexcept { return lc_bool2{static_cast<lc_bool>(v.x), static_cast<lc_bool>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_bool2(lc_ushort3 v) noexcept { return lc_bool2{static_cast<lc_bool>(v.x), static_cast<lc_bool>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_bool2(lc_ushort4 v) noexcept { return lc_bool2{static_cast<lc_bool>(v.x), static_cast<lc_bool>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_bool2(lc_int2 v) noexcept { return lc_bool2{static_cast<lc_bool>(v.x), static_cast<lc_bool>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_bool2(lc_int3 v) noexcept { return lc_bool2{static_cast<lc_bool>(v.x), static_cast<lc_bool>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_bool2(lc_int4 v) noexcept { return lc_bool2{static_cast<lc_bool>(v.x), static_cast<lc_bool>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_bool2(lc_uint2 v) noexcept { return lc_bool2{static_cast<lc_bool>(v.x), static_cast<lc_bool>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_bool2(lc_uint3 v) noexcept { return lc_bool2{static_cast<lc_bool>(v.x), static_cast<lc_bool>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_bool2(lc_uint4 v) noexcept { return lc_bool2{static_cast<lc_bool>(v.x), static_cast<lc_bool>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_bool2(lc_half2 v) noexcept { return lc_bool2{static_cast<lc_bool>(v.x), static_cast<lc_bool>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_bool2(lc_half3 v) noexcept { return lc_bool2{static_cast<lc_bool>(v.x), static_cast<lc_bool>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_bool2(lc_half4 v) noexcept { return lc_bool2{static_cast<lc_bool>(v.x), static_cast<lc_bool>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_bool2(lc_float2 v) noexcept { return lc_bool2{static_cast<lc_bool>(v.x), static_cast<lc_bool>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_bool2(lc_float3 v) noexcept { return lc_bool2{static_cast<lc_bool>(v.x), static_cast<lc_bool>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_bool2(lc_float4 v) noexcept { return lc_bool2{static_cast<lc_bool>(v.x), static_cast<lc_bool>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_bool2(lc_bool2 v) noexcept { return lc_bool2{static_cast<lc_bool>(v.x), static_cast<lc_bool>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_bool2(lc_bool3 v) noexcept { return lc_bool2{static_cast<lc_bool>(v.x), static_cast<lc_bool>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_bool2(lc_bool4 v) noexcept { return lc_bool2{static_cast<lc_bool>(v.x), static_cast<lc_bool>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_bool2(lc_long2 v) noexcept { return lc_bool2{static_cast<lc_bool>(v.x), static_cast<lc_bool>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_bool2(lc_long3 v) noexcept { return lc_bool2{static_cast<lc_bool>(v.x), static_cast<lc_bool>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_bool2(lc_long4 v) noexcept { return lc_bool2{static_cast<lc_bool>(v.x), static_cast<lc_bool>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_bool2(lc_ulong2 v) noexcept { return lc_bool2{static_cast<lc_bool>(v.x), static_cast<lc_bool>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_bool2(lc_ulong3 v) noexcept { return lc_bool2{static_cast<lc_bool>(v.x), static_cast<lc_bool>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_bool2(lc_ulong4 v) noexcept { return lc_bool2{static_cast<lc_bool>(v.x), static_cast<lc_bool>(v.y)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_bool3(lc_bool s = 0) noexcept { return lc_bool3{s, s, s}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_bool3(lc_bool x, lc_bool y, lc_bool z) noexcept { return lc_bool3{x, y, z}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_bool3(lc_bool x, lc_bool2 yz) noexcept { return lc_bool3{x, yz.x, yz.y}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_bool3(lc_bool2 xy, lc_bool z) noexcept { return lc_bool3{xy.x, xy.y, z}; }
[[nodiscard]] __device__ constexpr auto lc_make_bool3(lc_byte3 v) noexcept { return lc_bool3{static_cast<lc_bool>(v.x), static_cast<lc_bool>(v.y), static_cast<lc_bool>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_bool3(lc_byte4 v) noexcept { return lc_bool3{static_cast<lc_bool>(v.x), static_cast<lc_bool>(v.y), static_cast<lc_bool>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_bool3(lc_ubyte3 v) noexcept { return lc_bool3{static_cast<lc_bool>(v.x), static_cast<lc_bool>(v.y), static_cast<lc_bool>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_bool3(lc_ubyte4 v) noexcept { return lc_bool3{static_cast<lc_bool>(v.x), static_cast<lc_bool>(v.y), static_cast<lc_bool>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_bool3(lc_short3 v) noexcept { return lc_bool3{static_cast<lc_bool>(v.x), static_cast<lc_bool>(v.y), static_cast<lc_bool>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_bool3(lc_short4 v) noexcept { return lc_bool3{static_cast<lc_bool>(v.x), static_cast<lc_bool>(v.y), static_cast<lc_bool>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_bool3(lc_ushort3 v) noexcept { return lc_bool3{static_cast<lc_bool>(v.x), static_cast<lc_bool>(v.y), static_cast<lc_bool>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_bool3(lc_ushort4 v) noexcept { return lc_bool3{static_cast<lc_bool>(v.x), static_cast<lc_bool>(v.y), static_cast<lc_bool>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_bool3(lc_int3 v) noexcept { return lc_bool3{static_cast<lc_bool>(v.x), static_cast<lc_bool>(v.y), static_cast<lc_bool>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_bool3(lc_int4 v) noexcept { return lc_bool3{static_cast<lc_bool>(v.x), static_cast<lc_bool>(v.y), static_cast<lc_bool>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_bool3(lc_uint3 v) noexcept { return lc_bool3{static_cast<lc_bool>(v.x), static_cast<lc_bool>(v.y), static_cast<lc_bool>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_bool3(lc_uint4 v) noexcept { return lc_bool3{static_cast<lc_bool>(v.x), static_cast<lc_bool>(v.y), static_cast<lc_bool>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_bool3(lc_half3 v) noexcept { return lc_bool3{static_cast<lc_bool>(v.x), static_cast<lc_bool>(v.y), static_cast<lc_bool>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_bool3(lc_half4 v) noexcept { return lc_bool3{static_cast<lc_bool>(v.x), static_cast<lc_bool>(v.y), static_cast<lc_bool>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_bool3(lc_float3 v) noexcept { return lc_bool3{static_cast<lc_bool>(v.x), static_cast<lc_bool>(v.y), static_cast<lc_bool>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_bool3(lc_float4 v) noexcept { return lc_bool3{static_cast<lc_bool>(v.x), static_cast<lc_bool>(v.y), static_cast<lc_bool>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_bool3(lc_bool3 v) noexcept { return lc_bool3{static_cast<lc_bool>(v.x), static_cast<lc_bool>(v.y), static_cast<lc_bool>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_bool3(lc_bool4 v) noexcept { return lc_bool3{static_cast<lc_bool>(v.x), static_cast<lc_bool>(v.y), static_cast<lc_bool>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_bool3(lc_long3 v) noexcept { return lc_bool3{static_cast<lc_bool>(v.x), static_cast<lc_bool>(v.y), static_cast<lc_bool>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_bool3(lc_long4 v) noexcept { return lc_bool3{static_cast<lc_bool>(v.x), static_cast<lc_bool>(v.y), static_cast<lc_bool>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_bool3(lc_ulong3 v) noexcept { return lc_bool3{static_cast<lc_bool>(v.x), static_cast<lc_bool>(v.y), static_cast<lc_bool>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_bool3(lc_ulong4 v) noexcept { return lc_bool3{static_cast<lc_bool>(v.x), static_cast<lc_bool>(v.y), static_cast<lc_bool>(v.z)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_bool4(lc_bool s = 0) noexcept { return lc_bool4{s, s, s, s}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_bool4(lc_bool x, lc_bool y, lc_bool z, lc_bool w) noexcept { return lc_bool4{x, y, z, w}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_bool4(lc_bool x, lc_bool y, lc_bool2 zw) noexcept { return lc_bool4{x, y, zw.x, zw.y}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_bool4(lc_bool x, lc_bool2 yz, lc_bool w) noexcept { return lc_bool4{x, yz.x, yz.y, w}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_bool4(lc_bool2 xy, lc_bool z, lc_bool w) noexcept { return lc_bool4{xy.x, xy.y, z, w}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_bool4(lc_bool2 xy, lc_bool2 zw) noexcept { return lc_bool4{xy.x, xy.y, zw.x, zw.y}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_bool4(lc_bool x, lc_bool3 yzw) noexcept { return lc_bool4{x, yzw.x, yzw.y, yzw.z}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_bool4(lc_bool3 xyz, lc_bool w) noexcept { return lc_bool4{xyz.x, xyz.y, xyz.z, w}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_bool4(lc_byte4 v) noexcept { return lc_bool4{static_cast<lc_bool>(v.x), static_cast<lc_bool>(v.y), static_cast<lc_bool>(v.z), static_cast<lc_bool>(v.w)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_bool4(lc_ubyte4 v) noexcept { return lc_bool4{static_cast<lc_bool>(v.x), static_cast<lc_bool>(v.y), static_cast<lc_bool>(v.z), static_cast<lc_bool>(v.w)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_bool4(lc_short4 v) noexcept { return lc_bool4{static_cast<lc_bool>(v.x), static_cast<lc_bool>(v.y), static_cast<lc_bool>(v.z), static_cast<lc_bool>(v.w)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_bool4(lc_ushort4 v) noexcept { return lc_bool4{static_cast<lc_bool>(v.x), static_cast<lc_bool>(v.y), static_cast<lc_bool>(v.z), static_cast<lc_bool>(v.w)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_bool4(lc_int4 v) noexcept { return lc_bool4{static_cast<lc_bool>(v.x), static_cast<lc_bool>(v.y), static_cast<lc_bool>(v.z), static_cast<lc_bool>(v.w)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_bool4(lc_uint4 v) noexcept { return lc_bool4{static_cast<lc_bool>(v.x), static_cast<lc_bool>(v.y), static_cast<lc_bool>(v.z), static_cast<lc_bool>(v.w)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_bool4(lc_half4 v) noexcept { return lc_bool4{static_cast<lc_bool>(v.x), static_cast<lc_bool>(v.y), static_cast<lc_bool>(v.z), static_cast<lc_bool>(v.w)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_bool4(lc_float4 v) noexcept { return lc_bool4{static_cast<lc_bool>(v.x), static_cast<lc_bool>(v.y), static_cast<lc_bool>(v.z), static_cast<lc_bool>(v.w)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_bool4(lc_bool4 v) noexcept { return lc_bool4{static_cast<lc_bool>(v.x), static_cast<lc_bool>(v.y), static_cast<lc_bool>(v.z), static_cast<lc_bool>(v.w)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_bool4(lc_long4 v) noexcept { return lc_bool4{static_cast<lc_bool>(v.x), static_cast<lc_bool>(v.y), static_cast<lc_bool>(v.z), static_cast<lc_bool>(v.w)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_bool4(lc_ulong4 v) noexcept { return lc_bool4{static_cast<lc_bool>(v.x), static_cast<lc_bool>(v.y), static_cast<lc_bool>(v.z), static_cast<lc_bool>(v.w)}; }

[[nodiscard]] __device__ inline constexpr auto lc_make_long2(lc_long s = 0) noexcept { return lc_long2{s, s}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_long2(lc_long x, lc_long y) noexcept { return lc_long2{x, y}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_long2(lc_byte2 v) noexcept { return lc_long2{static_cast<lc_long>(v.x), static_cast<lc_long>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_long2(lc_byte3 v) noexcept { return lc_long2{static_cast<lc_long>(v.x), static_cast<lc_long>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_long2(lc_byte4 v) noexcept { return lc_long2{static_cast<lc_long>(v.x), static_cast<lc_long>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_long2(lc_ubyte2 v) noexcept { return lc_long2{static_cast<lc_long>(v.x), static_cast<lc_long>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_long2(lc_ubyte3 v) noexcept { return lc_long2{static_cast<lc_long>(v.x), static_cast<lc_long>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_long2(lc_ubyte4 v) noexcept { return lc_long2{static_cast<lc_long>(v.x), static_cast<lc_long>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_long2(lc_short2 v) noexcept { return lc_long2{static_cast<lc_long>(v.x), static_cast<lc_long>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_long2(lc_short3 v) noexcept { return lc_long2{static_cast<lc_long>(v.x), static_cast<lc_long>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_long2(lc_short4 v) noexcept { return lc_long2{static_cast<lc_long>(v.x), static_cast<lc_long>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_long2(lc_ushort2 v) noexcept { return lc_long2{static_cast<lc_long>(v.x), static_cast<lc_long>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_long2(lc_ushort3 v) noexcept { return lc_long2{static_cast<lc_long>(v.x), static_cast<lc_long>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_long2(lc_ushort4 v) noexcept { return lc_long2{static_cast<lc_long>(v.x), static_cast<lc_long>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_long2(lc_int2 v) noexcept { return lc_long2{static_cast<lc_long>(v.x), static_cast<lc_long>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_long2(lc_int3 v) noexcept { return lc_long2{static_cast<lc_long>(v.x), static_cast<lc_long>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_long2(lc_int4 v) noexcept { return lc_long2{static_cast<lc_long>(v.x), static_cast<lc_long>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_long2(lc_uint2 v) noexcept { return lc_long2{static_cast<lc_long>(v.x), static_cast<lc_long>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_long2(lc_uint3 v) noexcept { return lc_long2{static_cast<lc_long>(v.x), static_cast<lc_long>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_long2(lc_uint4 v) noexcept { return lc_long2{static_cast<lc_long>(v.x), static_cast<lc_long>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_long2(lc_half2 v) noexcept { return lc_long2{static_cast<lc_long>(v.x), static_cast<lc_long>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_long2(lc_half3 v) noexcept { return lc_long2{static_cast<lc_long>(v.x), static_cast<lc_long>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_long2(lc_half4 v) noexcept { return lc_long2{static_cast<lc_long>(v.x), static_cast<lc_long>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_long2(lc_float2 v) noexcept { return lc_long2{static_cast<lc_long>(v.x), static_cast<lc_long>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_long2(lc_float3 v) noexcept { return lc_long2{static_cast<lc_long>(v.x), static_cast<lc_long>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_long2(lc_float4 v) noexcept { return lc_long2{static_cast<lc_long>(v.x), static_cast<lc_long>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_long2(lc_bool2 v) noexcept { return lc_long2{static_cast<lc_long>(v.x), static_cast<lc_long>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_long2(lc_bool3 v) noexcept { return lc_long2{static_cast<lc_long>(v.x), static_cast<lc_long>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_long2(lc_bool4 v) noexcept { return lc_long2{static_cast<lc_long>(v.x), static_cast<lc_long>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_long2(lc_long2 v) noexcept { return lc_long2{static_cast<lc_long>(v.x), static_cast<lc_long>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_long2(lc_long3 v) noexcept { return lc_long2{static_cast<lc_long>(v.x), static_cast<lc_long>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_long2(lc_long4 v) noexcept { return lc_long2{static_cast<lc_long>(v.x), static_cast<lc_long>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_long2(lc_ulong2 v) noexcept { return lc_long2{static_cast<lc_long>(v.x), static_cast<lc_long>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_long2(lc_ulong3 v) noexcept { return lc_long2{static_cast<lc_long>(v.x), static_cast<lc_long>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_long2(lc_ulong4 v) noexcept { return lc_long2{static_cast<lc_long>(v.x), static_cast<lc_long>(v.y)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_long3(lc_long s = 0) noexcept { return lc_long3{s, s, s}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_long3(lc_long x, lc_long y, lc_long z) noexcept { return lc_long3{x, y, z}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_long3(lc_long x, lc_long2 yz) noexcept { return lc_long3{x, yz.x, yz.y}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_long3(lc_long2 xy, lc_long z) noexcept { return lc_long3{xy.x, xy.y, z}; }
[[nodiscard]] __device__ constexpr auto lc_make_long3(lc_byte3 v) noexcept { return lc_long3{static_cast<lc_long>(v.x), static_cast<lc_long>(v.y), static_cast<lc_long>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_long3(lc_byte4 v) noexcept { return lc_long3{static_cast<lc_long>(v.x), static_cast<lc_long>(v.y), static_cast<lc_long>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_long3(lc_ubyte3 v) noexcept { return lc_long3{static_cast<lc_long>(v.x), static_cast<lc_long>(v.y), static_cast<lc_long>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_long3(lc_ubyte4 v) noexcept { return lc_long3{static_cast<lc_long>(v.x), static_cast<lc_long>(v.y), static_cast<lc_long>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_long3(lc_short3 v) noexcept { return lc_long3{static_cast<lc_long>(v.x), static_cast<lc_long>(v.y), static_cast<lc_long>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_long3(lc_short4 v) noexcept { return lc_long3{static_cast<lc_long>(v.x), static_cast<lc_long>(v.y), static_cast<lc_long>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_long3(lc_ushort3 v) noexcept { return lc_long3{static_cast<lc_long>(v.x), static_cast<lc_long>(v.y), static_cast<lc_long>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_long3(lc_ushort4 v) noexcept { return lc_long3{static_cast<lc_long>(v.x), static_cast<lc_long>(v.y), static_cast<lc_long>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_long3(lc_int3 v) noexcept { return lc_long3{static_cast<lc_long>(v.x), static_cast<lc_long>(v.y), static_cast<lc_long>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_long3(lc_int4 v) noexcept { return lc_long3{static_cast<lc_long>(v.x), static_cast<lc_long>(v.y), static_cast<lc_long>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_long3(lc_uint3 v) noexcept { return lc_long3{static_cast<lc_long>(v.x), static_cast<lc_long>(v.y), static_cast<lc_long>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_long3(lc_uint4 v) noexcept { return lc_long3{static_cast<lc_long>(v.x), static_cast<lc_long>(v.y), static_cast<lc_long>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_long3(lc_half3 v) noexcept { return lc_long3{static_cast<lc_long>(v.x), static_cast<lc_long>(v.y), static_cast<lc_long>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_long3(lc_half4 v) noexcept { return lc_long3{static_cast<lc_long>(v.x), static_cast<lc_long>(v.y), static_cast<lc_long>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_long3(lc_float3 v) noexcept { return lc_long3{static_cast<lc_long>(v.x), static_cast<lc_long>(v.y), static_cast<lc_long>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_long3(lc_float4 v) noexcept { return lc_long3{static_cast<lc_long>(v.x), static_cast<lc_long>(v.y), static_cast<lc_long>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_long3(lc_bool3 v) noexcept { return lc_long3{static_cast<lc_long>(v.x), static_cast<lc_long>(v.y), static_cast<lc_long>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_long3(lc_bool4 v) noexcept { return lc_long3{static_cast<lc_long>(v.x), static_cast<lc_long>(v.y), static_cast<lc_long>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_long3(lc_long3 v) noexcept { return lc_long3{static_cast<lc_long>(v.x), static_cast<lc_long>(v.y), static_cast<lc_long>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_long3(lc_long4 v) noexcept { return lc_long3{static_cast<lc_long>(v.x), static_cast<lc_long>(v.y), static_cast<lc_long>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_long3(lc_ulong3 v) noexcept { return lc_long3{static_cast<lc_long>(v.x), static_cast<lc_long>(v.y), static_cast<lc_long>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_long3(lc_ulong4 v) noexcept { return lc_long3{static_cast<lc_long>(v.x), static_cast<lc_long>(v.y), static_cast<lc_long>(v.z)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_long4(lc_long s = 0) noexcept { return lc_long4{s, s, s, s}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_long4(lc_long x, lc_long y, lc_long z, lc_long w) noexcept { return lc_long4{x, y, z, w}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_long4(lc_long x, lc_long y, lc_long2 zw) noexcept { return lc_long4{x, y, zw.x, zw.y}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_long4(lc_long x, lc_long2 yz, lc_long w) noexcept { return lc_long4{x, yz.x, yz.y, w}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_long4(lc_long2 xy, lc_long z, lc_long w) noexcept { return lc_long4{xy.x, xy.y, z, w}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_long4(lc_long2 xy, lc_long2 zw) noexcept { return lc_long4{xy.x, xy.y, zw.x, zw.y}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_long4(lc_long x, lc_long3 yzw) noexcept { return lc_long4{x, yzw.x, yzw.y, yzw.z}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_long4(lc_long3 xyz, lc_long w) noexcept { return lc_long4{xyz.x, xyz.y, xyz.z, w}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_long4(lc_byte4 v) noexcept { return lc_long4{static_cast<lc_long>(v.x), static_cast<lc_long>(v.y), static_cast<lc_long>(v.z), static_cast<lc_long>(v.w)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_long4(lc_ubyte4 v) noexcept { return lc_long4{static_cast<lc_long>(v.x), static_cast<lc_long>(v.y), static_cast<lc_long>(v.z), static_cast<lc_long>(v.w)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_long4(lc_short4 v) noexcept { return lc_long4{static_cast<lc_long>(v.x), static_cast<lc_long>(v.y), static_cast<lc_long>(v.z), static_cast<lc_long>(v.w)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_long4(lc_ushort4 v) noexcept { return lc_long4{static_cast<lc_long>(v.x), static_cast<lc_long>(v.y), static_cast<lc_long>(v.z), static_cast<lc_long>(v.w)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_long4(lc_int4 v) noexcept { return lc_long4{static_cast<lc_long>(v.x), static_cast<lc_long>(v.y), static_cast<lc_long>(v.z), static_cast<lc_long>(v.w)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_long4(lc_uint4 v) noexcept { return lc_long4{static_cast<lc_long>(v.x), static_cast<lc_long>(v.y), static_cast<lc_long>(v.z), static_cast<lc_long>(v.w)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_long4(lc_half4 v) noexcept { return lc_long4{static_cast<lc_long>(v.x), static_cast<lc_long>(v.y), static_cast<lc_long>(v.z), static_cast<lc_long>(v.w)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_long4(lc_float4 v) noexcept { return lc_long4{static_cast<lc_long>(v.x), static_cast<lc_long>(v.y), static_cast<lc_long>(v.z), static_cast<lc_long>(v.w)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_long4(lc_bool4 v) noexcept { return lc_long4{static_cast<lc_long>(v.x), static_cast<lc_long>(v.y), static_cast<lc_long>(v.z), static_cast<lc_long>(v.w)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_long4(lc_long4 v) noexcept { return lc_long4{static_cast<lc_long>(v.x), static_cast<lc_long>(v.y), static_cast<lc_long>(v.z), static_cast<lc_long>(v.w)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_long4(lc_ulong4 v) noexcept { return lc_long4{static_cast<lc_long>(v.x), static_cast<lc_long>(v.y), static_cast<lc_long>(v.z), static_cast<lc_long>(v.w)}; }

[[nodiscard]] __device__ inline constexpr auto lc_make_ulong2(lc_ulong s = 0) noexcept { return lc_ulong2{s, s}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ulong2(lc_ulong x, lc_ulong y) noexcept { return lc_ulong2{x, y}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ulong2(lc_byte2 v) noexcept { return lc_ulong2{static_cast<lc_ulong>(v.x), static_cast<lc_ulong>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ulong2(lc_byte3 v) noexcept { return lc_ulong2{static_cast<lc_ulong>(v.x), static_cast<lc_ulong>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ulong2(lc_byte4 v) noexcept { return lc_ulong2{static_cast<lc_ulong>(v.x), static_cast<lc_ulong>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ulong2(lc_ubyte2 v) noexcept { return lc_ulong2{static_cast<lc_ulong>(v.x), static_cast<lc_ulong>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ulong2(lc_ubyte3 v) noexcept { return lc_ulong2{static_cast<lc_ulong>(v.x), static_cast<lc_ulong>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ulong2(lc_ubyte4 v) noexcept { return lc_ulong2{static_cast<lc_ulong>(v.x), static_cast<lc_ulong>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ulong2(lc_short2 v) noexcept { return lc_ulong2{static_cast<lc_ulong>(v.x), static_cast<lc_ulong>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ulong2(lc_short3 v) noexcept { return lc_ulong2{static_cast<lc_ulong>(v.x), static_cast<lc_ulong>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ulong2(lc_short4 v) noexcept { return lc_ulong2{static_cast<lc_ulong>(v.x), static_cast<lc_ulong>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ulong2(lc_ushort2 v) noexcept { return lc_ulong2{static_cast<lc_ulong>(v.x), static_cast<lc_ulong>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ulong2(lc_ushort3 v) noexcept { return lc_ulong2{static_cast<lc_ulong>(v.x), static_cast<lc_ulong>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ulong2(lc_ushort4 v) noexcept { return lc_ulong2{static_cast<lc_ulong>(v.x), static_cast<lc_ulong>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ulong2(lc_int2 v) noexcept { return lc_ulong2{static_cast<lc_ulong>(v.x), static_cast<lc_ulong>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ulong2(lc_int3 v) noexcept { return lc_ulong2{static_cast<lc_ulong>(v.x), static_cast<lc_ulong>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ulong2(lc_int4 v) noexcept { return lc_ulong2{static_cast<lc_ulong>(v.x), static_cast<lc_ulong>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ulong2(lc_uint2 v) noexcept { return lc_ulong2{static_cast<lc_ulong>(v.x), static_cast<lc_ulong>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ulong2(lc_uint3 v) noexcept { return lc_ulong2{static_cast<lc_ulong>(v.x), static_cast<lc_ulong>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ulong2(lc_uint4 v) noexcept { return lc_ulong2{static_cast<lc_ulong>(v.x), static_cast<lc_ulong>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ulong2(lc_half2 v) noexcept { return lc_ulong2{static_cast<lc_ulong>(v.x), static_cast<lc_ulong>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ulong2(lc_half3 v) noexcept { return lc_ulong2{static_cast<lc_ulong>(v.x), static_cast<lc_ulong>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ulong2(lc_half4 v) noexcept { return lc_ulong2{static_cast<lc_ulong>(v.x), static_cast<lc_ulong>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ulong2(lc_float2 v) noexcept { return lc_ulong2{static_cast<lc_ulong>(v.x), static_cast<lc_ulong>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ulong2(lc_float3 v) noexcept { return lc_ulong2{static_cast<lc_ulong>(v.x), static_cast<lc_ulong>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ulong2(lc_float4 v) noexcept { return lc_ulong2{static_cast<lc_ulong>(v.x), static_cast<lc_ulong>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ulong2(lc_bool2 v) noexcept { return lc_ulong2{static_cast<lc_ulong>(v.x), static_cast<lc_ulong>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ulong2(lc_bool3 v) noexcept { return lc_ulong2{static_cast<lc_ulong>(v.x), static_cast<lc_ulong>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ulong2(lc_bool4 v) noexcept { return lc_ulong2{static_cast<lc_ulong>(v.x), static_cast<lc_ulong>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ulong2(lc_long2 v) noexcept { return lc_ulong2{static_cast<lc_ulong>(v.x), static_cast<lc_ulong>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ulong2(lc_long3 v) noexcept { return lc_ulong2{static_cast<lc_ulong>(v.x), static_cast<lc_ulong>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ulong2(lc_long4 v) noexcept { return lc_ulong2{static_cast<lc_ulong>(v.x), static_cast<lc_ulong>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ulong2(lc_ulong2 v) noexcept { return lc_ulong2{static_cast<lc_ulong>(v.x), static_cast<lc_ulong>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ulong2(lc_ulong3 v) noexcept { return lc_ulong2{static_cast<lc_ulong>(v.x), static_cast<lc_ulong>(v.y)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ulong2(lc_ulong4 v) noexcept { return lc_ulong2{static_cast<lc_ulong>(v.x), static_cast<lc_ulong>(v.y)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_ulong3(lc_ulong s = 0) noexcept { return lc_ulong3{s, s, s}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ulong3(lc_ulong x, lc_ulong y, lc_ulong z) noexcept { return lc_ulong3{x, y, z}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ulong3(lc_ulong x, lc_ulong2 yz) noexcept { return lc_ulong3{x, yz.x, yz.y}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ulong3(lc_ulong2 xy, lc_ulong z) noexcept { return lc_ulong3{xy.x, xy.y, z}; }
[[nodiscard]] __device__ constexpr auto lc_make_ulong3(lc_byte3 v) noexcept { return lc_ulong3{static_cast<lc_ulong>(v.x), static_cast<lc_ulong>(v.y), static_cast<lc_ulong>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_ulong3(lc_byte4 v) noexcept { return lc_ulong3{static_cast<lc_ulong>(v.x), static_cast<lc_ulong>(v.y), static_cast<lc_ulong>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_ulong3(lc_ubyte3 v) noexcept { return lc_ulong3{static_cast<lc_ulong>(v.x), static_cast<lc_ulong>(v.y), static_cast<lc_ulong>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_ulong3(lc_ubyte4 v) noexcept { return lc_ulong3{static_cast<lc_ulong>(v.x), static_cast<lc_ulong>(v.y), static_cast<lc_ulong>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_ulong3(lc_short3 v) noexcept { return lc_ulong3{static_cast<lc_ulong>(v.x), static_cast<lc_ulong>(v.y), static_cast<lc_ulong>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_ulong3(lc_short4 v) noexcept { return lc_ulong3{static_cast<lc_ulong>(v.x), static_cast<lc_ulong>(v.y), static_cast<lc_ulong>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_ulong3(lc_ushort3 v) noexcept { return lc_ulong3{static_cast<lc_ulong>(v.x), static_cast<lc_ulong>(v.y), static_cast<lc_ulong>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_ulong3(lc_ushort4 v) noexcept { return lc_ulong3{static_cast<lc_ulong>(v.x), static_cast<lc_ulong>(v.y), static_cast<lc_ulong>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_ulong3(lc_int3 v) noexcept { return lc_ulong3{static_cast<lc_ulong>(v.x), static_cast<lc_ulong>(v.y), static_cast<lc_ulong>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_ulong3(lc_int4 v) noexcept { return lc_ulong3{static_cast<lc_ulong>(v.x), static_cast<lc_ulong>(v.y), static_cast<lc_ulong>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_ulong3(lc_uint3 v) noexcept { return lc_ulong3{static_cast<lc_ulong>(v.x), static_cast<lc_ulong>(v.y), static_cast<lc_ulong>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_ulong3(lc_uint4 v) noexcept { return lc_ulong3{static_cast<lc_ulong>(v.x), static_cast<lc_ulong>(v.y), static_cast<lc_ulong>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_ulong3(lc_half3 v) noexcept { return lc_ulong3{static_cast<lc_ulong>(v.x), static_cast<lc_ulong>(v.y), static_cast<lc_ulong>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_ulong3(lc_half4 v) noexcept { return lc_ulong3{static_cast<lc_ulong>(v.x), static_cast<lc_ulong>(v.y), static_cast<lc_ulong>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_ulong3(lc_float3 v) noexcept { return lc_ulong3{static_cast<lc_ulong>(v.x), static_cast<lc_ulong>(v.y), static_cast<lc_ulong>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_ulong3(lc_float4 v) noexcept { return lc_ulong3{static_cast<lc_ulong>(v.x), static_cast<lc_ulong>(v.y), static_cast<lc_ulong>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_ulong3(lc_bool3 v) noexcept { return lc_ulong3{static_cast<lc_ulong>(v.x), static_cast<lc_ulong>(v.y), static_cast<lc_ulong>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_ulong3(lc_bool4 v) noexcept { return lc_ulong3{static_cast<lc_ulong>(v.x), static_cast<lc_ulong>(v.y), static_cast<lc_ulong>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_ulong3(lc_long3 v) noexcept { return lc_ulong3{static_cast<lc_ulong>(v.x), static_cast<lc_ulong>(v.y), static_cast<lc_ulong>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_ulong3(lc_long4 v) noexcept { return lc_ulong3{static_cast<lc_ulong>(v.x), static_cast<lc_ulong>(v.y), static_cast<lc_ulong>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_ulong3(lc_ulong3 v) noexcept { return lc_ulong3{static_cast<lc_ulong>(v.x), static_cast<lc_ulong>(v.y), static_cast<lc_ulong>(v.z)}; }
[[nodiscard]] __device__ constexpr auto lc_make_ulong3(lc_ulong4 v) noexcept { return lc_ulong3{static_cast<lc_ulong>(v.x), static_cast<lc_ulong>(v.y), static_cast<lc_ulong>(v.z)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_ulong4(lc_ulong s = 0) noexcept { return lc_ulong4{s, s, s, s}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ulong4(lc_ulong x, lc_ulong y, lc_ulong z, lc_ulong w) noexcept { return lc_ulong4{x, y, z, w}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ulong4(lc_ulong x, lc_ulong y, lc_ulong2 zw) noexcept { return lc_ulong4{x, y, zw.x, zw.y}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ulong4(lc_ulong x, lc_ulong2 yz, lc_ulong w) noexcept { return lc_ulong4{x, yz.x, yz.y, w}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ulong4(lc_ulong2 xy, lc_ulong z, lc_ulong w) noexcept { return lc_ulong4{xy.x, xy.y, z, w}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ulong4(lc_ulong2 xy, lc_ulong2 zw) noexcept { return lc_ulong4{xy.x, xy.y, zw.x, zw.y}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ulong4(lc_ulong x, lc_ulong3 yzw) noexcept { return lc_ulong4{x, yzw.x, yzw.y, yzw.z}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_ulong4(lc_ulong3 xyz, lc_ulong w) noexcept { return lc_ulong4{xyz.x, xyz.y, xyz.z, w}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_ulong4(lc_byte4 v) noexcept { return lc_ulong4{static_cast<lc_ulong>(v.x), static_cast<lc_ulong>(v.y), static_cast<lc_ulong>(v.z), static_cast<lc_ulong>(v.w)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_ulong4(lc_ubyte4 v) noexcept { return lc_ulong4{static_cast<lc_ulong>(v.x), static_cast<lc_ulong>(v.y), static_cast<lc_ulong>(v.z), static_cast<lc_ulong>(v.w)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_ulong4(lc_short4 v) noexcept { return lc_ulong4{static_cast<lc_ulong>(v.x), static_cast<lc_ulong>(v.y), static_cast<lc_ulong>(v.z), static_cast<lc_ulong>(v.w)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_ulong4(lc_ushort4 v) noexcept { return lc_ulong4{static_cast<lc_ulong>(v.x), static_cast<lc_ulong>(v.y), static_cast<lc_ulong>(v.z), static_cast<lc_ulong>(v.w)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_ulong4(lc_int4 v) noexcept { return lc_ulong4{static_cast<lc_ulong>(v.x), static_cast<lc_ulong>(v.y), static_cast<lc_ulong>(v.z), static_cast<lc_ulong>(v.w)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_ulong4(lc_uint4 v) noexcept { return lc_ulong4{static_cast<lc_ulong>(v.x), static_cast<lc_ulong>(v.y), static_cast<lc_ulong>(v.z), static_cast<lc_ulong>(v.w)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_ulong4(lc_half4 v) noexcept { return lc_ulong4{static_cast<lc_ulong>(v.x), static_cast<lc_ulong>(v.y), static_cast<lc_ulong>(v.z), static_cast<lc_ulong>(v.w)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_ulong4(lc_float4 v) noexcept { return lc_ulong4{static_cast<lc_ulong>(v.x), static_cast<lc_ulong>(v.y), static_cast<lc_ulong>(v.z), static_cast<lc_ulong>(v.w)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_ulong4(lc_bool4 v) noexcept { return lc_ulong4{static_cast<lc_ulong>(v.x), static_cast<lc_ulong>(v.y), static_cast<lc_ulong>(v.z), static_cast<lc_ulong>(v.w)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_ulong4(lc_long4 v) noexcept { return lc_ulong4{static_cast<lc_ulong>(v.x), static_cast<lc_ulong>(v.y), static_cast<lc_ulong>(v.z), static_cast<lc_ulong>(v.w)}; }
[[nodiscard]] inline __device__ constexpr auto lc_make_ulong4(lc_ulong4 v) noexcept { return lc_ulong4{static_cast<lc_ulong>(v.x), static_cast<lc_ulong>(v.y), static_cast<lc_ulong>(v.z), static_cast<lc_ulong>(v.w)}; }

[[nodiscard]] inline __device__ constexpr auto operator!(lc_byte2 v) noexcept { return lc_make_bool2(!v.x, !v.y); }
[[nodiscard]] inline __device__ constexpr auto operator+(lc_byte2 v) noexcept { return lc_make_byte2(+v.x, +v.y); }
[[nodiscard]] inline __device__ constexpr auto operator-(lc_byte2 v) noexcept { return lc_make_byte2(-v.x, -v.y); }
[[nodiscard]] inline  __device__ constexpr auto operator~(lc_byte2 v) noexcept { return lc_make_byte2(~v.x, ~v.y); }
[[nodiscard]] inline __device__ constexpr auto operator!(lc_byte3 v) noexcept { return lc_make_bool3(!v.x, !v.y, !v.z); }
[[nodiscard]] inline __device__ constexpr auto operator+(lc_byte3 v) noexcept { return lc_make_byte3(+v.x, +v.y, +v.z); }
[[nodiscard]] inline __device__ constexpr auto operator-(lc_byte3 v) noexcept { return lc_make_byte3(-v.x, -v.y, -v.z); }
[[nodiscard]] inline  __device__ constexpr auto operator~(lc_byte3 v) noexcept { return lc_make_byte3(~v.x, ~v.y, ~v.z); }
[[nodiscard]] inline __device__ constexpr auto operator!(lc_byte4 v) noexcept { return lc_make_bool4(!v.x, !v.y, !v.z, !v.w); }
[[nodiscard]] inline __device__ constexpr auto operator+(lc_byte4 v) noexcept { return lc_make_byte4(+v.x, +v.y, +v.z, +v.w); }
[[nodiscard]] inline __device__ constexpr auto operator-(lc_byte4 v) noexcept { return lc_make_byte4(-v.x, -v.y, -v.z, -v.w); }
[[nodiscard]] inline  __device__ constexpr auto operator~(lc_byte4 v) noexcept { return lc_make_byte4(~v.x, ~v.y, ~v.z, ~v.w); }

[[nodiscard]] inline __device__ constexpr auto operator!(lc_ubyte2 v) noexcept { return lc_make_bool2(!v.x, !v.y); }
[[nodiscard]] inline __device__ constexpr auto operator+(lc_ubyte2 v) noexcept { return lc_make_ubyte2(+v.x, +v.y); }
[[nodiscard]] inline __device__ constexpr auto operator-(lc_ubyte2 v) noexcept { return lc_make_ubyte2(-v.x, -v.y); }
[[nodiscard]] inline  __device__ constexpr auto operator~(lc_ubyte2 v) noexcept { return lc_make_ubyte2(~v.x, ~v.y); }
[[nodiscard]] inline __device__ constexpr auto operator!(lc_ubyte3 v) noexcept { return lc_make_bool3(!v.x, !v.y, !v.z); }
[[nodiscard]] inline __device__ constexpr auto operator+(lc_ubyte3 v) noexcept { return lc_make_ubyte3(+v.x, +v.y, +v.z); }
[[nodiscard]] inline __device__ constexpr auto operator-(lc_ubyte3 v) noexcept { return lc_make_ubyte3(-v.x, -v.y, -v.z); }
[[nodiscard]] inline  __device__ constexpr auto operator~(lc_ubyte3 v) noexcept { return lc_make_ubyte3(~v.x, ~v.y, ~v.z); }
[[nodiscard]] inline __device__ constexpr auto operator!(lc_ubyte4 v) noexcept { return lc_make_bool4(!v.x, !v.y, !v.z, !v.w); }
[[nodiscard]] inline __device__ constexpr auto operator+(lc_ubyte4 v) noexcept { return lc_make_ubyte4(+v.x, +v.y, +v.z, +v.w); }
[[nodiscard]] inline __device__ constexpr auto operator-(lc_ubyte4 v) noexcept { return lc_make_ubyte4(-v.x, -v.y, -v.z, -v.w); }
[[nodiscard]] inline  __device__ constexpr auto operator~(lc_ubyte4 v) noexcept { return lc_make_ubyte4(~v.x, ~v.y, ~v.z, ~v.w); }

[[nodiscard]] inline __device__ constexpr auto operator!(lc_short2 v) noexcept { return lc_make_bool2(!v.x, !v.y); }
[[nodiscard]] inline __device__ constexpr auto operator+(lc_short2 v) noexcept { return lc_make_short2(+v.x, +v.y); }
[[nodiscard]] inline __device__ constexpr auto operator-(lc_short2 v) noexcept { return lc_make_short2(-v.x, -v.y); }
[[nodiscard]] inline  __device__ constexpr auto operator~(lc_short2 v) noexcept { return lc_make_short2(~v.x, ~v.y); }
[[nodiscard]] inline __device__ constexpr auto operator!(lc_short3 v) noexcept { return lc_make_bool3(!v.x, !v.y, !v.z); }
[[nodiscard]] inline __device__ constexpr auto operator+(lc_short3 v) noexcept { return lc_make_short3(+v.x, +v.y, +v.z); }
[[nodiscard]] inline __device__ constexpr auto operator-(lc_short3 v) noexcept { return lc_make_short3(-v.x, -v.y, -v.z); }
[[nodiscard]] inline  __device__ constexpr auto operator~(lc_short3 v) noexcept { return lc_make_short3(~v.x, ~v.y, ~v.z); }
[[nodiscard]] inline __device__ constexpr auto operator!(lc_short4 v) noexcept { return lc_make_bool4(!v.x, !v.y, !v.z, !v.w); }
[[nodiscard]] inline __device__ constexpr auto operator+(lc_short4 v) noexcept { return lc_make_short4(+v.x, +v.y, +v.z, +v.w); }
[[nodiscard]] inline __device__ constexpr auto operator-(lc_short4 v) noexcept { return lc_make_short4(-v.x, -v.y, -v.z, -v.w); }
[[nodiscard]] inline  __device__ constexpr auto operator~(lc_short4 v) noexcept { return lc_make_short4(~v.x, ~v.y, ~v.z, ~v.w); }

[[nodiscard]] inline __device__ constexpr auto operator!(lc_ushort2 v) noexcept { return lc_make_bool2(!v.x, !v.y); }
[[nodiscard]] inline __device__ constexpr auto operator+(lc_ushort2 v) noexcept { return lc_make_ushort2(+v.x, +v.y); }
[[nodiscard]] inline __device__ constexpr auto operator-(lc_ushort2 v) noexcept { return lc_make_ushort2(-v.x, -v.y); }
[[nodiscard]] inline  __device__ constexpr auto operator~(lc_ushort2 v) noexcept { return lc_make_ushort2(~v.x, ~v.y); }
[[nodiscard]] inline __device__ constexpr auto operator!(lc_ushort3 v) noexcept { return lc_make_bool3(!v.x, !v.y, !v.z); }
[[nodiscard]] inline __device__ constexpr auto operator+(lc_ushort3 v) noexcept { return lc_make_ushort3(+v.x, +v.y, +v.z); }
[[nodiscard]] inline __device__ constexpr auto operator-(lc_ushort3 v) noexcept { return lc_make_ushort3(-v.x, -v.y, -v.z); }
[[nodiscard]] inline  __device__ constexpr auto operator~(lc_ushort3 v) noexcept { return lc_make_ushort3(~v.x, ~v.y, ~v.z); }
[[nodiscard]] inline __device__ constexpr auto operator!(lc_ushort4 v) noexcept { return lc_make_bool4(!v.x, !v.y, !v.z, !v.w); }
[[nodiscard]] inline __device__ constexpr auto operator+(lc_ushort4 v) noexcept { return lc_make_ushort4(+v.x, +v.y, +v.z, +v.w); }
[[nodiscard]] inline __device__ constexpr auto operator-(lc_ushort4 v) noexcept { return lc_make_ushort4(-v.x, -v.y, -v.z, -v.w); }
[[nodiscard]] inline  __device__ constexpr auto operator~(lc_ushort4 v) noexcept { return lc_make_ushort4(~v.x, ~v.y, ~v.z, ~v.w); }

[[nodiscard]] inline __device__ constexpr auto operator!(lc_int2 v) noexcept { return lc_make_bool2(!v.x, !v.y); }
[[nodiscard]] inline __device__ constexpr auto operator+(lc_int2 v) noexcept { return lc_make_int2(+v.x, +v.y); }
[[nodiscard]] inline __device__ constexpr auto operator-(lc_int2 v) noexcept { return lc_make_int2(-v.x, -v.y); }
[[nodiscard]] inline  __device__ constexpr auto operator~(lc_int2 v) noexcept { return lc_make_int2(~v.x, ~v.y); }
[[nodiscard]] inline __device__ constexpr auto operator!(lc_int3 v) noexcept { return lc_make_bool3(!v.x, !v.y, !v.z); }
[[nodiscard]] inline __device__ constexpr auto operator+(lc_int3 v) noexcept { return lc_make_int3(+v.x, +v.y, +v.z); }
[[nodiscard]] inline __device__ constexpr auto operator-(lc_int3 v) noexcept { return lc_make_int3(-v.x, -v.y, -v.z); }
[[nodiscard]] inline  __device__ constexpr auto operator~(lc_int3 v) noexcept { return lc_make_int3(~v.x, ~v.y, ~v.z); }
[[nodiscard]] inline __device__ constexpr auto operator!(lc_int4 v) noexcept { return lc_make_bool4(!v.x, !v.y, !v.z, !v.w); }
[[nodiscard]] inline __device__ constexpr auto operator+(lc_int4 v) noexcept { return lc_make_int4(+v.x, +v.y, +v.z, +v.w); }
[[nodiscard]] inline __device__ constexpr auto operator-(lc_int4 v) noexcept { return lc_make_int4(-v.x, -v.y, -v.z, -v.w); }
[[nodiscard]] inline  __device__ constexpr auto operator~(lc_int4 v) noexcept { return lc_make_int4(~v.x, ~v.y, ~v.z, ~v.w); }

[[nodiscard]] inline __device__ constexpr auto operator!(lc_uint2 v) noexcept { return lc_make_bool2(!v.x, !v.y); }
[[nodiscard]] inline __device__ constexpr auto operator+(lc_uint2 v) noexcept { return lc_make_uint2(+v.x, +v.y); }
[[nodiscard]] inline __device__ constexpr auto operator-(lc_uint2 v) noexcept { return lc_make_uint2(-v.x, -v.y); }
[[nodiscard]] inline  __device__ constexpr auto operator~(lc_uint2 v) noexcept { return lc_make_uint2(~v.x, ~v.y); }
[[nodiscard]] inline __device__ constexpr auto operator!(lc_uint3 v) noexcept { return lc_make_bool3(!v.x, !v.y, !v.z); }
[[nodiscard]] inline __device__ constexpr auto operator+(lc_uint3 v) noexcept { return lc_make_uint3(+v.x, +v.y, +v.z); }
[[nodiscard]] inline __device__ constexpr auto operator-(lc_uint3 v) noexcept { return lc_make_uint3(-v.x, -v.y, -v.z); }
[[nodiscard]] inline  __device__ constexpr auto operator~(lc_uint3 v) noexcept { return lc_make_uint3(~v.x, ~v.y, ~v.z); }
[[nodiscard]] inline __device__ constexpr auto operator!(lc_uint4 v) noexcept { return lc_make_bool4(!v.x, !v.y, !v.z, !v.w); }
[[nodiscard]] inline __device__ constexpr auto operator+(lc_uint4 v) noexcept { return lc_make_uint4(+v.x, +v.y, +v.z, +v.w); }
[[nodiscard]] inline __device__ constexpr auto operator-(lc_uint4 v) noexcept { return lc_make_uint4(-v.x, -v.y, -v.z, -v.w); }
[[nodiscard]] inline  __device__ constexpr auto operator~(lc_uint4 v) noexcept { return lc_make_uint4(~v.x, ~v.y, ~v.z, ~v.w); }

[[nodiscard]] inline __device__ constexpr auto operator!(lc_half2 v) noexcept { return lc_make_bool2(!v.x, !v.y); }
[[nodiscard]] inline __device__ constexpr auto operator+(lc_half2 v) noexcept { return lc_make_half2(+v.x, +v.y); }
[[nodiscard]] inline __device__ constexpr auto operator-(lc_half2 v) noexcept { return lc_make_half2(-v.x, -v.y); }
[[nodiscard]] inline __device__ constexpr auto operator!(lc_half3 v) noexcept { return lc_make_bool3(!v.x, !v.y, !v.z); }
[[nodiscard]] inline __device__ constexpr auto operator+(lc_half3 v) noexcept { return lc_make_half3(+v.x, +v.y, +v.z); }
[[nodiscard]] inline __device__ constexpr auto operator-(lc_half3 v) noexcept { return lc_make_half3(-v.x, -v.y, -v.z); }
[[nodiscard]] inline __device__ constexpr auto operator!(lc_half4 v) noexcept { return lc_make_bool4(!v.x, !v.y, !v.z, !v.w); }
[[nodiscard]] inline __device__ constexpr auto operator+(lc_half4 v) noexcept { return lc_make_half4(+v.x, +v.y, +v.z, +v.w); }
[[nodiscard]] inline __device__ constexpr auto operator-(lc_half4 v) noexcept { return lc_make_half4(-v.x, -v.y, -v.z, -v.w); }

[[nodiscard]] inline __device__ constexpr auto operator!(lc_float2 v) noexcept { return lc_make_bool2(!v.x, !v.y); }
[[nodiscard]] inline __device__ constexpr auto operator+(lc_float2 v) noexcept { return lc_make_float2(+v.x, +v.y); }
[[nodiscard]] inline __device__ constexpr auto operator-(lc_float2 v) noexcept { return lc_make_float2(-v.x, -v.y); }
[[nodiscard]] inline __device__ constexpr auto operator!(lc_float3 v) noexcept { return lc_make_bool3(!v.x, !v.y, !v.z); }
[[nodiscard]] inline __device__ constexpr auto operator+(lc_float3 v) noexcept { return lc_make_float3(+v.x, +v.y, +v.z); }
[[nodiscard]] inline __device__ constexpr auto operator-(lc_float3 v) noexcept { return lc_make_float3(-v.x, -v.y, -v.z); }
[[nodiscard]] inline __device__ constexpr auto operator!(lc_float4 v) noexcept { return lc_make_bool4(!v.x, !v.y, !v.z, !v.w); }
[[nodiscard]] inline __device__ constexpr auto operator+(lc_float4 v) noexcept { return lc_make_float4(+v.x, +v.y, +v.z, +v.w); }
[[nodiscard]] inline __device__ constexpr auto operator-(lc_float4 v) noexcept { return lc_make_float4(-v.x, -v.y, -v.z, -v.w); }

[[nodiscard]] inline __device__ constexpr auto operator!(lc_bool2 v) noexcept { return lc_make_bool2(!v.x, !v.y); }
[[nodiscard]] inline __device__ constexpr auto operator!(lc_bool3 v) noexcept { return lc_make_bool3(!v.x, !v.y, !v.z); }
[[nodiscard]] inline __device__ constexpr auto operator!(lc_bool4 v) noexcept { return lc_make_bool4(!v.x, !v.y, !v.z, !v.w); }

[[nodiscard]] inline __device__ constexpr auto operator!(lc_long2 v) noexcept { return lc_make_bool2(!v.x, !v.y); }
[[nodiscard]] inline __device__ constexpr auto operator+(lc_long2 v) noexcept { return lc_make_long2(+v.x, +v.y); }
[[nodiscard]] inline __device__ constexpr auto operator-(lc_long2 v) noexcept { return lc_make_long2(-v.x, -v.y); }
[[nodiscard]] inline  __device__ constexpr auto operator~(lc_long2 v) noexcept { return lc_make_long2(~v.x, ~v.y); }
[[nodiscard]] inline __device__ constexpr auto operator!(lc_long3 v) noexcept { return lc_make_bool3(!v.x, !v.y, !v.z); }
[[nodiscard]] inline __device__ constexpr auto operator+(lc_long3 v) noexcept { return lc_make_long3(+v.x, +v.y, +v.z); }
[[nodiscard]] inline __device__ constexpr auto operator-(lc_long3 v) noexcept { return lc_make_long3(-v.x, -v.y, -v.z); }
[[nodiscard]] inline  __device__ constexpr auto operator~(lc_long3 v) noexcept { return lc_make_long3(~v.x, ~v.y, ~v.z); }
[[nodiscard]] inline __device__ constexpr auto operator!(lc_long4 v) noexcept { return lc_make_bool4(!v.x, !v.y, !v.z, !v.w); }
[[nodiscard]] inline __device__ constexpr auto operator+(lc_long4 v) noexcept { return lc_make_long4(+v.x, +v.y, +v.z, +v.w); }
[[nodiscard]] inline __device__ constexpr auto operator-(lc_long4 v) noexcept { return lc_make_long4(-v.x, -v.y, -v.z, -v.w); }
[[nodiscard]] inline  __device__ constexpr auto operator~(lc_long4 v) noexcept { return lc_make_long4(~v.x, ~v.y, ~v.z, ~v.w); }

[[nodiscard]] inline __device__ constexpr auto operator!(lc_ulong2 v) noexcept { return lc_make_bool2(!v.x, !v.y); }
[[nodiscard]] inline __device__ constexpr auto operator+(lc_ulong2 v) noexcept { return lc_make_ulong2(+v.x, +v.y); }
[[nodiscard]] inline __device__ constexpr auto operator-(lc_ulong2 v) noexcept { return lc_make_ulong2(-v.x, -v.y); }
[[nodiscard]] inline  __device__ constexpr auto operator~(lc_ulong2 v) noexcept { return lc_make_ulong2(~v.x, ~v.y); }
[[nodiscard]] inline __device__ constexpr auto operator!(lc_ulong3 v) noexcept { return lc_make_bool3(!v.x, !v.y, !v.z); }
[[nodiscard]] inline __device__ constexpr auto operator+(lc_ulong3 v) noexcept { return lc_make_ulong3(+v.x, +v.y, +v.z); }
[[nodiscard]] inline __device__ constexpr auto operator-(lc_ulong3 v) noexcept { return lc_make_ulong3(-v.x, -v.y, -v.z); }
[[nodiscard]] inline  __device__ constexpr auto operator~(lc_ulong3 v) noexcept { return lc_make_ulong3(~v.x, ~v.y, ~v.z); }
[[nodiscard]] inline __device__ constexpr auto operator!(lc_ulong4 v) noexcept { return lc_make_bool4(!v.x, !v.y, !v.z, !v.w); }
[[nodiscard]] inline __device__ constexpr auto operator+(lc_ulong4 v) noexcept { return lc_make_ulong4(+v.x, +v.y, +v.z, +v.w); }
[[nodiscard]] inline __device__ constexpr auto operator-(lc_ulong4 v) noexcept { return lc_make_ulong4(-v.x, -v.y, -v.z, -v.w); }
[[nodiscard]] inline  __device__ constexpr auto operator~(lc_ulong4 v) noexcept { return lc_make_ulong4(~v.x, ~v.y, ~v.z, ~v.w); }

[[nodiscard]] inline __device__ constexpr auto operator==(lc_byte2 lhs, lc_byte2 rhs) noexcept { return lc_make_bool2(lhs.x == rhs.x, lhs.y == rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator==(lc_byte2 lhs, lc_byte rhs) noexcept { return lc_make_bool2(lhs.x == rhs, lhs.y == rhs); }
[[nodiscard]] inline __device__ constexpr auto operator==(lc_byte lhs, lc_byte2 rhs) noexcept { return lc_make_bool2(lhs == rhs.x, lhs == rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator==(lc_byte3 lhs, lc_byte3 rhs) noexcept { return lc_make_bool3(lhs.x == rhs.x, lhs.y == rhs.y, lhs.z == rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator==(lc_byte3 lhs, lc_byte rhs) noexcept { return lc_make_bool3(lhs.x == rhs, lhs.y == rhs, lhs.z == rhs); }
[[nodiscard]] inline __device__ constexpr auto operator==(lc_byte lhs, lc_byte3 rhs) noexcept { return lc_make_bool3(lhs == rhs.x, lhs == rhs.y, lhs == rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator==(lc_byte4 lhs, lc_byte4 rhs) noexcept { return lc_make_bool4(lhs.x == rhs.x, lhs.y == rhs.y, lhs.z == rhs.z, lhs.w == rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator==(lc_byte4 lhs, lc_byte rhs) noexcept { return lc_make_bool4(lhs.x == rhs, lhs.y == rhs, lhs.z == rhs, lhs.w == rhs); }
[[nodiscard]] inline __device__ constexpr auto operator==(lc_byte lhs, lc_byte4 rhs) noexcept { return lc_make_bool4(lhs == rhs.x, lhs == rhs.y, lhs == rhs.z, lhs == rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator==(lc_ubyte2 lhs, lc_ubyte2 rhs) noexcept { return lc_make_bool2(lhs.x == rhs.x, lhs.y == rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator==(lc_ubyte2 lhs, lc_ubyte rhs) noexcept { return lc_make_bool2(lhs.x == rhs, lhs.y == rhs); }
[[nodiscard]] inline __device__ constexpr auto operator==(lc_ubyte lhs, lc_ubyte2 rhs) noexcept { return lc_make_bool2(lhs == rhs.x, lhs == rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator==(lc_ubyte3 lhs, lc_ubyte3 rhs) noexcept { return lc_make_bool3(lhs.x == rhs.x, lhs.y == rhs.y, lhs.z == rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator==(lc_ubyte3 lhs, lc_ubyte rhs) noexcept { return lc_make_bool3(lhs.x == rhs, lhs.y == rhs, lhs.z == rhs); }
[[nodiscard]] inline __device__ constexpr auto operator==(lc_ubyte lhs, lc_ubyte3 rhs) noexcept { return lc_make_bool3(lhs == rhs.x, lhs == rhs.y, lhs == rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator==(lc_ubyte4 lhs, lc_ubyte4 rhs) noexcept { return lc_make_bool4(lhs.x == rhs.x, lhs.y == rhs.y, lhs.z == rhs.z, lhs.w == rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator==(lc_ubyte4 lhs, lc_ubyte rhs) noexcept { return lc_make_bool4(lhs.x == rhs, lhs.y == rhs, lhs.z == rhs, lhs.w == rhs); }
[[nodiscard]] inline __device__ constexpr auto operator==(lc_ubyte lhs, lc_ubyte4 rhs) noexcept { return lc_make_bool4(lhs == rhs.x, lhs == rhs.y, lhs == rhs.z, lhs == rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator==(lc_short2 lhs, lc_short2 rhs) noexcept { return lc_make_bool2(lhs.x == rhs.x, lhs.y == rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator==(lc_short2 lhs, lc_short rhs) noexcept { return lc_make_bool2(lhs.x == rhs, lhs.y == rhs); }
[[nodiscard]] inline __device__ constexpr auto operator==(lc_short lhs, lc_short2 rhs) noexcept { return lc_make_bool2(lhs == rhs.x, lhs == rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator==(lc_short3 lhs, lc_short3 rhs) noexcept { return lc_make_bool3(lhs.x == rhs.x, lhs.y == rhs.y, lhs.z == rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator==(lc_short3 lhs, lc_short rhs) noexcept { return lc_make_bool3(lhs.x == rhs, lhs.y == rhs, lhs.z == rhs); }
[[nodiscard]] inline __device__ constexpr auto operator==(lc_short lhs, lc_short3 rhs) noexcept { return lc_make_bool3(lhs == rhs.x, lhs == rhs.y, lhs == rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator==(lc_short4 lhs, lc_short4 rhs) noexcept { return lc_make_bool4(lhs.x == rhs.x, lhs.y == rhs.y, lhs.z == rhs.z, lhs.w == rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator==(lc_short4 lhs, lc_short rhs) noexcept { return lc_make_bool4(lhs.x == rhs, lhs.y == rhs, lhs.z == rhs, lhs.w == rhs); }
[[nodiscard]] inline __device__ constexpr auto operator==(lc_short lhs, lc_short4 rhs) noexcept { return lc_make_bool4(lhs == rhs.x, lhs == rhs.y, lhs == rhs.z, lhs == rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator==(lc_ushort2 lhs, lc_ushort2 rhs) noexcept { return lc_make_bool2(lhs.x == rhs.x, lhs.y == rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator==(lc_ushort2 lhs, lc_ushort rhs) noexcept { return lc_make_bool2(lhs.x == rhs, lhs.y == rhs); }
[[nodiscard]] inline __device__ constexpr auto operator==(lc_ushort lhs, lc_ushort2 rhs) noexcept { return lc_make_bool2(lhs == rhs.x, lhs == rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator==(lc_ushort3 lhs, lc_ushort3 rhs) noexcept { return lc_make_bool3(lhs.x == rhs.x, lhs.y == rhs.y, lhs.z == rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator==(lc_ushort3 lhs, lc_ushort rhs) noexcept { return lc_make_bool3(lhs.x == rhs, lhs.y == rhs, lhs.z == rhs); }
[[nodiscard]] inline __device__ constexpr auto operator==(lc_ushort lhs, lc_ushort3 rhs) noexcept { return lc_make_bool3(lhs == rhs.x, lhs == rhs.y, lhs == rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator==(lc_ushort4 lhs, lc_ushort4 rhs) noexcept { return lc_make_bool4(lhs.x == rhs.x, lhs.y == rhs.y, lhs.z == rhs.z, lhs.w == rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator==(lc_ushort4 lhs, lc_ushort rhs) noexcept { return lc_make_bool4(lhs.x == rhs, lhs.y == rhs, lhs.z == rhs, lhs.w == rhs); }
[[nodiscard]] inline __device__ constexpr auto operator==(lc_ushort lhs, lc_ushort4 rhs) noexcept { return lc_make_bool4(lhs == rhs.x, lhs == rhs.y, lhs == rhs.z, lhs == rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator==(lc_int2 lhs, lc_int2 rhs) noexcept { return lc_make_bool2(lhs.x == rhs.x, lhs.y == rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator==(lc_int2 lhs, lc_int rhs) noexcept { return lc_make_bool2(lhs.x == rhs, lhs.y == rhs); }
[[nodiscard]] inline __device__ constexpr auto operator==(lc_int lhs, lc_int2 rhs) noexcept { return lc_make_bool2(lhs == rhs.x, lhs == rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator==(lc_int3 lhs, lc_int3 rhs) noexcept { return lc_make_bool3(lhs.x == rhs.x, lhs.y == rhs.y, lhs.z == rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator==(lc_int3 lhs, lc_int rhs) noexcept { return lc_make_bool3(lhs.x == rhs, lhs.y == rhs, lhs.z == rhs); }
[[nodiscard]] inline __device__ constexpr auto operator==(lc_int lhs, lc_int3 rhs) noexcept { return lc_make_bool3(lhs == rhs.x, lhs == rhs.y, lhs == rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator==(lc_int4 lhs, lc_int4 rhs) noexcept { return lc_make_bool4(lhs.x == rhs.x, lhs.y == rhs.y, lhs.z == rhs.z, lhs.w == rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator==(lc_int4 lhs, lc_int rhs) noexcept { return lc_make_bool4(lhs.x == rhs, lhs.y == rhs, lhs.z == rhs, lhs.w == rhs); }
[[nodiscard]] inline __device__ constexpr auto operator==(lc_int lhs, lc_int4 rhs) noexcept { return lc_make_bool4(lhs == rhs.x, lhs == rhs.y, lhs == rhs.z, lhs == rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator==(lc_uint2 lhs, lc_uint2 rhs) noexcept { return lc_make_bool2(lhs.x == rhs.x, lhs.y == rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator==(lc_uint2 lhs, lc_uint rhs) noexcept { return lc_make_bool2(lhs.x == rhs, lhs.y == rhs); }
[[nodiscard]] inline __device__ constexpr auto operator==(lc_uint lhs, lc_uint2 rhs) noexcept { return lc_make_bool2(lhs == rhs.x, lhs == rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator==(lc_uint3 lhs, lc_uint3 rhs) noexcept { return lc_make_bool3(lhs.x == rhs.x, lhs.y == rhs.y, lhs.z == rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator==(lc_uint3 lhs, lc_uint rhs) noexcept { return lc_make_bool3(lhs.x == rhs, lhs.y == rhs, lhs.z == rhs); }
[[nodiscard]] inline __device__ constexpr auto operator==(lc_uint lhs, lc_uint3 rhs) noexcept { return lc_make_bool3(lhs == rhs.x, lhs == rhs.y, lhs == rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator==(lc_uint4 lhs, lc_uint4 rhs) noexcept { return lc_make_bool4(lhs.x == rhs.x, lhs.y == rhs.y, lhs.z == rhs.z, lhs.w == rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator==(lc_uint4 lhs, lc_uint rhs) noexcept { return lc_make_bool4(lhs.x == rhs, lhs.y == rhs, lhs.z == rhs, lhs.w == rhs); }
[[nodiscard]] inline __device__ constexpr auto operator==(lc_uint lhs, lc_uint4 rhs) noexcept { return lc_make_bool4(lhs == rhs.x, lhs == rhs.y, lhs == rhs.z, lhs == rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator==(lc_half2 lhs, lc_half2 rhs) noexcept { return lc_make_bool2(lhs.x == rhs.x, lhs.y == rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator==(lc_half2 lhs, lc_half rhs) noexcept { return lc_make_bool2(lhs.x == rhs, lhs.y == rhs); }
[[nodiscard]] inline __device__ constexpr auto operator==(lc_half lhs, lc_half2 rhs) noexcept { return lc_make_bool2(lhs == rhs.x, lhs == rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator==(lc_half3 lhs, lc_half3 rhs) noexcept { return lc_make_bool3(lhs.x == rhs.x, lhs.y == rhs.y, lhs.z == rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator==(lc_half3 lhs, lc_half rhs) noexcept { return lc_make_bool3(lhs.x == rhs, lhs.y == rhs, lhs.z == rhs); }
[[nodiscard]] inline __device__ constexpr auto operator==(lc_half lhs, lc_half3 rhs) noexcept { return lc_make_bool3(lhs == rhs.x, lhs == rhs.y, lhs == rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator==(lc_half4 lhs, lc_half4 rhs) noexcept { return lc_make_bool4(lhs.x == rhs.x, lhs.y == rhs.y, lhs.z == rhs.z, lhs.w == rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator==(lc_half4 lhs, lc_half rhs) noexcept { return lc_make_bool4(lhs.x == rhs, lhs.y == rhs, lhs.z == rhs, lhs.w == rhs); }
[[nodiscard]] inline __device__ constexpr auto operator==(lc_half lhs, lc_half4 rhs) noexcept { return lc_make_bool4(lhs == rhs.x, lhs == rhs.y, lhs == rhs.z, lhs == rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator==(lc_float2 lhs, lc_float2 rhs) noexcept { return lc_make_bool2(lhs.x == rhs.x, lhs.y == rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator==(lc_float2 lhs, lc_float rhs) noexcept { return lc_make_bool2(lhs.x == rhs, lhs.y == rhs); }
[[nodiscard]] inline __device__ constexpr auto operator==(lc_float lhs, lc_float2 rhs) noexcept { return lc_make_bool2(lhs == rhs.x, lhs == rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator==(lc_float3 lhs, lc_float3 rhs) noexcept { return lc_make_bool3(lhs.x == rhs.x, lhs.y == rhs.y, lhs.z == rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator==(lc_float3 lhs, lc_float rhs) noexcept { return lc_make_bool3(lhs.x == rhs, lhs.y == rhs, lhs.z == rhs); }
[[nodiscard]] inline __device__ constexpr auto operator==(lc_float lhs, lc_float3 rhs) noexcept { return lc_make_bool3(lhs == rhs.x, lhs == rhs.y, lhs == rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator==(lc_float4 lhs, lc_float4 rhs) noexcept { return lc_make_bool4(lhs.x == rhs.x, lhs.y == rhs.y, lhs.z == rhs.z, lhs.w == rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator==(lc_float4 lhs, lc_float rhs) noexcept { return lc_make_bool4(lhs.x == rhs, lhs.y == rhs, lhs.z == rhs, lhs.w == rhs); }
[[nodiscard]] inline __device__ constexpr auto operator==(lc_float lhs, lc_float4 rhs) noexcept { return lc_make_bool4(lhs == rhs.x, lhs == rhs.y, lhs == rhs.z, lhs == rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator==(lc_bool2 lhs, lc_bool2 rhs) noexcept { return lc_make_bool2(lhs.x == rhs.x, lhs.y == rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator==(lc_bool2 lhs, lc_bool rhs) noexcept { return lc_make_bool2(lhs.x == rhs, lhs.y == rhs); }
[[nodiscard]] inline __device__ constexpr auto operator==(lc_bool lhs, lc_bool2 rhs) noexcept { return lc_make_bool2(lhs == rhs.x, lhs == rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator==(lc_bool3 lhs, lc_bool3 rhs) noexcept { return lc_make_bool3(lhs.x == rhs.x, lhs.y == rhs.y, lhs.z == rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator==(lc_bool3 lhs, lc_bool rhs) noexcept { return lc_make_bool3(lhs.x == rhs, lhs.y == rhs, lhs.z == rhs); }
[[nodiscard]] inline __device__ constexpr auto operator==(lc_bool lhs, lc_bool3 rhs) noexcept { return lc_make_bool3(lhs == rhs.x, lhs == rhs.y, lhs == rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator==(lc_bool4 lhs, lc_bool4 rhs) noexcept { return lc_make_bool4(lhs.x == rhs.x, lhs.y == rhs.y, lhs.z == rhs.z, lhs.w == rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator==(lc_bool4 lhs, lc_bool rhs) noexcept { return lc_make_bool4(lhs.x == rhs, lhs.y == rhs, lhs.z == rhs, lhs.w == rhs); }
[[nodiscard]] inline __device__ constexpr auto operator==(lc_bool lhs, lc_bool4 rhs) noexcept { return lc_make_bool4(lhs == rhs.x, lhs == rhs.y, lhs == rhs.z, lhs == rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator==(lc_long2 lhs, lc_long2 rhs) noexcept { return lc_make_bool2(lhs.x == rhs.x, lhs.y == rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator==(lc_long2 lhs, lc_long rhs) noexcept { return lc_make_bool2(lhs.x == rhs, lhs.y == rhs); }
[[nodiscard]] inline __device__ constexpr auto operator==(lc_long lhs, lc_long2 rhs) noexcept { return lc_make_bool2(lhs == rhs.x, lhs == rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator==(lc_long3 lhs, lc_long3 rhs) noexcept { return lc_make_bool3(lhs.x == rhs.x, lhs.y == rhs.y, lhs.z == rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator==(lc_long3 lhs, lc_long rhs) noexcept { return lc_make_bool3(lhs.x == rhs, lhs.y == rhs, lhs.z == rhs); }
[[nodiscard]] inline __device__ constexpr auto operator==(lc_long lhs, lc_long3 rhs) noexcept { return lc_make_bool3(lhs == rhs.x, lhs == rhs.y, lhs == rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator==(lc_long4 lhs, lc_long4 rhs) noexcept { return lc_make_bool4(lhs.x == rhs.x, lhs.y == rhs.y, lhs.z == rhs.z, lhs.w == rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator==(lc_long4 lhs, lc_long rhs) noexcept { return lc_make_bool4(lhs.x == rhs, lhs.y == rhs, lhs.z == rhs, lhs.w == rhs); }
[[nodiscard]] inline __device__ constexpr auto operator==(lc_long lhs, lc_long4 rhs) noexcept { return lc_make_bool4(lhs == rhs.x, lhs == rhs.y, lhs == rhs.z, lhs == rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator==(lc_ulong2 lhs, lc_ulong2 rhs) noexcept { return lc_make_bool2(lhs.x == rhs.x, lhs.y == rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator==(lc_ulong2 lhs, lc_ulong rhs) noexcept { return lc_make_bool2(lhs.x == rhs, lhs.y == rhs); }
[[nodiscard]] inline __device__ constexpr auto operator==(lc_ulong lhs, lc_ulong2 rhs) noexcept { return lc_make_bool2(lhs == rhs.x, lhs == rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator==(lc_ulong3 lhs, lc_ulong3 rhs) noexcept { return lc_make_bool3(lhs.x == rhs.x, lhs.y == rhs.y, lhs.z == rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator==(lc_ulong3 lhs, lc_ulong rhs) noexcept { return lc_make_bool3(lhs.x == rhs, lhs.y == rhs, lhs.z == rhs); }
[[nodiscard]] inline __device__ constexpr auto operator==(lc_ulong lhs, lc_ulong3 rhs) noexcept { return lc_make_bool3(lhs == rhs.x, lhs == rhs.y, lhs == rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator==(lc_ulong4 lhs, lc_ulong4 rhs) noexcept { return lc_make_bool4(lhs.x == rhs.x, lhs.y == rhs.y, lhs.z == rhs.z, lhs.w == rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator==(lc_ulong4 lhs, lc_ulong rhs) noexcept { return lc_make_bool4(lhs.x == rhs, lhs.y == rhs, lhs.z == rhs, lhs.w == rhs); }
[[nodiscard]] inline __device__ constexpr auto operator==(lc_ulong lhs, lc_ulong4 rhs) noexcept { return lc_make_bool4(lhs == rhs.x, lhs == rhs.y, lhs == rhs.z, lhs == rhs.w); }

[[nodiscard]] inline __device__ constexpr auto operator!=(lc_byte2 lhs, lc_byte2 rhs) noexcept { return lc_make_bool2(lhs.x != rhs.x, lhs.y != rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator!=(lc_byte2 lhs, lc_byte rhs) noexcept { return lc_make_bool2(lhs.x != rhs, lhs.y != rhs); }
[[nodiscard]] inline __device__ constexpr auto operator!=(lc_byte lhs, lc_byte2 rhs) noexcept { return lc_make_bool2(lhs != rhs.x, lhs != rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator!=(lc_byte3 lhs, lc_byte3 rhs) noexcept { return lc_make_bool3(lhs.x != rhs.x, lhs.y != rhs.y, lhs.z != rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator!=(lc_byte3 lhs, lc_byte rhs) noexcept { return lc_make_bool3(lhs.x != rhs, lhs.y != rhs, lhs.z != rhs); }
[[nodiscard]] inline __device__ constexpr auto operator!=(lc_byte lhs, lc_byte3 rhs) noexcept { return lc_make_bool3(lhs != rhs.x, lhs != rhs.y, lhs != rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator!=(lc_byte4 lhs, lc_byte4 rhs) noexcept { return lc_make_bool4(lhs.x != rhs.x, lhs.y != rhs.y, lhs.z != rhs.z, lhs.w != rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator!=(lc_byte4 lhs, lc_byte rhs) noexcept { return lc_make_bool4(lhs.x != rhs, lhs.y != rhs, lhs.z != rhs, lhs.w != rhs); }
[[nodiscard]] inline __device__ constexpr auto operator!=(lc_byte lhs, lc_byte4 rhs) noexcept { return lc_make_bool4(lhs != rhs.x, lhs != rhs.y, lhs != rhs.z, lhs != rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator!=(lc_ubyte2 lhs, lc_ubyte2 rhs) noexcept { return lc_make_bool2(lhs.x != rhs.x, lhs.y != rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator!=(lc_ubyte2 lhs, lc_ubyte rhs) noexcept { return lc_make_bool2(lhs.x != rhs, lhs.y != rhs); }
[[nodiscard]] inline __device__ constexpr auto operator!=(lc_ubyte lhs, lc_ubyte2 rhs) noexcept { return lc_make_bool2(lhs != rhs.x, lhs != rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator!=(lc_ubyte3 lhs, lc_ubyte3 rhs) noexcept { return lc_make_bool3(lhs.x != rhs.x, lhs.y != rhs.y, lhs.z != rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator!=(lc_ubyte3 lhs, lc_ubyte rhs) noexcept { return lc_make_bool3(lhs.x != rhs, lhs.y != rhs, lhs.z != rhs); }
[[nodiscard]] inline __device__ constexpr auto operator!=(lc_ubyte lhs, lc_ubyte3 rhs) noexcept { return lc_make_bool3(lhs != rhs.x, lhs != rhs.y, lhs != rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator!=(lc_ubyte4 lhs, lc_ubyte4 rhs) noexcept { return lc_make_bool4(lhs.x != rhs.x, lhs.y != rhs.y, lhs.z != rhs.z, lhs.w != rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator!=(lc_ubyte4 lhs, lc_ubyte rhs) noexcept { return lc_make_bool4(lhs.x != rhs, lhs.y != rhs, lhs.z != rhs, lhs.w != rhs); }
[[nodiscard]] inline __device__ constexpr auto operator!=(lc_ubyte lhs, lc_ubyte4 rhs) noexcept { return lc_make_bool4(lhs != rhs.x, lhs != rhs.y, lhs != rhs.z, lhs != rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator!=(lc_short2 lhs, lc_short2 rhs) noexcept { return lc_make_bool2(lhs.x != rhs.x, lhs.y != rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator!=(lc_short2 lhs, lc_short rhs) noexcept { return lc_make_bool2(lhs.x != rhs, lhs.y != rhs); }
[[nodiscard]] inline __device__ constexpr auto operator!=(lc_short lhs, lc_short2 rhs) noexcept { return lc_make_bool2(lhs != rhs.x, lhs != rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator!=(lc_short3 lhs, lc_short3 rhs) noexcept { return lc_make_bool3(lhs.x != rhs.x, lhs.y != rhs.y, lhs.z != rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator!=(lc_short3 lhs, lc_short rhs) noexcept { return lc_make_bool3(lhs.x != rhs, lhs.y != rhs, lhs.z != rhs); }
[[nodiscard]] inline __device__ constexpr auto operator!=(lc_short lhs, lc_short3 rhs) noexcept { return lc_make_bool3(lhs != rhs.x, lhs != rhs.y, lhs != rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator!=(lc_short4 lhs, lc_short4 rhs) noexcept { return lc_make_bool4(lhs.x != rhs.x, lhs.y != rhs.y, lhs.z != rhs.z, lhs.w != rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator!=(lc_short4 lhs, lc_short rhs) noexcept { return lc_make_bool4(lhs.x != rhs, lhs.y != rhs, lhs.z != rhs, lhs.w != rhs); }
[[nodiscard]] inline __device__ constexpr auto operator!=(lc_short lhs, lc_short4 rhs) noexcept { return lc_make_bool4(lhs != rhs.x, lhs != rhs.y, lhs != rhs.z, lhs != rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator!=(lc_ushort2 lhs, lc_ushort2 rhs) noexcept { return lc_make_bool2(lhs.x != rhs.x, lhs.y != rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator!=(lc_ushort2 lhs, lc_ushort rhs) noexcept { return lc_make_bool2(lhs.x != rhs, lhs.y != rhs); }
[[nodiscard]] inline __device__ constexpr auto operator!=(lc_ushort lhs, lc_ushort2 rhs) noexcept { return lc_make_bool2(lhs != rhs.x, lhs != rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator!=(lc_ushort3 lhs, lc_ushort3 rhs) noexcept { return lc_make_bool3(lhs.x != rhs.x, lhs.y != rhs.y, lhs.z != rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator!=(lc_ushort3 lhs, lc_ushort rhs) noexcept { return lc_make_bool3(lhs.x != rhs, lhs.y != rhs, lhs.z != rhs); }
[[nodiscard]] inline __device__ constexpr auto operator!=(lc_ushort lhs, lc_ushort3 rhs) noexcept { return lc_make_bool3(lhs != rhs.x, lhs != rhs.y, lhs != rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator!=(lc_ushort4 lhs, lc_ushort4 rhs) noexcept { return lc_make_bool4(lhs.x != rhs.x, lhs.y != rhs.y, lhs.z != rhs.z, lhs.w != rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator!=(lc_ushort4 lhs, lc_ushort rhs) noexcept { return lc_make_bool4(lhs.x != rhs, lhs.y != rhs, lhs.z != rhs, lhs.w != rhs); }
[[nodiscard]] inline __device__ constexpr auto operator!=(lc_ushort lhs, lc_ushort4 rhs) noexcept { return lc_make_bool4(lhs != rhs.x, lhs != rhs.y, lhs != rhs.z, lhs != rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator!=(lc_int2 lhs, lc_int2 rhs) noexcept { return lc_make_bool2(lhs.x != rhs.x, lhs.y != rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator!=(lc_int2 lhs, lc_int rhs) noexcept { return lc_make_bool2(lhs.x != rhs, lhs.y != rhs); }
[[nodiscard]] inline __device__ constexpr auto operator!=(lc_int lhs, lc_int2 rhs) noexcept { return lc_make_bool2(lhs != rhs.x, lhs != rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator!=(lc_int3 lhs, lc_int3 rhs) noexcept { return lc_make_bool3(lhs.x != rhs.x, lhs.y != rhs.y, lhs.z != rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator!=(lc_int3 lhs, lc_int rhs) noexcept { return lc_make_bool3(lhs.x != rhs, lhs.y != rhs, lhs.z != rhs); }
[[nodiscard]] inline __device__ constexpr auto operator!=(lc_int lhs, lc_int3 rhs) noexcept { return lc_make_bool3(lhs != rhs.x, lhs != rhs.y, lhs != rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator!=(lc_int4 lhs, lc_int4 rhs) noexcept { return lc_make_bool4(lhs.x != rhs.x, lhs.y != rhs.y, lhs.z != rhs.z, lhs.w != rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator!=(lc_int4 lhs, lc_int rhs) noexcept { return lc_make_bool4(lhs.x != rhs, lhs.y != rhs, lhs.z != rhs, lhs.w != rhs); }
[[nodiscard]] inline __device__ constexpr auto operator!=(lc_int lhs, lc_int4 rhs) noexcept { return lc_make_bool4(lhs != rhs.x, lhs != rhs.y, lhs != rhs.z, lhs != rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator!=(lc_uint2 lhs, lc_uint2 rhs) noexcept { return lc_make_bool2(lhs.x != rhs.x, lhs.y != rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator!=(lc_uint2 lhs, lc_uint rhs) noexcept { return lc_make_bool2(lhs.x != rhs, lhs.y != rhs); }
[[nodiscard]] inline __device__ constexpr auto operator!=(lc_uint lhs, lc_uint2 rhs) noexcept { return lc_make_bool2(lhs != rhs.x, lhs != rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator!=(lc_uint3 lhs, lc_uint3 rhs) noexcept { return lc_make_bool3(lhs.x != rhs.x, lhs.y != rhs.y, lhs.z != rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator!=(lc_uint3 lhs, lc_uint rhs) noexcept { return lc_make_bool3(lhs.x != rhs, lhs.y != rhs, lhs.z != rhs); }
[[nodiscard]] inline __device__ constexpr auto operator!=(lc_uint lhs, lc_uint3 rhs) noexcept { return lc_make_bool3(lhs != rhs.x, lhs != rhs.y, lhs != rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator!=(lc_uint4 lhs, lc_uint4 rhs) noexcept { return lc_make_bool4(lhs.x != rhs.x, lhs.y != rhs.y, lhs.z != rhs.z, lhs.w != rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator!=(lc_uint4 lhs, lc_uint rhs) noexcept { return lc_make_bool4(lhs.x != rhs, lhs.y != rhs, lhs.z != rhs, lhs.w != rhs); }
[[nodiscard]] inline __device__ constexpr auto operator!=(lc_uint lhs, lc_uint4 rhs) noexcept { return lc_make_bool4(lhs != rhs.x, lhs != rhs.y, lhs != rhs.z, lhs != rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator!=(lc_half2 lhs, lc_half2 rhs) noexcept { return lc_make_bool2(lhs.x != rhs.x, lhs.y != rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator!=(lc_half2 lhs, lc_half rhs) noexcept { return lc_make_bool2(lhs.x != rhs, lhs.y != rhs); }
[[nodiscard]] inline __device__ constexpr auto operator!=(lc_half lhs, lc_half2 rhs) noexcept { return lc_make_bool2(lhs != rhs.x, lhs != rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator!=(lc_half3 lhs, lc_half3 rhs) noexcept { return lc_make_bool3(lhs.x != rhs.x, lhs.y != rhs.y, lhs.z != rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator!=(lc_half3 lhs, lc_half rhs) noexcept { return lc_make_bool3(lhs.x != rhs, lhs.y != rhs, lhs.z != rhs); }
[[nodiscard]] inline __device__ constexpr auto operator!=(lc_half lhs, lc_half3 rhs) noexcept { return lc_make_bool3(lhs != rhs.x, lhs != rhs.y, lhs != rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator!=(lc_half4 lhs, lc_half4 rhs) noexcept { return lc_make_bool4(lhs.x != rhs.x, lhs.y != rhs.y, lhs.z != rhs.z, lhs.w != rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator!=(lc_half4 lhs, lc_half rhs) noexcept { return lc_make_bool4(lhs.x != rhs, lhs.y != rhs, lhs.z != rhs, lhs.w != rhs); }
[[nodiscard]] inline __device__ constexpr auto operator!=(lc_half lhs, lc_half4 rhs) noexcept { return lc_make_bool4(lhs != rhs.x, lhs != rhs.y, lhs != rhs.z, lhs != rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator!=(lc_float2 lhs, lc_float2 rhs) noexcept { return lc_make_bool2(lhs.x != rhs.x, lhs.y != rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator!=(lc_float2 lhs, lc_float rhs) noexcept { return lc_make_bool2(lhs.x != rhs, lhs.y != rhs); }
[[nodiscard]] inline __device__ constexpr auto operator!=(lc_float lhs, lc_float2 rhs) noexcept { return lc_make_bool2(lhs != rhs.x, lhs != rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator!=(lc_float3 lhs, lc_float3 rhs) noexcept { return lc_make_bool3(lhs.x != rhs.x, lhs.y != rhs.y, lhs.z != rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator!=(lc_float3 lhs, lc_float rhs) noexcept { return lc_make_bool3(lhs.x != rhs, lhs.y != rhs, lhs.z != rhs); }
[[nodiscard]] inline __device__ constexpr auto operator!=(lc_float lhs, lc_float3 rhs) noexcept { return lc_make_bool3(lhs != rhs.x, lhs != rhs.y, lhs != rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator!=(lc_float4 lhs, lc_float4 rhs) noexcept { return lc_make_bool4(lhs.x != rhs.x, lhs.y != rhs.y, lhs.z != rhs.z, lhs.w != rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator!=(lc_float4 lhs, lc_float rhs) noexcept { return lc_make_bool4(lhs.x != rhs, lhs.y != rhs, lhs.z != rhs, lhs.w != rhs); }
[[nodiscard]] inline __device__ constexpr auto operator!=(lc_float lhs, lc_float4 rhs) noexcept { return lc_make_bool4(lhs != rhs.x, lhs != rhs.y, lhs != rhs.z, lhs != rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator!=(lc_bool2 lhs, lc_bool2 rhs) noexcept { return lc_make_bool2(lhs.x != rhs.x, lhs.y != rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator!=(lc_bool2 lhs, lc_bool rhs) noexcept { return lc_make_bool2(lhs.x != rhs, lhs.y != rhs); }
[[nodiscard]] inline __device__ constexpr auto operator!=(lc_bool lhs, lc_bool2 rhs) noexcept { return lc_make_bool2(lhs != rhs.x, lhs != rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator!=(lc_bool3 lhs, lc_bool3 rhs) noexcept { return lc_make_bool3(lhs.x != rhs.x, lhs.y != rhs.y, lhs.z != rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator!=(lc_bool3 lhs, lc_bool rhs) noexcept { return lc_make_bool3(lhs.x != rhs, lhs.y != rhs, lhs.z != rhs); }
[[nodiscard]] inline __device__ constexpr auto operator!=(lc_bool lhs, lc_bool3 rhs) noexcept { return lc_make_bool3(lhs != rhs.x, lhs != rhs.y, lhs != rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator!=(lc_bool4 lhs, lc_bool4 rhs) noexcept { return lc_make_bool4(lhs.x != rhs.x, lhs.y != rhs.y, lhs.z != rhs.z, lhs.w != rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator!=(lc_bool4 lhs, lc_bool rhs) noexcept { return lc_make_bool4(lhs.x != rhs, lhs.y != rhs, lhs.z != rhs, lhs.w != rhs); }
[[nodiscard]] inline __device__ constexpr auto operator!=(lc_bool lhs, lc_bool4 rhs) noexcept { return lc_make_bool4(lhs != rhs.x, lhs != rhs.y, lhs != rhs.z, lhs != rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator!=(lc_long2 lhs, lc_long2 rhs) noexcept { return lc_make_bool2(lhs.x != rhs.x, lhs.y != rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator!=(lc_long2 lhs, lc_long rhs) noexcept { return lc_make_bool2(lhs.x != rhs, lhs.y != rhs); }
[[nodiscard]] inline __device__ constexpr auto operator!=(lc_long lhs, lc_long2 rhs) noexcept { return lc_make_bool2(lhs != rhs.x, lhs != rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator!=(lc_long3 lhs, lc_long3 rhs) noexcept { return lc_make_bool3(lhs.x != rhs.x, lhs.y != rhs.y, lhs.z != rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator!=(lc_long3 lhs, lc_long rhs) noexcept { return lc_make_bool3(lhs.x != rhs, lhs.y != rhs, lhs.z != rhs); }
[[nodiscard]] inline __device__ constexpr auto operator!=(lc_long lhs, lc_long3 rhs) noexcept { return lc_make_bool3(lhs != rhs.x, lhs != rhs.y, lhs != rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator!=(lc_long4 lhs, lc_long4 rhs) noexcept { return lc_make_bool4(lhs.x != rhs.x, lhs.y != rhs.y, lhs.z != rhs.z, lhs.w != rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator!=(lc_long4 lhs, lc_long rhs) noexcept { return lc_make_bool4(lhs.x != rhs, lhs.y != rhs, lhs.z != rhs, lhs.w != rhs); }
[[nodiscard]] inline __device__ constexpr auto operator!=(lc_long lhs, lc_long4 rhs) noexcept { return lc_make_bool4(lhs != rhs.x, lhs != rhs.y, lhs != rhs.z, lhs != rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator!=(lc_ulong2 lhs, lc_ulong2 rhs) noexcept { return lc_make_bool2(lhs.x != rhs.x, lhs.y != rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator!=(lc_ulong2 lhs, lc_ulong rhs) noexcept { return lc_make_bool2(lhs.x != rhs, lhs.y != rhs); }
[[nodiscard]] inline __device__ constexpr auto operator!=(lc_ulong lhs, lc_ulong2 rhs) noexcept { return lc_make_bool2(lhs != rhs.x, lhs != rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator!=(lc_ulong3 lhs, lc_ulong3 rhs) noexcept { return lc_make_bool3(lhs.x != rhs.x, lhs.y != rhs.y, lhs.z != rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator!=(lc_ulong3 lhs, lc_ulong rhs) noexcept { return lc_make_bool3(lhs.x != rhs, lhs.y != rhs, lhs.z != rhs); }
[[nodiscard]] inline __device__ constexpr auto operator!=(lc_ulong lhs, lc_ulong3 rhs) noexcept { return lc_make_bool3(lhs != rhs.x, lhs != rhs.y, lhs != rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator!=(lc_ulong4 lhs, lc_ulong4 rhs) noexcept { return lc_make_bool4(lhs.x != rhs.x, lhs.y != rhs.y, lhs.z != rhs.z, lhs.w != rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator!=(lc_ulong4 lhs, lc_ulong rhs) noexcept { return lc_make_bool4(lhs.x != rhs, lhs.y != rhs, lhs.z != rhs, lhs.w != rhs); }
[[nodiscard]] inline __device__ constexpr auto operator!=(lc_ulong lhs, lc_ulong4 rhs) noexcept { return lc_make_bool4(lhs != rhs.x, lhs != rhs.y, lhs != rhs.z, lhs != rhs.w); }

[[nodiscard]] inline __device__ constexpr auto operator<(lc_short2 lhs, lc_short2 rhs) noexcept { return lc_make_bool2(lhs.x < rhs.x, lhs.y < rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator<(lc_short2 lhs, lc_short rhs) noexcept { return lc_make_bool2(lhs.x < rhs, lhs.y < rhs); }
[[nodiscard]] inline __device__ constexpr auto operator<(lc_short lhs, lc_short2 rhs) noexcept { return lc_make_bool2(lhs < rhs.x, lhs < rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator<(lc_short3 lhs, lc_short3 rhs) noexcept { return lc_make_bool3(lhs.x < rhs.x, lhs.y < rhs.y, lhs.z < rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator<(lc_short3 lhs, lc_short rhs) noexcept { return lc_make_bool3(lhs.x < rhs, lhs.y < rhs, lhs.z < rhs); }
[[nodiscard]] inline __device__ constexpr auto operator<(lc_short lhs, lc_short3 rhs) noexcept { return lc_make_bool3(lhs < rhs.x, lhs < rhs.y, lhs < rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator<(lc_short4 lhs, lc_short4 rhs) noexcept { return lc_make_bool4(lhs.x < rhs.x, lhs.y < rhs.y, lhs.z < rhs.z, lhs.w < rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator<(lc_short4 lhs, lc_short rhs) noexcept { return lc_make_bool4(lhs.x < rhs, lhs.y < rhs, lhs.z < rhs, lhs.w < rhs); }
[[nodiscard]] inline __device__ constexpr auto operator<(lc_short lhs, lc_short4 rhs) noexcept { return lc_make_bool4(lhs < rhs.x, lhs < rhs.y, lhs < rhs.z, lhs < rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator<(lc_ushort2 lhs, lc_ushort2 rhs) noexcept { return lc_make_bool2(lhs.x < rhs.x, lhs.y < rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator<(lc_ushort2 lhs, lc_ushort rhs) noexcept { return lc_make_bool2(lhs.x < rhs, lhs.y < rhs); }
[[nodiscard]] inline __device__ constexpr auto operator<(lc_ushort lhs, lc_ushort2 rhs) noexcept { return lc_make_bool2(lhs < rhs.x, lhs < rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator<(lc_ushort3 lhs, lc_ushort3 rhs) noexcept { return lc_make_bool3(lhs.x < rhs.x, lhs.y < rhs.y, lhs.z < rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator<(lc_ushort3 lhs, lc_ushort rhs) noexcept { return lc_make_bool3(lhs.x < rhs, lhs.y < rhs, lhs.z < rhs); }
[[nodiscard]] inline __device__ constexpr auto operator<(lc_ushort lhs, lc_ushort3 rhs) noexcept { return lc_make_bool3(lhs < rhs.x, lhs < rhs.y, lhs < rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator<(lc_ushort4 lhs, lc_ushort4 rhs) noexcept { return lc_make_bool4(lhs.x < rhs.x, lhs.y < rhs.y, lhs.z < rhs.z, lhs.w < rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator<(lc_ushort4 lhs, lc_ushort rhs) noexcept { return lc_make_bool4(lhs.x < rhs, lhs.y < rhs, lhs.z < rhs, lhs.w < rhs); }
[[nodiscard]] inline __device__ constexpr auto operator<(lc_ushort lhs, lc_ushort4 rhs) noexcept { return lc_make_bool4(lhs < rhs.x, lhs < rhs.y, lhs < rhs.z, lhs < rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator<(lc_int2 lhs, lc_int2 rhs) noexcept { return lc_make_bool2(lhs.x < rhs.x, lhs.y < rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator<(lc_int2 lhs, lc_int rhs) noexcept { return lc_make_bool2(lhs.x < rhs, lhs.y < rhs); }
[[nodiscard]] inline __device__ constexpr auto operator<(lc_int lhs, lc_int2 rhs) noexcept { return lc_make_bool2(lhs < rhs.x, lhs < rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator<(lc_int3 lhs, lc_int3 rhs) noexcept { return lc_make_bool3(lhs.x < rhs.x, lhs.y < rhs.y, lhs.z < rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator<(lc_int3 lhs, lc_int rhs) noexcept { return lc_make_bool3(lhs.x < rhs, lhs.y < rhs, lhs.z < rhs); }
[[nodiscard]] inline __device__ constexpr auto operator<(lc_int lhs, lc_int3 rhs) noexcept { return lc_make_bool3(lhs < rhs.x, lhs < rhs.y, lhs < rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator<(lc_int4 lhs, lc_int4 rhs) noexcept { return lc_make_bool4(lhs.x < rhs.x, lhs.y < rhs.y, lhs.z < rhs.z, lhs.w < rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator<(lc_int4 lhs, lc_int rhs) noexcept { return lc_make_bool4(lhs.x < rhs, lhs.y < rhs, lhs.z < rhs, lhs.w < rhs); }
[[nodiscard]] inline __device__ constexpr auto operator<(lc_int lhs, lc_int4 rhs) noexcept { return lc_make_bool4(lhs < rhs.x, lhs < rhs.y, lhs < rhs.z, lhs < rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator<(lc_uint2 lhs, lc_uint2 rhs) noexcept { return lc_make_bool2(lhs.x < rhs.x, lhs.y < rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator<(lc_uint2 lhs, lc_uint rhs) noexcept { return lc_make_bool2(lhs.x < rhs, lhs.y < rhs); }
[[nodiscard]] inline __device__ constexpr auto operator<(lc_uint lhs, lc_uint2 rhs) noexcept { return lc_make_bool2(lhs < rhs.x, lhs < rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator<(lc_uint3 lhs, lc_uint3 rhs) noexcept { return lc_make_bool3(lhs.x < rhs.x, lhs.y < rhs.y, lhs.z < rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator<(lc_uint3 lhs, lc_uint rhs) noexcept { return lc_make_bool3(lhs.x < rhs, lhs.y < rhs, lhs.z < rhs); }
[[nodiscard]] inline __device__ constexpr auto operator<(lc_uint lhs, lc_uint3 rhs) noexcept { return lc_make_bool3(lhs < rhs.x, lhs < rhs.y, lhs < rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator<(lc_uint4 lhs, lc_uint4 rhs) noexcept { return lc_make_bool4(lhs.x < rhs.x, lhs.y < rhs.y, lhs.z < rhs.z, lhs.w < rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator<(lc_uint4 lhs, lc_uint rhs) noexcept { return lc_make_bool4(lhs.x < rhs, lhs.y < rhs, lhs.z < rhs, lhs.w < rhs); }
[[nodiscard]] inline __device__ constexpr auto operator<(lc_uint lhs, lc_uint4 rhs) noexcept { return lc_make_bool4(lhs < rhs.x, lhs < rhs.y, lhs < rhs.z, lhs < rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator<(lc_half2 lhs, lc_half2 rhs) noexcept { return lc_make_bool2(lhs.x < rhs.x, lhs.y < rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator<(lc_half2 lhs, lc_half rhs) noexcept { return lc_make_bool2(lhs.x < rhs, lhs.y < rhs); }
[[nodiscard]] inline __device__ constexpr auto operator<(lc_half lhs, lc_half2 rhs) noexcept { return lc_make_bool2(lhs < rhs.x, lhs < rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator<(lc_half3 lhs, lc_half3 rhs) noexcept { return lc_make_bool3(lhs.x < rhs.x, lhs.y < rhs.y, lhs.z < rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator<(lc_half3 lhs, lc_half rhs) noexcept { return lc_make_bool3(lhs.x < rhs, lhs.y < rhs, lhs.z < rhs); }
[[nodiscard]] inline __device__ constexpr auto operator<(lc_half lhs, lc_half3 rhs) noexcept { return lc_make_bool3(lhs < rhs.x, lhs < rhs.y, lhs < rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator<(lc_half4 lhs, lc_half4 rhs) noexcept { return lc_make_bool4(lhs.x < rhs.x, lhs.y < rhs.y, lhs.z < rhs.z, lhs.w < rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator<(lc_half4 lhs, lc_half rhs) noexcept { return lc_make_bool4(lhs.x < rhs, lhs.y < rhs, lhs.z < rhs, lhs.w < rhs); }
[[nodiscard]] inline __device__ constexpr auto operator<(lc_half lhs, lc_half4 rhs) noexcept { return lc_make_bool4(lhs < rhs.x, lhs < rhs.y, lhs < rhs.z, lhs < rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator<(lc_float2 lhs, lc_float2 rhs) noexcept { return lc_make_bool2(lhs.x < rhs.x, lhs.y < rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator<(lc_float2 lhs, lc_float rhs) noexcept { return lc_make_bool2(lhs.x < rhs, lhs.y < rhs); }
[[nodiscard]] inline __device__ constexpr auto operator<(lc_float lhs, lc_float2 rhs) noexcept { return lc_make_bool2(lhs < rhs.x, lhs < rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator<(lc_float3 lhs, lc_float3 rhs) noexcept { return lc_make_bool3(lhs.x < rhs.x, lhs.y < rhs.y, lhs.z < rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator<(lc_float3 lhs, lc_float rhs) noexcept { return lc_make_bool3(lhs.x < rhs, lhs.y < rhs, lhs.z < rhs); }
[[nodiscard]] inline __device__ constexpr auto operator<(lc_float lhs, lc_float3 rhs) noexcept { return lc_make_bool3(lhs < rhs.x, lhs < rhs.y, lhs < rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator<(lc_float4 lhs, lc_float4 rhs) noexcept { return lc_make_bool4(lhs.x < rhs.x, lhs.y < rhs.y, lhs.z < rhs.z, lhs.w < rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator<(lc_float4 lhs, lc_float rhs) noexcept { return lc_make_bool4(lhs.x < rhs, lhs.y < rhs, lhs.z < rhs, lhs.w < rhs); }
[[nodiscard]] inline __device__ constexpr auto operator<(lc_float lhs, lc_float4 rhs) noexcept { return lc_make_bool4(lhs < rhs.x, lhs < rhs.y, lhs < rhs.z, lhs < rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator<(lc_long2 lhs, lc_long2 rhs) noexcept { return lc_make_bool2(lhs.x < rhs.x, lhs.y < rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator<(lc_long2 lhs, lc_long rhs) noexcept { return lc_make_bool2(lhs.x < rhs, lhs.y < rhs); }
[[nodiscard]] inline __device__ constexpr auto operator<(lc_long lhs, lc_long2 rhs) noexcept { return lc_make_bool2(lhs < rhs.x, lhs < rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator<(lc_long3 lhs, lc_long3 rhs) noexcept { return lc_make_bool3(lhs.x < rhs.x, lhs.y < rhs.y, lhs.z < rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator<(lc_long3 lhs, lc_long rhs) noexcept { return lc_make_bool3(lhs.x < rhs, lhs.y < rhs, lhs.z < rhs); }
[[nodiscard]] inline __device__ constexpr auto operator<(lc_long lhs, lc_long3 rhs) noexcept { return lc_make_bool3(lhs < rhs.x, lhs < rhs.y, lhs < rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator<(lc_long4 lhs, lc_long4 rhs) noexcept { return lc_make_bool4(lhs.x < rhs.x, lhs.y < rhs.y, lhs.z < rhs.z, lhs.w < rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator<(lc_long4 lhs, lc_long rhs) noexcept { return lc_make_bool4(lhs.x < rhs, lhs.y < rhs, lhs.z < rhs, lhs.w < rhs); }
[[nodiscard]] inline __device__ constexpr auto operator<(lc_long lhs, lc_long4 rhs) noexcept { return lc_make_bool4(lhs < rhs.x, lhs < rhs.y, lhs < rhs.z, lhs < rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator<(lc_ulong2 lhs, lc_ulong2 rhs) noexcept { return lc_make_bool2(lhs.x < rhs.x, lhs.y < rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator<(lc_ulong2 lhs, lc_ulong rhs) noexcept { return lc_make_bool2(lhs.x < rhs, lhs.y < rhs); }
[[nodiscard]] inline __device__ constexpr auto operator<(lc_ulong lhs, lc_ulong2 rhs) noexcept { return lc_make_bool2(lhs < rhs.x, lhs < rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator<(lc_ulong3 lhs, lc_ulong3 rhs) noexcept { return lc_make_bool3(lhs.x < rhs.x, lhs.y < rhs.y, lhs.z < rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator<(lc_ulong3 lhs, lc_ulong rhs) noexcept { return lc_make_bool3(lhs.x < rhs, lhs.y < rhs, lhs.z < rhs); }
[[nodiscard]] inline __device__ constexpr auto operator<(lc_ulong lhs, lc_ulong3 rhs) noexcept { return lc_make_bool3(lhs < rhs.x, lhs < rhs.y, lhs < rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator<(lc_ulong4 lhs, lc_ulong4 rhs) noexcept { return lc_make_bool4(lhs.x < rhs.x, lhs.y < rhs.y, lhs.z < rhs.z, lhs.w < rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator<(lc_ulong4 lhs, lc_ulong rhs) noexcept { return lc_make_bool4(lhs.x < rhs, lhs.y < rhs, lhs.z < rhs, lhs.w < rhs); }
[[nodiscard]] inline __device__ constexpr auto operator<(lc_ulong lhs, lc_ulong4 rhs) noexcept { return lc_make_bool4(lhs < rhs.x, lhs < rhs.y, lhs < rhs.z, lhs < rhs.w); }

[[nodiscard]] inline __device__ constexpr auto operator>(lc_short2 lhs, lc_short2 rhs) noexcept { return lc_make_bool2(lhs.x > rhs.x, lhs.y > rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator>(lc_short2 lhs, lc_short rhs) noexcept { return lc_make_bool2(lhs.x > rhs, lhs.y > rhs); }
[[nodiscard]] inline __device__ constexpr auto operator>(lc_short lhs, lc_short2 rhs) noexcept { return lc_make_bool2(lhs > rhs.x, lhs > rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator>(lc_short3 lhs, lc_short3 rhs) noexcept { return lc_make_bool3(lhs.x > rhs.x, lhs.y > rhs.y, lhs.z > rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator>(lc_short3 lhs, lc_short rhs) noexcept { return lc_make_bool3(lhs.x > rhs, lhs.y > rhs, lhs.z > rhs); }
[[nodiscard]] inline __device__ constexpr auto operator>(lc_short lhs, lc_short3 rhs) noexcept { return lc_make_bool3(lhs > rhs.x, lhs > rhs.y, lhs > rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator>(lc_short4 lhs, lc_short4 rhs) noexcept { return lc_make_bool4(lhs.x > rhs.x, lhs.y > rhs.y, lhs.z > rhs.z, lhs.w > rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator>(lc_short4 lhs, lc_short rhs) noexcept { return lc_make_bool4(lhs.x > rhs, lhs.y > rhs, lhs.z > rhs, lhs.w > rhs); }
[[nodiscard]] inline __device__ constexpr auto operator>(lc_short lhs, lc_short4 rhs) noexcept { return lc_make_bool4(lhs > rhs.x, lhs > rhs.y, lhs > rhs.z, lhs > rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator>(lc_ushort2 lhs, lc_ushort2 rhs) noexcept { return lc_make_bool2(lhs.x > rhs.x, lhs.y > rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator>(lc_ushort2 lhs, lc_ushort rhs) noexcept { return lc_make_bool2(lhs.x > rhs, lhs.y > rhs); }
[[nodiscard]] inline __device__ constexpr auto operator>(lc_ushort lhs, lc_ushort2 rhs) noexcept { return lc_make_bool2(lhs > rhs.x, lhs > rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator>(lc_ushort3 lhs, lc_ushort3 rhs) noexcept { return lc_make_bool3(lhs.x > rhs.x, lhs.y > rhs.y, lhs.z > rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator>(lc_ushort3 lhs, lc_ushort rhs) noexcept { return lc_make_bool3(lhs.x > rhs, lhs.y > rhs, lhs.z > rhs); }
[[nodiscard]] inline __device__ constexpr auto operator>(lc_ushort lhs, lc_ushort3 rhs) noexcept { return lc_make_bool3(lhs > rhs.x, lhs > rhs.y, lhs > rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator>(lc_ushort4 lhs, lc_ushort4 rhs) noexcept { return lc_make_bool4(lhs.x > rhs.x, lhs.y > rhs.y, lhs.z > rhs.z, lhs.w > rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator>(lc_ushort4 lhs, lc_ushort rhs) noexcept { return lc_make_bool4(lhs.x > rhs, lhs.y > rhs, lhs.z > rhs, lhs.w > rhs); }
[[nodiscard]] inline __device__ constexpr auto operator>(lc_ushort lhs, lc_ushort4 rhs) noexcept { return lc_make_bool4(lhs > rhs.x, lhs > rhs.y, lhs > rhs.z, lhs > rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator>(lc_int2 lhs, lc_int2 rhs) noexcept { return lc_make_bool2(lhs.x > rhs.x, lhs.y > rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator>(lc_int2 lhs, lc_int rhs) noexcept { return lc_make_bool2(lhs.x > rhs, lhs.y > rhs); }
[[nodiscard]] inline __device__ constexpr auto operator>(lc_int lhs, lc_int2 rhs) noexcept { return lc_make_bool2(lhs > rhs.x, lhs > rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator>(lc_int3 lhs, lc_int3 rhs) noexcept { return lc_make_bool3(lhs.x > rhs.x, lhs.y > rhs.y, lhs.z > rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator>(lc_int3 lhs, lc_int rhs) noexcept { return lc_make_bool3(lhs.x > rhs, lhs.y > rhs, lhs.z > rhs); }
[[nodiscard]] inline __device__ constexpr auto operator>(lc_int lhs, lc_int3 rhs) noexcept { return lc_make_bool3(lhs > rhs.x, lhs > rhs.y, lhs > rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator>(lc_int4 lhs, lc_int4 rhs) noexcept { return lc_make_bool4(lhs.x > rhs.x, lhs.y > rhs.y, lhs.z > rhs.z, lhs.w > rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator>(lc_int4 lhs, lc_int rhs) noexcept { return lc_make_bool4(lhs.x > rhs, lhs.y > rhs, lhs.z > rhs, lhs.w > rhs); }
[[nodiscard]] inline __device__ constexpr auto operator>(lc_int lhs, lc_int4 rhs) noexcept { return lc_make_bool4(lhs > rhs.x, lhs > rhs.y, lhs > rhs.z, lhs > rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator>(lc_uint2 lhs, lc_uint2 rhs) noexcept { return lc_make_bool2(lhs.x > rhs.x, lhs.y > rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator>(lc_uint2 lhs, lc_uint rhs) noexcept { return lc_make_bool2(lhs.x > rhs, lhs.y > rhs); }
[[nodiscard]] inline __device__ constexpr auto operator>(lc_uint lhs, lc_uint2 rhs) noexcept { return lc_make_bool2(lhs > rhs.x, lhs > rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator>(lc_uint3 lhs, lc_uint3 rhs) noexcept { return lc_make_bool3(lhs.x > rhs.x, lhs.y > rhs.y, lhs.z > rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator>(lc_uint3 lhs, lc_uint rhs) noexcept { return lc_make_bool3(lhs.x > rhs, lhs.y > rhs, lhs.z > rhs); }
[[nodiscard]] inline __device__ constexpr auto operator>(lc_uint lhs, lc_uint3 rhs) noexcept { return lc_make_bool3(lhs > rhs.x, lhs > rhs.y, lhs > rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator>(lc_uint4 lhs, lc_uint4 rhs) noexcept { return lc_make_bool4(lhs.x > rhs.x, lhs.y > rhs.y, lhs.z > rhs.z, lhs.w > rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator>(lc_uint4 lhs, lc_uint rhs) noexcept { return lc_make_bool4(lhs.x > rhs, lhs.y > rhs, lhs.z > rhs, lhs.w > rhs); }
[[nodiscard]] inline __device__ constexpr auto operator>(lc_uint lhs, lc_uint4 rhs) noexcept { return lc_make_bool4(lhs > rhs.x, lhs > rhs.y, lhs > rhs.z, lhs > rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator>(lc_half2 lhs, lc_half2 rhs) noexcept { return lc_make_bool2(lhs.x > rhs.x, lhs.y > rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator>(lc_half2 lhs, lc_half rhs) noexcept { return lc_make_bool2(lhs.x > rhs, lhs.y > rhs); }
[[nodiscard]] inline __device__ constexpr auto operator>(lc_half lhs, lc_half2 rhs) noexcept { return lc_make_bool2(lhs > rhs.x, lhs > rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator>(lc_half3 lhs, lc_half3 rhs) noexcept { return lc_make_bool3(lhs.x > rhs.x, lhs.y > rhs.y, lhs.z > rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator>(lc_half3 lhs, lc_half rhs) noexcept { return lc_make_bool3(lhs.x > rhs, lhs.y > rhs, lhs.z > rhs); }
[[nodiscard]] inline __device__ constexpr auto operator>(lc_half lhs, lc_half3 rhs) noexcept { return lc_make_bool3(lhs > rhs.x, lhs > rhs.y, lhs > rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator>(lc_half4 lhs, lc_half4 rhs) noexcept { return lc_make_bool4(lhs.x > rhs.x, lhs.y > rhs.y, lhs.z > rhs.z, lhs.w > rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator>(lc_half4 lhs, lc_half rhs) noexcept { return lc_make_bool4(lhs.x > rhs, lhs.y > rhs, lhs.z > rhs, lhs.w > rhs); }
[[nodiscard]] inline __device__ constexpr auto operator>(lc_half lhs, lc_half4 rhs) noexcept { return lc_make_bool4(lhs > rhs.x, lhs > rhs.y, lhs > rhs.z, lhs > rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator>(lc_float2 lhs, lc_float2 rhs) noexcept { return lc_make_bool2(lhs.x > rhs.x, lhs.y > rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator>(lc_float2 lhs, lc_float rhs) noexcept { return lc_make_bool2(lhs.x > rhs, lhs.y > rhs); }
[[nodiscard]] inline __device__ constexpr auto operator>(lc_float lhs, lc_float2 rhs) noexcept { return lc_make_bool2(lhs > rhs.x, lhs > rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator>(lc_float3 lhs, lc_float3 rhs) noexcept { return lc_make_bool3(lhs.x > rhs.x, lhs.y > rhs.y, lhs.z > rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator>(lc_float3 lhs, lc_float rhs) noexcept { return lc_make_bool3(lhs.x > rhs, lhs.y > rhs, lhs.z > rhs); }
[[nodiscard]] inline __device__ constexpr auto operator>(lc_float lhs, lc_float3 rhs) noexcept { return lc_make_bool3(lhs > rhs.x, lhs > rhs.y, lhs > rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator>(lc_float4 lhs, lc_float4 rhs) noexcept { return lc_make_bool4(lhs.x > rhs.x, lhs.y > rhs.y, lhs.z > rhs.z, lhs.w > rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator>(lc_float4 lhs, lc_float rhs) noexcept { return lc_make_bool4(lhs.x > rhs, lhs.y > rhs, lhs.z > rhs, lhs.w > rhs); }
[[nodiscard]] inline __device__ constexpr auto operator>(lc_float lhs, lc_float4 rhs) noexcept { return lc_make_bool4(lhs > rhs.x, lhs > rhs.y, lhs > rhs.z, lhs > rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator>(lc_long2 lhs, lc_long2 rhs) noexcept { return lc_make_bool2(lhs.x > rhs.x, lhs.y > rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator>(lc_long2 lhs, lc_long rhs) noexcept { return lc_make_bool2(lhs.x > rhs, lhs.y > rhs); }
[[nodiscard]] inline __device__ constexpr auto operator>(lc_long lhs, lc_long2 rhs) noexcept { return lc_make_bool2(lhs > rhs.x, lhs > rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator>(lc_long3 lhs, lc_long3 rhs) noexcept { return lc_make_bool3(lhs.x > rhs.x, lhs.y > rhs.y, lhs.z > rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator>(lc_long3 lhs, lc_long rhs) noexcept { return lc_make_bool3(lhs.x > rhs, lhs.y > rhs, lhs.z > rhs); }
[[nodiscard]] inline __device__ constexpr auto operator>(lc_long lhs, lc_long3 rhs) noexcept { return lc_make_bool3(lhs > rhs.x, lhs > rhs.y, lhs > rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator>(lc_long4 lhs, lc_long4 rhs) noexcept { return lc_make_bool4(lhs.x > rhs.x, lhs.y > rhs.y, lhs.z > rhs.z, lhs.w > rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator>(lc_long4 lhs, lc_long rhs) noexcept { return lc_make_bool4(lhs.x > rhs, lhs.y > rhs, lhs.z > rhs, lhs.w > rhs); }
[[nodiscard]] inline __device__ constexpr auto operator>(lc_long lhs, lc_long4 rhs) noexcept { return lc_make_bool4(lhs > rhs.x, lhs > rhs.y, lhs > rhs.z, lhs > rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator>(lc_ulong2 lhs, lc_ulong2 rhs) noexcept { return lc_make_bool2(lhs.x > rhs.x, lhs.y > rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator>(lc_ulong2 lhs, lc_ulong rhs) noexcept { return lc_make_bool2(lhs.x > rhs, lhs.y > rhs); }
[[nodiscard]] inline __device__ constexpr auto operator>(lc_ulong lhs, lc_ulong2 rhs) noexcept { return lc_make_bool2(lhs > rhs.x, lhs > rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator>(lc_ulong3 lhs, lc_ulong3 rhs) noexcept { return lc_make_bool3(lhs.x > rhs.x, lhs.y > rhs.y, lhs.z > rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator>(lc_ulong3 lhs, lc_ulong rhs) noexcept { return lc_make_bool3(lhs.x > rhs, lhs.y > rhs, lhs.z > rhs); }
[[nodiscard]] inline __device__ constexpr auto operator>(lc_ulong lhs, lc_ulong3 rhs) noexcept { return lc_make_bool3(lhs > rhs.x, lhs > rhs.y, lhs > rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator>(lc_ulong4 lhs, lc_ulong4 rhs) noexcept { return lc_make_bool4(lhs.x > rhs.x, lhs.y > rhs.y, lhs.z > rhs.z, lhs.w > rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator>(lc_ulong4 lhs, lc_ulong rhs) noexcept { return lc_make_bool4(lhs.x > rhs, lhs.y > rhs, lhs.z > rhs, lhs.w > rhs); }
[[nodiscard]] inline __device__ constexpr auto operator>(lc_ulong lhs, lc_ulong4 rhs) noexcept { return lc_make_bool4(lhs > rhs.x, lhs > rhs.y, lhs > rhs.z, lhs > rhs.w); }

[[nodiscard]] inline __device__ constexpr auto operator<=(lc_short2 lhs, lc_short2 rhs) noexcept { return lc_make_bool2(lhs.x <= rhs.x, lhs.y <= rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator<=(lc_short2 lhs, lc_short rhs) noexcept { return lc_make_bool2(lhs.x <= rhs, lhs.y <= rhs); }
[[nodiscard]] inline __device__ constexpr auto operator<=(lc_short lhs, lc_short2 rhs) noexcept { return lc_make_bool2(lhs <= rhs.x, lhs <= rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator<=(lc_short3 lhs, lc_short3 rhs) noexcept { return lc_make_bool3(lhs.x <= rhs.x, lhs.y <= rhs.y, lhs.z <= rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator<=(lc_short3 lhs, lc_short rhs) noexcept { return lc_make_bool3(lhs.x <= rhs, lhs.y <= rhs, lhs.z <= rhs); }
[[nodiscard]] inline __device__ constexpr auto operator<=(lc_short lhs, lc_short3 rhs) noexcept { return lc_make_bool3(lhs <= rhs.x, lhs <= rhs.y, lhs <= rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator<=(lc_short4 lhs, lc_short4 rhs) noexcept { return lc_make_bool4(lhs.x <= rhs.x, lhs.y <= rhs.y, lhs.z <= rhs.z, lhs.w <= rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator<=(lc_short4 lhs, lc_short rhs) noexcept { return lc_make_bool4(lhs.x <= rhs, lhs.y <= rhs, lhs.z <= rhs, lhs.w <= rhs); }
[[nodiscard]] inline __device__ constexpr auto operator<=(lc_short lhs, lc_short4 rhs) noexcept { return lc_make_bool4(lhs <= rhs.x, lhs <= rhs.y, lhs <= rhs.z, lhs <= rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator<=(lc_ushort2 lhs, lc_ushort2 rhs) noexcept { return lc_make_bool2(lhs.x <= rhs.x, lhs.y <= rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator<=(lc_ushort2 lhs, lc_ushort rhs) noexcept { return lc_make_bool2(lhs.x <= rhs, lhs.y <= rhs); }
[[nodiscard]] inline __device__ constexpr auto operator<=(lc_ushort lhs, lc_ushort2 rhs) noexcept { return lc_make_bool2(lhs <= rhs.x, lhs <= rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator<=(lc_ushort3 lhs, lc_ushort3 rhs) noexcept { return lc_make_bool3(lhs.x <= rhs.x, lhs.y <= rhs.y, lhs.z <= rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator<=(lc_ushort3 lhs, lc_ushort rhs) noexcept { return lc_make_bool3(lhs.x <= rhs, lhs.y <= rhs, lhs.z <= rhs); }
[[nodiscard]] inline __device__ constexpr auto operator<=(lc_ushort lhs, lc_ushort3 rhs) noexcept { return lc_make_bool3(lhs <= rhs.x, lhs <= rhs.y, lhs <= rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator<=(lc_ushort4 lhs, lc_ushort4 rhs) noexcept { return lc_make_bool4(lhs.x <= rhs.x, lhs.y <= rhs.y, lhs.z <= rhs.z, lhs.w <= rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator<=(lc_ushort4 lhs, lc_ushort rhs) noexcept { return lc_make_bool4(lhs.x <= rhs, lhs.y <= rhs, lhs.z <= rhs, lhs.w <= rhs); }
[[nodiscard]] inline __device__ constexpr auto operator<=(lc_ushort lhs, lc_ushort4 rhs) noexcept { return lc_make_bool4(lhs <= rhs.x, lhs <= rhs.y, lhs <= rhs.z, lhs <= rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator<=(lc_int2 lhs, lc_int2 rhs) noexcept { return lc_make_bool2(lhs.x <= rhs.x, lhs.y <= rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator<=(lc_int2 lhs, lc_int rhs) noexcept { return lc_make_bool2(lhs.x <= rhs, lhs.y <= rhs); }
[[nodiscard]] inline __device__ constexpr auto operator<=(lc_int lhs, lc_int2 rhs) noexcept { return lc_make_bool2(lhs <= rhs.x, lhs <= rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator<=(lc_int3 lhs, lc_int3 rhs) noexcept { return lc_make_bool3(lhs.x <= rhs.x, lhs.y <= rhs.y, lhs.z <= rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator<=(lc_int3 lhs, lc_int rhs) noexcept { return lc_make_bool3(lhs.x <= rhs, lhs.y <= rhs, lhs.z <= rhs); }
[[nodiscard]] inline __device__ constexpr auto operator<=(lc_int lhs, lc_int3 rhs) noexcept { return lc_make_bool3(lhs <= rhs.x, lhs <= rhs.y, lhs <= rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator<=(lc_int4 lhs, lc_int4 rhs) noexcept { return lc_make_bool4(lhs.x <= rhs.x, lhs.y <= rhs.y, lhs.z <= rhs.z, lhs.w <= rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator<=(lc_int4 lhs, lc_int rhs) noexcept { return lc_make_bool4(lhs.x <= rhs, lhs.y <= rhs, lhs.z <= rhs, lhs.w <= rhs); }
[[nodiscard]] inline __device__ constexpr auto operator<=(lc_int lhs, lc_int4 rhs) noexcept { return lc_make_bool4(lhs <= rhs.x, lhs <= rhs.y, lhs <= rhs.z, lhs <= rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator<=(lc_uint2 lhs, lc_uint2 rhs) noexcept { return lc_make_bool2(lhs.x <= rhs.x, lhs.y <= rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator<=(lc_uint2 lhs, lc_uint rhs) noexcept { return lc_make_bool2(lhs.x <= rhs, lhs.y <= rhs); }
[[nodiscard]] inline __device__ constexpr auto operator<=(lc_uint lhs, lc_uint2 rhs) noexcept { return lc_make_bool2(lhs <= rhs.x, lhs <= rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator<=(lc_uint3 lhs, lc_uint3 rhs) noexcept { return lc_make_bool3(lhs.x <= rhs.x, lhs.y <= rhs.y, lhs.z <= rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator<=(lc_uint3 lhs, lc_uint rhs) noexcept { return lc_make_bool3(lhs.x <= rhs, lhs.y <= rhs, lhs.z <= rhs); }
[[nodiscard]] inline __device__ constexpr auto operator<=(lc_uint lhs, lc_uint3 rhs) noexcept { return lc_make_bool3(lhs <= rhs.x, lhs <= rhs.y, lhs <= rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator<=(lc_uint4 lhs, lc_uint4 rhs) noexcept { return lc_make_bool4(lhs.x <= rhs.x, lhs.y <= rhs.y, lhs.z <= rhs.z, lhs.w <= rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator<=(lc_uint4 lhs, lc_uint rhs) noexcept { return lc_make_bool4(lhs.x <= rhs, lhs.y <= rhs, lhs.z <= rhs, lhs.w <= rhs); }
[[nodiscard]] inline __device__ constexpr auto operator<=(lc_uint lhs, lc_uint4 rhs) noexcept { return lc_make_bool4(lhs <= rhs.x, lhs <= rhs.y, lhs <= rhs.z, lhs <= rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator<=(lc_half2 lhs, lc_half2 rhs) noexcept { return lc_make_bool2(lhs.x <= rhs.x, lhs.y <= rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator<=(lc_half2 lhs, lc_half rhs) noexcept { return lc_make_bool2(lhs.x <= rhs, lhs.y <= rhs); }
[[nodiscard]] inline __device__ constexpr auto operator<=(lc_half lhs, lc_half2 rhs) noexcept { return lc_make_bool2(lhs <= rhs.x, lhs <= rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator<=(lc_half3 lhs, lc_half3 rhs) noexcept { return lc_make_bool3(lhs.x <= rhs.x, lhs.y <= rhs.y, lhs.z <= rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator<=(lc_half3 lhs, lc_half rhs) noexcept { return lc_make_bool3(lhs.x <= rhs, lhs.y <= rhs, lhs.z <= rhs); }
[[nodiscard]] inline __device__ constexpr auto operator<=(lc_half lhs, lc_half3 rhs) noexcept { return lc_make_bool3(lhs <= rhs.x, lhs <= rhs.y, lhs <= rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator<=(lc_half4 lhs, lc_half4 rhs) noexcept { return lc_make_bool4(lhs.x <= rhs.x, lhs.y <= rhs.y, lhs.z <= rhs.z, lhs.w <= rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator<=(lc_half4 lhs, lc_half rhs) noexcept { return lc_make_bool4(lhs.x <= rhs, lhs.y <= rhs, lhs.z <= rhs, lhs.w <= rhs); }
[[nodiscard]] inline __device__ constexpr auto operator<=(lc_half lhs, lc_half4 rhs) noexcept { return lc_make_bool4(lhs <= rhs.x, lhs <= rhs.y, lhs <= rhs.z, lhs <= rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator<=(lc_float2 lhs, lc_float2 rhs) noexcept { return lc_make_bool2(lhs.x <= rhs.x, lhs.y <= rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator<=(lc_float2 lhs, lc_float rhs) noexcept { return lc_make_bool2(lhs.x <= rhs, lhs.y <= rhs); }
[[nodiscard]] inline __device__ constexpr auto operator<=(lc_float lhs, lc_float2 rhs) noexcept { return lc_make_bool2(lhs <= rhs.x, lhs <= rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator<=(lc_float3 lhs, lc_float3 rhs) noexcept { return lc_make_bool3(lhs.x <= rhs.x, lhs.y <= rhs.y, lhs.z <= rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator<=(lc_float3 lhs, lc_float rhs) noexcept { return lc_make_bool3(lhs.x <= rhs, lhs.y <= rhs, lhs.z <= rhs); }
[[nodiscard]] inline __device__ constexpr auto operator<=(lc_float lhs, lc_float3 rhs) noexcept { return lc_make_bool3(lhs <= rhs.x, lhs <= rhs.y, lhs <= rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator<=(lc_float4 lhs, lc_float4 rhs) noexcept { return lc_make_bool4(lhs.x <= rhs.x, lhs.y <= rhs.y, lhs.z <= rhs.z, lhs.w <= rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator<=(lc_float4 lhs, lc_float rhs) noexcept { return lc_make_bool4(lhs.x <= rhs, lhs.y <= rhs, lhs.z <= rhs, lhs.w <= rhs); }
[[nodiscard]] inline __device__ constexpr auto operator<=(lc_float lhs, lc_float4 rhs) noexcept { return lc_make_bool4(lhs <= rhs.x, lhs <= rhs.y, lhs <= rhs.z, lhs <= rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator<=(lc_long2 lhs, lc_long2 rhs) noexcept { return lc_make_bool2(lhs.x <= rhs.x, lhs.y <= rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator<=(lc_long2 lhs, lc_long rhs) noexcept { return lc_make_bool2(lhs.x <= rhs, lhs.y <= rhs); }
[[nodiscard]] inline __device__ constexpr auto operator<=(lc_long lhs, lc_long2 rhs) noexcept { return lc_make_bool2(lhs <= rhs.x, lhs <= rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator<=(lc_long3 lhs, lc_long3 rhs) noexcept { return lc_make_bool3(lhs.x <= rhs.x, lhs.y <= rhs.y, lhs.z <= rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator<=(lc_long3 lhs, lc_long rhs) noexcept { return lc_make_bool3(lhs.x <= rhs, lhs.y <= rhs, lhs.z <= rhs); }
[[nodiscard]] inline __device__ constexpr auto operator<=(lc_long lhs, lc_long3 rhs) noexcept { return lc_make_bool3(lhs <= rhs.x, lhs <= rhs.y, lhs <= rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator<=(lc_long4 lhs, lc_long4 rhs) noexcept { return lc_make_bool4(lhs.x <= rhs.x, lhs.y <= rhs.y, lhs.z <= rhs.z, lhs.w <= rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator<=(lc_long4 lhs, lc_long rhs) noexcept { return lc_make_bool4(lhs.x <= rhs, lhs.y <= rhs, lhs.z <= rhs, lhs.w <= rhs); }
[[nodiscard]] inline __device__ constexpr auto operator<=(lc_long lhs, lc_long4 rhs) noexcept { return lc_make_bool4(lhs <= rhs.x, lhs <= rhs.y, lhs <= rhs.z, lhs <= rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator<=(lc_ulong2 lhs, lc_ulong2 rhs) noexcept { return lc_make_bool2(lhs.x <= rhs.x, lhs.y <= rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator<=(lc_ulong2 lhs, lc_ulong rhs) noexcept { return lc_make_bool2(lhs.x <= rhs, lhs.y <= rhs); }
[[nodiscard]] inline __device__ constexpr auto operator<=(lc_ulong lhs, lc_ulong2 rhs) noexcept { return lc_make_bool2(lhs <= rhs.x, lhs <= rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator<=(lc_ulong3 lhs, lc_ulong3 rhs) noexcept { return lc_make_bool3(lhs.x <= rhs.x, lhs.y <= rhs.y, lhs.z <= rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator<=(lc_ulong3 lhs, lc_ulong rhs) noexcept { return lc_make_bool3(lhs.x <= rhs, lhs.y <= rhs, lhs.z <= rhs); }
[[nodiscard]] inline __device__ constexpr auto operator<=(lc_ulong lhs, lc_ulong3 rhs) noexcept { return lc_make_bool3(lhs <= rhs.x, lhs <= rhs.y, lhs <= rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator<=(lc_ulong4 lhs, lc_ulong4 rhs) noexcept { return lc_make_bool4(lhs.x <= rhs.x, lhs.y <= rhs.y, lhs.z <= rhs.z, lhs.w <= rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator<=(lc_ulong4 lhs, lc_ulong rhs) noexcept { return lc_make_bool4(lhs.x <= rhs, lhs.y <= rhs, lhs.z <= rhs, lhs.w <= rhs); }
[[nodiscard]] inline __device__ constexpr auto operator<=(lc_ulong lhs, lc_ulong4 rhs) noexcept { return lc_make_bool4(lhs <= rhs.x, lhs <= rhs.y, lhs <= rhs.z, lhs <= rhs.w); }

[[nodiscard]] inline __device__ constexpr auto operator>=(lc_short2 lhs, lc_short2 rhs) noexcept { return lc_make_bool2(lhs.x >= rhs.x, lhs.y >= rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator>=(lc_short2 lhs, lc_short rhs) noexcept { return lc_make_bool2(lhs.x >= rhs, lhs.y >= rhs); }
[[nodiscard]] inline __device__ constexpr auto operator>=(lc_short lhs, lc_short2 rhs) noexcept { return lc_make_bool2(lhs >= rhs.x, lhs >= rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator>=(lc_short3 lhs, lc_short3 rhs) noexcept { return lc_make_bool3(lhs.x >= rhs.x, lhs.y >= rhs.y, lhs.z >= rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator>=(lc_short3 lhs, lc_short rhs) noexcept { return lc_make_bool3(lhs.x >= rhs, lhs.y >= rhs, lhs.z >= rhs); }
[[nodiscard]] inline __device__ constexpr auto operator>=(lc_short lhs, lc_short3 rhs) noexcept { return lc_make_bool3(lhs >= rhs.x, lhs >= rhs.y, lhs >= rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator>=(lc_short4 lhs, lc_short4 rhs) noexcept { return lc_make_bool4(lhs.x >= rhs.x, lhs.y >= rhs.y, lhs.z >= rhs.z, lhs.w >= rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator>=(lc_short4 lhs, lc_short rhs) noexcept { return lc_make_bool4(lhs.x >= rhs, lhs.y >= rhs, lhs.z >= rhs, lhs.w >= rhs); }
[[nodiscard]] inline __device__ constexpr auto operator>=(lc_short lhs, lc_short4 rhs) noexcept { return lc_make_bool4(lhs >= rhs.x, lhs >= rhs.y, lhs >= rhs.z, lhs >= rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator>=(lc_ushort2 lhs, lc_ushort2 rhs) noexcept { return lc_make_bool2(lhs.x >= rhs.x, lhs.y >= rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator>=(lc_ushort2 lhs, lc_ushort rhs) noexcept { return lc_make_bool2(lhs.x >= rhs, lhs.y >= rhs); }
[[nodiscard]] inline __device__ constexpr auto operator>=(lc_ushort lhs, lc_ushort2 rhs) noexcept { return lc_make_bool2(lhs >= rhs.x, lhs >= rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator>=(lc_ushort3 lhs, lc_ushort3 rhs) noexcept { return lc_make_bool3(lhs.x >= rhs.x, lhs.y >= rhs.y, lhs.z >= rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator>=(lc_ushort3 lhs, lc_ushort rhs) noexcept { return lc_make_bool3(lhs.x >= rhs, lhs.y >= rhs, lhs.z >= rhs); }
[[nodiscard]] inline __device__ constexpr auto operator>=(lc_ushort lhs, lc_ushort3 rhs) noexcept { return lc_make_bool3(lhs >= rhs.x, lhs >= rhs.y, lhs >= rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator>=(lc_ushort4 lhs, lc_ushort4 rhs) noexcept { return lc_make_bool4(lhs.x >= rhs.x, lhs.y >= rhs.y, lhs.z >= rhs.z, lhs.w >= rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator>=(lc_ushort4 lhs, lc_ushort rhs) noexcept { return lc_make_bool4(lhs.x >= rhs, lhs.y >= rhs, lhs.z >= rhs, lhs.w >= rhs); }
[[nodiscard]] inline __device__ constexpr auto operator>=(lc_ushort lhs, lc_ushort4 rhs) noexcept { return lc_make_bool4(lhs >= rhs.x, lhs >= rhs.y, lhs >= rhs.z, lhs >= rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator>=(lc_int2 lhs, lc_int2 rhs) noexcept { return lc_make_bool2(lhs.x >= rhs.x, lhs.y >= rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator>=(lc_int2 lhs, lc_int rhs) noexcept { return lc_make_bool2(lhs.x >= rhs, lhs.y >= rhs); }
[[nodiscard]] inline __device__ constexpr auto operator>=(lc_int lhs, lc_int2 rhs) noexcept { return lc_make_bool2(lhs >= rhs.x, lhs >= rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator>=(lc_int3 lhs, lc_int3 rhs) noexcept { return lc_make_bool3(lhs.x >= rhs.x, lhs.y >= rhs.y, lhs.z >= rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator>=(lc_int3 lhs, lc_int rhs) noexcept { return lc_make_bool3(lhs.x >= rhs, lhs.y >= rhs, lhs.z >= rhs); }
[[nodiscard]] inline __device__ constexpr auto operator>=(lc_int lhs, lc_int3 rhs) noexcept { return lc_make_bool3(lhs >= rhs.x, lhs >= rhs.y, lhs >= rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator>=(lc_int4 lhs, lc_int4 rhs) noexcept { return lc_make_bool4(lhs.x >= rhs.x, lhs.y >= rhs.y, lhs.z >= rhs.z, lhs.w >= rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator>=(lc_int4 lhs, lc_int rhs) noexcept { return lc_make_bool4(lhs.x >= rhs, lhs.y >= rhs, lhs.z >= rhs, lhs.w >= rhs); }
[[nodiscard]] inline __device__ constexpr auto operator>=(lc_int lhs, lc_int4 rhs) noexcept { return lc_make_bool4(lhs >= rhs.x, lhs >= rhs.y, lhs >= rhs.z, lhs >= rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator>=(lc_uint2 lhs, lc_uint2 rhs) noexcept { return lc_make_bool2(lhs.x >= rhs.x, lhs.y >= rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator>=(lc_uint2 lhs, lc_uint rhs) noexcept { return lc_make_bool2(lhs.x >= rhs, lhs.y >= rhs); }
[[nodiscard]] inline __device__ constexpr auto operator>=(lc_uint lhs, lc_uint2 rhs) noexcept { return lc_make_bool2(lhs >= rhs.x, lhs >= rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator>=(lc_uint3 lhs, lc_uint3 rhs) noexcept { return lc_make_bool3(lhs.x >= rhs.x, lhs.y >= rhs.y, lhs.z >= rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator>=(lc_uint3 lhs, lc_uint rhs) noexcept { return lc_make_bool3(lhs.x >= rhs, lhs.y >= rhs, lhs.z >= rhs); }
[[nodiscard]] inline __device__ constexpr auto operator>=(lc_uint lhs, lc_uint3 rhs) noexcept { return lc_make_bool3(lhs >= rhs.x, lhs >= rhs.y, lhs >= rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator>=(lc_uint4 lhs, lc_uint4 rhs) noexcept { return lc_make_bool4(lhs.x >= rhs.x, lhs.y >= rhs.y, lhs.z >= rhs.z, lhs.w >= rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator>=(lc_uint4 lhs, lc_uint rhs) noexcept { return lc_make_bool4(lhs.x >= rhs, lhs.y >= rhs, lhs.z >= rhs, lhs.w >= rhs); }
[[nodiscard]] inline __device__ constexpr auto operator>=(lc_uint lhs, lc_uint4 rhs) noexcept { return lc_make_bool4(lhs >= rhs.x, lhs >= rhs.y, lhs >= rhs.z, lhs >= rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator>=(lc_half2 lhs, lc_half2 rhs) noexcept { return lc_make_bool2(lhs.x >= rhs.x, lhs.y >= rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator>=(lc_half2 lhs, lc_half rhs) noexcept { return lc_make_bool2(lhs.x >= rhs, lhs.y >= rhs); }
[[nodiscard]] inline __device__ constexpr auto operator>=(lc_half lhs, lc_half2 rhs) noexcept { return lc_make_bool2(lhs >= rhs.x, lhs >= rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator>=(lc_half3 lhs, lc_half3 rhs) noexcept { return lc_make_bool3(lhs.x >= rhs.x, lhs.y >= rhs.y, lhs.z >= rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator>=(lc_half3 lhs, lc_half rhs) noexcept { return lc_make_bool3(lhs.x >= rhs, lhs.y >= rhs, lhs.z >= rhs); }
[[nodiscard]] inline __device__ constexpr auto operator>=(lc_half lhs, lc_half3 rhs) noexcept { return lc_make_bool3(lhs >= rhs.x, lhs >= rhs.y, lhs >= rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator>=(lc_half4 lhs, lc_half4 rhs) noexcept { return lc_make_bool4(lhs.x >= rhs.x, lhs.y >= rhs.y, lhs.z >= rhs.z, lhs.w >= rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator>=(lc_half4 lhs, lc_half rhs) noexcept { return lc_make_bool4(lhs.x >= rhs, lhs.y >= rhs, lhs.z >= rhs, lhs.w >= rhs); }
[[nodiscard]] inline __device__ constexpr auto operator>=(lc_half lhs, lc_half4 rhs) noexcept { return lc_make_bool4(lhs >= rhs.x, lhs >= rhs.y, lhs >= rhs.z, lhs >= rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator>=(lc_float2 lhs, lc_float2 rhs) noexcept { return lc_make_bool2(lhs.x >= rhs.x, lhs.y >= rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator>=(lc_float2 lhs, lc_float rhs) noexcept { return lc_make_bool2(lhs.x >= rhs, lhs.y >= rhs); }
[[nodiscard]] inline __device__ constexpr auto operator>=(lc_float lhs, lc_float2 rhs) noexcept { return lc_make_bool2(lhs >= rhs.x, lhs >= rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator>=(lc_float3 lhs, lc_float3 rhs) noexcept { return lc_make_bool3(lhs.x >= rhs.x, lhs.y >= rhs.y, lhs.z >= rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator>=(lc_float3 lhs, lc_float rhs) noexcept { return lc_make_bool3(lhs.x >= rhs, lhs.y >= rhs, lhs.z >= rhs); }
[[nodiscard]] inline __device__ constexpr auto operator>=(lc_float lhs, lc_float3 rhs) noexcept { return lc_make_bool3(lhs >= rhs.x, lhs >= rhs.y, lhs >= rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator>=(lc_float4 lhs, lc_float4 rhs) noexcept { return lc_make_bool4(lhs.x >= rhs.x, lhs.y >= rhs.y, lhs.z >= rhs.z, lhs.w >= rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator>=(lc_float4 lhs, lc_float rhs) noexcept { return lc_make_bool4(lhs.x >= rhs, lhs.y >= rhs, lhs.z >= rhs, lhs.w >= rhs); }
[[nodiscard]] inline __device__ constexpr auto operator>=(lc_float lhs, lc_float4 rhs) noexcept { return lc_make_bool4(lhs >= rhs.x, lhs >= rhs.y, lhs >= rhs.z, lhs >= rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator>=(lc_long2 lhs, lc_long2 rhs) noexcept { return lc_make_bool2(lhs.x >= rhs.x, lhs.y >= rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator>=(lc_long2 lhs, lc_long rhs) noexcept { return lc_make_bool2(lhs.x >= rhs, lhs.y >= rhs); }
[[nodiscard]] inline __device__ constexpr auto operator>=(lc_long lhs, lc_long2 rhs) noexcept { return lc_make_bool2(lhs >= rhs.x, lhs >= rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator>=(lc_long3 lhs, lc_long3 rhs) noexcept { return lc_make_bool3(lhs.x >= rhs.x, lhs.y >= rhs.y, lhs.z >= rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator>=(lc_long3 lhs, lc_long rhs) noexcept { return lc_make_bool3(lhs.x >= rhs, lhs.y >= rhs, lhs.z >= rhs); }
[[nodiscard]] inline __device__ constexpr auto operator>=(lc_long lhs, lc_long3 rhs) noexcept { return lc_make_bool3(lhs >= rhs.x, lhs >= rhs.y, lhs >= rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator>=(lc_long4 lhs, lc_long4 rhs) noexcept { return lc_make_bool4(lhs.x >= rhs.x, lhs.y >= rhs.y, lhs.z >= rhs.z, lhs.w >= rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator>=(lc_long4 lhs, lc_long rhs) noexcept { return lc_make_bool4(lhs.x >= rhs, lhs.y >= rhs, lhs.z >= rhs, lhs.w >= rhs); }
[[nodiscard]] inline __device__ constexpr auto operator>=(lc_long lhs, lc_long4 rhs) noexcept { return lc_make_bool4(lhs >= rhs.x, lhs >= rhs.y, lhs >= rhs.z, lhs >= rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator>=(lc_ulong2 lhs, lc_ulong2 rhs) noexcept { return lc_make_bool2(lhs.x >= rhs.x, lhs.y >= rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator>=(lc_ulong2 lhs, lc_ulong rhs) noexcept { return lc_make_bool2(lhs.x >= rhs, lhs.y >= rhs); }
[[nodiscard]] inline __device__ constexpr auto operator>=(lc_ulong lhs, lc_ulong2 rhs) noexcept { return lc_make_bool2(lhs >= rhs.x, lhs >= rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator>=(lc_ulong3 lhs, lc_ulong3 rhs) noexcept { return lc_make_bool3(lhs.x >= rhs.x, lhs.y >= rhs.y, lhs.z >= rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator>=(lc_ulong3 lhs, lc_ulong rhs) noexcept { return lc_make_bool3(lhs.x >= rhs, lhs.y >= rhs, lhs.z >= rhs); }
[[nodiscard]] inline __device__ constexpr auto operator>=(lc_ulong lhs, lc_ulong3 rhs) noexcept { return lc_make_bool3(lhs >= rhs.x, lhs >= rhs.y, lhs >= rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator>=(lc_ulong4 lhs, lc_ulong4 rhs) noexcept { return lc_make_bool4(lhs.x >= rhs.x, lhs.y >= rhs.y, lhs.z >= rhs.z, lhs.w >= rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator>=(lc_ulong4 lhs, lc_ulong rhs) noexcept { return lc_make_bool4(lhs.x >= rhs, lhs.y >= rhs, lhs.z >= rhs, lhs.w >= rhs); }
[[nodiscard]] inline __device__ constexpr auto operator>=(lc_ulong lhs, lc_ulong4 rhs) noexcept { return lc_make_bool4(lhs >= rhs.x, lhs >= rhs.y, lhs >= rhs.z, lhs >= rhs.w); }

[[nodiscard]] inline __device__ constexpr auto operator+(lc_short2 lhs, lc_short2 rhs) noexcept { return lc_make_short2(lhs.x + rhs.x, lhs.y + rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator+(lc_short2 lhs, lc_short rhs) noexcept { return lc_make_short2(lhs.x + rhs, lhs.y + rhs); }
[[nodiscard]] inline __device__ constexpr auto operator+(lc_short lhs, lc_short2 rhs) noexcept { return lc_make_short2(lhs + rhs.x, lhs + rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator+(lc_short3 lhs, lc_short3 rhs) noexcept { return lc_make_short3(lhs.x + rhs.x, lhs.y + rhs.y, lhs.z + rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator+(lc_short3 lhs, lc_short rhs) noexcept { return lc_make_short3(lhs.x + rhs, lhs.y + rhs, lhs.z + rhs); }
[[nodiscard]] inline __device__ constexpr auto operator+(lc_short lhs, lc_short3 rhs) noexcept { return lc_make_short3(lhs + rhs.x, lhs + rhs.y, lhs + rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator+(lc_short4 lhs, lc_short4 rhs) noexcept { return lc_make_short4(lhs.x + rhs.x, lhs.y + rhs.y, lhs.z + rhs.z, lhs.w + rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator+(lc_short4 lhs, lc_short rhs) noexcept { return lc_make_short4(lhs.x + rhs, lhs.y + rhs, lhs.z + rhs, lhs.w + rhs); }
[[nodiscard]] inline __device__ constexpr auto operator+(lc_short lhs, lc_short4 rhs) noexcept { return lc_make_short4(lhs + rhs.x, lhs + rhs.y, lhs + rhs.z, lhs + rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator+(lc_ushort2 lhs, lc_ushort2 rhs) noexcept { return lc_make_ushort2(lhs.x + rhs.x, lhs.y + rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator+(lc_ushort2 lhs, lc_ushort rhs) noexcept { return lc_make_ushort2(lhs.x + rhs, lhs.y + rhs); }
[[nodiscard]] inline __device__ constexpr auto operator+(lc_ushort lhs, lc_ushort2 rhs) noexcept { return lc_make_ushort2(lhs + rhs.x, lhs + rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator+(lc_ushort3 lhs, lc_ushort3 rhs) noexcept { return lc_make_ushort3(lhs.x + rhs.x, lhs.y + rhs.y, lhs.z + rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator+(lc_ushort3 lhs, lc_ushort rhs) noexcept { return lc_make_ushort3(lhs.x + rhs, lhs.y + rhs, lhs.z + rhs); }
[[nodiscard]] inline __device__ constexpr auto operator+(lc_ushort lhs, lc_ushort3 rhs) noexcept { return lc_make_ushort3(lhs + rhs.x, lhs + rhs.y, lhs + rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator+(lc_ushort4 lhs, lc_ushort4 rhs) noexcept { return lc_make_ushort4(lhs.x + rhs.x, lhs.y + rhs.y, lhs.z + rhs.z, lhs.w + rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator+(lc_ushort4 lhs, lc_ushort rhs) noexcept { return lc_make_ushort4(lhs.x + rhs, lhs.y + rhs, lhs.z + rhs, lhs.w + rhs); }
[[nodiscard]] inline __device__ constexpr auto operator+(lc_ushort lhs, lc_ushort4 rhs) noexcept { return lc_make_ushort4(lhs + rhs.x, lhs + rhs.y, lhs + rhs.z, lhs + rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator+(lc_int2 lhs, lc_int2 rhs) noexcept { return lc_make_int2(lhs.x + rhs.x, lhs.y + rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator+(lc_int2 lhs, lc_int rhs) noexcept { return lc_make_int2(lhs.x + rhs, lhs.y + rhs); }
[[nodiscard]] inline __device__ constexpr auto operator+(lc_int lhs, lc_int2 rhs) noexcept { return lc_make_int2(lhs + rhs.x, lhs + rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator+(lc_int3 lhs, lc_int3 rhs) noexcept { return lc_make_int3(lhs.x + rhs.x, lhs.y + rhs.y, lhs.z + rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator+(lc_int3 lhs, lc_int rhs) noexcept { return lc_make_int3(lhs.x + rhs, lhs.y + rhs, lhs.z + rhs); }
[[nodiscard]] inline __device__ constexpr auto operator+(lc_int lhs, lc_int3 rhs) noexcept { return lc_make_int3(lhs + rhs.x, lhs + rhs.y, lhs + rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator+(lc_int4 lhs, lc_int4 rhs) noexcept { return lc_make_int4(lhs.x + rhs.x, lhs.y + rhs.y, lhs.z + rhs.z, lhs.w + rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator+(lc_int4 lhs, lc_int rhs) noexcept { return lc_make_int4(lhs.x + rhs, lhs.y + rhs, lhs.z + rhs, lhs.w + rhs); }
[[nodiscard]] inline __device__ constexpr auto operator+(lc_int lhs, lc_int4 rhs) noexcept { return lc_make_int4(lhs + rhs.x, lhs + rhs.y, lhs + rhs.z, lhs + rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator+(lc_uint2 lhs, lc_uint2 rhs) noexcept { return lc_make_uint2(lhs.x + rhs.x, lhs.y + rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator+(lc_uint2 lhs, lc_uint rhs) noexcept { return lc_make_uint2(lhs.x + rhs, lhs.y + rhs); }
[[nodiscard]] inline __device__ constexpr auto operator+(lc_uint lhs, lc_uint2 rhs) noexcept { return lc_make_uint2(lhs + rhs.x, lhs + rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator+(lc_uint3 lhs, lc_uint3 rhs) noexcept { return lc_make_uint3(lhs.x + rhs.x, lhs.y + rhs.y, lhs.z + rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator+(lc_uint3 lhs, lc_uint rhs) noexcept { return lc_make_uint3(lhs.x + rhs, lhs.y + rhs, lhs.z + rhs); }
[[nodiscard]] inline __device__ constexpr auto operator+(lc_uint lhs, lc_uint3 rhs) noexcept { return lc_make_uint3(lhs + rhs.x, lhs + rhs.y, lhs + rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator+(lc_uint4 lhs, lc_uint4 rhs) noexcept { return lc_make_uint4(lhs.x + rhs.x, lhs.y + rhs.y, lhs.z + rhs.z, lhs.w + rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator+(lc_uint4 lhs, lc_uint rhs) noexcept { return lc_make_uint4(lhs.x + rhs, lhs.y + rhs, lhs.z + rhs, lhs.w + rhs); }
[[nodiscard]] inline __device__ constexpr auto operator+(lc_uint lhs, lc_uint4 rhs) noexcept { return lc_make_uint4(lhs + rhs.x, lhs + rhs.y, lhs + rhs.z, lhs + rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator+(lc_half2 lhs, lc_half2 rhs) noexcept { return lc_make_half2(lhs.x + rhs.x, lhs.y + rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator+(lc_half2 lhs, lc_half rhs) noexcept { return lc_make_half2(lhs.x + rhs, lhs.y + rhs); }
[[nodiscard]] inline __device__ constexpr auto operator+(lc_half lhs, lc_half2 rhs) noexcept { return lc_make_half2(lhs + rhs.x, lhs + rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator+(lc_half3 lhs, lc_half3 rhs) noexcept { return lc_make_half3(lhs.x + rhs.x, lhs.y + rhs.y, lhs.z + rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator+(lc_half3 lhs, lc_half rhs) noexcept { return lc_make_half3(lhs.x + rhs, lhs.y + rhs, lhs.z + rhs); }
[[nodiscard]] inline __device__ constexpr auto operator+(lc_half lhs, lc_half3 rhs) noexcept { return lc_make_half3(lhs + rhs.x, lhs + rhs.y, lhs + rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator+(lc_half4 lhs, lc_half4 rhs) noexcept { return lc_make_half4(lhs.x + rhs.x, lhs.y + rhs.y, lhs.z + rhs.z, lhs.w + rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator+(lc_half4 lhs, lc_half rhs) noexcept { return lc_make_half4(lhs.x + rhs, lhs.y + rhs, lhs.z + rhs, lhs.w + rhs); }
[[nodiscard]] inline __device__ constexpr auto operator+(lc_half lhs, lc_half4 rhs) noexcept { return lc_make_half4(lhs + rhs.x, lhs + rhs.y, lhs + rhs.z, lhs + rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator+(lc_float2 lhs, lc_float2 rhs) noexcept { return lc_make_float2(lhs.x + rhs.x, lhs.y + rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator+(lc_float2 lhs, lc_float rhs) noexcept { return lc_make_float2(lhs.x + rhs, lhs.y + rhs); }
[[nodiscard]] inline __device__ constexpr auto operator+(lc_float lhs, lc_float2 rhs) noexcept { return lc_make_float2(lhs + rhs.x, lhs + rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator+(lc_float3 lhs, lc_float3 rhs) noexcept { return lc_make_float3(lhs.x + rhs.x, lhs.y + rhs.y, lhs.z + rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator+(lc_float3 lhs, lc_float rhs) noexcept { return lc_make_float3(lhs.x + rhs, lhs.y + rhs, lhs.z + rhs); }
[[nodiscard]] inline __device__ constexpr auto operator+(lc_float lhs, lc_float3 rhs) noexcept { return lc_make_float3(lhs + rhs.x, lhs + rhs.y, lhs + rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator+(lc_float4 lhs, lc_float4 rhs) noexcept { return lc_make_float4(lhs.x + rhs.x, lhs.y + rhs.y, lhs.z + rhs.z, lhs.w + rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator+(lc_float4 lhs, lc_float rhs) noexcept { return lc_make_float4(lhs.x + rhs, lhs.y + rhs, lhs.z + rhs, lhs.w + rhs); }
[[nodiscard]] inline __device__ constexpr auto operator+(lc_float lhs, lc_float4 rhs) noexcept { return lc_make_float4(lhs + rhs.x, lhs + rhs.y, lhs + rhs.z, lhs + rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator+(lc_long2 lhs, lc_long2 rhs) noexcept { return lc_make_long2(lhs.x + rhs.x, lhs.y + rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator+(lc_long2 lhs, lc_long rhs) noexcept { return lc_make_long2(lhs.x + rhs, lhs.y + rhs); }
[[nodiscard]] inline __device__ constexpr auto operator+(lc_long lhs, lc_long2 rhs) noexcept { return lc_make_long2(lhs + rhs.x, lhs + rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator+(lc_long3 lhs, lc_long3 rhs) noexcept { return lc_make_long3(lhs.x + rhs.x, lhs.y + rhs.y, lhs.z + rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator+(lc_long3 lhs, lc_long rhs) noexcept { return lc_make_long3(lhs.x + rhs, lhs.y + rhs, lhs.z + rhs); }
[[nodiscard]] inline __device__ constexpr auto operator+(lc_long lhs, lc_long3 rhs) noexcept { return lc_make_long3(lhs + rhs.x, lhs + rhs.y, lhs + rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator+(lc_long4 lhs, lc_long4 rhs) noexcept { return lc_make_long4(lhs.x + rhs.x, lhs.y + rhs.y, lhs.z + rhs.z, lhs.w + rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator+(lc_long4 lhs, lc_long rhs) noexcept { return lc_make_long4(lhs.x + rhs, lhs.y + rhs, lhs.z + rhs, lhs.w + rhs); }
[[nodiscard]] inline __device__ constexpr auto operator+(lc_long lhs, lc_long4 rhs) noexcept { return lc_make_long4(lhs + rhs.x, lhs + rhs.y, lhs + rhs.z, lhs + rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator+(lc_ulong2 lhs, lc_ulong2 rhs) noexcept { return lc_make_ulong2(lhs.x + rhs.x, lhs.y + rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator+(lc_ulong2 lhs, lc_ulong rhs) noexcept { return lc_make_ulong2(lhs.x + rhs, lhs.y + rhs); }
[[nodiscard]] inline __device__ constexpr auto operator+(lc_ulong lhs, lc_ulong2 rhs) noexcept { return lc_make_ulong2(lhs + rhs.x, lhs + rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator+(lc_ulong3 lhs, lc_ulong3 rhs) noexcept { return lc_make_ulong3(lhs.x + rhs.x, lhs.y + rhs.y, lhs.z + rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator+(lc_ulong3 lhs, lc_ulong rhs) noexcept { return lc_make_ulong3(lhs.x + rhs, lhs.y + rhs, lhs.z + rhs); }
[[nodiscard]] inline __device__ constexpr auto operator+(lc_ulong lhs, lc_ulong3 rhs) noexcept { return lc_make_ulong3(lhs + rhs.x, lhs + rhs.y, lhs + rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator+(lc_ulong4 lhs, lc_ulong4 rhs) noexcept { return lc_make_ulong4(lhs.x + rhs.x, lhs.y + rhs.y, lhs.z + rhs.z, lhs.w + rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator+(lc_ulong4 lhs, lc_ulong rhs) noexcept { return lc_make_ulong4(lhs.x + rhs, lhs.y + rhs, lhs.z + rhs, lhs.w + rhs); }
[[nodiscard]] inline __device__ constexpr auto operator+(lc_ulong lhs, lc_ulong4 rhs) noexcept { return lc_make_ulong4(lhs + rhs.x, lhs + rhs.y, lhs + rhs.z, lhs + rhs.w); }

[[nodiscard]] inline __device__ constexpr auto operator-(lc_short2 lhs, lc_short2 rhs) noexcept { return lc_make_short2(lhs.x - rhs.x, lhs.y - rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator-(lc_short2 lhs, lc_short rhs) noexcept { return lc_make_short2(lhs.x - rhs, lhs.y - rhs); }
[[nodiscard]] inline __device__ constexpr auto operator-(lc_short lhs, lc_short2 rhs) noexcept { return lc_make_short2(lhs - rhs.x, lhs - rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator-(lc_short3 lhs, lc_short3 rhs) noexcept { return lc_make_short3(lhs.x - rhs.x, lhs.y - rhs.y, lhs.z - rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator-(lc_short3 lhs, lc_short rhs) noexcept { return lc_make_short3(lhs.x - rhs, lhs.y - rhs, lhs.z - rhs); }
[[nodiscard]] inline __device__ constexpr auto operator-(lc_short lhs, lc_short3 rhs) noexcept { return lc_make_short3(lhs - rhs.x, lhs - rhs.y, lhs - rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator-(lc_short4 lhs, lc_short4 rhs) noexcept { return lc_make_short4(lhs.x - rhs.x, lhs.y - rhs.y, lhs.z - rhs.z, lhs.w - rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator-(lc_short4 lhs, lc_short rhs) noexcept { return lc_make_short4(lhs.x - rhs, lhs.y - rhs, lhs.z - rhs, lhs.w - rhs); }
[[nodiscard]] inline __device__ constexpr auto operator-(lc_short lhs, lc_short4 rhs) noexcept { return lc_make_short4(lhs - rhs.x, lhs - rhs.y, lhs - rhs.z, lhs - rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator-(lc_ushort2 lhs, lc_ushort2 rhs) noexcept { return lc_make_ushort2(lhs.x - rhs.x, lhs.y - rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator-(lc_ushort2 lhs, lc_ushort rhs) noexcept { return lc_make_ushort2(lhs.x - rhs, lhs.y - rhs); }
[[nodiscard]] inline __device__ constexpr auto operator-(lc_ushort lhs, lc_ushort2 rhs) noexcept { return lc_make_ushort2(lhs - rhs.x, lhs - rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator-(lc_ushort3 lhs, lc_ushort3 rhs) noexcept { return lc_make_ushort3(lhs.x - rhs.x, lhs.y - rhs.y, lhs.z - rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator-(lc_ushort3 lhs, lc_ushort rhs) noexcept { return lc_make_ushort3(lhs.x - rhs, lhs.y - rhs, lhs.z - rhs); }
[[nodiscard]] inline __device__ constexpr auto operator-(lc_ushort lhs, lc_ushort3 rhs) noexcept { return lc_make_ushort3(lhs - rhs.x, lhs - rhs.y, lhs - rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator-(lc_ushort4 lhs, lc_ushort4 rhs) noexcept { return lc_make_ushort4(lhs.x - rhs.x, lhs.y - rhs.y, lhs.z - rhs.z, lhs.w - rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator-(lc_ushort4 lhs, lc_ushort rhs) noexcept { return lc_make_ushort4(lhs.x - rhs, lhs.y - rhs, lhs.z - rhs, lhs.w - rhs); }
[[nodiscard]] inline __device__ constexpr auto operator-(lc_ushort lhs, lc_ushort4 rhs) noexcept { return lc_make_ushort4(lhs - rhs.x, lhs - rhs.y, lhs - rhs.z, lhs - rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator-(lc_int2 lhs, lc_int2 rhs) noexcept { return lc_make_int2(lhs.x - rhs.x, lhs.y - rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator-(lc_int2 lhs, lc_int rhs) noexcept { return lc_make_int2(lhs.x - rhs, lhs.y - rhs); }
[[nodiscard]] inline __device__ constexpr auto operator-(lc_int lhs, lc_int2 rhs) noexcept { return lc_make_int2(lhs - rhs.x, lhs - rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator-(lc_int3 lhs, lc_int3 rhs) noexcept { return lc_make_int3(lhs.x - rhs.x, lhs.y - rhs.y, lhs.z - rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator-(lc_int3 lhs, lc_int rhs) noexcept { return lc_make_int3(lhs.x - rhs, lhs.y - rhs, lhs.z - rhs); }
[[nodiscard]] inline __device__ constexpr auto operator-(lc_int lhs, lc_int3 rhs) noexcept { return lc_make_int3(lhs - rhs.x, lhs - rhs.y, lhs - rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator-(lc_int4 lhs, lc_int4 rhs) noexcept { return lc_make_int4(lhs.x - rhs.x, lhs.y - rhs.y, lhs.z - rhs.z, lhs.w - rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator-(lc_int4 lhs, lc_int rhs) noexcept { return lc_make_int4(lhs.x - rhs, lhs.y - rhs, lhs.z - rhs, lhs.w - rhs); }
[[nodiscard]] inline __device__ constexpr auto operator-(lc_int lhs, lc_int4 rhs) noexcept { return lc_make_int4(lhs - rhs.x, lhs - rhs.y, lhs - rhs.z, lhs - rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator-(lc_uint2 lhs, lc_uint2 rhs) noexcept { return lc_make_uint2(lhs.x - rhs.x, lhs.y - rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator-(lc_uint2 lhs, lc_uint rhs) noexcept { return lc_make_uint2(lhs.x - rhs, lhs.y - rhs); }
[[nodiscard]] inline __device__ constexpr auto operator-(lc_uint lhs, lc_uint2 rhs) noexcept { return lc_make_uint2(lhs - rhs.x, lhs - rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator-(lc_uint3 lhs, lc_uint3 rhs) noexcept { return lc_make_uint3(lhs.x - rhs.x, lhs.y - rhs.y, lhs.z - rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator-(lc_uint3 lhs, lc_uint rhs) noexcept { return lc_make_uint3(lhs.x - rhs, lhs.y - rhs, lhs.z - rhs); }
[[nodiscard]] inline __device__ constexpr auto operator-(lc_uint lhs, lc_uint3 rhs) noexcept { return lc_make_uint3(lhs - rhs.x, lhs - rhs.y, lhs - rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator-(lc_uint4 lhs, lc_uint4 rhs) noexcept { return lc_make_uint4(lhs.x - rhs.x, lhs.y - rhs.y, lhs.z - rhs.z, lhs.w - rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator-(lc_uint4 lhs, lc_uint rhs) noexcept { return lc_make_uint4(lhs.x - rhs, lhs.y - rhs, lhs.z - rhs, lhs.w - rhs); }
[[nodiscard]] inline __device__ constexpr auto operator-(lc_uint lhs, lc_uint4 rhs) noexcept { return lc_make_uint4(lhs - rhs.x, lhs - rhs.y, lhs - rhs.z, lhs - rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator-(lc_half2 lhs, lc_half2 rhs) noexcept { return lc_make_half2(lhs.x - rhs.x, lhs.y - rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator-(lc_half2 lhs, lc_half rhs) noexcept { return lc_make_half2(lhs.x - rhs, lhs.y - rhs); }
[[nodiscard]] inline __device__ constexpr auto operator-(lc_half lhs, lc_half2 rhs) noexcept { return lc_make_half2(lhs - rhs.x, lhs - rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator-(lc_half3 lhs, lc_half3 rhs) noexcept { return lc_make_half3(lhs.x - rhs.x, lhs.y - rhs.y, lhs.z - rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator-(lc_half3 lhs, lc_half rhs) noexcept { return lc_make_half3(lhs.x - rhs, lhs.y - rhs, lhs.z - rhs); }
[[nodiscard]] inline __device__ constexpr auto operator-(lc_half lhs, lc_half3 rhs) noexcept { return lc_make_half3(lhs - rhs.x, lhs - rhs.y, lhs - rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator-(lc_half4 lhs, lc_half4 rhs) noexcept { return lc_make_half4(lhs.x - rhs.x, lhs.y - rhs.y, lhs.z - rhs.z, lhs.w - rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator-(lc_half4 lhs, lc_half rhs) noexcept { return lc_make_half4(lhs.x - rhs, lhs.y - rhs, lhs.z - rhs, lhs.w - rhs); }
[[nodiscard]] inline __device__ constexpr auto operator-(lc_half lhs, lc_half4 rhs) noexcept { return lc_make_half4(lhs - rhs.x, lhs - rhs.y, lhs - rhs.z, lhs - rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator-(lc_float2 lhs, lc_float2 rhs) noexcept { return lc_make_float2(lhs.x - rhs.x, lhs.y - rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator-(lc_float2 lhs, lc_float rhs) noexcept { return lc_make_float2(lhs.x - rhs, lhs.y - rhs); }
[[nodiscard]] inline __device__ constexpr auto operator-(lc_float lhs, lc_float2 rhs) noexcept { return lc_make_float2(lhs - rhs.x, lhs - rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator-(lc_float3 lhs, lc_float3 rhs) noexcept { return lc_make_float3(lhs.x - rhs.x, lhs.y - rhs.y, lhs.z - rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator-(lc_float3 lhs, lc_float rhs) noexcept { return lc_make_float3(lhs.x - rhs, lhs.y - rhs, lhs.z - rhs); }
[[nodiscard]] inline __device__ constexpr auto operator-(lc_float lhs, lc_float3 rhs) noexcept { return lc_make_float3(lhs - rhs.x, lhs - rhs.y, lhs - rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator-(lc_float4 lhs, lc_float4 rhs) noexcept { return lc_make_float4(lhs.x - rhs.x, lhs.y - rhs.y, lhs.z - rhs.z, lhs.w - rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator-(lc_float4 lhs, lc_float rhs) noexcept { return lc_make_float4(lhs.x - rhs, lhs.y - rhs, lhs.z - rhs, lhs.w - rhs); }
[[nodiscard]] inline __device__ constexpr auto operator-(lc_float lhs, lc_float4 rhs) noexcept { return lc_make_float4(lhs - rhs.x, lhs - rhs.y, lhs - rhs.z, lhs - rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator-(lc_long2 lhs, lc_long2 rhs) noexcept { return lc_make_long2(lhs.x - rhs.x, lhs.y - rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator-(lc_long2 lhs, lc_long rhs) noexcept { return lc_make_long2(lhs.x - rhs, lhs.y - rhs); }
[[nodiscard]] inline __device__ constexpr auto operator-(lc_long lhs, lc_long2 rhs) noexcept { return lc_make_long2(lhs - rhs.x, lhs - rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator-(lc_long3 lhs, lc_long3 rhs) noexcept { return lc_make_long3(lhs.x - rhs.x, lhs.y - rhs.y, lhs.z - rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator-(lc_long3 lhs, lc_long rhs) noexcept { return lc_make_long3(lhs.x - rhs, lhs.y - rhs, lhs.z - rhs); }
[[nodiscard]] inline __device__ constexpr auto operator-(lc_long lhs, lc_long3 rhs) noexcept { return lc_make_long3(lhs - rhs.x, lhs - rhs.y, lhs - rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator-(lc_long4 lhs, lc_long4 rhs) noexcept { return lc_make_long4(lhs.x - rhs.x, lhs.y - rhs.y, lhs.z - rhs.z, lhs.w - rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator-(lc_long4 lhs, lc_long rhs) noexcept { return lc_make_long4(lhs.x - rhs, lhs.y - rhs, lhs.z - rhs, lhs.w - rhs); }
[[nodiscard]] inline __device__ constexpr auto operator-(lc_long lhs, lc_long4 rhs) noexcept { return lc_make_long4(lhs - rhs.x, lhs - rhs.y, lhs - rhs.z, lhs - rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator-(lc_ulong2 lhs, lc_ulong2 rhs) noexcept { return lc_make_ulong2(lhs.x - rhs.x, lhs.y - rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator-(lc_ulong2 lhs, lc_ulong rhs) noexcept { return lc_make_ulong2(lhs.x - rhs, lhs.y - rhs); }
[[nodiscard]] inline __device__ constexpr auto operator-(lc_ulong lhs, lc_ulong2 rhs) noexcept { return lc_make_ulong2(lhs - rhs.x, lhs - rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator-(lc_ulong3 lhs, lc_ulong3 rhs) noexcept { return lc_make_ulong3(lhs.x - rhs.x, lhs.y - rhs.y, lhs.z - rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator-(lc_ulong3 lhs, lc_ulong rhs) noexcept { return lc_make_ulong3(lhs.x - rhs, lhs.y - rhs, lhs.z - rhs); }
[[nodiscard]] inline __device__ constexpr auto operator-(lc_ulong lhs, lc_ulong3 rhs) noexcept { return lc_make_ulong3(lhs - rhs.x, lhs - rhs.y, lhs - rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator-(lc_ulong4 lhs, lc_ulong4 rhs) noexcept { return lc_make_ulong4(lhs.x - rhs.x, lhs.y - rhs.y, lhs.z - rhs.z, lhs.w - rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator-(lc_ulong4 lhs, lc_ulong rhs) noexcept { return lc_make_ulong4(lhs.x - rhs, lhs.y - rhs, lhs.z - rhs, lhs.w - rhs); }
[[nodiscard]] inline __device__ constexpr auto operator-(lc_ulong lhs, lc_ulong4 rhs) noexcept { return lc_make_ulong4(lhs - rhs.x, lhs - rhs.y, lhs - rhs.z, lhs - rhs.w); }

[[nodiscard]] inline __device__ constexpr auto operator*(lc_short2 lhs, lc_short2 rhs) noexcept { return lc_make_short2(lhs.x * rhs.x, lhs.y * rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator*(lc_short2 lhs, lc_short rhs) noexcept { return lc_make_short2(lhs.x * rhs, lhs.y * rhs); }
[[nodiscard]] inline __device__ constexpr auto operator*(lc_short lhs, lc_short2 rhs) noexcept { return lc_make_short2(lhs * rhs.x, lhs * rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator*(lc_short3 lhs, lc_short3 rhs) noexcept { return lc_make_short3(lhs.x * rhs.x, lhs.y * rhs.y, lhs.z * rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator*(lc_short3 lhs, lc_short rhs) noexcept { return lc_make_short3(lhs.x * rhs, lhs.y * rhs, lhs.z * rhs); }
[[nodiscard]] inline __device__ constexpr auto operator*(lc_short lhs, lc_short3 rhs) noexcept { return lc_make_short3(lhs * rhs.x, lhs * rhs.y, lhs * rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator*(lc_short4 lhs, lc_short4 rhs) noexcept { return lc_make_short4(lhs.x * rhs.x, lhs.y * rhs.y, lhs.z * rhs.z, lhs.w * rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator*(lc_short4 lhs, lc_short rhs) noexcept { return lc_make_short4(lhs.x * rhs, lhs.y * rhs, lhs.z * rhs, lhs.w * rhs); }
[[nodiscard]] inline __device__ constexpr auto operator*(lc_short lhs, lc_short4 rhs) noexcept { return lc_make_short4(lhs * rhs.x, lhs * rhs.y, lhs * rhs.z, lhs * rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator*(lc_ushort2 lhs, lc_ushort2 rhs) noexcept { return lc_make_ushort2(lhs.x * rhs.x, lhs.y * rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator*(lc_ushort2 lhs, lc_ushort rhs) noexcept { return lc_make_ushort2(lhs.x * rhs, lhs.y * rhs); }
[[nodiscard]] inline __device__ constexpr auto operator*(lc_ushort lhs, lc_ushort2 rhs) noexcept { return lc_make_ushort2(lhs * rhs.x, lhs * rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator*(lc_ushort3 lhs, lc_ushort3 rhs) noexcept { return lc_make_ushort3(lhs.x * rhs.x, lhs.y * rhs.y, lhs.z * rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator*(lc_ushort3 lhs, lc_ushort rhs) noexcept { return lc_make_ushort3(lhs.x * rhs, lhs.y * rhs, lhs.z * rhs); }
[[nodiscard]] inline __device__ constexpr auto operator*(lc_ushort lhs, lc_ushort3 rhs) noexcept { return lc_make_ushort3(lhs * rhs.x, lhs * rhs.y, lhs * rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator*(lc_ushort4 lhs, lc_ushort4 rhs) noexcept { return lc_make_ushort4(lhs.x * rhs.x, lhs.y * rhs.y, lhs.z * rhs.z, lhs.w * rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator*(lc_ushort4 lhs, lc_ushort rhs) noexcept { return lc_make_ushort4(lhs.x * rhs, lhs.y * rhs, lhs.z * rhs, lhs.w * rhs); }
[[nodiscard]] inline __device__ constexpr auto operator*(lc_ushort lhs, lc_ushort4 rhs) noexcept { return lc_make_ushort4(lhs * rhs.x, lhs * rhs.y, lhs * rhs.z, lhs * rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator*(lc_int2 lhs, lc_int2 rhs) noexcept { return lc_make_int2(lhs.x * rhs.x, lhs.y * rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator*(lc_int2 lhs, lc_int rhs) noexcept { return lc_make_int2(lhs.x * rhs, lhs.y * rhs); }
[[nodiscard]] inline __device__ constexpr auto operator*(lc_int lhs, lc_int2 rhs) noexcept { return lc_make_int2(lhs * rhs.x, lhs * rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator*(lc_int3 lhs, lc_int3 rhs) noexcept { return lc_make_int3(lhs.x * rhs.x, lhs.y * rhs.y, lhs.z * rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator*(lc_int3 lhs, lc_int rhs) noexcept { return lc_make_int3(lhs.x * rhs, lhs.y * rhs, lhs.z * rhs); }
[[nodiscard]] inline __device__ constexpr auto operator*(lc_int lhs, lc_int3 rhs) noexcept { return lc_make_int3(lhs * rhs.x, lhs * rhs.y, lhs * rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator*(lc_int4 lhs, lc_int4 rhs) noexcept { return lc_make_int4(lhs.x * rhs.x, lhs.y * rhs.y, lhs.z * rhs.z, lhs.w * rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator*(lc_int4 lhs, lc_int rhs) noexcept { return lc_make_int4(lhs.x * rhs, lhs.y * rhs, lhs.z * rhs, lhs.w * rhs); }
[[nodiscard]] inline __device__ constexpr auto operator*(lc_int lhs, lc_int4 rhs) noexcept { return lc_make_int4(lhs * rhs.x, lhs * rhs.y, lhs * rhs.z, lhs * rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator*(lc_uint2 lhs, lc_uint2 rhs) noexcept { return lc_make_uint2(lhs.x * rhs.x, lhs.y * rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator*(lc_uint2 lhs, lc_uint rhs) noexcept { return lc_make_uint2(lhs.x * rhs, lhs.y * rhs); }
[[nodiscard]] inline __device__ constexpr auto operator*(lc_uint lhs, lc_uint2 rhs) noexcept { return lc_make_uint2(lhs * rhs.x, lhs * rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator*(lc_uint3 lhs, lc_uint3 rhs) noexcept { return lc_make_uint3(lhs.x * rhs.x, lhs.y * rhs.y, lhs.z * rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator*(lc_uint3 lhs, lc_uint rhs) noexcept { return lc_make_uint3(lhs.x * rhs, lhs.y * rhs, lhs.z * rhs); }
[[nodiscard]] inline __device__ constexpr auto operator*(lc_uint lhs, lc_uint3 rhs) noexcept { return lc_make_uint3(lhs * rhs.x, lhs * rhs.y, lhs * rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator*(lc_uint4 lhs, lc_uint4 rhs) noexcept { return lc_make_uint4(lhs.x * rhs.x, lhs.y * rhs.y, lhs.z * rhs.z, lhs.w * rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator*(lc_uint4 lhs, lc_uint rhs) noexcept { return lc_make_uint4(lhs.x * rhs, lhs.y * rhs, lhs.z * rhs, lhs.w * rhs); }
[[nodiscard]] inline __device__ constexpr auto operator*(lc_uint lhs, lc_uint4 rhs) noexcept { return lc_make_uint4(lhs * rhs.x, lhs * rhs.y, lhs * rhs.z, lhs * rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator*(lc_half2 lhs, lc_half2 rhs) noexcept { return lc_make_half2(lhs.x * rhs.x, lhs.y * rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator*(lc_half2 lhs, lc_half rhs) noexcept { return lc_make_half2(lhs.x * rhs, lhs.y * rhs); }
[[nodiscard]] inline __device__ constexpr auto operator*(lc_half lhs, lc_half2 rhs) noexcept { return lc_make_half2(lhs * rhs.x, lhs * rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator*(lc_half3 lhs, lc_half3 rhs) noexcept { return lc_make_half3(lhs.x * rhs.x, lhs.y * rhs.y, lhs.z * rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator*(lc_half3 lhs, lc_half rhs) noexcept { return lc_make_half3(lhs.x * rhs, lhs.y * rhs, lhs.z * rhs); }
[[nodiscard]] inline __device__ constexpr auto operator*(lc_half lhs, lc_half3 rhs) noexcept { return lc_make_half3(lhs * rhs.x, lhs * rhs.y, lhs * rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator*(lc_half4 lhs, lc_half4 rhs) noexcept { return lc_make_half4(lhs.x * rhs.x, lhs.y * rhs.y, lhs.z * rhs.z, lhs.w * rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator*(lc_half4 lhs, lc_half rhs) noexcept { return lc_make_half4(lhs.x * rhs, lhs.y * rhs, lhs.z * rhs, lhs.w * rhs); }
[[nodiscard]] inline __device__ constexpr auto operator*(lc_half lhs, lc_half4 rhs) noexcept { return lc_make_half4(lhs * rhs.x, lhs * rhs.y, lhs * rhs.z, lhs * rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator*(lc_float2 lhs, lc_float2 rhs) noexcept { return lc_make_float2(lhs.x * rhs.x, lhs.y * rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator*(lc_float2 lhs, lc_float rhs) noexcept { return lc_make_float2(lhs.x * rhs, lhs.y * rhs); }
[[nodiscard]] inline __device__ constexpr auto operator*(lc_float lhs, lc_float2 rhs) noexcept { return lc_make_float2(lhs * rhs.x, lhs * rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator*(lc_float3 lhs, lc_float3 rhs) noexcept { return lc_make_float3(lhs.x * rhs.x, lhs.y * rhs.y, lhs.z * rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator*(lc_float3 lhs, lc_float rhs) noexcept { return lc_make_float3(lhs.x * rhs, lhs.y * rhs, lhs.z * rhs); }
[[nodiscard]] inline __device__ constexpr auto operator*(lc_float lhs, lc_float3 rhs) noexcept { return lc_make_float3(lhs * rhs.x, lhs * rhs.y, lhs * rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator*(lc_float4 lhs, lc_float4 rhs) noexcept { return lc_make_float4(lhs.x * rhs.x, lhs.y * rhs.y, lhs.z * rhs.z, lhs.w * rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator*(lc_float4 lhs, lc_float rhs) noexcept { return lc_make_float4(lhs.x * rhs, lhs.y * rhs, lhs.z * rhs, lhs.w * rhs); }
[[nodiscard]] inline __device__ constexpr auto operator*(lc_float lhs, lc_float4 rhs) noexcept { return lc_make_float4(lhs * rhs.x, lhs * rhs.y, lhs * rhs.z, lhs * rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator*(lc_long2 lhs, lc_long2 rhs) noexcept { return lc_make_long2(lhs.x * rhs.x, lhs.y * rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator*(lc_long2 lhs, lc_long rhs) noexcept { return lc_make_long2(lhs.x * rhs, lhs.y * rhs); }
[[nodiscard]] inline __device__ constexpr auto operator*(lc_long lhs, lc_long2 rhs) noexcept { return lc_make_long2(lhs * rhs.x, lhs * rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator*(lc_long3 lhs, lc_long3 rhs) noexcept { return lc_make_long3(lhs.x * rhs.x, lhs.y * rhs.y, lhs.z * rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator*(lc_long3 lhs, lc_long rhs) noexcept { return lc_make_long3(lhs.x * rhs, lhs.y * rhs, lhs.z * rhs); }
[[nodiscard]] inline __device__ constexpr auto operator*(lc_long lhs, lc_long3 rhs) noexcept { return lc_make_long3(lhs * rhs.x, lhs * rhs.y, lhs * rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator*(lc_long4 lhs, lc_long4 rhs) noexcept { return lc_make_long4(lhs.x * rhs.x, lhs.y * rhs.y, lhs.z * rhs.z, lhs.w * rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator*(lc_long4 lhs, lc_long rhs) noexcept { return lc_make_long4(lhs.x * rhs, lhs.y * rhs, lhs.z * rhs, lhs.w * rhs); }
[[nodiscard]] inline __device__ constexpr auto operator*(lc_long lhs, lc_long4 rhs) noexcept { return lc_make_long4(lhs * rhs.x, lhs * rhs.y, lhs * rhs.z, lhs * rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator*(lc_ulong2 lhs, lc_ulong2 rhs) noexcept { return lc_make_ulong2(lhs.x * rhs.x, lhs.y * rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator*(lc_ulong2 lhs, lc_ulong rhs) noexcept { return lc_make_ulong2(lhs.x * rhs, lhs.y * rhs); }
[[nodiscard]] inline __device__ constexpr auto operator*(lc_ulong lhs, lc_ulong2 rhs) noexcept { return lc_make_ulong2(lhs * rhs.x, lhs * rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator*(lc_ulong3 lhs, lc_ulong3 rhs) noexcept { return lc_make_ulong3(lhs.x * rhs.x, lhs.y * rhs.y, lhs.z * rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator*(lc_ulong3 lhs, lc_ulong rhs) noexcept { return lc_make_ulong3(lhs.x * rhs, lhs.y * rhs, lhs.z * rhs); }
[[nodiscard]] inline __device__ constexpr auto operator*(lc_ulong lhs, lc_ulong3 rhs) noexcept { return lc_make_ulong3(lhs * rhs.x, lhs * rhs.y, lhs * rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator*(lc_ulong4 lhs, lc_ulong4 rhs) noexcept { return lc_make_ulong4(lhs.x * rhs.x, lhs.y * rhs.y, lhs.z * rhs.z, lhs.w * rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator*(lc_ulong4 lhs, lc_ulong rhs) noexcept { return lc_make_ulong4(lhs.x * rhs, lhs.y * rhs, lhs.z * rhs, lhs.w * rhs); }
[[nodiscard]] inline __device__ constexpr auto operator*(lc_ulong lhs, lc_ulong4 rhs) noexcept { return lc_make_ulong4(lhs * rhs.x, lhs * rhs.y, lhs * rhs.z, lhs * rhs.w); }

[[nodiscard]] inline __device__ constexpr auto operator/(lc_short2 lhs, lc_short2 rhs) noexcept { return lc_make_short2(lhs.x / rhs.x, lhs.y / rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator/(lc_short2 lhs, lc_short rhs) noexcept { return lc_make_short2(lhs.x / rhs, lhs.y / rhs); }
[[nodiscard]] inline __device__ constexpr auto operator/(lc_short lhs, lc_short2 rhs) noexcept { return lc_make_short2(lhs / rhs.x, lhs / rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator/(lc_short3 lhs, lc_short3 rhs) noexcept { return lc_make_short3(lhs.x / rhs.x, lhs.y / rhs.y, lhs.z / rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator/(lc_short3 lhs, lc_short rhs) noexcept { return lc_make_short3(lhs.x / rhs, lhs.y / rhs, lhs.z / rhs); }
[[nodiscard]] inline __device__ constexpr auto operator/(lc_short lhs, lc_short3 rhs) noexcept { return lc_make_short3(lhs / rhs.x, lhs / rhs.y, lhs / rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator/(lc_short4 lhs, lc_short4 rhs) noexcept { return lc_make_short4(lhs.x / rhs.x, lhs.y / rhs.y, lhs.z / rhs.z, lhs.w / rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator/(lc_short4 lhs, lc_short rhs) noexcept { return lc_make_short4(lhs.x / rhs, lhs.y / rhs, lhs.z / rhs, lhs.w / rhs); }
[[nodiscard]] inline __device__ constexpr auto operator/(lc_short lhs, lc_short4 rhs) noexcept { return lc_make_short4(lhs / rhs.x, lhs / rhs.y, lhs / rhs.z, lhs / rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator/(lc_ushort2 lhs, lc_ushort2 rhs) noexcept { return lc_make_ushort2(lhs.x / rhs.x, lhs.y / rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator/(lc_ushort2 lhs, lc_ushort rhs) noexcept { return lc_make_ushort2(lhs.x / rhs, lhs.y / rhs); }
[[nodiscard]] inline __device__ constexpr auto operator/(lc_ushort lhs, lc_ushort2 rhs) noexcept { return lc_make_ushort2(lhs / rhs.x, lhs / rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator/(lc_ushort3 lhs, lc_ushort3 rhs) noexcept { return lc_make_ushort3(lhs.x / rhs.x, lhs.y / rhs.y, lhs.z / rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator/(lc_ushort3 lhs, lc_ushort rhs) noexcept { return lc_make_ushort3(lhs.x / rhs, lhs.y / rhs, lhs.z / rhs); }
[[nodiscard]] inline __device__ constexpr auto operator/(lc_ushort lhs, lc_ushort3 rhs) noexcept { return lc_make_ushort3(lhs / rhs.x, lhs / rhs.y, lhs / rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator/(lc_ushort4 lhs, lc_ushort4 rhs) noexcept { return lc_make_ushort4(lhs.x / rhs.x, lhs.y / rhs.y, lhs.z / rhs.z, lhs.w / rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator/(lc_ushort4 lhs, lc_ushort rhs) noexcept { return lc_make_ushort4(lhs.x / rhs, lhs.y / rhs, lhs.z / rhs, lhs.w / rhs); }
[[nodiscard]] inline __device__ constexpr auto operator/(lc_ushort lhs, lc_ushort4 rhs) noexcept { return lc_make_ushort4(lhs / rhs.x, lhs / rhs.y, lhs / rhs.z, lhs / rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator/(lc_int2 lhs, lc_int2 rhs) noexcept { return lc_make_int2(lhs.x / rhs.x, lhs.y / rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator/(lc_int2 lhs, lc_int rhs) noexcept { return lc_make_int2(lhs.x / rhs, lhs.y / rhs); }
[[nodiscard]] inline __device__ constexpr auto operator/(lc_int lhs, lc_int2 rhs) noexcept { return lc_make_int2(lhs / rhs.x, lhs / rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator/(lc_int3 lhs, lc_int3 rhs) noexcept { return lc_make_int3(lhs.x / rhs.x, lhs.y / rhs.y, lhs.z / rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator/(lc_int3 lhs, lc_int rhs) noexcept { return lc_make_int3(lhs.x / rhs, lhs.y / rhs, lhs.z / rhs); }
[[nodiscard]] inline __device__ constexpr auto operator/(lc_int lhs, lc_int3 rhs) noexcept { return lc_make_int3(lhs / rhs.x, lhs / rhs.y, lhs / rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator/(lc_int4 lhs, lc_int4 rhs) noexcept { return lc_make_int4(lhs.x / rhs.x, lhs.y / rhs.y, lhs.z / rhs.z, lhs.w / rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator/(lc_int4 lhs, lc_int rhs) noexcept { return lc_make_int4(lhs.x / rhs, lhs.y / rhs, lhs.z / rhs, lhs.w / rhs); }
[[nodiscard]] inline __device__ constexpr auto operator/(lc_int lhs, lc_int4 rhs) noexcept { return lc_make_int4(lhs / rhs.x, lhs / rhs.y, lhs / rhs.z, lhs / rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator/(lc_uint2 lhs, lc_uint2 rhs) noexcept { return lc_make_uint2(lhs.x / rhs.x, lhs.y / rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator/(lc_uint2 lhs, lc_uint rhs) noexcept { return lc_make_uint2(lhs.x / rhs, lhs.y / rhs); }
[[nodiscard]] inline __device__ constexpr auto operator/(lc_uint lhs, lc_uint2 rhs) noexcept { return lc_make_uint2(lhs / rhs.x, lhs / rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator/(lc_uint3 lhs, lc_uint3 rhs) noexcept { return lc_make_uint3(lhs.x / rhs.x, lhs.y / rhs.y, lhs.z / rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator/(lc_uint3 lhs, lc_uint rhs) noexcept { return lc_make_uint3(lhs.x / rhs, lhs.y / rhs, lhs.z / rhs); }
[[nodiscard]] inline __device__ constexpr auto operator/(lc_uint lhs, lc_uint3 rhs) noexcept { return lc_make_uint3(lhs / rhs.x, lhs / rhs.y, lhs / rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator/(lc_uint4 lhs, lc_uint4 rhs) noexcept { return lc_make_uint4(lhs.x / rhs.x, lhs.y / rhs.y, lhs.z / rhs.z, lhs.w / rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator/(lc_uint4 lhs, lc_uint rhs) noexcept { return lc_make_uint4(lhs.x / rhs, lhs.y / rhs, lhs.z / rhs, lhs.w / rhs); }
[[nodiscard]] inline __device__ constexpr auto operator/(lc_uint lhs, lc_uint4 rhs) noexcept { return lc_make_uint4(lhs / rhs.x, lhs / rhs.y, lhs / rhs.z, lhs / rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator/(lc_half2 lhs, lc_half2 rhs) noexcept { return lc_make_half2(lhs.x / rhs.x, lhs.y / rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator/(lc_half2 lhs, lc_half rhs) noexcept { return lc_make_half2(lhs.x / rhs, lhs.y / rhs); }
[[nodiscard]] inline __device__ constexpr auto operator/(lc_half lhs, lc_half2 rhs) noexcept { return lc_make_half2(lhs / rhs.x, lhs / rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator/(lc_half3 lhs, lc_half3 rhs) noexcept { return lc_make_half3(lhs.x / rhs.x, lhs.y / rhs.y, lhs.z / rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator/(lc_half3 lhs, lc_half rhs) noexcept { return lc_make_half3(lhs.x / rhs, lhs.y / rhs, lhs.z / rhs); }
[[nodiscard]] inline __device__ constexpr auto operator/(lc_half lhs, lc_half3 rhs) noexcept { return lc_make_half3(lhs / rhs.x, lhs / rhs.y, lhs / rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator/(lc_half4 lhs, lc_half4 rhs) noexcept { return lc_make_half4(lhs.x / rhs.x, lhs.y / rhs.y, lhs.z / rhs.z, lhs.w / rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator/(lc_half4 lhs, lc_half rhs) noexcept { return lc_make_half4(lhs.x / rhs, lhs.y / rhs, lhs.z / rhs, lhs.w / rhs); }
[[nodiscard]] inline __device__ constexpr auto operator/(lc_half lhs, lc_half4 rhs) noexcept { return lc_make_half4(lhs / rhs.x, lhs / rhs.y, lhs / rhs.z, lhs / rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator/(lc_float2 lhs, lc_float2 rhs) noexcept { return lc_make_float2(lhs.x / rhs.x, lhs.y / rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator/(lc_float2 lhs, lc_float rhs) noexcept { return lc_make_float2(lhs.x / rhs, lhs.y / rhs); }
[[nodiscard]] inline __device__ constexpr auto operator/(lc_float lhs, lc_float2 rhs) noexcept { return lc_make_float2(lhs / rhs.x, lhs / rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator/(lc_float3 lhs, lc_float3 rhs) noexcept { return lc_make_float3(lhs.x / rhs.x, lhs.y / rhs.y, lhs.z / rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator/(lc_float3 lhs, lc_float rhs) noexcept { return lc_make_float3(lhs.x / rhs, lhs.y / rhs, lhs.z / rhs); }
[[nodiscard]] inline __device__ constexpr auto operator/(lc_float lhs, lc_float3 rhs) noexcept { return lc_make_float3(lhs / rhs.x, lhs / rhs.y, lhs / rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator/(lc_float4 lhs, lc_float4 rhs) noexcept { return lc_make_float4(lhs.x / rhs.x, lhs.y / rhs.y, lhs.z / rhs.z, lhs.w / rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator/(lc_float4 lhs, lc_float rhs) noexcept { return lc_make_float4(lhs.x / rhs, lhs.y / rhs, lhs.z / rhs, lhs.w / rhs); }
[[nodiscard]] inline __device__ constexpr auto operator/(lc_float lhs, lc_float4 rhs) noexcept { return lc_make_float4(lhs / rhs.x, lhs / rhs.y, lhs / rhs.z, lhs / rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator/(lc_long2 lhs, lc_long2 rhs) noexcept { return lc_make_long2(lhs.x / rhs.x, lhs.y / rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator/(lc_long2 lhs, lc_long rhs) noexcept { return lc_make_long2(lhs.x / rhs, lhs.y / rhs); }
[[nodiscard]] inline __device__ constexpr auto operator/(lc_long lhs, lc_long2 rhs) noexcept { return lc_make_long2(lhs / rhs.x, lhs / rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator/(lc_long3 lhs, lc_long3 rhs) noexcept { return lc_make_long3(lhs.x / rhs.x, lhs.y / rhs.y, lhs.z / rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator/(lc_long3 lhs, lc_long rhs) noexcept { return lc_make_long3(lhs.x / rhs, lhs.y / rhs, lhs.z / rhs); }
[[nodiscard]] inline __device__ constexpr auto operator/(lc_long lhs, lc_long3 rhs) noexcept { return lc_make_long3(lhs / rhs.x, lhs / rhs.y, lhs / rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator/(lc_long4 lhs, lc_long4 rhs) noexcept { return lc_make_long4(lhs.x / rhs.x, lhs.y / rhs.y, lhs.z / rhs.z, lhs.w / rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator/(lc_long4 lhs, lc_long rhs) noexcept { return lc_make_long4(lhs.x / rhs, lhs.y / rhs, lhs.z / rhs, lhs.w / rhs); }
[[nodiscard]] inline __device__ constexpr auto operator/(lc_long lhs, lc_long4 rhs) noexcept { return lc_make_long4(lhs / rhs.x, lhs / rhs.y, lhs / rhs.z, lhs / rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator/(lc_ulong2 lhs, lc_ulong2 rhs) noexcept { return lc_make_ulong2(lhs.x / rhs.x, lhs.y / rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator/(lc_ulong2 lhs, lc_ulong rhs) noexcept { return lc_make_ulong2(lhs.x / rhs, lhs.y / rhs); }
[[nodiscard]] inline __device__ constexpr auto operator/(lc_ulong lhs, lc_ulong2 rhs) noexcept { return lc_make_ulong2(lhs / rhs.x, lhs / rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator/(lc_ulong3 lhs, lc_ulong3 rhs) noexcept { return lc_make_ulong3(lhs.x / rhs.x, lhs.y / rhs.y, lhs.z / rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator/(lc_ulong3 lhs, lc_ulong rhs) noexcept { return lc_make_ulong3(lhs.x / rhs, lhs.y / rhs, lhs.z / rhs); }
[[nodiscard]] inline __device__ constexpr auto operator/(lc_ulong lhs, lc_ulong3 rhs) noexcept { return lc_make_ulong3(lhs / rhs.x, lhs / rhs.y, lhs / rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator/(lc_ulong4 lhs, lc_ulong4 rhs) noexcept { return lc_make_ulong4(lhs.x / rhs.x, lhs.y / rhs.y, lhs.z / rhs.z, lhs.w / rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator/(lc_ulong4 lhs, lc_ulong rhs) noexcept { return lc_make_ulong4(lhs.x / rhs, lhs.y / rhs, lhs.z / rhs, lhs.w / rhs); }
[[nodiscard]] inline __device__ constexpr auto operator/(lc_ulong lhs, lc_ulong4 rhs) noexcept { return lc_make_ulong4(lhs / rhs.x, lhs / rhs.y, lhs / rhs.z, lhs / rhs.w); }

[[nodiscard]] inline __device__ constexpr auto operator%(lc_short2 lhs, lc_short2 rhs) noexcept { return lc_make_short2(lhs.x % rhs.x, lhs.y % rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator%(lc_short2 lhs, lc_short rhs) noexcept { return lc_make_short2(lhs.x % rhs, lhs.y % rhs); }
[[nodiscard]] inline __device__ constexpr auto operator%(lc_short lhs, lc_short2 rhs) noexcept { return lc_make_short2(lhs % rhs.x, lhs % rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator%(lc_short3 lhs, lc_short3 rhs) noexcept { return lc_make_short3(lhs.x % rhs.x, lhs.y % rhs.y, lhs.z % rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator%(lc_short3 lhs, lc_short rhs) noexcept { return lc_make_short3(lhs.x % rhs, lhs.y % rhs, lhs.z % rhs); }
[[nodiscard]] inline __device__ constexpr auto operator%(lc_short lhs, lc_short3 rhs) noexcept { return lc_make_short3(lhs % rhs.x, lhs % rhs.y, lhs % rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator%(lc_short4 lhs, lc_short4 rhs) noexcept { return lc_make_short4(lhs.x % rhs.x, lhs.y % rhs.y, lhs.z % rhs.z, lhs.w % rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator%(lc_short4 lhs, lc_short rhs) noexcept { return lc_make_short4(lhs.x % rhs, lhs.y % rhs, lhs.z % rhs, lhs.w % rhs); }
[[nodiscard]] inline __device__ constexpr auto operator%(lc_short lhs, lc_short4 rhs) noexcept { return lc_make_short4(lhs % rhs.x, lhs % rhs.y, lhs % rhs.z, lhs % rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator%(lc_ushort2 lhs, lc_ushort2 rhs) noexcept { return lc_make_ushort2(lhs.x % rhs.x, lhs.y % rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator%(lc_ushort2 lhs, lc_ushort rhs) noexcept { return lc_make_ushort2(lhs.x % rhs, lhs.y % rhs); }
[[nodiscard]] inline __device__ constexpr auto operator%(lc_ushort lhs, lc_ushort2 rhs) noexcept { return lc_make_ushort2(lhs % rhs.x, lhs % rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator%(lc_ushort3 lhs, lc_ushort3 rhs) noexcept { return lc_make_ushort3(lhs.x % rhs.x, lhs.y % rhs.y, lhs.z % rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator%(lc_ushort3 lhs, lc_ushort rhs) noexcept { return lc_make_ushort3(lhs.x % rhs, lhs.y % rhs, lhs.z % rhs); }
[[nodiscard]] inline __device__ constexpr auto operator%(lc_ushort lhs, lc_ushort3 rhs) noexcept { return lc_make_ushort3(lhs % rhs.x, lhs % rhs.y, lhs % rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator%(lc_ushort4 lhs, lc_ushort4 rhs) noexcept { return lc_make_ushort4(lhs.x % rhs.x, lhs.y % rhs.y, lhs.z % rhs.z, lhs.w % rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator%(lc_ushort4 lhs, lc_ushort rhs) noexcept { return lc_make_ushort4(lhs.x % rhs, lhs.y % rhs, lhs.z % rhs, lhs.w % rhs); }
[[nodiscard]] inline __device__ constexpr auto operator%(lc_ushort lhs, lc_ushort4 rhs) noexcept { return lc_make_ushort4(lhs % rhs.x, lhs % rhs.y, lhs % rhs.z, lhs % rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator%(lc_int2 lhs, lc_int2 rhs) noexcept { return lc_make_int2(lhs.x % rhs.x, lhs.y % rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator%(lc_int2 lhs, lc_int rhs) noexcept { return lc_make_int2(lhs.x % rhs, lhs.y % rhs); }
[[nodiscard]] inline __device__ constexpr auto operator%(lc_int lhs, lc_int2 rhs) noexcept { return lc_make_int2(lhs % rhs.x, lhs % rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator%(lc_int3 lhs, lc_int3 rhs) noexcept { return lc_make_int3(lhs.x % rhs.x, lhs.y % rhs.y, lhs.z % rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator%(lc_int3 lhs, lc_int rhs) noexcept { return lc_make_int3(lhs.x % rhs, lhs.y % rhs, lhs.z % rhs); }
[[nodiscard]] inline __device__ constexpr auto operator%(lc_int lhs, lc_int3 rhs) noexcept { return lc_make_int3(lhs % rhs.x, lhs % rhs.y, lhs % rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator%(lc_int4 lhs, lc_int4 rhs) noexcept { return lc_make_int4(lhs.x % rhs.x, lhs.y % rhs.y, lhs.z % rhs.z, lhs.w % rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator%(lc_int4 lhs, lc_int rhs) noexcept { return lc_make_int4(lhs.x % rhs, lhs.y % rhs, lhs.z % rhs, lhs.w % rhs); }
[[nodiscard]] inline __device__ constexpr auto operator%(lc_int lhs, lc_int4 rhs) noexcept { return lc_make_int4(lhs % rhs.x, lhs % rhs.y, lhs % rhs.z, lhs % rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator%(lc_uint2 lhs, lc_uint2 rhs) noexcept { return lc_make_uint2(lhs.x % rhs.x, lhs.y % rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator%(lc_uint2 lhs, lc_uint rhs) noexcept { return lc_make_uint2(lhs.x % rhs, lhs.y % rhs); }
[[nodiscard]] inline __device__ constexpr auto operator%(lc_uint lhs, lc_uint2 rhs) noexcept { return lc_make_uint2(lhs % rhs.x, lhs % rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator%(lc_uint3 lhs, lc_uint3 rhs) noexcept { return lc_make_uint3(lhs.x % rhs.x, lhs.y % rhs.y, lhs.z % rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator%(lc_uint3 lhs, lc_uint rhs) noexcept { return lc_make_uint3(lhs.x % rhs, lhs.y % rhs, lhs.z % rhs); }
[[nodiscard]] inline __device__ constexpr auto operator%(lc_uint lhs, lc_uint3 rhs) noexcept { return lc_make_uint3(lhs % rhs.x, lhs % rhs.y, lhs % rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator%(lc_uint4 lhs, lc_uint4 rhs) noexcept { return lc_make_uint4(lhs.x % rhs.x, lhs.y % rhs.y, lhs.z % rhs.z, lhs.w % rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator%(lc_uint4 lhs, lc_uint rhs) noexcept { return lc_make_uint4(lhs.x % rhs, lhs.y % rhs, lhs.z % rhs, lhs.w % rhs); }
[[nodiscard]] inline __device__ constexpr auto operator%(lc_uint lhs, lc_uint4 rhs) noexcept { return lc_make_uint4(lhs % rhs.x, lhs % rhs.y, lhs % rhs.z, lhs % rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator%(lc_long2 lhs, lc_long2 rhs) noexcept { return lc_make_long2(lhs.x % rhs.x, lhs.y % rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator%(lc_long2 lhs, lc_long rhs) noexcept { return lc_make_long2(lhs.x % rhs, lhs.y % rhs); }
[[nodiscard]] inline __device__ constexpr auto operator%(lc_long lhs, lc_long2 rhs) noexcept { return lc_make_long2(lhs % rhs.x, lhs % rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator%(lc_long3 lhs, lc_long3 rhs) noexcept { return lc_make_long3(lhs.x % rhs.x, lhs.y % rhs.y, lhs.z % rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator%(lc_long3 lhs, lc_long rhs) noexcept { return lc_make_long3(lhs.x % rhs, lhs.y % rhs, lhs.z % rhs); }
[[nodiscard]] inline __device__ constexpr auto operator%(lc_long lhs, lc_long3 rhs) noexcept { return lc_make_long3(lhs % rhs.x, lhs % rhs.y, lhs % rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator%(lc_long4 lhs, lc_long4 rhs) noexcept { return lc_make_long4(lhs.x % rhs.x, lhs.y % rhs.y, lhs.z % rhs.z, lhs.w % rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator%(lc_long4 lhs, lc_long rhs) noexcept { return lc_make_long4(lhs.x % rhs, lhs.y % rhs, lhs.z % rhs, lhs.w % rhs); }
[[nodiscard]] inline __device__ constexpr auto operator%(lc_long lhs, lc_long4 rhs) noexcept { return lc_make_long4(lhs % rhs.x, lhs % rhs.y, lhs % rhs.z, lhs % rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator%(lc_ulong2 lhs, lc_ulong2 rhs) noexcept { return lc_make_ulong2(lhs.x % rhs.x, lhs.y % rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator%(lc_ulong2 lhs, lc_ulong rhs) noexcept { return lc_make_ulong2(lhs.x % rhs, lhs.y % rhs); }
[[nodiscard]] inline __device__ constexpr auto operator%(lc_ulong lhs, lc_ulong2 rhs) noexcept { return lc_make_ulong2(lhs % rhs.x, lhs % rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator%(lc_ulong3 lhs, lc_ulong3 rhs) noexcept { return lc_make_ulong3(lhs.x % rhs.x, lhs.y % rhs.y, lhs.z % rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator%(lc_ulong3 lhs, lc_ulong rhs) noexcept { return lc_make_ulong3(lhs.x % rhs, lhs.y % rhs, lhs.z % rhs); }
[[nodiscard]] inline __device__ constexpr auto operator%(lc_ulong lhs, lc_ulong3 rhs) noexcept { return lc_make_ulong3(lhs % rhs.x, lhs % rhs.y, lhs % rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator%(lc_ulong4 lhs, lc_ulong4 rhs) noexcept { return lc_make_ulong4(lhs.x % rhs.x, lhs.y % rhs.y, lhs.z % rhs.z, lhs.w % rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator%(lc_ulong4 lhs, lc_ulong rhs) noexcept { return lc_make_ulong4(lhs.x % rhs, lhs.y % rhs, lhs.z % rhs, lhs.w % rhs); }
[[nodiscard]] inline __device__ constexpr auto operator%(lc_ulong lhs, lc_ulong4 rhs) noexcept { return lc_make_ulong4(lhs % rhs.x, lhs % rhs.y, lhs % rhs.z, lhs % rhs.w); }

[[nodiscard]] inline __device__ constexpr auto operator<<(lc_short2 lhs, lc_short2 rhs) noexcept { return lc_make_short2(lhs.x << rhs.x, lhs.y << rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator<<(lc_short2 lhs, lc_short rhs) noexcept { return lc_make_short2(lhs.x << rhs, lhs.y << rhs); }
[[nodiscard]] inline __device__ constexpr auto operator<<(lc_short lhs, lc_short2 rhs) noexcept { return lc_make_short2(lhs << rhs.x, lhs << rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator<<(lc_short3 lhs, lc_short3 rhs) noexcept { return lc_make_short3(lhs.x << rhs.x, lhs.y << rhs.y, lhs.z << rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator<<(lc_short3 lhs, lc_short rhs) noexcept { return lc_make_short3(lhs.x << rhs, lhs.y << rhs, lhs.z << rhs); }
[[nodiscard]] inline __device__ constexpr auto operator<<(lc_short lhs, lc_short3 rhs) noexcept { return lc_make_short3(lhs << rhs.x, lhs << rhs.y, lhs << rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator<<(lc_short4 lhs, lc_short4 rhs) noexcept { return lc_make_short4(lhs.x << rhs.x, lhs.y << rhs.y, lhs.z << rhs.z, lhs.w << rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator<<(lc_short4 lhs, lc_short rhs) noexcept { return lc_make_short4(lhs.x << rhs, lhs.y << rhs, lhs.z << rhs, lhs.w << rhs); }
[[nodiscard]] inline __device__ constexpr auto operator<<(lc_short lhs, lc_short4 rhs) noexcept { return lc_make_short4(lhs << rhs.x, lhs << rhs.y, lhs << rhs.z, lhs << rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator<<(lc_ushort2 lhs, lc_ushort2 rhs) noexcept { return lc_make_ushort2(lhs.x << rhs.x, lhs.y << rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator<<(lc_ushort2 lhs, lc_ushort rhs) noexcept { return lc_make_ushort2(lhs.x << rhs, lhs.y << rhs); }
[[nodiscard]] inline __device__ constexpr auto operator<<(lc_ushort lhs, lc_ushort2 rhs) noexcept { return lc_make_ushort2(lhs << rhs.x, lhs << rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator<<(lc_ushort3 lhs, lc_ushort3 rhs) noexcept { return lc_make_ushort3(lhs.x << rhs.x, lhs.y << rhs.y, lhs.z << rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator<<(lc_ushort3 lhs, lc_ushort rhs) noexcept { return lc_make_ushort3(lhs.x << rhs, lhs.y << rhs, lhs.z << rhs); }
[[nodiscard]] inline __device__ constexpr auto operator<<(lc_ushort lhs, lc_ushort3 rhs) noexcept { return lc_make_ushort3(lhs << rhs.x, lhs << rhs.y, lhs << rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator<<(lc_ushort4 lhs, lc_ushort4 rhs) noexcept { return lc_make_ushort4(lhs.x << rhs.x, lhs.y << rhs.y, lhs.z << rhs.z, lhs.w << rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator<<(lc_ushort4 lhs, lc_ushort rhs) noexcept { return lc_make_ushort4(lhs.x << rhs, lhs.y << rhs, lhs.z << rhs, lhs.w << rhs); }
[[nodiscard]] inline __device__ constexpr auto operator<<(lc_ushort lhs, lc_ushort4 rhs) noexcept { return lc_make_ushort4(lhs << rhs.x, lhs << rhs.y, lhs << rhs.z, lhs << rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator<<(lc_int2 lhs, lc_int2 rhs) noexcept { return lc_make_int2(lhs.x << rhs.x, lhs.y << rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator<<(lc_int2 lhs, lc_int rhs) noexcept { return lc_make_int2(lhs.x << rhs, lhs.y << rhs); }
[[nodiscard]] inline __device__ constexpr auto operator<<(lc_int lhs, lc_int2 rhs) noexcept { return lc_make_int2(lhs << rhs.x, lhs << rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator<<(lc_int3 lhs, lc_int3 rhs) noexcept { return lc_make_int3(lhs.x << rhs.x, lhs.y << rhs.y, lhs.z << rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator<<(lc_int3 lhs, lc_int rhs) noexcept { return lc_make_int3(lhs.x << rhs, lhs.y << rhs, lhs.z << rhs); }
[[nodiscard]] inline __device__ constexpr auto operator<<(lc_int lhs, lc_int3 rhs) noexcept { return lc_make_int3(lhs << rhs.x, lhs << rhs.y, lhs << rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator<<(lc_int4 lhs, lc_int4 rhs) noexcept { return lc_make_int4(lhs.x << rhs.x, lhs.y << rhs.y, lhs.z << rhs.z, lhs.w << rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator<<(lc_int4 lhs, lc_int rhs) noexcept { return lc_make_int4(lhs.x << rhs, lhs.y << rhs, lhs.z << rhs, lhs.w << rhs); }
[[nodiscard]] inline __device__ constexpr auto operator<<(lc_int lhs, lc_int4 rhs) noexcept { return lc_make_int4(lhs << rhs.x, lhs << rhs.y, lhs << rhs.z, lhs << rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator<<(lc_uint2 lhs, lc_uint2 rhs) noexcept { return lc_make_uint2(lhs.x << rhs.x, lhs.y << rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator<<(lc_uint2 lhs, lc_uint rhs) noexcept { return lc_make_uint2(lhs.x << rhs, lhs.y << rhs); }
[[nodiscard]] inline __device__ constexpr auto operator<<(lc_uint lhs, lc_uint2 rhs) noexcept { return lc_make_uint2(lhs << rhs.x, lhs << rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator<<(lc_uint3 lhs, lc_uint3 rhs) noexcept { return lc_make_uint3(lhs.x << rhs.x, lhs.y << rhs.y, lhs.z << rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator<<(lc_uint3 lhs, lc_uint rhs) noexcept { return lc_make_uint3(lhs.x << rhs, lhs.y << rhs, lhs.z << rhs); }
[[nodiscard]] inline __device__ constexpr auto operator<<(lc_uint lhs, lc_uint3 rhs) noexcept { return lc_make_uint3(lhs << rhs.x, lhs << rhs.y, lhs << rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator<<(lc_uint4 lhs, lc_uint4 rhs) noexcept { return lc_make_uint4(lhs.x << rhs.x, lhs.y << rhs.y, lhs.z << rhs.z, lhs.w << rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator<<(lc_uint4 lhs, lc_uint rhs) noexcept { return lc_make_uint4(lhs.x << rhs, lhs.y << rhs, lhs.z << rhs, lhs.w << rhs); }
[[nodiscard]] inline __device__ constexpr auto operator<<(lc_uint lhs, lc_uint4 rhs) noexcept { return lc_make_uint4(lhs << rhs.x, lhs << rhs.y, lhs << rhs.z, lhs << rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator<<(lc_long2 lhs, lc_long2 rhs) noexcept { return lc_make_long2(lhs.x << rhs.x, lhs.y << rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator<<(lc_long2 lhs, lc_long rhs) noexcept { return lc_make_long2(lhs.x << rhs, lhs.y << rhs); }
[[nodiscard]] inline __device__ constexpr auto operator<<(lc_long lhs, lc_long2 rhs) noexcept { return lc_make_long2(lhs << rhs.x, lhs << rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator<<(lc_long3 lhs, lc_long3 rhs) noexcept { return lc_make_long3(lhs.x << rhs.x, lhs.y << rhs.y, lhs.z << rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator<<(lc_long3 lhs, lc_long rhs) noexcept { return lc_make_long3(lhs.x << rhs, lhs.y << rhs, lhs.z << rhs); }
[[nodiscard]] inline __device__ constexpr auto operator<<(lc_long lhs, lc_long3 rhs) noexcept { return lc_make_long3(lhs << rhs.x, lhs << rhs.y, lhs << rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator<<(lc_long4 lhs, lc_long4 rhs) noexcept { return lc_make_long4(lhs.x << rhs.x, lhs.y << rhs.y, lhs.z << rhs.z, lhs.w << rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator<<(lc_long4 lhs, lc_long rhs) noexcept { return lc_make_long4(lhs.x << rhs, lhs.y << rhs, lhs.z << rhs, lhs.w << rhs); }
[[nodiscard]] inline __device__ constexpr auto operator<<(lc_long lhs, lc_long4 rhs) noexcept { return lc_make_long4(lhs << rhs.x, lhs << rhs.y, lhs << rhs.z, lhs << rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator<<(lc_ulong2 lhs, lc_ulong2 rhs) noexcept { return lc_make_ulong2(lhs.x << rhs.x, lhs.y << rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator<<(lc_ulong2 lhs, lc_ulong rhs) noexcept { return lc_make_ulong2(lhs.x << rhs, lhs.y << rhs); }
[[nodiscard]] inline __device__ constexpr auto operator<<(lc_ulong lhs, lc_ulong2 rhs) noexcept { return lc_make_ulong2(lhs << rhs.x, lhs << rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator<<(lc_ulong3 lhs, lc_ulong3 rhs) noexcept { return lc_make_ulong3(lhs.x << rhs.x, lhs.y << rhs.y, lhs.z << rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator<<(lc_ulong3 lhs, lc_ulong rhs) noexcept { return lc_make_ulong3(lhs.x << rhs, lhs.y << rhs, lhs.z << rhs); }
[[nodiscard]] inline __device__ constexpr auto operator<<(lc_ulong lhs, lc_ulong3 rhs) noexcept { return lc_make_ulong3(lhs << rhs.x, lhs << rhs.y, lhs << rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator<<(lc_ulong4 lhs, lc_ulong4 rhs) noexcept { return lc_make_ulong4(lhs.x << rhs.x, lhs.y << rhs.y, lhs.z << rhs.z, lhs.w << rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator<<(lc_ulong4 lhs, lc_ulong rhs) noexcept { return lc_make_ulong4(lhs.x << rhs, lhs.y << rhs, lhs.z << rhs, lhs.w << rhs); }
[[nodiscard]] inline __device__ constexpr auto operator<<(lc_ulong lhs, lc_ulong4 rhs) noexcept { return lc_make_ulong4(lhs << rhs.x, lhs << rhs.y, lhs << rhs.z, lhs << rhs.w); }

[[nodiscard]] inline __device__ constexpr auto operator>>(lc_short2 lhs, lc_short2 rhs) noexcept { return lc_make_short2(lhs.x >> rhs.x, lhs.y >> rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator>>(lc_short2 lhs, lc_short rhs) noexcept { return lc_make_short2(lhs.x >> rhs, lhs.y >> rhs); }
[[nodiscard]] inline __device__ constexpr auto operator>>(lc_short lhs, lc_short2 rhs) noexcept { return lc_make_short2(lhs >> rhs.x, lhs >> rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator>>(lc_short3 lhs, lc_short3 rhs) noexcept { return lc_make_short3(lhs.x >> rhs.x, lhs.y >> rhs.y, lhs.z >> rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator>>(lc_short3 lhs, lc_short rhs) noexcept { return lc_make_short3(lhs.x >> rhs, lhs.y >> rhs, lhs.z >> rhs); }
[[nodiscard]] inline __device__ constexpr auto operator>>(lc_short lhs, lc_short3 rhs) noexcept { return lc_make_short3(lhs >> rhs.x, lhs >> rhs.y, lhs >> rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator>>(lc_short4 lhs, lc_short4 rhs) noexcept { return lc_make_short4(lhs.x >> rhs.x, lhs.y >> rhs.y, lhs.z >> rhs.z, lhs.w >> rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator>>(lc_short4 lhs, lc_short rhs) noexcept { return lc_make_short4(lhs.x >> rhs, lhs.y >> rhs, lhs.z >> rhs, lhs.w >> rhs); }
[[nodiscard]] inline __device__ constexpr auto operator>>(lc_short lhs, lc_short4 rhs) noexcept { return lc_make_short4(lhs >> rhs.x, lhs >> rhs.y, lhs >> rhs.z, lhs >> rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator>>(lc_ushort2 lhs, lc_ushort2 rhs) noexcept { return lc_make_ushort2(lhs.x >> rhs.x, lhs.y >> rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator>>(lc_ushort2 lhs, lc_ushort rhs) noexcept { return lc_make_ushort2(lhs.x >> rhs, lhs.y >> rhs); }
[[nodiscard]] inline __device__ constexpr auto operator>>(lc_ushort lhs, lc_ushort2 rhs) noexcept { return lc_make_ushort2(lhs >> rhs.x, lhs >> rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator>>(lc_ushort3 lhs, lc_ushort3 rhs) noexcept { return lc_make_ushort3(lhs.x >> rhs.x, lhs.y >> rhs.y, lhs.z >> rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator>>(lc_ushort3 lhs, lc_ushort rhs) noexcept { return lc_make_ushort3(lhs.x >> rhs, lhs.y >> rhs, lhs.z >> rhs); }
[[nodiscard]] inline __device__ constexpr auto operator>>(lc_ushort lhs, lc_ushort3 rhs) noexcept { return lc_make_ushort3(lhs >> rhs.x, lhs >> rhs.y, lhs >> rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator>>(lc_ushort4 lhs, lc_ushort4 rhs) noexcept { return lc_make_ushort4(lhs.x >> rhs.x, lhs.y >> rhs.y, lhs.z >> rhs.z, lhs.w >> rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator>>(lc_ushort4 lhs, lc_ushort rhs) noexcept { return lc_make_ushort4(lhs.x >> rhs, lhs.y >> rhs, lhs.z >> rhs, lhs.w >> rhs); }
[[nodiscard]] inline __device__ constexpr auto operator>>(lc_ushort lhs, lc_ushort4 rhs) noexcept { return lc_make_ushort4(lhs >> rhs.x, lhs >> rhs.y, lhs >> rhs.z, lhs >> rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator>>(lc_int2 lhs, lc_int2 rhs) noexcept { return lc_make_int2(lhs.x >> rhs.x, lhs.y >> rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator>>(lc_int2 lhs, lc_int rhs) noexcept { return lc_make_int2(lhs.x >> rhs, lhs.y >> rhs); }
[[nodiscard]] inline __device__ constexpr auto operator>>(lc_int lhs, lc_int2 rhs) noexcept { return lc_make_int2(lhs >> rhs.x, lhs >> rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator>>(lc_int3 lhs, lc_int3 rhs) noexcept { return lc_make_int3(lhs.x >> rhs.x, lhs.y >> rhs.y, lhs.z >> rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator>>(lc_int3 lhs, lc_int rhs) noexcept { return lc_make_int3(lhs.x >> rhs, lhs.y >> rhs, lhs.z >> rhs); }
[[nodiscard]] inline __device__ constexpr auto operator>>(lc_int lhs, lc_int3 rhs) noexcept { return lc_make_int3(lhs >> rhs.x, lhs >> rhs.y, lhs >> rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator>>(lc_int4 lhs, lc_int4 rhs) noexcept { return lc_make_int4(lhs.x >> rhs.x, lhs.y >> rhs.y, lhs.z >> rhs.z, lhs.w >> rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator>>(lc_int4 lhs, lc_int rhs) noexcept { return lc_make_int4(lhs.x >> rhs, lhs.y >> rhs, lhs.z >> rhs, lhs.w >> rhs); }
[[nodiscard]] inline __device__ constexpr auto operator>>(lc_int lhs, lc_int4 rhs) noexcept { return lc_make_int4(lhs >> rhs.x, lhs >> rhs.y, lhs >> rhs.z, lhs >> rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator>>(lc_uint2 lhs, lc_uint2 rhs) noexcept { return lc_make_uint2(lhs.x >> rhs.x, lhs.y >> rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator>>(lc_uint2 lhs, lc_uint rhs) noexcept { return lc_make_uint2(lhs.x >> rhs, lhs.y >> rhs); }
[[nodiscard]] inline __device__ constexpr auto operator>>(lc_uint lhs, lc_uint2 rhs) noexcept { return lc_make_uint2(lhs >> rhs.x, lhs >> rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator>>(lc_uint3 lhs, lc_uint3 rhs) noexcept { return lc_make_uint3(lhs.x >> rhs.x, lhs.y >> rhs.y, lhs.z >> rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator>>(lc_uint3 lhs, lc_uint rhs) noexcept { return lc_make_uint3(lhs.x >> rhs, lhs.y >> rhs, lhs.z >> rhs); }
[[nodiscard]] inline __device__ constexpr auto operator>>(lc_uint lhs, lc_uint3 rhs) noexcept { return lc_make_uint3(lhs >> rhs.x, lhs >> rhs.y, lhs >> rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator>>(lc_uint4 lhs, lc_uint4 rhs) noexcept { return lc_make_uint4(lhs.x >> rhs.x, lhs.y >> rhs.y, lhs.z >> rhs.z, lhs.w >> rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator>>(lc_uint4 lhs, lc_uint rhs) noexcept { return lc_make_uint4(lhs.x >> rhs, lhs.y >> rhs, lhs.z >> rhs, lhs.w >> rhs); }
[[nodiscard]] inline __device__ constexpr auto operator>>(lc_uint lhs, lc_uint4 rhs) noexcept { return lc_make_uint4(lhs >> rhs.x, lhs >> rhs.y, lhs >> rhs.z, lhs >> rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator>>(lc_long2 lhs, lc_long2 rhs) noexcept { return lc_make_long2(lhs.x >> rhs.x, lhs.y >> rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator>>(lc_long2 lhs, lc_long rhs) noexcept { return lc_make_long2(lhs.x >> rhs, lhs.y >> rhs); }
[[nodiscard]] inline __device__ constexpr auto operator>>(lc_long lhs, lc_long2 rhs) noexcept { return lc_make_long2(lhs >> rhs.x, lhs >> rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator>>(lc_long3 lhs, lc_long3 rhs) noexcept { return lc_make_long3(lhs.x >> rhs.x, lhs.y >> rhs.y, lhs.z >> rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator>>(lc_long3 lhs, lc_long rhs) noexcept { return lc_make_long3(lhs.x >> rhs, lhs.y >> rhs, lhs.z >> rhs); }
[[nodiscard]] inline __device__ constexpr auto operator>>(lc_long lhs, lc_long3 rhs) noexcept { return lc_make_long3(lhs >> rhs.x, lhs >> rhs.y, lhs >> rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator>>(lc_long4 lhs, lc_long4 rhs) noexcept { return lc_make_long4(lhs.x >> rhs.x, lhs.y >> rhs.y, lhs.z >> rhs.z, lhs.w >> rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator>>(lc_long4 lhs, lc_long rhs) noexcept { return lc_make_long4(lhs.x >> rhs, lhs.y >> rhs, lhs.z >> rhs, lhs.w >> rhs); }
[[nodiscard]] inline __device__ constexpr auto operator>>(lc_long lhs, lc_long4 rhs) noexcept { return lc_make_long4(lhs >> rhs.x, lhs >> rhs.y, lhs >> rhs.z, lhs >> rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator>>(lc_ulong2 lhs, lc_ulong2 rhs) noexcept { return lc_make_ulong2(lhs.x >> rhs.x, lhs.y >> rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator>>(lc_ulong2 lhs, lc_ulong rhs) noexcept { return lc_make_ulong2(lhs.x >> rhs, lhs.y >> rhs); }
[[nodiscard]] inline __device__ constexpr auto operator>>(lc_ulong lhs, lc_ulong2 rhs) noexcept { return lc_make_ulong2(lhs >> rhs.x, lhs >> rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator>>(lc_ulong3 lhs, lc_ulong3 rhs) noexcept { return lc_make_ulong3(lhs.x >> rhs.x, lhs.y >> rhs.y, lhs.z >> rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator>>(lc_ulong3 lhs, lc_ulong rhs) noexcept { return lc_make_ulong3(lhs.x >> rhs, lhs.y >> rhs, lhs.z >> rhs); }
[[nodiscard]] inline __device__ constexpr auto operator>>(lc_ulong lhs, lc_ulong3 rhs) noexcept { return lc_make_ulong3(lhs >> rhs.x, lhs >> rhs.y, lhs >> rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator>>(lc_ulong4 lhs, lc_ulong4 rhs) noexcept { return lc_make_ulong4(lhs.x >> rhs.x, lhs.y >> rhs.y, lhs.z >> rhs.z, lhs.w >> rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator>>(lc_ulong4 lhs, lc_ulong rhs) noexcept { return lc_make_ulong4(lhs.x >> rhs, lhs.y >> rhs, lhs.z >> rhs, lhs.w >> rhs); }
[[nodiscard]] inline __device__ constexpr auto operator>>(lc_ulong lhs, lc_ulong4 rhs) noexcept { return lc_make_ulong4(lhs >> rhs.x, lhs >> rhs.y, lhs >> rhs.z, lhs >> rhs.w); }

[[nodiscard]] inline __device__ constexpr auto operator|(lc_short2 lhs, lc_short2 rhs) noexcept { return lc_make_short2(lhs.x | rhs.x, lhs.y | rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator|(lc_short2 lhs, lc_short rhs) noexcept { return lc_make_short2(lhs.x | rhs, lhs.y | rhs); }
[[nodiscard]] inline __device__ constexpr auto operator|(lc_short lhs, lc_short2 rhs) noexcept { return lc_make_short2(lhs | rhs.x, lhs | rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator|(lc_short3 lhs, lc_short3 rhs) noexcept { return lc_make_short3(lhs.x | rhs.x, lhs.y | rhs.y, lhs.z | rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator|(lc_short3 lhs, lc_short rhs) noexcept { return lc_make_short3(lhs.x | rhs, lhs.y | rhs, lhs.z | rhs); }
[[nodiscard]] inline __device__ constexpr auto operator|(lc_short lhs, lc_short3 rhs) noexcept { return lc_make_short3(lhs | rhs.x, lhs | rhs.y, lhs | rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator|(lc_short4 lhs, lc_short4 rhs) noexcept { return lc_make_short4(lhs.x | rhs.x, lhs.y | rhs.y, lhs.z | rhs.z, lhs.w | rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator|(lc_short4 lhs, lc_short rhs) noexcept { return lc_make_short4(lhs.x | rhs, lhs.y | rhs, lhs.z | rhs, lhs.w | rhs); }
[[nodiscard]] inline __device__ constexpr auto operator|(lc_short lhs, lc_short4 rhs) noexcept { return lc_make_short4(lhs | rhs.x, lhs | rhs.y, lhs | rhs.z, lhs | rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator|(lc_ushort2 lhs, lc_ushort2 rhs) noexcept { return lc_make_ushort2(lhs.x | rhs.x, lhs.y | rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator|(lc_ushort2 lhs, lc_ushort rhs) noexcept { return lc_make_ushort2(lhs.x | rhs, lhs.y | rhs); }
[[nodiscard]] inline __device__ constexpr auto operator|(lc_ushort lhs, lc_ushort2 rhs) noexcept { return lc_make_ushort2(lhs | rhs.x, lhs | rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator|(lc_ushort3 lhs, lc_ushort3 rhs) noexcept { return lc_make_ushort3(lhs.x | rhs.x, lhs.y | rhs.y, lhs.z | rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator|(lc_ushort3 lhs, lc_ushort rhs) noexcept { return lc_make_ushort3(lhs.x | rhs, lhs.y | rhs, lhs.z | rhs); }
[[nodiscard]] inline __device__ constexpr auto operator|(lc_ushort lhs, lc_ushort3 rhs) noexcept { return lc_make_ushort3(lhs | rhs.x, lhs | rhs.y, lhs | rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator|(lc_ushort4 lhs, lc_ushort4 rhs) noexcept { return lc_make_ushort4(lhs.x | rhs.x, lhs.y | rhs.y, lhs.z | rhs.z, lhs.w | rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator|(lc_ushort4 lhs, lc_ushort rhs) noexcept { return lc_make_ushort4(lhs.x | rhs, lhs.y | rhs, lhs.z | rhs, lhs.w | rhs); }
[[nodiscard]] inline __device__ constexpr auto operator|(lc_ushort lhs, lc_ushort4 rhs) noexcept { return lc_make_ushort4(lhs | rhs.x, lhs | rhs.y, lhs | rhs.z, lhs | rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator|(lc_int2 lhs, lc_int2 rhs) noexcept { return lc_make_int2(lhs.x | rhs.x, lhs.y | rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator|(lc_int2 lhs, lc_int rhs) noexcept { return lc_make_int2(lhs.x | rhs, lhs.y | rhs); }
[[nodiscard]] inline __device__ constexpr auto operator|(lc_int lhs, lc_int2 rhs) noexcept { return lc_make_int2(lhs | rhs.x, lhs | rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator|(lc_int3 lhs, lc_int3 rhs) noexcept { return lc_make_int3(lhs.x | rhs.x, lhs.y | rhs.y, lhs.z | rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator|(lc_int3 lhs, lc_int rhs) noexcept { return lc_make_int3(lhs.x | rhs, lhs.y | rhs, lhs.z | rhs); }
[[nodiscard]] inline __device__ constexpr auto operator|(lc_int lhs, lc_int3 rhs) noexcept { return lc_make_int3(lhs | rhs.x, lhs | rhs.y, lhs | rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator|(lc_int4 lhs, lc_int4 rhs) noexcept { return lc_make_int4(lhs.x | rhs.x, lhs.y | rhs.y, lhs.z | rhs.z, lhs.w | rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator|(lc_int4 lhs, lc_int rhs) noexcept { return lc_make_int4(lhs.x | rhs, lhs.y | rhs, lhs.z | rhs, lhs.w | rhs); }
[[nodiscard]] inline __device__ constexpr auto operator|(lc_int lhs, lc_int4 rhs) noexcept { return lc_make_int4(lhs | rhs.x, lhs | rhs.y, lhs | rhs.z, lhs | rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator|(lc_uint2 lhs, lc_uint2 rhs) noexcept { return lc_make_uint2(lhs.x | rhs.x, lhs.y | rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator|(lc_uint2 lhs, lc_uint rhs) noexcept { return lc_make_uint2(lhs.x | rhs, lhs.y | rhs); }
[[nodiscard]] inline __device__ constexpr auto operator|(lc_uint lhs, lc_uint2 rhs) noexcept { return lc_make_uint2(lhs | rhs.x, lhs | rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator|(lc_uint3 lhs, lc_uint3 rhs) noexcept { return lc_make_uint3(lhs.x | rhs.x, lhs.y | rhs.y, lhs.z | rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator|(lc_uint3 lhs, lc_uint rhs) noexcept { return lc_make_uint3(lhs.x | rhs, lhs.y | rhs, lhs.z | rhs); }
[[nodiscard]] inline __device__ constexpr auto operator|(lc_uint lhs, lc_uint3 rhs) noexcept { return lc_make_uint3(lhs | rhs.x, lhs | rhs.y, lhs | rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator|(lc_uint4 lhs, lc_uint4 rhs) noexcept { return lc_make_uint4(lhs.x | rhs.x, lhs.y | rhs.y, lhs.z | rhs.z, lhs.w | rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator|(lc_uint4 lhs, lc_uint rhs) noexcept { return lc_make_uint4(lhs.x | rhs, lhs.y | rhs, lhs.z | rhs, lhs.w | rhs); }
[[nodiscard]] inline __device__ constexpr auto operator|(lc_uint lhs, lc_uint4 rhs) noexcept { return lc_make_uint4(lhs | rhs.x, lhs | rhs.y, lhs | rhs.z, lhs | rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator|(lc_bool2 lhs, lc_bool2 rhs) noexcept { return lc_make_bool2(lhs.x | rhs.x, lhs.y | rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator|(lc_bool2 lhs, lc_bool rhs) noexcept { return lc_make_bool2(lhs.x | rhs, lhs.y | rhs); }
[[nodiscard]] inline __device__ constexpr auto operator|(lc_bool lhs, lc_bool2 rhs) noexcept { return lc_make_bool2(lhs | rhs.x, lhs | rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator|(lc_bool3 lhs, lc_bool3 rhs) noexcept { return lc_make_bool3(lhs.x | rhs.x, lhs.y | rhs.y, lhs.z | rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator|(lc_bool3 lhs, lc_bool rhs) noexcept { return lc_make_bool3(lhs.x | rhs, lhs.y | rhs, lhs.z | rhs); }
[[nodiscard]] inline __device__ constexpr auto operator|(lc_bool lhs, lc_bool3 rhs) noexcept { return lc_make_bool3(lhs | rhs.x, lhs | rhs.y, lhs | rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator|(lc_bool4 lhs, lc_bool4 rhs) noexcept { return lc_make_bool4(lhs.x | rhs.x, lhs.y | rhs.y, lhs.z | rhs.z, lhs.w | rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator|(lc_bool4 lhs, lc_bool rhs) noexcept { return lc_make_bool4(lhs.x | rhs, lhs.y | rhs, lhs.z | rhs, lhs.w | rhs); }
[[nodiscard]] inline __device__ constexpr auto operator|(lc_bool lhs, lc_bool4 rhs) noexcept { return lc_make_bool4(lhs | rhs.x, lhs | rhs.y, lhs | rhs.z, lhs | rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator|(lc_long2 lhs, lc_long2 rhs) noexcept { return lc_make_long2(lhs.x | rhs.x, lhs.y | rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator|(lc_long2 lhs, lc_long rhs) noexcept { return lc_make_long2(lhs.x | rhs, lhs.y | rhs); }
[[nodiscard]] inline __device__ constexpr auto operator|(lc_long lhs, lc_long2 rhs) noexcept { return lc_make_long2(lhs | rhs.x, lhs | rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator|(lc_long3 lhs, lc_long3 rhs) noexcept { return lc_make_long3(lhs.x | rhs.x, lhs.y | rhs.y, lhs.z | rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator|(lc_long3 lhs, lc_long rhs) noexcept { return lc_make_long3(lhs.x | rhs, lhs.y | rhs, lhs.z | rhs); }
[[nodiscard]] inline __device__ constexpr auto operator|(lc_long lhs, lc_long3 rhs) noexcept { return lc_make_long3(lhs | rhs.x, lhs | rhs.y, lhs | rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator|(lc_long4 lhs, lc_long4 rhs) noexcept { return lc_make_long4(lhs.x | rhs.x, lhs.y | rhs.y, lhs.z | rhs.z, lhs.w | rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator|(lc_long4 lhs, lc_long rhs) noexcept { return lc_make_long4(lhs.x | rhs, lhs.y | rhs, lhs.z | rhs, lhs.w | rhs); }
[[nodiscard]] inline __device__ constexpr auto operator|(lc_long lhs, lc_long4 rhs) noexcept { return lc_make_long4(lhs | rhs.x, lhs | rhs.y, lhs | rhs.z, lhs | rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator|(lc_ulong2 lhs, lc_ulong2 rhs) noexcept { return lc_make_ulong2(lhs.x | rhs.x, lhs.y | rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator|(lc_ulong2 lhs, lc_ulong rhs) noexcept { return lc_make_ulong2(lhs.x | rhs, lhs.y | rhs); }
[[nodiscard]] inline __device__ constexpr auto operator|(lc_ulong lhs, lc_ulong2 rhs) noexcept { return lc_make_ulong2(lhs | rhs.x, lhs | rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator|(lc_ulong3 lhs, lc_ulong3 rhs) noexcept { return lc_make_ulong3(lhs.x | rhs.x, lhs.y | rhs.y, lhs.z | rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator|(lc_ulong3 lhs, lc_ulong rhs) noexcept { return lc_make_ulong3(lhs.x | rhs, lhs.y | rhs, lhs.z | rhs); }
[[nodiscard]] inline __device__ constexpr auto operator|(lc_ulong lhs, lc_ulong3 rhs) noexcept { return lc_make_ulong3(lhs | rhs.x, lhs | rhs.y, lhs | rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator|(lc_ulong4 lhs, lc_ulong4 rhs) noexcept { return lc_make_ulong4(lhs.x | rhs.x, lhs.y | rhs.y, lhs.z | rhs.z, lhs.w | rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator|(lc_ulong4 lhs, lc_ulong rhs) noexcept { return lc_make_ulong4(lhs.x | rhs, lhs.y | rhs, lhs.z | rhs, lhs.w | rhs); }
[[nodiscard]] inline __device__ constexpr auto operator|(lc_ulong lhs, lc_ulong4 rhs) noexcept { return lc_make_ulong4(lhs | rhs.x, lhs | rhs.y, lhs | rhs.z, lhs | rhs.w); }

[[nodiscard]] inline __device__ constexpr auto operator&(lc_short2 lhs, lc_short2 rhs) noexcept { return lc_make_short2(lhs.x & rhs.x, lhs.y & rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator&(lc_short2 lhs, lc_short rhs) noexcept { return lc_make_short2(lhs.x & rhs, lhs.y & rhs); }
[[nodiscard]] inline __device__ constexpr auto operator&(lc_short lhs, lc_short2 rhs) noexcept { return lc_make_short2(lhs & rhs.x, lhs & rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator&(lc_short3 lhs, lc_short3 rhs) noexcept { return lc_make_short3(lhs.x & rhs.x, lhs.y & rhs.y, lhs.z & rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator&(lc_short3 lhs, lc_short rhs) noexcept { return lc_make_short3(lhs.x & rhs, lhs.y & rhs, lhs.z & rhs); }
[[nodiscard]] inline __device__ constexpr auto operator&(lc_short lhs, lc_short3 rhs) noexcept { return lc_make_short3(lhs & rhs.x, lhs & rhs.y, lhs & rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator&(lc_short4 lhs, lc_short4 rhs) noexcept { return lc_make_short4(lhs.x & rhs.x, lhs.y & rhs.y, lhs.z & rhs.z, lhs.w & rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator&(lc_short4 lhs, lc_short rhs) noexcept { return lc_make_short4(lhs.x & rhs, lhs.y & rhs, lhs.z & rhs, lhs.w & rhs); }
[[nodiscard]] inline __device__ constexpr auto operator&(lc_short lhs, lc_short4 rhs) noexcept { return lc_make_short4(lhs & rhs.x, lhs & rhs.y, lhs & rhs.z, lhs & rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator&(lc_ushort2 lhs, lc_ushort2 rhs) noexcept { return lc_make_ushort2(lhs.x & rhs.x, lhs.y & rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator&(lc_ushort2 lhs, lc_ushort rhs) noexcept { return lc_make_ushort2(lhs.x & rhs, lhs.y & rhs); }
[[nodiscard]] inline __device__ constexpr auto operator&(lc_ushort lhs, lc_ushort2 rhs) noexcept { return lc_make_ushort2(lhs & rhs.x, lhs & rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator&(lc_ushort3 lhs, lc_ushort3 rhs) noexcept { return lc_make_ushort3(lhs.x & rhs.x, lhs.y & rhs.y, lhs.z & rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator&(lc_ushort3 lhs, lc_ushort rhs) noexcept { return lc_make_ushort3(lhs.x & rhs, lhs.y & rhs, lhs.z & rhs); }
[[nodiscard]] inline __device__ constexpr auto operator&(lc_ushort lhs, lc_ushort3 rhs) noexcept { return lc_make_ushort3(lhs & rhs.x, lhs & rhs.y, lhs & rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator&(lc_ushort4 lhs, lc_ushort4 rhs) noexcept { return lc_make_ushort4(lhs.x & rhs.x, lhs.y & rhs.y, lhs.z & rhs.z, lhs.w & rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator&(lc_ushort4 lhs, lc_ushort rhs) noexcept { return lc_make_ushort4(lhs.x & rhs, lhs.y & rhs, lhs.z & rhs, lhs.w & rhs); }
[[nodiscard]] inline __device__ constexpr auto operator&(lc_ushort lhs, lc_ushort4 rhs) noexcept { return lc_make_ushort4(lhs & rhs.x, lhs & rhs.y, lhs & rhs.z, lhs & rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator&(lc_int2 lhs, lc_int2 rhs) noexcept { return lc_make_int2(lhs.x & rhs.x, lhs.y & rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator&(lc_int2 lhs, lc_int rhs) noexcept { return lc_make_int2(lhs.x & rhs, lhs.y & rhs); }
[[nodiscard]] inline __device__ constexpr auto operator&(lc_int lhs, lc_int2 rhs) noexcept { return lc_make_int2(lhs & rhs.x, lhs & rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator&(lc_int3 lhs, lc_int3 rhs) noexcept { return lc_make_int3(lhs.x & rhs.x, lhs.y & rhs.y, lhs.z & rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator&(lc_int3 lhs, lc_int rhs) noexcept { return lc_make_int3(lhs.x & rhs, lhs.y & rhs, lhs.z & rhs); }
[[nodiscard]] inline __device__ constexpr auto operator&(lc_int lhs, lc_int3 rhs) noexcept { return lc_make_int3(lhs & rhs.x, lhs & rhs.y, lhs & rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator&(lc_int4 lhs, lc_int4 rhs) noexcept { return lc_make_int4(lhs.x & rhs.x, lhs.y & rhs.y, lhs.z & rhs.z, lhs.w & rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator&(lc_int4 lhs, lc_int rhs) noexcept { return lc_make_int4(lhs.x & rhs, lhs.y & rhs, lhs.z & rhs, lhs.w & rhs); }
[[nodiscard]] inline __device__ constexpr auto operator&(lc_int lhs, lc_int4 rhs) noexcept { return lc_make_int4(lhs & rhs.x, lhs & rhs.y, lhs & rhs.z, lhs & rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator&(lc_uint2 lhs, lc_uint2 rhs) noexcept { return lc_make_uint2(lhs.x & rhs.x, lhs.y & rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator&(lc_uint2 lhs, lc_uint rhs) noexcept { return lc_make_uint2(lhs.x & rhs, lhs.y & rhs); }
[[nodiscard]] inline __device__ constexpr auto operator&(lc_uint lhs, lc_uint2 rhs) noexcept { return lc_make_uint2(lhs & rhs.x, lhs & rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator&(lc_uint3 lhs, lc_uint3 rhs) noexcept { return lc_make_uint3(lhs.x & rhs.x, lhs.y & rhs.y, lhs.z & rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator&(lc_uint3 lhs, lc_uint rhs) noexcept { return lc_make_uint3(lhs.x & rhs, lhs.y & rhs, lhs.z & rhs); }
[[nodiscard]] inline __device__ constexpr auto operator&(lc_uint lhs, lc_uint3 rhs) noexcept { return lc_make_uint3(lhs & rhs.x, lhs & rhs.y, lhs & rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator&(lc_uint4 lhs, lc_uint4 rhs) noexcept { return lc_make_uint4(lhs.x & rhs.x, lhs.y & rhs.y, lhs.z & rhs.z, lhs.w & rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator&(lc_uint4 lhs, lc_uint rhs) noexcept { return lc_make_uint4(lhs.x & rhs, lhs.y & rhs, lhs.z & rhs, lhs.w & rhs); }
[[nodiscard]] inline __device__ constexpr auto operator&(lc_uint lhs, lc_uint4 rhs) noexcept { return lc_make_uint4(lhs & rhs.x, lhs & rhs.y, lhs & rhs.z, lhs & rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator&(lc_bool2 lhs, lc_bool2 rhs) noexcept { return lc_make_bool2(lhs.x & rhs.x, lhs.y & rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator&(lc_bool2 lhs, lc_bool rhs) noexcept { return lc_make_bool2(lhs.x & rhs, lhs.y & rhs); }
[[nodiscard]] inline __device__ constexpr auto operator&(lc_bool lhs, lc_bool2 rhs) noexcept { return lc_make_bool2(lhs & rhs.x, lhs & rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator&(lc_bool3 lhs, lc_bool3 rhs) noexcept { return lc_make_bool3(lhs.x & rhs.x, lhs.y & rhs.y, lhs.z & rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator&(lc_bool3 lhs, lc_bool rhs) noexcept { return lc_make_bool3(lhs.x & rhs, lhs.y & rhs, lhs.z & rhs); }
[[nodiscard]] inline __device__ constexpr auto operator&(lc_bool lhs, lc_bool3 rhs) noexcept { return lc_make_bool3(lhs & rhs.x, lhs & rhs.y, lhs & rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator&(lc_bool4 lhs, lc_bool4 rhs) noexcept { return lc_make_bool4(lhs.x & rhs.x, lhs.y & rhs.y, lhs.z & rhs.z, lhs.w & rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator&(lc_bool4 lhs, lc_bool rhs) noexcept { return lc_make_bool4(lhs.x & rhs, lhs.y & rhs, lhs.z & rhs, lhs.w & rhs); }
[[nodiscard]] inline __device__ constexpr auto operator&(lc_bool lhs, lc_bool4 rhs) noexcept { return lc_make_bool4(lhs & rhs.x, lhs & rhs.y, lhs & rhs.z, lhs & rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator&(lc_long2 lhs, lc_long2 rhs) noexcept { return lc_make_long2(lhs.x & rhs.x, lhs.y & rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator&(lc_long2 lhs, lc_long rhs) noexcept { return lc_make_long2(lhs.x & rhs, lhs.y & rhs); }
[[nodiscard]] inline __device__ constexpr auto operator&(lc_long lhs, lc_long2 rhs) noexcept { return lc_make_long2(lhs & rhs.x, lhs & rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator&(lc_long3 lhs, lc_long3 rhs) noexcept { return lc_make_long3(lhs.x & rhs.x, lhs.y & rhs.y, lhs.z & rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator&(lc_long3 lhs, lc_long rhs) noexcept { return lc_make_long3(lhs.x & rhs, lhs.y & rhs, lhs.z & rhs); }
[[nodiscard]] inline __device__ constexpr auto operator&(lc_long lhs, lc_long3 rhs) noexcept { return lc_make_long3(lhs & rhs.x, lhs & rhs.y, lhs & rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator&(lc_long4 lhs, lc_long4 rhs) noexcept { return lc_make_long4(lhs.x & rhs.x, lhs.y & rhs.y, lhs.z & rhs.z, lhs.w & rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator&(lc_long4 lhs, lc_long rhs) noexcept { return lc_make_long4(lhs.x & rhs, lhs.y & rhs, lhs.z & rhs, lhs.w & rhs); }
[[nodiscard]] inline __device__ constexpr auto operator&(lc_long lhs, lc_long4 rhs) noexcept { return lc_make_long4(lhs & rhs.x, lhs & rhs.y, lhs & rhs.z, lhs & rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator&(lc_ulong2 lhs, lc_ulong2 rhs) noexcept { return lc_make_ulong2(lhs.x & rhs.x, lhs.y & rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator&(lc_ulong2 lhs, lc_ulong rhs) noexcept { return lc_make_ulong2(lhs.x & rhs, lhs.y & rhs); }
[[nodiscard]] inline __device__ constexpr auto operator&(lc_ulong lhs, lc_ulong2 rhs) noexcept { return lc_make_ulong2(lhs & rhs.x, lhs & rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator&(lc_ulong3 lhs, lc_ulong3 rhs) noexcept { return lc_make_ulong3(lhs.x & rhs.x, lhs.y & rhs.y, lhs.z & rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator&(lc_ulong3 lhs, lc_ulong rhs) noexcept { return lc_make_ulong3(lhs.x & rhs, lhs.y & rhs, lhs.z & rhs); }
[[nodiscard]] inline __device__ constexpr auto operator&(lc_ulong lhs, lc_ulong3 rhs) noexcept { return lc_make_ulong3(lhs & rhs.x, lhs & rhs.y, lhs & rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator&(lc_ulong4 lhs, lc_ulong4 rhs) noexcept { return lc_make_ulong4(lhs.x & rhs.x, lhs.y & rhs.y, lhs.z & rhs.z, lhs.w & rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator&(lc_ulong4 lhs, lc_ulong rhs) noexcept { return lc_make_ulong4(lhs.x & rhs, lhs.y & rhs, lhs.z & rhs, lhs.w & rhs); }
[[nodiscard]] inline __device__ constexpr auto operator&(lc_ulong lhs, lc_ulong4 rhs) noexcept { return lc_make_ulong4(lhs & rhs.x, lhs & rhs.y, lhs & rhs.z, lhs & rhs.w); }

[[nodiscard]] inline __device__ constexpr auto operator^(lc_short2 lhs, lc_short2 rhs) noexcept { return lc_make_short2(lhs.x ^ rhs.x, lhs.y ^ rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator^(lc_short2 lhs, lc_short rhs) noexcept { return lc_make_short2(lhs.x ^ rhs, lhs.y ^ rhs); }
[[nodiscard]] inline __device__ constexpr auto operator^(lc_short lhs, lc_short2 rhs) noexcept { return lc_make_short2(lhs ^ rhs.x, lhs ^ rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator^(lc_short3 lhs, lc_short3 rhs) noexcept { return lc_make_short3(lhs.x ^ rhs.x, lhs.y ^ rhs.y, lhs.z ^ rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator^(lc_short3 lhs, lc_short rhs) noexcept { return lc_make_short3(lhs.x ^ rhs, lhs.y ^ rhs, lhs.z ^ rhs); }
[[nodiscard]] inline __device__ constexpr auto operator^(lc_short lhs, lc_short3 rhs) noexcept { return lc_make_short3(lhs ^ rhs.x, lhs ^ rhs.y, lhs ^ rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator^(lc_short4 lhs, lc_short4 rhs) noexcept { return lc_make_short4(lhs.x ^ rhs.x, lhs.y ^ rhs.y, lhs.z ^ rhs.z, lhs.w ^ rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator^(lc_short4 lhs, lc_short rhs) noexcept { return lc_make_short4(lhs.x ^ rhs, lhs.y ^ rhs, lhs.z ^ rhs, lhs.w ^ rhs); }
[[nodiscard]] inline __device__ constexpr auto operator^(lc_short lhs, lc_short4 rhs) noexcept { return lc_make_short4(lhs ^ rhs.x, lhs ^ rhs.y, lhs ^ rhs.z, lhs ^ rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator^(lc_ushort2 lhs, lc_ushort2 rhs) noexcept { return lc_make_ushort2(lhs.x ^ rhs.x, lhs.y ^ rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator^(lc_ushort2 lhs, lc_ushort rhs) noexcept { return lc_make_ushort2(lhs.x ^ rhs, lhs.y ^ rhs); }
[[nodiscard]] inline __device__ constexpr auto operator^(lc_ushort lhs, lc_ushort2 rhs) noexcept { return lc_make_ushort2(lhs ^ rhs.x, lhs ^ rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator^(lc_ushort3 lhs, lc_ushort3 rhs) noexcept { return lc_make_ushort3(lhs.x ^ rhs.x, lhs.y ^ rhs.y, lhs.z ^ rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator^(lc_ushort3 lhs, lc_ushort rhs) noexcept { return lc_make_ushort3(lhs.x ^ rhs, lhs.y ^ rhs, lhs.z ^ rhs); }
[[nodiscard]] inline __device__ constexpr auto operator^(lc_ushort lhs, lc_ushort3 rhs) noexcept { return lc_make_ushort3(lhs ^ rhs.x, lhs ^ rhs.y, lhs ^ rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator^(lc_ushort4 lhs, lc_ushort4 rhs) noexcept { return lc_make_ushort4(lhs.x ^ rhs.x, lhs.y ^ rhs.y, lhs.z ^ rhs.z, lhs.w ^ rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator^(lc_ushort4 lhs, lc_ushort rhs) noexcept { return lc_make_ushort4(lhs.x ^ rhs, lhs.y ^ rhs, lhs.z ^ rhs, lhs.w ^ rhs); }
[[nodiscard]] inline __device__ constexpr auto operator^(lc_ushort lhs, lc_ushort4 rhs) noexcept { return lc_make_ushort4(lhs ^ rhs.x, lhs ^ rhs.y, lhs ^ rhs.z, lhs ^ rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator^(lc_int2 lhs, lc_int2 rhs) noexcept { return lc_make_int2(lhs.x ^ rhs.x, lhs.y ^ rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator^(lc_int2 lhs, lc_int rhs) noexcept { return lc_make_int2(lhs.x ^ rhs, lhs.y ^ rhs); }
[[nodiscard]] inline __device__ constexpr auto operator^(lc_int lhs, lc_int2 rhs) noexcept { return lc_make_int2(lhs ^ rhs.x, lhs ^ rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator^(lc_int3 lhs, lc_int3 rhs) noexcept { return lc_make_int3(lhs.x ^ rhs.x, lhs.y ^ rhs.y, lhs.z ^ rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator^(lc_int3 lhs, lc_int rhs) noexcept { return lc_make_int3(lhs.x ^ rhs, lhs.y ^ rhs, lhs.z ^ rhs); }
[[nodiscard]] inline __device__ constexpr auto operator^(lc_int lhs, lc_int3 rhs) noexcept { return lc_make_int3(lhs ^ rhs.x, lhs ^ rhs.y, lhs ^ rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator^(lc_int4 lhs, lc_int4 rhs) noexcept { return lc_make_int4(lhs.x ^ rhs.x, lhs.y ^ rhs.y, lhs.z ^ rhs.z, lhs.w ^ rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator^(lc_int4 lhs, lc_int rhs) noexcept { return lc_make_int4(lhs.x ^ rhs, lhs.y ^ rhs, lhs.z ^ rhs, lhs.w ^ rhs); }
[[nodiscard]] inline __device__ constexpr auto operator^(lc_int lhs, lc_int4 rhs) noexcept { return lc_make_int4(lhs ^ rhs.x, lhs ^ rhs.y, lhs ^ rhs.z, lhs ^ rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator^(lc_uint2 lhs, lc_uint2 rhs) noexcept { return lc_make_uint2(lhs.x ^ rhs.x, lhs.y ^ rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator^(lc_uint2 lhs, lc_uint rhs) noexcept { return lc_make_uint2(lhs.x ^ rhs, lhs.y ^ rhs); }
[[nodiscard]] inline __device__ constexpr auto operator^(lc_uint lhs, lc_uint2 rhs) noexcept { return lc_make_uint2(lhs ^ rhs.x, lhs ^ rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator^(lc_uint3 lhs, lc_uint3 rhs) noexcept { return lc_make_uint3(lhs.x ^ rhs.x, lhs.y ^ rhs.y, lhs.z ^ rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator^(lc_uint3 lhs, lc_uint rhs) noexcept { return lc_make_uint3(lhs.x ^ rhs, lhs.y ^ rhs, lhs.z ^ rhs); }
[[nodiscard]] inline __device__ constexpr auto operator^(lc_uint lhs, lc_uint3 rhs) noexcept { return lc_make_uint3(lhs ^ rhs.x, lhs ^ rhs.y, lhs ^ rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator^(lc_uint4 lhs, lc_uint4 rhs) noexcept { return lc_make_uint4(lhs.x ^ rhs.x, lhs.y ^ rhs.y, lhs.z ^ rhs.z, lhs.w ^ rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator^(lc_uint4 lhs, lc_uint rhs) noexcept { return lc_make_uint4(lhs.x ^ rhs, lhs.y ^ rhs, lhs.z ^ rhs, lhs.w ^ rhs); }
[[nodiscard]] inline __device__ constexpr auto operator^(lc_uint lhs, lc_uint4 rhs) noexcept { return lc_make_uint4(lhs ^ rhs.x, lhs ^ rhs.y, lhs ^ rhs.z, lhs ^ rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator^(lc_bool2 lhs, lc_bool2 rhs) noexcept { return lc_make_bool2(lhs.x ^ rhs.x, lhs.y ^ rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator^(lc_bool2 lhs, lc_bool rhs) noexcept { return lc_make_bool2(lhs.x ^ rhs, lhs.y ^ rhs); }
[[nodiscard]] inline __device__ constexpr auto operator^(lc_bool lhs, lc_bool2 rhs) noexcept { return lc_make_bool2(lhs ^ rhs.x, lhs ^ rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator^(lc_bool3 lhs, lc_bool3 rhs) noexcept { return lc_make_bool3(lhs.x ^ rhs.x, lhs.y ^ rhs.y, lhs.z ^ rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator^(lc_bool3 lhs, lc_bool rhs) noexcept { return lc_make_bool3(lhs.x ^ rhs, lhs.y ^ rhs, lhs.z ^ rhs); }
[[nodiscard]] inline __device__ constexpr auto operator^(lc_bool lhs, lc_bool3 rhs) noexcept { return lc_make_bool3(lhs ^ rhs.x, lhs ^ rhs.y, lhs ^ rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator^(lc_bool4 lhs, lc_bool4 rhs) noexcept { return lc_make_bool4(lhs.x ^ rhs.x, lhs.y ^ rhs.y, lhs.z ^ rhs.z, lhs.w ^ rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator^(lc_bool4 lhs, lc_bool rhs) noexcept { return lc_make_bool4(lhs.x ^ rhs, lhs.y ^ rhs, lhs.z ^ rhs, lhs.w ^ rhs); }
[[nodiscard]] inline __device__ constexpr auto operator^(lc_bool lhs, lc_bool4 rhs) noexcept { return lc_make_bool4(lhs ^ rhs.x, lhs ^ rhs.y, lhs ^ rhs.z, lhs ^ rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator^(lc_long2 lhs, lc_long2 rhs) noexcept { return lc_make_long2(lhs.x ^ rhs.x, lhs.y ^ rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator^(lc_long2 lhs, lc_long rhs) noexcept { return lc_make_long2(lhs.x ^ rhs, lhs.y ^ rhs); }
[[nodiscard]] inline __device__ constexpr auto operator^(lc_long lhs, lc_long2 rhs) noexcept { return lc_make_long2(lhs ^ rhs.x, lhs ^ rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator^(lc_long3 lhs, lc_long3 rhs) noexcept { return lc_make_long3(lhs.x ^ rhs.x, lhs.y ^ rhs.y, lhs.z ^ rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator^(lc_long3 lhs, lc_long rhs) noexcept { return lc_make_long3(lhs.x ^ rhs, lhs.y ^ rhs, lhs.z ^ rhs); }
[[nodiscard]] inline __device__ constexpr auto operator^(lc_long lhs, lc_long3 rhs) noexcept { return lc_make_long3(lhs ^ rhs.x, lhs ^ rhs.y, lhs ^ rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator^(lc_long4 lhs, lc_long4 rhs) noexcept { return lc_make_long4(lhs.x ^ rhs.x, lhs.y ^ rhs.y, lhs.z ^ rhs.z, lhs.w ^ rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator^(lc_long4 lhs, lc_long rhs) noexcept { return lc_make_long4(lhs.x ^ rhs, lhs.y ^ rhs, lhs.z ^ rhs, lhs.w ^ rhs); }
[[nodiscard]] inline __device__ constexpr auto operator^(lc_long lhs, lc_long4 rhs) noexcept { return lc_make_long4(lhs ^ rhs.x, lhs ^ rhs.y, lhs ^ rhs.z, lhs ^ rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator^(lc_ulong2 lhs, lc_ulong2 rhs) noexcept { return lc_make_ulong2(lhs.x ^ rhs.x, lhs.y ^ rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator^(lc_ulong2 lhs, lc_ulong rhs) noexcept { return lc_make_ulong2(lhs.x ^ rhs, lhs.y ^ rhs); }
[[nodiscard]] inline __device__ constexpr auto operator^(lc_ulong lhs, lc_ulong2 rhs) noexcept { return lc_make_ulong2(lhs ^ rhs.x, lhs ^ rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator^(lc_ulong3 lhs, lc_ulong3 rhs) noexcept { return lc_make_ulong3(lhs.x ^ rhs.x, lhs.y ^ rhs.y, lhs.z ^ rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator^(lc_ulong3 lhs, lc_ulong rhs) noexcept { return lc_make_ulong3(lhs.x ^ rhs, lhs.y ^ rhs, lhs.z ^ rhs); }
[[nodiscard]] inline __device__ constexpr auto operator^(lc_ulong lhs, lc_ulong3 rhs) noexcept { return lc_make_ulong3(lhs ^ rhs.x, lhs ^ rhs.y, lhs ^ rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator^(lc_ulong4 lhs, lc_ulong4 rhs) noexcept { return lc_make_ulong4(lhs.x ^ rhs.x, lhs.y ^ rhs.y, lhs.z ^ rhs.z, lhs.w ^ rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator^(lc_ulong4 lhs, lc_ulong rhs) noexcept { return lc_make_ulong4(lhs.x ^ rhs, lhs.y ^ rhs, lhs.z ^ rhs, lhs.w ^ rhs); }
[[nodiscard]] inline __device__ constexpr auto operator^(lc_ulong lhs, lc_ulong4 rhs) noexcept { return lc_make_ulong4(lhs ^ rhs.x, lhs ^ rhs.y, lhs ^ rhs.z, lhs ^ rhs.w); }

[[nodiscard]] inline __device__ constexpr auto operator||(lc_bool2 lhs, lc_bool2 rhs) noexcept { return lc_make_bool2(lhs.x || rhs.x, lhs.y || rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator||(lc_bool2 lhs, lc_bool rhs) noexcept { return lc_make_bool2(lhs.x || rhs, lhs.y || rhs); }
[[nodiscard]] inline __device__ constexpr auto operator||(lc_bool lhs, lc_bool2 rhs) noexcept { return lc_make_bool2(lhs || rhs.x, lhs || rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator||(lc_bool3 lhs, lc_bool3 rhs) noexcept { return lc_make_bool3(lhs.x || rhs.x, lhs.y || rhs.y, lhs.z || rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator||(lc_bool3 lhs, lc_bool rhs) noexcept { return lc_make_bool3(lhs.x || rhs, lhs.y || rhs, lhs.z || rhs); }
[[nodiscard]] inline __device__ constexpr auto operator||(lc_bool lhs, lc_bool3 rhs) noexcept { return lc_make_bool3(lhs || rhs.x, lhs || rhs.y, lhs || rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator||(lc_bool4 lhs, lc_bool4 rhs) noexcept { return lc_make_bool4(lhs.x || rhs.x, lhs.y || rhs.y, lhs.z || rhs.z, lhs.w || rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator||(lc_bool4 lhs, lc_bool rhs) noexcept { return lc_make_bool4(lhs.x || rhs, lhs.y || rhs, lhs.z || rhs, lhs.w || rhs); }
[[nodiscard]] inline __device__ constexpr auto operator||(lc_bool lhs, lc_bool4 rhs) noexcept { return lc_make_bool4(lhs || rhs.x, lhs || rhs.y, lhs || rhs.z, lhs || rhs.w); }

[[nodiscard]] inline __device__ constexpr auto operator&&(lc_bool2 lhs, lc_bool2 rhs) noexcept { return lc_make_bool2(lhs.x && rhs.x, lhs.y && rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator&&(lc_bool2 lhs, lc_bool rhs) noexcept { return lc_make_bool2(lhs.x && rhs, lhs.y && rhs); }
[[nodiscard]] inline __device__ constexpr auto operator&&(lc_bool lhs, lc_bool2 rhs) noexcept { return lc_make_bool2(lhs && rhs.x, lhs && rhs.y); }
[[nodiscard]] inline __device__ constexpr auto operator&&(lc_bool3 lhs, lc_bool3 rhs) noexcept { return lc_make_bool3(lhs.x && rhs.x, lhs.y && rhs.y, lhs.z && rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator&&(lc_bool3 lhs, lc_bool rhs) noexcept { return lc_make_bool3(lhs.x && rhs, lhs.y && rhs, lhs.z && rhs); }
[[nodiscard]] inline __device__ constexpr auto operator&&(lc_bool lhs, lc_bool3 rhs) noexcept { return lc_make_bool3(lhs && rhs.x, lhs && rhs.y, lhs && rhs.z); }
[[nodiscard]] inline __device__ constexpr auto operator&&(lc_bool4 lhs, lc_bool4 rhs) noexcept { return lc_make_bool4(lhs.x && rhs.x, lhs.y && rhs.y, lhs.z && rhs.z, lhs.w && rhs.w); }
[[nodiscard]] inline __device__ constexpr auto operator&&(lc_bool4 lhs, lc_bool rhs) noexcept { return lc_make_bool4(lhs.x && rhs, lhs.y && rhs, lhs.z && rhs, lhs.w && rhs); }
[[nodiscard]] inline __device__ constexpr auto operator&&(lc_bool lhs, lc_bool4 rhs) noexcept { return lc_make_bool4(lhs && rhs.x, lhs && rhs.y, lhs && rhs.z, lhs && rhs.w); }

[[nodiscard]] __device__ inline constexpr auto lc_any(lc_bool2 v) noexcept { return v.x || v.y; }
[[nodiscard]] __device__ inline constexpr auto lc_any(lc_bool3 v) noexcept { return v.x || v.y || v.z; }
[[nodiscard]] __device__ inline constexpr auto lc_any(lc_bool4 v) noexcept { return v.x || v.y || v.z || v.w; }
[[nodiscard]] __device__ inline constexpr auto lc_all(lc_bool2 v) noexcept { return v.x && v.y; }
[[nodiscard]] __device__ inline constexpr auto lc_all(lc_bool3 v) noexcept { return v.x && v.y && v.z; }
[[nodiscard]] __device__ inline constexpr auto lc_all(lc_bool4 v) noexcept { return v.x && v.y && v.z && v.w; }
[[nodiscard]] __device__ inline constexpr auto lc_none(lc_bool2 v) noexcept { return !v.x && !v.y; }
[[nodiscard]] __device__ inline constexpr auto lc_none(lc_bool3 v) noexcept { return !v.x && !v.y && !v.z; }
[[nodiscard]] __device__ inline constexpr auto lc_none(lc_bool4 v) noexcept { return !v.x && !v.y && !v.z && !v.w; }

struct lc_float2x2 {
lc_float2 cols[2];
__device__ inline constexpr lc_float2x2() noexcept : cols{} {}
__device__ inline explicit constexpr lc_float2x2(lc_float s) noexcept
    : cols{lc_make_float2(s, 0.0f), lc_make_float2(0.0f, s)} {}
__device__ inline constexpr static auto full(lc_float s) noexcept { return lc_float2x2{lc_float2(s), lc_float2(s)}; }
__device__ inline constexpr static auto zero() noexcept { return lc_float2x2{lc_float2::zero(), lc_float2::zero()}; }
__device__ inline constexpr static auto one() noexcept { return lc_float2x2{lc_float2::one(), lc_float2::one()}; }
__device__ inline constexpr lc_float2x2(lc_float2 c0, lc_float2 c1) noexcept
    : cols{c0, c1} {}
[[nodiscard]] __device__ inline constexpr auto &operator[](lc_uint i) noexcept { return cols[i]; }
[[nodiscard]] __device__ inline constexpr auto operator[](lc_uint i) const noexcept { return cols[i]; }
[[nodiscard]] __device__ inline constexpr auto comp_mul(const lc_float2x2 &rhs) const noexcept { return lc_float2x2{cols[0] * rhs[0], cols[1] * rhs[1]}; }
};

struct lc_float3x3 {
lc_float3 cols[3];
__device__ inline constexpr lc_float3x3() noexcept : cols{} {}
__device__ inline explicit constexpr lc_float3x3(lc_float s) noexcept
    : cols{lc_make_float3(s, 0.0f, 0.0f), lc_make_float3(0.0f, s, 0.0f), lc_make_float3(0.0f, 0.0f, s)} {}
__device__ inline constexpr static auto full(lc_float s) noexcept { return lc_float3x3{lc_float3(s), lc_float3(s), lc_float3(s)}; }
__device__ inline constexpr static auto zero() noexcept { return lc_float3x3{lc_float3::zero(), lc_float3::zero(), lc_float3::zero()}; }
__device__ inline constexpr static auto one() noexcept { return lc_float3x3{lc_float3::one(), lc_float3::one(), lc_float3::one()}; }
__device__ inline constexpr lc_float3x3(lc_float3 c0, lc_float3 c1, lc_float3 c2) noexcept
    : cols{c0, c1, c2} {}
[[nodiscard]] __device__ inline constexpr auto &operator[](lc_uint i) noexcept { return cols[i]; }
[[nodiscard]] __device__ inline constexpr auto operator[](lc_uint i) const noexcept { return cols[i]; }
[[nodiscard]] __device__ inline constexpr auto comp_mul(const lc_float3x3 &rhs) const noexcept { return lc_float3x3{cols[0] * rhs[0], cols[1] * rhs[1], cols[2] * rhs[2]}; }
};

struct lc_float4x4 {
lc_float4 cols[4];
__device__ inline constexpr lc_float4x4() noexcept : cols{} {}
__device__ inline explicit constexpr lc_float4x4(lc_float s) noexcept
    : cols{lc_make_float4(s, 0.0f, 0.0f, 0.0f), lc_make_float4(0.0f, s, 0.0f, 0.0f), lc_make_float4(0.0f, 0.0f, s, 0.0f), lc_make_float4(0.0f, 0.0f, 0.0f, s)} {}
__device__ inline constexpr static auto full(lc_float s) noexcept { return lc_float4x4{lc_float4(s), lc_float4(s), lc_float4(s), lc_float4(s)}; }
__device__ inline constexpr static auto zero() noexcept { return lc_float4x4{lc_float4::zero(), lc_float4::zero(), lc_float4::zero(), lc_float4::zero()}; }
__device__ inline constexpr static auto one() noexcept { return lc_float4x4{lc_float4::one(), lc_float4::one(), lc_float4::one(), lc_float4::one()}; }
__device__ inline constexpr lc_float4x4(lc_float4 c0, lc_float4 c1, lc_float4 c2, lc_float4 c3) noexcept
    : cols{c0, c1, c2, c3} {}
[[nodiscard]] __device__ inline constexpr auto &operator[](lc_uint i) noexcept { return cols[i]; }
[[nodiscard]] __device__ inline constexpr auto operator[](lc_uint i) const noexcept { return cols[i]; }
[[nodiscard]] __device__ inline constexpr auto comp_mul(const lc_float4x4 &rhs) const noexcept { return lc_float4x4{cols[0] * rhs[0], cols[1] * rhs[1], cols[2] * rhs[2], cols[3] * rhs[3]}; }
};

[[nodiscard]] __device__ inline constexpr auto operator*(const lc_float2x2 m, lc_float s) noexcept { return lc_float2x2{m[0] * s, m[1] * s}; }
[[nodiscard]] __device__ inline constexpr auto operator*(lc_float s, const lc_float2x2 m) noexcept { return m * s; }
[[nodiscard]] __device__ inline constexpr auto operator/(const lc_float2x2 m, lc_float s) noexcept { return m * (1.0f / s); }
[[nodiscard]] __device__ inline constexpr auto operator*(const lc_float2x2 m, const lc_float2 v) noexcept { return v.x * m[0] + v.y * m[1]; }
[[nodiscard]] __device__ inline constexpr auto operator*(const lc_float2x2 lhs, const lc_float2x2 rhs) noexcept { return lc_float2x2{lhs * rhs[0], lhs * rhs[1]}; }
[[nodiscard]] __device__ inline constexpr auto operator+(const lc_float2x2 lhs, const lc_float2x2 rhs) noexcept { return lc_float2x2{lhs[0] + rhs[0], lhs[1] + rhs[1]}; }
[[nodiscard]] __device__ inline constexpr auto operator-(const lc_float2x2 lhs, const lc_float2x2 rhs) noexcept { return lc_float2x2{lhs[0] - rhs[0], lhs[1] - rhs[1]}; }

[[nodiscard]] __device__ inline constexpr auto operator*(const lc_float3x3 m, lc_float s) noexcept { return lc_float3x3{m[0] * s, m[1] * s, m[2] * s}; }
[[nodiscard]] __device__ inline constexpr auto operator*(lc_float s, const lc_float3x3 m) noexcept { return m * s; }
[[nodiscard]] __device__ inline constexpr auto operator/(const lc_float3x3 m, lc_float s) noexcept { return m * (1.0f / s); }
[[nodiscard]] __device__ inline constexpr auto operator*(const lc_float3x3 m, const lc_float3 v) noexcept { return v.x * m[0] + v.y * m[1] + v.z * m[2]; }
[[nodiscard]] __device__ inline constexpr auto operator*(const lc_float3x3 lhs, const lc_float3x3 rhs) noexcept { return lc_float3x3{lhs * rhs[0], lhs * rhs[1], lhs * rhs[2]}; }
[[nodiscard]] __device__ inline constexpr auto operator+(const lc_float3x3 lhs, const lc_float3x3 rhs) noexcept { return lc_float3x3{lhs[0] + rhs[0], lhs[1] + rhs[1], lhs[2] + rhs[2]}; }
[[nodiscard]] __device__ inline constexpr auto operator-(const lc_float3x3 lhs, const lc_float3x3 rhs) noexcept { return lc_float3x3{lhs[0] - rhs[0], lhs[1] - rhs[1], lhs[2] - rhs[2]}; }

[[nodiscard]] __device__ inline constexpr auto operator*(const lc_float4x4 m, lc_float s) noexcept { return lc_float4x4{m[0] * s, m[1] * s, m[2] * s, m[3] * s}; }
[[nodiscard]] __device__ inline constexpr auto operator*(lc_float s, const lc_float4x4 m) noexcept { return m * s; }
[[nodiscard]] __device__ inline constexpr auto operator/(const lc_float4x4 m, lc_float s) noexcept { return m * (1.0f / s); }
[[nodiscard]] __device__ inline constexpr auto operator*(const lc_float4x4 m, const lc_float4 v) noexcept { return v.x * m[0] + v.y * m[1] + v.z * m[2] + v.w * m[3]; }
[[nodiscard]] __device__ inline constexpr auto operator*(const lc_float4x4 lhs, const lc_float4x4 rhs) noexcept { return lc_float4x4{lhs * rhs[0], lhs * rhs[1], lhs * rhs[2], lhs * rhs[3]}; }
[[nodiscard]] __device__ inline constexpr auto operator+(const lc_float4x4 lhs, const lc_float4x4 rhs) noexcept { return lc_float4x4{lhs[0] + rhs[0], lhs[1] + rhs[1], lhs[2] + rhs[2], lhs[3] + rhs[3]}; }
[[nodiscard]] __device__ inline constexpr auto operator-(const lc_float4x4 lhs, const lc_float4x4 rhs) noexcept { return lc_float4x4{lhs[0] - rhs[0], lhs[1] - rhs[1], lhs[2] - rhs[2], lhs[3] - rhs[3]}; }

[[nodiscard]] __device__ inline constexpr auto lc_make_float2x2(lc_float s = 1.0f) noexcept { return lc_float2x2{lc_make_float2(s, 0.0f), lc_make_float2(0.0f, s)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_float2x2(lc_float m00, lc_float m01, lc_float m10, lc_float m11) noexcept { return lc_float2x2{lc_make_float2(m00, m01), lc_make_float2(m10, m11)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_float2x2(lc_float2 c0, lc_float2 c1) noexcept { return lc_float2x2{c0, c1}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_float2x2(lc_float2x2 m) noexcept { return m; }
[[nodiscard]] __device__ inline constexpr auto lc_make_float2x2(lc_float3x3 m) noexcept { return lc_float2x2{lc_make_float2(m[0]), lc_make_float2(m[1])}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_float2x2(lc_float4x4 m) noexcept { return lc_float2x2{lc_make_float2(m[0]), lc_make_float2(m[1])}; }

[[nodiscard]] __device__ inline constexpr auto lc_make_float3x3(lc_float s = 1.0f) noexcept { return lc_float3x3{lc_make_float3(s, 0.0f, 0.0f), lc_make_float3(0.0f, s, 0.0f), lc_make_float3(0.0f, 0.0f, s)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_float3x3(lc_float m00, lc_float m01, lc_float m02, lc_float m10, lc_float m11, lc_float m12, lc_float m20, lc_float m21, lc_float m22) noexcept { return lc_float3x3{lc_make_float3(m00, m01, m02), lc_make_float3(m10, m11, m12), lc_make_float3(m20, m21, m22)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_float3x3(lc_float3 c0, lc_float3 c1, lc_float3 c2) noexcept { return lc_float3x3{c0, c1, c2}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_float3x3(lc_float2x2 m) noexcept { return lc_float3x3{lc_make_float3(m[0], 0.0f), lc_make_float3(m[1], 0.0f), lc_make_float3(0.0f, 0.0f, 1.0f)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_float3x3(lc_float3x3 m) noexcept { return m; }
[[nodiscard]] __device__ inline constexpr auto lc_make_float3x3(lc_float4x4 m) noexcept { return lc_float3x3{lc_make_float3(m[0]), lc_make_float3(m[1]), lc_make_float3(m[2])}; }

[[nodiscard]] __device__ inline constexpr auto lc_make_float4x4(lc_float s = 1.0f) noexcept { return lc_float4x4{lc_make_float4(s, 0.0f, 0.0f, 0.0f), lc_make_float4(0.0f, s, 0.0f, 0.0f), lc_make_float4(0.0f, 0.0f, s, 0.0f), lc_make_float4(0.0f, 0.0f, 0.0f, s)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_float4x4(lc_float m00, lc_float m01, lc_float m02, lc_float m03, lc_float m10, lc_float m11, lc_float m12, lc_float m13, lc_float m20, lc_float m21, lc_float m22, lc_float m23, lc_float m30, lc_float m31, lc_float m32, lc_float m33) noexcept { return lc_float4x4{lc_make_float4(m00, m01, m02, m03), lc_make_float4(m10, m11, m12, m13), lc_make_float4(m20, m21, m22, m23), lc_make_float4(m30, m31, m32, m33)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_float4x4(lc_float4 c0, lc_float4 c1, lc_float4 c2, lc_float4 c3) noexcept { return lc_float4x4{c0, c1, c2, c3}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_float4x4(lc_float2x2 m) noexcept { return lc_float4x4{lc_make_float4(m[0], 0.0f, 0.0f), lc_make_float4(m[1], 0.0f, 0.0f), lc_make_float4(0.0f, 0.0f, 0.0f, 0.0f), lc_make_float4(0.0f, 0.0f, 0.0f, 1.0f)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_float4x4(lc_float3x3 m) noexcept { return lc_float4x4{lc_make_float4(m[0], 0.0f), lc_make_float4(m[1], 0.0f), lc_make_float4(m[2], 0.0f), lc_make_float4(0.0f, 0.0f, 0.0f, 1.0f)}; }
[[nodiscard]] __device__ inline constexpr auto lc_make_float4x4(lc_float4x4 m) noexcept { return m; }

template<typename T>
[[nodiscard]] __device__ inline auto lc_select(T f, T t, bool p) noexcept { return p ? t : f; }
[[nodiscard]] __device__ inline auto lc_select(lc_short2 f, lc_short2 t, lc_bool2 p) noexcept { return lc_make_short2(lc_select<lc_short>(f.x, t.x, p.x), lc_select<lc_short>(f.y, t.y, p.y)); }
[[nodiscard]] __device__ inline auto lc_select(lc_short3 f, lc_short3 t, lc_bool3 p) noexcept { return lc_make_short3(lc_select<lc_short>(f.x, t.x, p.x), lc_select<lc_short>(f.y, t.y, p.y), lc_select<lc_short>(f.z, t.z, p.z)); }
[[nodiscard]] __device__ inline auto lc_select(lc_short4 f, lc_short4 t, lc_bool4 p) noexcept { return lc_make_short4(lc_select<lc_short>(f.x, t.x, p.x), lc_select<lc_short>(f.y, t.y, p.y), lc_select<lc_short>(f.z, t.z, p.z), lc_select<lc_short>(f.w, t.w, p.w)); }
[[nodiscard]] __device__ inline auto lc_select(lc_ushort2 f, lc_ushort2 t, lc_bool2 p) noexcept { return lc_make_ushort2(lc_select<lc_ushort>(f.x, t.x, p.x), lc_select<lc_ushort>(f.y, t.y, p.y)); }
[[nodiscard]] __device__ inline auto lc_select(lc_ushort3 f, lc_ushort3 t, lc_bool3 p) noexcept { return lc_make_ushort3(lc_select<lc_ushort>(f.x, t.x, p.x), lc_select<lc_ushort>(f.y, t.y, p.y), lc_select<lc_ushort>(f.z, t.z, p.z)); }
[[nodiscard]] __device__ inline auto lc_select(lc_ushort4 f, lc_ushort4 t, lc_bool4 p) noexcept { return lc_make_ushort4(lc_select<lc_ushort>(f.x, t.x, p.x), lc_select<lc_ushort>(f.y, t.y, p.y), lc_select<lc_ushort>(f.z, t.z, p.z), lc_select<lc_ushort>(f.w, t.w, p.w)); }
[[nodiscard]] __device__ inline auto lc_select(lc_int2 f, lc_int2 t, lc_bool2 p) noexcept { return lc_make_int2(lc_select<lc_int>(f.x, t.x, p.x), lc_select<lc_int>(f.y, t.y, p.y)); }
[[nodiscard]] __device__ inline auto lc_select(lc_int3 f, lc_int3 t, lc_bool3 p) noexcept { return lc_make_int3(lc_select<lc_int>(f.x, t.x, p.x), lc_select<lc_int>(f.y, t.y, p.y), lc_select<lc_int>(f.z, t.z, p.z)); }
[[nodiscard]] __device__ inline auto lc_select(lc_int4 f, lc_int4 t, lc_bool4 p) noexcept { return lc_make_int4(lc_select<lc_int>(f.x, t.x, p.x), lc_select<lc_int>(f.y, t.y, p.y), lc_select<lc_int>(f.z, t.z, p.z), lc_select<lc_int>(f.w, t.w, p.w)); }
[[nodiscard]] __device__ inline auto lc_select(lc_uint2 f, lc_uint2 t, lc_bool2 p) noexcept { return lc_make_uint2(lc_select<lc_uint>(f.x, t.x, p.x), lc_select<lc_uint>(f.y, t.y, p.y)); }
[[nodiscard]] __device__ inline auto lc_select(lc_uint3 f, lc_uint3 t, lc_bool3 p) noexcept { return lc_make_uint3(lc_select<lc_uint>(f.x, t.x, p.x), lc_select<lc_uint>(f.y, t.y, p.y), lc_select<lc_uint>(f.z, t.z, p.z)); }
[[nodiscard]] __device__ inline auto lc_select(lc_uint4 f, lc_uint4 t, lc_bool4 p) noexcept { return lc_make_uint4(lc_select<lc_uint>(f.x, t.x, p.x), lc_select<lc_uint>(f.y, t.y, p.y), lc_select<lc_uint>(f.z, t.z, p.z), lc_select<lc_uint>(f.w, t.w, p.w)); }
[[nodiscard]] __device__ inline auto lc_select(lc_half2 f, lc_half2 t, lc_bool2 p) noexcept { return lc_make_half2(lc_select<lc_half>(f.x, t.x, p.x), lc_select<lc_half>(f.y, t.y, p.y)); }
[[nodiscard]] __device__ inline auto lc_select(lc_half3 f, lc_half3 t, lc_bool3 p) noexcept { return lc_make_half3(lc_select<lc_half>(f.x, t.x, p.x), lc_select<lc_half>(f.y, t.y, p.y), lc_select<lc_half>(f.z, t.z, p.z)); }
[[nodiscard]] __device__ inline auto lc_select(lc_half4 f, lc_half4 t, lc_bool4 p) noexcept { return lc_make_half4(lc_select<lc_half>(f.x, t.x, p.x), lc_select<lc_half>(f.y, t.y, p.y), lc_select<lc_half>(f.z, t.z, p.z), lc_select<lc_half>(f.w, t.w, p.w)); }
[[nodiscard]] __device__ inline auto lc_select(lc_float2 f, lc_float2 t, lc_bool2 p) noexcept { return lc_make_float2(lc_select<lc_float>(f.x, t.x, p.x), lc_select<lc_float>(f.y, t.y, p.y)); }
[[nodiscard]] __device__ inline auto lc_select(lc_float3 f, lc_float3 t, lc_bool3 p) noexcept { return lc_make_float3(lc_select<lc_float>(f.x, t.x, p.x), lc_select<lc_float>(f.y, t.y, p.y), lc_select<lc_float>(f.z, t.z, p.z)); }
[[nodiscard]] __device__ inline auto lc_select(lc_float4 f, lc_float4 t, lc_bool4 p) noexcept { return lc_make_float4(lc_select<lc_float>(f.x, t.x, p.x), lc_select<lc_float>(f.y, t.y, p.y), lc_select<lc_float>(f.z, t.z, p.z), lc_select<lc_float>(f.w, t.w, p.w)); }
[[nodiscard]] __device__ inline auto lc_select(lc_bool2 f, lc_bool2 t, lc_bool2 p) noexcept { return lc_make_bool2(lc_select<lc_bool>(f.x, t.x, p.x), lc_select<lc_bool>(f.y, t.y, p.y)); }
[[nodiscard]] __device__ inline auto lc_select(lc_bool3 f, lc_bool3 t, lc_bool3 p) noexcept { return lc_make_bool3(lc_select<lc_bool>(f.x, t.x, p.x), lc_select<lc_bool>(f.y, t.y, p.y), lc_select<lc_bool>(f.z, t.z, p.z)); }
[[nodiscard]] __device__ inline auto lc_select(lc_bool4 f, lc_bool4 t, lc_bool4 p) noexcept { return lc_make_bool4(lc_select<lc_bool>(f.x, t.x, p.x), lc_select<lc_bool>(f.y, t.y, p.y), lc_select<lc_bool>(f.z, t.z, p.z), lc_select<lc_bool>(f.w, t.w, p.w)); }
[[nodiscard]] __device__ inline auto lc_select(lc_long2 f, lc_long2 t, lc_bool2 p) noexcept { return lc_make_long2(lc_select<lc_long>(f.x, t.x, p.x), lc_select<lc_long>(f.y, t.y, p.y)); }
[[nodiscard]] __device__ inline auto lc_select(lc_long3 f, lc_long3 t, lc_bool3 p) noexcept { return lc_make_long3(lc_select<lc_long>(f.x, t.x, p.x), lc_select<lc_long>(f.y, t.y, p.y), lc_select<lc_long>(f.z, t.z, p.z)); }
[[nodiscard]] __device__ inline auto lc_select(lc_long4 f, lc_long4 t, lc_bool4 p) noexcept { return lc_make_long4(lc_select<lc_long>(f.x, t.x, p.x), lc_select<lc_long>(f.y, t.y, p.y), lc_select<lc_long>(f.z, t.z, p.z), lc_select<lc_long>(f.w, t.w, p.w)); }
[[nodiscard]] __device__ inline auto lc_select(lc_ulong2 f, lc_ulong2 t, lc_bool2 p) noexcept { return lc_make_ulong2(lc_select<lc_ulong>(f.x, t.x, p.x), lc_select<lc_ulong>(f.y, t.y, p.y)); }
[[nodiscard]] __device__ inline auto lc_select(lc_ulong3 f, lc_ulong3 t, lc_bool3 p) noexcept { return lc_make_ulong3(lc_select<lc_ulong>(f.x, t.x, p.x), lc_select<lc_ulong>(f.y, t.y, p.y), lc_select<lc_ulong>(f.z, t.z, p.z)); }
[[nodiscard]] __device__ inline auto lc_select(lc_ulong4 f, lc_ulong4 t, lc_bool4 p) noexcept { return lc_make_ulong4(lc_select<lc_ulong>(f.x, t.x, p.x), lc_select<lc_ulong>(f.y, t.y, p.y), lc_select<lc_ulong>(f.z, t.z, p.z), lc_select<lc_ulong>(f.w, t.w, p.w)); }

[[nodiscard]] __device__ inline auto lc_outer_product(lc_float2 a, lc_float2 b) noexcept { return lc_float2x2(a * b.x, a * b.y); }
[[nodiscard]] __device__ inline auto lc_outer_product(lc_float3 a, lc_float3 b) noexcept { return lc_float3x3(a * b.x, a * b.y, a * b.z); }
[[nodiscard]] __device__ inline auto lc_outer_product(lc_float4 a, lc_float4 b) noexcept { return lc_float4x4(a * b.x, a * b.y, a * b.z, a * b.w); }
[[nodiscard]] __device__ inline lc_float lc_min(lc_float a, lc_float b) noexcept { return fminf(a, b); }
[[nodiscard]] __device__ inline lc_float2 lc_min(lc_float2 a, lc_float2 b) noexcept { return lc_make_float2(fminf(a.x, b.x), fminf(a.y, b.y)); }
[[nodiscard]] __device__ inline lc_float3 lc_min(lc_float3 a, lc_float3 b) noexcept { return lc_make_float3(fminf(a.x, b.x), fminf(a.y, b.y), fminf(a.z, b.z)); }
[[nodiscard]] __device__ inline lc_float4 lc_min(lc_float4 a, lc_float4 b) noexcept { return lc_make_float4(fminf(a.x, b.x), fminf(a.y, b.y), fminf(a.z, b.z), fminf(a.w, b.w)); }

[[nodiscard]] __device__ inline lc_half lc_min(lc_half a, lc_half b) noexcept { return __hmin(a, b); }
[[nodiscard]] __device__ inline lc_half2 lc_min(lc_half2 a, lc_half2 b) noexcept { return lc_make_half2(__hmin(a.x, b.x), __hmin(a.y, b.y)); }
[[nodiscard]] __device__ inline lc_half3 lc_min(lc_half3 a, lc_half3 b) noexcept { return lc_make_half3(__hmin(a.x, b.x), __hmin(a.y, b.y), __hmin(a.z, b.z)); }
[[nodiscard]] __device__ inline lc_half4 lc_min(lc_half4 a, lc_half4 b) noexcept { return lc_make_half4(__hmin(a.x, b.x), __hmin(a.y, b.y), __hmin(a.z, b.z), __hmin(a.w, b.w)); }

[[nodiscard]] __device__ inline lc_float lc_max(lc_float a, lc_float b) noexcept { return fmaxf(a, b); }
[[nodiscard]] __device__ inline lc_float2 lc_max(lc_float2 a, lc_float2 b) noexcept { return lc_make_float2(fmaxf(a.x, b.x), fmaxf(a.y, b.y)); }
[[nodiscard]] __device__ inline lc_float3 lc_max(lc_float3 a, lc_float3 b) noexcept { return lc_make_float3(fmaxf(a.x, b.x), fmaxf(a.y, b.y), fmaxf(a.z, b.z)); }
[[nodiscard]] __device__ inline lc_float4 lc_max(lc_float4 a, lc_float4 b) noexcept { return lc_make_float4(fmaxf(a.x, b.x), fmaxf(a.y, b.y), fmaxf(a.z, b.z), fmaxf(a.w, b.w)); }

[[nodiscard]] __device__ inline lc_half lc_max(lc_half a, lc_half b) noexcept { return __hmax(a, b); }
[[nodiscard]] __device__ inline lc_half2 lc_max(lc_half2 a, lc_half2 b) noexcept { return lc_make_half2(__hmax(a.x, b.x), __hmax(a.y, b.y)); }
[[nodiscard]] __device__ inline lc_half3 lc_max(lc_half3 a, lc_half3 b) noexcept { return lc_make_half3(__hmax(a.x, b.x), __hmax(a.y, b.y), __hmax(a.z, b.z)); }
[[nodiscard]] __device__ inline lc_half4 lc_max(lc_half4 a, lc_half4 b) noexcept { return lc_make_half4(__hmax(a.x, b.x), __hmax(a.y, b.y), __hmax(a.z, b.z), __hmax(a.w, b.w)); }

[[nodiscard]] __device__ inline lc_float lc_abs(lc_float x) noexcept { return fabsf(x); }
[[nodiscard]] __device__ inline lc_float2 lc_abs(lc_float2 x) noexcept { return lc_make_float2(fabsf(x.x), fabsf(x.y)); }
[[nodiscard]] __device__ inline lc_float3 lc_abs(lc_float3 x) noexcept { return lc_make_float3(fabsf(x.x), fabsf(x.y), fabsf(x.z)); }
[[nodiscard]] __device__ inline lc_float4 lc_abs(lc_float4 x) noexcept { return lc_make_float4(fabsf(x.x), fabsf(x.y), fabsf(x.z), fabsf(x.w)); }

[[nodiscard]] __device__ inline lc_int lc_abs(lc_int x) noexcept { return abs(x); }
[[nodiscard]] __device__ inline lc_int2 lc_abs(lc_int2 x) noexcept { return lc_make_int2(abs(x.x), abs(x.y)); }
[[nodiscard]] __device__ inline lc_int3 lc_abs(lc_int3 x) noexcept { return lc_make_int3(abs(x.x), abs(x.y), abs(x.z)); }
[[nodiscard]] __device__ inline lc_int4 lc_abs(lc_int4 x) noexcept { return lc_make_int4(abs(x.x), abs(x.y), abs(x.z), abs(x.w)); }

[[nodiscard]] __device__ inline lc_long lc_abs(lc_long x) noexcept { return llabs(x); }
[[nodiscard]] __device__ inline lc_long2 lc_abs(lc_long2 x) noexcept { return lc_make_long2(llabs(x.x), llabs(x.y)); }
[[nodiscard]] __device__ inline lc_long3 lc_abs(lc_long3 x) noexcept { return lc_make_long3(llabs(x.x), llabs(x.y), llabs(x.z)); }
[[nodiscard]] __device__ inline lc_long4 lc_abs(lc_long4 x) noexcept { return lc_make_long4(llabs(x.x), llabs(x.y), llabs(x.z), llabs(x.w)); }

[[nodiscard]] __device__ inline lc_half lc_abs(lc_half x) noexcept { return __habs(x); }
[[nodiscard]] __device__ inline lc_half2 lc_abs(lc_half2 x) noexcept { return lc_make_half2(__habs(x.x), __habs(x.y)); }
[[nodiscard]] __device__ inline lc_half3 lc_abs(lc_half3 x) noexcept { return lc_make_half3(__habs(x.x), __habs(x.y), __habs(x.z)); }
[[nodiscard]] __device__ inline lc_half4 lc_abs(lc_half4 x) noexcept { return lc_make_half4(__habs(x.x), __habs(x.y), __habs(x.z), __habs(x.w)); }

[[nodiscard]] __device__ inline lc_half lc_acos(lc_half x) noexcept { return acosf(x); }
[[nodiscard]] __device__ inline lc_half2 lc_acos(lc_half2 x) noexcept { return lc_make_half2(acosf(x.x), acosf(x.y)); }
[[nodiscard]] __device__ inline lc_half3 lc_acos(lc_half3 x) noexcept { return lc_make_half3(acosf(x.x), acosf(x.y), acosf(x.z)); }
[[nodiscard]] __device__ inline lc_half4 lc_acos(lc_half4 x) noexcept { return lc_make_half4(acosf(x.x), acosf(x.y), acosf(x.z), acosf(x.w)); }
[[nodiscard]] __device__ inline lc_float lc_acos(lc_float x) noexcept { return acosf(x); }
[[nodiscard]] __device__ inline lc_float2 lc_acos(lc_float2 x) noexcept { return lc_make_float2(acosf(x.x), acosf(x.y)); }
[[nodiscard]] __device__ inline lc_float3 lc_acos(lc_float3 x) noexcept { return lc_make_float3(acosf(x.x), acosf(x.y), acosf(x.z)); }
[[nodiscard]] __device__ inline lc_float4 lc_acos(lc_float4 x) noexcept { return lc_make_float4(acosf(x.x), acosf(x.y), acosf(x.z), acosf(x.w)); }

[[nodiscard]] __device__ inline lc_half lc_asin(lc_half x) noexcept { return asinf(x); }
[[nodiscard]] __device__ inline lc_half2 lc_asin(lc_half2 x) noexcept { return lc_make_half2(asinf(x.x), asinf(x.y)); }
[[nodiscard]] __device__ inline lc_half3 lc_asin(lc_half3 x) noexcept { return lc_make_half3(asinf(x.x), asinf(x.y), asinf(x.z)); }
[[nodiscard]] __device__ inline lc_half4 lc_asin(lc_half4 x) noexcept { return lc_make_half4(asinf(x.x), asinf(x.y), asinf(x.z), asinf(x.w)); }
[[nodiscard]] __device__ inline lc_float lc_asin(lc_float x) noexcept { return asinf(x); }
[[nodiscard]] __device__ inline lc_float2 lc_asin(lc_float2 x) noexcept { return lc_make_float2(asinf(x.x), asinf(x.y)); }
[[nodiscard]] __device__ inline lc_float3 lc_asin(lc_float3 x) noexcept { return lc_make_float3(asinf(x.x), asinf(x.y), asinf(x.z)); }
[[nodiscard]] __device__ inline lc_float4 lc_asin(lc_float4 x) noexcept { return lc_make_float4(asinf(x.x), asinf(x.y), asinf(x.z), asinf(x.w)); }

[[nodiscard]] __device__ inline lc_half lc_atan(lc_half x) noexcept { return atanf(x); }
[[nodiscard]] __device__ inline lc_half2 lc_atan(lc_half2 x) noexcept { return lc_make_half2(atanf(x.x), atanf(x.y)); }
[[nodiscard]] __device__ inline lc_half3 lc_atan(lc_half3 x) noexcept { return lc_make_half3(atanf(x.x), atanf(x.y), atanf(x.z)); }
[[nodiscard]] __device__ inline lc_half4 lc_atan(lc_half4 x) noexcept { return lc_make_half4(atanf(x.x), atanf(x.y), atanf(x.z), atanf(x.w)); }
[[nodiscard]] __device__ inline lc_float lc_atan(lc_float x) noexcept { return atanf(x); }
[[nodiscard]] __device__ inline lc_float2 lc_atan(lc_float2 x) noexcept { return lc_make_float2(atanf(x.x), atanf(x.y)); }
[[nodiscard]] __device__ inline lc_float3 lc_atan(lc_float3 x) noexcept { return lc_make_float3(atanf(x.x), atanf(x.y), atanf(x.z)); }
[[nodiscard]] __device__ inline lc_float4 lc_atan(lc_float4 x) noexcept { return lc_make_float4(atanf(x.x), atanf(x.y), atanf(x.z), atanf(x.w)); }

[[nodiscard]] __device__ inline lc_half lc_acosh(lc_half x) noexcept { return acoshf(x); }
[[nodiscard]] __device__ inline lc_half2 lc_acosh(lc_half2 x) noexcept { return lc_make_half2(acoshf(x.x), acoshf(x.y)); }
[[nodiscard]] __device__ inline lc_half3 lc_acosh(lc_half3 x) noexcept { return lc_make_half3(acoshf(x.x), acoshf(x.y), acoshf(x.z)); }
[[nodiscard]] __device__ inline lc_half4 lc_acosh(lc_half4 x) noexcept { return lc_make_half4(acoshf(x.x), acoshf(x.y), acoshf(x.z), acoshf(x.w)); }
[[nodiscard]] __device__ inline lc_float lc_acosh(lc_float x) noexcept { return acoshf(x); }
[[nodiscard]] __device__ inline lc_float2 lc_acosh(lc_float2 x) noexcept { return lc_make_float2(acoshf(x.x), acoshf(x.y)); }
[[nodiscard]] __device__ inline lc_float3 lc_acosh(lc_float3 x) noexcept { return lc_make_float3(acoshf(x.x), acoshf(x.y), acoshf(x.z)); }
[[nodiscard]] __device__ inline lc_float4 lc_acosh(lc_float4 x) noexcept { return lc_make_float4(acoshf(x.x), acoshf(x.y), acoshf(x.z), acoshf(x.w)); }

[[nodiscard]] __device__ inline lc_half lc_asinh(lc_half x) noexcept { return asinhf(x); }
[[nodiscard]] __device__ inline lc_half2 lc_asinh(lc_half2 x) noexcept { return lc_make_half2(asinhf(x.x), asinhf(x.y)); }
[[nodiscard]] __device__ inline lc_half3 lc_asinh(lc_half3 x) noexcept { return lc_make_half3(asinhf(x.x), asinhf(x.y), asinhf(x.z)); }
[[nodiscard]] __device__ inline lc_half4 lc_asinh(lc_half4 x) noexcept { return lc_make_half4(asinhf(x.x), asinhf(x.y), asinhf(x.z), asinhf(x.w)); }
[[nodiscard]] __device__ inline lc_float lc_asinh(lc_float x) noexcept { return asinhf(x); }
[[nodiscard]] __device__ inline lc_float2 lc_asinh(lc_float2 x) noexcept { return lc_make_float2(asinhf(x.x), asinhf(x.y)); }
[[nodiscard]] __device__ inline lc_float3 lc_asinh(lc_float3 x) noexcept { return lc_make_float3(asinhf(x.x), asinhf(x.y), asinhf(x.z)); }
[[nodiscard]] __device__ inline lc_float4 lc_asinh(lc_float4 x) noexcept { return lc_make_float4(asinhf(x.x), asinhf(x.y), asinhf(x.z), asinhf(x.w)); }

[[nodiscard]] __device__ inline lc_half lc_atanh(lc_half x) noexcept { return atanhf(x); }
[[nodiscard]] __device__ inline lc_half2 lc_atanh(lc_half2 x) noexcept { return lc_make_half2(atanhf(x.x), atanhf(x.y)); }
[[nodiscard]] __device__ inline lc_half3 lc_atanh(lc_half3 x) noexcept { return lc_make_half3(atanhf(x.x), atanhf(x.y), atanhf(x.z)); }
[[nodiscard]] __device__ inline lc_half4 lc_atanh(lc_half4 x) noexcept { return lc_make_half4(atanhf(x.x), atanhf(x.y), atanhf(x.z), atanhf(x.w)); }
[[nodiscard]] __device__ inline lc_float lc_atanh(lc_float x) noexcept { return atanhf(x); }
[[nodiscard]] __device__ inline lc_float2 lc_atanh(lc_float2 x) noexcept { return lc_make_float2(atanhf(x.x), atanhf(x.y)); }
[[nodiscard]] __device__ inline lc_float3 lc_atanh(lc_float3 x) noexcept { return lc_make_float3(atanhf(x.x), atanhf(x.y), atanhf(x.z)); }
[[nodiscard]] __device__ inline lc_float4 lc_atanh(lc_float4 x) noexcept { return lc_make_float4(atanhf(x.x), atanhf(x.y), atanhf(x.z), atanhf(x.w)); }

[[nodiscard]] __device__ inline lc_half lc_atan2(lc_half y, lc_half x) noexcept { return atan2f(y, x); }
[[nodiscard]] __device__ inline lc_half2 lc_atan2(lc_half2 y, lc_half2 x) noexcept { return lc_make_half2(atan2f(y.x, x.x), atan2f(y.y, x.y)); }
[[nodiscard]] __device__ inline lc_half3 lc_atan2(lc_half3 y, lc_half3 x) noexcept { return lc_make_half3(atan2f(y.x, x.x), atan2f(y.y, x.y), atan2f(y.z, x.z)); }
[[nodiscard]] __device__ inline lc_half4 lc_atan2(lc_half4 y, lc_half4 x) noexcept { return lc_make_half4(atan2f(y.x, x.x), atan2f(y.y, x.y), atan2f(y.z, x.z), atan2f(y.w, x.w)); }
[[nodiscard]] __device__ inline lc_float lc_atan2(lc_float y, lc_float x) noexcept { return atan2f(y, x); }
[[nodiscard]] __device__ inline lc_float2 lc_atan2(lc_float2 y, lc_float2 x) noexcept { return lc_make_float2(atan2f(y.x, x.x), atan2f(y.y, x.y)); }
[[nodiscard]] __device__ inline lc_float3 lc_atan2(lc_float3 y, lc_float3 x) noexcept { return lc_make_float3(atan2f(y.x, x.x), atan2f(y.y, x.y), atan2f(y.z, x.z)); }
[[nodiscard]] __device__ inline lc_float4 lc_atan2(lc_float4 y, lc_float4 x) noexcept { return lc_make_float4(atan2f(y.x, x.x), atan2f(y.y, x.y), atan2f(y.z, x.z), atan2f(y.w, x.w)); }

[[nodiscard]] __device__ inline lc_half lc_cosh(lc_half x) noexcept { return coshf(x); }
[[nodiscard]] __device__ inline lc_half2 lc_cosh(lc_half2 x) noexcept { return lc_make_half2(coshf(x.x), coshf(x.y)); }
[[nodiscard]] __device__ inline lc_half3 lc_cosh(lc_half3 x) noexcept { return lc_make_half3(coshf(x.x), coshf(x.y), coshf(x.z)); }
[[nodiscard]] __device__ inline lc_half4 lc_cosh(lc_half4 x) noexcept { return lc_make_half4(coshf(x.x), coshf(x.y), coshf(x.z), coshf(x.w)); }
[[nodiscard]] __device__ inline lc_float lc_cosh(lc_float x) noexcept { return coshf(x); }
[[nodiscard]] __device__ inline lc_float2 lc_cosh(lc_float2 x) noexcept { return lc_make_float2(coshf(x.x), coshf(x.y)); }
[[nodiscard]] __device__ inline lc_float3 lc_cosh(lc_float3 x) noexcept { return lc_make_float3(coshf(x.x), coshf(x.y), coshf(x.z)); }
[[nodiscard]] __device__ inline lc_float4 lc_cosh(lc_float4 x) noexcept { return lc_make_float4(coshf(x.x), coshf(x.y), coshf(x.z), coshf(x.w)); }

[[nodiscard]] __device__ inline lc_half lc_sinh(lc_half x) noexcept { return sinhf(x); }
[[nodiscard]] __device__ inline lc_half2 lc_sinh(lc_half2 x) noexcept { return lc_make_half2(sinhf(x.x), sinhf(x.y)); }
[[nodiscard]] __device__ inline lc_half3 lc_sinh(lc_half3 x) noexcept { return lc_make_half3(sinhf(x.x), sinhf(x.y), sinhf(x.z)); }
[[nodiscard]] __device__ inline lc_half4 lc_sinh(lc_half4 x) noexcept { return lc_make_half4(sinhf(x.x), sinhf(x.y), sinhf(x.z), sinhf(x.w)); }
[[nodiscard]] __device__ inline lc_float lc_sinh(lc_float x) noexcept { return sinhf(x); }
[[nodiscard]] __device__ inline lc_float2 lc_sinh(lc_float2 x) noexcept { return lc_make_float2(sinhf(x.x), sinhf(x.y)); }
[[nodiscard]] __device__ inline lc_float3 lc_sinh(lc_float3 x) noexcept { return lc_make_float3(sinhf(x.x), sinhf(x.y), sinhf(x.z)); }
[[nodiscard]] __device__ inline lc_float4 lc_sinh(lc_float4 x) noexcept { return lc_make_float4(sinhf(x.x), sinhf(x.y), sinhf(x.z), sinhf(x.w)); }

[[nodiscard]] __device__ inline lc_half lc_tanh(lc_half x) noexcept { return tanhf(x); }
[[nodiscard]] __device__ inline lc_half2 lc_tanh(lc_half2 x) noexcept { return lc_make_half2(tanhf(x.x), tanhf(x.y)); }
[[nodiscard]] __device__ inline lc_half3 lc_tanh(lc_half3 x) noexcept { return lc_make_half3(tanhf(x.x), tanhf(x.y), tanhf(x.z)); }
[[nodiscard]] __device__ inline lc_half4 lc_tanh(lc_half4 x) noexcept { return lc_make_half4(tanhf(x.x), tanhf(x.y), tanhf(x.z), tanhf(x.w)); }
[[nodiscard]] __device__ inline lc_float lc_tanh(lc_float x) noexcept { return tanhf(x); }
[[nodiscard]] __device__ inline lc_float2 lc_tanh(lc_float2 x) noexcept { return lc_make_float2(tanhf(x.x), tanhf(x.y)); }
[[nodiscard]] __device__ inline lc_float3 lc_tanh(lc_float3 x) noexcept { return lc_make_float3(tanhf(x.x), tanhf(x.y), tanhf(x.z)); }
[[nodiscard]] __device__ inline lc_float4 lc_tanh(lc_float4 x) noexcept { return lc_make_float4(tanhf(x.x), tanhf(x.y), tanhf(x.z), tanhf(x.w)); }

[[nodiscard]] __device__ inline lc_half lc_cos(lc_half x) noexcept { return cosf(x); }
[[nodiscard]] __device__ inline lc_half2 lc_cos(lc_half2 x) noexcept { return lc_make_half2(cosf(x.x), cosf(x.y)); }
[[nodiscard]] __device__ inline lc_half3 lc_cos(lc_half3 x) noexcept { return lc_make_half3(cosf(x.x), cosf(x.y), cosf(x.z)); }
[[nodiscard]] __device__ inline lc_half4 lc_cos(lc_half4 x) noexcept { return lc_make_half4(cosf(x.x), cosf(x.y), cosf(x.z), cosf(x.w)); }
[[nodiscard]] __device__ inline lc_float lc_cos(lc_float x) noexcept { return cosf(x); }
[[nodiscard]] __device__ inline lc_float2 lc_cos(lc_float2 x) noexcept { return lc_make_float2(cosf(x.x), cosf(x.y)); }
[[nodiscard]] __device__ inline lc_float3 lc_cos(lc_float3 x) noexcept { return lc_make_float3(cosf(x.x), cosf(x.y), cosf(x.z)); }
[[nodiscard]] __device__ inline lc_float4 lc_cos(lc_float4 x) noexcept { return lc_make_float4(cosf(x.x), cosf(x.y), cosf(x.z), cosf(x.w)); }

[[nodiscard]] __device__ inline lc_half lc_sin(lc_half x) noexcept { return sinf(x); }
[[nodiscard]] __device__ inline lc_half2 lc_sin(lc_half2 x) noexcept { return lc_make_half2(sinf(x.x), sinf(x.y)); }
[[nodiscard]] __device__ inline lc_half3 lc_sin(lc_half3 x) noexcept { return lc_make_half3(sinf(x.x), sinf(x.y), sinf(x.z)); }
[[nodiscard]] __device__ inline lc_half4 lc_sin(lc_half4 x) noexcept { return lc_make_half4(sinf(x.x), sinf(x.y), sinf(x.z), sinf(x.w)); }
[[nodiscard]] __device__ inline lc_float lc_sin(lc_float x) noexcept { return sinf(x); }
[[nodiscard]] __device__ inline lc_float2 lc_sin(lc_float2 x) noexcept { return lc_make_float2(sinf(x.x), sinf(x.y)); }
[[nodiscard]] __device__ inline lc_float3 lc_sin(lc_float3 x) noexcept { return lc_make_float3(sinf(x.x), sinf(x.y), sinf(x.z)); }
[[nodiscard]] __device__ inline lc_float4 lc_sin(lc_float4 x) noexcept { return lc_make_float4(sinf(x.x), sinf(x.y), sinf(x.z), sinf(x.w)); }

[[nodiscard]] __device__ inline lc_half lc_tan(lc_half x) noexcept { return tanf(x); }
[[nodiscard]] __device__ inline lc_half2 lc_tan(lc_half2 x) noexcept { return lc_make_half2(tanf(x.x), tanf(x.y)); }
[[nodiscard]] __device__ inline lc_half3 lc_tan(lc_half3 x) noexcept { return lc_make_half3(tanf(x.x), tanf(x.y), tanf(x.z)); }
[[nodiscard]] __device__ inline lc_half4 lc_tan(lc_half4 x) noexcept { return lc_make_half4(tanf(x.x), tanf(x.y), tanf(x.z), tanf(x.w)); }
[[nodiscard]] __device__ inline lc_float lc_tan(lc_float x) noexcept { return tanf(x); }
[[nodiscard]] __device__ inline lc_float2 lc_tan(lc_float2 x) noexcept { return lc_make_float2(tanf(x.x), tanf(x.y)); }
[[nodiscard]] __device__ inline lc_float3 lc_tan(lc_float3 x) noexcept { return lc_make_float3(tanf(x.x), tanf(x.y), tanf(x.z)); }
[[nodiscard]] __device__ inline lc_float4 lc_tan(lc_float4 x) noexcept { return lc_make_float4(tanf(x.x), tanf(x.y), tanf(x.z), tanf(x.w)); }

[[nodiscard]] __device__ inline lc_half lc_exp(lc_half x) noexcept { return expf(x); }
[[nodiscard]] __device__ inline lc_half2 lc_exp(lc_half2 x) noexcept { return lc_make_half2(expf(x.x), expf(x.y)); }
[[nodiscard]] __device__ inline lc_half3 lc_exp(lc_half3 x) noexcept { return lc_make_half3(expf(x.x), expf(x.y), expf(x.z)); }
[[nodiscard]] __device__ inline lc_half4 lc_exp(lc_half4 x) noexcept { return lc_make_half4(expf(x.x), expf(x.y), expf(x.z), expf(x.w)); }
[[nodiscard]] __device__ inline lc_float lc_exp(lc_float x) noexcept { return expf(x); }
[[nodiscard]] __device__ inline lc_float2 lc_exp(lc_float2 x) noexcept { return lc_make_float2(expf(x.x), expf(x.y)); }
[[nodiscard]] __device__ inline lc_float3 lc_exp(lc_float3 x) noexcept { return lc_make_float3(expf(x.x), expf(x.y), expf(x.z)); }
[[nodiscard]] __device__ inline lc_float4 lc_exp(lc_float4 x) noexcept { return lc_make_float4(expf(x.x), expf(x.y), expf(x.z), expf(x.w)); }

[[nodiscard]] __device__ inline lc_float lc_exp2(lc_float x) noexcept { return exp2f(x); }
[[nodiscard]] __device__ inline lc_float2 lc_exp2(lc_float2 x) noexcept { return lc_make_float2(exp2f(x.x), exp2f(x.y)); }
[[nodiscard]] __device__ inline lc_float3 lc_exp2(lc_float3 x) noexcept { return lc_make_float3(exp2f(x.x), exp2f(x.y), exp2f(x.z)); }
[[nodiscard]] __device__ inline lc_float4 lc_exp2(lc_float4 x) noexcept { return lc_make_float4(exp2f(x.x), exp2f(x.y), exp2f(x.z), exp2f(x.w)); }

[[nodiscard]] __device__ inline lc_half lc_exp2(lc_half x) noexcept { return hexp2(x); }
[[nodiscard]] __device__ inline lc_half2 lc_exp2(lc_half2 x) noexcept { return lc_make_half2(hexp2(x.x), hexp2(x.y)); }
[[nodiscard]] __device__ inline lc_half3 lc_exp2(lc_half3 x) noexcept { return lc_make_half3(hexp2(x.x), hexp2(x.y), hexp2(x.z)); }
[[nodiscard]] __device__ inline lc_half4 lc_exp2(lc_half4 x) noexcept { return lc_make_half4(hexp2(x.x), hexp2(x.y), hexp2(x.z), hexp2(x.w)); }

[[nodiscard]] __device__ inline lc_half lc_exp10(lc_half x) noexcept { return exp10f(x); }
[[nodiscard]] __device__ inline lc_half2 lc_exp10(lc_half2 x) noexcept { return lc_make_half2(exp10f(x.x), exp10f(x.y)); }
[[nodiscard]] __device__ inline lc_half3 lc_exp10(lc_half3 x) noexcept { return lc_make_half3(exp10f(x.x), exp10f(x.y), exp10f(x.z)); }
[[nodiscard]] __device__ inline lc_half4 lc_exp10(lc_half4 x) noexcept { return lc_make_half4(exp10f(x.x), exp10f(x.y), exp10f(x.z), exp10f(x.w)); }
[[nodiscard]] __device__ inline lc_float lc_exp10(lc_float x) noexcept { return exp10f(x); }
[[nodiscard]] __device__ inline lc_float2 lc_exp10(lc_float2 x) noexcept { return lc_make_float2(exp10f(x.x), exp10f(x.y)); }
[[nodiscard]] __device__ inline lc_float3 lc_exp10(lc_float3 x) noexcept { return lc_make_float3(exp10f(x.x), exp10f(x.y), exp10f(x.z)); }
[[nodiscard]] __device__ inline lc_float4 lc_exp10(lc_float4 x) noexcept { return lc_make_float4(exp10f(x.x), exp10f(x.y), exp10f(x.z), exp10f(x.w)); }

[[nodiscard]] __device__ inline lc_half lc_log(lc_half x) noexcept { return logf(x); }
[[nodiscard]] __device__ inline lc_half2 lc_log(lc_half2 x) noexcept { return lc_make_half2(logf(x.x), logf(x.y)); }
[[nodiscard]] __device__ inline lc_half3 lc_log(lc_half3 x) noexcept { return lc_make_half3(logf(x.x), logf(x.y), logf(x.z)); }
[[nodiscard]] __device__ inline lc_half4 lc_log(lc_half4 x) noexcept { return lc_make_half4(logf(x.x), logf(x.y), logf(x.z), logf(x.w)); }
[[nodiscard]] __device__ inline lc_float lc_log(lc_float x) noexcept { return logf(x); }
[[nodiscard]] __device__ inline lc_float2 lc_log(lc_float2 x) noexcept { return lc_make_float2(logf(x.x), logf(x.y)); }
[[nodiscard]] __device__ inline lc_float3 lc_log(lc_float3 x) noexcept { return lc_make_float3(logf(x.x), logf(x.y), logf(x.z)); }
[[nodiscard]] __device__ inline lc_float4 lc_log(lc_float4 x) noexcept { return lc_make_float4(logf(x.x), logf(x.y), logf(x.z), logf(x.w)); }

[[nodiscard]] __device__ inline lc_half lc_log2(lc_half x) noexcept { return log2f(x); }
[[nodiscard]] __device__ inline lc_half2 lc_log2(lc_half2 x) noexcept { return lc_make_half2(log2f(x.x), log2f(x.y)); }
[[nodiscard]] __device__ inline lc_half3 lc_log2(lc_half3 x) noexcept { return lc_make_half3(log2f(x.x), log2f(x.y), log2f(x.z)); }
[[nodiscard]] __device__ inline lc_half4 lc_log2(lc_half4 x) noexcept { return lc_make_half4(log2f(x.x), log2f(x.y), log2f(x.z), log2f(x.w)); }
[[nodiscard]] __device__ inline lc_float lc_log2(lc_float x) noexcept { return log2f(x); }
[[nodiscard]] __device__ inline lc_float2 lc_log2(lc_float2 x) noexcept { return lc_make_float2(log2f(x.x), log2f(x.y)); }
[[nodiscard]] __device__ inline lc_float3 lc_log2(lc_float3 x) noexcept { return lc_make_float3(log2f(x.x), log2f(x.y), log2f(x.z)); }
[[nodiscard]] __device__ inline lc_float4 lc_log2(lc_float4 x) noexcept { return lc_make_float4(log2f(x.x), log2f(x.y), log2f(x.z), log2f(x.w)); }

[[nodiscard]] __device__ inline lc_half lc_log10(lc_half x) noexcept { return log10f(x); }
[[nodiscard]] __device__ inline lc_half2 lc_log10(lc_half2 x) noexcept { return lc_make_half2(log10f(x.x), log10f(x.y)); }
[[nodiscard]] __device__ inline lc_half3 lc_log10(lc_half3 x) noexcept { return lc_make_half3(log10f(x.x), log10f(x.y), log10f(x.z)); }
[[nodiscard]] __device__ inline lc_half4 lc_log10(lc_half4 x) noexcept { return lc_make_half4(log10f(x.x), log10f(x.y), log10f(x.z), log10f(x.w)); }
[[nodiscard]] __device__ inline lc_float lc_log10(lc_float x) noexcept { return log10f(x); }
[[nodiscard]] __device__ inline lc_float2 lc_log10(lc_float2 x) noexcept { return lc_make_float2(log10f(x.x), log10f(x.y)); }
[[nodiscard]] __device__ inline lc_float3 lc_log10(lc_float3 x) noexcept { return lc_make_float3(log10f(x.x), log10f(x.y), log10f(x.z)); }
[[nodiscard]] __device__ inline lc_float4 lc_log10(lc_float4 x) noexcept { return lc_make_float4(log10f(x.x), log10f(x.y), log10f(x.z), log10f(x.w)); }

[[nodiscard]] __device__ inline lc_half lc_pow(lc_half x, lc_half a) noexcept { return powf_impl(x, a); }
[[nodiscard]] __device__ inline lc_half2 lc_pow(lc_half2 x, lc_half2 a) noexcept { return lc_make_half2(powf_impl(x.x, a.x), powf_impl(x.y, a.y)); }
[[nodiscard]] __device__ inline lc_half3 lc_pow(lc_half3 x, lc_half3 a) noexcept { return lc_make_half3(powf_impl(x.x, a.x), powf_impl(x.y, a.y), powf_impl(x.z, a.z)); }
[[nodiscard]] __device__ inline lc_half4 lc_pow(lc_half4 x, lc_half4 a) noexcept { return lc_make_half4(powf_impl(x.x, a.x), powf_impl(x.y, a.y), powf_impl(x.z, a.z), powf_impl(x.w, a.w)); }
[[nodiscard]] __device__ inline lc_float lc_pow(lc_float x, lc_float a) noexcept { return powf_impl(x, a); }
[[nodiscard]] __device__ inline lc_float2 lc_pow(lc_float2 x, lc_float2 a) noexcept { return lc_make_float2(powf_impl(x.x, a.x), powf_impl(x.y, a.y)); }
[[nodiscard]] __device__ inline lc_float3 lc_pow(lc_float3 x, lc_float3 a) noexcept { return lc_make_float3(powf_impl(x.x, a.x), powf_impl(x.y, a.y), powf_impl(x.z, a.z)); }
[[nodiscard]] __device__ inline lc_float4 lc_pow(lc_float4 x, lc_float4 a) noexcept { return lc_make_float4(powf_impl(x.x, a.x), powf_impl(x.y, a.y), powf_impl(x.z, a.z), powf_impl(x.w, a.w)); }

[[nodiscard]] __device__ inline lc_half lc_powi(lc_half x, lc_half a) noexcept { return powi_impl(x, a); }
[[nodiscard]] __device__ inline lc_half2 lc_powi(lc_half2 x, lc_half2 a) noexcept { return lc_make_half2(powi_impl(x.x, a.x), powi_impl(x.y, a.y)); }
[[nodiscard]] __device__ inline lc_half3 lc_powi(lc_half3 x, lc_half3 a) noexcept { return lc_make_half3(powi_impl(x.x, a.x), powi_impl(x.y, a.y), powi_impl(x.z, a.z)); }
[[nodiscard]] __device__ inline lc_half4 lc_powi(lc_half4 x, lc_half4 a) noexcept { return lc_make_half4(powi_impl(x.x, a.x), powi_impl(x.y, a.y), powi_impl(x.z, a.z), powi_impl(x.w, a.w)); }
[[nodiscard]] __device__ inline lc_float lc_powi(lc_float x, lc_float a) noexcept { return powi_impl(x, a); }
[[nodiscard]] __device__ inline lc_float2 lc_powi(lc_float2 x, lc_float2 a) noexcept { return lc_make_float2(powi_impl(x.x, a.x), powi_impl(x.y, a.y)); }
[[nodiscard]] __device__ inline lc_float3 lc_powi(lc_float3 x, lc_float3 a) noexcept { return lc_make_float3(powi_impl(x.x, a.x), powi_impl(x.y, a.y), powi_impl(x.z, a.z)); }
[[nodiscard]] __device__ inline lc_float4 lc_powi(lc_float4 x, lc_float4 a) noexcept { return lc_make_float4(powi_impl(x.x, a.x), powi_impl(x.y, a.y), powi_impl(x.z, a.z), powi_impl(x.w, a.w)); }

[[nodiscard]] __device__ inline lc_float lc_sqrt(lc_float x) noexcept { return sqrtf(x); }
[[nodiscard]] __device__ inline lc_float2 lc_sqrt(lc_float2 x) noexcept { return lc_make_float2(sqrtf(x.x), sqrtf(x.y)); }
[[nodiscard]] __device__ inline lc_float3 lc_sqrt(lc_float3 x) noexcept { return lc_make_float3(sqrtf(x.x), sqrtf(x.y), sqrtf(x.z)); }
[[nodiscard]] __device__ inline lc_float4 lc_sqrt(lc_float4 x) noexcept { return lc_make_float4(sqrtf(x.x), sqrtf(x.y), sqrtf(x.z), sqrtf(x.w)); }

[[nodiscard]] __device__ inline lc_half lc_sqrt(lc_half x) noexcept { return hsqrt(x); }
[[nodiscard]] __device__ inline lc_half2 lc_sqrt(lc_half2 x) noexcept { return lc_make_half2(hsqrt(x.x), hsqrt(x.y)); }
[[nodiscard]] __device__ inline lc_half3 lc_sqrt(lc_half3 x) noexcept { return lc_make_half3(hsqrt(x.x), hsqrt(x.y), hsqrt(x.z)); }
[[nodiscard]] __device__ inline lc_half4 lc_sqrt(lc_half4 x) noexcept { return lc_make_half4(hsqrt(x.x), hsqrt(x.y), hsqrt(x.z), hsqrt(x.w)); }

[[nodiscard]] __device__ inline lc_float lc_rsqrt(lc_float x) noexcept { return rsqrtf(x); }
[[nodiscard]] __device__ inline lc_float2 lc_rsqrt(lc_float2 x) noexcept { return lc_make_float2(rsqrtf(x.x), rsqrtf(x.y)); }
[[nodiscard]] __device__ inline lc_float3 lc_rsqrt(lc_float3 x) noexcept { return lc_make_float3(rsqrtf(x.x), rsqrtf(x.y), rsqrtf(x.z)); }
[[nodiscard]] __device__ inline lc_float4 lc_rsqrt(lc_float4 x) noexcept { return lc_make_float4(rsqrtf(x.x), rsqrtf(x.y), rsqrtf(x.z), rsqrtf(x.w)); }

[[nodiscard]] __device__ inline lc_half lc_rsqrt(lc_half x) noexcept { return hrsqrt(x); }
[[nodiscard]] __device__ inline lc_half2 lc_rsqrt(lc_half2 x) noexcept { return lc_make_half2(hrsqrt(x.x), hrsqrt(x.y)); }
[[nodiscard]] __device__ inline lc_half3 lc_rsqrt(lc_half3 x) noexcept { return lc_make_half3(hrsqrt(x.x), hrsqrt(x.y), hrsqrt(x.z)); }
[[nodiscard]] __device__ inline lc_half4 lc_rsqrt(lc_half4 x) noexcept { return lc_make_half4(hrsqrt(x.x), hrsqrt(x.y), hrsqrt(x.z), hrsqrt(x.w)); }

[[nodiscard]] __device__ inline lc_float lc_ceil(lc_float x) noexcept { return ceilf(x); }
[[nodiscard]] __device__ inline lc_float2 lc_ceil(lc_float2 x) noexcept { return lc_make_float2(ceilf(x.x), ceilf(x.y)); }
[[nodiscard]] __device__ inline lc_float3 lc_ceil(lc_float3 x) noexcept { return lc_make_float3(ceilf(x.x), ceilf(x.y), ceilf(x.z)); }
[[nodiscard]] __device__ inline lc_float4 lc_ceil(lc_float4 x) noexcept { return lc_make_float4(ceilf(x.x), ceilf(x.y), ceilf(x.z), ceilf(x.w)); }

[[nodiscard]] __device__ inline lc_half lc_ceil(lc_half x) noexcept { return hceil(x); }
[[nodiscard]] __device__ inline lc_half2 lc_ceil(lc_half2 x) noexcept { return lc_make_half2(hceil(x.x), hceil(x.y)); }
[[nodiscard]] __device__ inline lc_half3 lc_ceil(lc_half3 x) noexcept { return lc_make_half3(hceil(x.x), hceil(x.y), hceil(x.z)); }
[[nodiscard]] __device__ inline lc_half4 lc_ceil(lc_half4 x) noexcept { return lc_make_half4(hceil(x.x), hceil(x.y), hceil(x.z), hceil(x.w)); }

[[nodiscard]] __device__ inline lc_float lc_floor(lc_float x) noexcept { return floorf(x); }
[[nodiscard]] __device__ inline lc_float2 lc_floor(lc_float2 x) noexcept { return lc_make_float2(floorf(x.x), floorf(x.y)); }
[[nodiscard]] __device__ inline lc_float3 lc_floor(lc_float3 x) noexcept { return lc_make_float3(floorf(x.x), floorf(x.y), floorf(x.z)); }
[[nodiscard]] __device__ inline lc_float4 lc_floor(lc_float4 x) noexcept { return lc_make_float4(floorf(x.x), floorf(x.y), floorf(x.z), floorf(x.w)); }

[[nodiscard]] __device__ inline lc_half lc_floor(lc_half x) noexcept { return hfloor(x); }
[[nodiscard]] __device__ inline lc_half2 lc_floor(lc_half2 x) noexcept { return lc_make_half2(hfloor(x.x), hfloor(x.y)); }
[[nodiscard]] __device__ inline lc_half3 lc_floor(lc_half3 x) noexcept { return lc_make_half3(hfloor(x.x), hfloor(x.y), hfloor(x.z)); }
[[nodiscard]] __device__ inline lc_half4 lc_floor(lc_half4 x) noexcept { return lc_make_half4(hfloor(x.x), hfloor(x.y), hfloor(x.z), hfloor(x.w)); }

[[nodiscard]] __device__ inline lc_float lc_trunc(lc_float x) noexcept { return truncf(x); }
[[nodiscard]] __device__ inline lc_float2 lc_trunc(lc_float2 x) noexcept { return lc_make_float2(truncf(x.x), truncf(x.y)); }
[[nodiscard]] __device__ inline lc_float3 lc_trunc(lc_float3 x) noexcept { return lc_make_float3(truncf(x.x), truncf(x.y), truncf(x.z)); }
[[nodiscard]] __device__ inline lc_float4 lc_trunc(lc_float4 x) noexcept { return lc_make_float4(truncf(x.x), truncf(x.y), truncf(x.z), truncf(x.w)); }

[[nodiscard]] __device__ inline lc_half lc_trunc(lc_half x) noexcept { return htrunc(x); }
[[nodiscard]] __device__ inline lc_half2 lc_trunc(lc_half2 x) noexcept { return lc_make_half2(htrunc(x.x), htrunc(x.y)); }
[[nodiscard]] __device__ inline lc_half3 lc_trunc(lc_half3 x) noexcept { return lc_make_half3(htrunc(x.x), htrunc(x.y), htrunc(x.z)); }
[[nodiscard]] __device__ inline lc_half4 lc_trunc(lc_half4 x) noexcept { return lc_make_half4(htrunc(x.x), htrunc(x.y), htrunc(x.z), htrunc(x.w)); }

[[nodiscard]] __device__ inline lc_half lc_round(lc_half x) noexcept { return roundf(x); }
[[nodiscard]] __device__ inline lc_half2 lc_round(lc_half2 x) noexcept { return lc_make_half2(roundf(x.x), roundf(x.y)); }
[[nodiscard]] __device__ inline lc_half3 lc_round(lc_half3 x) noexcept { return lc_make_half3(roundf(x.x), roundf(x.y), roundf(x.z)); }
[[nodiscard]] __device__ inline lc_half4 lc_round(lc_half4 x) noexcept { return lc_make_half4(roundf(x.x), roundf(x.y), roundf(x.z), roundf(x.w)); }
[[nodiscard]] __device__ inline lc_float lc_round(lc_float x) noexcept { return roundf(x); }
[[nodiscard]] __device__ inline lc_float2 lc_round(lc_float2 x) noexcept { return lc_make_float2(roundf(x.x), roundf(x.y)); }
[[nodiscard]] __device__ inline lc_float3 lc_round(lc_float3 x) noexcept { return lc_make_float3(roundf(x.x), roundf(x.y), roundf(x.z)); }
[[nodiscard]] __device__ inline lc_float4 lc_round(lc_float4 x) noexcept { return lc_make_float4(roundf(x.x), roundf(x.y), roundf(x.z), roundf(x.w)); }

[[nodiscard]] __device__ inline lc_float lc_fma(lc_float x, lc_float y, lc_float z) noexcept { return fmaf(x, y, z); }
[[nodiscard]] __device__ inline lc_float2 lc_fma(lc_float2 x, lc_float2 y, lc_float2 z) noexcept { return lc_make_float2(fmaf(x.x, y.x, z.x), fmaf(x.y, y.y, z.y)); }
[[nodiscard]] __device__ inline lc_float3 lc_fma(lc_float3 x, lc_float3 y, lc_float3 z) noexcept { return lc_make_float3(fmaf(x.x, y.x, z.x), fmaf(x.y, y.y, z.y), fmaf(x.z, y.z, z.z)); }
[[nodiscard]] __device__ inline lc_float4 lc_fma(lc_float4 x, lc_float4 y, lc_float4 z) noexcept { return lc_make_float4(fmaf(x.x, y.x, z.x), fmaf(x.y, y.y, z.y), fmaf(x.z, y.z, z.z), fmaf(x.w, y.w, z.w)); }

[[nodiscard]] __device__ inline lc_half lc_fma(lc_half x, lc_half y, lc_half z) noexcept { return __hfma(x, y, z); }
[[nodiscard]] __device__ inline lc_half2 lc_fma(lc_half2 x, lc_half2 y, lc_half2 z) noexcept { return lc_make_half2(__hfma(x.x, y.x, z.x), __hfma(x.y, y.y, z.y)); }
[[nodiscard]] __device__ inline lc_half3 lc_fma(lc_half3 x, lc_half3 y, lc_half3 z) noexcept { return lc_make_half3(__hfma(x.x, y.x, z.x), __hfma(x.y, y.y, z.y), __hfma(x.z, y.z, z.z)); }
[[nodiscard]] __device__ inline lc_half4 lc_fma(lc_half4 x, lc_half4 y, lc_half4 z) noexcept { return lc_make_half4(__hfma(x.x, y.x, z.x), __hfma(x.y, y.y, z.y), __hfma(x.z, y.z, z.z), __hfma(x.w, y.w, z.w)); }


[[nodiscard]] __device__ inline auto lc_copysign_impl(lc_half x, lc_half y) noexcept {
auto ux = __half_as_short(x);
auto uy = __half_as_short(y);
return __short_as_half((ux & 0x7fffu) | (uy & 0x8000u));
}
[[nodiscard]] __device__ inline lc_float lc_copysign(lc_float x, lc_float y) noexcept { return copysignf(x, y); }
[[nodiscard]] __device__ inline lc_float2 lc_copysign(lc_float2 x, lc_float2 y) noexcept { return lc_make_float2(copysignf(x.x, y.x), copysignf(x.y, y.y)); }
[[nodiscard]] __device__ inline lc_float3 lc_copysign(lc_float3 x, lc_float3 y) noexcept { return lc_make_float3(copysignf(x.x, y.x), copysignf(x.y, y.y), copysignf(x.z, y.z)); }
[[nodiscard]] __device__ inline lc_float4 lc_copysign(lc_float4 x, lc_float4 y) noexcept { return lc_make_float4(copysignf(x.x, y.x), copysignf(x.y, y.y), copysignf(x.z, y.z), copysignf(x.w, y.w)); }

[[nodiscard]] __device__ inline lc_half lc_copysign(lc_half x, lc_half y) noexcept { return lc_copysign_impl(x, y); }
[[nodiscard]] __device__ inline lc_half2 lc_copysign(lc_half2 x, lc_half2 y) noexcept { return lc_make_half2(lc_copysign_impl(x.x, y.x), lc_copysign_impl(x.y, y.y)); }
[[nodiscard]] __device__ inline lc_half3 lc_copysign(lc_half3 x, lc_half3 y) noexcept { return lc_make_half3(lc_copysign_impl(x.x, y.x), lc_copysign_impl(x.y, y.y), lc_copysign_impl(x.z, y.z)); }
[[nodiscard]] __device__ inline lc_half4 lc_copysign(lc_half4 x, lc_half4 y) noexcept { return lc_make_half4(lc_copysign_impl(x.x, y.x), lc_copysign_impl(x.y, y.y), lc_copysign_impl(x.z, y.z), lc_copysign_impl(x.w, y.w)); }

[[nodiscard]] __device__ inline lc_bool lc_isinf(lc_float x) noexcept { return isinf_impl(x); }
[[nodiscard]] __device__ inline lc_bool2 lc_isinf(lc_float2 x) noexcept { return lc_make_bool2(isinf_impl(x.x), isinf_impl(x.y)); }
[[nodiscard]] __device__ inline lc_bool3 lc_isinf(lc_float3 x) noexcept { return lc_make_bool3(isinf_impl(x.x), isinf_impl(x.y), isinf_impl(x.z)); }
[[nodiscard]] __device__ inline lc_bool4 lc_isinf(lc_float4 x) noexcept { return lc_make_bool4(isinf_impl(x.x), isinf_impl(x.y), isinf_impl(x.z), isinf_impl(x.w)); }

[[nodiscard]] __device__ inline lc_bool lc_isnan(lc_float x) noexcept { return isnan_impl(x); }
[[nodiscard]] __device__ inline lc_bool2 lc_isnan(lc_float2 x) noexcept { return lc_make_bool2(isnan_impl(x.x), isnan_impl(x.y)); }
[[nodiscard]] __device__ inline lc_bool3 lc_isnan(lc_float3 x) noexcept { return lc_make_bool3(isnan_impl(x.x), isnan_impl(x.y), isnan_impl(x.z)); }
[[nodiscard]] __device__ inline lc_bool4 lc_isnan(lc_float4 x) noexcept { return lc_make_bool4(isnan_impl(x.x), isnan_impl(x.y), isnan_impl(x.z), isnan_impl(x.w)); }

[[nodiscard]] __device__ inline lc_bool lc_isinf(lc_half x) noexcept { return __hisinf(x); }
[[nodiscard]] __device__ inline lc_bool2 lc_isinf(lc_half2 x) noexcept { return lc_make_bool2(__hisinf(x.x), __hisinf(x.y)); }
[[nodiscard]] __device__ inline lc_bool3 lc_isinf(lc_half3 x) noexcept { return lc_make_bool3(__hisinf(x.x), __hisinf(x.y), __hisinf(x.z)); }
[[nodiscard]] __device__ inline lc_bool4 lc_isinf(lc_half4 x) noexcept { return lc_make_bool4(__hisinf(x.x), __hisinf(x.y), __hisinf(x.z), __hisinf(x.w)); }

[[nodiscard]] __device__ inline lc_bool lc_isnan(lc_half x) noexcept { return __hisnan(x); }
[[nodiscard]] __device__ inline lc_bool2 lc_isnan(lc_half2 x) noexcept { return lc_make_bool2(__hisnan(x.x), __hisnan(x.y)); }
[[nodiscard]] __device__ inline lc_bool3 lc_isnan(lc_half3 x) noexcept { return lc_make_bool3(__hisnan(x.x), __hisnan(x.y), __hisnan(x.z)); }
[[nodiscard]] __device__ inline lc_bool4 lc_isnan(lc_half4 x) noexcept { return lc_make_bool4(__hisnan(x.x), __hisnan(x.y), __hisnan(x.z), __hisnan(x.w)); }

[[nodiscard]] __device__ inline auto lc_reduce_sum(lc_short2 v) noexcept { return lc_short(v.x+v.y); }
[[nodiscard]] __device__ inline auto lc_reduce_prod(lc_short2 v) noexcept { return lc_short(v.x*v.y); }
[[nodiscard]] __device__ inline auto lc_reduce_min(lc_short2 v) noexcept { return lc_short(lc_min(v.x, v.y)); }
[[nodiscard]] __device__ inline auto lc_reduce_max(lc_short2 v) noexcept { return lc_short(lc_max(v.x, v.y)); }
[[nodiscard]] __device__ inline auto lc_reduce_sum(lc_short3 v) noexcept { return lc_short(v.x+v.y+v.z); }
[[nodiscard]] __device__ inline auto lc_reduce_prod(lc_short3 v) noexcept { return lc_short(v.x*v.y*v.z); }
[[nodiscard]] __device__ inline auto lc_reduce_min(lc_short3 v) noexcept { return lc_short(lc_min(v.x, lc_min(v.y, v.z))); }
[[nodiscard]] __device__ inline auto lc_reduce_max(lc_short3 v) noexcept { return lc_short(lc_max(v.x, lc_max(v.y, v.z))); }
[[nodiscard]] __device__ inline auto lc_reduce_sum(lc_short4 v) noexcept { return lc_short(v.x+v.y+v.z+v.w); }
[[nodiscard]] __device__ inline auto lc_reduce_prod(lc_short4 v) noexcept { return lc_short(v.x*v.y*v.z*v.w); }
[[nodiscard]] __device__ inline auto lc_reduce_min(lc_short4 v) noexcept { return lc_short(lc_min(v.x, lc_min(v.y, lc_min(v.z, v.w)))); }
[[nodiscard]] __device__ inline auto lc_reduce_max(lc_short4 v) noexcept { return lc_short(lc_max(v.x, lc_max(v.y, lc_max(v.z, v.w)))); }
[[nodiscard]] __device__ inline auto lc_reduce_sum(lc_ushort2 v) noexcept { return lc_ushort(v.x+v.y); }
[[nodiscard]] __device__ inline auto lc_reduce_prod(lc_ushort2 v) noexcept { return lc_ushort(v.x*v.y); }
[[nodiscard]] __device__ inline auto lc_reduce_min(lc_ushort2 v) noexcept { return lc_ushort(lc_min(v.x, v.y)); }
[[nodiscard]] __device__ inline auto lc_reduce_max(lc_ushort2 v) noexcept { return lc_ushort(lc_max(v.x, v.y)); }
[[nodiscard]] __device__ inline auto lc_reduce_sum(lc_ushort3 v) noexcept { return lc_ushort(v.x+v.y+v.z); }
[[nodiscard]] __device__ inline auto lc_reduce_prod(lc_ushort3 v) noexcept { return lc_ushort(v.x*v.y*v.z); }
[[nodiscard]] __device__ inline auto lc_reduce_min(lc_ushort3 v) noexcept { return lc_ushort(lc_min(v.x, lc_min(v.y, v.z))); }
[[nodiscard]] __device__ inline auto lc_reduce_max(lc_ushort3 v) noexcept { return lc_ushort(lc_max(v.x, lc_max(v.y, v.z))); }
[[nodiscard]] __device__ inline auto lc_reduce_sum(lc_ushort4 v) noexcept { return lc_ushort(v.x+v.y+v.z+v.w); }
[[nodiscard]] __device__ inline auto lc_reduce_prod(lc_ushort4 v) noexcept { return lc_ushort(v.x*v.y*v.z*v.w); }
[[nodiscard]] __device__ inline auto lc_reduce_min(lc_ushort4 v) noexcept { return lc_ushort(lc_min(v.x, lc_min(v.y, lc_min(v.z, v.w)))); }
[[nodiscard]] __device__ inline auto lc_reduce_max(lc_ushort4 v) noexcept { return lc_ushort(lc_max(v.x, lc_max(v.y, lc_max(v.z, v.w)))); }
[[nodiscard]] __device__ inline auto lc_reduce_sum(lc_int2 v) noexcept { return lc_int(v.x+v.y); }
[[nodiscard]] __device__ inline auto lc_reduce_prod(lc_int2 v) noexcept { return lc_int(v.x*v.y); }
[[nodiscard]] __device__ inline auto lc_reduce_min(lc_int2 v) noexcept { return lc_int(lc_min(v.x, v.y)); }
[[nodiscard]] __device__ inline auto lc_reduce_max(lc_int2 v) noexcept { return lc_int(lc_max(v.x, v.y)); }
[[nodiscard]] __device__ inline auto lc_reduce_sum(lc_int3 v) noexcept { return lc_int(v.x+v.y+v.z); }
[[nodiscard]] __device__ inline auto lc_reduce_prod(lc_int3 v) noexcept { return lc_int(v.x*v.y*v.z); }
[[nodiscard]] __device__ inline auto lc_reduce_min(lc_int3 v) noexcept { return lc_int(lc_min(v.x, lc_min(v.y, v.z))); }
[[nodiscard]] __device__ inline auto lc_reduce_max(lc_int3 v) noexcept { return lc_int(lc_max(v.x, lc_max(v.y, v.z))); }
[[nodiscard]] __device__ inline auto lc_reduce_sum(lc_int4 v) noexcept { return lc_int(v.x+v.y+v.z+v.w); }
[[nodiscard]] __device__ inline auto lc_reduce_prod(lc_int4 v) noexcept { return lc_int(v.x*v.y*v.z*v.w); }
[[nodiscard]] __device__ inline auto lc_reduce_min(lc_int4 v) noexcept { return lc_int(lc_min(v.x, lc_min(v.y, lc_min(v.z, v.w)))); }
[[nodiscard]] __device__ inline auto lc_reduce_max(lc_int4 v) noexcept { return lc_int(lc_max(v.x, lc_max(v.y, lc_max(v.z, v.w)))); }
[[nodiscard]] __device__ inline auto lc_reduce_sum(lc_uint2 v) noexcept { return lc_uint(v.x+v.y); }
[[nodiscard]] __device__ inline auto lc_reduce_prod(lc_uint2 v) noexcept { return lc_uint(v.x*v.y); }
[[nodiscard]] __device__ inline auto lc_reduce_min(lc_uint2 v) noexcept { return lc_uint(lc_min(v.x, v.y)); }
[[nodiscard]] __device__ inline auto lc_reduce_max(lc_uint2 v) noexcept { return lc_uint(lc_max(v.x, v.y)); }
[[nodiscard]] __device__ inline auto lc_reduce_sum(lc_uint3 v) noexcept { return lc_uint(v.x+v.y+v.z); }
[[nodiscard]] __device__ inline auto lc_reduce_prod(lc_uint3 v) noexcept { return lc_uint(v.x*v.y*v.z); }
[[nodiscard]] __device__ inline auto lc_reduce_min(lc_uint3 v) noexcept { return lc_uint(lc_min(v.x, lc_min(v.y, v.z))); }
[[nodiscard]] __device__ inline auto lc_reduce_max(lc_uint3 v) noexcept { return lc_uint(lc_max(v.x, lc_max(v.y, v.z))); }
[[nodiscard]] __device__ inline auto lc_reduce_sum(lc_uint4 v) noexcept { return lc_uint(v.x+v.y+v.z+v.w); }
[[nodiscard]] __device__ inline auto lc_reduce_prod(lc_uint4 v) noexcept { return lc_uint(v.x*v.y*v.z*v.w); }
[[nodiscard]] __device__ inline auto lc_reduce_min(lc_uint4 v) noexcept { return lc_uint(lc_min(v.x, lc_min(v.y, lc_min(v.z, v.w)))); }
[[nodiscard]] __device__ inline auto lc_reduce_max(lc_uint4 v) noexcept { return lc_uint(lc_max(v.x, lc_max(v.y, lc_max(v.z, v.w)))); }
[[nodiscard]] __device__ inline auto lc_reduce_sum(lc_half2 v) noexcept { return lc_half(v.x+v.y); }
[[nodiscard]] __device__ inline auto lc_reduce_prod(lc_half2 v) noexcept { return lc_half(v.x*v.y); }
[[nodiscard]] __device__ inline auto lc_reduce_min(lc_half2 v) noexcept { return lc_half(lc_min(v.x, v.y)); }
[[nodiscard]] __device__ inline auto lc_reduce_max(lc_half2 v) noexcept { return lc_half(lc_max(v.x, v.y)); }
[[nodiscard]] __device__ inline auto lc_reduce_sum(lc_half3 v) noexcept { return lc_half(v.x+v.y+v.z); }
[[nodiscard]] __device__ inline auto lc_reduce_prod(lc_half3 v) noexcept { return lc_half(v.x*v.y*v.z); }
[[nodiscard]] __device__ inline auto lc_reduce_min(lc_half3 v) noexcept { return lc_half(lc_min(v.x, lc_min(v.y, v.z))); }
[[nodiscard]] __device__ inline auto lc_reduce_max(lc_half3 v) noexcept { return lc_half(lc_max(v.x, lc_max(v.y, v.z))); }
[[nodiscard]] __device__ inline auto lc_reduce_sum(lc_half4 v) noexcept { return lc_half(v.x+v.y+v.z+v.w); }
[[nodiscard]] __device__ inline auto lc_reduce_prod(lc_half4 v) noexcept { return lc_half(v.x*v.y*v.z*v.w); }
[[nodiscard]] __device__ inline auto lc_reduce_min(lc_half4 v) noexcept { return lc_half(lc_min(v.x, lc_min(v.y, lc_min(v.z, v.w)))); }
[[nodiscard]] __device__ inline auto lc_reduce_max(lc_half4 v) noexcept { return lc_half(lc_max(v.x, lc_max(v.y, lc_max(v.z, v.w)))); }
[[nodiscard]] __device__ inline auto lc_reduce_sum(lc_float2 v) noexcept { return lc_float(v.x+v.y); }
[[nodiscard]] __device__ inline auto lc_reduce_prod(lc_float2 v) noexcept { return lc_float(v.x*v.y); }
[[nodiscard]] __device__ inline auto lc_reduce_min(lc_float2 v) noexcept { return lc_float(lc_min(v.x, v.y)); }
[[nodiscard]] __device__ inline auto lc_reduce_max(lc_float2 v) noexcept { return lc_float(lc_max(v.x, v.y)); }
[[nodiscard]] __device__ inline auto lc_reduce_sum(lc_float3 v) noexcept { return lc_float(v.x+v.y+v.z); }
[[nodiscard]] __device__ inline auto lc_reduce_prod(lc_float3 v) noexcept { return lc_float(v.x*v.y*v.z); }
[[nodiscard]] __device__ inline auto lc_reduce_min(lc_float3 v) noexcept { return lc_float(lc_min(v.x, lc_min(v.y, v.z))); }
[[nodiscard]] __device__ inline auto lc_reduce_max(lc_float3 v) noexcept { return lc_float(lc_max(v.x, lc_max(v.y, v.z))); }
[[nodiscard]] __device__ inline auto lc_reduce_sum(lc_float4 v) noexcept { return lc_float(v.x+v.y+v.z+v.w); }
[[nodiscard]] __device__ inline auto lc_reduce_prod(lc_float4 v) noexcept { return lc_float(v.x*v.y*v.z*v.w); }
[[nodiscard]] __device__ inline auto lc_reduce_min(lc_float4 v) noexcept { return lc_float(lc_min(v.x, lc_min(v.y, lc_min(v.z, v.w)))); }
[[nodiscard]] __device__ inline auto lc_reduce_max(lc_float4 v) noexcept { return lc_float(lc_max(v.x, lc_max(v.y, lc_max(v.z, v.w)))); }
[[nodiscard]] __device__ inline auto lc_reduce_sum(lc_long2 v) noexcept { return lc_long(v.x+v.y); }
[[nodiscard]] __device__ inline auto lc_reduce_prod(lc_long2 v) noexcept { return lc_long(v.x*v.y); }
[[nodiscard]] __device__ inline auto lc_reduce_min(lc_long2 v) noexcept { return lc_long(lc_min(v.x, v.y)); }
[[nodiscard]] __device__ inline auto lc_reduce_max(lc_long2 v) noexcept { return lc_long(lc_max(v.x, v.y)); }
[[nodiscard]] __device__ inline auto lc_reduce_sum(lc_long3 v) noexcept { return lc_long(v.x+v.y+v.z); }
[[nodiscard]] __device__ inline auto lc_reduce_prod(lc_long3 v) noexcept { return lc_long(v.x*v.y*v.z); }
[[nodiscard]] __device__ inline auto lc_reduce_min(lc_long3 v) noexcept { return lc_long(lc_min(v.x, lc_min(v.y, v.z))); }
[[nodiscard]] __device__ inline auto lc_reduce_max(lc_long3 v) noexcept { return lc_long(lc_max(v.x, lc_max(v.y, v.z))); }
[[nodiscard]] __device__ inline auto lc_reduce_sum(lc_long4 v) noexcept { return lc_long(v.x+v.y+v.z+v.w); }
[[nodiscard]] __device__ inline auto lc_reduce_prod(lc_long4 v) noexcept { return lc_long(v.x*v.y*v.z*v.w); }
[[nodiscard]] __device__ inline auto lc_reduce_min(lc_long4 v) noexcept { return lc_long(lc_min(v.x, lc_min(v.y, lc_min(v.z, v.w)))); }
[[nodiscard]] __device__ inline auto lc_reduce_max(lc_long4 v) noexcept { return lc_long(lc_max(v.x, lc_max(v.y, lc_max(v.z, v.w)))); }
[[nodiscard]] __device__ inline auto lc_reduce_sum(lc_ulong2 v) noexcept { return lc_ulong(v.x+v.y); }
[[nodiscard]] __device__ inline auto lc_reduce_prod(lc_ulong2 v) noexcept { return lc_ulong(v.x*v.y); }
[[nodiscard]] __device__ inline auto lc_reduce_min(lc_ulong2 v) noexcept { return lc_ulong(lc_min(v.x, v.y)); }
[[nodiscard]] __device__ inline auto lc_reduce_max(lc_ulong2 v) noexcept { return lc_ulong(lc_max(v.x, v.y)); }
[[nodiscard]] __device__ inline auto lc_reduce_sum(lc_ulong3 v) noexcept { return lc_ulong(v.x+v.y+v.z); }
[[nodiscard]] __device__ inline auto lc_reduce_prod(lc_ulong3 v) noexcept { return lc_ulong(v.x*v.y*v.z); }
[[nodiscard]] __device__ inline auto lc_reduce_min(lc_ulong3 v) noexcept { return lc_ulong(lc_min(v.x, lc_min(v.y, v.z))); }
[[nodiscard]] __device__ inline auto lc_reduce_max(lc_ulong3 v) noexcept { return lc_ulong(lc_max(v.x, lc_max(v.y, v.z))); }
[[nodiscard]] __device__ inline auto lc_reduce_sum(lc_ulong4 v) noexcept { return lc_ulong(v.x+v.y+v.z+v.w); }
[[nodiscard]] __device__ inline auto lc_reduce_prod(lc_ulong4 v) noexcept { return lc_ulong(v.x*v.y*v.z*v.w); }
[[nodiscard]] __device__ inline auto lc_reduce_min(lc_ulong4 v) noexcept { return lc_ulong(lc_min(v.x, lc_min(v.y, lc_min(v.z, v.w)))); }
[[nodiscard]] __device__ inline auto lc_reduce_max(lc_ulong4 v) noexcept { return lc_ulong(lc_max(v.x, lc_max(v.y, lc_max(v.z, v.w)))); }
[[nodiscard]] __device__ inline auto lc_min_impl(lc_short a, lc_short b) noexcept { return a < b ? a : b; }
[[nodiscard]] __device__ inline auto lc_max_impl(lc_short a, lc_short b) noexcept { return a > b ? a : b; }
[[nodiscard]] __device__ inline auto lc_min_impl(lc_ushort a, lc_ushort b) noexcept { return a < b ? a : b; }
[[nodiscard]] __device__ inline auto lc_max_impl(lc_ushort a, lc_ushort b) noexcept { return a > b ? a : b; }
[[nodiscard]] __device__ inline auto lc_min_impl(lc_int a, lc_int b) noexcept { return a < b ? a : b; }
[[nodiscard]] __device__ inline auto lc_max_impl(lc_int a, lc_int b) noexcept { return a > b ? a : b; }
[[nodiscard]] __device__ inline auto lc_min_impl(lc_uint a, lc_uint b) noexcept { return a < b ? a : b; }
[[nodiscard]] __device__ inline auto lc_max_impl(lc_uint a, lc_uint b) noexcept { return a > b ? a : b; }
[[nodiscard]] __device__ inline auto lc_min_impl(lc_long a, lc_long b) noexcept { return a < b ? a : b; }
[[nodiscard]] __device__ inline auto lc_max_impl(lc_long a, lc_long b) noexcept { return a > b ? a : b; }
[[nodiscard]] __device__ inline auto lc_min_impl(lc_ulong a, lc_ulong b) noexcept { return a < b ? a : b; }
[[nodiscard]] __device__ inline auto lc_max_impl(lc_ulong a, lc_ulong b) noexcept { return a > b ? a : b; }
[[nodiscard]] __device__ inline lc_short lc_min(lc_short a, lc_short b) noexcept { return lc_min_impl(a, b); }
[[nodiscard]] __device__ inline lc_short2 lc_min(lc_short2 a, lc_short2 b) noexcept { return lc_make_short2(lc_min_impl(a.x, b.x), lc_min_impl(a.y, b.y)); }
[[nodiscard]] __device__ inline lc_short3 lc_min(lc_short3 a, lc_short3 b) noexcept { return lc_make_short3(lc_min_impl(a.x, b.x), lc_min_impl(a.y, b.y), lc_min_impl(a.z, b.z)); }
[[nodiscard]] __device__ inline lc_short4 lc_min(lc_short4 a, lc_short4 b) noexcept { return lc_make_short4(lc_min_impl(a.x, b.x), lc_min_impl(a.y, b.y), lc_min_impl(a.z, b.z), lc_min_impl(a.w, b.w)); }
[[nodiscard]] __device__ inline lc_ushort lc_min(lc_ushort a, lc_ushort b) noexcept { return lc_min_impl(a, b); }
[[nodiscard]] __device__ inline lc_ushort2 lc_min(lc_ushort2 a, lc_ushort2 b) noexcept { return lc_make_ushort2(lc_min_impl(a.x, b.x), lc_min_impl(a.y, b.y)); }
[[nodiscard]] __device__ inline lc_ushort3 lc_min(lc_ushort3 a, lc_ushort3 b) noexcept { return lc_make_ushort3(lc_min_impl(a.x, b.x), lc_min_impl(a.y, b.y), lc_min_impl(a.z, b.z)); }
[[nodiscard]] __device__ inline lc_ushort4 lc_min(lc_ushort4 a, lc_ushort4 b) noexcept { return lc_make_ushort4(lc_min_impl(a.x, b.x), lc_min_impl(a.y, b.y), lc_min_impl(a.z, b.z), lc_min_impl(a.w, b.w)); }
[[nodiscard]] __device__ inline lc_int lc_min(lc_int a, lc_int b) noexcept { return lc_min_impl(a, b); }
[[nodiscard]] __device__ inline lc_int2 lc_min(lc_int2 a, lc_int2 b) noexcept { return lc_make_int2(lc_min_impl(a.x, b.x), lc_min_impl(a.y, b.y)); }
[[nodiscard]] __device__ inline lc_int3 lc_min(lc_int3 a, lc_int3 b) noexcept { return lc_make_int3(lc_min_impl(a.x, b.x), lc_min_impl(a.y, b.y), lc_min_impl(a.z, b.z)); }
[[nodiscard]] __device__ inline lc_int4 lc_min(lc_int4 a, lc_int4 b) noexcept { return lc_make_int4(lc_min_impl(a.x, b.x), lc_min_impl(a.y, b.y), lc_min_impl(a.z, b.z), lc_min_impl(a.w, b.w)); }
[[nodiscard]] __device__ inline lc_uint lc_min(lc_uint a, lc_uint b) noexcept { return lc_min_impl(a, b); }
[[nodiscard]] __device__ inline lc_uint2 lc_min(lc_uint2 a, lc_uint2 b) noexcept { return lc_make_uint2(lc_min_impl(a.x, b.x), lc_min_impl(a.y, b.y)); }
[[nodiscard]] __device__ inline lc_uint3 lc_min(lc_uint3 a, lc_uint3 b) noexcept { return lc_make_uint3(lc_min_impl(a.x, b.x), lc_min_impl(a.y, b.y), lc_min_impl(a.z, b.z)); }
[[nodiscard]] __device__ inline lc_uint4 lc_min(lc_uint4 a, lc_uint4 b) noexcept { return lc_make_uint4(lc_min_impl(a.x, b.x), lc_min_impl(a.y, b.y), lc_min_impl(a.z, b.z), lc_min_impl(a.w, b.w)); }
[[nodiscard]] __device__ inline lc_long lc_min(lc_long a, lc_long b) noexcept { return lc_min_impl(a, b); }
[[nodiscard]] __device__ inline lc_long2 lc_min(lc_long2 a, lc_long2 b) noexcept { return lc_make_long2(lc_min_impl(a.x, b.x), lc_min_impl(a.y, b.y)); }
[[nodiscard]] __device__ inline lc_long3 lc_min(lc_long3 a, lc_long3 b) noexcept { return lc_make_long3(lc_min_impl(a.x, b.x), lc_min_impl(a.y, b.y), lc_min_impl(a.z, b.z)); }
[[nodiscard]] __device__ inline lc_long4 lc_min(lc_long4 a, lc_long4 b) noexcept { return lc_make_long4(lc_min_impl(a.x, b.x), lc_min_impl(a.y, b.y), lc_min_impl(a.z, b.z), lc_min_impl(a.w, b.w)); }
[[nodiscard]] __device__ inline lc_ulong lc_min(lc_ulong a, lc_ulong b) noexcept { return lc_min_impl(a, b); }
[[nodiscard]] __device__ inline lc_ulong2 lc_min(lc_ulong2 a, lc_ulong2 b) noexcept { return lc_make_ulong2(lc_min_impl(a.x, b.x), lc_min_impl(a.y, b.y)); }
[[nodiscard]] __device__ inline lc_ulong3 lc_min(lc_ulong3 a, lc_ulong3 b) noexcept { return lc_make_ulong3(lc_min_impl(a.x, b.x), lc_min_impl(a.y, b.y), lc_min_impl(a.z, b.z)); }
[[nodiscard]] __device__ inline lc_ulong4 lc_min(lc_ulong4 a, lc_ulong4 b) noexcept { return lc_make_ulong4(lc_min_impl(a.x, b.x), lc_min_impl(a.y, b.y), lc_min_impl(a.z, b.z), lc_min_impl(a.w, b.w)); }

[[nodiscard]] __device__ inline lc_short lc_max(lc_short a, lc_short b) noexcept { return lc_max_impl(a, b); }
[[nodiscard]] __device__ inline lc_short2 lc_max(lc_short2 a, lc_short2 b) noexcept { return lc_make_short2(lc_max_impl(a.x, b.x), lc_max_impl(a.y, b.y)); }
[[nodiscard]] __device__ inline lc_short3 lc_max(lc_short3 a, lc_short3 b) noexcept { return lc_make_short3(lc_max_impl(a.x, b.x), lc_max_impl(a.y, b.y), lc_max_impl(a.z, b.z)); }
[[nodiscard]] __device__ inline lc_short4 lc_max(lc_short4 a, lc_short4 b) noexcept { return lc_make_short4(lc_max_impl(a.x, b.x), lc_max_impl(a.y, b.y), lc_max_impl(a.z, b.z), lc_max_impl(a.w, b.w)); }
[[nodiscard]] __device__ inline lc_ushort lc_max(lc_ushort a, lc_ushort b) noexcept { return lc_max_impl(a, b); }
[[nodiscard]] __device__ inline lc_ushort2 lc_max(lc_ushort2 a, lc_ushort2 b) noexcept { return lc_make_ushort2(lc_max_impl(a.x, b.x), lc_max_impl(a.y, b.y)); }
[[nodiscard]] __device__ inline lc_ushort3 lc_max(lc_ushort3 a, lc_ushort3 b) noexcept { return lc_make_ushort3(lc_max_impl(a.x, b.x), lc_max_impl(a.y, b.y), lc_max_impl(a.z, b.z)); }
[[nodiscard]] __device__ inline lc_ushort4 lc_max(lc_ushort4 a, lc_ushort4 b) noexcept { return lc_make_ushort4(lc_max_impl(a.x, b.x), lc_max_impl(a.y, b.y), lc_max_impl(a.z, b.z), lc_max_impl(a.w, b.w)); }
[[nodiscard]] __device__ inline lc_int lc_max(lc_int a, lc_int b) noexcept { return lc_max_impl(a, b); }
[[nodiscard]] __device__ inline lc_int2 lc_max(lc_int2 a, lc_int2 b) noexcept { return lc_make_int2(lc_max_impl(a.x, b.x), lc_max_impl(a.y, b.y)); }
[[nodiscard]] __device__ inline lc_int3 lc_max(lc_int3 a, lc_int3 b) noexcept { return lc_make_int3(lc_max_impl(a.x, b.x), lc_max_impl(a.y, b.y), lc_max_impl(a.z, b.z)); }
[[nodiscard]] __device__ inline lc_int4 lc_max(lc_int4 a, lc_int4 b) noexcept { return lc_make_int4(lc_max_impl(a.x, b.x), lc_max_impl(a.y, b.y), lc_max_impl(a.z, b.z), lc_max_impl(a.w, b.w)); }
[[nodiscard]] __device__ inline lc_uint lc_max(lc_uint a, lc_uint b) noexcept { return lc_max_impl(a, b); }
[[nodiscard]] __device__ inline lc_uint2 lc_max(lc_uint2 a, lc_uint2 b) noexcept { return lc_make_uint2(lc_max_impl(a.x, b.x), lc_max_impl(a.y, b.y)); }
[[nodiscard]] __device__ inline lc_uint3 lc_max(lc_uint3 a, lc_uint3 b) noexcept { return lc_make_uint3(lc_max_impl(a.x, b.x), lc_max_impl(a.y, b.y), lc_max_impl(a.z, b.z)); }
[[nodiscard]] __device__ inline lc_uint4 lc_max(lc_uint4 a, lc_uint4 b) noexcept { return lc_make_uint4(lc_max_impl(a.x, b.x), lc_max_impl(a.y, b.y), lc_max_impl(a.z, b.z), lc_max_impl(a.w, b.w)); }
[[nodiscard]] __device__ inline lc_long lc_max(lc_long a, lc_long b) noexcept { return lc_max_impl(a, b); }
[[nodiscard]] __device__ inline lc_long2 lc_max(lc_long2 a, lc_long2 b) noexcept { return lc_make_long2(lc_max_impl(a.x, b.x), lc_max_impl(a.y, b.y)); }
[[nodiscard]] __device__ inline lc_long3 lc_max(lc_long3 a, lc_long3 b) noexcept { return lc_make_long3(lc_max_impl(a.x, b.x), lc_max_impl(a.y, b.y), lc_max_impl(a.z, b.z)); }
[[nodiscard]] __device__ inline lc_long4 lc_max(lc_long4 a, lc_long4 b) noexcept { return lc_make_long4(lc_max_impl(a.x, b.x), lc_max_impl(a.y, b.y), lc_max_impl(a.z, b.z), lc_max_impl(a.w, b.w)); }
[[nodiscard]] __device__ inline lc_ulong lc_max(lc_ulong a, lc_ulong b) noexcept { return lc_max_impl(a, b); }
[[nodiscard]] __device__ inline lc_ulong2 lc_max(lc_ulong2 a, lc_ulong2 b) noexcept { return lc_make_ulong2(lc_max_impl(a.x, b.x), lc_max_impl(a.y, b.y)); }
[[nodiscard]] __device__ inline lc_ulong3 lc_max(lc_ulong3 a, lc_ulong3 b) noexcept { return lc_make_ulong3(lc_max_impl(a.x, b.x), lc_max_impl(a.y, b.y), lc_max_impl(a.z, b.z)); }
[[nodiscard]] __device__ inline lc_ulong4 lc_max(lc_ulong4 a, lc_ulong4 b) noexcept { return lc_make_ulong4(lc_max_impl(a.x, b.x), lc_max_impl(a.y, b.y), lc_max_impl(a.z, b.z), lc_max_impl(a.w, b.w)); }

[[nodiscard]] __device__ inline auto lc_clamp_impl(lc_short v, lc_short lo, lc_short hi) noexcept { return lc_min(lc_max(v, lo), hi); }
[[nodiscard]] __device__ inline auto lc_clamp_impl(lc_ushort v, lc_ushort lo, lc_ushort hi) noexcept { return lc_min(lc_max(v, lo), hi); }
[[nodiscard]] __device__ inline auto lc_clamp_impl(lc_int v, lc_int lo, lc_int hi) noexcept { return lc_min(lc_max(v, lo), hi); }
[[nodiscard]] __device__ inline auto lc_clamp_impl(lc_uint v, lc_uint lo, lc_uint hi) noexcept { return lc_min(lc_max(v, lo), hi); }
[[nodiscard]] __device__ inline auto lc_clamp_impl(lc_half v, lc_half lo, lc_half hi) noexcept { return lc_min(lc_max(v, lo), hi); }
[[nodiscard]] __device__ inline auto lc_clamp_impl(lc_float v, lc_float lo, lc_float hi) noexcept { return lc_min(lc_max(v, lo), hi); }
[[nodiscard]] __device__ inline auto lc_clamp_impl(lc_long v, lc_long lo, lc_long hi) noexcept { return lc_min(lc_max(v, lo), hi); }
[[nodiscard]] __device__ inline auto lc_clamp_impl(lc_ulong v, lc_ulong lo, lc_ulong hi) noexcept { return lc_min(lc_max(v, lo), hi); }
[[nodiscard]] __device__ inline lc_short lc_clamp(lc_short v, lc_short lo, lc_short hi) noexcept { return lc_clamp_impl(v, lo, hi); }
[[nodiscard]] __device__ inline lc_short2 lc_clamp(lc_short2 v, lc_short2 lo, lc_short2 hi) noexcept { return lc_make_short2(lc_clamp_impl(v.x, lo.x, hi.x), lc_clamp_impl(v.y, lo.y, hi.y)); }
[[nodiscard]] __device__ inline lc_short3 lc_clamp(lc_short3 v, lc_short3 lo, lc_short3 hi) noexcept { return lc_make_short3(lc_clamp_impl(v.x, lo.x, hi.x), lc_clamp_impl(v.y, lo.y, hi.y), lc_clamp_impl(v.z, lo.z, hi.z)); }
[[nodiscard]] __device__ inline lc_short4 lc_clamp(lc_short4 v, lc_short4 lo, lc_short4 hi) noexcept { return lc_make_short4(lc_clamp_impl(v.x, lo.x, hi.x), lc_clamp_impl(v.y, lo.y, hi.y), lc_clamp_impl(v.z, lo.z, hi.z), lc_clamp_impl(v.w, lo.w, hi.w)); }
[[nodiscard]] __device__ inline lc_ushort lc_clamp(lc_ushort v, lc_ushort lo, lc_ushort hi) noexcept { return lc_clamp_impl(v, lo, hi); }
[[nodiscard]] __device__ inline lc_ushort2 lc_clamp(lc_ushort2 v, lc_ushort2 lo, lc_ushort2 hi) noexcept { return lc_make_ushort2(lc_clamp_impl(v.x, lo.x, hi.x), lc_clamp_impl(v.y, lo.y, hi.y)); }
[[nodiscard]] __device__ inline lc_ushort3 lc_clamp(lc_ushort3 v, lc_ushort3 lo, lc_ushort3 hi) noexcept { return lc_make_ushort3(lc_clamp_impl(v.x, lo.x, hi.x), lc_clamp_impl(v.y, lo.y, hi.y), lc_clamp_impl(v.z, lo.z, hi.z)); }
[[nodiscard]] __device__ inline lc_ushort4 lc_clamp(lc_ushort4 v, lc_ushort4 lo, lc_ushort4 hi) noexcept { return lc_make_ushort4(lc_clamp_impl(v.x, lo.x, hi.x), lc_clamp_impl(v.y, lo.y, hi.y), lc_clamp_impl(v.z, lo.z, hi.z), lc_clamp_impl(v.w, lo.w, hi.w)); }
[[nodiscard]] __device__ inline lc_int lc_clamp(lc_int v, lc_int lo, lc_int hi) noexcept { return lc_clamp_impl(v, lo, hi); }
[[nodiscard]] __device__ inline lc_int2 lc_clamp(lc_int2 v, lc_int2 lo, lc_int2 hi) noexcept { return lc_make_int2(lc_clamp_impl(v.x, lo.x, hi.x), lc_clamp_impl(v.y, lo.y, hi.y)); }
[[nodiscard]] __device__ inline lc_int3 lc_clamp(lc_int3 v, lc_int3 lo, lc_int3 hi) noexcept { return lc_make_int3(lc_clamp_impl(v.x, lo.x, hi.x), lc_clamp_impl(v.y, lo.y, hi.y), lc_clamp_impl(v.z, lo.z, hi.z)); }
[[nodiscard]] __device__ inline lc_int4 lc_clamp(lc_int4 v, lc_int4 lo, lc_int4 hi) noexcept { return lc_make_int4(lc_clamp_impl(v.x, lo.x, hi.x), lc_clamp_impl(v.y, lo.y, hi.y), lc_clamp_impl(v.z, lo.z, hi.z), lc_clamp_impl(v.w, lo.w, hi.w)); }
[[nodiscard]] __device__ inline lc_uint lc_clamp(lc_uint v, lc_uint lo, lc_uint hi) noexcept { return lc_clamp_impl(v, lo, hi); }
[[nodiscard]] __device__ inline lc_uint2 lc_clamp(lc_uint2 v, lc_uint2 lo, lc_uint2 hi) noexcept { return lc_make_uint2(lc_clamp_impl(v.x, lo.x, hi.x), lc_clamp_impl(v.y, lo.y, hi.y)); }
[[nodiscard]] __device__ inline lc_uint3 lc_clamp(lc_uint3 v, lc_uint3 lo, lc_uint3 hi) noexcept { return lc_make_uint3(lc_clamp_impl(v.x, lo.x, hi.x), lc_clamp_impl(v.y, lo.y, hi.y), lc_clamp_impl(v.z, lo.z, hi.z)); }
[[nodiscard]] __device__ inline lc_uint4 lc_clamp(lc_uint4 v, lc_uint4 lo, lc_uint4 hi) noexcept { return lc_make_uint4(lc_clamp_impl(v.x, lo.x, hi.x), lc_clamp_impl(v.y, lo.y, hi.y), lc_clamp_impl(v.z, lo.z, hi.z), lc_clamp_impl(v.w, lo.w, hi.w)); }
[[nodiscard]] __device__ inline lc_long lc_clamp(lc_long v, lc_long lo, lc_long hi) noexcept { return lc_clamp_impl(v, lo, hi); }
[[nodiscard]] __device__ inline lc_long2 lc_clamp(lc_long2 v, lc_long2 lo, lc_long2 hi) noexcept { return lc_make_long2(lc_clamp_impl(v.x, lo.x, hi.x), lc_clamp_impl(v.y, lo.y, hi.y)); }
[[nodiscard]] __device__ inline lc_long3 lc_clamp(lc_long3 v, lc_long3 lo, lc_long3 hi) noexcept { return lc_make_long3(lc_clamp_impl(v.x, lo.x, hi.x), lc_clamp_impl(v.y, lo.y, hi.y), lc_clamp_impl(v.z, lo.z, hi.z)); }
[[nodiscard]] __device__ inline lc_long4 lc_clamp(lc_long4 v, lc_long4 lo, lc_long4 hi) noexcept { return lc_make_long4(lc_clamp_impl(v.x, lo.x, hi.x), lc_clamp_impl(v.y, lo.y, hi.y), lc_clamp_impl(v.z, lo.z, hi.z), lc_clamp_impl(v.w, lo.w, hi.w)); }
[[nodiscard]] __device__ inline lc_ulong lc_clamp(lc_ulong v, lc_ulong lo, lc_ulong hi) noexcept { return lc_clamp_impl(v, lo, hi); }
[[nodiscard]] __device__ inline lc_ulong2 lc_clamp(lc_ulong2 v, lc_ulong2 lo, lc_ulong2 hi) noexcept { return lc_make_ulong2(lc_clamp_impl(v.x, lo.x, hi.x), lc_clamp_impl(v.y, lo.y, hi.y)); }
[[nodiscard]] __device__ inline lc_ulong3 lc_clamp(lc_ulong3 v, lc_ulong3 lo, lc_ulong3 hi) noexcept { return lc_make_ulong3(lc_clamp_impl(v.x, lo.x, hi.x), lc_clamp_impl(v.y, lo.y, hi.y), lc_clamp_impl(v.z, lo.z, hi.z)); }
[[nodiscard]] __device__ inline lc_ulong4 lc_clamp(lc_ulong4 v, lc_ulong4 lo, lc_ulong4 hi) noexcept { return lc_make_ulong4(lc_clamp_impl(v.x, lo.x, hi.x), lc_clamp_impl(v.y, lo.y, hi.y), lc_clamp_impl(v.z, lo.z, hi.z), lc_clamp_impl(v.w, lo.w, hi.w)); }
[[nodiscard]] __device__ inline lc_half lc_clamp(lc_half v, lc_half lo, lc_half hi) noexcept { return lc_clamp_impl(v, lo, hi); }
[[nodiscard]] __device__ inline lc_half2 lc_clamp(lc_half2 v, lc_half2 lo, lc_half2 hi) noexcept { return lc_make_half2(lc_clamp_impl(v.x, lo.x, hi.x), lc_clamp_impl(v.y, lo.y, hi.y)); }
[[nodiscard]] __device__ inline lc_half3 lc_clamp(lc_half3 v, lc_half3 lo, lc_half3 hi) noexcept { return lc_make_half3(lc_clamp_impl(v.x, lo.x, hi.x), lc_clamp_impl(v.y, lo.y, hi.y), lc_clamp_impl(v.z, lo.z, hi.z)); }
[[nodiscard]] __device__ inline lc_half4 lc_clamp(lc_half4 v, lc_half4 lo, lc_half4 hi) noexcept { return lc_make_half4(lc_clamp_impl(v.x, lo.x, hi.x), lc_clamp_impl(v.y, lo.y, hi.y), lc_clamp_impl(v.z, lo.z, hi.z), lc_clamp_impl(v.w, lo.w, hi.w)); }
[[nodiscard]] __device__ inline lc_float lc_clamp(lc_float v, lc_float lo, lc_float hi) noexcept { return lc_clamp_impl(v, lo, hi); }
[[nodiscard]] __device__ inline lc_float2 lc_clamp(lc_float2 v, lc_float2 lo, lc_float2 hi) noexcept { return lc_make_float2(lc_clamp_impl(v.x, lo.x, hi.x), lc_clamp_impl(v.y, lo.y, hi.y)); }
[[nodiscard]] __device__ inline lc_float3 lc_clamp(lc_float3 v, lc_float3 lo, lc_float3 hi) noexcept { return lc_make_float3(lc_clamp_impl(v.x, lo.x, hi.x), lc_clamp_impl(v.y, lo.y, hi.y), lc_clamp_impl(v.z, lo.z, hi.z)); }
[[nodiscard]] __device__ inline lc_float4 lc_clamp(lc_float4 v, lc_float4 lo, lc_float4 hi) noexcept { return lc_make_float4(lc_clamp_impl(v.x, lo.x, hi.x), lc_clamp_impl(v.y, lo.y, hi.y), lc_clamp_impl(v.z, lo.z, hi.z), lc_clamp_impl(v.w, lo.w, hi.w)); }

[[nodiscard]] __device__ inline auto lc_lerp_impl(lc_half a, lc_half b, lc_half t) noexcept { return t * (b - a) + a; }
[[nodiscard]] __device__ inline auto lc_saturate(lc_half x) noexcept { return lc_clamp(x, lc_half(0.0f), lc_half(1.0f)); }
[[nodiscard]] __device__ inline auto lc_saturate(lc_half2 x) noexcept { return lc_clamp(x, lc_make_half2(0.0f), lc_make_half2(1.0f)); }
[[nodiscard]] __device__ inline auto lc_saturate(lc_half3 x) noexcept { return lc_clamp(x, lc_make_half3(0.0f), lc_make_half3(1.0f)); }
[[nodiscard]] __device__ inline auto lc_saturate(lc_half4 x) noexcept { return lc_clamp(x, lc_make_half4(0.0f), lc_make_half4(1.0f)); }

[[nodiscard]] __device__ inline auto lc_degrees_impl(lc_half rad) noexcept { return rad * (lc_half)(180.0f * 0.318309886183790671537767526745028724f); }
[[nodiscard]] __device__ inline auto lc_radians_impl(lc_half deg) noexcept { return deg * (lc_half)(3.14159265358979323846264338327950288f / 180.0f); }
[[nodiscard]] __device__ inline auto lc_step_impl(lc_half edge, lc_half x) noexcept { return lc_select(lc_half(1.f), lc_half(0.f), x < edge); }
[[nodiscard]] __device__ inline auto lc_smoothstep_impl(lc_half edge0, lc_half edge1, lc_half x) noexcept {
auto t = lc_clamp((x - edge0) / (edge1 - edge0), lc_half(0.0f), lc_half(1.0f));
return t * t * (lc_half(3.f) - lc_half(2.f) * t);
}
[[nodiscard]] __device__ inline auto lc_mod_impl(lc_half x, lc_half y) noexcept { return x - y * lc_floor(x / y); }
[[nodiscard]] __device__ inline auto lc_fmod_impl(lc_half x, lc_half y) noexcept { return x - y * lc_trunc(x / y); }
[[nodiscard]] __device__ inline auto lc_fract_impl(lc_half x) noexcept { return x - lc_floor(x); }
[[nodiscard]] __device__ inline auto lc_lerp_impl(lc_float a, lc_float b, lc_float t) noexcept { return t * (b - a) + a; }
[[nodiscard]] __device__ inline auto lc_saturate(lc_float x) noexcept { return lc_clamp(x, lc_float(0.0f), lc_float(1.0f)); }
[[nodiscard]] __device__ inline auto lc_saturate(lc_float2 x) noexcept { return lc_clamp(x, lc_make_float2(0.0f), lc_make_float2(1.0f)); }
[[nodiscard]] __device__ inline auto lc_saturate(lc_float3 x) noexcept { return lc_clamp(x, lc_make_float3(0.0f), lc_make_float3(1.0f)); }
[[nodiscard]] __device__ inline auto lc_saturate(lc_float4 x) noexcept { return lc_clamp(x, lc_make_float4(0.0f), lc_make_float4(1.0f)); }

[[nodiscard]] __device__ inline auto lc_degrees_impl(lc_float rad) noexcept { return rad * (lc_float)(180.0f * 0.318309886183790671537767526745028724f); }
[[nodiscard]] __device__ inline auto lc_radians_impl(lc_float deg) noexcept { return deg * (lc_float)(3.14159265358979323846264338327950288f / 180.0f); }
[[nodiscard]] __device__ inline auto lc_step_impl(lc_float edge, lc_float x) noexcept { return lc_select(lc_float(1.f), lc_float(0.f), x < edge); }
[[nodiscard]] __device__ inline auto lc_smoothstep_impl(lc_float edge0, lc_float edge1, lc_float x) noexcept {
auto t = lc_clamp((x - edge0) / (edge1 - edge0), lc_float(0.0f), lc_float(1.0f));
return t * t * (lc_float(3.f) - lc_float(2.f) * t);
}
[[nodiscard]] __device__ inline auto lc_mod_impl(lc_float x, lc_float y) noexcept { return x - y * lc_floor(x / y); }
[[nodiscard]] __device__ inline auto lc_fmod_impl(lc_float x, lc_float y) noexcept { return fmodf(x, y); }
[[nodiscard]] __device__ inline auto lc_fract_impl(lc_float x) noexcept { return x - lc_floor(x); }
[[nodiscard]] __device__ inline lc_half lc_lerp(lc_half a, lc_half b, lc_half t) noexcept { return lc_lerp_impl(a, b, t); }
[[nodiscard]] __device__ inline lc_half2 lc_lerp(lc_half2 a, lc_half2 b, lc_half2 t) noexcept { return lc_make_half2(lc_lerp_impl(a.x, b.x, t.x), lc_lerp_impl(a.y, b.y, t.y)); }
[[nodiscard]] __device__ inline lc_half3 lc_lerp(lc_half3 a, lc_half3 b, lc_half3 t) noexcept { return lc_make_half3(lc_lerp_impl(a.x, b.x, t.x), lc_lerp_impl(a.y, b.y, t.y), lc_lerp_impl(a.z, b.z, t.z)); }
[[nodiscard]] __device__ inline lc_half4 lc_lerp(lc_half4 a, lc_half4 b, lc_half4 t) noexcept { return lc_make_half4(lc_lerp_impl(a.x, b.x, t.x), lc_lerp_impl(a.y, b.y, t.y), lc_lerp_impl(a.z, b.z, t.z), lc_lerp_impl(a.w, b.w, t.w)); }
[[nodiscard]] __device__ inline lc_float lc_lerp(lc_float a, lc_float b, lc_float t) noexcept { return lc_lerp_impl(a, b, t); }
[[nodiscard]] __device__ inline lc_float2 lc_lerp(lc_float2 a, lc_float2 b, lc_float2 t) noexcept { return lc_make_float2(lc_lerp_impl(a.x, b.x, t.x), lc_lerp_impl(a.y, b.y, t.y)); }
[[nodiscard]] __device__ inline lc_float3 lc_lerp(lc_float3 a, lc_float3 b, lc_float3 t) noexcept { return lc_make_float3(lc_lerp_impl(a.x, b.x, t.x), lc_lerp_impl(a.y, b.y, t.y), lc_lerp_impl(a.z, b.z, t.z)); }
[[nodiscard]] __device__ inline lc_float4 lc_lerp(lc_float4 a, lc_float4 b, lc_float4 t) noexcept { return lc_make_float4(lc_lerp_impl(a.x, b.x, t.x), lc_lerp_impl(a.y, b.y, t.y), lc_lerp_impl(a.z, b.z, t.z), lc_lerp_impl(a.w, b.w, t.w)); }

[[nodiscard]] __device__ inline lc_half lc_degrees(lc_half rad) noexcept { return lc_degrees_impl(rad); }
[[nodiscard]] __device__ inline lc_half2 lc_degrees(lc_half2 rad) noexcept { return lc_make_half2(lc_degrees_impl(rad.x), lc_degrees_impl(rad.y)); }
[[nodiscard]] __device__ inline lc_half3 lc_degrees(lc_half3 rad) noexcept { return lc_make_half3(lc_degrees_impl(rad.x), lc_degrees_impl(rad.y), lc_degrees_impl(rad.z)); }
[[nodiscard]] __device__ inline lc_half4 lc_degrees(lc_half4 rad) noexcept { return lc_make_half4(lc_degrees_impl(rad.x), lc_degrees_impl(rad.y), lc_degrees_impl(rad.z), lc_degrees_impl(rad.w)); }
[[nodiscard]] __device__ inline lc_float lc_degrees(lc_float rad) noexcept { return lc_degrees_impl(rad); }
[[nodiscard]] __device__ inline lc_float2 lc_degrees(lc_float2 rad) noexcept { return lc_make_float2(lc_degrees_impl(rad.x), lc_degrees_impl(rad.y)); }
[[nodiscard]] __device__ inline lc_float3 lc_degrees(lc_float3 rad) noexcept { return lc_make_float3(lc_degrees_impl(rad.x), lc_degrees_impl(rad.y), lc_degrees_impl(rad.z)); }
[[nodiscard]] __device__ inline lc_float4 lc_degrees(lc_float4 rad) noexcept { return lc_make_float4(lc_degrees_impl(rad.x), lc_degrees_impl(rad.y), lc_degrees_impl(rad.z), lc_degrees_impl(rad.w)); }

[[nodiscard]] __device__ inline lc_half lc_radians(lc_half deg) noexcept { return lc_radians_impl(deg); }
[[nodiscard]] __device__ inline lc_half2 lc_radians(lc_half2 deg) noexcept { return lc_make_half2(lc_radians_impl(deg.x), lc_radians_impl(deg.y)); }
[[nodiscard]] __device__ inline lc_half3 lc_radians(lc_half3 deg) noexcept { return lc_make_half3(lc_radians_impl(deg.x), lc_radians_impl(deg.y), lc_radians_impl(deg.z)); }
[[nodiscard]] __device__ inline lc_half4 lc_radians(lc_half4 deg) noexcept { return lc_make_half4(lc_radians_impl(deg.x), lc_radians_impl(deg.y), lc_radians_impl(deg.z), lc_radians_impl(deg.w)); }
[[nodiscard]] __device__ inline lc_float lc_radians(lc_float deg) noexcept { return lc_radians_impl(deg); }
[[nodiscard]] __device__ inline lc_float2 lc_radians(lc_float2 deg) noexcept { return lc_make_float2(lc_radians_impl(deg.x), lc_radians_impl(deg.y)); }
[[nodiscard]] __device__ inline lc_float3 lc_radians(lc_float3 deg) noexcept { return lc_make_float3(lc_radians_impl(deg.x), lc_radians_impl(deg.y), lc_radians_impl(deg.z)); }
[[nodiscard]] __device__ inline lc_float4 lc_radians(lc_float4 deg) noexcept { return lc_make_float4(lc_radians_impl(deg.x), lc_radians_impl(deg.y), lc_radians_impl(deg.z), lc_radians_impl(deg.w)); }

[[nodiscard]] __device__ inline lc_half lc_step(lc_half edge, lc_half x) noexcept { return lc_step_impl(edge, x); }
[[nodiscard]] __device__ inline lc_half2 lc_step(lc_half2 edge, lc_half2 x) noexcept { return lc_make_half2(lc_step_impl(edge.x, x.x), lc_step_impl(edge.y, x.y)); }
[[nodiscard]] __device__ inline lc_half3 lc_step(lc_half3 edge, lc_half3 x) noexcept { return lc_make_half3(lc_step_impl(edge.x, x.x), lc_step_impl(edge.y, x.y), lc_step_impl(edge.z, x.z)); }
[[nodiscard]] __device__ inline lc_half4 lc_step(lc_half4 edge, lc_half4 x) noexcept { return lc_make_half4(lc_step_impl(edge.x, x.x), lc_step_impl(edge.y, x.y), lc_step_impl(edge.z, x.z), lc_step_impl(edge.w, x.w)); }
[[nodiscard]] __device__ inline lc_float lc_step(lc_float edge, lc_float x) noexcept { return lc_step_impl(edge, x); }
[[nodiscard]] __device__ inline lc_float2 lc_step(lc_float2 edge, lc_float2 x) noexcept { return lc_make_float2(lc_step_impl(edge.x, x.x), lc_step_impl(edge.y, x.y)); }
[[nodiscard]] __device__ inline lc_float3 lc_step(lc_float3 edge, lc_float3 x) noexcept { return lc_make_float3(lc_step_impl(edge.x, x.x), lc_step_impl(edge.y, x.y), lc_step_impl(edge.z, x.z)); }
[[nodiscard]] __device__ inline lc_float4 lc_step(lc_float4 edge, lc_float4 x) noexcept { return lc_make_float4(lc_step_impl(edge.x, x.x), lc_step_impl(edge.y, x.y), lc_step_impl(edge.z, x.z), lc_step_impl(edge.w, x.w)); }

[[nodiscard]] __device__ inline lc_half lc_smoothstep(lc_half e0, lc_half e1, lc_half x) noexcept { return lc_smoothstep_impl(e0, e1, x); }
[[nodiscard]] __device__ inline lc_half2 lc_smoothstep(lc_half2 e0, lc_half2 e1, lc_half2 x) noexcept { return lc_make_half2(lc_smoothstep_impl(e0.x, e1.x, x.x), lc_smoothstep_impl(e0.y, e1.y, x.y)); }
[[nodiscard]] __device__ inline lc_half3 lc_smoothstep(lc_half3 e0, lc_half3 e1, lc_half3 x) noexcept { return lc_make_half3(lc_smoothstep_impl(e0.x, e1.x, x.x), lc_smoothstep_impl(e0.y, e1.y, x.y), lc_smoothstep_impl(e0.z, e1.z, x.z)); }
[[nodiscard]] __device__ inline lc_half4 lc_smoothstep(lc_half4 e0, lc_half4 e1, lc_half4 x) noexcept { return lc_make_half4(lc_smoothstep_impl(e0.x, e1.x, x.x), lc_smoothstep_impl(e0.y, e1.y, x.y), lc_smoothstep_impl(e0.z, e1.z, x.z), lc_smoothstep_impl(e0.w, e1.w, x.w)); }
[[nodiscard]] __device__ inline lc_float lc_smoothstep(lc_float e0, lc_float e1, lc_float x) noexcept { return lc_smoothstep_impl(e0, e1, x); }
[[nodiscard]] __device__ inline lc_float2 lc_smoothstep(lc_float2 e0, lc_float2 e1, lc_float2 x) noexcept { return lc_make_float2(lc_smoothstep_impl(e0.x, e1.x, x.x), lc_smoothstep_impl(e0.y, e1.y, x.y)); }
[[nodiscard]] __device__ inline lc_float3 lc_smoothstep(lc_float3 e0, lc_float3 e1, lc_float3 x) noexcept { return lc_make_float3(lc_smoothstep_impl(e0.x, e1.x, x.x), lc_smoothstep_impl(e0.y, e1.y, x.y), lc_smoothstep_impl(e0.z, e1.z, x.z)); }
[[nodiscard]] __device__ inline lc_float4 lc_smoothstep(lc_float4 e0, lc_float4 e1, lc_float4 x) noexcept { return lc_make_float4(lc_smoothstep_impl(e0.x, e1.x, x.x), lc_smoothstep_impl(e0.y, e1.y, x.y), lc_smoothstep_impl(e0.z, e1.z, x.z), lc_smoothstep_impl(e0.w, e1.w, x.w)); }

[[nodiscard]] __device__ inline lc_half lc_mod(lc_half x, lc_half y) noexcept { return lc_mod_impl(x, y); }
[[nodiscard]] __device__ inline lc_half2 lc_mod(lc_half2 x, lc_half2 y) noexcept { return lc_make_half2(lc_mod_impl(x.x, y.x), lc_mod_impl(x.y, y.y)); }
[[nodiscard]] __device__ inline lc_half3 lc_mod(lc_half3 x, lc_half3 y) noexcept { return lc_make_half3(lc_mod_impl(x.x, y.x), lc_mod_impl(x.y, y.y), lc_mod_impl(x.z, y.z)); }
[[nodiscard]] __device__ inline lc_half4 lc_mod(lc_half4 x, lc_half4 y) noexcept { return lc_make_half4(lc_mod_impl(x.x, y.x), lc_mod_impl(x.y, y.y), lc_mod_impl(x.z, y.z), lc_mod_impl(x.w, y.w)); }
[[nodiscard]] __device__ inline lc_float lc_mod(lc_float x, lc_float y) noexcept { return lc_mod_impl(x, y); }
[[nodiscard]] __device__ inline lc_float2 lc_mod(lc_float2 x, lc_float2 y) noexcept { return lc_make_float2(lc_mod_impl(x.x, y.x), lc_mod_impl(x.y, y.y)); }
[[nodiscard]] __device__ inline lc_float3 lc_mod(lc_float3 x, lc_float3 y) noexcept { return lc_make_float3(lc_mod_impl(x.x, y.x), lc_mod_impl(x.y, y.y), lc_mod_impl(x.z, y.z)); }
[[nodiscard]] __device__ inline lc_float4 lc_mod(lc_float4 x, lc_float4 y) noexcept { return lc_make_float4(lc_mod_impl(x.x, y.x), lc_mod_impl(x.y, y.y), lc_mod_impl(x.z, y.z), lc_mod_impl(x.w, y.w)); }

[[nodiscard]] __device__ inline lc_half lc_fmod(lc_half x, lc_half y) noexcept { return lc_fmod_impl(x, y); }
[[nodiscard]] __device__ inline lc_half2 lc_fmod(lc_half2 x, lc_half2 y) noexcept { return lc_make_half2(lc_fmod_impl(x.x, y.x), lc_fmod_impl(x.y, y.y)); }
[[nodiscard]] __device__ inline lc_half3 lc_fmod(lc_half3 x, lc_half3 y) noexcept { return lc_make_half3(lc_fmod_impl(x.x, y.x), lc_fmod_impl(x.y, y.y), lc_fmod_impl(x.z, y.z)); }
[[nodiscard]] __device__ inline lc_half4 lc_fmod(lc_half4 x, lc_half4 y) noexcept { return lc_make_half4(lc_fmod_impl(x.x, y.x), lc_fmod_impl(x.y, y.y), lc_fmod_impl(x.z, y.z), lc_fmod_impl(x.w, y.w)); }
[[nodiscard]] __device__ inline lc_float lc_fmod(lc_float x, lc_float y) noexcept { return lc_fmod_impl(x, y); }
[[nodiscard]] __device__ inline lc_float2 lc_fmod(lc_float2 x, lc_float2 y) noexcept { return lc_make_float2(lc_fmod_impl(x.x, y.x), lc_fmod_impl(x.y, y.y)); }
[[nodiscard]] __device__ inline lc_float3 lc_fmod(lc_float3 x, lc_float3 y) noexcept { return lc_make_float3(lc_fmod_impl(x.x, y.x), lc_fmod_impl(x.y, y.y), lc_fmod_impl(x.z, y.z)); }
[[nodiscard]] __device__ inline lc_float4 lc_fmod(lc_float4 x, lc_float4 y) noexcept { return lc_make_float4(lc_fmod_impl(x.x, y.x), lc_fmod_impl(x.y, y.y), lc_fmod_impl(x.z, y.z), lc_fmod_impl(x.w, y.w)); }

[[nodiscard]] __device__ inline lc_half lc_fract(lc_half x) noexcept { return lc_fract_impl(x); }
[[nodiscard]] __device__ inline lc_half2 lc_fract(lc_half2 x) noexcept { return lc_make_half2(lc_fract_impl(x.x), lc_fract_impl(x.y)); }
[[nodiscard]] __device__ inline lc_half3 lc_fract(lc_half3 x) noexcept { return lc_make_half3(lc_fract_impl(x.x), lc_fract_impl(x.y), lc_fract_impl(x.z)); }
[[nodiscard]] __device__ inline lc_half4 lc_fract(lc_half4 x) noexcept { return lc_make_half4(lc_fract_impl(x.x), lc_fract_impl(x.y), lc_fract_impl(x.z), lc_fract_impl(x.w)); }
[[nodiscard]] __device__ inline lc_float lc_fract(lc_float x) noexcept { return lc_fract_impl(x); }
[[nodiscard]] __device__ inline lc_float2 lc_fract(lc_float2 x) noexcept { return lc_make_float2(lc_fract_impl(x.x), lc_fract_impl(x.y)); }
[[nodiscard]] __device__ inline lc_float3 lc_fract(lc_float3 x) noexcept { return lc_make_float3(lc_fract_impl(x.x), lc_fract_impl(x.y), lc_fract_impl(x.z)); }
[[nodiscard]] __device__ inline lc_float4 lc_fract(lc_float4 x) noexcept { return lc_make_float4(lc_fract_impl(x.x), lc_fract_impl(x.y), lc_fract_impl(x.z), lc_fract_impl(x.w)); }

[[nodiscard]] __device__ inline lc_uint lc_clz(lc_uint x) noexcept { return __clz(x); }
[[nodiscard]] __device__ inline lc_uint2 lc_clz(lc_uint2 x) noexcept { return lc_make_uint2(__clz(x.x), __clz(x.y)); }
[[nodiscard]] __device__ inline lc_uint3 lc_clz(lc_uint3 x) noexcept { return lc_make_uint3(__clz(x.x), __clz(x.y), __clz(x.z)); }
[[nodiscard]] __device__ inline lc_uint4 lc_clz(lc_uint4 x) noexcept { return lc_make_uint4(__clz(x.x), __clz(x.y), __clz(x.z), __clz(x.w)); }

[[nodiscard]] __device__ inline lc_ulong lc_clz(lc_ulong x) noexcept { return __clzll(x); }
[[nodiscard]] __device__ inline lc_ulong2 lc_clz(lc_ulong2 x) noexcept { return lc_make_ulong2(__clzll(x.x), __clzll(x.y)); }
[[nodiscard]] __device__ inline lc_ulong3 lc_clz(lc_ulong3 x) noexcept { return lc_make_ulong3(__clzll(x.x), __clzll(x.y), __clzll(x.z)); }
[[nodiscard]] __device__ inline lc_ulong4 lc_clz(lc_ulong4 x) noexcept { return lc_make_ulong4(__clzll(x.x), __clzll(x.y), __clzll(x.z), __clzll(x.w)); }

[[nodiscard]] __device__ inline lc_uint lc_popcount(lc_uint x) noexcept { return __popc(x); }
[[nodiscard]] __device__ inline lc_uint2 lc_popcount(lc_uint2 x) noexcept { return lc_make_uint2(__popc(x.x), __popc(x.y)); }
[[nodiscard]] __device__ inline lc_uint3 lc_popcount(lc_uint3 x) noexcept { return lc_make_uint3(__popc(x.x), __popc(x.y), __popc(x.z)); }
[[nodiscard]] __device__ inline lc_uint4 lc_popcount(lc_uint4 x) noexcept { return lc_make_uint4(__popc(x.x), __popc(x.y), __popc(x.z), __popc(x.w)); }

[[nodiscard]] __device__ inline lc_ulong lc_popcount(lc_ulong x) noexcept { return __popcll(x); }
[[nodiscard]] __device__ inline lc_ulong2 lc_popcount(lc_ulong2 x) noexcept { return lc_make_ulong2(__popcll(x.x), __popcll(x.y)); }
[[nodiscard]] __device__ inline lc_ulong3 lc_popcount(lc_ulong3 x) noexcept { return lc_make_ulong3(__popcll(x.x), __popcll(x.y), __popcll(x.z)); }
[[nodiscard]] __device__ inline lc_ulong4 lc_popcount(lc_ulong4 x) noexcept { return lc_make_ulong4(__popcll(x.x), __popcll(x.y), __popcll(x.z), __popcll(x.w)); }

[[nodiscard]] __device__ inline lc_uint lc_reverse(lc_uint x) noexcept { return __brev(x); }
[[nodiscard]] __device__ inline lc_uint2 lc_reverse(lc_uint2 x) noexcept { return lc_make_uint2(__brev(x.x), __brev(x.y)); }
[[nodiscard]] __device__ inline lc_uint3 lc_reverse(lc_uint3 x) noexcept { return lc_make_uint3(__brev(x.x), __brev(x.y), __brev(x.z)); }
[[nodiscard]] __device__ inline lc_uint4 lc_reverse(lc_uint4 x) noexcept { return lc_make_uint4(__brev(x.x), __brev(x.y), __brev(x.z), __brev(x.w)); }

[[nodiscard]] __device__ inline lc_ulong lc_reverse(lc_ulong x) noexcept { return __brevll(x); }
[[nodiscard]] __device__ inline lc_ulong2 lc_reverse(lc_ulong2 x) noexcept { return lc_make_ulong2(__brevll(x.x), __brevll(x.y)); }
[[nodiscard]] __device__ inline lc_ulong3 lc_reverse(lc_ulong3 x) noexcept { return lc_make_ulong3(__brevll(x.x), __brevll(x.y), __brevll(x.z)); }
[[nodiscard]] __device__ inline lc_ulong4 lc_reverse(lc_ulong4 x) noexcept { return lc_make_ulong4(__brevll(x.x), __brevll(x.y), __brevll(x.z), __brevll(x.w)); }

[[nodiscard]] __device__ inline auto lc_ctz_impl(lc_uint x) noexcept { return (__ffs(x) - 1u) % 32u; }
[[nodiscard]] __device__ inline auto lc_ctz_impl(lc_ulong x) noexcept { return (__ffsll(x) - 1u) % 64u; }
[[nodiscard]] __device__ inline lc_uint lc_ctz(lc_uint x) noexcept { return lc_ctz_impl(x); }
[[nodiscard]] __device__ inline lc_uint2 lc_ctz(lc_uint2 x) noexcept { return lc_make_uint2(lc_ctz_impl(x.x), lc_ctz_impl(x.y)); }
[[nodiscard]] __device__ inline lc_uint3 lc_ctz(lc_uint3 x) noexcept { return lc_make_uint3(lc_ctz_impl(x.x), lc_ctz_impl(x.y), lc_ctz_impl(x.z)); }
[[nodiscard]] __device__ inline lc_uint4 lc_ctz(lc_uint4 x) noexcept { return lc_make_uint4(lc_ctz_impl(x.x), lc_ctz_impl(x.y), lc_ctz_impl(x.z), lc_ctz_impl(x.w)); }
[[nodiscard]] __device__ inline lc_ulong lc_ctz(lc_ulong x) noexcept { return lc_ctz_impl(x); }
[[nodiscard]] __device__ inline lc_ulong2 lc_ctz(lc_ulong2 x) noexcept { return lc_make_ulong2(lc_ctz_impl(x.x), lc_ctz_impl(x.y)); }
[[nodiscard]] __device__ inline lc_ulong3 lc_ctz(lc_ulong3 x) noexcept { return lc_make_ulong3(lc_ctz_impl(x.x), lc_ctz_impl(x.y), lc_ctz_impl(x.z)); }
[[nodiscard]] __device__ inline lc_ulong4 lc_ctz(lc_ulong4 x) noexcept { return lc_make_ulong4(lc_ctz_impl(x.x), lc_ctz_impl(x.y), lc_ctz_impl(x.z), lc_ctz_impl(x.w)); }

[[nodiscard]] __device__ inline constexpr auto lc_cross(lc_float3 u, lc_float3 v) noexcept {
return lc_make_float3(u.y * v.z - v.y * u.z,
                    u.z * v.x - v.z * u.x,
                    u.x * v.y - v.x * u.y);
}

[[nodiscard]] __device__ inline auto lc_dot(lc_float2 a, lc_float2 b) noexcept {
return a.x * b.x + a.y * b.y;
}
[[nodiscard]] __device__ inline auto lc_dot(lc_float3 a, lc_float3 b) noexcept {
return a.x * b.x + a.y * b.y + a.z * b.z;
}
[[nodiscard]] __device__ inline auto lc_dot(lc_float4 a, lc_float4 b) noexcept {
return a.x * b.x + a.y * b.y + a.z * b.z + a.w * b.w;
}

[[nodiscard]] __device__ inline auto lc_length(lc_float2 v) noexcept { return lc_sqrt(lc_dot(v, v)); }
[[nodiscard]] __device__ inline auto lc_length(lc_float3 v) noexcept { return lc_sqrt(lc_dot(v, v)); }
[[nodiscard]] __device__ inline auto lc_length(lc_float4 v) noexcept { return lc_sqrt(lc_dot(v, v)); }

[[nodiscard]] __device__ inline auto lc_length_squared(lc_float2 v) noexcept { return lc_dot(v, v); }
[[nodiscard]] __device__ inline auto lc_length_squared(lc_float3 v) noexcept { return lc_dot(v, v); }
[[nodiscard]] __device__ inline auto lc_length_squared(lc_float4 v) noexcept { return lc_dot(v, v); }

[[nodiscard]] __device__ inline auto lc_distance(lc_float2 a, lc_float2 b) noexcept { return lc_length(a - b); }
[[nodiscard]] __device__ inline auto lc_distance(lc_float3 a, lc_float3 b) noexcept { return lc_length(a - b); }
[[nodiscard]] __device__ inline auto lc_distance(lc_float4 a, lc_float4 b) noexcept { return lc_length(a - b); }

[[nodiscard]] __device__ inline auto lc_distance_squared(lc_float2 a, lc_float2 b) noexcept { return lc_length_squared(a - b); }
[[nodiscard]] __device__ inline auto lc_distance_squared(lc_float3 a, lc_float3 b) noexcept { return lc_length_squared(a - b); }
[[nodiscard]] __device__ inline auto lc_distance_squared(lc_float4 a, lc_float4 b) noexcept { return lc_length_squared(a - b); }

[[nodiscard]] __device__ inline auto lc_faceforward(lc_float3 n, lc_float3 i, lc_float3 n_ref) noexcept { return lc_select(-n, n, lc_dot(n_ref, i) < lc_float(0.f)); }

[[nodiscard]] __device__ inline auto lc_normalize(lc_float2 v) noexcept { return v * lc_rsqrt(lc_dot(v, v)); }
[[nodiscard]] __device__ inline auto lc_normalize(lc_float3 v) noexcept { return v * lc_rsqrt(lc_dot(v, v)); }
[[nodiscard]] __device__ inline auto lc_normalize(lc_float4 v) noexcept { return v * lc_rsqrt(lc_dot(v, v)); }

[[nodiscard]] __device__ inline constexpr auto lc_cross(lc_half3 u, lc_half3 v) noexcept {
return lc_make_half3(u.y * v.z - v.y * u.z,
                    u.z * v.x - v.z * u.x,
                    u.x * v.y - v.x * u.y);
}

[[nodiscard]] __device__ inline auto lc_dot(lc_half2 a, lc_half2 b) noexcept {
return a.x * b.x + a.y * b.y;
}
[[nodiscard]] __device__ inline auto lc_dot(lc_half3 a, lc_half3 b) noexcept {
return a.x * b.x + a.y * b.y + a.z * b.z;
}
[[nodiscard]] __device__ inline auto lc_dot(lc_half4 a, lc_half4 b) noexcept {
return a.x * b.x + a.y * b.y + a.z * b.z + a.w * b.w;
}

[[nodiscard]] __device__ inline auto lc_length(lc_half2 v) noexcept { return lc_sqrt(lc_dot(v, v)); }
[[nodiscard]] __device__ inline auto lc_length(lc_half3 v) noexcept { return lc_sqrt(lc_dot(v, v)); }
[[nodiscard]] __device__ inline auto lc_length(lc_half4 v) noexcept { return lc_sqrt(lc_dot(v, v)); }

[[nodiscard]] __device__ inline auto lc_length_squared(lc_half2 v) noexcept { return lc_dot(v, v); }
[[nodiscard]] __device__ inline auto lc_length_squared(lc_half3 v) noexcept { return lc_dot(v, v); }
[[nodiscard]] __device__ inline auto lc_length_squared(lc_half4 v) noexcept { return lc_dot(v, v); }

[[nodiscard]] __device__ inline auto lc_distance(lc_half2 a, lc_half2 b) noexcept { return lc_length(a - b); }
[[nodiscard]] __device__ inline auto lc_distance(lc_half3 a, lc_half3 b) noexcept { return lc_length(a - b); }
[[nodiscard]] __device__ inline auto lc_distance(lc_half4 a, lc_half4 b) noexcept { return lc_length(a - b); }

[[nodiscard]] __device__ inline auto lc_distance_squared(lc_half2 a, lc_half2 b) noexcept { return lc_length_squared(a - b); }
[[nodiscard]] __device__ inline auto lc_distance_squared(lc_half3 a, lc_half3 b) noexcept { return lc_length_squared(a - b); }
[[nodiscard]] __device__ inline auto lc_distance_squared(lc_half4 a, lc_half4 b) noexcept { return lc_length_squared(a - b); }

[[nodiscard]] __device__ inline auto lc_faceforward(lc_half3 n, lc_half3 i, lc_half3 n_ref) noexcept { return lc_select(-n, n, lc_dot(n_ref, i) < lc_half(0.f)); }

[[nodiscard]] __device__ inline auto lc_normalize(lc_half2 v) noexcept { return v * lc_rsqrt(lc_dot(v, v)); }
[[nodiscard]] __device__ inline auto lc_normalize(lc_half3 v) noexcept { return v * lc_rsqrt(lc_dot(v, v)); }
[[nodiscard]] __device__ inline auto lc_normalize(lc_half4 v) noexcept { return v * lc_rsqrt(lc_dot(v, v)); }

[[nodiscard]] __device__ inline constexpr auto lc_transpose(const lc_float2x2 m) noexcept { return lc_make_float2x2(m[0].x, m[1].x, m[0].y, m[1].y); }
[[nodiscard]] __device__ inline constexpr auto lc_transpose(const lc_float3x3 m) noexcept { return lc_make_float3x3(m[0].x, m[1].x, m[2].x, m[0].y, m[1].y, m[2].y, m[0].z, m[1].z, m[2].z); }
[[nodiscard]] __device__ inline constexpr auto lc_transpose(const lc_float4x4 m) noexcept { return lc_make_float4x4(m[0].x, m[1].x, m[2].x, m[3].x, m[0].y, m[1].y, m[2].y, m[3].y, m[0].z, m[1].z, m[2].z, m[3].z, m[0].w, m[1].w, m[2].w, m[3].w); }

[[nodiscard]] __device__ inline constexpr auto lc_determinant(const lc_float2x2 m) noexcept {
return m[0][0] * m[1][1] - m[1][0] * m[0][1];
}

[[nodiscard]] __device__ constexpr auto lc_determinant(const lc_float3x3 m) noexcept {// from GLM
return m[0].x * (m[1].y * m[2].z - m[2].y * m[1].z)
    - m[1].x * (m[0].y * m[2].z - m[2].y * m[0].z)
    + m[2].x * (m[0].y * m[1].z - m[1].y * m[0].z);
}

[[nodiscard]] __device__ inline constexpr auto lc_determinant(const lc_float4x4 m) noexcept {// from GLM
const auto coef00 = m[2].z * m[3].w - m[3].z * m[2].w;
const auto coef02 = m[1].z * m[3].w - m[3].z * m[1].w;
const auto coef03 = m[1].z * m[2].w - m[2].z * m[1].w;
const auto coef04 = m[2].y * m[3].w - m[3].y * m[2].w;
const auto coef06 = m[1].y * m[3].w - m[3].y * m[1].w;
const auto coef07 = m[1].y * m[2].w - m[2].y * m[1].w;
const auto coef08 = m[2].y * m[3].z - m[3].y * m[2].z;
const auto coef10 = m[1].y * m[3].z - m[3].y * m[1].z;
const auto coef11 = m[1].y * m[2].z - m[2].y * m[1].z;
const auto coef12 = m[2].x * m[3].w - m[3].x * m[2].w;
const auto coef14 = m[1].x * m[3].w - m[3].x * m[1].w;
const auto coef15 = m[1].x * m[2].w - m[2].x * m[1].w;
const auto coef16 = m[2].x * m[3].z - m[3].x * m[2].z;
const auto coef18 = m[1].x * m[3].z - m[3].x * m[1].z;
const auto coef19 = m[1].x * m[2].z - m[2].x * m[1].z;
const auto coef20 = m[2].x * m[3].y - m[3].x * m[2].y;
const auto coef22 = m[1].x * m[3].y - m[3].x * m[1].y;
const auto coef23 = m[1].x * m[2].y - m[2].x * m[1].y;
const auto fac0 = lc_make_float4(coef00, coef00, coef02, coef03);
const auto fac1 = lc_make_float4(coef04, coef04, coef06, coef07);
const auto fac2 = lc_make_float4(coef08, coef08, coef10, coef11);
const auto fac3 = lc_make_float4(coef12, coef12, coef14, coef15);
const auto fac4 = lc_make_float4(coef16, coef16, coef18, coef19);
const auto fac5 = lc_make_float4(coef20, coef20, coef22, coef23);
const auto Vec0 = lc_make_float4(m[1].x, m[0].x, m[0].x, m[0].x);
const auto Vec1 = lc_make_float4(m[1].y, m[0].y, m[0].y, m[0].y);
const auto Vec2 = lc_make_float4(m[1].z, m[0].z, m[0].z, m[0].z);
const auto Vec3 = lc_make_float4(m[1].w, m[0].w, m[0].w, m[0].w);
const auto inv0 = Vec1 * fac0 - Vec2 * fac1 + Vec3 * fac2;
const auto inv1 = Vec0 * fac0 - Vec2 * fac3 + Vec3 * fac4;
const auto inv2 = Vec0 * fac1 - Vec1 * fac3 + Vec3 * fac5;
const auto inv3 = Vec0 * fac2 - Vec1 * fac4 + Vec2 * fac5;
constexpr auto sign_a = lc_make_float4(+1.0f, -1.0f, +1.0f, -1.0f);
constexpr auto sign_b = lc_make_float4(-1.0f, +1.0f, -1.0f, +1.0f);
const auto inv_0 = inv0 * sign_a;
const auto inv_1 = inv1 * sign_b;
const auto inv_2 = inv2 * sign_a;
const auto inv_3 = inv3 * sign_b;
const auto dot0 = m[0] * lc_make_float4(inv_0.x, inv_1.x, inv_2.x, inv_3.x);
return dot0.x + dot0.y + dot0.z + dot0.w;
}

[[nodiscard]] __device__ inline constexpr auto lc_inverse(const lc_float2x2 m) noexcept {
const auto one_over_determinant = 1.0f / (m[0][0] * m[1][1] - m[1][0] * m[0][1]);
return lc_make_float2x2(m[1][1] * one_over_determinant,
                    - m[0][1] * one_over_determinant,
                    - m[1][0] * one_over_determinant,
                    + m[0][0] * one_over_determinant);
}

[[nodiscard]] __device__ inline constexpr auto lc_inverse(const lc_float3x3 m) noexcept {// from GLM
const auto one_over_determinant = 1.0f
                                / (m[0].x * (m[1].y * m[2].z - m[2].y * m[1].z)
                                - m[1].x * (m[0].y * m[2].z - m[2].y * m[0].z)
                                + m[2].x * (m[0].y * m[1].z - m[1].y * m[0].z));
return lc_make_float3x3(
    (m[1].y * m[2].z - m[2].y * m[1].z) * one_over_determinant,
    (m[2].y * m[0].z - m[0].y * m[2].z) * one_over_determinant,
    (m[0].y * m[1].z - m[1].y * m[0].z) * one_over_determinant,
    (m[2].x * m[1].z - m[1].x * m[2].z) * one_over_determinant,
    (m[0].x * m[2].z - m[2].x * m[0].z) * one_over_determinant,
    (m[1].x * m[0].z - m[0].x * m[1].z) * one_over_determinant,
    (m[1].x * m[2].y - m[2].x * m[1].y) * one_over_determinant,
    (m[2].x * m[0].y - m[0].x * m[2].y) * one_over_determinant,
    (m[0].x * m[1].y - m[1].x * m[0].y) * one_over_determinant);
}

[[nodiscard]] __device__ inline constexpr auto lc_inverse(const lc_float4x4 m) noexcept {// from GLM
const auto coef00 = m[2].z * m[3].w - m[3].z * m[2].w;
const auto coef02 = m[1].z * m[3].w - m[3].z * m[1].w;
const auto coef03 = m[1].z * m[2].w - m[2].z * m[1].w;
const auto coef04 = m[2].y * m[3].w - m[3].y * m[2].w;
const auto coef06 = m[1].y * m[3].w - m[3].y * m[1].w;
const auto coef07 = m[1].y * m[2].w - m[2].y * m[1].w;
const auto coef08 = m[2].y * m[3].z - m[3].y * m[2].z;
const auto coef10 = m[1].y * m[3].z - m[3].y * m[1].z;
const auto coef11 = m[1].y * m[2].z - m[2].y * m[1].z;
const auto coef12 = m[2].x * m[3].w - m[3].x * m[2].w;
const auto coef14 = m[1].x * m[3].w - m[3].x * m[1].w;
const auto coef15 = m[1].x * m[2].w - m[2].x * m[1].w;
const auto coef16 = m[2].x * m[3].z - m[3].x * m[2].z;
const auto coef18 = m[1].x * m[3].z - m[3].x * m[1].z;
const auto coef19 = m[1].x * m[2].z - m[2].x * m[1].z;
const auto coef20 = m[2].x * m[3].y - m[3].x * m[2].y;
const auto coef22 = m[1].x * m[3].y - m[3].x * m[1].y;
const auto coef23 = m[1].x * m[2].y - m[2].x * m[1].y;
const auto fac0 = lc_make_float4(coef00, coef00, coef02, coef03);
const auto fac1 = lc_make_float4(coef04, coef04, coef06, coef07);
const auto fac2 = lc_make_float4(coef08, coef08, coef10, coef11);
const auto fac3 = lc_make_float4(coef12, coef12, coef14, coef15);
const auto fac4 = lc_make_float4(coef16, coef16, coef18, coef19);
const auto fac5 = lc_make_float4(coef20, coef20, coef22, coef23);
const auto Vec0 = lc_make_float4(m[1].x, m[0].x, m[0].x, m[0].x);
const auto Vec1 = lc_make_float4(m[1].y, m[0].y, m[0].y, m[0].y);
const auto Vec2 = lc_make_float4(m[1].z, m[0].z, m[0].z, m[0].z);
const auto Vec3 = lc_make_float4(m[1].w, m[0].w, m[0].w, m[0].w);
const auto inv0 = Vec1 * fac0 - Vec2 * fac1 + Vec3 * fac2;
const auto inv1 = Vec0 * fac0 - Vec2 * fac3 + Vec3 * fac4;
const auto inv2 = Vec0 * fac1 - Vec1 * fac3 + Vec3 * fac5;
const auto inv3 = Vec0 * fac2 - Vec1 * fac4 + Vec2 * fac5;
constexpr auto sign_a = lc_make_float4(+1.0f, -1.0f, +1.0f, -1.0f);
constexpr auto sign_b = lc_make_float4(-1.0f, +1.0f, -1.0f, +1.0f);
const auto inv_0 = inv0 * sign_a;
const auto inv_1 = inv1 * sign_b;
const auto inv_2 = inv2 * sign_a;
const auto inv_3 = inv3 * sign_b;
const auto dot0 = m[0] * lc_make_float4(inv_0.x, inv_1.x, inv_2.x, inv_3.x);
const auto dot1 = dot0.x + dot0.y + dot0.z + dot0.w;
const auto one_over_determinant = 1.0f / dot1;
return lc_make_float4x4(inv_0 * one_over_determinant,
                        inv_1 * one_over_determinant,
                        inv_2 * one_over_determinant,
                        inv_3 * one_over_determinant);
}

[[nodiscard]] __device__ inline auto lc_reflect(const lc_float3 v, const lc_float3 n) noexcept {
return v - 2.0f * lc_dot(v, n) * n;
}

template<typename D, typename S>
[[nodiscard]] __device__ inline auto lc_bit_cast(S s) noexcept {
static_assert(sizeof(D) == sizeof(S));
return reinterpret_cast<const D &>(s);
}
template<class T>
[[nodiscard]] __device__ inline constexpr auto lc_zero() noexcept {
return T{};
}
template<class T>
[[nodiscard]] __device__ inline constexpr auto lc_one() noexcept {
return T::one();
}
template<>
[[nodiscard]] __device__ inline constexpr auto lc_one<lc_int>() noexcept {
return lc_int(1);
}
template<>
[[nodiscard]] __device__ inline constexpr auto lc_one<lc_float>() noexcept {
return lc_float(1.0f);
}
template<>
[[nodiscard]] __device__ inline auto lc_one<lc_half>() noexcept {
return lc_half(1.0f);
}
template<>
[[nodiscard]] __device__ inline constexpr auto lc_one<lc_uint>() noexcept {
return lc_uint(1u);
}
template<>
[[nodiscard]] __device__ inline constexpr auto lc_one<lc_long>() noexcept {
return lc_long(1);
}
template<>
[[nodiscard]] __device__ inline constexpr auto lc_one<lc_ulong>() noexcept {
return lc_ulong(1);
}
template<>
[[nodiscard]] __device__ inline constexpr auto lc_one<lc_short>() noexcept {
return lc_short(1);
}
template<>
[[nodiscard]] __device__ inline constexpr auto lc_one<lc_ushort>() noexcept {
return lc_ushort(1);
}
template<>
[[nodiscard]] __device__ inline constexpr auto lc_one<lc_byte>() noexcept {
return lc_byte(1);
}
template<>
[[nodiscard]] __device__ inline constexpr auto lc_one<lc_ubyte>() noexcept {
return lc_ubyte(1);
}
template<>
[[nodiscard]] __device__ inline constexpr auto lc_one<lc_bool>() noexcept {
return true;
}
template<typename T>
struct lc_ptr {
    T *data{};
    explicit lc_ptr(lc_ulong addr) noexcept : data(reinterpret_cast<T *>(addr)) {}
    T &operator[](size_t i) noexcept { return data[i]; }
    T &operator*() noexcept { return *data; }
};
template<typename T, size_t N>
class lc_array {

private:
T _data[N];

public:
template<typename... Elem>
__device__ constexpr lc_array(Elem... elem) noexcept : _data{elem...} {}
__device__ constexpr lc_array(lc_array &&) noexcept = default;
__device__ constexpr lc_array(const lc_array &) noexcept = default;
__device__ constexpr lc_array &operator=(lc_array &&) noexcept = default;
__device__ constexpr lc_array &operator=(const lc_array &) noexcept = default;
[[nodiscard]] __device__ T &operator[](size_t i) noexcept { return _data[i]; }
[[nodiscard]] __device__ T operator[](size_t i) const noexcept { return _data[i]; }

public:
[[nodiscard]] __device__ static auto one() noexcept {
    lc_array<T, N> ret;
    #pragma unroll
    for (auto i = 0u; i < N; i++) { ret[i] = lc_one<T>(); }
    return ret;
}
};

[[nodiscard]] __device__ inline auto lc_mat_comp_mul(lc_float2x2 lhs, lc_float2x2 rhs) noexcept {
return lc_make_float2x2(lhs[0] * rhs[0],
                        lhs[1] * rhs[1]);
}

[[nodiscard]] __device__ inline auto lc_mat_comp_mul(lc_float3x3 lhs, lc_float3x3 rhs) noexcept {
return lc_make_float3x3(lhs[0] * rhs[0],
                        lhs[1] * rhs[1],
                        lhs[2] * rhs[2]);
}

[[nodiscard]] __device__ inline auto lc_mat_comp_mul(lc_float4x4 lhs, lc_float4x4 rhs) noexcept {
return lc_make_float4x4(lhs[0] * rhs[0],
                        lhs[1] * rhs[1],
                        lhs[2] * rhs[2],
                        lhs[3] * rhs[3]);
}

template<class T> struct element_type_{using type = void;};
template<class T> using element_type = typename element_type_<T>::type;

template<> struct element_type_<lc_float2> { using type = lc_float; };
template<> struct element_type_<lc_float3> { using type = lc_float; };
template<> struct element_type_<lc_float4> { using type = lc_float; };
template<> struct element_type_<lc_half2> { using type = lc_half; };
template<> struct element_type_<lc_half3> { using type = lc_half; };
template<> struct element_type_<lc_half4> { using type = lc_half; };
template<> struct element_type_<lc_short2> { using type = lc_short; };
template<> struct element_type_<lc_short3> { using type = lc_short; };
template<> struct element_type_<lc_short4> { using type = lc_short; };
template<> struct element_type_<lc_ushort2> { using type = lc_ushort; };
template<> struct element_type_<lc_ushort3> { using type = lc_ushort; };
template<> struct element_type_<lc_ushort4> { using type = lc_ushort; };
template<> struct element_type_<lc_byte2> { using type = lc_byte; };
template<> struct element_type_<lc_byte3> { using type = lc_byte; };
template<> struct element_type_<lc_byte4> { using type = lc_byte; };
template<> struct element_type_<lc_ubyte2> { using type = lc_ubyte; };
template<> struct element_type_<lc_ubyte3> { using type = lc_ubyte; };
template<> struct element_type_<lc_ubyte4> { using type = lc_ubyte; };
template<> struct element_type_<lc_int2> { using type = lc_int; };
template<> struct element_type_<lc_int3> { using type = lc_int; };
template<> struct element_type_<lc_int4> { using type = lc_int; };
template<> struct element_type_<lc_uint2> { using type = lc_uint; };
template<> struct element_type_<lc_uint3> { using type = lc_uint; };
template<> struct element_type_<lc_uint4> { using type = lc_uint; };
template<> struct element_type_<lc_long2> { using type = lc_long; };
template<> struct element_type_<lc_long3> { using type = lc_long; };
template<> struct element_type_<lc_long4> { using type = lc_long; };
template<> struct element_type_<lc_ulong2> { using type = lc_ulong; };
template<> struct element_type_<lc_ulong3> { using type = lc_ulong; };
template<> struct element_type_<lc_ulong4> { using type = lc_ulong; };

template<class T>
struct __builtin__Buffer {
    T *data{};
    size_t size{};
    __device__ T &operator[](size_t i) noexcept { return data[i]; }
    __device__ T &operator[](size_t i) const noexcept { return data[i]; }
};

