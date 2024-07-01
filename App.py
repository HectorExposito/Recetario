from enum import Enum
from tkinter.tix import ComboBox
import Receta
from tkinter import *
import tkinter as tk

class Frames(Enum):
    MAIN_MENU=0
    RECIPES_MENU=1
    INGREDIENTS_MENU=2
    ADD_RECIPE=3
    SEE_RECIPES=4
    ADD_INGREDIENTS=5
    SEE_INGREDIENTS=6

class MyWindow:

    def __init__(self,root):
        self.root=root
        self.root.title("Recetario")
        self.setMainMenuFrame()

    def configureFrame(self,numberOfCols,numberOfRows):
            frame=Frame(self.root,width=600,height=600)
            frame.grid(column=1,row=1,sticky=(N,E,S,W))

            #Grid configuration
            if(numberOfCols==3):
                for i in range (0,numberOfCols):
                    if i==1:
                        frame.grid_columnconfigure(i,weight=1,minsize=(600/6)*4)
                    else:
                        frame.grid_columnconfigure(i,weight=1,minsize=600/6)
            else:
                for i in range (0,numberOfCols):
                   frame.grid_columnconfigure(i,weight=1,minsize=600/numberOfCols) 
                
            for i in range (0,numberOfRows):
                frame.grid_rowconfigure(i,weight=1,minsize=600/numberOfRows)
            
            return frame

    def setMainMenuFrame(self):
        mainMenu_frame=self.configureFrame(3,5)

        #Label with the name
        list_label=Label(mainMenu_frame,text="RECETARIO")
        list_label.grid(column=1,row=0,sticky=(N,E,S,W)) 

        #Set the buttons for the main panel
        recipes_button=Button(mainMenu_frame, text="Recipes",command=lambda:self.changePanel(mainMenu_frame,Frames.RECIPES_MENU))
        recipes_button.grid(column=1,row=1,sticky=(N,E,S,W))

        ingredients_button=Button(mainMenu_frame, text="Ingredients",command=lambda:self.changePanel(mainMenu_frame,Frames.INGREDIENTS_MENU))
        ingredients_button.grid(column=1,row=2,sticky=(N,E,S,W))

        close_button=Button(mainMenu_frame, text="Close",command=self.closeApp)
        close_button.grid(column=1,row=3,sticky=(N,E,S,W))

    def setRecipeMenuFrame(self):
        recipeMenu_frame=self.configureFrame(3,6)

        #Label with the name
        list_label=Label(recipeMenu_frame,text="RECIPES")
        list_label.grid(column=1,row=0,sticky=(N,E,S,W)) 

        #Set the buttons for the recipe menu
        addRecipe_button=Button(recipeMenu_frame, text="Add recipe",command=lambda:self.changePanel(recipeMenu_frame,Frames.ADD_RECIPE))
        addRecipe_button.grid(column=1,row=1,sticky=(N,E,S,W))

        seeRecipe_button=Button(recipeMenu_frame, text="See recipes",command=lambda:self.changePanel(recipeMenu_frame,Frames.SEE_RECIPES))
        seeRecipe_button.grid(column=1,row=2,sticky=(N,E,S,W))

        export_button=Button(recipeMenu_frame, text="Export recipes",command=lambda:self.changePanel(recipeMenu_frame,Frames.INGREDIENTS_MENU))
        export_button.grid(column=1,row=3,sticky=(N,E,S,W))

        return_button=Button(recipeMenu_frame, text="Return",command=lambda:self.changePanel(recipeMenu_frame,Frames.MAIN_MENU))
        return_button.grid(column=1,row=4,sticky=(N,E,S,W))

    def setIngredientsMenuFrame(self):
        ingredientsMenu_frame=self.configureFrame(3,5)

        #Label with the name
        list_label=Label(ingredientsMenu_frame,text="INGREDIENTS")
        list_label.grid(column=1,row=0,sticky=(N,E,S,W)) 

        #Set the buttons for the recipe menu
        addRecipe_button=Button(ingredientsMenu_frame, text="Add recipe",command=lambda:self.changePanel(ingredientsMenu_frame,Frames.RECIPES_MENU))
        addRecipe_button.grid(column=1,row=1,sticky=(N,E,S,W))

        seeRecipe_button=Button(ingredientsMenu_frame, text="See recipes",command=lambda:self.changePanel(ingredientsMenu_frame,Frames.INGREDIENTS_MENU))
        seeRecipe_button.grid(column=1,row=2,sticky=(N,E,S,W))

        return_button=Button(ingredientsMenu_frame, text="Return",command=lambda:self.changePanel(ingredientsMenu_frame,Frames.MAIN_MENU))
        return_button.grid(column=1,row=3,sticky=(N,E,S,W))

    def setAddRecipeFrame(self):
        addRecipe_frame=self.configureFrame(6,7)

        #Name of the recipe
        name=""
        name_label=Label(addRecipe_frame,text="Name:")
        name_label.grid(column=1,row=0,sticky=(N,E,S,W)) 

        name_entry=Entry(addRecipe_frame, textvariable=name)
        name_entry.grid(column=2,columnspan=3,row=0,sticky=(N,E,S,W))

        #Ingredient info
        ingredient_label=Label(addRecipe_frame,text="Ingredient:")
        ingredient_label.grid(column=1,row=1,sticky=(N,E,S,W)) 

        ingredient=""
        #ingredients_combo=ComboBox(addRecipe_frame,values=["a","b","c"],textvariable=ingredient)
        #ingredients_combo.grid(column=2,row=1,sticky=(N,E,S,W)) 

        quantity=0
        quantity_entry=Entry(addRecipe_frame, textvariable=quantity)
        quantity_entry.grid(column=3,row=1,sticky=(N,E,S,W))

        addIngredient_button=Button(addRecipe_frame, text="Add")
        addIngredient_button.grid(column=4,row=1,sticky=(N,E,S,W))

        #Ingredients list
        ingredients_list=Listbox(addRecipe_frame)#,listvariable=self.to_do_names)
        ingredients_list.grid(column=1,columnspan=4,row=2,sticky=(N,E,S,W))

        #Steps info
        step_label=Label(addRecipe_frame,text="Step:")
        step_label.grid(column=1,row=3,sticky=(N,E,S,W)) 

        step_entry=Entry(addRecipe_frame, textvariable=quantity)
        step_entry.grid(column=2,columnspan=2,row=3,sticky=(N,E,S,W))

        addStep_button=Button(addRecipe_frame, text="Add")
        addStep_button.grid(column=4,row=3,sticky=(N,E,S,W))

        #Steps list
        steps_list=Listbox(addRecipe_frame,height=10)#,listvariable=self.to_do_names)
        steps_list.grid(column=1,columnspan=4,row=4,sticky=(N,E,S,W))

        #Image selection
        image_label=Label(addRecipe_frame,text="Image:")
        image_label.grid(column=1,row=5,sticky=(N,E,S,W)) 

        #Buttons
        addRecipe_button=Button(addRecipe_frame, text="Add recipe")
        addRecipe_button.grid(column=2,row=6,sticky=(N,E,S,W))

        return_button=Button(addRecipe_frame, text="Return",command=lambda:self.changePanel(addRecipe_frame,Frames.RECIPES_MENU))
        return_button.grid(column=3,row=6,sticky=(N,E,S,W))

    def changePanel(self,frameToClose,frameToChange):
        frameToClose.destroy()

        if(frameToChange==Frames.MAIN_MENU):
            self.setMainMenuFrame()
        elif(frameToChange==Frames.RECIPES_MENU):
            self.setRecipeMenuFrame()
        elif(frameToChange==Frames.INGREDIENTS_MENU):
            self.setIngredientsMenuFrame()
        elif(frameToChange==Frames.ADD_RECIPE):
            self.setAddRecipeFrame()

    def closeApp(self):
        self.root.destroy()


root=Tk()
root.geometry("600x600")
root.resizable(width=False, height=False)
MyWindow(root)
root.mainloop()