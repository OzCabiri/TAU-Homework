   Expected output               C interface command                 Python interface command
similarity_matrix_1        ./symnmf sym tests/input_1.txt      python symnmf.py 5 sym tests/input_1.txt 
diagonal_degree_matrix_1   ./symnmf ddg tests/input_1.txt      python symnmf.py 5 ddg tests/input_1.txt
normalized_matrix_1        ./symnmf norm tests/input_1.txt     python symnmf.py 5 norm tests/input_1.txt
H_matrices_1                                                   python symnmf.py 5 symnmf tests/input_1.txt
analyze_scores_1                                               python analysis.py 5 tests/input_1.txt

similarity_matrix_2        ./symnmf sym tests/input_2.txt      python symnmf.py 4 sym tests/input_2.txt 
diagonal_degree_matrix_2   ./symnmf ddg tests/input_2.txt      python symnmf.py 4 ddg tests/input_2.txt
normalized_matrix_2        ./symnmf norm tests/input_2.txt     python symnmf.py 4 norm tests/input_2.txt
H_matrices_2                                                   python symnmf.py 4 symnmf tests/input_2.txt
analyze_scores_1                                               python analysis.py 4 tests/input_2.txt

similarity_matrix_3        ./symnmf sym tests/input_3.txt      python symnmf.py 7 sym tests/input_3.txt 
diagonal_degree_matrix_3   ./symnmf ddg tests/input_3.txt      python symnmf.py 7 ddg tests/input_3.txt
normalized_matrix_3        ./symnmf norm tests/input_3.txt     python symnmf.py 7 norm tests/input_3.txt
H_matrices_3                                                   python symnmf.py 7 symnmf tests/input_3.txt
analyze_scores_1                                               python analysis.py 7 tests/input_3.txt
