from PIL import Image

# Load the .ico file
ico = Image.open("icon.ico")

# Save 128x128 version as PNG
ico.save("static/icon128.png", format="PNG", sizes=[(128, 128)])
ico.save("static/iconOutline.png", format="PNG", sizes=[(128, 128)])  # Placeholder - same as color
print("✅ PNG icons saved in static/")
