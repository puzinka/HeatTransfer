import meshio

def read_vtk_temperatures(vtk_file):
  

    # Read the VTK file.
    mesh = meshio.read(vtk_file)

    # Get the point data.
    point_data = mesh.point_data

    # Extract the temperature values.
    temperatures = point_data["T"]

    # Create a dictionary of node numbers and temperatures.
    temperatures_dict = dict()
    for i, node_id in enumerate(mesh.points):
        temperatures_dict[str(i)] = temperatures[i]
    return temperatures_dict

def save_to_file(arr, filename):
  with open(filename, 'w') as f:
    # increment = 0
    increment = 643
    for temper in arr:
        key_value_pairs = list(temper.items())
        key_value_pairs.sort(key=lambda x: x[0])
        temper = dict(key_value_pairs)

        for key, value in temper.items():
            f.write(str(increment) + ","+str(key)+","+str(value) + "\n")
        increment = increment + 1



save_to_file([read_vtk_temperatures('./tmp/mesh730.vtk')], "temp_last.csv")