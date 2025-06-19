# define PY_SSIZE_T_CLEAN
# include <Python.h>
# include <stdio.h>
# include <math.h>
# include "symnmf.h"

static int N, vecdim, k;

/**
 * Convert a Python list of lists to a C array.
 *
 * This function takes a Python list of lists (obj) and converts it into a C array (arr).
 * The dimensions of the array are specified by n (number of rows) and m (number of columns).
 * Each element in the Python list is converted to a double and stored in the corresponding
 * position in the C array.
 *
 * @param obj A PyObject representing a Python list of lists.
 * @param arr A double pointer representing the C array to be filled.
 * @param n An integer representing the number of rows in the array.
 * @param m An integer representing the number of columns in the array.
 * @return A double pointer representing the filled C array.
 */
double** convert_pylist2carray(PyObject* obj, double** arr, int n, int m)
{
    int i,j;
    PyObject* row;
    for (i=0;i<n;i++)
    {
        row = PyList_GetItem(obj, i);
        for (j=0;j<m;j++)
        {
            arr[i][j] = PyFloat_AsDouble(PyList_GetItem(row, j));
        }
    }
    return arr;
}

/**
 * Convert a C array to a Python list of lists.
 *
 * This function takes a C array (received_matrix) and converts it into a Python list of lists.
 * The dimensions of the array are specified by n (number of rows) and m (number of columns).
 * Each element in the C array is converted to a Python float and stored in the corresponding
 * position in the Python list.
 *
 * @param received_matrix A double pointer representing the C array to be converted.
 * @param n An integer representing the number of rows in the array.
 * @param m An integer representing the number of columns in the array.
 * @return A PyObject representing the Python list of lists.
 */
PyObject* convert_carray2pylist(double** received_matrix, int n, int m)
{
    int i,j;
    PyObject* final_matrix = PyList_New(n);
    PyObject* final_row;
    for (i=0;i<n;i++)
    {
        final_row = PyList_New(m);
        for (j=0;j<m;j++)
        {
            PyList_SetItem(final_row, j, PyFloat_FromDouble(received_matrix[i][j]));
        }
        PyList_SetItem(final_matrix, i, final_row);
    }

    return final_matrix;
}

/**
 * Convert a Python list of vectors to a C array.
 *
 * This function takes a Python list of vectors (vec_arr_obj) and converts it into a C array (vec_arr).
 * It first parses the Python argument to get the list of vectors, then determines the dimensions
 * of the array (N and vecdim). It allocates memory for the C array and converts the Python list
 * into the C array.
 *
 * @param self A PyObject representing the module or class (not used).
 * @param args A PyObject representing the arguments passed to the function.
 * @return A double pointer representing the C array of vectors, or NULL if an error occurs.
 */
double** convert_vectors(PyObject* self, PyObject* args)
{
    PyObject* vec_arr_obj;
    double** vec_arr = NULL;
    
    /* Parse Python argument: */
    if(!PyArg_ParseTuple(args, "O", &vec_arr_obj)) return NULL; /* In the CPython API, a NULL value is never valid for a
                                                                    PyObject* so it is used to signal that an error has occurred. */

    /* Get N and vecdim from the python object */
    N = PyList_Size(vec_arr_obj);
    vecdim = PyList_Size(PyList_GetItem(vec_arr_obj, 0));

    /* Allocate memory for C array */
    if((vec_arr = matrix_malloc(vec_arr, N, vecdim)) == NULL) return NULL; /* Memory allocation failed */

    /* Convert python list into C array */
    vec_arr = convert_pylist2carray(vec_arr_obj, vec_arr, N, vecdim);
    return vec_arr;
}

/**
 * Perform Symmetric Non-negative Matrix Factorization (SymNMF) on the given vectors.
 *
 * This function takes a Python list of vectors, converts it to a C array, performs SymNMF,
 * and returns the resulting matrix as a Python list of lists. It handles memory allocation
 * and deallocation for the C arrays.
 *
 * @param self A PyObject representing the module or class (not used).
 * @param args A PyObject representing the arguments passed to the function.
 * @return A PyObject representing the resulting matrix as a Python list of lists, or NULL if an error occurs.
 */
static PyObject* symmodule(PyObject* self, PyObject* args)
{
    double** vectors_matrix = convert_vectors(self, args);
    if(vectors_matrix == NULL) return NULL; /* Failure occured */
    
    double** sym_matrix = sym(vectors_matrix, N, vecdim);
    if(sym_matrix == NULL) /* Memory allocation failed */
    {
        matrix_free(vectors_matrix, N);
        return NULL;
    }

    /* Convert our C double** to a python list of lists */
    PyObject* final_sym = convert_carray2pylist(sym_matrix, N, N);

    /* Free all allocated memory */
    matrix_free(vectors_matrix, N);
    matrix_free(sym_matrix, N);

    return Py_BuildValue("O", final_sym);
}

/**
 * Perform Degree Diagonal Matrix (DDG) calculation on the given vectors.
 *
 * This function takes a Python list of vectors, converts it to a C array, performs the DDG calculation,
 * and returns the resulting matrix as a Python list of lists. It handles memory allocation
 * and deallocation for the C arrays.
 *
 * @param self A PyObject representing the module or class (not used).
 * @param args A PyObject representing the arguments passed to the function.
 * @return A PyObject representing the resulting matrix as a Python list of lists, or NULL if an error occurs.
 */
static PyObject* ddgmodule(PyObject* self, PyObject* args)
{
    double** vectors_matrix = convert_vectors(self, args);
    if(vectors_matrix == NULL) return NULL; /* Failure occured */

    double** ddg_matrix = ddg(vectors_matrix, N, vecdim);
    if(ddg_matrix == NULL) /* Memory allocation failed */
    {
        matrix_free(vectors_matrix, N);
        return NULL;
    }

    /* Convert our C double** to a python list of lists */
    PyObject* final_ddg = convert_carray2pylist(ddg_matrix, N, N);

    /* Free all allocated memory */
    matrix_free(vectors_matrix, N);
    matrix_free(ddg_matrix, N);

    return Py_BuildValue("O", final_ddg);
}

/**
 * Perform Normalization on the given vectors.
 *
 * This function takes a Python list of vectors, converts it to a C array, performs normalization,
 * and returns the resulting matrix as a Python list of lists. It handles memory allocation
 * and deallocation for the C arrays.
 *
 * @param self A PyObject representing the module or class (not used).
 * @param args A PyObject representing the arguments passed to the function.
 * @return A PyObject representing the resulting matrix as a Python list of lists, or NULL if an error occurs.
 */
static PyObject* normmodule(PyObject* self, PyObject* args)
{
    double** vectors_matrix = convert_vectors(self, args);
    if(vectors_matrix == NULL) return NULL; /* Failure occured */

    double** norm_matrix = norm(vectors_matrix, N, vecdim);
    if(norm_matrix == NULL) /* Memory allocation failed */
    {
        matrix_free(vectors_matrix, N);
        return NULL;
    }

    /* Convert our C double** to a python list of lists */
    PyObject* final_norm = convert_carray2pylist(norm_matrix, N, N);

    /* Free all allocated memory */
    matrix_free(vectors_matrix, N);
    matrix_free(norm_matrix, N);

    return Py_BuildValue("O", final_norm);
}

/**
 * Perform Symmetric Non-negative Matrix Factorization (SymNMF) on the given vectors.
 *
 * This function takes a Python list of vectors, converts it to a C array, performs SymNMF,
 * and returns the resulting matrix as a Python list of lists. It handles memory allocation
 * and deallocation for the C arrays.
 *
 * @param self A PyObject representing the module or class (not used).
 * @param args A PyObject representing the arguments passed to the function.
 * @return A double pointer representing the resulting matrix as a C array, or NULL if an error occurs.
 */
double** convert_symnmf(PyObject* self, PyObject* args)
{
    PyObject* w_mat_obj;
    PyObject* h_mat_obj;
    double** w_mat = NULL;
    double** h_mat = NULL;
    
    /* Parse Python arguments: */
    if(!PyArg_ParseTuple(args, "OOi", &w_mat_obj, &h_mat_obj, &k)) return NULL; /* In the CPython API, a NULL value is never valid for a
                                                                                                    PyObject* so it is used to signal that an error has occurred. */
    
    /* Get N and vecdim from the python object */
    N = PyList_Size(w_mat_obj);

    /* Allocate memory for C arrays and check if allocation failed */
    if((w_mat = matrix_malloc(w_mat, N, N)) == NULL) return NULL; /* Memory allocation failed */
    if((h_mat = matrix_malloc(h_mat, N, k)) == NULL) /* Memory allocation failed */
    {
        matrix_free(w_mat, N);
        return NULL;
    }

    /* Convert python lists into C arrays */
    w_mat = convert_pylist2carray(w_mat_obj, w_mat, N, N);
    h_mat = convert_pylist2carray(h_mat_obj, h_mat, N, k);

    /* Call the symnmf function */
    double** final_h = symnmf(w_mat, h_mat, N, k);
    if(final_h == NULL) /* Memory allocation failed*/
    {
        matrix_free(w_mat, N);
        matrix_free(h_mat, N);
        return NULL;
    }

    /* Free all allocated memory */
    matrix_free(w_mat, N);
    matrix_free(h_mat, N);

    return final_h;
}

/**
 * Perform Symmetric Non-negative Matrix Factorization (SymNMF) on the given vectors.
 *
 * This function takes a Python list of vectors, converts it to a C array, performs SymNMF,
 * and returns the resulting H matrix as a Python list of lists. It handles memory allocation
 * and deallocation for the C arrays.
 *
 * @param self A PyObject representing the module or class (not used).
 * @param args A PyObject representing the arguments passed to the function.
 * @return A PyObject representing the resulting H matrix as a Python list of lists, or NULL if an error occurs.
 */
static PyObject* symnmfmodule(PyObject* self, PyObject* args)
{    
    double** h_matrix = convert_symnmf(self, args);
    if(h_matrix == NULL) return NULL; /* Failure occured */

    PyObject* final_h = convert_carray2pylist(h_matrix, N, k);

    return Py_BuildValue("O", final_h);;
}

static PyMethodDef symnmfMethods[] = {
    {"sym",                   /* the Python method name that will be used */
      (PyCFunction) symmodule, /* the C-function that implements the Python function and returns static PyObject*  */
      METH_VARARGS,           /* flags indicating parameters accepted for this function */
      PyDoc_STR("Calculates similarity matrix from given vectors")}, /*  The docstring for the function */

    {"ddg",
      (PyCFunction) ddgmodule,
      METH_VARARGS,
      PyDoc_STR("Calculates diagonal degree matrix from given vectors")},
    
    {"norm",
      (PyCFunction) normmodule,
      METH_VARARGS,
      PyDoc_STR("Calculates normalized similarity matrix from given vectors")},

    {"symnmf",
      (PyCFunction) symnmfmodule,
      METH_VARARGS,
      PyDoc_STR("Calculates and updates the association matrix (H) matrix from given vectors until convergence or max iterations")},

    {NULL, NULL, 0, NULL}     /* The last entry must be all NULL as shown to act as a
                                 sentinel. Python looks for this entry to know that all
                                 of the functions for the module have been defined. */
};

static struct PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT,
    "mysymnmfsp", /* name of module */
    NULL, /* module documentation, may be NULL */
    -1,  /* size of per-interpreter state of the module, or -1 if the module keeps state in global variables. */
    symnmfMethods /* the PyMethodDef array from before containing the methods of the extension */
};

PyMODINIT_FUNC PyInit_mysymnmfsp(void)
{
    PyObject *m;
    m = PyModule_Create(&moduledef);
    if (!m) {
        return NULL;
    }
    return m;
}
