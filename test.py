from PIL import Image

im = Image.open("static/img/templates/16 by 9/1.jpeg")
im2 = im.resize((1024, 768))
im2.save("static/img/templates/4 by 3/1.jpeg")