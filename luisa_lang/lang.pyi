# for compiler internal use only
def lcpyc(*args, **kwargs):...

@lcpyc("bultin_type")
class u16(int):
    pass

@lcpyc("bultin_type")
class u32(int):
    pass

@lcpyc("bultin_type")
class u64(int):
    pass

@lcpyc("bultin_type")
class i16(int):
    pass

@lcpyc("bultin_type")
class i32(int):
    pass

@lcpyc("bultin_type")
class i64(int):
    pass

@lcpyc("bultin_type")
class f32(float):
    pass