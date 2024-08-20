import Bdd
from numpy import append
import sqlalchemy as db
from sqlalchemy import Column, Integer, PrimaryKeyConstraint, String, Float, BLOB, UniqueConstraint

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

class Recipe(Bdd.Base):
    __tablename__='recipes'
    name = Column(String, primary_key=True)
    image = Column(BLOB)

    def __init__(self,name,image):
        self.name=name
        self.image=image

    def getName(self):
        return self.name
    def getImage(self):
        return self.image

class RecipeAndIngredient(Bdd.Base):
    __tablename__='recipeAndIngredients'
    
    name = Column(String, primary_key=True)
    ingredient = Column(String, primary_key=True)

    __table_args__ = (
        PrimaryKeyConstraint(
            name,
            ingredient),
        {})

    def __init__(self,recipeName,ingredient):
        self.name=recipeName
        self.ingredient=ingredient
    
    def getName(self):
        return self.name
    
    def getIngredient(self):
        return self.ingredient

class RecipeAndSteps(Bdd.Base):
    __tablename__='recipeAndSteps'
    name = Column(String, primary_key=True)
    step = Column(String,primary_key=True)

    __table_args__ = (
        PrimaryKeyConstraint(
            name,
            step),
        {})

    def __init__(self,recipeName,step):
        self.name=recipeName
        self.step=step

    def getName(self):
        return self.name
    
    def getStep(self):
        return self.step

class RecipeAllInfo:
    def __init__(self,name,image,ingredients,steps):
        self.name=name
        self.image=image
        self.ingredients=ingredients
        self.steps=steps

    def getName(self):
        return self.name
    
    def getSteps(self):
        return self.steps
    
    def getImage(self):
        return self.image
    
    def getIngredients(self):
        return self.ingredients

class Recetario:
    def __init__(self):
        self.recetas=[]

    def addReceta(self,receta):
        self.recetas=append(self.recetas,receta)
