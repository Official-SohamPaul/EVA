from Tools.speechRecogOnline import *
from Tools.computerVoice import *
# from Tools.predict_tool import predict_intent
from GenAI.gemini import *
from Automation.automateYouTube import SearchYouTube
from Automation.automateGoogleSearch import SearchGoogle
from random import choice
import cv2
import pickle
from FaceRecognition import detect_face
from FaceRecognition import faceRecog
from ObjectDetection import objects_detection
  

#import dependancy

import wikipedia
import webbrowser,keyboard
import datetime
import os
import time
import requests



limitation_responses=('I can not understand what did you say','sorry I can not understand','due to code limitation, I can not perform this','sorry, it is byond my code limitation','sorry I am unable to do so','sorry I am bound with code limitation to perfrom this task','I think this task is out of my hand')

class ComputerAssistant:
    youtube_obj=SearchYouTube() 
    google_obj=SearchGoogle()
    assistant_name='eva'

    def makeDecision(self,voice,query):
        if query != None and query!='':
            sw=True
            if 'hello' in query or self.assistant_name in query or f'hey {self.assistant_name}' in query:
                    speak(voice,'Yes , How can I help you ?')

            elif 'good night' in query:
                    speak(voice,'good night sir. Anythings else ?')
                    q=recognize()
                    if 'no' in q or 'nothing' in q:
                        speak(voice,'Okay. Thank You.')
                        sw=False

            elif 'your name' in query or 'about yourself' in query:
                speak(voice,choice([f'My name is {self.assistant_name}, I am a desktop assitant. I can perform many tasks like search, automate as well as generating text, detecting faces or objects. I am developed by Soham on 2024',f'my name is {self.assistant_name}, I am a desktop assistant. How may I assist you today?',f'I\'m {self.assistant_name}, a desktop assistant, I can assist you from searching something on youtube or google to detecting objects ']))


            elif 'search on wikipedia' in query:
                    speak(voice,'Searching Wikipedia...')
                    query = query.replace("search on wikipedia about", "")
                    results = wikipedia.summary(query, sentences = 3)
                    try :
                        speak(voice,"According to Wikipedia")
                        print(results)
                        speak(voice,results) 
                    except wikipedia.exceptions.PageError:
                        speak(voice,f"I am sorry but I can not find any pages related with {query} on Wikipedia")
                    
            elif 'youtube' in query:
                trash_words=('play','about','song',' on','youtube','open',' in','and')
                for word in trash_words: query=query.replace(word,'')
                if query!='' or query!=None:
                    self.youtube_obj.open_youtube(query)
                                                
                    
            elif 'gemini' in query or 'generate' in query or 'AI' in query:
                    try:
                        speak(voice,generate_text(query.replace('gemini','').replace('generate','').replace('ai','')))
                    except TypeError:
                        speak(voice,choice(('Yes, I am listening you','gemini is here','Yes,','yes how can I help you?')))
                        q=recognize()
                        if q.replace('gemini','') is not None:
                            speak(voice,generate_text(q.replace('gemini','')))
                        else:
                            speak(voice,'sorry, I can not get you')

            elif 'google' in query:
                trash_words=('open','google','search','about',' in','and')
                for word in trash_words: query=query.replace(word,'')
                if query!='' or query!=None:
                    speak(voice, choice(('Here you go','Opening google','searching on google','Ok opening google','ok got it')))
                    self.google_obj.search_on_google(query)
                    

            elif 'play music' in query or "play song" in query:
                    speak(voice,"Here you go with music")
                    music_dir = "C:/Users/ASUS/Music"
                    # music_dir=""
                    # ?????????????????????????????????????????????????????????????????????????????
                    songs = os.listdir(music_dir)    
                    os.startfile(os.path.join(music_dir, choice(songs)))

            elif 'open' in query and ('.com' in query or '.in' in query or '.org' in query):
                trash_word=('open','in','browser','chrome',' ')
                for word in trash_word: query=query.replace(word,'')
                speak(voice,choice((f'opening {query}',f'ok, opening {query} in browser',f'here you go to {query}','ok opening browser')))
                webbrowser.open(query)
                while True:
                    time.sleep(0.2)
                    q=recognize()
                    if q != None and q !='' :
                        if 'close' in q or 'exit' in q:
                            keyboard.press('ctrl+w')
                            break
                        else:
                            # speak(voice,choice(limitation_responses))
                            self.makeDecision(voice,q)
        
            elif 'the time' in query:
                    # if str(datetime.datetime.now().strftime('%p')) is 'AM':
                    strTime=str(datetime.datetime.now().strftime('%I:%M:%S %p'))
                    speak(voice,choice((f"the time is {strTime} now",f'current time is {strTime}',f'it is now {strTime}')))
            
            elif 'date' in query:
                day_month_year=str(datetime.datetime.now().strftime('%dth %B %Y'))
                speak(voice,f'today is {day_month_year}')
                     
            elif 'week day' in query or 'today' in query:
                 weekday=str(datetime.datetime.now().strftime('%A'))
                 speak(voice,f'today is {weekday}')

            elif 'guess my name' in query or 'what is my name' in query or 'do you remember me' in query or 'my name' in query:
                lookAhead=0
                detected=False
                dataLists=None
                cap=cv2.VideoCapture(CAM_ID)
                _,img=cap.read()
                
                with open('./FaceRecognition/faceEncodingsData.p','rb') as file:
                    dataLists=pickle.load(file)

                
                
                while not detected or lookAhead:
                    _,img=cap.read()
                    detected,known_info,stranger_info=detect_face.faceRecognition(img,dataLists)
                    lookAhead+=1
                    # Wait 2sec to detect for a face
                    if lookAhead==2*cap.get(cv2.CAP_PROP_FPS) or detected:
                        cap.release()
                        break

                if detected:
                    frame=img.copy()
                    persons=''

                    for name in known_info:
                        persons+=(' '+name[0]+',')
                        
                        frame=detect_face.draw_boundbox(frame,name[0],name[1])
                    if persons!='':
                        speak(voice,choice(['I know, you are','I remember you','I guess you are','your name is'])+persons)
                        cv2.imshow('Faces',frame)
                        cv2.waitKey(5000)
                    
                        # print(name[0]) 

                    for stranger in stranger_info:
                        frame=img.copy()
                        frame=detect_face.draw_boundbox(frame,' Name ?',stranger[1])
                        cv2.imshow('Detected Faces',frame)
                        
                        speak(voice,'I cannot remember this person. What is the name of this person?')

                        name=recognize()
                        while not name:
                            name=recognize()
                            cv2.imshow('Detected Faces',frame)
                            cv2.waitKey(1)
                        

                        if 'no' in name or 'not' in name:
                            speak(voice,'Ok')
                        else :
                            trash_words=['he','is','she','her','name','his','the','person']
                            for trash in trash_words:
                                name.replace(trash,'')
                            speak(voice,f'so the name of this person is {name}. shall I proceed register?')

                            reply=recognize()
                            while not reply:
                                reply=recognize()
                                cv2.imshow('Detected Faces',frame)
                                cv2.waitKey(1)
                            if 'yes' in reply:
                                if detect_face.register_face(img,stranger[1],name):
                                    speak(voice,f'{name} is registered successfully')
                            else:
                                speak(voice,'Ok. command me to retry detecting faces')
                    cv2.destroyAllWindows()
                            
                else:
                    #'I cannot see faces'
                    speak(voice,'May be I cannot detect any faces or detected very blurry face. Here it is')
                    cv2.imshow('Undetected_frame',img)
                    cv2.waitKey(2000)
                    cv2.destroyAllWindows()

            elif 'encode images' in query:
                speak(voice,choice(['encoding started','encoding started, it may take some time','encoding the images']))
                detect_face.encode_images('./FaceRecognition/registered_faces')
                speak(voice,'encoding completed')

            elif 'register me' in query or 'register my face' in query:
                lookAhead=0
                detected=False
                img=None
                cap=cv2.VideoCapture(CAM_ID)
                
                with open('./FaceRecognition/faceEncodingsData.p','rb') as file:
                    dataLists=pickle.load(file)
                
                
                while not detected or lookAhead:
                    _,img=cap.read()
                    detected,known_info,stranger_info=detect_face.faceRecognition(img,dataLists)
                    lookAhead+=1
                    # Wait 5sec to detect for a face
                    if lookAhead==5*cap.get(cv2.CAP_PROP_FPS) or detected:
                        cap.release()
                        break

                if detected and stranger_info:
                    for stranger in stranger_info:
                        frame=img.copy()
                        frame=detect_face.draw_boundbox(frame,' Name ?',stranger[1])
                        cv2.imshow('Register',frame)
                        speak(voice,'What is your full name?')
                        answer=recognize()
                        while not answer and answer !='':
                            cv2.imshow('Register',frame)
                            answer=recognize()
                            cv2.waitKey(1)
                        
                        if 'no' in answer or 'not mine' in query:
                            speak(voice,'ok fine')
                            
                        else:
                            trashes=['my','name','is','i','am']
                            for trash in trashes: answer.replace(trash,'')
                            speak(voice,choice([f'is your name is {answer}?',f'confirm your name as {answer}?',f'so the name of this person is {answer}. shall I proceed register?']))
                            reply=None
                            while not reply and reply!='':
                                reply=recognize()
                            
                            if 'yes' in reply or 'confirm' in reply:
                                if detect_face.register_face(img,stranger[1],answer):
                                    speak(voice,f'{answer} is registered successfully')
                                else:
                                    speak(voice,'Something went wrong')
                            else:
                                speak(voice,'please try again')
                        cv2.destroyAllWindows()

                elif detected and known_info:
                    persons=''
                    for known_person in known_info:
                        persons+=(' '+known_person[0].split(' ')[0]+',')
                    speak(voice,choice([f'Hey! I know you {persons} are you kidding me?',f'are you kidding me {persons} ?']))
                    
                elif not detected:
                    speak(voice,'image is very blurry or no person is detected')


            elif 'face recognition' in query:
                cap=cv2.VideoCapture(CAM_ID)
                
                speak(voice,'press Escape button to exit')
                with open('./FaceRecognition/faceEncodingsData.p','rb') as file:
                    dataLists=pickle.load(file)
                while True:
                    _,img=cap.read()
                    frame=faceRecog.faceRecognition(img,dataLists)
                    cv2.imshow('Face Recognition',frame)
                    if cv2.waitKey(1)==27:
                        break
                
                cv2.destroyAllWindows()
                cap.release()


            elif 'object detection' in query:
                cap=cv2.VideoCapture(CAM_ID)
                speak(voice,'press Escape button to exit')
                while True:
                    _,img=cap.read()
                    frame,visuals=objects_detection.detect_objects(img)
                    cv2.imshow('Object_Detection',frame)
                    if cv2.waitKey(1)==27:
                        break
                
                cv2.destroyAllWindows()
                cap.release()

            elif 'detect object' in query or 'how many object' in query:
                cap=cv2.VideoCapture(CAM_ID)
                _,img=cap.read()
                
                frame,visuals=objects_detection.detect_objects(img)

                # Wait for detecting object for 2Sec
                lookAhead=0
                while len(visuals)==0:
                    _,img=cap.read()
                    frame,visuals=objects_detection.detect_objects(img)
                    lookAhead+=1
                    if lookAhead>cap.get(cv2.CAP_PROP_FPS)*2:
                        break

                if len(visuals)>0:
                    speech=''
                    for visual in visuals:
                        if visuals[visual][0]>1:
                            speech=speech+' '+str(visuals[visual][0])+' '+visual+'s ,'
                        else:
                            speech=speech+' '+str(visuals[visual][0])+' '+visual+' ,'

                    speak(voice,'I can see {}'.format(speech))
                    cv2.imshow('Detected_Object',frame)
                    cv2.waitKey(2000)
                    cv2.destroyAllWindows()
                    cap.release()
                else:
                    speak(voice,'I cannot detect objects It may be I dont know the objects or here has not enough light to detect')
                    cv2.imshow('Object_detection',frame)
                    cv2.waitKey(2000)
                    cv2.destroyAllWindows()
            
            else:
                speak(voice,choice(limitation_responses))

            return sw


    def quit_assistance(self):
        self.youtube_obj.destroy_session()
        self.google_obj.destroy_session()
        cv2.destroyAllWindows()

    def map_timmings(self,timmings):
        if int(timmings) in list(range(4,12)):
            return 'morning'
        elif int(timmings) in list(range(12,17)):
            return 'afternoon'
        elif int(timmings) in list(range(17,19)):
            return 'evening'
        elif int(timmings) in range(0,4) or int(timmings) in range(19,24):
            # return 'night'
             return 'evening'


    def main(self):
        
        #setting up voice as female
        voice=createTone(150,1.0,1)
        timmings=self.map_timmings(datetime.datetime.now().strftime('%H'))

        
        with open('./FaceRecognition/faceEncodingsData.p','rb') as file:
            dataLists=pickle.load(file)
        # isDetected,persons_info,stranger_info=detect_face.faceRecognition(img,dataLists)

        cap=cv2.VideoCapture(CAM_ID)
        wait=0
        isDetected=False
        while not isDetected or wait:
            _,img=cap.read()
            isDetected,persons_info,stranger_info=detect_face.faceRecognition(img,dataLists)
            wait+=1
            # Wait 2sec to detect for a face
            if wait==2*cap.get(cv2.CAP_PROP_FPS) or isDetected:
                cap.release()
                break
        
        name=''
        if isDetected:
            for person in persons_info:
                name=name+' '+person[0].split(' ')[0]
                
        speak(voice,f'Good {timmings}{name}!')
        
        ''' Checking For Internet Connection '''
        connectedToInternet=False
        connectionTimeout=0
        while not connectedToInternet:
            try:
                request=requests.get('https://www.google.com/',timeout=3)
                connectedToInternet=True
                connectionTimeout=0
            except (requests.ConnectionError,requests.Timeout):
                speak(voice,choice(['Plese Ensure the internet connection','please connect the device with internet','configure internet connection','please ensure the device is properly connected to internet']))
                time.sleep(5)
                connectionTimeout+=1
                if connectionTimeout>5:
                    break

        if connectedToInternet:
            switch=True
            asking_responses=("How can I assist you?", 
                            "Hey! What can I do for you?", 
                            "What brings you here?", 
                            "How may I help you?", 
                            "How can I be of service?", 
                            "What do you need assistance with?", 
                            "How may I assist you?", 
                            "How can I help?", 
                            "What's on your mind?", 
                            "How can I assist you today?",
                            "Please share your request, and I'll see how I can assist you effectively.",
                            'Please let me know how can i help you ?',
                            'How may I help you ?')
            
            speak(voice,choice(asking_responses))

            while switch:
                query=''
                query=recognize()
                if query!=None and 'exit' in query:
                    speak(voice,'Happy to assist you today, Thank you!')
                    break
                elif query != None:
                    # indent,response =predict_intent(query)
                    # print(f'Machine Predicted:{indent}\nMachine Responsed: {response}')
                    switch=self.makeDecision(voice,query)

        else:
            speak(voice,'Sorry Internet connection is not established properly. Closing the assistance.')


CAM_ID=int(input('Computer: Enter your Camera ID: '))
assistant=ComputerAssistant()
try:
    assistant.main()
    assistant.quit_assistance()
except Exception as e:
    print('Exception:',e)
    assistant.quit_assistance()
