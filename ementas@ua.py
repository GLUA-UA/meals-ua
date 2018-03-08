# Rodrigo Rosmaninho - MIECT / Universidade de Aveiro - 2018
# https://github.com/RodrigoRosmaninho/ementas-ua

# VERSION 1.1

# Necessary imports
import urllib.request as urllib
import os, sys

# Try to import xmltodict. If the module is not found, print an error and quit program
try:
    import xmltodict 
except:
    print("\n Erro! Módulo 'xmltodict' não encontrado! Siga as instruções no README.md para instalar e volte a correr o programa.\n")
    sys.exit()

os.system('clear') # Clear the terminal screen

class bcolors: # Define colors
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m' # ENDC makes the color return to normal
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Determine whether there is internet access, return boolean
def internet_on():
    try:
        urllib.urlopen('http://www.google.pt', timeout=1)
        return True
    except urllib.URLError as err: 
        return False

print(bcolors.OKGREEN + '\n%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n' + bcolors.ENDC + bcolors.BOLD + '                       Ementas na UA\n' + bcolors.ENDC +  bcolors.OKGREEN + '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n' + bcolors.ENDC)
print('By Rodrigo Rosmaninho - MIECT - 2018\n')

if not internet_on(): # If there is no internet print errors
    print(bcolors.FAIL + '\n======================== ERRO ========================' + bcolors.ENDC)
    print(bcolors.FAIL + 'Não existe conexão à internet.\nEste script necessita de uma ligação estável à internet para aceder ao API da UA.\n' + bcolors.ENDC)

else:
    file = urllib.urlopen('http://services.web.ua.pt/sas/ementas') # open the result of the API as a file
    data = file.read()
    file.close()

    data = xmltodict.parse(data) # Use xmltodict module to parse data from XML to a Python Dict
    # Sample data: https://codebeautify.org/jsonviewer/cb6c4994
    data = data['result']['menus']['menu'] # Get to the relevent section of the data. 'menu' is an array of objects, each object matches a meal at a certain canteen

    print(bcolors.WARNING + 'Data' + bcolors.ENDC + ': ' + bcolors.HEADER + bcolors.BOLD + data[0]['@date'][:-15] + '\n' + bcolors.ENDC) # Print current date, as found in the dict

    # Iterate through the array of meals
    for i in range(len(data)): 
        if data[i]['@meal'] == 'Almoço': # Each canteen can serve 2 meals (Lunch, Dinner). If the current meal is Lunch, print the name of the canteen
            print(bcolors.OKBLUE + '\n================== ' + '{: ^22}'.format(data[i]['@canteen']) + ' ==================\n' + bcolors.ENDC) # Prints the name of the canteen properly formatted. The space between the '=' must be 22 characters.

        print(bcolors.UNDERLINE + data[i]['@meal'] + '\n' + bcolors.ENDC) # Print what meal it is, i.e. Lunch or Dinner

        if data[i]['@disabled'] == '0': # If the meal is not 'disabled', in other words, if the canteen is in fact serving this meal
            # Iterate through all the diffent options on the menu
            for x in range(len(data[i]['items']['item'])):
                if '#text' in data[i]['items']['item'][x]: # If the option name has a corresponding value (food), print both the name and the value
                    print(bcolors.WARNING + data[i]['items']['item'][x]['@name'] + bcolors.ENDC + ': ' + bcolors.BOLD +  data[i]['items']['item'][x]['#text'] + bcolors.ENDC)

        else:
            print(bcolors.FAIL + data[i]['@disabled'] + bcolors.ENDC) # If the meal is 'disabled', print the disable message included in the data
    
        print()

    print(bcolors.UNDERLINE + '\n\nBom Apetite!\n' + bcolors.ENDC)