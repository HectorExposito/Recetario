
from numpy import append


class Ingredientes:
    def __init__(self,medida,nombre):
        self.medida=medida
        self.nombre=nombre
    
    def getMedida(self):
        return self.medida

    def getNombre(self):
        return self.nombre

class Receta:
    def __init__(self,nombre,ingredientes):
        self.ingredientes=ingredientes
        self.nombre=nombre

    def getIngredientes(self):
        return self.ingredientes

    def getNombre(self):
        return self.nombre

class Recetario:
    def __init__(self):
        self.recetas=[]

    def addReceta(self,receta):
        self.recetas=append(self.recetas,receta)

ingr=[]
for i in range(0,10):
    ingr.append(Ingredientes("Cucharada","Ingrediente {}"+str(i)))

for i in range(0,10):
   print(ingr[i].getMedida(),ingr[i].getNombre())

rec=[]
for i in range(0,10):
   rec.append(Receta("Receta "+str(i),ingr))

for i in range(0,10):
    ing=""
    lista=rec[i].getIngredientes()
    for j in range(0,len(lista)):
        ing+=lista[j].getNombre()+","
    print(rec[i].getNombre(),ing)