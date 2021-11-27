
def mergeLists(L, R):
    n1 = len(L)
    n2 = len(R)
    arr = []
    i = 0
    j = 0

    while i < n1 and j < n2:
        if L[i]['id'] == R[j]['id']:
            arr.append(L[i])
            i += 1
            j += 1
        elif L[i]['id'] < R[j]['id']:
            arr.append(L[i])
            i += 1
        else:
            arr.append(R[j])
            j += 1

    while i < n1:
        arr.append(L[i])
        i += 1

    while j < n2:
        arr.append(R[j])
        j += 1
    
    return arr

if __name__ == '__main__':
    l = [1, 3, 4, 7, 13]
    r = [6, 7, 8, 10, 11]
    print(mergeLists(l, r))