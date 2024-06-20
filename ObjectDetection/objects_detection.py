from ultralytics import YOLO
import cv2

model=YOLO('./ObjectDetection//Models/yolov8n.pt')

def detect_objects(img):

    frame=img.copy()
    results=model.predict(frame,conf=0.6,verbose=False)

    visual_info={}
    for result in results:
        
        for box in result.boxes:
            classes=box.cls
            class_name = result.names[classes.item()]
            confidence='%.2f'%box.conf.tolist()[0]

            # output processing
            x1,y1,x2,y2=[int(points) for points in box.xyxy.tolist()[0]]
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255, 0), 2)
            cv2.rectangle(frame, ((x1-1), (y1-25)), ((x2+1), y1), (0,255, 0), -1)
            cv2.putText(frame,f'{class_name}',(x1, (y1-7)),cv2.FONT_HERSHEY_COMPLEX,0.75,(255,255,255),1)
            cv2.putText(frame,f'conf: {confidence}',((x1+5), (y1+25)),cv2.FONT_HERSHEY_COMPLEX,0.5,(0,0,255),1)

            if class_name not in visual_info:
                visual_info[class_name]=[1,(x1,y1,x2,y2)]
            else :
                visual_info[class_name]=[visual_info[class_name][0]+1,(x1,y1,x2,y2)]
            
        
    return frame,visual_info
    
# Driver Code
# cap=cv2.VideoCapture(1)
# while True:
#     _,img=cap.read()
#     frame,vision=detect_objects(img)
#     cv2.imshow('Window',frame)
#     print(vision)

#     if cv2.waitKey(1) & 0xFF == ord("q"):
#         break