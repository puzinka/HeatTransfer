import meshio
from readingMesh import readingMesh
from main import temperature, elementsLibrary, nodesLibrary
# from main3D import temperature, elementsLibrary, nodesLibrary
import json

points = []
for i in nodesLibrary:
    points.append(nodesLibrary[i])

elements = []
for i in elementsLibrary:
    elements.append([x - 1 for x in elementsLibrary[i]])

cells = [
    ("triangle", elements)
]



for step in range(len(temperature)):
    data = dict()

    data["T"] = temperature[step]

    mesh = meshio.Mesh(
        points,
        cells,
        point_data = data,
    )

    mesh.write(
        "tmp/mesh"+str(step)+".vtk",
        binary=False
    )


def create_vtk_series(filesCount, time_step):
    vtk_series = {
        "file-series-version": "1.0",
        "files": []
    }

    time = 0
    for i in range(filesCount):
        vtk_file = {
            "name": "mesh"+str(i)+".vtk",
            "time": time
        }
        vtk_series["files"].append(vtk_file)
        time += time_step

    with open("tmp/mesh.vtk.series", "w") as f:
        json.dump(vtk_series, f, indent=2)

create_vtk_series(len(temperature), 1)