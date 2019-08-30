import re

# Define characters to replace if makeReplacements = True

rep = {
    "âˆ’":"-",
    "â€™":"'",
    'â€“':'-'
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


def AddBestiary(Bestiary,creature,printDetails=False):
    Filename='./bestiary/creatures/'+ creature +'.html'
    if creature not in Bestiary:
        Bestiary[creature]={}
        #reached="start"
        reached="Traits"
        TraitStarted=True
        with open(Filename, "r") as f:
            #count += 1
            for line in f:
                if printDetails:
                    print(line)
                if reached == "nothing":
                    if re.search("<h1 class=\"post-title\">([^\<]+)</h1>",line):
                        creature = re.findall("<h1 class=\"post-title\">([^\<]+)</h1>",line)[0]
                        reached = "start"
                        if printCreatures:
                            print("File " + str(count) + ": " + str(creature))
                elif reached == "start":
                    if re.search("<dt>Tags:</dt>",line):
                        reached = "size"
                elif reached == "size":
                    if re.search("<[^>]+>([^\<]+)</a>",line):
                        Bestiary[creature]["size"] = re.findall("<[^>]+>([^\<]+)</a>",line)[0]
                        reached = "type"
                        if printDetails:
                            print(" .. size")
                elif reached == "type":
                    if re.search("<[^>]+>([^\<]+)</a>",line):
                        Bestiary[creature]["type"] = re.findall("<[^>]+>([^\<]+)</a>",line)[0]
                        reached = "CR"
                        if printDetails:
                            print(" .. type")
                elif reached == "CR":
                    if re.search("<[^>]+>([^\<]+)</a>",line):
                        Bestiary[creature]["CR"] = re.findall("<[^>]+>([^\<]+)</a>",line)[0]
                        reached = "specs"
                        if printDetails:
                            print(" .. CR")
                elif reached == "specs":
                    if re.search("<p><strong>([^\<]+)</strong>([^\<]+)</p>",line):
                        values = FixText(re.findall("<p><strong>([^\<]+)</strong>([^\<]+)</p>",line)[0])
                        Bestiary[creature][values[0]] = values[1]
                        if printDetails:
                            print(" .. specs: " + str(values[0]))
                    elif re.search("<tbody>",line):
                        reached = "STR"
                elif reached == "STR":
                    if re.search("<td style=\"text-align: center\">([^\<]+)</td>",line):
                        values = FixText(re.findall("<td style=\"text-align: center\">([^\<]+)</td>",line)[0])
                        Bestiary[creature]["STR"] = FixText(values)
                        reached = "DEX"
                        if printDetails:
                            print(" .. STR")
                elif reached == "DEX":
                    if re.search("<td style=\"text-align: center\">([^\<]+)</td>",line):
                        values = FixText(re.findall("<td style=\"text-align: center\">([^\<]+)</td>",line)[0])
                        Bestiary[creature]["DEX"] = FixText(values)
                        reached = "CON"
                        if printDetails:
                            print(" .. DEX")
                elif reached == "CON":
                    if re.search("<td style=\"text-align: center\">([^\<]+)</td>",line):
                        values = FixText(re.findall("<td style=\"text-align: center\">([^\<]+)</td>",line)[0])
                        Bestiary[creature]["CON"] = FixText(values)
                        reached = "INT"
                        if printDetails:
                            print(" .. CON")
                elif reached == "INT":
                    if re.search("<td style=\"text-align: center\">([^\<]+)</td>",line):
                        values = FixText(re.findall("<td style=\"text-align: center\">([^\<]+)</td>",line)[0])
                        Bestiary[creature]["INT"] = FixText(values)
                        reached = "WIS"
                        if printDetails:
                            print(" .. INT")
                elif reached == "WIS":
                    if re.search("<td style=\"text-align: center\">([^\<]+)</td>",line):
                        values = FixText(re.findall("<td style=\"text-align: center\">([^\<]+)</td>",line)[0])
                        Bestiary[creature]["WIS"] = FixText(values)
                        reached = "CHA"
                        if printDetails:
                            print(" .. WIS")
                elif reached == "CHA":
                    if re.search("<td style=\"text-align: center\">([^\<]+)</td>",line):
                        values = FixText(re.findall("<td style=\"text-align: center\">([^\<]+)</td>",line)[0])
                        Bestiary[creature]["CHA"] = FixText(values)
                        TraitStarted=True
                        if printDetails:
                            print(" .. CHA")
                        reached="specs2"
                        
                elif reached == "specs2":
                    if re.search("<p><strong>([^\<]+)</strong>([^\<]+)</p>",line):
                        values = FixText(re.findall("<p><strong>([^\<]+)</strong>([^\<]+)</p>",line)[0])
                        if printDetails:
                            print('values=',values)
                        if "." in values[0]:
                            current = "Misc"
                            Bestiary[creature][current][values[0]] = values[1]
                        else:
                            Bestiary[creature][values[0]] = values[1]
                        if printDetails:
                            print(" .. " + str(values[0]))
                    elif re.search("<p><strong>([^\<]+)</strong></p>",line):
                        reached = "details"
                        current = re.findall("<p><strong>([^\<]+)</strong></p>",line)[0]
                        if printDetails:
                            print(" .. " + str(current))
                    elif re.search("<p><strong><em>([^\<]+)</em></strong>([^\<]+)</p>",line):
                        reached="Traits"
                        if printDetails:
                            print('Started traits.')
                        
                if reached == "Traits":
                    if TraitStarted:
                        TraitStarted=False
                        Bestiary[creature]['Traits']={}
                    if re.search("<p><strong><em>([^\<]+)</em></strong>([^\<]+)</p>",line):
                        values = FixText(re.findall("<p><strong><em>([^\<]+)</em></strong>([^\<]+)</p>",line)[0])
                        if printDetails:
                            print('values=',values)
                        if "." in values[0]:
                            Bestiary[creature]['Traits'][values[0]]=values[1]
                            subtrait=values[0]
                            subsubtrait=values[1]
                    elif re.search("<p><em>([^\<]+)</em>([^\<]+)</p>",line):
                        values = FixText(re.findall("<p><em>([^\<]+)</em>([^\<]+)</p>",line)[0])
                        if printDetails:
                            print('values=', values)
                        if type(Bestiary[creature]['Traits'][subtrait])==dict:
                            PreviousTrait=Bestiary[creature]['Traits'][subtrait].get(subsubtrait, {})
                            NewTrait={values[0]: values[1]}
                            NewTrait.update(PreviousTrait)
                        else:
                            NewTrait={values[0]: values[1]}
                        Bestiary[creature]['Traits'][subtrait]={subsubtrait:NewTrait}
                    elif 'Actions' in line:
                        StartedActions=True
                        reached= "actions"
                    else:
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
                        if re.search("<p><em>([^\<]+)</em>([^\<]+)</p>",line):
                            values = FixText(re.findall("<p><em>([^\<]+)</em>([^\<]+)</p>",line)[0])
                            if printDetails:
                                print('values=', values)
                            if type(Bestiary[creature]['Actions'][subaction])==dict:
                                PreviousAction=Bestiary[creature]['Actions'][subaction].get(subsubaction, {})
                                NewAction={values[0]: values[1]}
                                NewAction.update(PreviousAction)
                            else:
                                NewAction={values[0]: values[1]}
                            Bestiary[creature]['Actions'][subaction]={subsubaction:NewAction}

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
                        Bestiary[creature]['Traits']['Legendary Actions']=values
                                             
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
        print(Info['Traits']['Legendary Actions'])
        print('\n')
        for key in Info['Legendary Actions']:
            if type(Info['Legendary Actions'][key])==dict:
                for subkey in Info['Legendary Actions'][key]:
                    print('-'+key+': '+subkey+'\n')
                    for subsubkey in Info['Legendary Actions'][key][subkey]:
                        print('\t'+subsubkey+Info['Legendary Actions'][key][subkey][subsubkey])
            else: print('-'+key+': '+Info['Legendary Actions'][key]+'\n')
        print('\n')
    
