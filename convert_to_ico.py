from PIL import Image

img = Image.open("icon.png")
img.save("icon.ico", format="ICO", sizes=[(256, 256)])
