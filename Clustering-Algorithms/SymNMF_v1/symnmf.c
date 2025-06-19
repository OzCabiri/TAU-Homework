#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#define MAX_LINE_LENGTH 1024  /* Define max line length for buffer */

static int N_c, vecdim_c;

/* 
prints a matrix of doubles with dimensions n*m
@param matrix: the matrix to be printed
@param n: the number of rows
@param m: the number of columns
@return void
*/
void print_matrix(double** matrix, int n, int m)
{
    int i,j;
    for(i=0;i<n;i++)
    {
        for(j=0;j<m;j++)
        {
            printf("%.4f ", matrix[i][j]);
            if(j != m-1)
            {
                printf(",");
            }
        }
        printf("\n");
    }
}   

/*
frees a matrix of doubles with dimensions n*m
@param p: the matrix to be freed
@param n: the number of rows
@return void
*/
void matrix_free(double** p, int n)
{
    int i;
    for(i=0;i<n;i++)
    {
        free(p[i]);
    }
    free(p); 
}

/*
allocates memory for a matrix of doubles with dimensions n*m
@param new_matrix: the matrix to be allocated
@param n: the number of rows
@param m: the number of columns
@return double**: the allocated matrix
*/
double** matrix_malloc(double** new_matrix, int n, int m)
{
    int i;
    if((new_matrix = malloc(n*sizeof(double*))) == NULL)
    {
        printf("An Error Has Occured");
        free(new_matrix);
        return NULL;
    }
    for(i=0;i<n;i++)
    {
        if ((new_matrix[i] = malloc(m * sizeof(double))) == NULL)
        {
            printf("An Error Has Occured");
            matrix_free(new_matrix, n);
            return NULL;
        }
    }
    return new_matrix;
}

/*
multiplies two matrices of doubles
@param matrix1: the first matrix
@param matrix2: the second matrix
@param n: the number of rows of the first matrix
@param m: the number of columns of the first matrix and the number of rows of the second matrix
@param p: the number of columns of the second matrix
@return double**: the result matrix
*/
double** matrix_multiplication(double** matrix1, double** matrix2, int n, int m, int p)
{
    int i,j,k;
    double sum;
    double** result_matrix = NULL;
    
    if((result_matrix = matrix_malloc(result_matrix, n, p)) == NULL) return NULL; /* Memory allocation failed */

    for(i=0;i<n;i++)
    {
        for(j=0;j<p;j++)
        {
            sum = 0;
            for(k=0;k<m;k++)
            {
                sum += matrix1[i][k] * matrix2[k][j];
            }
            result_matrix[i][j] = sum;
        }
    }
    return result_matrix;
}

/*
transposes a matrix of doubles
@param matrix: the matrix to be transposed
@param n: the number of rows
@param m: the number of columns
@return double**: the transposed matrix
*/
double** matrix_transpose(double** matrix, int n, int m)
{
    int i,j;
    double** transposed_matrix = NULL;
    
    if((transposed_matrix = matrix_malloc(transposed_matrix, m, n)) == NULL) return NULL; /* Memory allocation failed */

    for(i=0;i<n;i++)
    {
        for(j=0;j<m;j++)
        {
            transposed_matrix[j][i] = matrix[i][j];
        }
    }

    return transposed_matrix;
}

/*
substracts two matrices of doubles
@param matrix1: the first matrix
@param matrix2: the second matrix
@param n: the number of rows
@param m: the number of columns
@return double**: the result matrix
*/
double** matrix_substraction(double** matrix1, double** matrix2, int n, int m)
{
    int i,j;
    double** result_matrix = NULL;
    
    if((result_matrix = matrix_malloc(result_matrix, n, m)) == NULL) return NULL; /* Memory allocation failed */

    for(i=0;i<n;i++)
    {
        for(j=0;j<m;j++)
        {
            result_matrix[i][j] = matrix1[i][j] - matrix2[i][j];
        }
    }

    return result_matrix;
}

/*
performs the update step of the symnmf algorithm by using the recursive formula
@param new_H: the new H matrix
@param H: the old H matrix
@param nom_matrix: the numerator matrix
@param denom_matrix: the denominator matrix
@param N: the number of rows
@param k: the number of columns
@return void
*/
void update_new_H(double** new_H, double** H, double** nom_matrix, double** denom_matrix, int N, int k)
{
    int i,j;
    double beta = 0.5;
    for(i=0;i<N;i++)
        {
            for(j=0;j<k;j++)
            {
                new_H[i][j] = H[i][j] * (1 - beta + beta*(nom_matrix[i][j] / denom_matrix[i][j]));
            }
        }
}

/*
swiches the old H matrix with the new H matrix
@param H: the old H matrix
@param new_H: the new H matrix
@param N: the number of rows
@param k: the number of columns
@return void
*/
void advance_H(double** H, double** new_H, int N, int k)
{
    int i,j;
    for(i=0;i<N;i++)
    {
        for(j=0;j<k;j++)
        {
            H[i][j] = new_H[i][j];
        }
    }
}

/*
calculates the forbius norm of a matrix of doubles
@param matrix: the matrix
@param n: the number of rows
@param m: the number of columns
@param is_squared: a flag to determine if the squared norm should be returned
@return double: the forbius norm
*/
double forbius_norm(double** matrix, int n, int m, int is_squared)
{
    int i,j;
    double sum = 0;
    for(i=0;i<n;i++)
    {
        for(j=0;j<m;j++)
        {
            sum += pow(matrix[i][j], 2);
        }
    }
    return (is_squared == 0) ? sqrt(sum) : sum;
}

/*
checks the convergence of two matrices of doubles by calculating the forbius norm of their difference
@param matrix1: the first matrix
@param matrix2: the second matrix
@param n: the number of rows
@param m: the number of columns
@return double: the forbius norm of the difference
*/
double matrix_convergence(double** matrix1, double** matrix2, int n, int m)
{
    double** result_matrix = matrix_substraction(matrix1, matrix2, n, m);
    double norm = forbius_norm(result_matrix, n, m, 1);
    matrix_free(result_matrix, n);
    
    return norm;
}

/*
calculates the euclidean distance between two vectors of doubles
@param vec1: the first vector
@param vec2: the second vector
@param vecdim: the number of dimensions
@param is_squared: a flag to determine if the squared distance should be returned
@return double: the euclidean distance
*/
double euclidean_distance(double* vec1, double* vec2, int vecdim, int is_squared)
{
    int i;
    double sum = 0;
    for (i=0;i<vecdim;i++)
    {
        sum += pow(vec1[i] - vec2[i], 2);
    }
    return (is_squared==0) ? sqrt(sum) : sum;
}

/*
calculates the symilarity matrix of a matrix of doubles
@param vectors: the matrix of vectors
@param N: the number of rows
@param vecdim: the number of dimensions
@return double**: the symilarity matrix
*/
double** sym(double** vectors, int N, int vecdim)
{
    int i,j;
    double value;
    double** sym_matrix = NULL;

    /* malloc a matrix of doubles sized N*N */
    if((sym_matrix = matrix_malloc(sym_matrix, N, N)) == NULL) return NULL; /* Memory allocation failed */

    /* calculate the symilarity matrix */
    for(i=0;i<N;i++)
    {
        for(j=i;j<N;j++)
        {
            if (i==j)
            {
                sym_matrix[i][j] = 0;
            }
            else
            {
                value = euclidean_distance(vectors[i], vectors[j], vecdim, 1);
                value = exp(-value/2);

                sym_matrix[i][j] = value;
                sym_matrix[j][i] = value;
            }
        }
    }

    return sym_matrix;
}

/*
calculates the ddg matrix of a matrix of doubles
@param vectors: the matrix of vectors
@param N: the number of rows
@param vecdim: the number of dimensions
@return double**: the ddg matrix
*/
double** ddg(double** vectors, int N, int vecdim)
{
    int i,j;
    double sum;
    double** sym_matrix = NULL;
    double** ddg_matrix = NULL;

    /* calculate sym and malloc a matrix of doubles sized N*n */
    if((sym_matrix = sym(vectors, N, vecdim)) == NULL) return NULL;  /* Memory allocation failed */

    if ((ddg_matrix = matrix_malloc(ddg_matrix, N, N)) == NULL) /* Memory allocation failed */
    {
        matrix_free(sym_matrix, N);
        return NULL;
    }
    

    /* initialize the ddg matrix */
    for(i=0;i<N;i++)
    {
        for(j=0;j<N;j++)
        {
            ddg_matrix[i][j] = 0;
        }
    }
    /* calculate the ddg matrix */
    for(i=0;i<N;i++)
    {
        sum = 0;
        for(j=0;j<N;j++)
        {
            sum += sym_matrix[i][j];
        }
        ddg_matrix[i][i] = sum;
    }

    matrix_free(sym_matrix, N);
    return ddg_matrix;
}

/*
calculates the norm matrix of a matrix of doubles
@param vectors: the matrix of vectors
@param N: the number of rows
@param vecdim: the number of dimensions
@return double**: the norm matrix
*/
double** norm(double** vectors, int N, int vecdim)
{
    int i,j;
    double** sym_matrix = NULL;
    double** ddg_matrix = NULL;
    double** norm_matrix = NULL;

    /* malloc a matrix of doubles sized N on vecdim */
    if((sym_matrix = sym(vectors, N, vecdim)) == NULL) return NULL; /* Memory allocation failed */

    if((ddg_matrix = ddg(vectors, N, vecdim)) == NULL) /* Memory allocation failed */
    {
        matrix_free(sym_matrix, N);
        return NULL;
    }

    if ((norm_matrix = matrix_malloc(norm_matrix, N, N)) == NULL) /* Memory allocation failed */
    {
        matrix_free(sym_matrix, N);
        matrix_free(ddg_matrix, N);
        return NULL;
    }

    /* calculate the norm matrix */
    for(i=0;i<N;i++)
    {
        for(j=0;j<N;j++)
        {
            norm_matrix[i][j] = sym_matrix[i][j] / sqrt(ddg_matrix[i][i] * ddg_matrix[j][j]);
        }
    }

    matrix_free(sym_matrix, N);
    matrix_free(ddg_matrix, N);
    return norm_matrix;
}

/*
calculates the symnmf matrix of a matrix of doubles using norm and H matrices
check the convergence of the H matrix and updates it until convergence is reached for epsilon = 0.0001
or until 300 iterations are reached
@param W: the norm matrix
@param H: the H matrix
@param N: the number of rows
@param k: the number of columns
@return double**: the symnmf matrix
*/
double** symnmf(double** W, double** H, int N, int k)
{
    int i;
    double** new_H = NULL;
    int iter = 300;
    double eps = 0.0001;
    new_H = matrix_malloc(new_H, N, k);
    if(new_H == NULL) return NULL; /* Memory allocation failed */

    for(i=0;i<iter;i++)
    {
        /* calculate the numerator and denominator matrices */
        double** nom_matrix;
        double** transposed_matrix;
        double** denom_matrix;
        double** helper_matrix;

        if((nom_matrix = matrix_multiplication(W, H, N, N, k)) == NULL) return NULL;/* Memory allocation failed */

        if((transposed_matrix = matrix_transpose(H, N, k)) == NULL) /* Memory allocation failed */
        {
            matrix_free(nom_matrix, N);
            return NULL;
        }

        helper_matrix = matrix_multiplication(H, transposed_matrix, N, k, N);
        matrix_free(transposed_matrix, k);
        if(helper_matrix == NULL) /* Memory allocation failed */
        {
            matrix_free(nom_matrix, N);
            return NULL;
        }

        denom_matrix = matrix_multiplication(helper_matrix, H, N, N, k);
        matrix_free(helper_matrix, N);
        if(denom_matrix == NULL) /* Memory allocation failed */
        {
            matrix_free(nom_matrix, N);
            return NULL;
        }

        /* update the new_H matrix */
        update_new_H(new_H, H, nom_matrix, denom_matrix, N, k);

        /* free allocated memory for next iteration */
        matrix_free(nom_matrix, N);
        matrix_free(denom_matrix, N);

        if(matrix_convergence(new_H, H, N, k) < eps)
        {
            return new_H;
        }
        else
        {
            advance_H(H, new_H, N, k);
        }
    }
    return new_H;
}

/*
function to duplicate a string
@param src: the string to be duplicated
@return char*: the duplicated string
 */
char* duplicateString(char* src)
{
    char* str;
    char* p;
    int len = 0;

    if(src == NULL)
    {
        printf("An error has occured");
        return NULL;
    }
    
    while (src[len])
        len++;
    str = malloc(len + 1);
    p = str;
    while (*src)
        *p++ = *src++;
    *p = '\0';
    return str;
}

/*
read vectors from a file and store them in a matrix of doubles
@param filename: the name of the file
@return double**: the matrix of vectors
*/
double** read_vectors_from_file(const char *filename)
{
    char line[MAX_LINE_LENGTH];
    char* token;
    int i,j;
    int row_count = 0;
    int col_count = 0;
    double** matrix = NULL;

    FILE *file = fopen(filename, "r");
    if (file == NULL) {
        perror("Error opening file");
        return NULL;
    }

    /* First pass to determine the number of rows and columns */
    while (fgets(line, sizeof(line), file)) {
        row_count++;

        /* Count columns in the first row */
        if (row_count == 1) {
            char* temp = duplicateString(line);  /* Duplicate line for counting columns */
            char* token = strtok(temp, ",");
            while (token != NULL) {
                col_count++;
                token = strtok(NULL, ",");
            }
            free(temp);
        }
    }
    N_c = row_count;
    vecdim_c = col_count;

    /* Allocate memory for the 2D matrix */
    matrix = matrix_malloc(matrix, N_c, vecdim_c);

    /* Reset file pointer to beginning and read values into matrix */
    rewind(file);
    i = 0;
    while (fgets(line, sizeof(line), file)) {
        j = 0;
        token = strtok(line, ",");
        while (token != NULL) {
            matrix[i][j++] = atof(token);  /* Convert token to double and store in matrix */
            token = strtok(NULL, ",");
        }
        i++;
    }

    fclose(file);
   
    return matrix;
}

int main(int argc, char* argv[])
{
    double** vectors;
    double** goal_matrix = NULL;

    char* goal = duplicateString(argv[1]);
    char* filename = duplicateString(argv[2]);

    (void)argc;

    vectors = read_vectors_from_file(filename);
    if(vectors == NULL) 
    {
        free(goal);
        free(filename);
        return 1;
    }
    
    if(!strcmp(goal,"sym"))
    {
        goal_matrix = sym(vectors, N_c, vecdim_c);
    }
    else if(!strcmp(goal,"ddg"))
    {
        goal_matrix = ddg(vectors, N_c, vecdim_c);
    }
    else if(!strcmp(goal,"norm"))
    {
        goal_matrix = norm(vectors, N_c, vecdim_c);
    }
    print_matrix(goal_matrix, N_c, N_c);
    matrix_free(goal_matrix, N_c);
    matrix_free(vectors, N_c);
    free(goal);
    free(filename);
    
    return 0;
}

