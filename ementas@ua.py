# Rodrigo Rosmaninho - MIECT / Universidade de Aveiro - 2018
# https://github.com/RodrigoRosmaninho/ementas-ua

# VERSION 2

# Necessary imports
import urllib.request as urllib
import sys, os
import argparse
import json
from os.path import expanduser

# Get home directory. Works both on Linux and Windows
home = expanduser("~")

class bcolors:  # Define colors
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'  # ENDC makes the color return to normal
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


global parser
# Instantiate the parser
parser = argparse.ArgumentParser(
    description="Script simples em python que apresenta os menus do dia (ou semana) em todos os refeitórios da Universidade de Aveiro")

# Presents the week's menu
parser.add_argument('-w', action='store_true', default=False, dest='showWeek',
                    help='Apresenta os menus de toda a semana')

# Presents the week's menu
parser.add_argument('-t', action='store_true', default=False, dest='showTutorial',
                    help='Volta a apresentar o tutorial inicial')

# Specifies which zone to display results from
parser.add_argument('-l', type=int, nargs=1, dest='displayZone',
                    default=1,
                    help='Especifica os refeitórios a apresentar: 1 - Campus (Santiago, Crasto, e Snack), 2 - ESTGA, 3 - Restaurante Universitário, 4 - ESAN',
                    )

# Save JSON config file on the user's home directory
def save_config_file():
    file = open(home + "/.ementasrc", "w")
    json_data = json.loads("{}")
    json_data["skip_tutorial"] = True
    file.write(json.dumps(json_data))

# Show Tutorial
def initial_screen():
    print(bcolors.OKGREEN + '************************* Tutorial *************************' + bcolors.ENDC)
    print("Bem vindo. Este tutorial apenas aparecerá uma vez.")
    print("Este script serve para conseguir facilmente consultar as ementas dos vários refeitórios da Universidade de Aveiro.")
    print("Por defeito, são apresentadas as ementas do dia atual nos refeitórios do campus da UA (Santiago, Crasto, e Snack)")
    print("No entanto, pode utilizar o parâmetro " + bcolors.BOLD + "-w" + bcolors.ENDC + " para visualizar as ementas de toda a semana e o parâmetro " + bcolors.BOLD + "-l" + bcolors.ENDC + " para especificar o local a consultar, sendo que:")
    print(" " + bcolors.BOLD + "-l 1" + bcolors.ENDC + " devolve as ementas no Campus\n " + bcolors.BOLD + "-l 2" + bcolors.ENDC + " devolve as ementas na ESTGA\n " + bcolors.BOLD + "-l 3" + bcolors.ENDC + " devolve as ementas no Restaurante Universitário\n " + bcolors.BOLD + "-l 4" + bcolors.ENDC + " devolve as ementas na ESAN")
    print("É possível conjugar ambos os parâmetros. Por exemplo, " + bcolors.BOLD + "ementa -w -l 2" + bcolors.ENDC + " devolve todas as ementas da semana correnta na ESTGA")
    print("\nSe ainda não o fez, deveria correr o script 'install.sh' incluído neste diretório.\nDesta forma, poderá executar o programa de forma fácil e sem ter de navegar até ao diretório para onde o descarregou.")
    print("Para o fazer, execute os seguintes comandos:" + bcolors.WARNING + "\nchmod +x install.sh\n./install.sh" + bcolors.ENDC)
    print("\nEste software é open-source e o código pode ser consultado em: " + bcolors.OKBLUE + "https://github.com/RodrigoRosmaninho/ementas-ua" + bcolors.ENDC)
    print("Se encontrar algum problema, por favor crie um issue nessa página, para que este possa ser rapidamente resolvido.")
    print("\nPara consultar novamente este tutorial pode usar o parâmetro " + bcolors.BOLD + "-t" + bcolors.ENDC + "")
    print("Para apresentar a página de ajuda pode usar o parâmetro " + bcolors.BOLD + "-h" + bcolors.ENDC + " ou " + bcolors.BOLD + "--help" + bcolors.ENDC + "")
    print(bcolors.OKGREEN + '************************************************************\n' + bcolors.ENDC)

# Check if config file exists and if the tutorial has already been shown
def check_config():
    if os.path.isfile(home + "/.ementasrc"):
        file = open(home + "/.ementasrc")
        data = json.loads(file.read())
        if 'skip_tutorial' in data:
            if not data['skip_tutorial']:
                save_config_file()
                initial_screen()
        else:
            save_config_file()
            initial_screen()
    else:
        save_config_file()
        initial_screen()

# Determine whether there is internet access, return boolean
def internet_on():
    try:
        urllib.urlopen('http://www.google.pt', timeout=1)
        return True
    except urllib.URLError as err:
        return False

# Handle an error that happens when there is no meal data for a given place (happens a lot with ESAN)
def handle_key_error(displayZone):
    if displayZone == [2]:
        place="no refeitório da ESTGA"
    elif displayZone == [3]:
        place = "no Restaurante Universitário"
    elif displayZone == [4]:
        place = "no refeitório da ESAN"
    else:
        place = "nos refeitórios do Campus"
    
    print(bcolors.WARNING + "De momento não há informações sobre a ementa " + place + "!" + bcolors.ENDC + "\n")
    sys.exit()

def main():
    print(bcolors.OKGREEN + '\n%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n' + bcolors.ENDC + bcolors.BOLD +
        '                       Ementas na UA\n' + bcolors.ENDC + bcolors.OKGREEN + '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%' + bcolors.ENDC)
    print('By Rodrigo Rosmaninho & André Alves - MIECT - 2018\n')

    # Get arguments
    args = parser.parse_args()

    if args.showTutorial:
        initial_screen()
        sys.exit()

    check_config()  

    # Try to import xmltodict. If the module is not found, print an error and quit program
    try:
        import xmltodict
    except:
        print("\nErro! Módulo 'xmltodict' não encontrado! Siga as instruções no README.md para instalar e volte a correr o programa.")
        print("Ou faça sh ./install.sh no diretório deste ficheiro.")
        sys.exit()

    if not internet_on():  # If there is no internet print errors
        print(bcolors.FAIL +
            '=========================== ERRO ===========================' + bcolors.ENDC)
        print(bcolors.FAIL + 'Não existe conexão à internet.\nEste script necessita de uma ligação estável à internet para aceder ao API da UA.\n' + bcolors.ENDC)

    else:
        
        if args.showWeek:
            date = "week"
        else:
            date = "day"

        if args.displayZone == [2]:
            place="ESTGA"
        elif args.displayZone == [3]:
            place = "rest"
        elif args.displayZone == [4]:
            place = "ESAN"
        else:
            place = "santiago"

        file = urllib.urlopen('http://services.web.ua.pt/sas/ementas?date=' + date + '&place=' + place) # open the result of the API as a file

        response = file.read()
        file.close()

        response = xmltodict.parse(response) # Use xmltodict module to parse data from XML to a Python Dict
        # Sample data: https://codebeautify.org/jsonviewer/cb6c4994

        try:
            response = response['result']['menus']['menu'] # Get to the relevent section of the data. 'menu' is an array of objects, each object matches a meal at a certain canteen
        except KeyError:
            handle_key_error(args.displayZone)

        data = response
        if not isinstance(response, list):
            data = [1]
            data[0] = response

        last_date = ""
        # Iterate through the array of meals
        for i in range(len(data)): 
            if data[i]['@date'] != last_date and data[i]['@meal'] == 'Almoço':
                last_date = data[i]['@date']
                print(bcolors.WARNING + '****************** ' + bcolors.HEADER + bcolors.BOLD + '{: ^22}'.format(data[i]['@date'][:-15]) + bcolors.WARNING + ' ******************\n' + bcolors.ENDC) # Prints the day properly formatted. The space between the '=' must be 22 characters.
            if data[i]['@meal'] == 'Almoço': # Each canteen can serve 2 meals (Lunch, Dinner). If the current meal is Lunch, print the name of the canteen
                print(bcolors.OKBLUE + '================== ' + '{: ^22}'.format(data[i]['@canteen']) + ' ==================\n' + bcolors.ENDC) # Prints the name of the canteen properly formatted. The space between the '=' must be 22 characters.

            print(bcolors.UNDERLINE + data[i]['@meal'] + '\n' + bcolors.ENDC) # Print what meal it is, i.e. Lunch or Dinner

            if data[i]['@disabled'] == '0': # If the meal is not 'disabled', in other words, if the canteen is in fact serving this meal
                # Iterate through all the diffent options on the menu
                for x in range(len(data[i]['items']['item'])):
                    if '#text' in data[i]['items']['item'][x]: # If the option name has a corresponding value (food), print both the name and the value
                        print(bcolors.WARNING + data[i]['items']['item'][x]['@name'] + bcolors.ENDC + ': ' + bcolors.BOLD +  data[i]['items']['item'][x]['#text'] + bcolors.ENDC)

            else:
                print(bcolors.FAIL + data[i]['@disabled'] + bcolors.ENDC) # If the meal is 'disabled', print the disable message included in the data
        
            print()

        print(bcolors.UNDERLINE + '\nBom Apetite!\n' + bcolors.ENDC)

if __name__ == "__main__":
	main()