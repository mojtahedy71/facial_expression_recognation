import cv2
import sqlite3 as lite
import os.path

def create_or_open_db(db_file):
    db_is_new = not os.path.exists(db_file)
    conn = lite.connect(db_file)
    if db_is_new:
        print 'Creating schema'
        sql = '''create table if not exists PICTURES(
        
        PICTURE BLOB,
        EMOTION TEXT
        );'''
        conn.execute(sql) # shortcut for conn.cursor().execute(sql)
        conn.commit()
    else:
        print 'Schema exists\n'
    return conn


def resize(img):
    width = 200
    height = 250   
    resized_image = cv2.resize(img, (width, height))
    return resized_image
    

def detect_feature(path):
    img = cv2.imread(path)
    cv2.imshow('img',img)
    cv2.waitKey()
    cascade = cv2.CascadeClassifier("C:\Python27\opencv\data\haarcascades\haarcascade_frontalface_alt.xml")
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    rects = cascade.detectMultiScale(img, 1.3, 4 )
    

    if len(rects) == 0:
        return [], img
    rects[:, 2:] += rects[:, :2]
    
    return rects, img


def box(rects, img):
    for x1, y1, x2, y2 in rects:
        
        cv2.rectangle(img, (x1, y1), (x2, y2), (127, 255, 0), 2)
        crop_img = img[y1:y2 , x1:x2]
        break
    im = resize(crop_img)
    cv2.imwrite('detected.jpg', im);
   # cv2.imshow('img2',crop_img)
   # cv2.waitKey()
    


def insert_picture(conn ,expression):
       
    sql = '''INSERT INTO PICTURES
    VALUES(?,?);'''
    im = open('detected.jpg','rb').read()
    
    cur=conn.cursor()
    cur.execute(sql,(lite.Binary(im), expression)) 
    conn.commit()

