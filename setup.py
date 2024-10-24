from setuptools import setup, find_packages

setup(
    name="luisa-python-lang",
    description="A New DSL Frontend for LuisaCompute",
    version="0.1",
    packages=find_packages(),
    package_data={"luisa_lang": ["py.typed"]},
    install_requires=["sourceinspect"],
)
