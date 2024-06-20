
assistant_name='Computer'
intents={
    'greet':{
        'patterns':['hello','computer',f'{assistant_name}',f'hey {assistant_name}','hey computer'],
        'responses':[]
    },
    'yes no query':{
        'patterns':['can you','do you','are you'],
        'responses':[]
    },
    'good night':{
        'patterns':['good night'],
        'responses':[]
    },
    'wikipedia':{
        'patterns':['search on wikipedia','wikipedia'],
        'responses':[]
    },
    'youtube':{
        'patterns':['search on youtube','open youtube'],
        'responses':[]
    },
    'gemini':{
        'patterns':['generate','generative AI','gemini'],
        'responses':[]
    },
    'google':{
        'patterns':['open google'],
        'responses':[]
    },
    'play music':{
        'patterns':[],
        'responses':[]
    },
    'open website':{
        'patterns':[],
        'responses':[]
    },
    'current time':{
        'patterns':[],
        'responses':[]
    },
    'date':{
        'patterns':[],
        'responses':[]
    },
    'run detection':{
        'patterns':[],
        'responses':[]
    },
    'detect object':{
        'patterns':[],
        'responses':[]
    },
    'what is my name' : {
        "patterns":['can you guess my name','who am i','do you know me','what is my name','can you recognize me','can you see me','guess my name','can you guess my name'],
        "responses":['Hmm, let me see... Is it {name}?','How about {name}?','Yes, Maybe its {name}?','Is it {name}?','Ok, Could it be {name}?','Is your name {name}?','Perhaps its {name}?','Maybe it {name}?','Could it be {name}?','Is it {name}?']
    },
    

}