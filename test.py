import pathlib
path=str( pathlib.Path().absolute())#+'\\images\\image-2.png'

#print(path+"\index.html")

html=open(path+"\index.html",'r')
print(open(path+"\index.html",'r').read())
html.close()