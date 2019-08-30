version=3.1


import random as r
import os
import datetime
import subprocess
import re
import math
from operator import itemgetter, attrgetter
from copy import deepcopy
from FunctionDefinitions import *
from ClassDefinitions import *
from Presets import *
from tkinter import *
from tkinter import messagebox
import tkinter


class InitiativeGUI():
    def __init__(self,master,Info={},Combatants=[["No current combatants","N/A",""]],Bestiary={}):
        self.master=master
        self.master.resizable(True,True)
        #self.master.config(height=75,width=30)
        self.TurnCount=0
        self.CurrentTurn=-1
        self.Info=Info
        self.Combatants=Combatants
        self.Bestiary=Bestiary
        self.DisplayedStats={}
        self.PinIndex=2

        self.CanRemove='disabled'
        
        
        self.AutoRemove=False
        self.VulnerabilityModifier=2
        self.Randomise=True
        self.DoPrintStats=True
        self.SortDisplay='alphabetic'
        
        
        self.InitiativeList=PanedWindow(self.master)
        self.InitiativeList.pack(fill=BOTH, expand=1)
        #self.InitiativeList.config(height=350,width=750,sashwidth=5)
        self.Frame1=Frame(self.InitiativeList)
        self.Text1=Text(self.Frame1)
        self.InitiativeList.add(self.Frame1)        
        self.Functions=PanedWindow(self.InitiativeList)
        self.InitiativeList.add(self.Functions)

        self.InitiativeList.config(height=350,width=710,sashwidth=5)
        self.InitiativeList.paneconfigure(self.Frame1,width=450)
        self.InitiativeList.paneconfigure(self.Functions,width=250)

        self.TitleText=Text(self.Functions,width=30,height=7,pady=10,relief='raised',bg='light blue')
        self.TitleText.insert(1.0,"Initiative "+str(version)+"\n","title")
        self.TitleText.insert(2.0,"Round: "+str(self.TurnCount+1)+'\n',"round")
        self.TitleText.tag_config("title",font=("Helvetica",20,"bold italic"),justify='center')
        self.TitleText.tag_config("round",font=("Helvetica",14,"bold"),justify='center')
        self.TitleText.grid(row=1,column=1,rowspan=4,columnspan=10)

        self.Next=Button(self.Frame1,text="Next",command=self.NextTurn)
        self.Next.pack(side= BOTTOM)


        self.Add=Button(self.Functions,text="Add",command=self.Add)
        self.Minions=Button(self.Functions,text="Minions",command=self.Minions)
        self.Damage=Button(self.Functions,text="Damage",state=self.CanRemove,command=self.Damage)
        self.Healing=Button(self.Functions,text="Healing",state=self.CanRemove,command=self.Healing)
        self.Preset=Button(self.Functions,text="Preset",command=self.Preset)
        self.Remove=Button(self.Functions,text="Remove",state=self.CanRemove,command=self.Remove)
        self.Settings=Button(self.Functions,text="Settings",command=self.Settings)
        self.Quit=Button(self.Functions,text="Quit",command=self.Quit)

        self.Add.grid(row=10,column=1)
        self.Minions.grid(row=10,column=2)
        self.Preset.grid(row=10,column=3)
        self.Damage.grid(row=11,column=1)
        self.Healing.grid(row=11,column=2)
        self.Remove.grid(row=11,column=3)
        self.Settings.grid(row=12,column=1)
        self.Quit.grid(row=12,column=2)


        self._CreateDisplay()
        self.master.mainloop()

    def _CheckRemoval(self):
        if self.CurrentTurn<0:
            self.CanRemove='disabled'
        else:
            self.CanRemove='normal'
        self.Damage.config(state=self.CanRemove)
        self.Remove.config(state=self.CanRemove)
        self.Healing.config(state=self.CanRemove)

    def _CreateDisplay(self):
        self.CurrentRow=0
        self.PCombatants=DisplayCombatants(self.Combatants)
        for Combatant in self.PCombatants:
            tag=str(self.CurrentRow)
            self.Text1.insert(END,Combatant,(tag))
            self.CurrentRow+=1
        self.Text1.tag_config(str(self.CurrentTurn),background="yellow")
        self.Text1.pack()

##        self.Next=Button(self.Frame1,text="Next",command=self.NextTurn)
##        self.Next.pack(side= BOTTOM)

    def _RecreateDisplay(self):
        for i in range(0,len(self.Combatants)):
            self.Text1.tag_config(str(i),background="white")
        self.Text1.delete(1.0,END)
        self._CreateDisplay()
        self.TitleText.delete(2.0,END)
        self.TitleText.insert(END,'\n')
        self.TitleText.insert(2.0,"Round: "+str(self.TurnCount+1)+'\n',"round")
        self._CheckRemoval()
        self.master.update_idletasks()
        
    def NextTurn(self):
        self.CurrentTurn+=1
        if self.CurrentTurn>=len(self.Combatants):
            self.CurrentTurn=-1
            self.TurnCount+=1
            if self.Randomise==True:
                for Combatant in self.Info:
                    self.Info[Combatant]=InitiativeRoll(self.Info[Combatant],self.TurnCount)
            self.Combatants=Initialise(self.Info)
            self._RecreateDisplay()
            
        else:    
            self.Text1.tag_config(str(self.CurrentTurn-1),background="white")
            self.Text1.tag_config(str(self.CurrentTurn),background="yellow")
            name=self.Combatants[self.CurrentTurn][0]
            self._CheckRemoval()
            if self.DoPrintStats==True and 'Bestiary' in self.Info[name] and not self.DisplayedStats[self.Info[name]['Bestiary']].get():
                PrintGUI=Toplevel()
                self.DisplayedStats[self.Info[name]['Bestiary']].set(True)
                #self.DisplayedStats[self.Info[name]['Bestiary']].trace_add("write",  self.callback2)
                Stats=PrintStatsGUI(PrintGUI,self.Bestiary,self.Info[name]['Bestiary'])
                self.DisplayedStats[self.Info[name]['Bestiary']]=Stats.IsOpen
                Stats.master.protocol("WM_DELETE_WINDOW",Stats.callback)
                #Stats.IsOpen.trace_add("write",  self.callback2)

    #def callback2(self,*dummy): #name,index,mode
    #    for Name in self.DisplayedStats:
    #        self.DisplayedStats[Name].set(False)        


    def _Add(self,Dictionary):
        self.Info.update(Dictionary)
        for Combatant in Dictionary:
            self.Combatants,self.CurrentTurn=AddToInitiative(Dictionary[Combatant],self.Combatants,self.CurrentTurn,False,True)
        self._RecreateDisplay()

    def _Remove(self,Name):
        if self.Info[Name]['Initiative']>self.Combatants[self.CurrentTurn][1]:
            self.CurrentTurn-=1
        del self.Info[Name]
        self.Combatants=Initialise(self.Info)
        self._RecreateDisplay()

    def _Damage(self,Dictionary):
        for Combatant in Dictionary:
            if "HP" in self.Info[Combatant]:
                if Dictionary[Combatant]>0:
                    temp=self.Info[Combatant].get("TempHP",0)
                    damage=Dictionary[Combatant]
                    self.Info[Combatant]["TempHP"],damage=max(temp-damage,0),max(damage-temp,0)
                    self.Info[Combatant]["HP"]-=damage
                    if self.Info[Combatant]["HP"]<=0:
                        if messagebox.askokcancel("Remove",Combatant+" has died. Do you want to remove them from initiative?") or self.AutoRemove==True:
                            self._Remove(Combatant)
                else:
                    self.Info[Combatant]["HP"]-=Dictionary[Combatant]
                    if self.Info[Combatant]["HP"]>self.Info[Combatant]["MaxHP"]:
                        self.Info[Combatant]["HP"]=self.Info[Combatant]["MaxHP"]

                    
        self.Combatants=Initialise(self.Info)
        self._RecreateDisplay()

    def _TempHP(self,Dictionary):
        for Combatant in Dictionary:
            if "HP" in self.Info[Combatant]:
                self.Info[Combatant]["TempHP"]=max(self.Info[Combatant].get("TempHP",0),Dictionary[Combatant],0)
        self.Combatants=Initialise(self.Info)
        self._RecreateDisplay()

    def _Settings(self,Settings):
        self.Randomise=Settings["Randomise"]
        self.AutoRemove=Settings["AutoRemove"]
        self.VulnerabilityModifier=Settings["VulnerabilityModifier"]
        self.SortDisplay=Settings["SortDisplay"]

    def _Pin(self,creature):
        PinWindow=PanedWindow(self.InitiativeList,orient='vertical')
        self.InitiativeList.add(PinWindow)
        #PinFrame=Frame(PinWindow)
        #PinFrame.pack()
        Pin=PrintStatsPin(PinWindow,self.Bestiary,creature,len(self.master.winfo_children()))
        self.DisplayedStats[creature]=Pin.IsOpen
        self.InitiativeList.config(height=500,width=1415,sashwidth=5)
        #self.InitiativeList.childconfigure(PinWindow,width=500)
        #Unpinbutton=Button(PinWindow,text="Unpin",command=Pin.unpin)
        #Unpinbutton.pack(side=BOTTOM)
        self.master.update_idletasks()

    def _SortCombatantsForGUI(self):
        Combatants=[Combatant[0] for Combatant in self.Combatants if len(Combatant)>=4]
        if self.SortDisplay=='alphabetic':
            Combatants.sort()
        return Combatants
        
    def Add(self):
        Notebook=Toplevel()
        GUI=AddGUI(Notebook,self.Bestiary,self.TurnCount)
        self.master.wait_window(GUI.master)
        if len(GUI.ToAdd)!=0:
            self._Add(GUI.ToAdd)
        if len(GUI.Bestiary)!=0:
            self.Bestiary.update(GUI.Bestiary)
            for entry in GUI.Bestiary:
                if entry not in self.DisplayedStats:
                    self.DisplayedStats[entry]=BooleanVar()
                    self.DisplayedStats[entry].set(False)
        if GUI.Pin!='':
            self._Pin(GUI.Pin)
            self.DisplayedStats[GUI.Pin].set(True)


    def Minions(self):
        Notebook=Toplevel()
        GUI=MinionsGUI(Notebook,self.Bestiary,self.TurnCount)
        self.master.wait_window(GUI.master)
        if len(GUI.ToAdd)!=0:
            self._Add(GUI.ToAdd)
        if len(GUI.Bestiary)!=0:
            self.Bestiary.update(GUI.Bestiary)
            for entry in GUI.Bestiary:
                if entry not in self.DisplayedStats:
                    self.DisplayedStats[entry]=BooleanVar()
                    self.DisplayedStats[entry].set(False)
        if GUI.Pin!='':
            self._Pin(GUI.Pin)
            self.DisplayedStats[GUI.Pin].set(True)



    def Damage(self):
        Notebook=Toplevel()
        Combatants=self._SortCombatantsForGUI()
        GUI=DamageGUI(Notebook,Combatants,self.VulnerabilityModifier)
        self.master.wait_window(GUI.master)
        if len(GUI.damages)!=0:
            self._Damage(GUI.damages)

    def Healing(self):
        Notebook=Toplevel()
        Combatants=self._SortCombatantsForGUI()
        GUI=HealingGUI(Notebook,Combatants)
        self.master.wait_window(GUI.master)
        self._Damage(GUI.healing)
        self._TempHP(GUI.tempHP)

    def Preset(self):
        Notebook=Toplevel()
        GUI=PresetGUI(Notebook)
        self.master.wait_window(GUI.master)
        if len(GUI.Settings)!=0:
            self._Settings(GUI.Settings)
        if len(GUI.Preset)!=0:
            self._Add(GUI.Preset)
        
    def Remove(self):
        Notebook=Toplevel()
        Combatants=self._SortCombatantsForGUI()
        GUI=RemoveGUI(Notebook,Combatants)
        self.master.wait_window(GUI.master)
        if len(GUI.ToRemove)!=0:
            for name in GUI.ToRemove:
                self._Remove(name)

    def Settings(self):
        Notebook=Toplevel()
        GUI=SettingsGUI(Notebook)
        self.master.wait_window(GUI.master)
        if len(GUI.Settings)!=0:
            self._Settings(GUI.Settings)

    def Quit(self):
        self.master.destroy()


master=tkinter.Tk()
master.title("Initiative")
Initiative=InitiativeGUI(master)

