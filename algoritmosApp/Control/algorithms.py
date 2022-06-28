import numpy as np
import sys
from numpy import linalg as LA

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

def get_clusters(graph, k):
    numnodes = graph.shape[0]
    # labels = np.random.randint(1, size=num_nodes)

    clusters = [list(range(numnodes))]

    for i in range(k - 1):


        old_cluster_index = 0

        old_cluster_ss_eval = sys.maxsize
        new_clusters = [clusters[old_cluster_index]]
        # newclusterfound = False
        # crear nuevos clústeres a partir de un clúster grande anterior
        for cluster_index, cluster in enumerate(clusters):
            # matriz de adyacencia para nodos de clúster
            if len(cluster) <= 1:
                continue
            cluster_adj_mat = graph[:, cluster]
            cluster_adj_mat = cluster_adj_mat[cluster, :]
            possible_new_clusters, ss_eval = spectral_partition(cluster_adj_mat, cluster)
            # if ss_eval <= old_cluster_ss_eval and len(possible_new_clusters[0])>0 and len(possible_new_clusters[1])>0:
            if ss_eval <= old_cluster_ss_eval:
                old_cluster_ss_eval = ss_eval
                old_cluster_index = cluster_index
                new_clusters = possible_new_clusters

        del clusters[old_cluster_index]
        clusters += new_clusters

        # print("newclusters:",clusters)
        # print("creating cluster ", (i + 1))
        # print()

    # for i,v in enumerate(clusters):
    #    labels[v] = i
    clusters_dict = {}
    for i, v in enumerate(clusters):
        cluster_label = "cluster_" + str(i + 1)
        clusters_dict[cluster_label] = v
    return clusters_dict


def spectral_partition(adj_mat, nodeIds):
    # grado de todos los nodos del grafo
    # print("Calculando grado")
    degrees = np.sum(adj_mat, axis=1)

    # matriz laplaciana del grafo
    #print("matriz laplacianamatriz laplaciana")
    lap_mat = np.diag(degrees) - adj_mat

    #print("Calculating eval and evecs")
    #st = time.time()
    e_vals, e_vecs = LA.eigh(lap_mat)
    #print("matriz laplaciana:",lap_mat)
    #print("evals:", e_vals)
    #print("evec:", e_vecs)
    #tt = time.time() - st
    #print("Time to calculate eval of shape:", adj_mat.shape[0], " is:", tt)

    # Como todos los valores propios de la matriz laplaciana son mayores o iguales a 0, se recorta cualquier valor negativo pequeño
    e_vals = e_vals.clip(0)

    #print("sorting eval")
    sorted_evals_index = np.argsort(e_vals)

    # ss_index para almacenar el índice del segundo valor propio más pequeño
    ss_index = 0
    for index in sorted_evals_index:
        if (e_vals[index] > 0):
            ss_index = index
            break

    # vector propio del segundo valor propio más pequeño
    ss_evec = e_vecs[:, ss_index]

    # second smallest eigen value
    ss_eval = e_vals[ss_index]

    clusters = getClusterFromEvec(ss_evec, nodeIds)
    #print(clusters)
    if (len(clusters[0]) == 0 or len(clusters[1]) == 0):
        clusters = getClusterFromEvec(e_vecs[:, 1], nodeIds)
        ss_eval = e_vals[1]
        #print("inside:",clusters)
        #print("evec:",e_vecs)
    #print("clusters recibidos:",nodeIds)
    #print("clusters retornados:",clusters)
    return clusters, ss_eval


def getClusterFromEvec(ss_evec, nodeIds):
    # print("creating 2 clus")
    clusters = [[], []]
    for i, v in enumerate(ss_evec):
        if v >= 0:
            clusters[0].append(nodeIds[i])
        else:
            clusters[1].append(nodeIds[i])
    return clusters
    
def inicializarCluster(adyacencia, ncluster):
    grafo = np.array(adyacencia)
    return get_clusters(grafo, ncluster)
    

