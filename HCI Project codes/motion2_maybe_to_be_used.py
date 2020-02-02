import cv2
import numpy as np
import time
import datetime
def main():
   #window_name="Cam feed"
   #cv2.namedWindow(window_name)
   cap=cv2.VideoCapture(0) # value (0) selects the devices default camera

   #filename = 'F:\sample.avi'
   #codec=cv2.VideoWriter_fourcc('X','V','I','D')
   #framerate=30
   #resolution = (500,500)

 #  VideoFileOutput = cv2.VideoWriter(filename,codec,framerate,resolution)

   
   if cap.isOpened():
      
      ret,frame = cap.read()

   else:
      ret =False

   ret,frame1 = cap.read()
   ret,frame2 = cap.read()

   while ret:
      
      ret,frame = cap.read()
      #VideoFileOutput.write(frame)
      text = 'Unoccupied'

      d=cv2.absdiff(frame1,frame2)

      grey=cv2.cvtColor(d,cv2.COLOR_BGR2GRAY)

      blur =cv2.GaussianBlur(grey,(5,5),0)
      ret,th=cv2.threshold(blur,20,255,cv2.THRESH_BINARY)
      dilated=cv2.dilate(th,np.ones((3,3),np.uint8),iterations=3)
      cnt,h=cv2.findContours(dilated , cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)[-2:]
      # contours gives 3 diffrent ouputs image, contours and hierarchy, so using [1] on end means contours = [1](cnt)
        # cv2.CHAIN_APPROX_SIMPLE saves memory by removing all redundent points and comppressing the contour, if you have a rectangle
        # with 4 straight lines you dont need to plot each point along the line, you only need to plot the corners of the rectangle
        # and then join the lines, eg instead of having say 750 points, you have 4 points.... look at the memory you save!
      for c in cnt:
         if cv2.contourArea(c) > 1000: # if contour area is less then 1000 non-zero(not-black) pixels(white)
             (x, y, w, h) = cv2.boundingRect(c) # x,y are the top left of the contour and w,h are the width and hieght 

             cv2.rectangle(frame1, (x,y), (x+w, y+h), (0, 255, 0), 2) # (0, 255, 0) = color R,G,B = lime / 2 = thickness(i think?)(YES IM RITE!)
             # image used for rectangle is frame so that its on the secruity feed image and not the binary/threshold/foreground image
             # as its already used the threshold/(binary image) to find the contours this image/frame is what image it will be drawed on
             cv2.drawContours(frame1,c,-1,(0,255,0),2)

             text = 'Occupied'
             # text that appears when there is motion in video feed
         else:
             pass

         cv2.putText(frame1, '{+} Room Status: %s' % (text), (10,20), cv2.FONT_HERSHEY_SIMPLEX , 0.5, (0, 0, 255), 2)
        # frame is the image on wich the text will go. 0.5 is size of font, (0,0,255) is R,G,B color of font, 2 on end is LINE THICKNESS! OK :)
         cv2.putText(frame1, datetime.datetime.now().strftime('%A %d %B %Y %I:%M:%S%p'), (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX , 0.35, (0, 0, 255),1) 
        # frame.shape[0] = hieght, frame.shape[1] = width,ssssssssssssss
        # using datetime to get date/time stamp, for font positions using frame.shape() wich returns a tuple of (rows,columns,channels)
        # going 10 accross in rows/width so need columns with frame.shape()[0] we are selecting columns so how ever many pixel height 
        # the image is - 10 so oppisite end at bottom instead of being at the top like the other text
      #cv2.imshow("win1",frame2)
      cv2.imshow("inter",frame1)
      
      
      if cv2.waitKey(40) == 27:
         break
      frame1 = frame2
      ret,frame2 = cap.read()
      key = cv2.waitKey(1) & 0xFF # (1) = time delay in seconds before execution, and 0xFF takes the last 8 bit to check value or sumin
      if key == ord('q'):
        cv2.destroyAllWindows()
        break
   #VideoFileOutput.release()
   #cap.release()
main()   
    