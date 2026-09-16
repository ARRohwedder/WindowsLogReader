# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import csv
import numpy as np
import tkinter as tk
from tkinter import filedialog

instruments = ['Aurox','Axio','LSM900','Olympus','STED','Stellaris','Thunder']
#detpos = [5,5,5,5,5,7,5]
monatnamen = ['Januar','Februar','März','April','Mai','Juni','Juli','August','September','November','Dezember']
monkurz = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
stopeventnr = ['1074','4647','4634','6008','6006','6013']
kopf = "User/evt no,Group/evt name,Day,Month,Year,Hour,Min,mon.minute\n"
prozesse = ["4647","4634","41","1076","1074","6008","6006","6005","6009","6013"]
#"4624",

tagminuten = 1440

users = []
names = []
groups = []

datatime = []
evtcode = []
evtname = []
details = []
datatimer = []
evtcoder = []
evtnamer = []
detailsr = []

with open('Userlist.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        users.append(row[0])
        names.append(row[1])
        groups.append(row[2])
csv_file.close()

def splitforprocess(filename):
    
    for i in range (0,len(prozesse)):#-1
        pname = prozesse[i]+".csv"
        with open(pname, "w") as f:
            with open(filename) as data_file:
                data_reader = csv.reader(data_file, delimiter=',')
                fields = next(data_reader)
                kopf = "Ebene,Datum,Quelle,Ereignis,Katekorie,Details\n"
                f.write(kopf)
                for row in data_reader:
                    if prozesse[i] in row and len(row)>1:
                        datatimer.append(row[1])
                        evtcoder.append(row[3])
                        evtnamer.append(row[4])
                        detailsr.append(row[5])
                        s = ','.join(row)
                        s = s+"\n"
                        f.write(s)
        f.close()
        data_file.close()
    return (datatimer,evtcoder,evtnamer,detailsr)

def loadthedata(instrument):
    innen = 0
    detnumber = 5
    filename = filedialog.askopenfilename(initialdir = "C:/Users/AK126086/Documents/Verwaltung/Logdata/2025/",title = "Select a File",filetypes = (("CSV files","*.csv*"),("all files","*.*")))
    print ("loaded file: ",filename,"\n")
    with open(filename) as data_file:
        data_reader = csv.reader(data_file, delimiter=',')
        fields = next(data_reader)
        #if instrument=="LSM900":
        #    detnumber = 5
        for row in data_reader:
            innen +=1
            datatime.append(row[1])
            evtcode.append(row[3])
            evtname.append(row[4])
            details.append(row[detnumber])
    data_file.close()
    return (datatime,evtcode,evtname,details,filename)
        
def toreal(zeit,abb):
    splitzeit = zeit.split(':')
    stunde = int(splitzeit[0])
    minute = int(splitzeit[1])
    sekunde = int(splitzeit[2])
    if "PM" in abb and stunde < 12:
        stunde = stunde+12
    if stunde > 23:
        stunde = 0
    return (stunde,minute,sekunde)

def datbreak(datum,cformat):
    if cformat == "eng":
        splitdatum = datum.split('/')
        monat = int(splitdatum[0])
        tag = int(splitdatum[1])
        jahr = int(splitdatum[2])
    if cformat == "de":
        splitdatum = datum.split('/')
        tag = int(splitdatum[0])
        monat = int(splitdatum[1])
        jahr = int(splitdatum[2])
    if cformat == "text":
        splitdatum = datum.split('-')
        tag = int(splitdatum[0])
        monat = monkurz.index(splitdatum[1])+1
        jahr = int(splitdatum[2])
    if cformat == "de2":
        splitdatum = datum.split('.')
        tag = int(splitdatum[0])
        monat = int(splitdatum[1])
        jahr = int(splitdatum[2])
    return (tag,monat,jahr)

def minutenseit(tag,monat,jahr,stunde,minute):
    tagstand = tagminuten * (int(tag)-1)
    stundenminuten = int(stunde) * 60
    standminuten = tagstand + stundenminuten + int(minute)
    return (standminuten)

def findeuser2(details,evtname):
    loginline = []
    userentry = []
    groupentry = []
    for i in range(0,len(evtname)):#-1
        #print (evtname[i])
        if "Logon" in evtname[i]:
            #print (evtname[i])
            for j in range(0,len(users)):#-1
                #print (users[j])
                if users[j] in details[i]:
                    print(i," ",users[j]," ",evtname[i])
                    userentry.append(users[j])
                    loginline.append(i)
                    groupentry.append(groups[j])
    return(loginline,userentry,groupentry)

def zerlegezeit(splittimes):
    if len(splittimes)>2:
            (stunde,minute,sekunde) = toreal(splittimes[1],splittimes[2])
            (tag,monat,jahr) = datbreak(splittimes[0],"eng")
    else:
        nextsplit = splittimes[1].split(":")
        stunde = nextsplit[0]
        minute = nextsplit[1]
        if "-" in splittimes[0]:
            (tag,monat,jahr) = datbreak(splittimes[0],"text")
        if "." in splittimes[0]:
            (tag,monat,jahr) = datbreak(splittimes[0],"de2")
        else:
            (tag,monat,jahr) = datbreak(splittimes[0],"de")
    zeitindex = minutenseit(tag,monat,jahr,stunde,minute)
    return(tag,monat,jahr,stunde,minute,zeitindex)

def logindata(datatime,loginpos,userl,groupl,monindex):
    loginarray = []
    loginline = ""
    for i in range(0,len(userl)):#-1
        splittimes = datatime[loginpos[i]].split(" ")
        (tag,monat,jahr,stunde,minute,zeitindex) = zerlegezeit(splittimes)
        if monat == monindex: 
            loginline = userl[i]+","+groupl[i]+","+str(tag)+","+str(monat)+","+str(jahr)+","+str(stunde)+","+str(minute)+","+str(zeitindex)
            loginarray.append(loginline)

    return(loginarray)

def procarray(datatimer,evtcoder,evtnamer,monindex):
    procedarray = []
    procedline = ""
    for i in range (0,len(datatimer)):#-1
        splittimes = datatimer[i].split(" ")
        (tag,monat,jahr,stunde,minute,zeitindex) = zerlegezeit(splittimes)
        if evtcoder[i] == "1074":
            evtnamer[i] = "Shutdown"
        if evtcoder[i] == "6005":
            evtnamer[i] = "System Startup"
        if evtcoder[i] == "6009":
            evtnamer[i] = "Startup"
        if monat == monindex:
            procedline = evtcoder[i]+","+evtnamer[i]+","+str(tag)+","+str(monat)+","+str(jahr)+","+str(stunde)+","+str(minute)+","+str(zeitindex)
            procedarray.append(procedline)
    return (procedarray)

def calctime(final,monindex):
    zeiten = []
    if len(final[0]) < 10:
        del final[0]
    for i in range(0,len(final)):
        a = final[i].split(",")
        if len(a)<18 and a[4] == str(monindex):
            difmin = int(a[16])-int(a[8])
            result = final[i]+","+str(difmin)+"\n"
            zeiten.append(result)
    zeiten = np.unique(zeiten)

    return(zeiten)

def savedata(zeiten,filename,instrument,monchoice,jahreingabe):
    a = filename.split("/")
    del a[-1]
    b = "/".join(list(a))
    
    dataname = b+"/"+instrument+"_"+monchoice+"_"+jahreingabe+".csv"
    
    print ("saved as: ",dataname)
    
    with open(dataname, "w") as f:
        f.write(kopf)
        for i in range(0,len(zeiten)):
            f.write (zeiten[i])
    f.close()

def browseFiles():
    
    instrument = instname.get()
    monchoice = monvar.get()
    jahreingabe = jahrentry.get()
    monindex = monatnamen.index(monchoice)+1
    
    print (instrument," Monat: ",monchoice,",Jahr: ",jahreingabe)
    
    (datatime,evtcode,evtname,details,filename) = loadthedata(instrument)
    (datatimer,evtcoder,evtnamer,detailsr) = splitforprocess(filename)

    (loginpos,userl,groupl) = findeuser2(details,evtname)

    loginarray = logindata(datatime,loginpos,userl,groupl,monindex)
    loginarray = np.unique(loginarray)
    
    procedarray = procarray(datatimer,evtcoder,evtnamer,monindex)
    procedarray = np.unique(procedarray)

    ausgabe = []
    for i in range(0,len(loginarray)):#-1
        ausgabe.append(loginarray[i]+"\n")
    for i in range(0,len(procedarray)):#-1
        ausgabe.append(procedarray[i]+"\n")
        
    savedata(ausgabe,filename,instrument,monchoice,jahreingabe)


window = tk.Tk()
window.title('Logdata Import')
window.geometry("300x200")
frame=tk.Frame(window)
frame.pack()

labelmonth = tk.Label(frame, text="Monat:")
labelmonth.pack()

monvar = tk.StringVar(frame)
monvar.set(monatnamen[0])
monmenu = tk.OptionMenu(frame, monvar, *monatnamen)
monmenu.pack()

labelinst = tk.Label(frame, text="Instrument:")
labelinst.pack()

instname = tk.StringVar(frame)
instname.set(instruments[0])
instmenu = tk.OptionMenu(frame, instname, *instruments)
instmenu.pack()

labelJahr = tk.Label(frame, text="Jahr eingeben:")
labelJahr.pack()

jahrentry= tk.Entry(frame,text = "Jahr")
jahrentry.pack()

button_explore = tk.Button(frame,text = "Logfile:",command = browseFiles)
button_explore.pack()

button_close = tk.Button(frame, text='Quit', command=window.destroy)
button_close.pack()

window.mainloop()
