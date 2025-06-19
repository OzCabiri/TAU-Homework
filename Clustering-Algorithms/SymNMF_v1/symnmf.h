/* C header file */
#ifndef SYMNMF_H
#define SYMNMF_H

void matrix_free(double **p, int n);
double** matrix_malloc(double** new_matrix, int n, int m);
double** sym(double** vectors, int N, int vecdim);
double** ddg(double** vectors, int N, int vecdim);
double** norm(double** vectors, int N, int vecdim);
double** symnmf(double** W, double** H, int N, int k);

#endif