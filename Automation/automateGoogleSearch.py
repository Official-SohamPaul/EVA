from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from Tools.speechRecogOnline import recognize
from Tools.computerVoice import *

import random

from selenium.webdriver.common.action_chains import ActionChains
import time
#import dependancy
voice=createTone()


#browserPath='C:\Program Files\Google\Chrome\Application\chrome.exe'


class SearchGoogle:
    driver=webdriver.Chrome()
    website_URL='https://www.google.com/'
    page_count=0
   

    __all__={
         'search_on_google',
         'scroll_down',
         'scroll_up',
        #  'open_link',
        'close_window',
        'destroy_session',
        'back_page',
        'refresh_page',
        'maximize',
        'minimize'
    }

    def __init__(self):
        self.driver.minimize_window()

    def search_on_google(self,query:str):
        if query.lower() != None and query.lower() != '':
            self.driver.get(self.website_URL)
            self.driver.maximize_window()
            self.driver.implicitly_wait(1)
            try:
                search=self.driver.find_element(By.XPATH,'//*[@id="APjFqb"]')
                search.send_keys(query)
                search.send_keys(Keys.ENTER)
                while True:
                    time.sleep(0.2)
                    #code for voice assist
                    query=recognize()
                    if query != None and query != '':
                        if 'close' in query or 'exit' in query:
                            self.close_window()
                            break
                        elif 'scroll down' in query:
                            self.scroll_down()
                        elif 'scroll up' in query:
                            self.scroll_up()
                        elif 'search' in query:
                            q=query.replace('search','').replace('for','')
                            search=self.driver.find_element(By.XPATH,'//*[@id="APjFqb"]')
                            search.clear()
                            search.send_keys(q)
                            search.send_keys(Keys.ENTER)
                        elif 'open' in query :
                            query=query.replace('open','').replace('link','').replace('links','')
                            if query is not None or query == '':
                                speak(voice,random.choice((f'which link shoould I open ?','this link ?','are you want to open this link ?'))) 
                                q=recognize()
                                if q != None and q!='':
                                    self.open_link(q)
                            elif query!='' and query!= None:
                                self.open_link(query)
                            else:
                                speak(voice,random.choice(('please provide a webpage name','what is the webpage name','which website should I open?','tell me the website name')))     
                        elif 'reload' in query or 'refresh' in query:
                            self.refresh_page()
                        elif 'back' in query:
                            self.back_page()
                        elif 'minimize' in query:
                            self.minimize()
                        elif 'maximize' in query:
                            self.maximize()
                        else:
                            pass #make decision
            except Exception as e:
                print(f'Exception: {e} occured')
                

    def scroll_down(self):
            speak(voice,random.choice(('scrolling down','scrolling','ok scrolling','scrolled down','ok')))
            for i in range(0,12):self.driver.find_element(By.XPATH,'/html').send_keys(Keys.ARROW_DOWN)
            # self.driver.execute_script('window.scrollBy(0,100)')
            
    def scroll_up(self):
            speak(voice,random.choice(('scrolling up','scorolling','ok scrolling up','scrolled up','ok')))
            for i in range(0,12):self.driver.find_element(By.XPATH,'/html').send_keys(Keys.ARROW_UP)

    def open_link(self,linked_text):
            try:
                # links=self.driver.find_elements(By.CLASS_NAME,'LC20lb')
                links=self.driver.find_elements(By.PARTIAL_LINK_TEXT,linked_text)
                actions=ActionChains(self.driver)
                actions.scroll_to_element(links[0])
                actions.move_to_element(links[0])
                actions.click()
                actions.perform()
                pass
                # element=self.driver.find_element(By.CLASS_NAME,'LC20lb MBeuO DKV0Md')
                # for i in element: print(i)
                # self.actions.click(element).perform()
            except Exception :
                print('Exception(opening the link): '+Exception)
            
    def close_window(self) :
        self.driver.minimize_window()
        speak(voice,random.choice(('closing this window','exiting the window','ok closing','got it','ok it is closing now')))
        for i in range(0,self.page_count+1):self.driver.back() 
        self.page_count=0

    def destroy_session(self):
        self.driver.close()
        self.driver.quit()
    
    def back_page(self):
        self.driver.back()
        self.page_count-=1
    
    def refresh_page(self):
        self.driver.refresh()

    def minimize(self):
        self.driver.minimize_window()

    def maximize(self):
         self.driver.maximize_window()

# TEST
# obj=SearchGoogle()
# obj.search_on_google('what is keyboard')
# time.sleep(10)
# obj.close_window()
# obj1=SearchGoogle()
# obj1.search_on_google('what is computer')
# time.sleep()
# obj1.close_window()
