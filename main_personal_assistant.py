from tkinter import Tk,Canvas,StringVar,Entry,PhotoImage,Menu,Text
from tkinter import HORIZONTAL,HIDDEN,END,WORD,VERTICAL,GROOVE
import tkinter.ttk as ttk
from ttkthemes import ThemedStyle
import datetime
from tkinter.messagebox import showinfo, askokcancel
from tkinter import messagebox
from tkinter.filedialog import askopenfilename, asksaveasfilename
import os
from io import StringIO
from PIL import Image
from PIL import ImageTk
# import pyttsx3
# import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import random
import smtplib
import wolframalpha
from configurations import APP_ID,api_key
from wolframalpha import Client
import time
import sys
import re
import subprocess
import pyowm
from pyowm import OWM
from install_apps import app_list, Action

# engine = pyttsx3.init()
# voices = engine.getProperty('voices')
# engine.setProperty('voices',voices[0].id)        
chrome = webbrowser.get('windows-default')



class MyApp(Tk):
    def __init__(self):
        Tk.__init__(self)
        # s.theme_use(themename='scidblue')
        container = ttk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        self.frames = {}
        for F in (HelloPage,Application,ByePage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky='NSEW')
        self.show_frame(HelloPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()



class HelloPage(ttk.Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        ttk.Frame.__init__(self, parent)
        self.make_widget()

    def set_key_binding(self,event):
        event.widget.configure()
        event.widget.focus_set()  # give keyboard focus to the label
        event.widget.bind('<Key>',self.controller.show_frame(Application))

    def wishme(self):
        hour = int(datetime.datetime.now().hour)
        wish=''
        if hour>=0 and hour <12:
           wish = "Good Morning!!!\n"
            # self.speak("Good Morning!!!")
        elif hour>=12 and hour <18:
            wish = "Good Afternoon!!!\n"
            # self.speak("Good Afternoon!!!")
        else:
            wish = "Good Evening!!!\n"
            # self.speak("Good Evening!!!")
        return wish+"How can i help you sir?"
        # self.speak("I am your personal assistant. I am here help you.!!!")

    def change_page(self):
        pass

    def make_widget(self):
        self.cvs = Canvas(self, width=20,height=500,background="#7ce577")
        self.cvs.create_oval(60, 65, 250, 250, fill="#a0ccda", outline="#a0ccdb")
        self.wish_var = StringVar()
        self.wish_var=self.wishme()
        self.cvs.create_text(155,165,text=self.wish_var,
                            font="Calibri 13 bold", state="normal",activefill='blue')


        # demo Label to change page
        self.lbl=ttk.Label(self.cvs, text='Click to Continue...',padding=5,cursor='hand2',font='Arial 10 bold',
                        foreground="red",background='#a0ccda')    #bg="#a0ccda",fg='red'
        self.lbl.focus_set()
        self.lbl.bind('<Button-1>',self.set_key_binding)
        self.lbl.place(x=92, y=260, width="130", height="50")
        self.cvs.pack(fill="both", expand=True)




class Application(ttk.Frame):
    def __init__(self, parent, controller):
        self.controller = controller  
        ttk.Frame.__init__(self, parent)
        self.make_widget()

    def change_page(self):
            pass

    # def speak(self,audio):
    #     engine.say(audio)
    #     engine.runAndWait()

    def newfile(self):
        app.title("Untitled - Personal Assistant")
        self.file=None
        self.outputtext_area.delete(1.0,'end')


    def openfile(self):
        self.file= askopenfilename(defaultextension=".txt",
                            filetypes=[("All Files","*.*"),("Text Document","*.txt")])
        if self.file =="":
            self.file=None
        else:
            app.title(os.path.basename(self.file)+" - Personal Assistant")
            self.outputtext_area.delete(1.0,'end')
            f=open(self.file,"r")
            self.outputtext_area.insert(1.0,f.read())

    def about(self):
        showinfo("Personal Assistant","Personal Assistant\nVersion-1.0")

    def savefile(self):
        if self.file == None:
            self.file = asksaveasfilename(initialfile = 'Untitled.txt', defaultextension=".txt",
                            filetypes=[("All Files", "*.*"),
                                        ("Text Documents", "*.txt")])
            if self.file =="":
                self.file = None

            else:
                #Save as a new file
                f = open(self.file, "w")
                f.write(self.outputtext_area.get(1.0, END))
                f.close()

                app.title(os.path.basename(self.file) + " - Personal Assistant")
                showinfo("Success","File Saved")
        else:
            # Save the file
            f = open(self.file, "w")
            f.write(self.outputtext_area.get(1.0, END))
            f.close()

    def buttonClicked(self,btn):
        if (btn==self.btnList[0]):
            self.newfile()
        elif (btn==self.btnList[1]):
            self.openfile()
        elif (btn==self.btnList[2]):
            self.savefile()
        elif (btn==self.btnList[3]):
            self.about()
        else:
            pass
        

    # def takeCommand(self):
    #     r= sr.Recognizer()
    #     with sr.Microphone() as source:
    #         print("Listening....")
    #         self.speak("Listening")
    #         r.pause_threshold=1.0
    #         audio = r.listen(source)
    #     try:
    #         print("Recognizing...")
    #         self.speak("Recognizing")
    #         query = r.recognize_google(audio)
    #         print(f"User Said: {query}\n")

    #     except Exception:
    #         print("Say That Again Please...")
    #         self.speak("Say That Again Please...")
    #         time.sleep(0.5)
    #         return None
    #     return query.lower()

            


    def search(self,query):
        self.query=self.query_input_area.get()
        try:

            if "what you can do" in query:
                return Action

            
            elif "wikipedia" in query:
                # print("searching wikipedia...")
                # self.speak("searching wikipedia...")
                query = query.replace("wikipedia", "")
                results = wikipedia.summary(query, sentences = 2)            
                # self.speak("According to wikipedia")
                return ("According to wikipedia: "+results)
                #self.speak(results)
                


            elif "play music" in query:
                music_dir = r"D:\music"
                songs = os.listdir(music_dir)
                random_song= random.choice(songs)
                os.startfile(os.path.join(music_dir,random_song))
                return ("Playing - "+random_song)

            elif "the time" in query:
                strtime = datetime.datetime.now().strftime("%H:%M:%S")
                return (f"The time is: {strtime}")
                #self.speak(f"The time is: {strtime}")
                
                


            elif "the date" in query:
                today_date = datetime.datetime.now().strftime("%d:%m:%Y")
                return (f"The date is: {today_date}")
                # self.speak(f"The date is: {today_date}")


            elif 'youtube' in query: 
                #self.speak("Opening youtube")
                youtube_query = query.replace('youtube',"") .strip()
                chrome.open("http://www.youtube.com/results?search_query="+(youtube_query.replace(" ","+"))) 
                return (f"Playing {youtube_query} on Youtube...")

            elif 'current weather' in query:
                reg_ex = re.search('current weather in (.*)', query)
                if reg_ex:
                    city = reg_ex.group(1)
                    owm = OWM(API_key=api_key)      #from configurations
                    obs = owm.weather_at_place(city)
                    w = obs.get_weather()
                    k = w.get_status()
                    x = w.get_temperature(unit='celsius')
                    return ('Current weather in %s is %s. The maximum temperature is %0.2f and the minimum temperature is %0.2f degree celcius' % (city, k, x['temp_max'], x['temp_min']))
                    #self.speak('Current weather in %s is %s. The maximum temperature is %0.2f and the minimum temperature is %0.2f degree celcius' % (city, k, x['temp_max'], x['temp_min']))

            elif 'google' in query: 

                google_query = query.replace('google',"",1) .strip()
                chrome.open("https://www.google.com/search?q="+(google_query.replace(" ","+"))) 
                return(f"Searching {google_query} on Google...")

            elif "convert" in query: 
                        
                # write your wolframalpha app_id here
                # input=query
                app_id = APP_ID      #from configurations
                client = wolframalpha.Client(app_id) 
                # indx = input.split().index('convert') 
                # query = input.split()[indx + 1:] 
                res = client.query(''.join(query))
                answer = next(res.results).text
                return ("The answer is " + answer) 
                # self.speak("The answer is " + answer)     

            elif "calculate" in query: 
                # write your wolframalpha app_id here
                input_query=query
                app_id = APP_ID
                client = wolframalpha.Client(app_id) #from configurations
                indx = input_query.split().index('calculate') 
                query_calc = input_query.split()[indx + 1:] 
                res = client.query(' '.join(query_calc)) 
                answer = next(res.results).text
                return (" Answer = " + answer) 
                # self.speak("The answer is " + answer)
                
            elif 'list app' in query:
                list_of_apps= list(app_list.keys())
                str_of_apps = '\n'.join([str(elem) for elem in list_of_apps])
                return "List of apps\n"+str_of_apps

            elif 'launch' in query:
                # print("Here is a list of application: ")
                # self.speak("Here is a list of application")
                # self.query_input_area.delete(0,'end')
                indx = query.split().index('launch') 
                res = (query.split()[indx + 1:])
                
                query = ' '.join([str(elem) for elem in res])
                # for key in app_list.keys():
                #     print(key)
                # print("Which app you want to launch?")
                
                # app_name=self.query_input_area.get().lower()

                # app_name=self.takeCommand().lower()
                try:

                    if query in app_list.keys():
                        path = app_list.get(query)
                        # print('Launching the desired application')
                        # self.speak('Launching the desired application')
                        subprocess.Popen([path], stdout=subprocess.PIPE)
                        return (f"Launching {query}")
                    else:
                        return "App Not Found."
                except Exception:
                    return 'Try Again'

            elif query and not query.isspace():
                chrome.open("https://www.google.com/search?q="+(query.replace(" ","+")))
                return "Unspecific Command, Searching on google"


        except Exception:
            return "Sorry! I am unable to get this at the moment"
    
    def conversation(self,event):
        #Your code that inputs the message on text area
        self.varContent = self.query_input_area.get()
        self.get_query  = self.query_input_area.get().lower()# get what's written in the inputentry entry widget
        self.cli_output=self.search(self.get_query)
        self.query_input_area.delete(0,'end')
        if self.get_query is not None:
            self.outputtext_area.tag_configure('bold-15',font=('Constantia', 14, 'bold'),justify='right')
            self.outputtext_area.insert(END,"You:\n"+self.varContent+"\n",'bold-15')
            # self.outputtext_area.tag_add('self.varContent','1.0',tk.END)
            # self.outputtext_area.tag_config('self.varContent', font='lucida 13 bold')


        if self.cli_output is not None:
            self.outputtext_area.tag_configure('normal-13', relief=GROOVE, font=('Tempus Sans ITC', 13))
            self.outputtext_area.insert(END,"P.A:\n"+self.cli_output+"\n",'normal-13')
            # self.outputtext_area.tag_add('self.cli_output',tk.END,'end')
            # self.outputtext_area.tag_config('self.cli_output', font='lucida 12 normal')
        self.outputtext_area.insert(END,"-----------------------------------------------\n")
        self.outputtext_area.see("end")

    def confirmquit(self):
        response = askokcancel("Personal Assistant", "QUIT ?",default="ok")
        if response == True:
            app.destroy()
        else:
            self.controller.show_frame(Application)


    def make_widget(self):
        
        self.search_area_frame = ttk.Frame(self)
        self.query_input_area=Entry(self.search_area_frame,font="lucida 16 bold")
        self.query_input_area.bind("<Return>",self.conversation)
        self.search_image = PhotoImage(file="search.png")
        self.search_button = ttk.Button(self.search_area_frame,image=self.search_image)     #,relief='flat'
        self.search_button.bind("<Button-1>",self.conversation)
        self.search_button.pack(padx=2,ipadx=5,ipady=5,side='right',anchor='e')
        self.input_scrollbar=ttk.Scrollbar(self.search_area_frame,orient=HORIZONTAL)    # width='6'
        self.input_scrollbar.config(cursor = 'target',command=self.query_input_area.xview)
        self.input_scrollbar.pack(side='top',fill='x')
        self.query_input_area.config(xscrollcommand = self.input_scrollbar.set)
        self.search_area_frame.pack(side='bottom')
        self.query_input_area.pack(ipadx=5,padx=1,pady=1,ipady=2,anchor='center',fill='both')
        
        

        self.conversation_frame=ttk.Frame(self)
        

        self.image_title = Image.open("personal_assistant.png")
        self.image_title = self.image_title.resize((250,50))
        self.image_title = ImageTk.PhotoImage(self.image_title)
        self.title_image_label=ttk.Label(self.conversation_frame,image=self.image_title)   # ,relief='ridge'
        self.title_image_label.grid(row='0',column='0',rowspan='2',columnspan='4',sticky='w')

        self.quit = ttk.Button(self.conversation_frame ,text="QUIT",        # bg="#a0ccda",fg="red",relief='raised'
                        cursor='X_cursor',command=lambda: [self.controller.show_frame(ByePage),self.confirmquit()])
        self.quit.grid(row='0',column='10',padx=6,ipadx=8,pady=0,sticky='ne')

        self.more_options = ttk.Menubutton(self.conversation_frame,text='...')     #bg="#a0ccda",cursor='hand2',text="...",relief=RAISED,fg="DarkOrange3")
        self.contentMenu = Menu(self.more_options,tearoff=0)
        self.more_options.config(menu=self.contentMenu)     # ,height=1,width=4
        self.more_options.grid(row='1',column='10',padx=6,ipadx=8,pady=0)
        self.btnList = ('New','Open', 'Save', 'About')
        for btn in self.btnList:
            self.contentMenu.add_command(label=btn,command = lambda btn=btn: self.buttonClicked(btn))
        self.conversation_frame.pack(side='top')


        self.outputtext_area = Text(self,width=16,height=22,font='14',bg='bisque', wrap=WORD)  #26
        self.screen_scrollbar=ttk.Scrollbar(self,orient=VERTICAL)
        self.screen_scrollbar.config(cursor = 'target',command=self.outputtext_area.yview)
        self.screen_scrollbar.pack(fill='y',side='right',padx='1',pady='1')
        self.outputtext_area.config(yscrollcommand = self.screen_scrollbar.set)
        self.outputtext_area.see("end")
        self.outputtext_area.pack(fill='x')




        # button1 = ttk.Button(self, text='Next Page',
        #                    command=lambda: self.controller.show_frame(ByePage))
        # button1.pack()



class ByePage(ttk.Frame):
    def __init__(self, parent, controller):
        self.controller = controller  
        ttk.Frame.__init__(self, parent)
        self.make_widget()

    # def set_key_binding(self,event):
    #     event.widget.configure()
    #     event.widget.focus_set()  # give keyboard focus to the label
    #     event.widget.bind('<Key>',sys.exit())

    def make_widget(self):

        self.cvs = Canvas(self, width=20,height=499,background="firebrick1")
        self.cvs.create_oval(60, 65, 250, 250, fill="chocolate3", outline="#a0ccdb")
        self.cvs.create_text(155,165,text='Thank You!!!', font="Calibri 16 bold", state="normal",fill='cyan')
        self.cvs.pack(fill="both", expand=True)
        # lbl=Label(self, text='This is page three')
        # # button1 = ttk.Button(self, text='Previous Page',
        #                     #  command=lambda: self.controller.show_frame(Application))
        # lbl.focus_set()
        # lbl.bind('<Button-1>',self.set_key_binding)
        # lbl.pack()
        # # button1.grid()




if __name__ == '__main__':


    # self = tk.Tk()         #ThemedTk(theme="arc")
   
    # 
    app = MyApp()
    # self.geometry("296x500") #296
    p1 = PhotoImage(file = 'icon_assistant.png')
    app.geometry("316x504")
    app.iconphoto(True,p1)
    app.title("Personal Assistant")
    style = ThemedStyle(app)
    style.set_theme("scidgrey")
    app.resizable(0, 0)
    
    app.mainloop()