# NumPy documentation
# https://numpy.org/doc/stable/index.html
# Version: 1.24

# https://numpy.org/doc/stable/user/absolute_beginners.html

'''
NumPy (Numerical Python) is an open source Python library that’s used in almost every field of science and engineering. 
It’s the universal standard for working with numerical data in Python, and it’s at the core of the scientific Python and 
PyData ecosystems. NumPy users include everyone from beginning coders to experienced researchers doing state-of-the-art 
scientific and industrial research and development. The NumPy API is used extensively in Pandas, SciPy, Matplotlib, 
scikit-learn, scikit-image and most other data science and scientific Python packages.

The NumPy library contains multidimensional array and matrix data structures (you’ll find more information about this 
in later sections). It provides ndarray, a homogeneous n-dimensional array object, with methods to efficiently operate on it. 
NumPy can be used to perform a wide variety of mathematical operations on arrays. It adds powerful data structures to 
Python that guarantee efficient calculations with arrays and matrices and it supplies an enormous library of high-level 
mathematical functions that operate on these arrays and matrices.
'''
# https://numpy.org/install/
# https://www.youtube.com/watch?v=q6dnyS-Ailo

# https://numpy.org/install/#reproducible-installs
# https://docs.python.org/3/tutorial/venv.html
# https://pip.pypa.io/en/latest/user_guide/#requirements-files
# https://dev.to/bowmanjd/python-tools-for-managing-virtual-environments-3bko#howto

import numpy as np

new_matrix = np.array([1, 2, 3, 4, 5, 6])
print(new_matrix)