import numpy as np
import cv2

path = '/some/path'

cap = cv2.VideoCapture(path)

# take first frame of the video
ret,frame = cap.read()
frame=cv2.flip(frame,0)
# setup initial location of window
r,h,c,w = 250,90,450,125  # simply hardcoded the values
track_window = (c,r,w,h)
# define the codec and create a VideoWriter OBJECTS
#fourcc=cv2.VideoWriter_fourcc(*'DIVX')
#output=cv2.VideoWriter('T_in_Vid.avi',fourcc,30.0,(640,480))
# set up the ROI for tracking
roi = frame[r:r+h, c:c+w]
hsv_roi =  cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv_roi, np.array((62., 100.,100.)), np.array((82.,255.,255.)))

roi_hist = cv2.calcHist([hsv_roi],[0],mask,[180],[0,180])
cv2.normalize(roi_hist,roi_hist,0,255,cv2.NORM_MINMAX)

# Setup the termination criteria, either 10 iteration or move by atleast 1 pt
term_crit = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1 )
c=0
while(1):
    ret ,frame = cap.read()

    if ret == True:
        frame=cv2.flip(frame,0)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        dst = cv2.calcBackProject([hsv],[0],roi_hist,[0,180],1)

        # apply meanshift to get the new location
        ret, track_window = cv2.meanShift(dst, track_window, term_crit)

        # Draw it on image
        x,y,w,h = track_window
        img2 = cv2.rectangle(frame, (x,y), (x+w,y+h), 255,2)
        cv2.imshow('img2',img2)
#        output.write(frame)
        #cv2.imwrite('img'+str(c)+'.jpg',img2)
        k = cv2.waitKey(25) & 0xff
        if k == 27:
            break
        #c+=1
    else:
        break

cv2.destroyAllWindows()
#output.release()
cap.release()
