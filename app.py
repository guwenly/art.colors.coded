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
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 
import smtplib 

artist = 'Abdur Rahman Chughtai'
def closest_colour(requested_colour):
    min_colours = {}
    for key, name in webcolors.CSS3_HEX_TO_NAMES.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_colour[0]) ** 2
        gd = (g_c - requested_colour[1]) ** 2
        bd = (b_c - requested_colour[2]) ** 2
        min_colours[(rd + gd + bd)] = name
    return min_colours[min(min_colours.keys())]

def get_colour_name(requested_colour):
    try:
        closest_name = actual_name = webcolors.rgb_to_name(requested_colour)
    except ValueError:
        closest_name = closest_colour(requested_colour)
        actual_name = None
    return actual_name, closest_name

def crop_center(pil_img, crop_width, crop_height):
    img_width, img_height = pil_img.size
    return pil_img.crop(((img_width - crop_width) // 2,
                         (img_height - crop_height) // 2,
                         (img_width + crop_width) // 2,
                         (img_height + crop_height) // 2))

def crop_max_square(pil_img):
    return crop_center(pil_img, min(pil_img.size), 13*min(pil_img.size)/14)

print("Ayırma işlemi Başlıyor.")
for file in glob.glob("artfiles/*"):
    try:
        #x = 9
        image = Image.open(file)
        image = crop_max_square(image)
        width, height = image.size
        #ImageDraw.Draw(image).text((8, 8), "@art.colors.coded", fill='rgb(0, 0, 0)', font=font)
        isim = os.path.splitext(os.path.basename(file))[0]
        print(isim)
        color_thief = ColorThief(file)
        palette = color_thief.get_palette(color_count=11)
        #while x > 0:
            #palette.insert(x,[255,255,255])
            #x-=1
        text_file = open('outputs/' + isim + ".txt", "w")
        text_file.write("The artist is:{}\n".format(artist))
        for pal in palette:
            actual_name, closest_name = get_colour_name(pal)
            text_file.write("{}: {}.\n".format(closest_name,str(pal).split('(')[1].split(')')[0]))
        palette = np.array(palette)[np.newaxis, :, :]
        plt.imshow(palette);
        plt.axis('off');
        plt.savefig('palettes/{}-palette.jpg'.format(isim),bbox_inches='tight')
        image.save(file)
        text_file.close()
    except:
        os.remove(file)

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
                #newImg2 = cv2.resize(newImg, (500,500))
                cv2.imwrite('outputs/{}-output.jpg'.format(isim), newImg)
                os.remove(file1)
                os.remove(file2)
            except:
                print('Bir tane atlandı.')
                continue

zipisim = '{}-pieces.zip'.format(time.strftime("%d%m%Y"))
zipObj = ZipFile(zipisim, 'w')
for files in glob.glob("outputs/*"):
	zipObj.write(files)
	os.remove(files)
zipObj.close()

def mail():
    fromaddr = "xxx@gmail.com"
    toaddr = "xxx@gmail.com"
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "art.colors.coded Pieces"
    body = "Have a great day. Here are the daily pieces."
    msg.attach(MIMEText(body, 'plain'))

    attachment = open(zipisim, "rb")
    a = MIMEBase('application', 'zip')
    a.set_payload(attachment.read())
    encoders.encode_base64(a)
    a.add_header('Content-Disposition', 'attachment',filename=zipisim)
    msg.attach(a)

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(fromaddr, "xxx")
    text = msg.as_string()
    s.sendmail(fromaddr, toaddr, text)
    s.quit()
    print("Mail yollandı.")

mail()
original = r'./{}'.format(zipisim)
target = r'backup/{}'.format(zipisim)
shutil.move(original,target)
print('Dosyalar taşındı.')
print('Bitti.')
