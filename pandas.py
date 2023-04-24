import pandas as pd
from pandas import *

#leer excel y convertirlo en json

df = pd.read_excel("C:/Users/frias/Downloads/ABRIL 2023 NOMINA DE EMPLEADOS Y FUNCIONARIOS FIJOS.xlsx")

df.to_json("C:/Users/frias/Downloads/ABRIL 2023 NOMINA DE EMPLEADOS Y FUNCIONARIOS FIJOS.json",orient="records")
