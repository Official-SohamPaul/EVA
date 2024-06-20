import cv2
import face_recognition

    


# Creating classified Box
def draw_boundbox(img,name,x1,y1,x2,y2,color=(255,0,0)):
    frame=cv2.rectangle(img,(x1-1,y1-30),(x2+1,y1),color,cv2.FILLED)
    frame=cv2.rectangle(frame,(x1,y1),(x2,y2),color,2)
    frame=cv2.putText(frame,' {}'.format(name),(x1,y1-10),cv2.FONT_HERSHEY_PLAIN,1.2,(255,255,255),1)
    # frame=cv2.putText(frame,'Gender: Male',(210,220),cv2.FONT_HERSHEY_PLAIN,1,(0,255,0),1)
    # frame=cv2.putText(frame,'Age: 22',(210,240),cv2.FONT_HERSHEY_PLAIN,1,(0,255,0),1)
    return frame

def faceRecognition(img,dataLists):
   
    colorRed=(0,0,250)
    colorGreen=(0,250,0)
    
    ids,names,encodings=dataLists
    frame=img.copy()

    # Detecting faces
    imgSmall=cv2.resize(src=img,dsize=(0,0),fx=0.25,fy=0.25)
    imgSmallRGB=cv2.cvtColor(imgSmall,cv2.COLOR_BGR2RGB)
    faceLocations=face_recognition.face_locations(imgSmallRGB)

    #classification
    curr_encodings=face_recognition.face_encodings(imgSmallRGB,faceLocations)
    known_persons=[]
    stranger=True
    for faceLocation,curr_encoding in zip(faceLocations,curr_encodings):
        y1, x2, y2, x1= faceLocation
        matches=face_recognition.compare_faces(encodings,curr_encoding)
        for i in range (0,len(matches)):
            if matches[i]:
                frame=draw_boundbox(frame,'{}'.format(names[i]),x1*4,y1*4,x2*4,y2*4,colorGreen)
                known_persons.append(names[i])
                stranger=False
        
        if stranger:
            frame=draw_boundbox(frame,'Stranger',x1*4,y1*4,x2*4,y2*4,colorRed)
        
        
    return frame
        
                
    

# encode_images()
# print('Computer: Total number of Registered Faces: ',len(encodings))
# faceRecognition()

