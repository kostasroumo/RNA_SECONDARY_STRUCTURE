import numpy as np
import sys

# A function for checking the validity of pairs. Valid combinations: {A, U} and {C, G}
def can_pair(base_1: str, base_2: str) -> bool:
    if (base_1 == 'A' and base_2 == 'U') or (base_1 == 'U' and base_2 == 'A'):
        return True
    elif (base_1 == 'C' and base_2 == 'G') or (base_1 == 'G' and base_2 == 'C'):
        return True
    else:
        return False


def get_dot_bracket_notation(n: int, sorted_pais) -> str:
    # Initialize the dot-bracket string with dots
    dot_bracket = ['.'] * n
    # Iterate through the sorted pairs of nodes
    for pair in sorted_pais:
        # Set the left and right indices of the pair
        i = pair[0]
        j = pair[1]
        # Update the dot-bracket string with brackets at the pair indices
        dot_bracket[i] = '('
        dot_bracket[j] = ')'
    # Join the dot-bracket string and return it
    return ''.join(dot_bracket)

# traceback and return pairs
def extract_pairs(matrix, i, j,rna_sequence):
    if i >= j:
        return []

    if matrix[i][j] == matrix[i + 1][j - 1] + 1 and can_pair(rna_sequence[i], rna_sequence[j]):
        return [(i, j)] + extract_pairs(matrix, i + 1, j - 1,sequence)

    for k in range(i, j):
        if matrix[i][j] == matrix[i][k] + matrix[k + 1][j]:
            return extract_pairs(matrix, i, k,sequence) + extract_pairs(matrix, k + 1, j,sequence)


#  return cell's opt_val 
def get_opt_val(sequence: str, opt_val: list, opt_val_pairs: list, i: int, j: int,fold) -> int:
    
    if i>=j:
        max_val=0
        return max_val
    else:
        if opt_val[i][j]!=-1:
            return opt_val[i][j]
        val=get_opt_val(sequence,opt_val,opt_val_pairs,i,j-1,fold)
        val_list=[]
        for t in range(i,j-4):
            if can_pair(sequence[t],sequence[j]):
                val_1=get_opt_val(sequence,opt_val,opt_val_pairs,i,t-1,fold)
                val_2=get_opt_val(sequence,opt_val,opt_val_pairs,t+1,j-1,fold)
                new_val=val_1+val_2 +1
                val_list.append(new_val)
            else:
                val_list.append(-1)
                
        max_1=max(val_list)
        if max_1>val:
            val=max_1
            
        opt_val[i][j]=val
        return val


# return secondary structure
def compute_rna_secondary_structure(sequence: str) -> tuple:
    n = len(sequence)
    # Initializations
    opt_val = [[-1 for j in range(n)] for i in range(n)]
    opt_val_pairs = [[[] for j in range(n)] for i in range(n)]

    for i in range(n):
        for j in range(n):
            if i >= j - 4:
                opt_val[i][j] = 0
    fold = []
    for k in range(5, n):
        for i in range(0, n - k):
            j = i + k
            get_opt_val(sequence, opt_val, opt_val_pairs, i, j,fold)
    
    fold=[]
    pairs=extract_pairs(opt_val,0,n-1,sequence)
    sorted_pairs = pairs
    dot_bracket_notation = get_dot_bracket_notation(n, sorted_pairs)
    
    return  sorted_pairs,dot_bracket_notation
    

