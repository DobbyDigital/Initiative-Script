import random as r
import os
import datetime
import subprocess
import re
import math
from operator import itemgetter, attrgetter
from copy import deepcopy

# Define characters to replace if makeReplacements = True

rep = {
    "âˆ’":"-",
    "â€™":"'",
    'â€“':'-',
    "â€™s":"'s"
    }

# Nice replacement method
rep = dict((re.escape(k), v) for k, v in rep.items())
pattern = re.compile("|".join(rep.keys()))
# You can now use this to make the changes:
# text = pattern.sub(lambda m: rep[re.escape(m.group(0))], text)


def FixText(text):
    if type(text)==str:
        text = pattern.sub(lambda m: rep[re.escape(m.group(0))], text)
    else:
        text=[FixText(i) for i in text]
    return text

def AddStats(Bestiary,creature,stat,line):
    temp=re.findall('(?<=<p>).*(?=</p>)',line)[0]
    Bestiary[creature][stat]=temp
    stat=''
    return stat,Bestiary

def AddBestiary(Bestiary,creature,printDetails=False):
    Filename='./bestiary/creatures/'+ creature +'.html'
    if creature not in Bestiary:
        Bestiary[creature]={}
        stat=''
        reached="description"
        TraitStarted=True
        with open(Filename, "r") as f:
            #count += 1
            for line in f:
                if printDetails:
                    print(line)
                if stat != '':
                    stat,Bestiary=AddStats(Bestiary,creature,stat,line)
                    continue
                if reached == "nothing":
                    if re.search("<h1>.* </h1>",line):
                        if printDetails:
                            print("Found creature name")
                        creature = re.findall("(?<= <h1>) .* (?=</h1>)",line)[0]
                        reached = "description"
                        if printCreatures:
                            print("File " + str(count) + ": " + str(creature))
                elif reached == "description":
                    if re.search("<h2>.*</h2>",line):
                        Bestiary[creature]["Description"]=re.findall("(?<=<h2>).*(?=</h2>)",line)[0]
                        reached="traits"
                        continue
                elif reached == "traits":
                    if re.search("<h4>.*</h4>",line):
                        if printDetails:
                            print("Found main trait")
                        stat=re.findall("(?<=<h4>).*(?=</h4>)",line)[0]
                        continue
                    elif re.search("<p><strong><em>.*</em></strong>.*</p>",line):
                        if printDetails:
                            print("Found secondary trait")
                        if 'Traits' not in Bestiary[creature]:
                            Bestiary[creature]["Traits"]={}
                        Bestiary[creature]["Traits"][re.findall("(?<=<p><strong><em>).*(?=</em></strong>)",line)[0]]=re.findall("(?<=</em></strong>).*(?=</p>)",line)[0]
                        continue
                    elif re.search('<h3 id="actions">Actions</h3>',line):
                        reached="actions"
                        StartedActions=True
                        if printDetails:
                            print(Bestiary[creature])
                        continue

                if reached == "actions":
                    if StartedActions:
                        if printDetails:
                            print('Started actions')
                        StartedActions=False
                        Bestiary[creature]['Actions']={}
                        continue

                    if 'Legendary Actions' in line:
                        reached="legendary actions"
                        StartedLegendaryActions=True
                        continue

                    if 'Actions' not in line:
                        if re.search("<p><strong><em>([^\<]+)</em></strong>([^\<]+)</p>",line):
                            values = FixText(re.findall("<p><strong><em>([^\<]+)</em></strong>([^\<]+)</p>",line)[0])
                            if printDetails:
                                print('Values= ',values)
                            if len(values)!=0 and "." in values[0]:
                                current = "Actions"
                                Bestiary[creature][current][values[0]]= values[1]
                                subaction=values[0]
                                subsubaction=values[1]
                        elif re.search("<p>.*</p>",line):
                            temp = FixText(re.findall("(?<=<p>).*(?=</p>)",line)[0])
                            temp=temp.split('.')
                            temp2=''
                            if printDetails:
                                print(temp)
                            if len(temp)>3:
                                #temp2=''
                                for i in range(1,len(temp)-1):
                                    temp2+=temp[i]
                            values=[temp[0],temp2]
                            if printDetails:
                                print('values=', values)
                            if type(Bestiary[creature]['Actions'][subaction])==dict:
                                PreviousAction=Bestiary[creature]['Actions'][subaction].get(subsubaction, {})
                                NewAction={values[0]: values[1]}
                                NewAction.update(PreviousAction)
                            else:
                                NewAction={values[0]: values[1]}
                            Bestiary[creature]['Actions'][subaction]={subsubaction:NewAction}
                        if re.search('<dl class="tag-list">',line) or re.search('h3 id="roleplaying-information">Roleplaying Information</h3>',line):
                            break

                if reached=='legendary actions':
                    if StartedLegendaryActions:
                        if printDetails:
                            print('Started legendary actions')
                        StartedLegendaryActions=False
                        Bestiary[creature]['Legendary Actions']={}

                    if re.search("<p>([^\<]+)</p>",line):
                        values = FixText(re.findall("<p>([^\<]+)</p>",line)[0])
                        if printDetails:
                            print('values=', values)
                        Bestiary[creature]['Legendary Actions']["Description"]=values
                                             
                    if 'Legendary Actions' not in line:
                        if re.search("<p><strong><em>([^\<]+)</em></strong>([^\<]+)</p>",line):
                            values = FixText(re.findall("<p><strong><em>([^\<]+)</em></strong>([^\<]+)</p>",line)[0])
                            if printDetails:
                                print('Values= ',values)
                            if len(values)!=0 and "." in values[0]:
                                current = "Legendary Actions"
                                Bestiary[creature][current][values[0]]= values[1]
                                subaction=values[0]
                                subsubaction=values[1]
                        if re.search("<p><em>([^\<]+)</em>([^\<]+)</p>",line):
                            values = FixText(re.findall("<p><em>([^\<]+)</em>([^\<]+)</p>",line)[0])
                            if printDetails:
                                print('values=', values)
                            if type(Bestiary[creature]['Legendary Actions'][subaction])==dict:
                                PreviousAction=Bestiary[creature]['Legendary Actions'][subaction].get(subsubaction, {})
                                NewAction={values[0]: values[1]}
                                NewAction.update(PreviousAction)
                            else:
                                NewAction={values[0]: values[1]}
                            Bestiary[creature]['Legendary Actions'][subaction]={subsubaction:NewAction}
                      
                if reached == "details":
                    if re.search("<p><strong>([^\<]+)</strong></p>",line):
                        reached = "details"
                        current = re.findall("<p><strong>([^\<]+)</strong></p>",line)[0]
                        if printDetails:
                            print(" .. " + str(current))
                    elif re.search("<p><strong><em>([^\<]+)</em></strong>([^\<]+)</p>",line):
                        values = FixText(re.findall("<p><strong><em>([^\<]+)</em></strong>([^\<]+)</p>",line)[0])
                        Bestiary[creature][current][values[0]] = values[1]
                        if printDetails:
                            print(" .. " + str(current) + ": " + str(values[0]))
                    elif re.search("</article>",line):
                        reached = "done"
                        if printDetails:
                            print(" .. Complete")
                       
            return Bestiary
    else:
        print(creature+' is already in the Bestiary. \n')
        return Bestiary

def PrintStats(Bestiary, creature, TLDR=True):
    Info=Bestiary[creature]
    print(Info["Description"]+"\n")
    print('{:^10} {:^10} {:^10} {:^10} {:^10} {:^10}  \n'.format('STR','DEX','CON','INT','WIS','CHA'))
    print('{:^10} {:^10} {:^10} {:^10} {:^10} {:^10}  \n'.format(Info['STR'],Info['DEX'],Info['CON'],Info['INT'],Info['WIS'],Info['CHA']))
    print('\n')

    if not TLDR:
        Saves=Info.get('Saving Throws', 'None')
        Skills=Info.get('Skills', 'None')
        DamageResistances=Info.get('Damage Resistances', 'None')
        DamageImmunities=Info.get('Damage Immunities', 'None')
        ConditionImmunities=Info.get('Condition Immunities', 'None')
        Senses=Info.get('Senses', 'None')
        Languages=Info.get('Languages', 'None')
        print('Saving throws:', Saves)
        print('Skills:', Skills)
        print('Speed:',Info['Speed'])
        print('Damage resistances:', DamageResistances)
        print('Damage immunities:', DamageImmunities)
        print('Condition immunities:', ConditionImmunities)
        print('Senses:', Senses)
        print('Languages:', Languages)
        print('\n')
    
    if 'Traits' in Info:
        print('Traits')
        for key in Info['Traits']:
            if type(Info['Traits'][key])==dict:
                for subkey in Info['Traits'][key]:
                    print('-'+key+': '+subkey+'\n')
                    for subsubkey in Info['Traits'][key][subkey]:
                        print('\t'+subsubkey+Info['Traits'][key][subkey][subsubkey])
            else: print('-'+key+': '+Info['Traits'][key]+'\n')
        print('\n')
    if 'Actions' in Info:
        print("Actions")
        for key in Info['Actions']:
            if type(Info['Actions'][key])==dict:
                for subkey in Info['Actions'][key]:
                    print('-'+key+': '+subkey+'\n')
                    for subsubkey in Info['Actions'][key][subkey]:
                        print('\t'+subsubkey+Info['Actions'][key][subkey][subsubkey])
            else: print('-'+key+': '+Info['Actions'][key]+'\n')
        print('\n')
    if 'Legendary Actions' in Info:
        print("Legendary Actions")
        print(Info['Legendary Actions'])
        print('\n')
        for key in Info['Legendary Actions']:
            if type(Info['Legendary Actions'][key])==dict:
                for subkey in Info['Legendary Actions'][key]:
                    print('-'+key+': '+subkey+'\n')
                    for subsubkey in Info['Legendary Actions'][key][subkey]:
                        print('\t'+subsubkey+Info['Legendary Actions'][key][subkey][subsubkey])
            else: print('-'+key+': '+Info['Legendary Actions'][key]+'\n')
        print('\n')
    

def DisplayCombatants(Combatants):
    NewList=[]
    for Combatant in Combatants:
        if len(Combatant)==3:
            temp=[str(Combatant[1])+':',str(Combatant[0])]
            NewList.append('{:>4}{:<15}\n'.format(*temp))
        else:
            temp=[str(Combatant[1])+':',str(Combatant[0]),"("+str(round(int(Combatant[3])/int(Combatant[4])*100))+"%:",str(Combatant[3])," HP of "+str(Combatant[4])+" HP total)"]
            NewList.append('{:>4}{:<10} {:>5}{:>3}{:<0} \n'.format(*temp))
    return NewList

def InitiativeRoll(Combatant,TurnCount=0):
    if TurnCount==0:
        Combatant['Initiative']=r.randint(1,20)+Combatant['FirstTurnBonus']
    else:
        Combatant['Initiative']+=r.randint(1,6+Combatant['DexterityMod'])
    return Combatant

def Initialise(Info):
    Combatants=[]
    for Combatant in Info:
        Stats=[Info[Combatant]['Name'],Info[Combatant]['Initiative'], Info[Combatant]['FirstTurnBonus']]
        if 'HP' in Info[Combatant]:
            Stats.append(Info[Combatant]['HP']+Info[Combatant].get('TempHP',0))
            Stats.append(Info[Combatant]['MaxHP'])
        Combatants.append(Stats)
    Combatants=sorted(Combatants,key=itemgetter(2),reverse=True)
    Combatants=sorted(Combatants,key=itemgetter(1),reverse=True)
    return Combatants

def AddToInitiative(Combatant,Combatants,CurrentTurn, PrintResults=True, sort=True):
    if Combatants==[["No current combatants","N/A",""]]:
        Combatants=[]
    Stats=[Combatant['Name'],Combatant['Initiative'],Combatant['FirstTurnBonus']]
    if 'HP' in Combatant:
        Stats.append(Combatant['HP'])
        Stats.append(Combatant['MaxHP'])
    Combatants.append(Stats)
    if sort:
        Combatants=sorted(Combatants,key=itemgetter(2), reverse=True)
        Combatants=sorted(Combatants,key=itemgetter(1),reverse=True)
    if Combatants.index(Stats)<=CurrentTurn and CurrentTurn>=0:
        CurrentTurn+=1
    if PrintResults:
        DisplayInitiative(Combatants)
    return Combatants, CurrentTurn

def ProcessInput(inputted):
    return(inputted.lower())

def ProcessBestiaryName(creature1):
    creature1=ProcessInput(creature1)
    creature1=creature1.split()
    if len(creature1)>1:
        creature=''
        for word in creature1:
            creature+=word+'-'
        creature=creature[:-1]
    else:
        creature=str(creature1[0])
    return creature
   

def D(die,number=1):
    out = []
    for num in range(0,number):
        out.append(r.randint(1,die))
    return(sum(out))


def Roll(toRoll, func="Identity", verbose=True, output=True):
    # Function resolution
    if func.lower() in ["max", "adv", "advantage", "a"]:
        func = "max"
    elif func.lower() in ["disadv", "dis", "disadvantage", "min", "d"]:
        func = "min"
    else:
        func = "Identity"

    # Determine outcomes
    inst = re.sub("(\d+)[Dd](\d+)","D(\\2,\\1)",toRoll)
    val1 = eval(inst)
    val2 = eval(inst)
    val = eval(func + "(" + str(val1) + "," + str(val2) + ")")

    # Print result summary if desired
    if verbose:
        print(" .. Roll outcome: " + str(val) + " (" + func + " on rolls of " + str(val1) + " and " + str(val2) + ")")

    # Output
    if output:
        return(val)
def Identity(*args):
    return(args[0])    
