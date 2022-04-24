from PIL import Image

im = Image.open("static/img/users/150px/ksenia_shiraeva@yandex.com.jpg")
im2 = im.resize((30, 30))
im2.save("static/img/users/30px/ksenia_shiraeva@yandex.com.jpg")