import numpy as np
import numpy.linalg as la
from time import time
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from readingMesh import readingMesh

# fileName = '../fixtures/Thermal.inp'
fileName = '../fixtures/Dam_plane.inp'

[Element_library, Node_library] = readingMesh(fileName)


Area = 0.5
t = 1
Lambda = 2
q = 5  ####Тепловой поток на границе
Length = 1 ####Длина грани элемента

NumberOfNodes = len(Node_library)
NumberOfElements = len(Element_library)

# NumberOfNodes = 12
# NumberOfElements = 12
# NodeLabels = np.arange(1, NumberOfNodes + 1)
# ElementLabels = np.arange(1, NumberOfElements + 1)
# CoordinatesX = np.array([0.0,0.0,0.0,0.0,1.0,1.0,1.0,1.0,2.0,2.0,2.0,2.0])
# CoordinatesY = np.array([0.0,1.0,2.0,3.0,3.0,2.0,1.0,0.0,0.0,1.0,2.0,3.0])
# NodesElements = np.array([[4,5,6],[4,3,6],[3,6,7],[3,2,7],
#                           [2,7,8],[2,1,8],[5,12,11],[5,6,11],
#                           [6,11,10],[6,7,10],[7,10,9],[7,8,9]])

# #%%Nodes and elements dictionaries

# #словарь, в котором [номер элемента: его узлы]
# Element_library = dict() 

# #словарь, в котором [номер элемента: его координаты]
# Node_library = dict()
# index = 0
# for Nodes in NodesElements:
#     element_label = ElementLabels[index]
#     Element_library[element_label] = [Nodes[0], Nodes[1], Nodes[2]]
#     index+=1
# index = 0
# for node_label in NodeLabels:
#     Node_library[node_label] = [CoordinatesX[index], CoordinatesY[index]]
#     index+=1

# # print('Node_library')
# # print(Node_library)
# # print('Element_library')
# # print(Element_library)

#%%Conductivity matrix assembling    

K = np.zeros((NumberOfNodes, NumberOfNodes))

for Element in Element_library:
    NodeLabel1 = Element_library[Element][0]
    NodeLabel2 = Element_library[Element][1]
    NodeLabel3 = Element_library[Element][2]
    x1 = Node_library[NodeLabel1][0]
    x2 = Node_library[NodeLabel2][0]
    x3 = Node_library[NodeLabel3][0]
    y1 = Node_library[NodeLabel1][1]
    y2 = Node_library[NodeLabel2][1]
    y3 = Node_library[NodeLabel3][1]
    
    dN1_dksi = -1.0
    dN2_dksi = 0.0
    dN3_dksi = 1.0

    dN1_deta = -1.0
    dN2_deta = 1.0
    dN3_deta = 0.0

    Koordinates = np.array([[x1, x2, x3],
                             [y1, y2, y3]])

    Koordinates = Koordinates.transpose()
    Jakobi = np.matmul(np.array([[dN1_dksi, dN2_dksi, dN3_dksi],
                                 [dN1_deta, dN2_deta, dN3_deta]]), Koordinates)

    Jakobi_inverse = la.inv(Jakobi)
    Jakobian = la.det(Jakobi)
    DN1_dx_DN1_dy = np.matmul(Jakobi_inverse, np.array([[dN1_dksi],[dN1_deta]]))
    DN2_dx_DN2_dy = np.matmul(Jakobi_inverse, np.array([[dN2_dksi],[dN2_deta]]))
    DN3_dx_DN3_dy = np.matmul(Jakobi_inverse, np.array([[dN3_dksi],[dN3_deta]]))
    
    B_matrix = np.zeros((2,3))
    B_matrix[:,0] = DN1_dx_DN1_dy.transpose()
    B_matrix[:,1] = DN2_dx_DN2_dy.transpose()
    B_matrix[:,2] = DN3_dx_DN3_dy.transpose()
    B_matrix_transpose = B_matrix.transpose()
           
    Klocal = 0.5*abs(Jakobian)*t*Lambda*np.matmul(B_matrix_transpose,B_matrix)

    k = (NodeLabel1 - 1)
    l = (NodeLabel2 - 1)
    m = (NodeLabel3 - 1)

#######Заполнение главной диагонали############
    K[k, k] += Klocal[0,0]
    K[l, l] += Klocal[1,1]
    K[m, m] += Klocal[2,2]

#######Верхний Блок k - l##########
    K[k, l] += Klocal[0,1]
    
######Нижний блок l - k##########    
    K[l, k] += Klocal[1,0]

#######Верхний Блок k - m##########    
    K[k, m] += Klocal[0,2]

######Нижний блок m - k##########      
    K[m, k] += Klocal[2,0]

#######Верхний Блок l - m##########    
    K[l, m] += Klocal[1,2]

######Нижний блок m - l##########      
    K[m, l] += Klocal[2,1]

#%%Boundary conditions and loads

K_reduced = K
K_reduced = np.delete(K_reduced,0,0)
K_reduced = np.delete(K_reduced,0,1)

K_reduced = np.delete(K_reduced,0,0)
K_reduced = np.delete(K_reduced,0,1)

K_reduced = np.delete(K_reduced,0,0)
K_reduced = np.delete(K_reduced,0,1)

K_reduced = np.delete(K_reduced,0,0)
K_reduced = np.delete(K_reduced,0,1)


F = np.zeros((NumberOfNodes - 4))
F[11 - 4] = q * Length * t / 2
F[10 - 4] = q * 2 * Length * t / 2
F[9 - 4]  = q * 2 * Length * t / 2
F[8 - 4]  = q * Length * t / 2

#%%Solution
T = la.solve(K_reduced,F)

#%%
T = np.insert(T,0,0,axis=0)
T = np.insert(T,0,0,axis=0)
T = np.insert(T,0,0,axis=0)
T = np.insert(T,0,0,axis=0)

#%%Plotting
X = np.array([0, 1, 2])
Y = np.array([0, 1, 2, 3])
Z = np.zeros((4,3))
Z[0] = (T[0],T[7],T[8])
Z[1] = (T[1], T[6], T[9])
Z[2] = (T[2], T[5], T[10])
Z[3] = (T[3], T[4], T[11])

fig = plt.figure(dpi=300)
plt.contourf(X, Y, Z)
plt.title('Temperature')
plt.colorbar()
#plt.axes().set_aspect('equal') 

plt.show()