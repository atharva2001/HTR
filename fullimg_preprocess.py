import cv2
import argparse
import subprocess
import os
import re
import numpy as np
#import image

#cv2.imshow('orig',image)
#cv2.waitKey(0)
result = list()
parser = argparse.ArgumentParser(description='Provide image path')
parser.add_argument('img')
args = parser.parse_args()


def get_result(img):
    command = (f'python main.py --img_file {img}').split()
    process=subprocess.Popen(command,stdout=subprocess.PIPE,shell=True)

    process_out= process.communicate()[0]
    process_out=str(process_out)
    return process_out

def full_preprocessing(img_path):
    image = cv2.imread(img_path)
    #grayscale
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    # cv2.imshow('gray',gray)
    # cv2.waitKey(0)

    #binary
    ret,thresh = cv2.threshold(gray,127,255,cv2.THRESH_BINARY_INV)
    # cv2.imshow('second',thresh)
    # cv2.waitKey(0)

    #dilation
    kernel = np.ones((5,100), np.uint8)
    img_dilation = cv2.dilate(thresh, kernel, iterations=1)
    # cv2.imshow('dilated',img_dilation)
    # cv2.waitKey(0)

    #find contours
    ctrs,hier= cv2.findContours(img_dilation.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    #sort contours
    sorted_ctrs = sorted(ctrs, key=lambda ctr: cv2.boundingRect(ctr)[0])

    for i, ctr in enumerate(sorted_ctrs):
        # Get bounding box
        x, y, w, h = cv2.boundingRect(ctr)

        # Getting ROI
        roi = image[y:y+h, x:x+w]

        # show ROI
        # cv2.imshow('segment no:'+str(i),roi)
        name="segment_no_"+str(i)+".png"
        cv2.imwrite(name,roi)
        # os.path.join('/temp',name)
        # cv2.rectangle(image,(x,y),( x + w, y + h ),(90,0,255),2)
        cv2.waitKey(0)
        result.append(get_result(name))

    for i in result:
        temp = re.findall("\".*\"",i)
        # print(temp)
        for j in temp:
            print(j)
    # print(result)
    # cv2.imwrite('final_bounded_box_image.png',image)
    # cv2.imshow('marked areas',image)
    # cv2.waitKey(0)
#if __name__ == '__main__':
full_preprocessing(args.img)