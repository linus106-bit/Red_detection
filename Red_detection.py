import cv2
import numpy as np
import math


cap = cv2.VideoCapture(0)

class FindNonZero:
    def FindSize(height,width,img): #빨간색의 물체 크기(총 개수) 찾는 함수
        count_img = 0
        x_axis = np.array([])
        y_axis = np.array([])
        for i in range(width):
            for j in range(height):
                if img[int(j),int(i)] > 0:
                    count_img += 1
                else:
                    pass
        return count_img

    def wherecenter(height,width,img): #빨간색 물체의 중심을 찾는 함수 
        height_img = np.array([])
        width_img = np.array([])
        bottom_img = np.array([])
        for i in range(height): #y좌표 찾기
            for j in range(width):
                if img[int(i),int(j)]>0:
                    height_img = np.append(height_img, i)
                    width_img = np.append(width_img, j)
                else:
                    pass

        for i in range(int(height_img[0]),int(height)): #x좌표 찾기
            if img[int(i),int(width_img[0])] > 0:
                pass
            else:
                bottom_img = np.append(bottom_img, i)

        center_y=int((height_img[0]+bottom_img[0])/2)
        center_x=int(width_img[0])
        print("center's height: ",int((height_img[0]+bottom_img[0])/2))
        print("center's width: ",width_img[0])
        if width_img[0]>(width/2):
            print("go left")
        if width_img[0]<(width/2):
            print("go right")
        if width_img[0]==(width/2):
            print("center")
        return center_x, center_y


while(cap.isOpened()):
    ret, frame = cap.read()
    #frame = cv2.flip(frame,0)
    #frame = cv2.flip(frame,1)
    frame = cv2.resize(frame, dsize=(320, 240), interpolation=cv2.INTER_AREA)
    
    if(ret) :
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        height, width = frame.shape[:2] # 높이 너비
        
        # 빨간색은 hsv에서 0-10, 170-180 두개로 검출해야됨
        lower_red = cv2.inRange(hsv, (0,100,100), (3,255,255))
        upper_red = cv2.inRange(hsv, (178,100,100), (180,255,255))
        added_red = cv2.addWeighted(lower_red, 1.0 ,upper_red, 1.0, 0.0) # 합친거
        red = cv2.bitwise_and(frame, frame, mask= added_red) #마스크를 씌움
        h,s,v = cv2.split(red)  #채널 개수를 1개로 만듬
        center_x, center_y = FindNonZero.wherecenter(height, width, v)
        size = FindNonZero.FindSize(height, width, v)
        print("Size: ", size)
        red = cv2.line(red,(center_x,center_y),(center_x,center_y),(0,255,0),5)
        cv2.imshow("new_red",red)
        k = cv2.waitKey(1) & 0xFF
        if k == 27 :
            break
        
cap.release()
cv2.destroyAllWindows()