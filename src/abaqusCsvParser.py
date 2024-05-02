import csv

def parse_csv(filename):

  with open(filename, "r") as f:
    reader = csv.reader(f)
    headers = next(reader)

    increment = ""

    tempers = []


    for row in reader:
        curTimeStep = row[2]
        if(curTimeStep != increment):
            increment = curTimeStep
            tempers.append(dict())
        node = row[4]
        temp = row[11]
        # node = row[5]
        # temp = row[12]
        tempers[len(tempers)-1][node] = temp

  return tempers


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



  


data = parse_csv("../abaqus21_04.csv")


save_to_file(data[643:], "test3.csv")



