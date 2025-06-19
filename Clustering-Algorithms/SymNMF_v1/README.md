<a id="readme-top"></a>

<br/>
<div align="center">
<h3 align="center"><a href="https://github.com/OzCabiri/SymNMF_v1">SymNMF</a></h3>
  <p align="center">
    Implementation of a clustering algorithm based on symmetric non-negative matrix factorization in Python and C.
  </p>
</div>


<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About</a>
    </li>
    <li>
      <a href="#preperations">Preperations</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#collaborators">Collaborators</a></li>
  </ol>
</details>


## About The Project
This is an implementation of a clustering algorithm based on symmetric non-negative matrix factorization.
It also includes code to compare its silhouette score aginst the KMeans algorithm (first K vectors are chosen as centroids deterministically) score.

Cousr: Software Project
<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Preperations

### Prerequisites

* It is assumed you have Python and a C compiler already set up on your machine.

* NumPy and Pandas

* scikit-learn

* make (for makefile)


### Installation
In order to run this project you will need to compile it on your machine.

1. Clone the repo
   ```sh
   git clone https://github.com/OzCabiri/SymNMF_v1.git
   ```
2. Build symnmf executable
   ```sh
   make -f ./Makefile
   ```
3. Build the extension
   ```sh
   python setup.py build_ext --inplace
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>


## Usage

Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.

### Using the Python interface:
The Python interface recieves 3 arguemtns: _k_, _goal_ and an _input file_.
* _k_ is the number of clusters
* _goal_ determines the function to produce
* _input file_ is a .txt file in a CSV format representing vectors

Ensure that _k_ is less than the number of vectors in your input file and that the vectors in _input file_ are of the same dimension.<br/>
_goal_ can be one of the following:
* _sym_: Prints the vectors' similarity matrix
* _ddg_: Prints the vectors' diagonal degree matrix
* _norm_: Prints the vectors' normalized similarity matrix
* _symnmf_: Derives a clustering solution and prints a matrix that can be viewd as an association matrix

Examples:
```sh
python symnmf.py 5 sym tests/input_1.txt
```
```sh
python symnmf.py 7 symnmf tests/input_3.txt
```
### Using the C interface:
The C interface recieves 2 arguemtns: _goal_ and an _input file_.
* _goal_ determines the function to produce
* _input file_ is a .txt file in a CSV format representing vectors

Ensure that _k_ is less than the number of vectors in your input file and that the vectors in _input file_ are of the same dimension.<br/>
_goal_ can be one of the following:
* _sym_: Prints the vectors' similarity matrix
* _ddg_: Prints the vectors' diagonal degree matrix
* _norm_: Prints the vectors' normalized similarity matrix

Examples:
```sh
./symnmf ddg tests/input_1.txt
```
```sh
./symnmf norm tests/input_2.txt
```

### Comparing silhouette scores of SymNMF and KMeans
The comparison is done with python and recieves 2 arguemtns: _k_ and an _input file_.
* _k_ is the number of clusters
* _input file_ is a .txt file in a CSV format representing vectors

Ensure that _k_ is less than the number of vectors in your input file and that the vectors in _input file_ are of the same dimension.<br/>

Example:
```sh
python analysis.py 5 tests/input_1.txt
```

_For more examples, please refer to the [Documentation](https://github.com/OzCabiri/SymNMF_v1/blob/main/tests/test_readme.txt)_

<p align="right">(<a href="#readme-top">back to top</a>)</p>


## Collaborators

This project was written by [Oz Cabiri](https://github.com/OzCabiri) and [Assaf Yaron](https://github.com/assafyaron).<br/>
We are students so we are open to any criticism you might have so we can improve.

You can also contact us on LinkedIn: [Oz Cabiri](https://linkedin.com/in/oz-cabiri), [Assaf Yaron](https://www.linkedin.com/in/assafyaron/)

<p align="right">(<a href="#readme-top">back to top</a>)</p>