from ast import stmt
import base64
from enum import Enum
from io import BytesIO
import io
from sqlite3 import Blob
from tkinter import filedialog
from tkinter import ttk
from tkinter.tix import ComboBox
from tkinter.ttk import Combobox, Treeview

from sqlalchemy import BLOB, null
import Receta as receta
import PDFCreator as pdf
import Bdd as bdd
from tkinter import *
import tkinter as tk
from PIL import Image,ImageTk as itk

class Frames(Enum):
    MAIN_MENU=0
    RECIPES_MENU=1
    INGREDIENTS_MENU=2
    ADD_RECIPE=3
    SEE_RECIPES=4
    ADD_INGREDIENTS=5
    SEE_INGREDIENTS=6
    EDIT_INGREDIENTS=7
    EDIT_RECIPES=8

class MyWindow:

    def __init__(self,root):
        self.root=root
        self.root.title("Recetario")
        self.root.protocol("WM_DELETE_WINDOW",self.closeApp)
        self.loadAllIngrediennts()
        self.loadAllRecipes()
        self.setMainMenuFrame()
        self.defaultRecipeImage=Image.open("Recetario/Recetario/res/receta.png")

#region GUI
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

        export_button=Button(recipeMenu_frame, text="Export recipes",command=self.createPDF())
        export_button.grid(column=1,row=3,sticky=(N,E,S,W))

        return_button=Button(recipeMenu_frame, text="Return",command=lambda:self.changePanel(recipeMenu_frame,Frames.MAIN_MENU))
        return_button.grid(column=1,row=4,sticky=(N,E,S,W))

    def setIngredientsMenuFrame(self):
        ingredientsMenu_frame=self.configureFrame(3,5)

        #Label with the name
        list_label=Label(ingredientsMenu_frame,text="INGREDIENTS")
        list_label.grid(column=1,row=0,sticky=(N,E,S,W)) 

        #Set the buttons for the recipe menu
        addIngredient_button=Button(ingredientsMenu_frame, text="Add ingredient",command=lambda:self.changePanel(ingredientsMenu_frame,Frames.ADD_INGREDIENTS))
        addIngredient_button.grid(column=1,row=1,sticky=(N,E,S,W))

        seeIngredients_button=Button(ingredientsMenu_frame, text="See ingredients",command=lambda:self.changePanel(ingredientsMenu_frame,Frames.SEE_INGREDIENTS))
        seeIngredients_button.grid(column=1,row=2,sticky=(N,E,S,W))

        return_button=Button(ingredientsMenu_frame, text="Return",command=lambda:self.changePanel(ingredientsMenu_frame,Frames.MAIN_MENU))
        return_button.grid(column=1,row=3,sticky=(N,E,S,W))

    def setAddRecipeFrame(self):
        addRecipe_frame=self.configureFrame(6,7)
        addRecipe_frame.grid_rowconfigure(3,weight=1)
        addRecipe_frame.grid_columnconfigure(2,weight=1)

        #Name of the recipe
        name=""
        name_label=Label(addRecipe_frame,text="Name:")
        name_label.grid(column=1,row=0,sticky=(N,E,S,W)) 

        self.name_entry=Entry(addRecipe_frame, textvariable=name)
        self.name_entry.grid(column=2,columnspan=3,row=0,sticky=(N,E,S,W))

        #Ingredient info
        ingredient_label=Label(addRecipe_frame,text="Ingredient:")
        ingredient_label.grid(column=1,row=1,sticky=(N,E,S,W)) 

        ingredient=""
        ingredientsNames=[]
        for ing in self.allIngredients:
            ingredientsNames.append(ing.name)
        self.ingredients_combo=Combobox(addRecipe_frame,values=ingredientsNames,textvariable=ingredient)
        self.ingredients_combo.grid(column=2,row=1,sticky=(N,E,S,W)) 
        self.ingredients_combo.bind('<<ComboboxSelected>>', self.comboBoxModified)
        #ingredients_combo=ComboBox(addRecipe_frame,values=["a","b","c"],textvariable=ingredient)
        #ingredients_combo.grid(column=2,row=1,sticky=(N,E,S,W)) 

        self.quantity_entry=Entry(addRecipe_frame)
        self.quantity_entry.grid(column=3,row=1,sticky=(N,E,S,W))

        addIngredient_button=Button(addRecipe_frame, text="Add",command=self.addIngredientToRecipe)
        addIngredient_button.grid(column=4,row=1,sticky=(N,E,S,W))

        #Ingredients list
        self.ingredients_list=Listbox(addRecipe_frame,height=1)#,listvariable=self.to_do_names)
        self.ingredients_list.grid(column=1,columnspan=4,row=2,sticky=(N,E,S,W))
        scrollBar=ttk.Scrollbar(self.ingredients_list,orient="vertical",command=self.ingredients_list.yview)
        scrollBar.pack(side='right', fill='y')
        self.ingredients_list.configure(yscrollcommand=scrollBar.set)

        #Steps info
        step_label=Label(addRecipe_frame,text="Step:")
        step_label.grid(column=1,row=3,sticky=(N,E,S,W)) 

        self.step_text=Text(addRecipe_frame,wrap="word",width=1,height=1)
        self.step_text.grid(column=2,columnspan=2,row=3,sticky="nsew")

        addStep_button=Button(addRecipe_frame, text="Add",command=self.addStepToList)
        addStep_button.grid(column=4,row=3,sticky=(N,E,S,W))

        #Steps list
        self.steps_list=Listbox(addRecipe_frame,height=1)
        self.steps_list.grid(column=1,columnspan=4,row=4,sticky=(N,E,S,W))
        scrollBar=ttk.Scrollbar(self.steps_list,orient="vertical",command=self.steps_list.yview)
        scrollBar.pack(side='right', fill='y')
        self.steps_list.configure(yscrollcommand=scrollBar.set)

        #Image selection
        imageText_label=Label(addRecipe_frame,text="Image:")
        imageText_label.grid(column=1,row=5,sticky=(N,E,S,W)) 

        self.recipeImagePath="Recetario/Recetario/res/receta.png"
        pi=PhotoImage(file=self.recipeImagePath)
        pi=pi.subsample(10,10)
        self.recipeImage_label=Label(addRecipe_frame,image=pi)
        self.recipeImage_label.image=pi
        self.recipeImage_label.grid(column=2,row=5,sticky=(N,E,S,W))

        browseImage_button=Button(addRecipe_frame, text="Browse image",command=self.select_image)
        browseImage_button.grid(column=3,row=5,sticky=(N,E,S,W))

        #Buttons
        addRecipe_button=Button(addRecipe_frame, text="Add recipe",command=self.addRecipe)
        addRecipe_button.grid(column=2,row=6,sticky=(N,E,S,W))

        return_button=Button(addRecipe_frame, text="Return",command=lambda:self.changePanel(addRecipe_frame,Frames.RECIPES_MENU))
        return_button.grid(column=3,row=6,sticky=(N,E,S,W))

    def setAddIngredientFrame(self):
        addIngredient=self.configureFrame(5,4)

        #Name of the recipe
        name_label=Label(addIngredient,text="Name:")
        name_label.grid(column=1,row=0,sticky=(N,E,S,W)) 

        self.ingredientName_entry=Entry(addIngredient)
        self.ingredientName_entry.grid(column=2,columnspan=2,row=0,sticky=(N,E,S,W))

        #Ingredient info
        ingredient_label=Label(addIngredient,text="Measurement:")
        ingredient_label.grid(column=1,row=1,sticky=(N,E,S,W)) 

        measurement=""
        self.measurement_combo=Combobox(addIngredient,values=["Quantity","Litres","Grams","Cups","Spoons","None"])
        self.measurement_combo.current(0)
        self.measurement_combo.grid(column=2,row=1,sticky=(N,E,S,W)) 

        #Image selection
        imageText_label=Label(addIngredient,text="Image:")
        imageText_label.grid(column=1,row=2,sticky=(N,E,S,W)) 


        self.ingredientImagePath="Recetario/Recetario/res/ingrediente.png"
        pi=PhotoImage(file=self.ingredientImagePath)
        pi=pi.subsample(10,10)
        self.ingredientImage_label=Label(addIngredient,image=pi)
        self.ingredientImage_label.image=pi
        self.ingredientImage_label.grid(column=2,row=2,sticky=(N,E,S,W))
        browseImage_button=Button(addIngredient, text="Browse image",command=lambda:self.select_image(TRUE))
        browseImage_button.grid(column=3,row=2,sticky=(N,E,S,W))

        #Buttons
        addIngredient_button=Button(addIngredient, text="Add ingredient",command=self.addIngredient)
        addIngredient_button.grid(column=1,row=3,sticky=(N,E,S,W))

        return_button=Button(addIngredient, text="Return",command=lambda:self.changePanel(addIngredient,Frames.INGREDIENTS_MENU))
        return_button.grid(column=3,row=3,sticky=(N,E,S,W))

    def setSeeIngredientsFrame(self):
        seeRecipe_frame=self.configureFrame(2,3)

        #Table
        self.ingredients_table=ttk.Treeview(seeRecipe_frame)

        scrollBar=ttk.Scrollbar(self.ingredients_table,orient="vertical",command=self.ingredients_table.yview)
        scrollBar.pack(side='right', fill='y')
        self.ingredients_table.configure(yscrollcommand=scrollBar.set)

        style=ttk.Style(self.ingredients_table)
        style.configure("Treeview",rowheight=100)

        self.ingredients_table.grid(column=0,columnspan=2,row=1,sticky=(N,E,S,W))
        self.ingredients_table['columns'] = ('name', 'measurement', 'image')
        self.ingredients_table.column("#0", width=0,  stretch=NO)
        self.ingredients_table.heading("#0",text="",anchor=CENTER)
        self.ingredients_table.heading("name",text="NAME",anchor=CENTER)
        self.ingredients_table.column("name", width=150,  stretch=YES)
        self.ingredients_table.heading("measurement",text="MEASUREMENT",anchor=CENTER)
        self.ingredients_table.column("measurement", width=150,  stretch=YES)
        self.ingredients_table.heading("image",text="IMAGE",anchor=CENTER)
        self.ingredients_table.column("image", width=300,  stretch=NO)
        row=0
        for ing in self.allIngredients:
            print(row)
            im = Image.open(io.BytesIO(ing.getImage()))
            im.thumbnail((100,100))
            photo = itk.PhotoImage(im)
            self.ingredients_table.insert(parent='',index='end',iid=row,text='',values=(ing.name,ing.measurement),image=photo)
            self.ingredients_table.rowconfigure(index=row,minsize=300)
            row=row+1
        self.ingredients_table.bind("<<TreeviewSelect>>", lambda s: self.changeEditIngredientButton())
        #Buttons
        self.editIngredient_button=Button(seeRecipe_frame, text="Edit ingredient",command=lambda:self.selectIngredientToEdit(seeRecipe_frame,Frames.EDIT_INGREDIENTS),state=tk.DISABLED)
        self.editIngredient_button.grid(column=0,row=2,sticky=(N,E,S,W))

        return_button=Button(seeRecipe_frame, text="Return",command=lambda:self.changePanel(seeRecipe_frame,Frames.INGREDIENTS_MENU))
        return_button.grid(column=1,row=2,sticky=(N,E,S,W))

    def setEditIngredientFrame(self):
        editIngredient=self.configureFrame(5,4)

        ingredientToEditCopy=self.ingredientToEdit

        #Name of the recipe
        name_label=Label(editIngredient,text="Name:")
        name_label.grid(column=1,row=0,sticky=(N,E,S,W)) 

        self.editIngredientName_entry=Entry(editIngredient)
        self.editIngredientName_entry.insert(0,ingredientToEditCopy.getName())
        self.editIngredientName_entry.grid(column=2,columnspan=2,row=0,sticky=(N,E,S,W))

        #Ingredient info
        ingredient_label=Label(editIngredient,text="Measurement:")
        ingredient_label.grid(column=1,row=1,sticky=(N,E,S,W)) 

        measurement=""
        self.editMeasurement_combo=Combobox(editIngredient,values=["Quantity","Litres","Grams","Cups","Spoons","None"])
        i=0
        for val in self.editMeasurement_combo["values"]:
            if(val==ingredientToEditCopy.getMeasurement()):
                break
            i+=1
        self.editMeasurement_combo.current(i)
        self.editMeasurement_combo.grid(column=2,row=1,sticky=(N,E,S,W)) 

        #Image selection
        imageText_label=Label(editIngredient,text="Image:")
        imageText_label.grid(column=1,row=2,sticky=(N,E,S,W)) 

        self.ingredientImagePath="Recetario/Recetario/res/ingrediente.png"
        pi=PhotoImage(file=self.ingredientImagePath)
        pi=pi.subsample(10,10)
        ingredientImage_label=Label(editIngredient,image=pi)
        ingredientImage_label.image=pi
        ingredientImage_label.grid(column=2,row=2,sticky=(N,E,S,W))

        browseImage_button=Button(editIngredient, text="Browse image",command=self.select_image)
        browseImage_button.grid(column=3,row=2,sticky=(N,E,S,W))

        #Buttons
        saveIngredient_button=Button(editIngredient, text="Save ingredient",command=lambda:self.editIngredient(editIngredient))
        saveIngredient_button.grid(column=1,row=3,sticky=(N,E,S,W))

        return_button=Button(editIngredient, text="Return",command=lambda:self.changePanel(editIngredient,Frames.SEE_INGREDIENTS))
        return_button.grid(column=3,row=3,sticky=(N,E,S,W))

    def setSeeRecipes(self):
        seeRecipe_frame=self.configureFrame(2,3)

        #Table
        self.recipes_table=ttk.Treeview(seeRecipe_frame)

        scrollBar=ttk.Scrollbar(self.recipes_table,orient="vertical",command=self.recipes_table.yview)
        scrollBar.pack(side='right', fill='y')
        self.recipes_table.configure(yscrollcommand=scrollBar.set)

        style=ttk.Style(self.recipes_table)
        style.configure("Treeview",rowheight=100)

        self.recipes_table.grid(column=0,columnspan=2,row=1,sticky=(N,E,S,W))
        self.recipes_table['columns'] = ('name', 'image')
        self.recipes_table.column("#0", width=0,  stretch=NO)
        self.recipes_table.heading("#0",text="",anchor=CENTER)
        self.recipes_table.heading("name",text="NAME",anchor=CENTER)
        self.recipes_table.column("name", width=150,  stretch=YES)
        self.recipes_table.heading("image",text="IMAGE",anchor=CENTER)
        self.recipes_table.column("image", width=300,  stretch=NO)
        row=0
        for r in self.allRecipes:
            print(row)
            im = Image.open(io.BytesIO(r.getImage()))
            im.thumbnail((100,100))
            photo = itk.PhotoImage(im)
            self.recipes_table.insert(parent='',index='end',iid=row,text='',values=(r.name),image=photo)
            self.recipes_table.rowconfigure(index=row,minsize=300)
            row=row+1
        self.recipes_table.bind("<<TreeviewSelect>>", lambda s: self.changeEditRecipeButton())
        #Buttons
        self.editRecipe_button=Button(seeRecipe_frame, text="See recipe",command=lambda:self.selectRecipeToEdit(seeRecipe_frame,Frames.EDIT_RECIPES),state=tk.DISABLED)
        self.editRecipe_button.grid(column=0,row=2,sticky=(N,E,S,W))

        return_button=Button(seeRecipe_frame, text="Return",command=lambda:self.changePanel(seeRecipe_frame,Frames.RECIPES_MENU))
        return_button.grid(column=1,row=2,sticky=(N,E,S,W))
    
    def setAddRecipeFrame(self):
        addRecipe_frame=self.configureFrame(6,7)
        addRecipe_frame.grid_rowconfigure(3,weight=1)
        addRecipe_frame.grid_columnconfigure(2,weight=1)

        #Name of the recipe
        name=""
        name_label=Label(addRecipe_frame,text="Name:")
        name_label.grid(column=1,row=0,sticky=(N,E,S,W)) 

        self.name_entry=Entry(addRecipe_frame, textvariable=name)
        self.name_entry.grid(column=2,columnspan=3,row=0,sticky=(N,E,S,W))

        #Ingredient info
        ingredient_label=Label(addRecipe_frame,text="Ingredient:")
        ingredient_label.grid(column=1,row=1,sticky=(N,E,S,W)) 

        ingredient=""
        ingredientsNames=[]
        for ing in self.allIngredients:
            ingredientsNames.append(ing.name)
        self.ingredients_combo=Combobox(addRecipe_frame,values=ingredientsNames,textvariable=ingredient)
        self.ingredients_combo.grid(column=2,row=1,sticky=(N,E,S,W)) 
        self.ingredients_combo.bind('<<ComboboxSelected>>', self.comboBoxModified)
        #ingredients_combo=ComboBox(addRecipe_frame,values=["a","b","c"],textvariable=ingredient)
        #ingredients_combo.grid(column=2,row=1,sticky=(N,E,S,W)) 

        self.quantity_entry=Entry(addRecipe_frame)
        self.quantity_entry.grid(column=3,row=1,sticky=(N,E,S,W))

        addIngredient_button=Button(addRecipe_frame, text="Add",command=self.addIngredientToRecipe)
        addIngredient_button.grid(column=4,row=1,sticky=(N,E,S,W))

        #Ingredients list
        self.ingredients_list=Listbox(addRecipe_frame,height=1)#,listvariable=self.to_do_names)
        self.ingredients_list.grid(column=1,columnspan=4,row=2,sticky=(N,E,S,W))
        scrollBar=ttk.Scrollbar(self.ingredients_list,orient="vertical",command=self.ingredients_list.yview)
        scrollBar.pack(side='right', fill='y')
        self.ingredients_list.configure(yscrollcommand=scrollBar.set)

        #Steps info
        step_label=Label(addRecipe_frame,text="Step:")
        step_label.grid(column=1,row=3,sticky=(N,E,S,W)) 

        self.step_text=Text(addRecipe_frame,wrap="word",width=1,height=1)
        self.step_text.grid(column=2,columnspan=2,row=3,sticky="nsew")

        addStep_button=Button(addRecipe_frame, text="Add",command=self.addStepToList)
        addStep_button.grid(column=4,row=3,sticky=(N,E,S,W))

        #Steps list
        self.steps_list=Listbox(addRecipe_frame,height=1)
        self.steps_list.grid(column=1,columnspan=4,row=4,sticky=(N,E,S,W))
        scrollBar=ttk.Scrollbar(self.steps_list,orient="vertical",command=self.steps_list.yview)
        scrollBar.pack(side='right', fill='y')
        self.steps_list.configure(yscrollcommand=scrollBar.set)

        #Image selection
        imageText_label=Label(addRecipe_frame,text="Image:")
        imageText_label.grid(column=1,row=5,sticky=(N,E,S,W)) 

        pi=PhotoImage(file="Recetario/Recetario/res/receta.png")
        pi=pi.subsample(10,10)
        image_label=Label(addRecipe_frame,image=pi)
        image_label.image=pi
        image_label.grid(column=2,row=5,sticky=(N,E,S,W))

        browseImage_button=Button(addRecipe_frame, text="Browse image",command=self.select_image)
        browseImage_button.grid(column=3,row=5,sticky=(N,E,S,W))

        #Buttons
        addRecipe_button=Button(addRecipe_frame, text="Add recipe",command=self.addRecipe)
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
        elif(frameToChange==Frames.ADD_INGREDIENTS):
            self.setAddIngredientFrame()
        elif(frameToChange==Frames.SEE_INGREDIENTS):
            self.setSeeIngredientsFrame()
        elif(frameToChange==Frames.EDIT_INGREDIENTS):
            self.setEditIngredientFrame()
        elif(frameToChange==Frames.SEE_RECIPES):
            self.setSeeRecipes()
        elif(frameToChange==Frames.EDIT_RECIPES):
            self.setAddRecipeFrame()

#endregion

#region save and edit ingredients
    def addIngredient(self):
        n=self.ingredientName_entry.get()
        m=self.measurement_combo.get()
        i=self.convertToBinaryData(self.ingredientImagePath)
        if(len(n)<3):
            print("nombre no valido")
            return
        
        ingredient=receta.Ingredient(n,m,i)
        if(self.allIngredients.__contains__(ingredient)==False):
            self.allIngredients.append(ingredient)
        
        
        print("ingrediente añadido "+n+" "+m)

    def editIngredient(self,editFrame):
        n=self.editIngredientName_entry.get()
        m=self.editMeasurement_combo.get()
        i=self.convertToBinaryData(self.ingredientImagePath)
        if(len(n)<3):
            print("nombre no valido")
            return
        ingredient=receta.Ingredient(n,m,i)

        for ing in self.allIngredients:
            if(self.ingredientToEdit==ing):
                self.allIngredients.remove(ing)
                self.removeIngredientFromDataBase(ing)
                self.allIngredients.append(ingredient)
                break
        
        print("ingrediente editado: "+self.ingredientToEdit.getName()+" "+self.ingredientToEdit.getMeasurement()+"\n"+
              ""+ing.getName()+" "+ing.getMeasurement())
        self.ingredientToEdit=null
        self.changePanel(editFrame,Frames.SEE_INGREDIENTS)
     
    def changeEditIngredientButton(self):
        if(self.editIngredient_button["state"]==tk.DISABLED):
            self.editIngredient_button["state"]=tk.NORMAL
        
    def selectIngredientToEdit(self,frameToClose,frameToChange):
        ingredientToEdit=self.ingredients_table.item(self.ingredients_table.focus())
        
        ingredientName=ingredientToEdit["values"][0]
        for ing in self.allIngredients:
            print(ing.getName()+" "+ingredientName)
            if(ing.getName()==ingredientName):
                self.ingredientToEdit=ing
                break
        
        self.changePanel(frameToClose,frameToChange)
    
#endregion
#region save and edit recipe
    def comboBoxModified(self,event):
        i=self.ingredients_combo.current()
        ing=self.allIngredients[i]
        if(ing.measurement=="None"):
            self.quantity_entry.config(state='disabled')
        else:
            self.quantity_entry.config(state='normal')

    def addIngredientToRecipe(self):
        q=self.quantity_entry.get()+" "
        q=q.strip()
        m=""
        i=self.ingredients_combo.current()
        ing=self.allIngredients[i]

        if(self.checkIfIngredientIsAlreadyOnRecipe(ing)==False):
            if(ing.measurement!="Quantity"):
                m=ing.measurement+" "
            if(ing.measurement=="None"):
                q=""
                m=""
            else:
                try:
                    float(q)
                except ValueError:
                    print("Not a float")
                    return

            self.ingredients_list.insert(len(self.ingredients_list.get(0,last=None)),q+""+m+""+ing.name)
        
        self.quantity_entry.delete(0, 'end')

    def checkIfIngredientIsAlreadyOnRecipe(self,ing):
        for i in self.ingredients_list.get(0,last=self.ingredients_list.size()):
            if ing.name in i:
                print("Existe ingrediente")
                return True
        print("No existe ingrediente")
        return False
    
    def addStepToList(self):
        step=self.step_text.get("1.0",END)
        step=step.strip()
        if(len(step)>=3):
            stepNumber=self.steps_list.size()+1
            step=str(stepNumber)+": "+step
            self.steps_list.insert(stepNumber-1,step)
            self.step_text.delete("1.0",END)
        
    def addRecipe(self):
        n=self.name_entry.get()
        n=n.strip()
        ing=self.ingredients_list.get(0,last=self.ingredients_list.size())
        steps=self.steps_list.get(0,last=self.steps_list.size())
        image=self.convertToBinaryData("Recetario/Recetario/res/receta.png")
        if(len(n)>=3 and len(ing)>0 and len(steps)>0):
            r=receta.Recipe(n,image)
            riList=list()
            for i in ing:
                print("Ingrediente "+i)
                riList.append(receta.RecipeAndIngredient(n,i))
            
            rsList=list()
            for s in steps:
                rsList.append(receta.RecipeAndSteps(n,s))
            recipe=receta.RecipeAllInfo(n,image,ing,steps)
            self.allRecipes.append(recipe)
            #self.addRecipeToDataBase(r,riList,rsList)
        else:
            print("no se puede guardar")

    def changeEditRecipeButton(self):
        if(self.editRecipe_button["state"]==tk.DISABLED):
            self.editRecipe_button["state"]=tk.NORMAL

    def selectIngredientToEdit(self,frameToClose,frameToChange):
        recipeToEdit=self.recipes_table.item(self.recipes_table.focus())
        
        recipeName=recipeToEdit["values"][0]
        for r in self.allRecipes:
            print(r.getName()+" "+recipeName)
            if(r.getName()==recipeName):
                self.recipeToEdit=r
                break
        
        self.changePanel(frameToClose,frameToChange)
     
#endregion
    def loadAllIngrediennts(self):
        selectIngredients=bdd.select(receta.Ingredient)
        self.allIngredients=[]
        for ing in bdd.session.execute(selectIngredients):
            self.allIngredients.append(ing[0])

    def loadAllRecipes(self):
        selectRecipes=bdd.select(receta.Recipe)
        selectRecipesAndIngredients=bdd.select(receta.RecipeAndIngredient)
        selectRecipesAndSteps=bdd.select(receta.RecipeAndSteps)

        recipes=[]
        for r in bdd.session.execute(selectRecipes):
            recipes.append(r[0])

        recipesAndIngredients=[]
        for ri in bdd.session.execute(selectRecipesAndIngredients):
            recipesAndIngredients.append(ri[0])

        recipesAndSteps=[]
        for rs in bdd.session.execute(selectRecipesAndSteps):
            recipesAndSteps.append(rs[0])

        self.allRecipes=[]
        for r in recipes:
            n=r.getName()
            i=r.getImage()
            ingredients=[]
            steps=[]
            for ri in recipesAndIngredients:
                if(n==ri.getName()):
                    ingredients.append(ri.getIngredient())

            for rs in recipesAndSteps:
                if(n==rs.getName()):
                    steps.append(rs.getStep())
            
            self.allRecipes.append(receta.RecipeAllInfo(n,i,ingredients,steps))

    def removeIngredientFromDataBase(self,ing):
        bdd.session.delete(ing)
    def convertToBinaryData(self,filename):
        # Convert binary format to images or files data
        with open(filename, 'rb') as file:
            blobData = file.read()
        return blobData

    def select_image(self,isIngredient=FALSE):
        filetypes = (
        ('Image files', '*.PNG'),
        ('All files','*.*')
        )

        filename = filedialog.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes)

        if(isIngredient):
            self.ingredientImagePath=filename
            pi=PhotoImage(file=self.ingredientImagePath)
            pi=pi.subsample(10,10)
            self.ingredientImage_label.configure(image=pi)
            self.ingredientImage_label.image=pi
        else:
            self.recipeImagePath=filename
            pi=PhotoImage(file=self.recipeImagePath)
            pi=pi.subsample(10,10)
            self.recipeImage_label.configure(image=pi)
            self.recipeImage_label.image=pi
        
        print(filename)
    def saveIngredientsOnDataBase(self):
        for ingredient in self.allIngredients:
            bdd.session.add(ingredient)
            bdd.session.commit()
    def saveRecipesOnDataBase(self):
        for r in self.allRecipes:
            q = bdd.session.query(receta.Recipe.name).filter(receta.Recipe.name==r.getName())
            print(bdd.session.query(q.exists()).scalar())
            if(bdd.session.query(q.exists()).scalar()==False):
                print(r.getName())
                recipe=receta.Recipe(r.getName(),r.getImage())
                bdd.session.add(recipe)
                bdd.session.commit()
                for i in r.getIngredients():
                    print(i)
                    bdd.session.add(receta.RecipeAndIngredient(r.getName(),i))
                    bdd.session.commit()
                for s in r.getSteps():
                    bdd.session.add(receta.RecipeAndSteps(r.getName(),s))
                    bdd.session.commit()
    def addRecipeToDataBase(self,r,riList,rsList):
        bdd.session.add(r)
        bdd.session.commit()

        for ri in riList:
            bdd.session.add(ri)
            bdd.session.commit()
        
        for rs in rsList:
            bdd.session.add(rs)
            bdd.session.commit()
    def closeApp(self):
        self.saveIngredientsOnDataBase()
        self.saveRecipesOnDataBase()
        self.root.destroy()
    def createPDF(self):
        pdf.CreatePdf(self.allRecipes,"Recetario.pdf")
bdd.Base.metadata.create_all(bdd.engine)
root=Tk()
root.geometry("600x600")
root.resizable(width=False, height=False)
MyWindow(root)
root.mainloop()