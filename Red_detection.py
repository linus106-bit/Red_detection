import cv2
import numpy as np
import math


class FindNonZero:

    def wherecenter(height,width,img): #빨간색 물체의 중심을 찾는 함수 
        height_img = np.array([])
        first_width_img = np.array([])
        first_height_img = np.array([])
        bottom_img = np.array([])
        width_img = np.array([])

        center_x, center_y, length, count_img = 0,0,0,0

        for i in range(height): #y좌표 찾기
            for j in range(width):
                if img[int(i),int(j)]>0:
                    first_height_img = np.append(first_height_img, i)
                    first_width_img = np.append(first_width_img, j)
                    count_img += 1
                else:
                    pass
            if len(first_width_img) < 25:  #무시하는 코드 새로 추가
                first_width_img = np.array([])
                first_height_img = np.array([])
            else:
                width_img = np.append(width_img, first_width_img)
                height_img = np.append(height_img, first_height_img)
            

        try:
            if len(height_img) > 0:
                for i in range(int(height_img[0]),int(height)): #x좌표 찾기
                    if img[int(i),int(width_img[0])] > 0:
                        pass
                    else:
                        bottom_img = np.append(bottom_img, i)
                print("height: ",height_img)
                print("width: ",width_img)
                print("bottom: ",bottom_img)


                center_y= int((height_img[0]+bottom_img[0])/2)
                center_x= int(width_img[0])
                length = int((bottom_img[0]-height_img[0])/2)

                print("center's height: ",int((height_img[0]+bottom_img[0])/2))
                print("center's width: ",width_img[0])

                if width_img[0]>(width/2):
                    print("go left")
                if width_img[0]<(width/2):
                    print("go right")
                if width_img[0]==(width/2):
                    print("center")
        except IndexError:
            pass
        return center_x, center_y, length, count_img

cap = cv2.VideoCapture(0)

while(cap.isOpened()):
    ret, frame = cap.read()
    #frame = cv2.flip(frame,0)
    #frame = cv2.flip(frame,1)
    frame = cv2.resize(frame, dsize=(320, 240), interpolation=cv2.INTER_AREA)
    
    if(ret) :
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        height, width = frame.shape[:2] # 높이 너비
        
        # 빨간색은 hsv에서 0-10, 170-180 두개로 검출해야됨
        lower_red = cv2.inRange(hsv, (0,100,100), (5,255,255))
        upper_red = cv2.inRange(hsv, (175,100,100), (180,255,255))
        added_red = cv2.addWeighted(lower_red, 1.0 ,upper_red, 1.0, 0.0) # 합친거
        red = cv2.bitwise_and(frame, frame, mask= added_red) #마스크를 씌움
        h,s,v = cv2.split(red)  #채널 개수를 1개로 만듬

        center_x, center_y, length, size= FindNonZero.wherecenter(height, width, v)
        if size > 100:
            red = cv2.line(red,(center_x,center_y),(center_x,center_y),(0,255,0),3)
            red = cv2.rectangle(red, (center_x-length,center_y-length), (center_x+length,center_y+length), (0,255,0), 3)
        else:
            pass

        cv2.imshow("new_red",red)
        k = cv2.waitKey(1) & 0xFF
        if k == 27 :
            break
          
cap.release()
cv2.destroyAllWindows()
