import numpy as np


def mutualInformation(m1, m2):
    sum_mi = 0.0
    x_value_list = np.unique(m1)
    y_value_list = np.unique(m2)
    Px = np.array([len(m1[m1 == xval])/float(len(m1))
                  for xval in x_value_list])
    Py = np.array([len(m2[m2 == yval])/float(len(m2))
                  for yval in y_value_list])
    for i in range(len(x_value_list)):
        if Px[i] == 0.:
            continue
        sy = m2[m1 == x_value_list[i]]
        if len(sy) == 0:
            continue
        pxy = np.array([len(sy[sy == yval])/float(len(m2))
                       for yval in y_value_list])
        t = pxy[Py > 0.]/Py[Py > 0.] / Px[i]
        sum_mi += sum(pxy[t > 0]*np.log2(t[t > 0]))
    return sum_mi


def pendent_pair(Vprime, V, S, f, params=None):
    x = 0
    vnew = Vprime[x]
    n = len(Vprime)
    Wi = []
    used = np.zeros((n, 1))
    used[x] = 1
    for i in range(n - 1):
        vold = vnew
        Wi = Wi + S[vold]
        # update keys
        keys = np.ones((n, 1)) * np.inf
        for j in range(n):
            if used[j]:
                continue
            keys[j] = f(Wi + S[Vprime[j]], V, params) - \
                f(S[Vprime[j]], V, params)
        # extract min
        argmin = np.argmin(keys)
        vnew = Vprime[argmin]
        used[argmin] = 1
        fval = np.min(keys)
    s = vold
    t = vnew
    return s, t, fval


def diff(A, B):
    m = np.amax(np.array([np.amax(A), np.amax(B)]))
    vals = np.zeros((m + 1, 1))
    vals[A] = 1
    vals[B] = 0
    idx = np.nonzero(vals)
    return idx[0]


z = []


def optimal_set(V, f, params=None):
    n = len(V)
    S = [[] for _ in range(n)]
    for i in range(n):
        S[i] = [V[i]]
    p = np.zeros((n - 1, 1))
    A = []
    idxs = range(n)
    for i in range(n - 1):
        # find a pendant pair
        t, u, fval = pendent_pair(idxs, V, S, f, params)
        # candidate solution
        A.append(S[u])
        z.append(S[u])
        p[i] = f(S[u], V, params)
        S[t] = [*S[t], *S[u]]
        idxs = diff(idxs, u)
        S[u] = []

    # return minimum solution
    i = np.argmin(p)
    R = A[i]
    fval = p[i]
    # make R look pretty
    notR = diff(V, R)
    ## R = sorted(R)
    ## notR = sorted(notR)
    if R[0] < notR[0]:
        R = (tuple(R), tuple(notR))
    else:
        R = (tuple(notR), tuple(R))
    return R, fval


def inicializar(adyacencia):
    rows = adyacencia.shape[0]
    cols = adyacencia.shape[1]
    aux = np.array(adyacencia)
    for x in range(0, rows):
        for y in range(0, cols):
            if aux[x,y] == 1:
                aux[x,y] = 0
            else:
                aux[x,y] = 1
    print("")
    print("ORIGINAL")
    print(adyacencia)
    print("")
    print("COMPLEMENTO")
    print(aux)
    print("")
    print("")
    print("")
    m1 = np.array( adyacencia ) 
    m2 = np.array(aux)  
    V = [x for x in range(1, len(aux) + 1)]
    f = lambda V,S, params: mutualInformation(adyacencia,aux)
    
    R, fval = optimal_set(V, f)
    print("RESULTADO: ", R)
    return R
