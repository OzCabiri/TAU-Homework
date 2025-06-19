# define PY_SSIZE_T_CLEAN
# include <Python.h>
# include <stdio.h>
# include <math.h>

void zero_clusters(double **clusters, int k, int vecdim)
{
    int i,j;
    for (i=0;i<k;i++)
    {
        for (j=0;j<vecdim;j++)
        {
            clusters[i][j] = 0;
        }
    }
}

double euclidean_distance(double *vec1, double *vec2, int vecdim)
{
    int i;
    double sum = 0;
    for (i=0;i<vecdim;i++)
    {
        sum += pow(vec1[i] - vec2[i], 2);
    }
    return sqrt(sum);
}

int find_closest_centroid(double *vec, double **centroids, int k, int vecdim)
{
    int i;
    double dist;
    double min_dist = euclidean_distance(vec, centroids[0], vecdim);
    int min_index = 0;
    for (i=1;i<k;i++)
    {
        dist = euclidean_distance(vec, centroids[i], vecdim);
        if (dist < min_dist)
        {
            min_dist = dist;
            min_index = i;
        }
    }
    return min_index;
}

void add_vec_to_cluster(double *vec, double *cluster, int vecdim)
{
    int i;
    for (i=0;i<vecdim;i++)
    {
        cluster[i] += vec[i];
    }
}

void divide_cluster(double *cluster, int vecdim, int k)
{
    int i;
    for (i=0;i<vecdim;i++)
    {
        cluster[i] /= k;
    }
}

void divide_all_clusters(double **clusters, int k, int vecdim, int *cluster_sizes)
{
    int i;
    for (i=0;i<k;i++)
    {
        if (cluster_sizes[i])
        {
            divide_cluster(clusters[i], vecdim, cluster_sizes[i]);
        }
    }
}

int check_convergence(double **centroids, double **clusters, int k, int vecdim, double eps)
{
    int i;
    int flag = 1;
    for (i=0;i<k;i++)
    {
        if (!(euclidean_distance(centroids[i], clusters[i], vecdim) < eps))
        {
            flag = 0;
            break;
        }
    }
    return flag;
}

void copy_clusters_to_centroids(double **clusters, double **centroids, int k, int vecdim)
{
    int i,j;
    for (i=0;i<k;i++)
    {
        for (j=0;j<vecdim;j++)
        {
            centroids[i][j] = clusters[i][j];
        }
    }
    zero_clusters(clusters, k, vecdim);
}

/* print a 2D array of doubles with only 4 digits after the point */
void print_vec_arr(double **vec_arr, int N, int vecdim)
{
    int i,j;
    for (i=0;i<N;i++)
    {
        for (j=0;j<vecdim;j++)
        {
            printf("%.4f", vec_arr[i][j]);
            if (j != vecdim-1)
            {
                printf(",");
            }
        }
        printf("\n");
    }
}

void zero_cluster_sizes(int *cluster_sizes, int k)
{
    int i;
    for (i=0;i<k;i++)
    {
        cluster_sizes[i] = 0;
    }
}

void matrix_free(double **p, int n)
{
    int i;
    for(i=0;i<n;i++)
    {
        free(p[i]);
    }
    free(p); 
}

int isNaturalNumber(char *number)
{
    int i = 0;
    int after_point = 0;
    while(number[i]!='\0')
    {
        if ((number[i] != '0') && after_point)
        {
            return 0;
        }
        if (number[i] == '.')
        {
            after_point = 1;
        }
        i++;
    }
    return 1;
}

double** kmeans(int k, int N, int vecdim, int iter, double eps, double **vec_arr, double **centroids)
{
    int i,j;

    /* Define clusters cluster_sizes */
    double **clusters;
    int *cluster_sizes;
    

    /* create clusters and cluster_sizes arrays */
    clusters = malloc(k * sizeof(double*));
    if (clusters == NULL)
    {
        printf("An Error Has Occured");
        matrix_free(vec_arr, N);
        matrix_free(clusters, k);
        matrix_free(centroids, k);
        return NULL;
    }
    
    cluster_sizes = malloc(k * sizeof(int));
    if (cluster_sizes == NULL)
    {
        printf("An Error Has Occured");
        matrix_free(vec_arr, N);
        matrix_free(clusters, k);
        matrix_free(centroids, k);
        free(cluster_sizes);
        return NULL;
    }

    /* zero out the cluster_sizes array */
    zero_cluster_sizes(cluster_sizes, k);

    /* initialize and zero out the clusters array */
    for (i=0;i<k;i++)
    {
        clusters[i] = malloc(vecdim * sizeof(double));
        if (clusters[i] == NULL)
        {
            printf("An Error Has Occured");
            matrix_free(vec_arr, N);
            matrix_free(clusters, k);
            matrix_free(centroids, k);
            free(cluster_sizes);
            return NULL;
        }
        for (j=0;j<vecdim;j++)
        {
            clusters[i][j] = 0;
        }
    }

    /* start the k-means algorithm */
    for (i=0;i<iter;i++)
    {
        /* iterate over all vectors */
        for (j=0;j<N;j++)
        {

            /* find the closest centroid */
            int closest_centroid = find_closest_centroid(vec_arr[j], centroids, k, vecdim);
            cluster_sizes[closest_centroid]++;

            /* add the vector to the closest cluster */
            add_vec_to_cluster(vec_arr[j], clusters[closest_centroid], vecdim);
        }

        /* divide all clusters by the number of vectors in them */
        divide_all_clusters(clusters, k, vecdim, cluster_sizes);

        /* check for convergence */
        if (check_convergence(centroids, clusters, k, vecdim, eps))
        {
            break;
        }
        else
        {
            copy_clusters_to_centroids(clusters, centroids, k, vecdim);
            zero_cluster_sizes(cluster_sizes, k);
        }
    }
        
    matrix_free(vec_arr, N);
    matrix_free(clusters, k);
    free(cluster_sizes);

    return centroids;
}

static PyObject* k_means(PyObject *self, PyObject *args)
{
    int k, N, vecdim, iter;
    double eps;
    PyObject* vec_arr_obj;
    PyObject* centroids_obj;
    double** vec_arr;
    double** centroids;
    
    /* This parses the Python arguments into:
        1. int (i) variables named k,N,vecdim,iter
        2. double (d) variable named eps
        3. A pointer to a pointer to a double (O) variable named vec_arr
        4. A pointer to a pointer to a double (O) variable named centroids */
    if(!PyArg_ParseTuple(args, "iiiidOO", &k, &N, &vecdim, &iter, &eps, &vec_arr_obj, &centroids_obj))
    {
        return NULL; /* In the CPython API, a NULL value is never valid for a
                        PyObject* so it is used to signal that an error has occurred. */
    }

    // Allocate memory for C arrays and check if allocation failed
    vec_arr = malloc(N*sizeof(double*));
    centroids = malloc(k*sizeof(double*));
    if (vec_arr == NULL || centroids == NULL)
    {
        PyErr_SetString(PyExc_MemoryError, "Memory allocation failed");
        free(vec_arr);
        free(centroids);
        return NULL;
    }
    
    
    int i,j;
    /* Allocate memory for each vector in vec_arr and centroids */
    for (i=0;i<N;i++)
    {
        vec_arr[i] = malloc(vecdim*sizeof(double));
        if (vec_arr[i] == NULL)
        {
            PyErr_SetString(PyExc_MemoryError, "Memory allocation failed");
            for (j=0;j<i;j++)
            {
                free(vec_arr[j]);
            }
            free(vec_arr);
            free(centroids);
            return NULL;
        }
    }
    for (i=0;i<k;i++)
    {
        centroids[i] = malloc(vecdim*sizeof(double));
        if (centroids[i] == NULL)
        {
            PyErr_SetString(PyExc_MemoryError, "Memory allocation failed");
            for (j=0;j<i;j++)
            {
                free(centroids[j]);
            }
            free(centroids);
            for (j=0;j<N;j++)
            {
                free(vec_arr[j]);
            }
            free(vec_arr);
            return NULL;
        }
    }

    /* Convert python lists into C arrays */
    PyObject* vec1;
    PyObject* vec2;
    for (i=0;i<N;i++)
    {
        vec1 = PyList_GetItem(vec_arr_obj, i);
        for (j=0;j<vecdim;j++)
        {
            vec_arr[i][j] = PyFloat_AsDouble(PyList_GetItem(vec1,j));
        }
    }
    for (i=0;i<k;i++)
    {
        vec2 = PyList_GetItem(centroids_obj, i);
        for (j=0;j<vecdim;j++)
        {
            centroids[i][j] = PyFloat_AsDouble(PyList_GetItem(vec2,j));
        }
    }

    /* save kmeans return value */
    double** kmeans_ret = malloc(k*sizeof(double*));
    if (kmeans_ret == NULL)
    {
        PyErr_SetString(PyExc_MemoryError, "Memory allocation failed");
        for (i=0;i<N;i++)
        {
            free(vec_arr[i]);
        }
        free(vec_arr);
        for (i=0;i<k;i++)
        {
            free(centroids[i]);
        }
        free(centroids);
        return NULL;
    }
    kmeans_ret = kmeans(k, N, vecdim, iter, eps, vec_arr, centroids);
    if(kmeans_ret == NULL)
    {
        return NULL;
    }
    
    /* Convert our C double** to a python list of lists*/
    PyObject* final_centroids = PyList_New(k);
    PyObject* final_centroid;
    for (i=0;i<k;i++)
    {
        final_centroid = PyList_New(vecdim);
        for (j=0;j<vecdim;j++)
        {
            PyList_SetItem(final_centroid, j, PyFloat_FromDouble(kmeans_ret[i][j]));
        }
        PyList_SetItem(final_centroids, i, final_centroid);
    }

    /* Free all allocated memory */
    for (i=0;i<k;i++)
    {
        free(centroids[i]);
    }
    free(centroids);

    return Py_BuildValue("O", final_centroids);
}

static PyMethodDef kmeansMethods[] = {
    {"fit",                   /* the Python method name that will be used */
      (PyCFunction) k_means, /* the C-function that implements the Python function and returns static PyObject*  */
      METH_VARARGS,           /* flags indicating parameters accepted for this function */
      PyDoc_STR("kmeans clustering algorithim using kmeans++ as intial centroids")}, /*  The docstring for the function */
    {NULL, NULL, 0, NULL}     /* The last entry must be all NULL as shown to act as a
                                 sentinel. Python looks for this entry to know that all
                                 of the functions for the module have been defined. */
};

static struct PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT,
    "mykmeanssp", /* name of module */
    NULL, /* module documentation, may be NULL */
    -1,  /* size of per-interpreter state of the module, or -1 if the module keeps state in global variables. */
    kmeansMethods /* the PyMethodDef array from before containing the methods of the extension */
};

PyMODINIT_FUNC PyInit_mykmeanssp(void)
{
    PyObject *m;
    m = PyModule_Create(&moduledef);
    if (!m) {
        return NULL;
    }
    return m;
}