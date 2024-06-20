from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import random
import time
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.action_chains import ActionChains

from Tools.speechRecogOnline import recognize
from Tools.computerVoice import *
voice=createTone()

limitation_responses=('due to code limitation, I can not perform this','sorry, it is byond my code limitation','sorry I am unable to do so','sorry I am bound with code limitation to perfrom this task','I think this task is out of my hand')



class SearchYouTube:
    web_URL='https://www.youtube.com'
    driver=webdriver.Chrome()

    __all__={
        'open_youtube',
        'search_on_youtube',
        'close_window',
        'destroy_session',
        'back_page',
        'refresh_page',
        'next_video',
        'pause_play_video',
        'skip_ads',
        'volume_up',
        'volume_down',
        'mute',
        'fullscreen',
        'subtitles'
    }
    def __init__(self):
        self.driver.minimize_window()
        
    
    volume=20
    pages_visited=0

    def open_youtube(self,query:str):
        speak(voice, random.choice(('Here you go','Opening youtube','here you go to youtube','Ok opening youtube')))
        self.driver.get(self.web_URL)
        self.driver.maximize_window()
        self.driver.implicitly_wait(1)
        self.pages_visited+=1
        while True:
            time.sleep(0.5)
            #code for voice assisted close
            
            if query != None and query != '':
                
                if 'close' in query or 'stop' in query:
                    self.close_window()
                    break
                elif 'skip' in query:
                    self.skip_ads()
                elif 'next' in query:
                    self.next_video()
                elif 'pause' in query or 'play' in query:
                    self.pause_play_video()
                elif 'volume up' in query:
                    self.volume_up()
                elif 'volume down' in query:
                    self.volume_down()
                elif 'mute' in query or 'unmute' in query:
                    self.mute()
                elif 'full screen' in query:
                    self.fullscreen()
                elif 'subtitles' in query:
                    self.subtitles()
                elif 'back' in query:
                    self.back_page()
                elif 'scroll up' in query:
                    self.scroll_up()
                elif 'scroll down' in query:
                    self.scroll_down()
                elif 'search' in query:
                    self.search_on_youtube(query.replace('search',''))
                else:
                    # speak(voice,random.choice(limitation_responses))
                    pass
                    
                    

            query=recognize()

    def search_on_youtube(self,query:str):
               
        if query!=None and query!='':
            self.driver.maximize_window()
            self.driver.find_element(By.XPATH,'//*[@id="search-form"]').click()
            time.sleep(2)
            search=self.driver.find_element(By.NAME,'search_query')
            search.clear()
            search.send_keys(query)
            search.send_keys(Keys.ENTER)
            time.sleep(2)
            self.driver.find_element(By.XPATH,'//*[@id="video-title"]/yt-formatted-string').click()
            self.pages_visited+=1

    def skip_ads(self):
        try: self.driver.find_elements(By.CLASS_NAME,'"ytp-ad-skip-button-modern').click()
        except Exception:
            speak(voice,random.choice(('skipping ads is not avaliable','skip ads is unavaliable','at first play a video','this option is not avaliable','option is unreachable','this option is unavaliable')))
            print(Exception)              


    def close_window(self):
        speak(voice,random.choice(('closing this window','exiting the window','ok closing','got it','ok it is closing now')))
        self.driver.minimize_window()
        for i in range(0,self.pages_visited+1):self.driver.back() 
        self.pages_visited=0
        # while True:
        #     if (self.driver.current_url() in self.web_URL):
        #         self.driver.back()
        #     else:
        #         break
                
    def destroy_session(self):
        self.driver.close()
        self.driver.quit()
    
    def back_page(self):
        speak(voice,'returning to previous page')
        self.driver.back()
        self.pages_visited-=1
    
    def refresh_page(self):
        self.driver.refresh()
            
    def next_video(self):
        try:
            self.driver.find_element(By.CLASS_NAME,'ytp-next-button').click()
            self.pages_visited+=1
            speak(voice,'playing the next video')
        except Exception:
            speak(voice,random.choice(('next video is not avaliable','next video is unavaliable','at first play a video','this option is not avaliable','options are unreachable','this option is unavaliable')))
            print(Exception)

    def pause_play_video(self):
        try: self.driver.find_element(By.CSS_SELECTOR,'button.ytp-play-button').click()
        except Exception: 
            speak(voice,random.choice(('pause or play options are not avaliable','pause or play options are unavaliable','at first play a video','this option is not avaliable','options are unreachable','this option is unavaliable')))
            print(Exception)
    def volume_up(self):
        try:
            sound_button = self.driver.find_element(By.CLASS_NAME, 'ytp-mute-button')
            volume_panel = self.driver.find_element(By.CLASS_NAME, 'ytp-volume-panel')
            actions = ActionChains(self.driver)
            actions.move_to_element(sound_button)
            actions.move_to_element(volume_panel)
            actions.click_and_hold(volume_panel)
            if self.volume<=15: self.volume+=5
            else : self.volume=20
            actions.move_to_element_with_offset(volume_panel,self.volume, 0)
            actions.perform()
        except Exception: 
            speak(voice,random.choice(('volumn up is not avaliable','volumn up is unavaliable','at first play a video','this option is not avaliable','options are unreachable','this option is unavaliable')))
            print(Exception)

    def volume_down(self):
        try:
            sound_button = self.driver.find_element(By.CLASS_NAME, 'ytp-mute-button')
            volume_panel = self.driver.find_element(By.CLASS_NAME, 'ytp-volume-panel')
            actions = ActionChains(self.driver)
            actions.move_to_element(sound_button)
            actions.move_to_element(volume_panel)
            actions.click_and_hold(volume_panel)
            if self.volume>=-15: self.volume-=5
            else : self.volume=-20
            actions.move_to_element_with_offset(volume_panel,self.volume, 0)
            actions.perform()
        except Exception: 
            speak(voice,random.choice(('volumn down is not avaliable','volumn down is unavaliable','at first play a video','this option is not avaliable','options are unreachable','this option is unavaliable')))
            print(Exception)

    def scroll_up(self):
        for i in range(0,10):self.driver.find_element(By.XPATH,'/html').send_keys(Keys.ARROW_UP)
        

    def scroll_down(self):
        for i in range(0,10): self.driver.find_element(By.XPATH,'/html').send_keys(Keys.ARROW_DOWN)
        

    def mute(self):
        try: self.driver.find_element(By.CLASS_NAME,'ytp-mute-button').click()
        except Exception: 
            speak(voice,random.choice(('mute is not avaliable','mute is unavaliable','at first play a video','this option is not avaliable','options are unreachable','this option is unavaliable')))
            print(Exception)

    def fullscreen(self):
        try: self.driver.find_element(By.CLASS_NAME,'ytp-fullscreen-button').click()
        except Exception: 
            speak(voice,random.choice(('fullscreen is not avaliable','fullscreen is unavaliable','at first play a video','this option is not avaliable','options are unreachable','this option is unavaliable')))
            print(Exception)

    def subtitles(self):
        try: self.driver.find_element(By.CLASS_NAME,'ytp-subtitles-button').click()
        except Exception : 
            speak(voice,random.choice(('subtitles is not avaliable','subtitles is unavaliable','at first play a video','this option is not avaliable','options are unreachable','this option is unavaliable')))
            print(Exception)


# TEST
# obj=SearchYouTube()
# obj.open_youtube('search tumi jake valobaso')
# obj.destroy_session
