import meshio
from main import elementsLibrary, nodesLibrary, temperature

nodes = []
for node in nodesLibrary:
    nodes.append(nodesLibrary[node])
points = nodes

elements = []
for el in elementsLibrary:
    elements.append(elementsLibrary[el])
for i in range(len(elements)):
    for j in range(len(elements[i])):
        elements[i][j] -= 1
cells = [
    ("triangle", elements),
]

data = dict()
for step in range(len(temperature)):
    data[f"{step}"] = temperature[step]
print(data)

mesh = meshio.Mesh(
    points,
    cells,
    point_data = {"T": data},
)

mesh.write(
    "data.vtk", 
)

meshio.write_points_cells("data.vtk", points, cells)