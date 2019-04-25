#!/usr/bin/env python3

# GLUA - Grupo de Linux da Universidade de Aveiro - 2019
# Visit https://glua.ua.pt or https://www.facebook.com/glua.ua/ for more information about us
# https://github.com/GLUA-UA/meals-ua

# Developed mainly by GLUA members:
# - Rodrigo Rosmaninho
# - Leonardo Costa
# - André Alves

# Helped by pull requests from:
# - Luís Silva

# Made possible by the University of Aveiro's public API

# VERSION 3

# Necessary imports
import urllib.request as urllib
import sys, os
import argparse
import json
from os.path import expanduser
from datetime import datetime

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

# See delete_last_prints()
CURSOR_UP_ONE = '\x1b[1A'
ERASE_LINE = '\x1b[2K'

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
                    help='Especifica os refeitórios a apresentar: 1 - Campus (Santiago, Crasto, Snack, e AFUAv), 2 - ESTGA, 3 - Restaurante Universitário, 4 - ESAN',
                    )

# Save JSON config file on the user's home directory
def save_config_file():
    file = open(home + "/.ementasrc", "w")
    json_data = json.loads("{}")
    json_data["skip_tutorial"] = True
    file.write(json.dumps(json_data))

# Show Tutorial
def show_tutorial():
    print(bcolors.OKGREEN + '************************* Tutorial *************************' + bcolors.ENDC)
    print("Bem vindo. Este tutorial apenas aparecerá uma vez.")
    print("Este script serve para conseguir facilmente consultar as ementas dos vários refeitórios da Universidade de Aveiro.")
    print("Por omissão, são apresentadas as ementas do dia atual nos refeitórios do campus da UA (Santiago, Crasto, e Snack)")
    print("No entanto, pode utilizar o parâmetro " + bcolors.BOLD + "-w" + bcolors.ENDC + " para visualizar as ementas de toda a semana e o parâmetro " + bcolors.BOLD + "-l" + bcolors.ENDC + " para especificar o local a consultar, sendo que:")
    print(" " + bcolors.BOLD + "-l 1" + bcolors.ENDC + " devolve as ementas no Campus\n " + bcolors.BOLD + "-l 2" + bcolors.ENDC + " devolve as ementas na ESTGA\n " + bcolors.BOLD + "-l 3" + bcolors.ENDC + " devolve as ementas no Restaurante Universitário\n " + bcolors.BOLD + "-l 4" + bcolors.ENDC + " devolve as ementas na ESAN")
    print("É possível conjugar ambos os parâmetros. Por exemplo, " + bcolors.BOLD + "ementa -w -l 2" + bcolors.ENDC + " devolve todas as ementas da semana correnta na ESTGA")
    print("\nSe ainda não o fez, deveria correr o script 'install.sh' incluído neste diretório.\nDesta forma, poderá executar o programa de forma fácil e sem ter de navegar até ao diretório para onde o descarregou.")
    print("Para o fazer, execute os seguintes comandos:" + bcolors.WARNING + "\nchmod +x install.sh\n./install.sh" + bcolors.ENDC)
    print("\nEste software é open-source e o código pode ser consultado em: " + bcolors.OKBLUE + "https://github.com/GLUA-UA/meals-ua" + bcolors.ENDC)
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
                show_tutorial()
        else:
            save_config_file()
            show_tutorial()
    else:
        save_config_file()
        show_tutorial()

# Determine whether there is internet access, return boolean
def internet_on():
    try:
        urllib.urlopen('http://www.google.pt', timeout=1)
        return True
    except urllib.URLError as err:
        return False

# Deletes last x prints (x = number)
def delete_last_prints(number):
    for _ in range(number):
        sys.stdout.write(CURSOR_UP_ONE)
        sys.stdout.write(ERASE_LINE)


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

# Query UA API for meal information and print it on the CLI
def query_UA_API(place, date):
    # Try to import xmltodict. If the module is not found, print an error and quit program
    try:
        import xmltodict
    except:
        print("\nErro! Módulo 'xmltodict' não encontrado! Siga as instruções no README.md para instalar e volte a correr o programa.")
        print("Ou faça sh ./install.sh no diretório deste ficheiro.")
        sys.exit()

    try:
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

    except:
        # Error has occured, print error message
        print(bcolors.FAIL + "Ocorreu um erro ao obter a informação das ementas na UA!\n  Por favor tente novamente. Se o erro persistir contacte o GLUA." + bcolors.ENDC)


# Scrap and print data from AFUAv's facebook page, where they regularly post the menu 
def query_AFUAv(hour):
    from lxml import etree, html
    import requests

    print(bcolors.OKBLUE + '================== ' + '{: ^22}'.format("AFUAv") + ' ==================\n' + bcolors.ENDC) # Prints the name of the canteen properly formatted. The space between the '=' must be 22 characters.

    print(bcolors.WARNING + "A obter os dados da página do facebook. Por favor aguarde..." + bcolors.ENDC)
    
    try: 
        f = requests.get('https://www.facebook.com/AFUAv-1411897009022037/', headers={'Connection':'close'})
        # Parse etree from html string
        doc = html.fromstring(f.content)
        # Filter by post
        posts = doc.xpath('//div[contains(@class, "userContentWrapper")]')
        ignore = ['Boa', 'Bom', 'Hoje', 'Ficamos', 'Ver', '...', '🍽️']
        for p in posts:
            # Convert utc timestamp to datetime object
            t = datetime.utcfromtimestamp(int(p.xpath('.//@data-utime')[0]))
            view = None
            if hour >= t.hour and ((t.hour in [11, 12] and hour < 14) or (t.hour in [18, 19] and hour < 22)):
                show = True
            else:
                show = True
            if show:
                view = ''
                # Get all text in the post
                meal = p.xpath(
                    './/div[@class="text_exposed_root"]//*[self::p or self::span]/text()')
                for m in meal:
                    # Show only dishes
                    if not any(sub in m for sub in ignore) and m != ' ':
                        view += m.strip() + '\n'
                
                # Delete standby print and print final result
                delete_last_prints(1)
                print(bcolors.WARNING + "Pratos disponíveis" + bcolors.ENDC + ":")
                print(bcolors.BOLD + view + bcolors.ENDC, end="")
                break
            else:
                continue
    except:
        # Error has occured, likely related to the request
        # Delete standby print and print error message
        delete_last_prints(1)
        print(bcolors.FAIL + "Ocorreu um erro ao obter a informação da página do facebook da AFUAv!\n  Por favor tente novamente. Se o erro persistir contacte o GLUA." + bcolors.ENDC)

def main():
    print(bcolors.OKGREEN + '\n%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n' + bcolors.ENDC + bcolors.BOLD +
        '                       Ementas na UA\n' + bcolors.ENDC + bcolors.OKGREEN + '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%' + bcolors.ENDC)
    print('By GLUA - Grupo de Linux da Universidade de Aveiro\n')

    # Get arguments
    global args
    args = parser.parse_args()

    if args.showTutorial:
        show_tutorial()
        sys.exit()

    check_config()  

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
            # UA's Main Campus
            place = "santiago"

        # Query and print UA API data for selected location and time period
        query_UA_API(place, date)

        # Query and print AFUAv data (only for UA's main campus and for the same day)
        if(place == "santiago" and date == "day"):
            now = datetime.now().hour
            query_AFUAv(now)

        print(bcolors.UNDERLINE + '\nBom Apetite!\n' + bcolors.ENDC)

if __name__ == "__main__":
	main()
