from PIL import Image
image=Image.open("H:/Clip/buildings_scale/campus_0.png")
image = image.convert('RGBA')
w, h = image.size

background = Image.new('RGB', size=(max(w, h), max(w, h)), color=(127,127,127))  # 创建背景图，颜色值为127
length = int(abs(w - h) // 2)  # 一侧需要填充的长度
box = (length, 0) if w < h else (0, length)  # 粘贴的位置
background.paste(image, box,mask=image)
image_data=background.resize((256,256))#缩放
background.show()

image_data.save("H:/Clip/buildings/output.jpg")

