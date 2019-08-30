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
import tkinter
from tkinter import font



class AddGUI():
    def __init__(self, master,Bestiary,TurnCount):
        self.master=master
        self.master.title("Add")
        self.Bestiary=Bestiary
        self.TurnCount=TurnCount
        self.ToAdd={}
        self.Pin=''
        self.ToPin=BooleanVar()
        self.ToPin.set(False)

        self.IsPlayer=BooleanVar()
        
        self.PlayerLabel=Label(self.master,text="Is this a player?")
        self.PlayerBox=Checkbutton(self.master,variable=self.IsPlayer, onvalue=True, offvalue=False,command=self.callback)
        self.PlayerLabel.grid(row=1,column=1,columnspan=2)
        self.PlayerBox.grid(row=1,column=3,columnspan=2)
        

        self.Name=StringVar()
        self.NameLabel=Label(self.master,text="Enter creature name:")
        self.NameBox=Entry(self.master,textvariable=self.Name, state=NORMAL)
        self.NameLabel.grid(row=2,column=1,columnspan=2)
        self.NameBox.grid(row=2,column=3,columnspan=2)

        self.IsBestiary=BooleanVar()
        
        self.IsBestiaryLabel=Label(self.master,text="Import stats from bestiary?")
        self.IsBestiaryBox=Checkbutton(self.master,variable=self.IsBestiary, onvalue=True, offvalue=False)
        self.IsBestiaryLabel.grid(row=3,column=1,columnspan=2)
        self.IsBestiaryBox.grid(row=3,column=3,columnspan=2)

        self.CurrentRow=4

        self.BestiaryName=StringVar()
        self.BestiaryLabel=Label(self.master,text="Enter name from bestiary:")
        self.BestiaryBox=Entry(self.master,textvariable=self.BestiaryName, state=NORMAL)
        self.BestiaryLabel.grid(row=self.CurrentRow,column=1,columnspan=2)
        self.BestiaryBox.grid(row=self.CurrentRow,column=3,columnspan=2)

        self.CurrentRow+=1
            
        self.Import=Button(self.master,text="Import stats",command=self.callback2)
        self.Import.grid(row=self.CurrentRow,column=1, columnspan=2)

        self.CurrentRow+=1
        
        self.Dex=StringVar()
        self.DexLabel=Label(self.master,text="Enter creature's dexterity modifier:")
        self.DexBox=Entry(self.master,textvariable=self.Dex, state=NORMAL)
        self.DexLabel.grid(row=self.CurrentRow,column=1,columnspan=2)
        self.DexBox.grid(row=self.CurrentRow,column=3,columnspan=2)

        self.CurrentRow+=1
        
        self.FirstTurn=StringVar()
        self.FirstTurnLabel=Label(self.master,text="Enter creature's first turn bonus to initiative:")
        self.FirstTurnBox=Entry(self.master,textvariable=self.FirstTurn, state=NORMAL)
        self.FirstTurnLabel.grid(row=self.CurrentRow,column=1,columnspan=2)
        self.FirstTurnBox.grid(row=self.CurrentRow,column=3,columnspan=2)        

        self.CurrentRow+=1
        
        self.HP=StringVar()
        self.HPLabel=Label(self.master,text="Enter creature's hit points:")
        self.HPBox=Entry(self.master,textvariable=self.HP, state=NORMAL)
        self.HPLabel.grid(row=self.CurrentRow,column=1,columnspan=2)
        self.HPBox.grid(row=self.CurrentRow,column=3,columnspan=2)

        self.CurrentRow+=1

        self.Initiative=StringVar()
        self.InitiativeLabel=Label(self.master,text="Enter creature's initiative roll:")
        self.InitiativeBox=Entry(self.master,textvariable=self.Initiative, state=NORMAL)
        self.InitiativeLabel.grid(row=self.CurrentRow,column=1,columnspan=2)
        self.InitiativeBox.grid(row=self.CurrentRow,column=3,columnspan=2)

        
        Apply=Button(self.master,text="Add to initiative",command = self.Add)
        Apply.grid(row=self.CurrentRow+1,column=1,columnspan=2)
        Cancel=Button(self.master,text="Cancel",command = self.quit)
        Cancel.grid(row=self.CurrentRow+1,column=3,columnspan=2)

    def callback(self):
        if self.IsPlayer.get()==True:
            self.HPBox.configure(state='disabled')
        else:
            self.HPBox.configure(state='normal')
        self.master.update_idletasks()
            
    def callback2(self):
        
        #Currently, the script will only add the bestiary info if you also click the "Import stats from bestiary" checkbox. Just a safeguard against accidentally clicking "import" button.
        if self.IsBestiary.get()==True:
            try:
                BestiaryName=ProcessBestiaryName(self.BestiaryName.get())
                self.Bestiary=AddBestiary(self.Bestiary,BestiaryName)
                self.ToAdd[self.Name.get()]=self.Bestiary[BestiaryName]
                self.Dex.set(int(self.ToAdd[self.Name.get()]['DEX'].split('(')[1].split(')')[0]))
                self.FirstTurn.set(self.Dex.get())
                self.DefaultHP=Label(self.master,text="Default is: "+self.ToAdd[self.Name.get()]['Hit Points'])
                self.DefaultHP.grid(row=self.CurrentRow-1,column=5,columnspan=3)
                DefaultHP=self.Bestiary[BestiaryName]['Hit Points'].split('(')[1].strip(')')
                self.HP.set(DefaultHP)
                self.DexBox.configure(state='disabled')
                self.FirstTurnBox.configure(state='disabled')

        
                self.ToPinLabel=Label(self.master,text="Pin creature to main page?")
                self.ToPinBox=Checkbutton(self.master,variable=self.ToPin, onvalue=True, offvalue=False)
                self.ToPinLabel.grid(row=3,column=5,columnspan=2)
                self.ToPinBox.grid(row=3,column=7,columnspan=2)

                
            except Exception as e:
                print(str(e))
                self.Warning=Label(self.master,text="Name not valid, try again")
                self.Warning.grid(row=5,column=5,columnspan=2)


        else:
            self.DexBox.configure(state='normal')
            self.FirstTurnBox.configure(state='normal')
        self.master.update_idletasks()
        
    def quit(self):
        self.ToAdd={}
        self.master.destroy()
        
    def Add(self):
        Name=self.Name.get()
        if len(self.ToAdd)==0:
            self.ToAdd[Name]={}
        self.ToAdd[Name]['Name']=self.Name.get()
        self.ToAdd[Name]['DexterityMod']=int(self.Dex.get())
        self.ToAdd[Name]['FirstTurnBonus']=int(self.FirstTurn.get())
        if self.Initiative.get()!='':
            self.ToAdd[Name]['Initiative']=int(self.Initiative.get())
        else:
            self.ToAdd[Name]['Initiative']=0
            self.ToAdd[Name]=InitiativeRoll(self.ToAdd[Name],self.TurnCount)
        if self.IsBestiary.get():
            self.ToAdd[Name]['Bestiary']=ProcessBestiaryName(self.BestiaryName.get())
        if self.HP.get()!='':
            self.ToAdd[Name]['HP']=Roll(self.HP.get(),verbose=False)
            self.ToAdd[Name]['MaxHP']=int(self.ToAdd[Name]['HP'])
        if self.ToPin.get():
            self.Pin=ProcessBestiaryName(self.BestiaryName.get())
        self.master.destroy()


########################################################################################################
class MinionsGUI():
    def __init__(self, master,Bestiary,TurnCount):
        self.master=master
        self.master.title("Add")
        self.ToAdd={}
        self.Bestiary=Bestiary
        self.TurnCount=TurnCount
        self.Pin=''
        self.ToPin=BooleanVar()
        self.ToPin.set(False)



        self.Name=StringVar()
        self.NameLabel=Label(self.master,text="Enter base creature name:")
        self.NameBox=Entry(self.master,textvariable=self.Name, state=NORMAL)
        self.NameLabel.grid(row=1,column=1,columnspan=2)
        self.NameBox.grid(row=1,column=3,columnspan=2)

        self.First=StringVar()
        self.FirstLabel=Label(self.master,text="Enter index of first creature:")
        self.FirstBox=Entry(self.master,textvariable=self.First, state=NORMAL)
        self.FirstLabel.grid(row=2,column=1,columnspan=2)
        self.FirstBox.grid(row=2,column=3,columnspan=2)

        self.Last=StringVar()
        self.LastLabel=Label(self.master,text="Enter index of last creature:")
        self.LastBox=Entry(self.master,textvariable=self.Last, state=NORMAL)
        self.LastLabel.grid(row=3,column=1,columnspan=2)
        self.LastBox.grid(row=3,column=3,columnspan=2)

        self.CurrentRow=4

        self.DefaultHP=StringVar()
        self.DefaultHPLabel=Label(self.master,text="Enter base hit points value:")
        self.DefaultHPBox=Entry(self.master,textvariable=self.DefaultHP, state=NORMAL)
        self.DefaultHPLabel.grid(row=self.CurrentRow,column=1,columnspan=2)
        self.DefaultHPBox.grid(row=self.CurrentRow,column=3,columnspan=2)        

        self.CurrentRow+=1

        self.IsBestiary=BooleanVar()
        
        self.IsBestiaryLabel=Label(self.master,text="Import stats from bestiary?")
        self.IsBestiaryBox=Checkbutton(self.master,variable=self.IsBestiary, onvalue=True, offvalue=False)
        self.IsBestiaryLabel.grid(row=self.CurrentRow,column=1,columnspan=2)
        self.IsBestiaryBox.grid(row=self.CurrentRow,column=3,columnspan=2)

        self.CurrentRow+=1

        self.BestiaryName=StringVar()
        self.BestiaryLabel=Label(self.master,text="Enter name from bestiary:")
        self.BestiaryBox=Entry(self.master,textvariable=self.BestiaryName, state=NORMAL)
        self.BestiaryLabel.grid(row=self.CurrentRow,column=1,columnspan=2)
        self.BestiaryBox.grid(row=self.CurrentRow,column=3,columnspan=2)

        self.CurrentRow+=1
           
        self.Import=Button(self.master,text="Import stats",command=self.callback2)
        self.Import.grid(row=self.CurrentRow,column=1, columnspan=2)

        self.Update=Button(self.master,text="Manual input",command=self.callback3)
        self.Update.grid(row=self.CurrentRow,column=3, columnspan=2)

        self.CurrentRow+=1
        
        self.Dex=StringVar()
        self.DexLabel=Label(self.master,text="Enter creature's base dexterity modifier:")
        self.DexBox=Entry(self.master,textvariable=self.Dex, state=NORMAL)
        self.DexLabel.grid(row=self.CurrentRow,column=1,columnspan=2)
        self.DexBox.grid(row=self.CurrentRow,column=3,columnspan=2)

        self.CurrentRow+=1
        
        self.FirstTurn=StringVar()
        self.FirstTurnLabel=Label(self.master,text="Enter creature's base first turn bonus to initiative:")
        self.FirstTurnBox=Entry(self.master,textvariable=self.FirstTurn, state=NORMAL)
        self.FirstTurnLabel.grid(row=self.CurrentRow,column=1,columnspan=2)
        self.FirstTurnBox.grid(row=self.CurrentRow,column=3,columnspan=2)

        self.CurrentRow+=1
        
        Apply=Button(self.master,text="Add to initiative",command = self.Add)
        Apply.grid(row=100,column=1,columnspan=2)
        Cancel=Button(self.master,text="Cancel",command = self.quit)
        Cancel.grid(row=100,column=3,columnspan=2)

    def callback(self):
        if self.IsPlayer.get()==True:
            self.HPBox.configure(state='disabled')
        else:
            self.HPBox.configure(state='normal')
        self.master.update_idletasks()
            
    def callback2(self):
        #Currently, the script will only add the bestiary info if you also click the "Import stats from bestiary" checkbox. Just a safeguard against accidentally clicking "import" button
        if self.IsBestiary.get()==True:
            try:
                BaseName=ProcessInput(self.Name.get())
                BestiaryName=ProcessBestiaryName(self.BestiaryName.get())
                self.Bestiary=AddBestiary(self.Bestiary,BestiaryName,False)
                self.Dex.set(int(self.Bestiary[BestiaryName]['DEX'].split('(')[1].split(')')[0]))
                self.FirstTurn.set(self.Dex.get())
                self.DefaultHP=Label(self.master,text="Default is: "+self.Bestiary[BestiaryName]['Hit Points'])
                self.DefaultHP.grid(row=self.CurrentRow,column=2,columnspan=3)
                self.DexBox.configure(state='disabled')
                self.FirstTurnBox.configure(state='disabled')
                self.DefaultHPBox.configure(state='disabled')
                DefaultHP=self.Bestiary[BestiaryName]['Hit Points'].split('(')[1].strip(')')

                        
                self.ToPinLabel=Label(self.master,text="Pin creature to main page?")
                self.ToPinBox=Checkbutton(self.master,variable=self.ToPin, onvalue=True, offvalue=False)
                self.ToPinLabel.grid(row=5,column=5,columnspan=2)
                self.ToPinBox.grid(row=5,column=7,columnspan=2)
                
                for i in range(int(self.First.get()),int(self.Last.get())+1):
                    Name=ProcessInput(BaseName+" "+str(i))              
                    self.ToAdd[Name]=deepcopy(self.Bestiary[BestiaryName])
                    self.ToAdd[Name]['Name']=Name
                    self.CurrentRow+=1
                    self.ToAdd[Name]['Bestiary']=BestiaryName

                    
                    self.ToAdd[Name]["HP"]=StringVar()
                    self.HPLabel=Label(self.master,text="Enter "+Name+"'s hit points:")
                    self.HPBox=Entry(self.master,textvariable=self.ToAdd[Name]["HP"], state=NORMAL)
                    self.ToAdd[Name]["HP"].set(DefaultHP)
                    self.HPLabel.grid(row=self.CurrentRow,column=1,columnspan=2)
                    self.HPBox.grid(row=self.CurrentRow,column=3,columnspan=2)                   
                    
            except Exception as e:
                print(str(e))
                self.Warning=Label(self.master,text="Name not valid, try again")
                self.Warning.grid(row=5,column=5,columnspan=2)


        else:
            self.DexBox.configure(state='normal')
            self.FirstTurnBox.configure(state='normal')
        self.master.update_idletasks()

    def callback3(self):
        BaseName=str(ProcessInput(self.Name.get()))
        for i in range(int(self.First.get()),int(self.Last.get())+1):
            Name=ProcessInput(BaseName+" "+str(i))              
            self.ToAdd[Name]={}
            self.ToAdd[Name]['Name']=Name
            self.CurrentRow+=1
            self.ToAdd[Name]["HP"]=StringVar()
            self.HPLabel=Label(self.master,text="Enter "+Name+"'s hit points:")
            self.HPBox=Entry(self.master,textvariable=self.ToAdd[Name]["HP"], state=NORMAL)
            self.ToAdd[Name]["HP"].set(str(self.DefaultHP.get()))
            self.HPLabel.grid(row=self.CurrentRow,column=1,columnspan=2)
            self.HPBox.grid(row=self.CurrentRow,column=3,columnspan=2) 
        
    def quit(self):
        self.Bestiary={}
        self.ToAdd={}
        self.master.destroy()
        
    def Add(self):
        for Name in self.ToAdd:
            self.ToAdd[Name]['DexterityMod']=int(self.Dex.get())
            self.ToAdd[Name]['FirstTurnBonus']=int(self.FirstTurn.get())
            self.ToAdd[Name]["HP"]=int(Roll(self.ToAdd[Name]["HP"].get(),verbose=False))
            self.ToAdd[Name]["MaxHP"]=int(self.ToAdd[Name]["HP"])
            self.ToAdd[Name]['Initiative']=0
            self.ToAdd[Name]=InitiativeRoll(self.ToAdd[Name],self.TurnCount)
        if self.ToPin.get():
            self.Pin=ProcessBestiaryName(self.BestiaryName.get())
        self.master.destroy()

################################################################################################

class DamageGUI():
    def __init__(self, master,Combatants,VulnerabilityModifier):
        self.master=master
        self.damages = None
        self.Combatants=Combatants


        self.Modifiers = {}
        for Combatant in self.Combatants:
            self.Modifiers[Combatant]={"DamageMultiplier":0,"ResistanceMultiplier":1}
        self.Damage=StringVar()
        self.Damage.set('0')
        DamageLabel=Label(self.master,text="How much damage was dealt?")
        DamageBox=Entry(self.master,textvariable=self.Damage)
        DamageLabel.grid(row=0,column=1,pady=20,columnspan=2)
        DamageBox.grid(row=0,column=3,pady=20,columnspan=2)


        Text=Label(self.master,text="Which combatants were damaged?")
        Text.grid(row=1,columnspan=5)

        FullLabel=Label(self.master,text="Full damage")
        FullLabel.grid(row=2,column=1)
        HalfLabel=Label(self.master,text="Half damage")
        HalfLabel.grid(row=2,column=2)
        ResistanceLabel=Label(self.master,text="Resistance")
        ResistanceLabel.grid(row=2,column=3)
        VulnerabilityLabel=Label(self.master,text="Vulnerability")
        VulnerabilityLabel.grid(row=2,column=4)

        CurrentRow=3
        for Combatant in self.Combatants:
            self.Modifiers[Combatant]["DamageMultiplier"]=DoubleVar()
            self.Modifiers[Combatant]["ResistanceMultiplier"]=DoubleVar()
            self.Modifiers[Combatant]["ResistanceMultiplier"].set(1)
            FullDamage = Checkbutton(self.master, variable = self.Modifiers[Combatant]["DamageMultiplier"], \
                         onvalue = 1, offvalue = 0, height=1, \
                         width = 10)
            HalfDamage = Checkbutton(self.master, variable = self.Modifiers[Combatant]["DamageMultiplier"], \
                         onvalue = 0.5, offvalue = 0, height=1, \
                         width = 10)
            Resistance = Checkbutton(self.master, variable = self.Modifiers[Combatant]["ResistanceMultiplier"], \
                         onvalue = 0.5, offvalue = 1, height=1, \
                         width = 10)
            Vulnerability = Checkbutton(self.master, variable = self.Modifiers[Combatant]["ResistanceMultiplier"], \
                         onvalue = VulnerabilityModifier, offvalue = 1, height=1, \
                         width = 10)
            Name=Label(self.master,text=Combatant)
            FullDamage.grid(row=CurrentRow,column=1,pady=0)
            HalfDamage.grid(row=CurrentRow,column=2,pady=0)
            Resistance.grid(row=CurrentRow,column=3,pady=0)
            Vulnerability.grid(row=CurrentRow,column=4,pady=0)
            Name.grid(row=CurrentRow,column=0,pady=0,padx=20)
            CurrentRow+=1

        Apply=Button(self.master,text="Apply",command = self.AddDamages)
        Apply.grid(row=CurrentRow,column=1,columnspan=2)
        Cancel=Button(self.master,text="Cancel",command = self.quit)
        Cancel.grid(row=CurrentRow,column=3,columnspan=2)

    def quit(self):
        self.damages={}
        self.master.destroy()
        
    def AddDamages(self):
        damages={}
        damage=int(Roll(self.Damage.get(),verbose=False))
        for Combatant in self.Combatants:
            damages[Combatant]=int(round(self.Modifiers[Combatant]["DamageMultiplier"].get()*self.Modifiers[Combatant]["ResistanceMultiplier"].get()*damage,1))
        self.damages=damages
        self.master.destroy()

#################################################################################################
        
class PresetGUI():
    def __init__(self, master):
        self.master=master
        self.master.title("Preset")

        self.PresetName=StringVar()
        
        self.PresetLabel=Label(self.master,text="Choose a preset:")
        self.PresetBox=Listbox(self.master, state=NORMAL)
        self.PresetLabel.grid(row=1,column=1,columnspan=2)
        self.PresetBox.grid(row=2,column=1,columnspan=2)
        self.CurrentRow=3
        for option in Presets:
            self.PresetBox.insert(1,option)
            self.CurrentRow+=1
        self.PresetBox.bind("<<ListboxSelect>>",self.on_selection)
        self.Import=Button(self.master,text="Import preset",command=self.callback)
        self.Import.grid(row=self.CurrentRow,column=1, columnspan=2)
        self.Cancel=Button(self.master,text="Cancel",command = self.quit)
        self.Cancel.grid(row=self.CurrentRow,column=3,columnspan=2)
    

    def on_selection(self,event):
        i=self.PresetBox.curselection()[0]
        self.text=self.PresetBox.get(i)



    def callback(self):
        self.PresetBox.unbind("<<ListboxSelect>>")
        self.CurrentRow=1
        self.PresetLabel.grid_forget()
        self.PresetBox.grid_forget()
        self.Import.grid_forget()
        self.Cancel.grid_forget()
        self.Preset=Presets[self.text]['Initiative']
        self.Settings=Presets[self.text]['Settings']
        self.InitiativeLabel=Label(self.master,text="Enter initiative rolls for the combatants:")
        self.InitiativeLabel.grid(row=self.CurrentRow,column=1,columnspan=4)
        self.CurrentRow+=1
        for Combatant in self.Preset:
            self.Preset[Combatant]['Initiative']=StringVar()
            InitiativeLabel=Label(self.master,text=Combatant)
            InitiativeBox=Entry(self.master,textvariable=self.Preset[Combatant]['Initiative'])
            InitiativeLabel.grid(row=self.CurrentRow,column=1,columnspan=2)
            InitiativeBox.grid(row=self.CurrentRow,column=3)
            self.CurrentRow+=1
        self.Apply=Button(self.master,text="Add to initiative",command=self.apply)
        self.Apply.grid(row=self.CurrentRow,column=1,columnspan=2)
        self.Cancel.grid(row=self.CurrentRow,column=3,columnspan=2)
        self.master.update_idletasks()

    def apply(self):
        for Combatant in self.Preset:
            self.Preset[Combatant]['Initiative']=int(self.Preset[Combatant]['Initiative'].get())
        self.master.destroy()
        
    def quit(self):
        self.Preset={}
        self.Settings={}
        self.master.destroy()

##############################################################################################################
        
class RemoveGUI():
    def __init__(self, master,Combatants):
        self.master=master
        self.Combatants=Combatants

        self.ToRemove = {}

        Text=Label(self.master,text="Remove which combatants?")
        Text.grid(row=1,columnspan=5)

        CurrentRow=2
        for Combatant in self.Combatants:
            self.ToRemove[Combatant]=BooleanVar()
            self.ToRemove[Combatant].set(False)
            RemoveBox = Checkbutton(self.master, variable = self.ToRemove[Combatant], \
                         onvalue = True, offvalue = False, height=1, \
                         width = 10)
            Name=Label(self.master,text=Combatant)
            RemoveBox.grid(row=CurrentRow,column=4,pady=0)
            Name.grid(row=CurrentRow,column=0,pady=0,padx=20)
            CurrentRow+=1

        Apply=Button(self.master,text="Apply",command = self.Remove)
        Apply.grid(row=CurrentRow,column=1,columnspan=2)
        Cancel=Button(self.master,text="Cancel",command = self.quit)
        Cancel.grid(row=CurrentRow,column=3,columnspan=2)

    def quit(self):
        self.ToRemove={}
        self.master.destroy()
        
    def Remove(self):
        Temp=[Combatant for Combatant in self.ToRemove if self.ToRemove[Combatant].get()==True]
        self.ToRemove=Temp
        self.master.destroy()

################################################################################

class PrintStatsGUI():
    def __init__(self,master,Bestiary,creature,index=99):
        self.master=master
        self.Bestiary=Bestiary
        self.creature=creature
        self.index=index
        self.master.title(self.creature)
        self.IsOpen=BooleanVar()
        self.IsOpen.set(True)

        self.NameFont=font.Font(family="Helvetica",size=20,weight='bold',slant='roman',underline=1)
        self.AbilityScoreFont=font.Font(family="helvetica",size=10,weight='normal',slant='roman',underline=0)
        self.AbilitiesFont=font.Font(family="helvetica",size=10,weight='bold',slant='roman',underline=0)
        self.SubAbilitiesFont=font.Font(family="helvetica",size=10,weight='normal',slant='italic',underline=0)
        self.TraitsFont=font.Font(family="Helvetica",size=10,weight='bold',slant='italic',underline=0)
        self.TextFont=font.Font(family="Helvetica",size=10,weight='normal',slant='roman',underline=0)
        self.ActionFont=font.Font(family="Helvetica",size=10,weight='bold',slant='roman',underline=0)
        self.PrintStats()

    def callback(self):
        self.IsOpen.set(False)
        self.master.destroy()

    def PrintStats(self):
        self.Frame1=Frame(self.master)
        self.Frame1.pack()
        self.Text1=Text(self.Frame1,spacing1=1,spacing3=1)
        self.Text1.pack()

        Info=self.Bestiary[self.creature]
        self.Text1.insert(1.0,self.creature.upper()+'\n','Name')
        self.Text1.insert(2.0,Info['Description'],'Abilities')
        
        StatText='{:^10} {:^10} {:^10} {:^10} {:^10} {:^10}'.format('STR','DEX','CON','INT','WIS','CHA')
        Stats='{:^10} {:^10} {:^10} {:^10} {:^10} {:^10}'.format(Info['STR'],Info['DEX'],Info['CON'],Info['INT'],Info['WIS'],Info['CHA'])
        Type=Info.get('type','')
        Size=Info.get('size','')
        CR=Info.get('CR','-').strip('cr')
        HP=Info.get('Hit Points','-')
        AC=Info.get('Armor Class','-')
        Speed=Info.get('Speed','-')
        Saves=Info.get('Saving Throws', 'None')
        Skills=Info.get('Skills', 'None')
        DamageResistances=Info.get('Damage Resistances', 'None')
        DamageImmunities=Info.get('Damage Immunities', 'None')
        ConditionImmunities=Info.get('Condition Immunities', 'None')
        Senses=Info.get('Senses', 'None')
        Languages=Info.get('Languages', 'None')

        self.Text1.insert(3.0,Size+" "+Type+'\n','Traits')

        self.Text1.insert(4.0,'AC:','Abilities')
        self.Text1.insert(END,AC+'\n','Text')

        self.Text1.insert(5.0,'Hit points:','Abilities')
        self.Text1.insert(END,HP+'\n','Text')

        self.Text1.insert(6.0,'Speed:','Abilities')
        self.Text1.insert(END,Speed+'\n','Text')

        self.Text1.insert(7.0,StatText+'\n','AbilityScore')
        
        self.Text1.insert(8.0,Stats+'\n','AbilityScore')
        
        self.Text1.insert(9.0,'Saving throws:','Abilities')
        self.Text1.insert(END,Saves+'\n','Text')

        self.Text1.insert("10.0",'Skills:','Abilities')
        self.Text1.insert(END,Skills+'\n','Text')

        self.Text1.insert("11.0",'Damage immunities:','Abilities')
        self.Text1.insert(END,DamageImmunities+'\n','Text')

        self.Text1.insert("12.0",'Damage resistances:','Abilities')
        self.Text1.insert(END,DamageResistances+'\n','Text')

        self.Text1.insert("13.0",'Senses:','Abilities')
        self.Text1.insert(END,Senses+'\n','Text')

        self.Text1.insert("14.0",'Languages:','Abilities')
        self.Text1.insert(END,Languages+'\n','Text')

        self.Text1.insert("15.0",'Challenge rating:','Abilities')
        self.Text1.insert(END,CR+'\n','Text')
        
        if 'Traits' in Info:
            for key in Info['Traits']:
                if type(Info['Traits'][key])==dict:
                    for subkey in Info['Traits'][key]:
                        #print('-'+key+': '+subkey+'\n')
                        self.Text1.insert(END,key+':','Traits')
                        self.Text1.insert(END,subkey+'\n','Text')
                        for subsubkey in Info['Traits'][key][subkey]:
                            #print('\t'+subsubkey+Info['Traits'][key][subkey][subsubkey])
                            self.Text1.insert(END,subsubkey+':','SubAbilities')
                            self.Text1.insert(END,Info['Traits'][key][subkey][subsubkey]+'\n','Text')
                else: #print('-'+key+': '+Info['Traits'][key]+'\n')
                    self.Text1.insert(END,key+':','Traits')
                    self.Text1.insert(END,Info['Traits'][key]+'\n','Text')
            #print('\n')
        if 'Actions' in Info:
            #print("Actions")
            self.Text1.insert(END,'Actions \n','Action')
            for key in Info['Actions']:
                if type(Info['Actions'][key])==dict:
                    for subkey in Info['Actions'][key]:
                        self.Text1.insert(END,key+':','Traits')
                        self.Text1.insert(END,subkey+'\n','Text')
                        #print('-'+key+': '+subkey+'\n')
                        for subsubkey in Info['Actions'][key][subkey]:
                            #print('\t'+subsubkey+Info['Actions'][key][subkey][subsubkey])
                            self.Text1.insert(END,subsubkey+':','SubAbilities')
                            self.Text1.insert(END,Info['Actions'][key][subkey][subsubkey]+'\n','Text')
                else: #print('-'+key+': '+Info['Actions'][key]+'\n')
                    self.Text1.insert(END,key+':','Traits')
                    self.Text1.insert(END,Info['Actions'][key]+'\n','Text')
           # print('\n')
        if 'Legendary Actions' in Info:
            #print("Legendary Actions")
            #print(Info['Traits']['Legendary Actions'])
            #print('\n')
            self.Text1.insert(END,'Legendary actions \n','Action')
            for key in Info['Legendary Actions']:
                if type(Info['Legendary Actions'][key])==dict:
                    for subkey in Info['Legendary Actions'][key]:
                        #print('-'+key+': '+subkey+'\n')
                        self.Text1.insert(END,key+':','Traits')
                        self.Text1.insert(END,subkey+'\n','Text')
                        for subsubkey in Info['Legendary Actions'][key][subkey]:
                            #print('\t'+subsubkey+Info['Legendary Actions'][key][subkey][subsubkey])
                            self.Text1.insert(END,subsubkey+':','SubAbilities')
                            self.Text1.insert(END,Info['Legendary Actions'][key][subkey][subsubkey]+'\n','Text')
                else: #print('-'+key+': '+Info['Legendary Actions'][key]+'\n')
                    self.Text1.insert(END,key+':','Traits')
                    self.Text1.insert(END,Info['Legendary Actions'][key]+'\n','Text')
            #print('\n')

        self.Text1.tag_config('Name',font=self.NameFont,justify='center')
        self.Text1.tag_config('Abilities',font=self.AbilitiesFont)
        self.Text1.tag_config('Traits',font=self.TraitsFont)
        self.Text1.tag_config('AbilityScore',font=self.AbilityScoreFont,relief='raised',background='light green')
        self.Text1.tag_config('Action',font=self.ActionFont,justify='center')
        self.Text1.tag_config('Text',font=self.TextFont)

    def unpin(self):
        self.winfo_toplevel().winfo_children()[self.index].pack_forget()

######################################################################################################################

class HealingGUI():
    def __init__(self, master,Combatants):
        self.master=master
        self.healing = {}
        self.tempHP={}
        self.Combatants=Combatants
        
        for Combatant in self.Combatants:
            self.healing[Combatant]=IntVar()
            self.tempHP[Combatant]=IntVar()

        self.Healing=StringVar()
        self.Healing.set('0')
        HealingLabel=Label(self.master,text="How much healing was given?")
        HealingBox=Entry(self.master,textvariable=self.Healing)
        HealingLabel.grid(row=0,column=1,pady=20,columnspan=2)
        HealingBox.grid(row=0,column=3,pady=20,columnspan=2)

        self.TempHP=StringVar()
        self.TempHP.set('0')
        TempHPLabel=Label(self.master,text="How many temporary hit points were given?")
        TempHPBox=Entry(self.master,textvariable=self.TempHP)
        TempHPLabel.grid(row=1,column=1,pady=20,columnspan=2)
        TempHPBox.grid(row=1,column=3,pady=20,columnspan=2)


        Text=Label(self.master,text="Which combatants were healed?")
        Text.grid(row=2,columnspan=5)

        FullHealingLabel=Label(self.master,text="Healing")
        FullHealingLabel.grid(row=3,column=1)
        TempHealingLabel=Label(self.master,text="Temp HP")
        TempHealingLabel.grid(row=3,column=2)


        CurrentRow=4
        for Combatant in self.Combatants:
            self.healing[Combatant]=DoubleVar()
            self.tempHP[Combatant]=DoubleVar()
            self.healing[Combatant].set(0)
            self.tempHP[Combatant].set(0)

            Healing = Checkbutton(self.master, variable = self.healing[Combatant], \
                         onvalue = 1, offvalue = 0, height=1, \
                         width = 10)
            Temporary = Checkbutton(self.master, variable = self.tempHP[Combatant], \
                         onvalue = 1, offvalue = 0, height=1, \
                         width = 10)

            Name=Label(self.master,text=Combatant)
            Healing.grid(row=CurrentRow,column=1,pady=0)
            Temporary.grid(row=CurrentRow,column=2,pady=0)
            Name.grid(row=CurrentRow,column=0,pady=0,padx=20)
            CurrentRow+=1

        Apply=Button(self.master,text="Apply",command = self.AddDamages)
        Apply.grid(row=CurrentRow,column=1,columnspan=2)
        Cancel=Button(self.master,text="Cancel",command = self.quit)
        Cancel.grid(row=CurrentRow,column=3,columnspan=2)

    def quit(self):
        self.healing={}
        self.master.destroy()
        
    def AddDamages(self):
        ToHeal=int(self.Healing.get())
        TempHPToAdd=int(self.TempHP.get())
        for Combatant in self.Combatants:
            #We multiply by -1 since this is sent to the _Damage function, which will then apply "negative" damage
            self.healing[Combatant]=-int(self.healing[Combatant].get())*ToHeal
            self.tempHP[Combatant]=int(self.tempHP[Combatant].get())*TempHPToAdd
        self.master.destroy()

#################################################################################################################
class SettingsGUI():
    def __init__(self, master):
        self.master=master
        self.master.title("Settings")
        self.Settings={}

        self.CurrentRow=1
        
        self.Randomise=BooleanVar()        
        self.RandomiseLabel=Label(self.master,text="Use randomised initiative rules?")
        self.RandomiseBox=Checkbutton(self.master,variable=self.Randomise, onvalue=True, offvalue=False)
        self.RandomiseLabel.grid(row=self.CurrentRow,column=1,columnspan=2)
        self.RandomiseBox.grid(row=self.CurrentRow,column=3,columnspan=2)

        self.CurrentRow+=1

        self.Vulnerability=StringVar()
        self.VulnerabilityLabel=Label(self.master,text="Enter vulnerability modifier:")
        self.VulnerabilityBox=Entry(self.master,textvariable=self.Vulnerability, state=NORMAL)
        self.VulnerabilityLabel.grid(row=self.CurrentRow,column=1,columnspan=2)
        self.VulnerabilityBox.grid(row=self.CurrentRow,column=3,columnspan=2)

        self.CurrentRow+=1
        
        self.AutoRemove=BooleanVar()        
        self.AutoRemoveLabel=Label(self.master,text="Automatically remove creatures at or below 0 HP from initiative?")
        self.AutoRemoveBox=Checkbutton(self.master,variable=self.AutoRemove, onvalue=True, offvalue=False)
        self.AutoRemoveLabel.grid(row=self.CurrentRow,column=1,columnspan=2)
        self.AutoRemoveBox.grid(row=self.CurrentRow,column=3,columnspan=2)


        
        Apply=Button(self.master,text="Apply settings",command = self.Add)
        Apply.grid(row=self.CurrentRow+1,column=1,columnspan=2)
        Cancel=Button(self.master,text="Cancel",command = self.quit)
        Cancel.grid(row=self.CurrentRow+1,column=3,columnspan=2)

        
    def quit(self):
        self.Settings={}
        self.master.destroy()
        
    def Add(self):
        self.Settings['Randomise']=self.Randomise.get()
        self.Settings['VulnerabilityModifier']=int(self.Vulnerability.get())
        self.Settings['AutoRemove']=self.AutoRemove.get()
        
        self.master.destroy()

###################################################################

class PinButton(Button):
    def __init__(self,master,*,creature,**kwds):
        self.creature=creature
        super().__init__(master,**kwds)

####################################################################

class UnpinButton(Button):
    def __init__(self,master,*,PinWindow,index,**kwds):
        self.master=master
        self.index=index
        self.PinWindow=PinWindow
        super().__init__(master,**kwds)

    def unpin(self):
        self.winfo_toplevel().winfo_children()[index].pack_forget()

####################################################################


class PrintStatsPin(tkinter.BaseWidget):
    def __init__(self,master,Bestiary,creature,index=99):
        self.master=master
        self.Bestiary=Bestiary
        self.creature=creature
        self.index=index
        self.IsOpen=BooleanVar()
        self.IsOpen.set(True)
        self.master.config(height=500,width=700)

        self.NameFont=font.Font(family="Helvetica",size=20,weight='bold',slant='roman',underline=1)
        self.AbilityScoreFont=font.Font(family="helvetica",size=10,weight='normal',slant='roman',underline=0)
        self.AbilitiesFont=font.Font(family="helvetica",size=10,weight='bold',slant='roman',underline=0)
        self.SubAbilitiesFont=font.Font(family="helvetica",size=10,weight='normal',slant='italic',underline=0)
        self.TraitsFont=font.Font(family="Helvetica",size=10,weight='bold',slant='italic',underline=0)
        self.TextFont=font.Font(family="Helvetica",size=10,weight='normal',slant='roman',underline=0)
        self.ActionFont=font.Font(family="Helvetica",size=10,weight='bold',slant='roman',underline=0)
        self.PrintStats()

    def callback(self):
        self.IsOpen.set(False)
        self.master.destroy()

    def PrintStats(self):
        self.Frame1=Frame(self.master)
        self.master.add(self.Frame1)
        self.Text1=Text(self.Frame1,spacing1=1,spacing3=1)
        self.Text1.pack()

        Info=self.Bestiary[self.creature]
        self.Text1.insert(1.0,self.creature.upper()+'\n','Name')
        Description=Info.get('description','')
        
        
        StatText='{:^10} {:^10} {:^10} {:^10} {:^10} {:^10}'.format('STR','DEX','CON','INT','WIS','CHA')
        Stats='{:^10} {:^10} {:^10} {:^10} {:^10} {:^10}'.format(Info['STR'],Info['DEX'],Info['CON'],Info['INT'],Info['WIS'],Info['CHA'])
        Type=Info.get('type','')
        Size=Info.get('size','')
        CR=Info.get('CR','-').strip('cr')
        HP=Info.get('Hit Points','-')
        AC=Info.get('Armor Class','-')
        Speed=Info.get('Speed','-')
        Saves=Info.get('Saving Throws', 'None')
        Skills=Info.get('Skills', 'None')
        DamageResistances=Info.get('Damage Resistances', 'None')
        DamageImmunities=Info.get('Damage Immunities', 'None')
        ConditionImmunities=Info.get('Condition Immunities', 'None')
        Senses=Info.get('Senses', 'None')
        Languages=Info.get('Languages', 'None')

        self.Text1.insert(2.0,Description+'\n','Traits')

        self.Text1.insert(3.0,Size+" "+Type+'\n','Traits')

        self.Text1.insert(4.0,'AC:','Abilities')
        self.Text1.insert(END,AC+'\n','Text')

        self.Text1.insert(5.0,'Hit points:','Abilities')
        self.Text1.insert(END,HP+'\n','Text')

        self.Text1.insert(6.0,'Speed:','Abilities')
        self.Text1.insert(END,Speed+'\n','Text')

        self.Text1.insert(7.0,StatText+'\n','AbilityScore')
        
        self.Text1.insert(8.0,Stats+'\n','AbilityScore')
        
        self.Text1.insert(9.0,'Saving throws:','Abilities')
        self.Text1.insert(END,Saves+'\n','Text')

        self.Text1.insert("10.0",'Skills:','Abilities')
        self.Text1.insert(END,Skills+'\n','Text')

        self.Text1.insert("11.0",'Damage immunities:','Abilities')
        self.Text1.insert(END,DamageImmunities+'\n','Text')

        self.Text1.insert("12.0",'Damage resistances:','Abilities')
        self.Text1.insert(END,DamageResistances+'\n','Text')

        self.Text1.insert("13.0",'Senses:','Abilities')
        self.Text1.insert(END,Senses+'\n','Text')

        self.Text1.insert("14.0",'Languages:','Abilities')
        self.Text1.insert(END,Languages+'\n','Text')

        self.Text1.insert("15.0",'Challenge rating:','Abilities')
        self.Text1.insert(END,CR+'\n','Text')
        
        if 'Traits' in Info:
            for key in Info['Traits']:
                if type(Info['Traits'][key])==dict:
                    for subkey in Info['Traits'][key]:
                        #print('-'+key+': '+subkey+'\n')
                        self.Text1.insert(END,key+':','Traits')
                        self.Text1.insert(END,subkey+'\n','Text')
                        for subsubkey in Info['Traits'][key][subkey]:
                            #print('\t'+subsubkey+Info['Traits'][key][subkey][subsubkey])
                            self.Text1.insert(END,subsubkey+':','SubAbilities')
                            self.Text1.insert(END,Info['Traits'][key][subkey][subsubkey]+'\n','Text')
                else: #print('-'+key+': '+Info['Traits'][key]+'\n')
                    self.Text1.insert(END,key+':','Traits')
                    self.Text1.insert(END,Info['Traits'][key]+'\n','Text')
            #print('\n')
        if 'Actions' in Info:
            #print("Actions")
            self.Text1.insert(END,'Actions \n','Action')
            for key in Info['Actions']:
                if type(Info['Actions'][key])==dict:
                    for subkey in Info['Actions'][key]:
                        self.Text1.insert(END,key+':','Traits')
                        self.Text1.insert(END,subkey+'\n','Text')
                        #print('-'+key+': '+subkey+'\n')
                        for subsubkey in Info['Actions'][key][subkey]:
                            #print('\t'+subsubkey+Info['Actions'][key][subkey][subsubkey])
                            self.Text1.insert(END,subsubkey+':','SubAbilities')
                            self.Text1.insert(END,Info['Actions'][key][subkey][subsubkey]+'\n','Text')
                else: #print('-'+key+': '+Info['Actions'][key]+'\n')
                    self.Text1.insert(END,key+':','Traits')
                    self.Text1.insert(END,Info['Actions'][key]+'\n','Text')
           # print('\n')
        if 'Legendary Actions' in Info:
            #print("Legendary Actions")
            #print(Info['Traits']['Legendary Actions'])
            #print('\n')
            self.Text1.insert(END,'Legendary actions \n','Action')
            for key in Info['Legendary Actions']:
                if type(Info['Legendary Actions'][key])==dict:
                    for subkey in Info['Legendary Actions'][key]:
                        #print('-'+key+': '+subkey+'\n')
                        self.Text1.insert(END,key+':','Traits')
                        self.Text1.insert(END,subkey+'\n','Text')
                        for subsubkey in Info['Legendary Actions'][key][subkey]:
                            #print('\t'+subsubkey+Info['Legendary Actions'][key][subkey][subsubkey])
                            self.Text1.insert(END,subsubkey+':','SubAbilities')
                            self.Text1.insert(END,Info['Legendary Actions'][key][subkey][subsubkey]+'\n','Text')
                else: #print('-'+key+': '+Info['Legendary Actions'][key]+'\n')
                    self.Text1.insert(END,key+':','Traits')
                    self.Text1.insert(END,Info['Legendary Actions'][key]+'\n','Text')
            #print('\n')

        self.Text1.tag_config('Name',font=self.NameFont,justify='center')
        self.Text1.tag_config('Abilities',font=self.AbilitiesFont)
        self.Text1.tag_config('Traits',font=self.TraitsFont)
        self.Text1.tag_config('AbilityScore',font=self.AbilityScoreFont,relief='raised',background='light green')
        self.Text1.tag_config('Action',font=self.ActionFont,justify='center')
        self.Text1.tag_config('Text',font=self.TextFont)

    def unpin(self):
        print(self.index)
        self.master.winfo_toplevel().winfo_children()[self.index].pack_forget()

######################################################################################################################

