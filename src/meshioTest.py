import meshio
from readingMesh import readingMesh
from main import temperature, countSteps, timeStep, elementsLibrary, nodesLibrary

# # two triangles and one quad
# points = [
#     [0.0, 0.0],
#     [1.0, 0.0],
#     [0.0, 1.0],
#     [1.0, 1.0],
#     [2.0, 0.0],
#     [2.0, 1.0],
# ]
# cells = [
#     ("triangle", [[0, 1, 2], [1, 3, 2]]),
# ]

# # mesh = meshio.Mesh(
# #     points,
# #     cells,
# #     # Optionally provide extra data on points, cells, etc.
# #     point_data={"T": [0.3, -1.2, 0.5, 0.7, 0.0, -3.0]},
# #     # Each item in cell data must match the cells array
# #     cell_data={"a": [[0.1, 0.2]]},
# # )
# # mesh.write(
# #     "foo.vtk",  # str, os.PathLike, or buffer/open file
# #     # file_format="vtk",  # optional if first argument is a path; inferred from extension
# # )

# # # Alternative with the same options
# # meshio.write_points_cells("foo.vtk", points, cells)

# with meshio.xdmf.TimeSeriesWriter("filename.xdmf") as writer:
#     writer.write_points_cells(points, cells)
#     for t in [0.0, 0.1, 0.21]:
#         writer.write_data(t, point_data={"phi": data})


# # fileName = '../fixtures/Thermal.inp'
# # fileName = '../fixtures/dam_heat-transfer_test.inp'
# # fileName = '../fixtures/dam_heat-transfer_test (copy).inp'
# fileName = '../fixtures/16-elem.inp'
# # fileName = '../fixtures/test_2271elements.inp'
# # fileName = '../fixtures/test_384elements.inp'
# # fileName = '../fixtures/test_169elements.inp'
# [elementsLibrary, nodesLibrary] = readingMesh(fileName)

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
for step in range(countSteps):
    transitiveTemperature[str(timeStep * step)] = temperature[step]

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

# # Alternative with the same options
# meshio.write_points_cells("foo.vtk", points, cells)

