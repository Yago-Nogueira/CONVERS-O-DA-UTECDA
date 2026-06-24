

def is_completa(matriz):
    resp = True
    if len(matriz) > 0:
        len_linha = len(matriz[0])
        for linha in range(1,len(matriz)):
            if ( len(matriz[linha]) != len_linha):
                resp = False
    else:
        resp = False
    return resp

A = [[1,3,5],[2,4,6]]
B = [[1,3],[2,4,6,8]]
D = []

print(is_completa(A))
print(is_completa(B))
print(is_completa(D))