import PIL
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
import Receta as receta

def CreatePdf(allRecipes,path):
    c = canvas.Canvas(path,pagesize=A4)
    w, h = A4
    text = c.beginText(50, h - 50)
    text.setFont("Times-Roman", 24)
    text.textLine("ÍNDICE")
    text.setFont("Times-Roman", 12)
    for r in allRecipes:
        text.textLine(r.getName())
    c.drawText(text)
    c.showPage()

    for r in allRecipes:
        im = PIL.Image.open(io.BytesIO(r.getImage()))
        img=ImageReader(im)
        c.drawImage(img,100, h - 100,width=50, height=50)
        text = c.beginText(50, h - 50)
        text.setFont("Times-Roman", 24)
        text.textLine(r.getName())
        text.setFont("Times-Roman", 16)
        text.textLine("Ingredientes")
        text.setFont("Times-Roman", 12)
        for i in r.getIngredients():
            text.textLine(i)
        text.setFont("Times-Roman", 16)
        text.textLine("Pasos")
        text.setFont("Times-Roman", 12)
        for s in r.getSteps():
            text.textLine(s)
        c.drawText(text)
        c.showPage()
    
    c.drawText(text)
    c.save()
