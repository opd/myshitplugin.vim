from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize

setup(
    # ext_modules = cythonize("matcher.pyx")
    ext_modules = cythonize([Extension("cmatch", ["cmatch.pyx"])])
)
# python setup.py build_ext -i

# python -c 'import cmatch; Q = cmatch.main()'
