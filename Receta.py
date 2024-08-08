import Bdd
from numpy import append
import sqlalchemy as db
from sqlalchemy import Column, Integer, String, Float, BLOB

class Ingredient(Bdd.Base):
    __tablename__='ingredients'

    name = Column(String, primary_key=True)
    measurement = Column(String, nullable=False)
    image = Column(BLOB)

    def __init__(self,name,measurement,image):
        self.measurement=measurement
        self.name=name
        self.image=image
    
    def getMeasurement(self):
        return self.measurement

    def getName(self):
        return self.name
    
    def getImage(self):
        return self.image
    
    def __eq__(self, other): 
        if not isinstance(other, Ingredient):
            # don't attempt to compare against unrelated types
            return False
        
        if(self.name==other.name):
            return True
        
        return False

class Recipe():
    
    def __init__(self,name,ingredients,image):
        self.ingredients=ingredients
        self.name=name
        self.image=image

    def getIngredients(self):
        return self.ingredients

    def getName(self):
        return self.name

class RecipeAndIngredient():
    def __init__(self,recipeName,recipeIngredient):
        self.recipeName=recipeName
        self.recipeIngredient=recipeIngredient
class Recetario:
    def __init__(self):
        self.recetas=[]

    def addReceta(self,receta):
        self.recetas=append(self.recetas,receta)
