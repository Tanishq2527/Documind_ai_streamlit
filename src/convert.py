import base64

file_path = "Mini Invoice Document.pdf"   # ✅ your DOCX file

with open(file_path, "rb") as f:
    encoded = base64.b64encode(f.read()).decode()

with open("base64.txt", "w") as f:
    f.write(encoded)

print("Base64 saved in base64.txt")