import pandas as pd

df = pd.read_csv("9-feb-16/data/titanic.csv", sep=",")
print(df)
print(df.shape)
print(type(df[["Pclass"]]))
print (df.values)

print(df.iloc[:,0:2]) # Esta forma de acceder a los datos puede provocar errores si los datos que nos llegan tienen las columnas desordenadas

print(df.loc[:5,"Survived"])
print("---------")
print(df.loc[:5,["Survived"]])

# La diferencia entre las dos anteriores lineas está en el tipo
print(type(df.loc[:5,"Survived"])) # tipo pandas.Series
print("---------")
print(type(df.loc[:5,["Survived"]]))# tipo pandas.DataFrame
# Si duplicamos un dataFrame con muchas series no duplicamos memoria, si duplicamos un dataFrame con un dataFrame sí duplicamos memoria

# Si queremos crear un DataFrame poco a poco sin duplicar memoria (evitando operaciones entre DataFrame y DataFrame
# Como lo que añadimos a dataFrame son filas usamos diccionarios, si añadieramos columnas usariamos pandas.Series

def proceso(i):
    return [1,2,3] # Aqui puede ser cualquier proceso complejo

df_final= {"n_coches": [], "velocidad_media":[], "n_personas":[]}

for i in range (100000):
    x = proceso(i)

#Faltan cosas

# Filtrar
column_name = "Embarked"

print(df.loc[df[column_name]=="S","Embarked"].count())

#Añadir y eliminar columnas

embarked_on_S = df[column_name]=="S"
print(embarked_on_S) # Es una Serie y no duplicamos memoria

df["embarked_on_S"] = embarked_on_S
print(df)

#Borrar una columna

df = df.drop(columns=[column_name]) #  La funcion drop duplica memoria

print(df)