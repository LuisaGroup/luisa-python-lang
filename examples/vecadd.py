# import luisa_lang
# from luisa_lang import Buffer, dispatch_id
# from dataclasses import dataclass


# @luisa_lang.kernel
# def vecadd(a: Buffer[float], b: Buffer[float], c: Buffer[float]):
#     tid = dispatch_id().x
#     c[tid] = a[tid] + b[tid]
