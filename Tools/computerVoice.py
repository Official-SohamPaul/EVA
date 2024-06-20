import pyttsx3
        
def createTone(changeRate:int=150,changeVolume:float=1.0,changeVoice:bool=1) :
    #Object Creation
    voiceEngine= pyttsx3.init()
        
    # RATE
    rate=voiceEngine.getProperty('rate')
    print('The Rate is set To %d'%changeRate)
    voiceEngine.setProperty('rate',changeRate)

    # VOLUME
    volume=voiceEngine.getProperty('volume')
    # set Volumn in between 0 and 1, minVolumn=0 and maxVolumn=1
    print('Currrent volume is set To %1.1f...'%changeVolume)
    voiceEngine.setProperty('volume',changeVolume)
    
    # VOICE
    voices=voiceEngine.getProperty('voices')
    #voices[0].id for male and voices[1].id for female
    print('Set to Female voice...') if changeVoice else print('Set to Male voice...')
    voiceEngine.setProperty('voice',voices[changeVoice].id) 
    
    return voiceEngine
    
def speak(voiceEngine,text:str) :
    print('\nComputer : '+text)
    voiceEngine.say(text)
    voiceEngine.runAndWait()

#TEST       
"""audio=createTone(150,1.0,1)
speak(audio,"Hello Mr Soham Paul. How are you?")"""