
#import libraries and modules
import Tkinter as tk
import ttk
from Tkinter import StringVar
from Tkinter import IntVar
import tkMessageBox as mBox

#imports for tag readers
import RPi.GPIO as GPIO
import spi
"""new classes for reading tags"""
import SimpleMFRC522_monitor
import SimpleMFRC522_normal

import pymysql

#imports for logging
import os
import datetime



"""new instances since last commit"""
#monitorInstance returns 0 if no tag found, only checks once
monitorInstance = SimpleMFRC522_monitor.SimpleMFRC522_monitor()
#normalReadInstance checks for tag until one is scanned
normalReadInstance = SimpleMFRC522_normal.SimpleMFRC522_normal()

#dictonary to hold database connection info
dbConfig = {
    'user': 'PythonAdmin',
    'password':'python17',
    'host':'127.0.0.1',
    'database': 'project'
    }
"""new global var for monitor"""
#global vars for monitoring
stopMonitor = False
reader = 1
stopMonitorForCheck = False

class GUI:
    def __init__(self, master):
        self.master = master
        master.title("Python GUI")
        master.config(background="lavender")
        self.initialize_UI()
    #def userLogin(self):
        
        
    def initialize_UI(self):
        #theme
        self.s = ttk.Style()
        self.s.theme_use("clam")
        """tabs"""
        self.tabControl = ttk.Notebook(self.master)
        #tab1
        self.tab1 = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab1,text="New person")
        #tab2
        self.tab2 = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab2,text="People already in database")
        #tab3
        self.tab3 = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab3,text="Monitor")
        self.tabControl.pack(expand=1,fill="both",ipadx=10,ipady=10)
        
        """""
            tab1
        """""
        #inputs to add new person to database
        self.create_person_fields()
        
       
        
        """""
            tab2
        """""
        
        self.tree = ttk.Treeview( self.tab2, columns=('Tagnumber','Surname','Firstname','Image','Access',))
        self.tree.heading('#1', text='Tagnumber')
        self.tree.heading('#2', text='Surname')
        self.tree.heading('#3', text='Firstname')
        self.tree.heading('#4', text='Photo')
        self.tree.heading('#5', text='Access')
        self.tree.column('#1',stretch='False',minwidth=0,width=100)
        self.tree.column('#2',stretch='False',minwidth=0,width=100)
        self.tree.column('#3',stretch='False',minwidth=0,width=100)
        self.tree.column('#4',stretch='False',minwidth=0,width=80)
        self.tree.column('#5',stretch='False',minwidth=0,width=80)
        self.tree.column('#0',width=0,stretch='False')#don't show first column
        self.tree.grid(row=0,column=0,sticky='snwe')
        #self.tree.bind('<<TreeviewSelect>>',self.selectedItem)

        treeScroll = ttk.Scrollbar(self.tab2,orient=tk.VERTICAL,command=self.tree.yview)
        self.tree['yscroll']=treeScroll.set
        treeScroll.grid(row=0,column=1,sticky='ns')
        
        self.BtnsFrame = ttk.Frame(self.tab2,width=100,height=50)
        self.BtnsFrame.grid(pady=5,padx=5,row=10)
        self.refreshBtn= ttk.Button(self.BtnsFrame,text="Refresh/Load",width=15,command=self.refresh)
        self.refreshBtn.grid(row=0,column=0,sticky="w",padx=5)
        self.editBtn= ttk.Button(self.BtnsFrame,text="Edit user information",command=self.editUser)
        self.editBtn.grid(row=0,column=1,sticky="w",padx=5)
        self.deleteBtn= ttk.Button(self.BtnsFrame,text="Delete user",command=self.deleteUser,width=15)
        self.deleteBtn.grid(row=0,column=2,sticky="w",padx=5)
        

        """""
            tab3
        """""
        #image frame
        self.frameImg = ttk.Frame(self.tab3,width=200,height=100)
        self.frameImg.grid(row=0,pady=2)
        #frame for name and entry
        self.frameEntry = ttk.Frame(self.tab3,width=200,height=100)
        self.frameEntry.grid(row=1,pady=2)
        #frame right or wrong
        self.frameResponse = ttk.Frame(self.tab3,width=50,height=50)
        self.frameResponse.grid(row=2,pady=2)
    
        #button to start monitor
        self.startBtn = ttk.Button(self.tab3,text="Start monitor",command=self.startMonitor,width=25)
        self.startBtn.grid(row=3,column=0)
        #button to stop monitor
        self.stopBtn = ttk.Button(self.tab3,text="Stop monitor",command=self.stopMonitor,width=25)
        self.stopBtn.grid(row=3,column=1)
        #monitor who enters
        self.monitor()
        
    def startMonitor(self):
        global stopMonitor
        stopMonitor = False
        self.checkReaders()
        
    def stopMonitor(self):
        global stopMonitor
        stopMonitor = True
        
    def checkReaders(self):
        global stopMonitor
        global reader
        global stopMonitorForCheck
        if stopMonitor != True:
            if reader == 1:
                spi.openSPI(device='/dev/spidev0.0',speed=1000000)
            elif reader == -1:
                spi.openSPI(device='/dev/spidev0.1',speed=1000000)
            try:
                id, text = monitorInstance.read()
                print(id)
                print(text)
            finally:
                GPIO.cleanup()
                if id == 0:
                    reader = reader*-1
                    gui.after(2000, self.checkReaders)
                else:
                    stopMonitorForCheck = True
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if stopMonitorForCheck == True:
            self.checkPerson(id, now, reader)
            stopMonitorForCheck = False
            gui.after(2000, self.checkReaders)
        
    def checkPerson(self,id, tijd, reader):
        connection = pymysql.connect(**dbConfig)
        cursor = connection.cursor()
        ingang=0
        functiePersoon=0
        naam=""
        voornaam=""
        granted = ""
        action = ""
        try:
            cursor.execute("Select * FROM Personen where ID = %s",(id))
            if reader == 1:
                self.pEntry.delete(tk.INSERT)
                self.pEntry.insert(tk.INSERT, "Reader 1")
                ingang = 1
            else:
                self.pEntry.delete(tk.INSERT)
                self.pEntry.insert(tk.INSERT, "Reader 2")
                ingang = 2
                
            for response in cursor:
                voornaam = response[1]
                naam = response[2]
                self.imgPerson = tk.PhotoImage(file=response[3])
                self.imgLabel.configure(image=self.imgPerson)
                self.pName.insert(tk.INSERT, response[1]+" "+response[2])
                functiePersoon = response[4]
                if id == response[0] and (response[5] == ingang or response[5] == 3) and response[6] == 1:
                    self.imgResponse = tk.PhotoImage(file="right.gif")
                    self.imgResLabel.configure(image=self.imgResponse)
                    granted = "approved."
                else:
                    self.imgResponse = tk.PhotoImage(file="error.gif")
                    self.imgResLabel.configure(image=self.imgResponse)
                    granted = "denied."
                if response[7] == 0:
                    #komt binnen
                    action = "entered"
                    try:
                        cursor.execute("""UPDATE Personen SET aanwezig=%s where id=%s""",(1,id))
                        connection.commit()
                    except pymysql.MySQLError as e:
                        connection.rollback()
                        print("Got error {!r}, errno is {}".format(e,e.args[0]))
                    
                if response[7] == 1:
                    #gaat weg
                    action = "left"
                    try:
                        cursor.execute("""UPDATE Personen SET aanwezig=%s where id=%s""",(0,id))
                        connection.commit()
                    except pymysql.MySQLError as e:
                        connection.rollback()
                        print("Got error {!r}, errno is {}".format(e,e.args[0]))
                
                
        except pymysql.MySQLError as e:
            print("Got error {!r}, errno is {}".format(e,e.args[0]))
        finally:
            cursor.close()
            connection.close()
            #opening logfile
            logfile = open("./log.txt", "a")
            logfile.write(tijd + " " + voornaam + " " + naam + ", " + str(functiePersoon) + ", " + action + " via entry: " + str(ingang) + ", entry was " + granted + "\n")
            logfile.close()
            
            
    def create_person_fields(self):
        #borderwidth = distance between border and elements
        self.frame_pinfo = ttk.Frame(self.tab1,width=200,height=300,relief="ridge",borderwidth=20)
        self.frame_pinfo.grid(row=0,column=0,padx=20,pady=20)
        self.label_new_person = ttk.Label(self.frame_pinfo,text="Add new person")
        self.label_new_person.grid(row=0,sticky="e,w",column = 1)
        
        self.vLabel = ttk.Label(self.frame_pinfo, text="First name:",width=15).grid(row=1,column=0)
        self.vnaam = ttk.Entry(self.frame_pinfo,width=20)
        self.vnaam.grid(row=1,column=1,pady=2)

        self.aLabel = ttk.Label(self.frame_pinfo, text="Last Name:",width=15).grid(row=2,column=0)
        self.anaam = ttk.Entry(self.frame_pinfo,width=20)
        self.anaam.grid(row=2,column=1,pady=2)

        self.iLabel = ttk.Label(self.frame_pinfo, text="Image:",width=15).grid(row=3,column=0)
        self.image = ttk.Entry(self.frame_pinfo,width=20)
        self.image.grid(row=3,column=1,pady=2)
        
        self.tagLabel = ttk.Label(self.frame_pinfo, text="Tag number:",width=15).grid(row=4,column=0)
        self.tagnummer = ttk.Entry(self.frame_pinfo,width=20)
        self.tagnummer.grid(row=4,column=1,pady=2)

        self.fLabel = ttk.Label(self.frame_pinfo, text="Function:",width=15).grid(row=5,column=0)
        self.functie = ttk.Entry(self.frame_pinfo,width=20)
        self.functie.grid(row=5,column=1,pady=2)

        self.tLabel = ttk.Label(self.frame_pinfo, text="Access:",width=15).grid(row=6,column=0)
        self.toegang = ttk.Entry(self.frame_pinfo,width=20)
        self.toegang.grid(row=6,column=1,pady=2)
      
        
        self.btn_read_tag = ttk.Button(self.frame_pinfo,text="Read tagnumber",width=25,command=self.readtag)
        self.btn_read_tag.grid(row=7,column=1,padx=1,pady=10)
        self.btn_addToDatabase = ttk.Button(self.frame_pinfo,text="Add to database",width=25,command=self.insertDb)
        self.btn_addToDatabase.grid(row=8,column=1,padx=1,pady=1)
        
    def monitor(self):
        #image of person
        self.imgPerson = tk.PhotoImage(file="mk.gif")
        self.imgLabel = ttk.Label(self.frameImg,image=self.imgPerson)
        self.imgLabel.grid(row=0,column=2,padx=10,pady=3,columnspan=2,rowspan=2)
        #name of person
        self.nameLabel = ttk.Label(self.frameEntry,text="Name:")
        self.nameLabel.grid(column=0,row=0,sticky="w",pady=2)
        self.pName = tk.Text(self.frameEntry,width=20,height=2,highlightthickness=2, highlightbackground="#333")
        self.pName.grid(column=0,row=1,sticky="w")
        #entry
        self.entryLabel = ttk.Label(self.frameEntry,text="Entry:")
        self.entryLabel.grid(column=0,row=2,sticky="w",pady=2)
        self.pEntry = tk.Text(self.frameEntry,width=20,height=2,highlightthickness=2, highlightbackground="#333")
        self.pEntry.grid(column=0,row=3,sticky="w")
        #image to show if entry was successful or not
        self.imgResponse = tk.PhotoImage(file="error.gif")
        self.imgResLabel = ttk.Label(self.frameResponse,image=self.imgResponse)
        self.imgResLabel.grid(row=0,column=0,padx=10,pady=2)
        
    def editUser(self):
        self.new = tk.Toplevel(self.master)
        
        self.vAccess = tk.IntVar()
        self.vState = tk.IntVar()
        self.new.fnew = ttk.Frame(self.new,width=200,height=300,relief="ridge",borderwidth=20)
        self.new.fnew.grid(row=0,column=0,padx=20,pady=20)

        self.new.tagLabel = ttk.Label(self.new.fnew, text="Tag number:",width=15).grid(row=0,column=0)
        self.new.tagnummer = ttk.Entry(self.new.fnew,width=20)
        self.new.tagnummer.grid(row=0,column=1,pady=2)
        
        self.new.vLabel = ttk.Label(self.new.fnew, text="First name:",width=15).grid(row=1,column=0)
        self.new.vnaam = ttk.Entry(self.new.fnew,width=20)
        self.new.vnaam.grid(row=1,column=1,pady=2)
        
        self.new.aLabel = ttk.Label(self.new.fnew, text="Last Name:",width=15).grid(row=2,column=0)
        self.new.anaam = ttk.Entry(self.new.fnew,width=20)
        self.new.anaam.grid(row=2,column=1,pady=2)

        self.new.lphoto = ttk.Label(self.new.fnew,text="Image:",width=15).grid(row=3,column=0)
        self.new.photo = ttk.Entry(self.new.fnew,width=20)
        self.new.photo.grid(row=3,column=1,pady=2)

        self.new.Lntag = ttk.Label(self.new.fnew, text="New tagnumber:",width=15).grid(row=4,column=0)
        self.new.nTag = ttk.Entry(self.new.fnew,width=20)
        self.new.nTag.grid(row=4,column=1,pady=2)

        #radio buttons
        self.new.frameAccess = ttk.Frame(self.new.fnew)
        self.new.frameAccess.grid(row=5,column=1)
        self.new.accessLb = ttk.Label(self.new.fnew ,text="Access:",width=15).grid(row=5,column=0) 
        self.new.accessRb1 = ttk.Radiobutton(self.new.frameAccess,text="Ingang 1",value=1,variable=self.vAccess)
        self.new.accessRb1.grid(row=0,column=1,padx=2)
        self.new.accessRb2 = ttk.Radiobutton( self.new.frameAccess ,text="Ingang2",value=2,variable=self.vAccess)
        self.new.accessRb2.grid(row=0,column=2,padx=2)
        self.new.accessRb3 = ttk.Radiobutton( self.new.frameAccess ,text="Beide",value=3,variable=self.vAccess)
        self.new.accessRb3.grid(row=0,column=3,padx=2)

        self.new.frameState = ttk.Frame(self.new.fnew)
        self.new.frameState.grid(row=6,column=1)
        self.new.stateLb = ttk.Label(self.new.fnew ,text="State:",width=15).grid(row=6,column=0) 
        self.new.stateRb1 = ttk.Radiobutton(self.new.frameState,text="On",value=0,variable=self.vState)
        self.new.stateRb1.grid(row=0,column=1,padx=7)
        self.new.stateRb2 = ttk.Radiobutton( self.new.frameState ,text="Off",value=1,variable=self.vState)
        self.new.stateRb2.grid(row=0,column=2,padx=7)
        
        
        self.new.tagBtn = ttk.Button(self.new.fnew,text="Read new tag",width=25,command=self.readNtag)
        self.new.tagBtn.grid(row=7,column=1,pady=2)

        self.new.saveBtn = ttk.Button(self.new.fnew,text="Save",width=25,command=self.saveEdit)
        self.new.saveBtn.grid(row=8,column=1,pady=2)

        item = self.tree.selection()[0]
        item_text = self.tree.item(item,"values")

        self.new.tagnummer.insert(0,item_text[0])
        self.new.vnaam.insert(0,item_text[1])
        self.new.anaam.insert(0,item_text[2])
        self.new.photo.insert(0,item_text[3])
        self.new.mainloop()
    def saveEdit(self):
        answer = mBox.askyesno("Add new user", "Are you want to edit this user's information?")

        voornaam = self.new.vnaam.get()
        achternaam = self.new.anaam.get()
        tagnummer = self.new.tagnummer.get()
        image = self.new.photo.get()
        nTag = self.new.nTag.get()
        access = self.vAccess.get()
        state = self.vState.get()
        
        connection = pymysql.connect(**dbConfig)
        cursor = connection.cursor()

        if answer:
            try:
                if nTag == "":
                    cursor.execute("""UPDATE Personen SET firstname=%s,lastname=%s,photo=%s,access=%s,state=%s where id=%s""",(voornaam,achternaam,image,access,state,tagnummer))
                else:
                    cursor.execute("""UPDATE Personen SET id=%s,firstname=%s,lastname=%s,photo=%s,access=%s,state=%s where id=%s""",(nTag,voornaam,achternaam,image,access,state,tagnummer))
                print(access,state)
                connection.commit()
            except pymysql.MySQLError as e:
                connection.rollback()
                print("Got error {!r}, errno is {}".format(e,e.args[0]))
            
            finally:
                cursor.close()
                connection.close()
                self.new.destroy()

    def refresh(self):
        self.tree.delete(*self.tree.get_children())
        
        connection = pymysql.connect(**dbConfig)
        cursor = connection.cursor()

        try:
            cursor.execute("Select * FROM Personen")
            for response in cursor:
                self.tree.insert('','end',values=(response[0],response[2],response[1],response[3],response[6]))
                
        except pymysql.MySQLError as e:
            print("Got error {!r}, errno is {}".format(e,e.args[0]))
        finally:
            cursor.close()
            connection.close()

    def insertDb(self):
        #let user confirm
        answer = mBox.askyesno("Add new user", "Are you sure you want to add this user?")
         
        if answer:
            voornaam = self.vnaam.get()
            achternaam = self.anaam.get()
            tagnummer = self.tagnummer.get()
            image = self.image.get()
            functie = self.functie.get()
            toegang = self.toegang.get()
            
            connection = pymysql.connect(**dbConfig)
            cursor = connection.cursor()
                
            try:
                query = """INSERT INTO Personen (id,firstname,lastname,photo,functionType,access,state) VALUES(%s,%s,%s,%s,%s,%s,%s)"""
                cursor.execute(query,(tagnummer,voornaam,achternaam,image,functie,toegang,1))
                connection.commit()
            except pymysql.MySQLError as e:
                connection.rollback()
                print("Got error {!r}, errno is {}".format(e,e.args[0]))    
            
            finally:
                cursor.close()
                connection.close()
                #clear entries
                self.vnaam.delete(0,'end')
                self.anaam.delete(0,'end')
                self.tagnummer.delete(0,'end')
                self.image.delete(0,'end')
                self.functie.delete(0,'end')
                self.toegang.delete(0,'end')
                

            
    def deleteUser(self):
        answer = mBox.askyesno("Delete user", "Are you sure you want to delete this user?")
        if answer:         
            connection = pymysql.connect(**dbConfig)
            cursor = connection.cursor()

            item = self.tree.selection()[0]
            item_text = self.tree.item(item,"values")

            #query database to delete user
            try :
                query ="DELETE FROM Personen where id = %s"
                ID = int(item_text[0])
                response = cursor.execute(query,(ID,))
                
                if response:
                    print("User deleted")
                else:
                    print("User could not be deleted")
                connection.commit()
            except pymysql.MySQLError as e:
                connection.rollback()
                print("Got error {!r}, errno is {}".format(e,e.args[0]))
                
            finally:
                    cursor.close()
                    connection.close()
    def readtag(self):
        id,text = normalReadInstance.read()
        self.tagnummer.insert(0,id)
    def readNtag(self):
        id,text = normalReadInstance.read()
        self.new.nTag.insert(0,id)
        
            
        
gui = tk.Tk()
my_gui = GUI(gui)
gui.mainloop()

