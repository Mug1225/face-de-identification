from PIL import Image
import cv2
import numpy as np
dna = {}
dna["00"] = "A"
dna["01"] = "T"
dna["10"] = "G"
dna["11"] = "C"
dna["A"] = [0, 0]
dna["T"] = [0, 1]
dna["G"] = [1, 0]
dna["C"] = [1, 1]
# DNA xor
dna["AA"] = dna["TT"] = dna["GG"] = dna["CC"] = "A"
dna["AG"] = dna["GA"] = dna["TC"] = dna["CT"] = "G"
dna["AC"] = dna["CA"] = dna["GT"] = dna["TG"] = "C"
dna["AT"] = dna["TA"] = dna["CG"] = dna["GC"] = "T"
def dna_encode(b, g, r):
    b = np.unpackbits(b, axis=1)
    g = np.unpackbits(g, axis=1)
    r = np.unpackbits(r, axis=1)
    m, n = b.shape
    r_enc = np.chararray((m, int(n / 2)))
    g_enc = np.chararray((m, int(n / 2)))
    b_enc = np.chararray((m, int(n / 2)))

    for color, enc in zip((b, g, r), (b_enc, g_enc, r_enc)):
        idx = 0
        for j in range(0, m):
            for i in range(0, n, 2):
                enc[j, idx] = dna["{0}{1}".format(color[j, i], color[j, i + 1])]
                idx += 1
                if (i == n - 2):
                    idx = 0
                    break

    b_enc = b_enc.astype(str)
    g_enc = g_enc.astype(str)
    r_enc = r_enc.astype(str)
    return b_enc, g_enc, r_enc
def xor_operation(b, g, r, mk):
    m, n = b.shape
    bx = np.chararray((m, n))
    gx = np.chararray((m, n))
    rx = np.chararray((m, n))
    b = b.astype(str)
    g = g.astype(str)
    r = r.astype(str)
    for i in range(0, m):
        for j in range(0, n):
            bx[i, j] = dna["{0}{1}".format(b[i, j], mk[i, j])]
            gx[i, j] = dna["{0}{1}".format(g[i, j], mk[i, j])]
            rx[i, j] = dna["{0}{1}".format(r[i, j], mk[i, j])]
    bx = bx.astype(str)
    gx = gx.astype(str)
    rx = rx.astype(str)
    return bx, gx, rx
def keymatrixencode(key, b):
    b = np.unpackbits(b, axis=1)
    m, n = b.shape
    key_bin = bin(int(key, 16))[2:].zfill(256)
    Mk = np.zeros((m, n), dtype=np.uint8)
    x = 0
    for j in range(0, m):
        for i in range(0, n):
            Mk[j, i] = key_bin[x % 256]
            x += 1

    Mk_enc = np.chararray((m, int(n / 2)))
    idx = 0
    for j in range(0, m):
        for i in range(0, n, 2):
            if idx == (n / 2):
                idx = 0
            Mk_enc[j, idx] = dna["{0}{1}".format(Mk[j, i], Mk[j, i + 1])]
            idx += 1
    Mk_enc = Mk_enc.astype(str)
    return Mk_enc
def dna_decode(b, g, r):
    m, n = b.shape
    r_dec = np.ndarray((m, int(n * 2)), dtype=np.uint8)
    g_dec = np.ndarray((m, int(n * 2)), dtype=np.uint8)
    b_dec = np.ndarray((m, int(n * 2)), dtype=np.uint8)
    for color, dec in zip((b, g, r), (b_dec, g_dec, r_dec)):
        for j in range(0, m):
            for i in range(0, n):
                dec[j, 2 * i] = dna["{0}".format(color[j, i])][0]
                dec[j, 2 * i + 1] = dna["{0}".format(color[j, i])][1]
    b_dec = (np.packbits(b_dec, axis=-1))
    g_dec = (np.packbits(g_dec, axis=-1))
    r_dec = (np.packbits(r_dec, axis=-1))
    return b_dec, g_dec, r_dec

def decompose_matrix(iname):
    image = cv2.imread(iname)
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
    return B, G, R
def recover_image(b, g, r, iname):
    img = cv2.imread(iname)
    iname=iname[:-4]
    print(iname)
    img[:, :, 2] = r
    img[:, :, 1] = g
    img[:, :, 0] = b
    cv2.imwrite(("enc.jpg"), img)
    print("saved ecrypted image as enc.jpg")
    im = Image.open(r"C:/pycharm/enc.jpg")
    im.show()
def encode(key,file):
    im = Image.open(file)
    pass1='1234asdfg'
    blue, green, red = decompose_matrix(file)
    blue_e, green_e, red_e = dna_encode(blue, green, red)
    Mk_e = keymatrixencode(key, blue)
    blue_final, green_final, red_final = xor_operation(blue_e, green_e, red_e, Mk_e)
    b, g, r = dna_decode(blue_final, green_final, red_final)
    recover_image(b, g, r, file)