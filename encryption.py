import cv2
import numpy as np
from tkinter import *
from PIL import Image
from tkinter import filedialog
def factor(m):
    key1=[]
    for i in range(2,m+1):
        if(m%i==0):
            key1.append(i)
    return key1
def keygen(x,r,size):
    key=[]
    index=[]
    for i in range(size):
        x=r*x*(1-x)
        key.append(x)
        index.append(i)
    for i in range(size):
        for j in range(size):
            if(key[i]>key[j]):
                key[i],key[j]=key[j],key[i]
                index[i],index[j]=index[j],index[i]
    return index
def shuffle(m,n,b,g,r,t):
    m, n = b.shape
    key1= factor(m)
    print(key1)
    length=len(key1)
    x=int(length/30*t)
    x=key1[x]
    B1 = np.zeros((m, n), dtype='int8')
    G1 = np.zeros((m, n), dtype='int8')
    R1 = np.zeros((m, n), dtype='int8')
    B2=np.zeros((m, n), dtype='int8')
    G2=np.zeros((m, n), dtype='int8')
    R2=np.zeros((m, n), dtype='int8')
    print(B1.shape, b.shape, x)
    key = []
    key = keygen(0.01, 3.95, x)
    print(m,x)
    for i in range(0, m, x):
        for k in range(0, x):
            for j in range(0,n):
                B1[i+k,j] = b[i + key[k],j]
                G1[i+k,j] = g[i + key[k],j]
                R1[i+k,j] = r[i + key[k],j]
    key1 = factor(n)
    print(key1)
    length = len(key1)
    y = int(length / 30 * t)
    y = key1[y]
    key = keygen(0.01, 3.95, y)
    for i in range(m):
        for j in range(0,n,y):
            for k in range(y):
                B2[i,j+k]=B1[i,j+key[k]]
                G2[i, j + k] = G1[i, j + key[k]]
                R2[i, j + k] = R1[i, j + key[k]]

    return B2,G2,R2
def recover_image(b, g, r, iname):
    img = cv2.imread(iname)
    iname=iname[:-4]
    print(iname)
    img[:, :, 2] = r
    img[:, :, 1] = g
    img[:, :, 0] = b
    cv2.imwrite(("diffused.jpg"), img)
    print("saved ecrypted image as diffused.jpg")
    im = Image.open(r"C:/pycharm/diffused.jpg")
    im.show()
#if (__name__ == "__main__"):
def main(a):
    path = "NULL"
    root = Tk()
    root.withdraw()
    path = filedialog.askopenfilename()

    image = cv2.imread(path)
    red = image[:, :, 2]
    green = image[:, :, 1]
    blue = image[:, :, 0]
    for values, channel in zip((red, green, blue), (2, 1, 0)):
        img = np.zeros((values.shape[0], values.shape[1]), dtype=np.uint8)
        img[:, :] = (values)
        if channel == 0:
            B = np.asmatrix(img)
        elif channel == 1:
            G = np.asmatrix(img)
        else:
            R = np.asmatrix(img)
    img = Image.open(path)
    m, n = img.size
    b, g, r = shuffle(m, n, B, G, R, a)
    recover_image(b, g, r, path)
    path="C:/pycharm/diffused.jpg"
    return path
