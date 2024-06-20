import cv2
import face_recognition
import pickle
import os


# Creating classified Box
def draw_boundbox(img,name,box,color=(255,0,0)):
    x1,y1,x2,y2=box
    frame=cv2.rectangle(img,(x1-1,y1-30),(x2+1,y1),color,cv2.FILLED)
    frame=cv2.rectangle(frame,(x1,y1),(x2,y2),color,2)
    frame=cv2.putText(frame,' {}'.format(name),(x1,y1-10),cv2.FONT_HERSHEY_PLAIN,1.2,(255,255,255),1)
    # frame=cv2.putText(frame,'Gender: Male',(210,220),cv2.FONT_HERSHEY_PLAIN,1,(0,255,0),1)
    # frame=cv2.putText(frame,'Age: 22',(210,240),cv2.FONT_HERSHEY_PLAIN,1,(0,255,0),1)
    return frame

def encode_images(img_path):
    os.chdir(img_path)
    ids=[]
    names=[]
    encodings=[]
    listImg=os.listdir()
    for imgflie in (listImg) :
        if '.jpg' in imgflie or '.jpeg' in imgflie:  
            img=cv2.imread(imgflie)
            img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
            encode=face_recognition.face_encodings(img)[0]
            ids.append(os.path.splitext(imgflie)[0].split('.')[0])
            names.append(os.path.splitext(imgflie)[0].split('.')[1])
            encodings.append(encode)
    with open('../faceEncodingsData.p','wb') as file:     
        pickle.dump([ids,names,encodings],file)
        

def register_face(img,faceLocation,name):
    x1, y1,x2, y2=faceLocation
    face=img[y1-80:y2+40,x1-40:x2+40]
    reg_faces=os.listdir('./FaceRecognition/registered_faces')
    total_faces=len(reg_faces)
    lastID=int(reg_faces[total_faces-1].split('.')[0])
    fileName=f'{lastID//20}{lastID%20+1}.{name}.jpg'
    try:
        cv2.imwrite(f'./FaceRecognition/registered_faces/{fileName}',face)
        encode_images('./FaceRecognition/registered_faces')
        return True
    except FileExistsError:
        return False



def faceRecognition(img,dataLists):
    #initialization
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
    isDetected=False
    known_info=[]
    stranger=True
    stranger_number=0
    stranger_info=[]
    for faceLocation,curr_encoding in zip(faceLocations,curr_encodings):
        y1, x2, y2, x1= faceLocation
        isDetected=True
        matches=face_recognition.compare_faces(encodings,curr_encoding)
        # print(matches)
        for i in range (0,len(matches)):
            if matches[i]:
                box=[x1*4,y1*4,x2*4,y2*4]
                frame=draw_boundbox(frame,'{}'.format(names[i]),box,colorGreen)
                known_info.append([names[i],box])
                stranger=False
        
        if stranger:
            stranger_number+=1
            box=[x1*4,y1*4,x2*4,y2*4]
            frame=draw_boundbox(frame,f'Stranger {stranger_number}',box,colorRed)
            stranger_info.append([stranger_number,box])

    return isDetected,known_info,stranger_info

# Driver code
# cap=cv2.VideoCapture(0)
# _,img=cap.read()
# with open('./FaceRecognition/faceEncodingsData.p','rb') as file:
#     dataLists=pickle.load(file)
# isDetected,frame,known_info,srtanger_info=faceRecognition(img,dataLists)
# cv2.imshow('frame',frame)
# cv2.waitKey(0)
# cap.release()

# encode_images('./registered_faces')

