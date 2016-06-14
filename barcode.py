# import the necessary packages
import numpy as np
import argparse
import cv2
 
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "path to the image file")
ap.add_argument("--Folder" , help = "path to store extracted barcode")
args = vars(ap.parse_args())

# load the image and convert it to grayscale
image = cv2.imread(args["image"])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
rows,cols = gray.shape
(_, thresh) = cv2.threshold(gray, 100,255, cv2.THRESH_BINARY_INV)
#thresh = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,7,2)
#cv2.imwrite('thresh.jpeg' , thresh)
width = 20;

# construct a closing kernel and apply it to the thresholded image

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1 , width/2 + 1))
E = cv2.erode(thresh, kernel, iterations = 1)
#cv2.imwrite('eroded.jpeg' , E)
kernel2 = cv2.getStructuringElement(cv2.MORPH_RECT, (8 , width/2 + 1))
#kernel3 = cv2.getStructuringElement(cv2.MORPH_RECT, (2 , 10))
D = cv2.dilate(E, kernel2, iterations = 2)

#cv2.imwrite('output.jpeg' , D)
#gradient = cv2.subtract(D , E);
#(_, thresh) = cv2.threshold(gradient, 100,255, cv2.THRESH_BINARY)
#opened = cv2.morphologyEx(gradient, cv2.MORPH_OPEN, kernel)
#eroded = cv2.erode(gradient, kernel, iterations = 1)

(cnts, _) = cv2.findContours(D.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
#print cnts

c = sorted(cnts, key = cv2.contourArea, reverse = True)
x , y, w , h = cv2.boundingRect(c[0])

count = 0

for index in range(0 , len(c) ):
	
	x , y, w1 , h1 = cv2.boundingRect(c[index])
	
	if(cv2.contourArea(c[index]) > 0.25*w*h and (w1 >  h1)):
		roi = image[y:y+h1, x:x+w1]
		exec("name = 'barcode%d.png'"%( count+1 ));
	
		cv2.imwrite(args["Folder"]+"/"+name, roi)
		
		count = count + 1;
		




# compute the rotated bounding box of the largest contour
#for index in range(0, count):
	#x, y, width, height = cv2.boundingRect(c[index])
#rect = cv2.minAreaRect(c)
#print rect
	#roi = image[y:y+height, x:x+width]
	#exec("name = 'barcode%d.png'"%( index+1 ));
	
	#cv2.imwrite(name, roi)



#cv2.imwrite('output.jpeg' , opened)



# Vertical barcode


M = cv2.getRotationMatrix2D((cols/2,rows/2),-90,1)
image = cv2.warpAffine(image,M,(cols,rows))
gray = cv2.warpAffine(gray,M,(cols,rows))

thresh = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,7,2)
#cv2.imwrite('thresh.jpeg' , thresh)
width = 20;

# construct a closing kernel and apply it to the thresholded image

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1 , width/2 + 1))
E = cv2.erode(thresh, kernel, iterations = 1)
#cv2.imwrite('eroded.jpeg' , E)
kernel2 = cv2.getStructuringElement(cv2.MORPH_RECT, (8 , width/2 + 1))
#kernel3 = cv2.getStructuringElement(cv2.MORPH_RECT, (2 , 10))
D = cv2.dilate(E, kernel2, iterations = 2)

#cv2.imwrite('output.jpeg' , D)
#gradient = cv2.subtract(D , E);
#(_, thresh) = cv2.threshold(gradient, 100,255, cv2.THRESH_BINARY)
#opened = cv2.morphologyEx(gradient, cv2.MORPH_OPEN, kernel)
#eroded = cv2.erode(gradient, kernel, iterations = 1)

(cnts, _) = cv2.findContours(D.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
#print cnts

c = sorted(cnts, key = cv2.contourArea, reverse = True)
x , y, w , h = cv2.boundingRect(c[0])



for index in range(0 , len(c) ):
	
	x , y, w1 , h1 = cv2.boundingRect(c[index])
	
	if(cv2.contourArea(c[index]) > 0.25*w*h and (w1 >  h1)):
		roi = image[y:y+h1, x:x+w1]
		exec("name = 'barcode%d.png'"%( count+1 ));
	
		cv2.imwrite(args["Folder"]+"/"+name, roi)
		
		count = count + 1;
		

print "number of barcodes detectected: %d"%(count)



