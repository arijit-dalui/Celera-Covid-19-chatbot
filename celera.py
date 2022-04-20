import pyttsx3
import pywhatkit
import urllib.request

from tkinter import *
import threading

main = Tk()

main.geometry("500x650")

main.title("Celera")



frame = Frame(main)

sc = Scrollbar(frame)
h= Scrollbar(frame,orient='horizontal')

msgs = Listbox(frame, width=80, height=20, yscrollcommand=sc.set, xscrollcommand=h.set)

sc.pack(side=RIGHT, fill=Y)
h.pack(side=BOTTOM, fill=X)
msgs.pack(side=LEFT, fill=BOTH, pady=10)

frame.pack()

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

    

def ask_from_bot():
    model = keras.models.load_model('chat_model')

    # load tokenizer object
    with open('tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)

    # load label encoder object
    with open('label_encoder.pickle', 'rb') as enc:
        lbl_encoder = pickle.load(enc)

    # parameters
    max_len = 120
    inp = textF.get()
    if inp=="":
        pass
    else:
        msgs.insert(END, "you : " + inp)
        result = model.predict(keras.preprocessing.sequence.pad_sequences(tokenizer.texts_to_sequences([inp]),
                                                 truncating='post', maxlen=max_len))
        
        temporary=[[i,r] for i,r in enumerate(result[0])]
        
        temporary.sort(key=lambda x: x[1], reverse=True)
        print(temporary[0][1])

        
        tag = lbl_encoder.inverse_transform([np.argmax(result)])

        if (temporary[0][1]<0.9 and temporary[0][1]>=0.6) or tag=='out_of_bound':
            msgs.insert(END, "celera : " + 'Please give me some time to think this')
            talk("")
            for i in range(10):
                talk("")
            talk('Please give me some time to think this')
            try:
                from googlesearch import search
            except ImportError:
                print("No module named 'google' found")
            query = inp
            search_results=[]
            for j in search(query, tld="co.in", num=10, stop=10, pause=2):
                search_results.append(j)
            import requests
            from bs4 import BeautifulSoup

            url = search_results[0]
            print(url)
            if url.find('https://www.youtube.com')>=0:
                talk('I found this which seems cool😁!!')
                msgs.insert(END, "celera : " + 'I found this which seems cool😁!!')
                pywhatkit.playonyt(url)
            
            else:
                response = requests.get(url)
                soup = BeautifulSoup(response.text)
                metas = soup.find_all('meta') #Get Meta Description
                flag=0
                for m in metas:
                    x=m.get('name')
                    if not(x=="") and x and x == 'Description' or x=='description':
                        print(x)
                        desc = m.get('content')
                        if desc=="":
                            pass
                        else:
                            flag=1
                            msgs.insert(END, "celera : " + desc)
                            msgs.insert(END, "celera : " + "you may visit: "+ url)
                            talk("")
                            for i in range(10):
                                talk("")
                            talk(desc)
                        break
                if(flag==0):
                    for m in metas:
                        x=m.get('name')
                        if not(x=="") and x and (x.find('Description') or x.find('description'))>=0:
                            desc = m.get('content')
                            if desc=="":
                                pass
                            else:
                                flag=1
                                msgs.insert(END, "celera : " + desc)
                                msgs.insert(END, "celera : " + "you may visit: "+ url)
                                talk("")
                                for i in range(10):
                                    talk("")
                                talk(desc)
                            break
                if(flag==0):
                    print(99)
                    msgs.insert(END, "celera : " + 'Sorry! I dont know')
                    talk("")
                    for i in range(10):
                        talk("")
                    talk('Sorry! I dont know')
        

        elif temporary[0][1]<0.6:
            msgs.insert(END, "celera : " + 'Sorry! I dont know')
            talk("")
            for i in range(10):
                talk("")
            talk('Sorry! I dont know')
        else:
            for i in data['intents']:
                if i['tag'] == tag:
                    answer=np.random.choice(i['responses'])
            answer_from_bot=answer
            print(type(answer_from_bot))
            talk("")
            for i in range(10):
                talk("")
            talk(answer)
            msgs.insert(END, "celera : " + str(answer_from_bot))
            speak(answer_from_bot)
            textF.delete(0, END)
            msgs.yview(END)
# creating a function

# creating text field

textF = Entry(main, font=("Courier", 10))
textF.pack(fill=X, pady=10)

btn = Button(main, text="Ask Celera", font=(
    "Courier", 10),bg='red', command=ask_from_bot)
btn.pack()


def enter_function(event):
    btn.invoke()


# going to bind main window with enter key...

main.bind('<Return>', enter_function)

def talk(text):
    engine.say(text)
    engine.runAndWait()


import json 
import numpy as np
from tensorflow import keras
from sklearn.preprocessing import LabelEncoder

import colorama 
colorama.init()
from colorama import Fore, Style, Back

import random
import pickle

with open("intents.json") as file:
    data = json.load(file)


        
        
        # print(Fore.GREEN + "ChatBot:" + Style.RESET_ALL,random.choice(responses))
talk("")
for i in range(20):
    talk("")
talk("Start messaging with celera")
print(Fore.YELLOW + "Start messaging with celera" + Style.RESET_ALL)

# def repeatL():
#     while True:
#         ask_from_bot()
# t = threading.Thread(target=repeatL)
main.iconbitmap('./bot.ico')
main.mainloop()