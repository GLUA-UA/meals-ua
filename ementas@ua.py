# Rodrigo Rosmaninho - MIECT / Universidade de Aveiro
# 2018

# VERSION 1.0

import urllib.request as urllib
import xmltodict
import json
import os
os.system('clear')

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def internet_on():
    try:
        urllib.urlopen('http://www.google.pt', timeout=1)
        return True
    except urllib.URLError as err: 
        return False

print(bcolors.OKGREEN + '\n%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n' + bcolors.ENDC + bcolors.BOLD + '                   Ementas na UA\n' + bcolors.ENDC +  bcolors.OKGREEN + '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n' + bcolors.ENDC)
print('By Rodrigo Rosmaninho - MIECT - 2018\n')

if not internet_on():
    print(bcolors.FAIL + '\n======================== ERRO ========================' + bcolors.ENDC)
    print(bcolors.FAIL + 'Não existe conexão à internet.\nEste script necessita de uma ligação estável à internet para aceder ao API da UA.\n' + bcolors.ENDC)

else:
    file = urllib.urlopen('http://services.web.ua.pt/sas/ementas')
    data = file.read()
    file.close()

    data = json.loads(json.dumps(xmltodict.parse(data)))
    data = data['result']['menus']['menu']

    print(bcolors.WARNING + 'Data' + bcolors.ENDC + ': ' + bcolors.HEADER + bcolors.BOLD + data[0]['@date'][:-15] + '\n' + bcolors.ENDC)

    for i in range(len(data)):
        if data[i]['@meal'] == 'Almoço':
            print(bcolors.OKBLUE + '\n================== ' + '{: ^22}'.format(data[i]['@canteen']) + ' ==================\n' + bcolors.ENDC)

        print(bcolors.UNDERLINE + data[i]['@meal'] + '\n' + bcolors.ENDC)

        if data[i]['@disabled'] == '0':   
            for x in range(len(data[i]['items']['item'])):
                if '#text' in data[i]['items']['item'][x]:
                    print(bcolors.WARNING + data[i]['items']['item'][x]['@name'] + bcolors.ENDC + ': ' + bcolors.BOLD +  data[i]['items']['item'][x]['#text'] + bcolors.ENDC)

        else:
            print(bcolors.FAIL + data[i]['@disabled'] + bcolors.ENDC)
    
        print()

    print(bcolors.UNDERLINE + '\n\nBom Apetite!\n' + bcolors.ENDC)