# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 20:47:04 2020

@author: EUNHANJO
"""

import cv2
import numpy as np
import pytesseract
from  PIL import Image
from PIL import ImageGrab 
import re

import urllib.request
import os

# image url to download
url = "https://firebasestorage.googleapis.com/v0/b/wncw-f04a4.appspot.com/o/images%2Fdrug.png?alt=media&"
# file path and file name to download
outpath = "C: desktop/test/"
outfile = "drug.jpg"

# Create when directory does not exist
if not os.path.isdir(outpath):
    os.makedirs(outpath)

# download
urllib.request.urlretrieve(url, outpath+outfile)
print("complete!")


def finding_letters(image):
    img = cv2.imread(image)
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    sharpen = cv2.filter2D(gray, -1, kernel)
    #cv2.imshow("gray",sharpen)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    blur = cv2.GaussianBlur(sharpen, ksize=(3,3), sigmaX=0)
    ret, thresh1 = cv2.threshold(blur, 127, 255, cv2.THRESH_BINARY)
    #cv2.imshow('blur',blur)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    cannya= cv2.Canny(gray,25,25)
    #cv2.imshow('canny',cannya)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    #src = cv2.imread("c:/")
    dst = cannya.copy()
    circles = cv2.HoughCircles(blur, cv2.HOUGH_GRADIENT, 1, 100, param1 = 250, param2 = 10, minRadius = 0, maxRadius = 0)
    cv2.circle(dst, (circles[0][0][0],circles[0][0][1]),circles[0][0][2], (255, 255, 255), 5)
    cv2.circle(dst, (circles[0][1][0],circles[0][1][1]),circles[0][1][2], (255, 255, 255), 5)
    #print(circles[0][0][0]) print(circles[0][0][1]) print(circles[0][0][2]) print(circles[0][1][0]) print(circles[0][1][1]) 
    #print(circles[0][1][2])
    #cv2.imshow("dst", dst)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    
#####타원 검출 ######
def finding_letters2(image):
    img = cv2.imread(image)
    #cv2.imshow('img',img)
    rblur = cv2.GaussianBlur(img, ksize=(205,205), sigmaX=0)
    #cv2.imshow('r',rblur)
    rimg_gr = cv2.cvtColor(rblur,cv2.COLOR_BGR2GRAY)
    rret,rthresh = cv2.threshold(rimg_gr,127,255,0)
    rcontours,_=cv2.findContours(rthresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(img,rcontours,-1,(0,255,0),3)
    #cv2.imshow('rimg',img)
    #cv2.imshow('rcountours',rthresh)
    rcontour = rcontours[0]
    x,y,w,h=cv2.boundingRect(rcontour)
    rim = cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),3)
    #print(x," ",y," ",w," ",h)
    rhull = cv2.convexHull(rcontour)
    rhim = cv2.drawContours(img,[rhull],-1,(255,0,0),4)
    rcropped=img[y+50:y+h-50,x+50:x+w-50]
    #cv2.imshow("cropped",rcropped)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    return preprocessing(rcropped)
 
#####타원 전처리#####
def preprocessing(rcropped):
    nblur = cv2.GaussianBlur(rcropped, ksize=(9,9), sigmaX=0)
    ngray = cv2.cvtColor(nblur, cv2.COLOR_RGB2GRAY)
    nngray = cv2.cvtColor(rcropped,cv2.COLOR_RGB2GRAY)
    #cv2.imshow('blur',ngray)
    nblackawhite=cv2.adaptiveThreshold(ngray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
    #cv2.imshow("blackandwhite",nblackawhite)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    return result(nblackawhite)
    
def result(r):
    txt=pytesseract.image_to_string(r,lang='eng')
    list_par =[]
    for i in txt:
        text = re.sub('[^a-zA-Z0-9]',' ',i).strip()
        if(text!=''):
            list_par.append(text)
        resulta=''
        for j in list_par:
            resulta+=j
    resulta=resulta.upper()
    return (resulta)

image =r'C:\Users\EUNHANJO\Desktop\ test\drug.jpg'


#print(finding_letters2(image))

###낱알 식별 파일 불러오기
import pandas as pd

drug_letters = pd.read_csv('drug_letters.csv')
letter_list_f=drug_letters['표시앞'] #앞면 리스트
letter_list_b=drug_letters['표시뒤'] #뒷면 리스트

def find_dr(letters):
    for k,v in letter_list_f.items():
        if(v==letters):
            #print('찾았다')
            return drug_letters.loc[k]['품목명']
        
print(find_dr(finding_letters2(image)))
            
        
###질병-약 부작용 찾기
dd = pd.read_excel('drugdisease.xlsx')
def find(drug, disease):
    for k,v in ing.items():
        if(v==drug):
           # print(k,",",v)
            for v2 in dd.loc[k]:
                for v3 in disease:
                    if(v2==v3):
                        return ('부작용 유발 가능성');            
                    
                    
                    
ing = dd['Ingredient_nm']
disease=['급성 호흡부전','중증 골수장애'] #이미 있는 병
drug='Flunitrazepam' #새로 들어온 약

#print(find(drug,disease))
 

####약-약 부작용 ####
dd1 = pd.read_excel('데이터 완성본1.xlsx')
dd2 = pd.read_excel('데이터 완성본2.xlsx')
newdd = pd.merge(dd1,dd2,how='outer')

def find2(drug1,drug2):
        lst = newdd['조합']
        if lst[lst.str.contains(drug1)].str.contains(drug2).any():
            return('찾았다.')
            
            
#print(find2( 'atazanavir','simvastatin'))
        
          
###flask back-end####            
from flask import Flask,render_template,request
from werkzeug.utils import secure_filename
app=Flask(__name__)

@app.route('/uploading')
def render_file():
    return render_template('uploading.html')

@app.route('/uploaded',methods=['Get','POST'])
def upload_file():
    if request.method == 'POST':
        f=request.files['file']
        f.save('C:/Users/EUNHANJO/Flask_test/uploaded/'+secure_filename(f.filename))
        return '전송 완료 되었습니다.'


import os
path_dir='C:/Users/EUNHANJO/Flask_test/uploaded'
file_list=os.listdir(path_dir)

for item in file_list:
    newimage=item;
    #print(newimage)
    str=path_dir+"/"
    str+=newimage
    txt= (find_dr(finding_letters2(str)))
#txt=(find_dr(finding_letters2(str)))        
    


@app.route('/result')
def resulting():
    return txt


if __name__=='__main__':
    app.run()
  



import os
path_dir='C:/Users/EUNHANJO/Flask_test/uploaded'
file_list=os.listdir(path_dir)

for item in file_list:
    newimage=item;
    #print(newimage)
    str=path_dir+"/"
    str+=newimage
    txt= (find_dr(finding_letters2(str)))
#txt=(find_dr(finding_letters2(str)))        
    

"""



import pyrebase


config = {
        "apiKey": "AIzaSyBpDKyTUOJReyY4XwRXQO5tGErozaDUqRg",
        "authDomain": "wncw-f04a4.firebaseapp.com",
        "databaseURL": "https://wncw-f04a4.firebaseio.com",
        "projectId": "wncw-f04a4",
        "storageBucket": "wncw-f04a4.appspot.com",
        "messagingSenderId": "666230885447",
        "appId": "1:666230885447:web:e53f247f0e8111f8f47562",
        "measurementId": "G-8QF76CVY7K"

}


firebase = pyrebase.initialize_app(config)

db = firebase.database()

db.child("guest").child("0").update({"drug": find_dr(finding_letters2(image)) })
"""