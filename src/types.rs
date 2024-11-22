#[cfg(feature = "glam")]
use glam::{Mat2, Mat3, Mat4};

pub type Byte = i8;
pub type Ubyte = u8;
pub type Short = i16;
pub type Ushort = u16;
pub type Int = i32;
pub type Uint = u32;
pub type Long = i64;
pub type Ulong = u64;
pub type Float = f32;
pub type Double = f64;

macro_rules! define_vector {
    ($name:ident, $scalar:ty, $glam_name:ty, $align:literal, $($comps:ident),+) => {
        #[repr(C, align($align))]
        pub struct $name {
            $(pub $comps: $scalar),+
        }
        impl $name {
            pub fn new($($comps: $scalar),+) -> Self {
                Self {
                    $($comps),+
                }
            }
        }
        #[cfg(feature = "glam")]
        impl From<$name> for $glam_name {
            fn from(v: $name) -> Self {
                Self::new($(v.$comps),+)
            }
        }
        #[cfg(feature = "glam")]
        impl From<$glam_name> for $name {
            fn from(v: $glam_name) -> Self {
                Self::new($(v.$comps as $scalar),+)
            }
        }
    };
    ($name:ident, $scalar:ty, $align:literal, $($comps:ident),+) => {
        #[repr(C, align($align))]
        pub struct $name {
            $(pub $comps: $scalar),+
        }
        impl $name {
            pub fn new($($comps: $scalar),+) -> Self {
                Self {
                    $($comps),+
                }
            }
        }
    }
}
define_vector!(Byte2, Byte, glam::I8Vec2, 2, x, y);
define_vector!(Byte3, Byte, glam::I8Vec3, 4, x, y, z);
define_vector!(Byte4, Byte, glam::I8Vec4, 4, x, y, z, w);

define_vector!(Ubyte2, Ubyte, glam::U8Vec2, 2, x, y);
define_vector!(Ubyte3, Ubyte, glam::U8Vec3, 4, x, y, z);
define_vector!(Ubyte4, Ubyte, glam::U8Vec4, 4, x, y, z, w);

define_vector!(Short2, Short, glam::I16Vec2, 4, x, y);
define_vector!(Short3, Short, glam::I16Vec3, 8, x, y, z);
define_vector!(Short4, Short, glam::I16Vec4, 8, x, y, z, w);

define_vector!(Ushort2, Ushort, glam::U16Vec2, 4, x, y);
define_vector!(Ushort3, Ushort, glam::U16Vec3, 8, x, y, z);
define_vector!(Ushort4, Ushort, glam::U16Vec4, 8, x, y, z, w);

define_vector!(Int2, Int, glam::IVec2, 8, x, y);
define_vector!(Int3, Int, glam::IVec3, 16, x, y, z);
define_vector!(Int4, Int, glam::IVec4, 16, x, y, z, w);

define_vector!(Uint2, Uint, glam::UVec2, 8, x, y);
define_vector!(Uint3, Uint, glam::UVec3, 16, x, y, z);
define_vector!(Uint4, Uint, glam::UVec4, 16, x, y, z, w);

define_vector!(Float2, Float, glam::Vec2, 8, x, y);
define_vector!(Float3, Float, glam::Vec3, 16, x, y, z);
define_vector!(Float4, Float, glam::Vec4, 16, x, y, z, w);

define_vector!(Double2, Double, glam::DVec2, 16, x, y);
define_vector!(Double3, Double, glam::DVec3, 32, x, y, z);
define_vector!(Double4, Double, glam::DVec4, 32, x, y, z, w);

define_vector!(Float2x2, Float2, 8, x, y);
define_vector!(Float3x3, Float3, 16, x, y, z);
define_vector!(Float4x4, Float4, 16, x, y, z, w);

define_vector!(Double2x2, Double2, 16, x, y);
define_vector!(Double3x3, Double3, 32, x, y, z);
define_vector!(Double4x4, Double4, 32, x, y, z, w);

#[cfg(feature = "glam")]
mod _convert {
    use super::*;
    impl From<Mat2> for Float2x2 {
        fn from(m: Mat2) -> Self {
            Self::new(
                Float2::new(m.x_axis.x, m.x_axis.y),
                Float2::new(m.y_axis.x, m.y_axis.y),
            )
        }
    }
    impl From<Float2x2> for Mat2 {
        fn from(m: Float2x2) -> Self {
            Mat2::from_cols(m.x.into(), m.y.into())
        }
    }
    impl From<Mat3> for Float3x3 {
        fn from(m: Mat3) -> Self {
            Self::new(
                Float3::new(m.x_axis.x, m.x_axis.y, m.x_axis.z),
                Float3::new(m.y_axis.x, m.y_axis.y, m.y_axis.z),
                Float3::new(m.z_axis.x, m.z_axis.y, m.z_axis.z),
            )
        }
    }
    impl From<Float3x3> for Mat3 {
        fn from(m: Float3x3) -> Self {
            Mat3::from_cols(m.x.into(), m.y.into(), m.z.into())
        }
    }
    impl From<Mat4> for Float4x4 {
        fn from(m: Mat4) -> Self {
            Self::new(
                Float4::new(m.x_axis.x, m.x_axis.y, m.x_axis.z, m.x_axis.w),
                Float4::new(m.y_axis.x, m.y_axis.y, m.y_axis.z, m.y_axis.w),
                Float4::new(m.z_axis.x, m.z_axis.y, m.z_axis.z, m.z_axis.w),
                Float4::new(m.w_axis.x, m.w_axis.y, m.w_axis.z, m.w_axis.w),
            )
        }
    }
    impl From<Float4x4> for Mat4 {
        fn from(m: Float4x4) -> Self {
            Mat4::from_cols(m.x.into(), m.y.into(), m.z.into(), m.w.into())
        }
    }
    impl From<glam::DMat2> for Double2x2 {
        fn from(m: glam::DMat2) -> Self {
            Self::new(
                Double2::new(m.x_axis.x, m.x_axis.y),
                Double2::new(m.y_axis.x, m.y_axis.y),
            )
        }
    }
    impl From<Double2x2> for glam::DMat2 {
        fn from(m: Double2x2) -> Self {
            glam::DMat2::from_cols(m.x.into(), m.y.into())
        }
    }
    impl From<glam::DMat3> for Double3x3 {
        fn from(m: glam::DMat3) -> Self {
            Self::new(
                Double3::new(m.x_axis.x, m.x_axis.y, m.x_axis.z),
                Double3::new(m.y_axis.x, m.y_axis.y, m.y_axis.z),
                Double3::new(m.z_axis.x, m.z_axis.y, m.z_axis.z),
            )
        }
    }
    impl From<Double3x3> for glam::DMat3 {
        fn from(m: Double3x3) -> Self {
            glam::DMat3::from_cols(m.x.into(), m.y.into(), m.z.into())
        }
    }
    impl From<glam::DMat4> for Double4x4 {
        fn from(m: glam::DMat4) -> Self {
            Self::new(
                Double4::new(m.x_axis.x, m.x_axis.y, m.x_axis.z, m.x_axis.w),
                Double4::new(m.y_axis.x, m.y_axis.y, m.y_axis.z, m.y_axis.w),
                Double4::new(m.z_axis.x, m.z_axis.y, m.z_axis.z, m.z_axis.w),
                Double4::new(m.w_axis.x, m.w_axis.y, m.w_axis.z, m.w_axis.w),
            )
        }
    }
    impl From<Double4x4> for glam::DMat4 {
        fn from(m: Double4x4) -> Self {
            glam::DMat4::from_cols(m.x.into(), m.y.into(), m.z.into(), m.w.into())
        }
    }
}
