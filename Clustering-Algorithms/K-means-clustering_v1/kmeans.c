#include <stdio.h>
#include <stdlib.h>
#include <math.h>

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

int check_convergence(double **centroids, double **clusters, int k, int vecdim)
{
    int i;
    int flag = 1;
    for (i=0;i<k;i++)
    {
        if (!(euclidean_distance(centroids[i], clusters[i], vecdim) < 0.0001))
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

int main(int argc, char* argv[])
{
    int i,j;
    double entry;
    /* init k, and check if iter was given */
    int k = atoi(argv[1]);
    int iter;
    /* N is the number of vectors */
    int N = 0;
    /* ch will be our temporary character
    vec dim will define the number of entries in each vector */
    char ch;
    int vecdim = 0;
    /* allocate memory for curr_dbl */
    size_t curr_dbl_size = 10; 
    char *curr_dbl = malloc(curr_dbl_size * sizeof(char));
    size_t curr_dbl_index = 0;
    /* first vector will be a dynamic array of doubles */
    double *first_vec = (double*)malloc(sizeof(double));
    /* Define vec_arr, clusters, centroids and cluster_sizes */
    double **vec_arr, **clusters, **centroids;
    int *cluster_sizes;
    /* make sure memory was allocated for curr_dbl and first_vec */
    if (first_vec == NULL)
    {
        printf("An Error Has Occured");
        free(curr_dbl);
        free(first_vec);   
        return 1;
    }
    if (curr_dbl == NULL)
    {
        printf("An Error Has Occured");
        free(curr_dbl);
        free(first_vec);
        return 1;
    }

    /* determine if iter was given and give default value 200 if not */
    if(!isNaturalNumber(argv[1]))
    {
        printf("Invalid number of clusters!\n");
        return 1;
    }
    if (argc == 3)
    {
        iter = atoi(argv[2]);
        if(!isNaturalNumber(argv[2]))
        {
            printf("Invalid number of iteration!\n");
            return 1;
        }
    }
    else
    {
        iter = 200; /* default value for iter if not given */
    }
    
    ch = getchar(); /* get the first character */
    
    /* iterating over the first vector to find its dimension */
    while (ch != '\n')
    {
        if (ch == ',')
        {
            curr_dbl[curr_dbl_index] = '\0'; /* terminate our string */

            /* cast our entry into a double */
            entry = atof(curr_dbl);
            
            /* we need to reallocate memory for one more double in our first vector */
            first_vec = realloc(first_vec, (vecdim+1) * sizeof(double));
            if (first_vec == NULL)
            {
                printf("Failed to reallocate memory");
                free(curr_dbl);
                free(first_vec);
                return 1;
            }

            /* add the current double to our first vector */
            first_vec[vecdim] = entry;
            
            vecdim++; /* increment the number of entries in the vector */
            curr_dbl_index = 0; /* reset the index */
        }
        else /* we need to append chars to curr_dbl */
        {
            /* we need to reallocate memory */
            if (curr_dbl_index+1 >= curr_dbl_size) /* +1 for the null terminator */
            {
                curr_dbl_size *= 2; /* double buffer size */
                curr_dbl = realloc(curr_dbl, curr_dbl_size * sizeof(char)); /* reallocate the memory */

                /* make sure memory was reallocated */
                if (curr_dbl == NULL)
                {
                    printf("Failed to reallocate memory");
                    free(curr_dbl);
                    free(first_vec);
                    return 1;
                }
            }

            /* else, no need to reallocate memory */
            curr_dbl[curr_dbl_index] = ch;
            curr_dbl_index++;
        }
        /* move on to next character */
        ch = getchar();
    }
    
    /* ------ add the last entry to vector --------- */
    curr_dbl[curr_dbl_index] = '\0'; /* terminate our string */

    /* cast our entry into a double */
    entry = atof(curr_dbl);
    
    /* we need to reallocate memory for one more double in our first vector */
    first_vec = realloc(first_vec, (vecdim+1) * sizeof(double));
    if (first_vec == NULL)
    {
        printf("Failed to reallocate memory");
        free(curr_dbl);
        free(first_vec);
        return 1;
    }

    /* add the current double to our first vector */
    first_vec[vecdim] = entry;
    
    vecdim++; /* increment the number of entries in the vector */
    curr_dbl_index = 0; /* reset the index */
    
    /* increment N */
    N++;

    /*-------------done with first vector---------------- */

    /* init vector array of arrays */
    vec_arr = malloc(sizeof(first_vec));
    if (vec_arr == NULL)
    {
        printf("An Error Has Occured");
        matrix_free(vec_arr, N);
        free(curr_dbl);
        free(first_vec);
        return 1;
    }   

    /* Get all other vectors */
    ch = getchar();

    while (ch != EOF) 
    {
        double *curr_vec = malloc(vecdim * sizeof(double));
        if (curr_vec == NULL)
        {
            printf("Failed to reallocate memory");
            matrix_free(vec_arr, N);
            free(curr_dbl);
            free(first_vec);
            free(curr_vec);
            return 1;
        }

        for (i=0;i<vecdim;i++)
        {
            while (ch != ',' && ch != '\n')
            {
                /* we need to reallocate memory */
                if (curr_dbl_index+1 >= curr_dbl_size) /* +1 for the null terminator */
                {
                    curr_dbl_size *= 2; /* double buffer size */
                    curr_dbl = realloc(curr_dbl, curr_dbl_size * sizeof(char)); /* reallocate the memory */

                    /* make sure memory was reallocated */
                    if (curr_dbl == NULL)
                    {
                        printf("Failed to reallocate memory");
                        matrix_free(vec_arr, N);
                        free(curr_dbl);
                        free(first_vec);
                        free(curr_vec);
                        return 1;
                    }
                }
                /* else, no need to reallocate memory */
                curr_dbl[curr_dbl_index] = ch;
                curr_dbl_index++;

                /* move on to next character */
                ch = getchar();
            }

            /*we reached the end of a float */
            curr_dbl[curr_dbl_index] = '\0'; /* terminate our string */

            /* cast our entry into a double */
            entry = atof(curr_dbl);

            /* add the current double to our first vector */
            curr_vec[i] = entry;
            
            curr_dbl_index = 0; /* reset the index */

            ch = getchar(); /* move on to next character */
        }

        /* increment N */
        N++;

        /* reallocate memory for one more vector */
        vec_arr = realloc(vec_arr, N*(sizeof(double*)));
        if (vec_arr == NULL)
        {
            printf("Failed to reallocate memory");
            matrix_free(vec_arr, N);
            free(curr_dbl);
            free(first_vec);
            free(curr_vec);
            return 1;
        }

        /* allocate memory for the new vector */
        vec_arr[N-1] = malloc(vecdim * sizeof(double));
        if (vec_arr[N-1] == NULL)
        {
            printf("An Error Has Occured");
            matrix_free(vec_arr, N);
            free(curr_dbl);
            free(first_vec);
            free(curr_vec);
            return 1;
        }

        /* copy the current vector into the array of vectors */
        for (i=0;i<vecdim;i++)
        {
            vec_arr[N-1][i] = curr_vec[i];
        }
        free(curr_vec); /* free the current vector */
    }

    /* done with curr_dbl - free it*/
    free(curr_dbl);

    /* copy the first vector into the array of vectors */
    vec_arr[0] = first_vec;
    
    /* MATRIX OF VECTORS IS NOW STORED IN vec_arr */
    /* ----------------------------------------------- */

    /* check if k, iter are legal */
    if (!(k > 1 && k < N))
    {
        printf("Invalid number of clusters!\n");
        return 1;
    }

    if (!(iter > 1 && iter < 1000)) {
        printf("Invalid maximum iteration!\n");
        return 1;
    }

    /* create clusters, centroids and cluster_sizes arrays */
    clusters = malloc(k * sizeof(double*));
    if (clusters == NULL)
    {
        printf("An Error Has Occured");
        matrix_free(vec_arr, N);
        matrix_free(clusters, k);
        return 1;
    }

    centroids = malloc(k * sizeof(double*));
    if (centroids == NULL)
    {
        printf("An Error Has Occured");
        matrix_free(vec_arr, N);
        matrix_free(clusters, k);
        matrix_free(centroids, k);
        return 1;
    }
    
    cluster_sizes = malloc(k * sizeof(int));
    if (cluster_sizes == NULL)
    {
        printf("An Error Has Occured");
        matrix_free(vec_arr, N);
        matrix_free(clusters, k);
        matrix_free(centroids, k);
        free(cluster_sizes);
        return 1;
    }

    /* zero out the cluster_sizes array */
    zero_cluster_sizes(cluster_sizes, k);

    /* insert first k vectors from vec_arr into centroids array */
    for (i=0;i<k;i++)
    {
        centroids[i] = malloc(vecdim * sizeof(double));
        if (centroids[i] == NULL)
        {
            printf("An Error Has Occured");
            matrix_free(vec_arr, N);
            matrix_free(clusters, k);
            matrix_free(centroids, k);
            free(cluster_sizes);
            return 1;
        }
        for (j=0;j<vecdim;j++)
        {
            centroids[i][j] = vec_arr[i][j];
        }
    }

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
            return 1;
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
        if (check_convergence(centroids, clusters, k, vecdim))
        {
            break;
        }
        else
        {
            copy_clusters_to_centroids(clusters, centroids, k, vecdim);
            zero_cluster_sizes(cluster_sizes, k);
        }
    }

    print_vec_arr(centroids, k, vecdim);
        
    matrix_free(vec_arr, N);
    matrix_free(clusters, k);
    matrix_free(centroids, k);
    free(cluster_sizes);

    return 0;
}
