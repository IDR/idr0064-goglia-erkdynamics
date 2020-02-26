import csv
from pathlib import Path

"""
Create the .screen files for idr0064-goglia-erkdynamics
"""

in_file = "/Users/dlindner/assays.txt"
out_dir = Path("/Users/dlindner/generated")
base_path = "/uod/idr/filesets/idr0064-goglia-erkdynamics/20190630-ftp/Plate {}/{}"

def write_plate(name, data):
  out_file = out_dir / "{}.screen".format(name)
  writer = open(out_file, "w")
  writer.write("[Plate]\n")
  writer.write("Name = {}\n".format(name))
  writer.write("Rows = 7\n")
  writer.write("Columns = 17\n")
  writer.write("Fields = 1\n")
  for i, path in enumerate(data):
    row = int(i / 17)
    col = i % 17
    writer.write("\n[Well {}]\n".format(i))
    writer.write("Row {}\n".format(row))
    writer.write("Column {}\n".format(col))
    if path:
      writer.write("Field_0 = {}\n".format(path))
  writer.close()

def well_row(name):
  if name.startswith("C"):
    return 2
  if name.startswith("D"):
    return 3
  if name.startswith("E"):
    return 4
  if name.startswith("F"):
    return 5
  if name.startswith("G"):
    return 6
  return None

def well_col(name):
  n = int(name[1:])
  return n - 1

cur_plate_name = ""
cur_plate = []

with open(in_file, newline="") as csvfile:
  reader = csv.DictReader(csvfile, delimiter="\t")

  for row in reader:
    if row["Plate"] != cur_plate_name:
      if len(cur_plate) > 0:
        write_plate(cur_plate_name, cur_plate)
      cur_plate_name = row["Plate"]
      cur_plate = [None for i in range(0,119)]

    well = row["Well"]
    img = row["FileName"]
    index = well_row(well) * 17 + well_col(well)
    cur_plate[index] = base_path.format(cur_plate_name, img)

  write_plate(cur_plate_name, cur_plate)
