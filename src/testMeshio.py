import meshio
from readingMesh import readingMesh
from main import temperature, elementsLibrary, nodesLibrary


points = []
for i in nodesLibrary:
    points.append(nodesLibrary[i])

elements = []
for i in elementsLibrary:
    elements.append([x - 1 for x in elementsLibrary[i]])

cells = [
    ("triangle", elements)
]

transitiveTemperature = dict()
for step in range(len(temperature)):
    transitiveTemperature[str(step)] = temperature[step]

# print(transitiveTemperature)

mesh = meshio.Mesh(
    points,
    cells,
    point_data = transitiveTemperature,
)

mesh.write(
    "mesh.vtk",  # str, os.PathLike, or buffer/open file
    # file_format="vtk",  # optional if first argument is a path; inferred from extension
)
