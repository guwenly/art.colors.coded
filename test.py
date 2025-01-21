import cv2
import glob
import os
import numpy as np
import matplotlib.pyplot as plt
os.chdir(os.path.dirname(os.path.realpath(__file__)))
import PIL
from colorthief import ColorThief
from PIL import Image, ImageDraw, ImageFont
#font = ImageFont.truetype('RobotoSlab-Medium.ttf', size=10)
import webcolors
from zipfile import ZipFile
import time
import shutil
import smtplib 

print("Ayırma işlemi Başlıyor.")
for file in glob.glob("artfiles/*"):
    try:
        image = Image.open(file)
        width, height = image.size
        isim = os.path.splitext(os.path.basename(file))[0]
        print(isim)
        color_thief = ColorThief(file)
        palette = color_thief.get_palette(color_count=11)
        palette = np.array(palette)[np.newaxis, :, :]
        plt.imshow(palette);
        plt.axis('off');
        plt.savefig('palettes/{}-palette.jpg'.format(isim),bbox_inches='tight')
        image.save(file)
    except:
        pass

print("Çıktılar alınıyor.")
for file1 in glob.glob("artfiles/*"):
    for file2 in glob.glob("palettes/*"):
        if os.path.splitext(os.path.basename(file2))[0].split('-palette')[0] == os.path.splitext(os.path.basename(file1))[0]:
            try:
                isim = os.path.splitext(os.path.basename(file1))[0]
                image = cv2.imread(file1)
                width, height = PIL.Image.open(file1).size
                bar = cv2.imread(file2)
                width1 = width
                height1 = int(height/14)
                #height1 = int(40)
                dsize = (width1, height1)
                barImage = cv2.resize(bar, dsize)
                newImg = np.concatenate([image, barImage], axis=0)
                cv2.imwrite('outputs/{}-output.jpg'.format(isim), newImg)
            except:
                print('Bir tane atlandı.')
                continue

print('Bitti.')
