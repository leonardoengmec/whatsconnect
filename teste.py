with open("./config.py","r+") as f:
    old = f.read()
    f.seek(len(old)-1)
    f.write('    "123456": "Teste", \n}')