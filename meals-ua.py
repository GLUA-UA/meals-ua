#!/usr/bin/env python3

# GLUA - Grupo de Linux da Universidade de Aveiro - 2023
# Visit https://glua.ua.pt or https://www.facebook.com/glua.ua/ for more information about us
# https://github.com/GLUA-UA/meals-ua

# Developed mainly by GLUA members:
# - Rodrigo Rosmaninho
# - Leonardo Costa
# - André Alves

# Helped by pull requests from:
# - Luís Silva

# Made possible by the University of Aveiro's public API

# VERSION 4

# Necessary imports
import urllib.request as urllib
import sys, os
import argparse
import json
import requests
import time
import threading
from os.path import expanduser
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

done_loading = False

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
                    default=5,
                    help='Especifica os refeitórios a apresentar: 1 - Campus (Santiago, Crasto, Grelhados), 2 - ESTGA, 3 - ESAN, 4 - Restaurante Universitário, 5 - Restaurante Vegetariano',
                    )

places = {
    "Campus": [
        "Santiago",
        "Crasto",
        "Grelhados"
    ],
    "ESTGA": ["ESTGA"],
    "ESAN": ["ESAN"],
    "Restaurante": ["Restaurante Universitário"],
    "Vegetariano" : ["Vegetariano", "Restaurante Vegetariano"]
}

replace = {
    "Santiago": "Refeitório de Santiago",
    "Crasto": "Refeitório do Crasto",
    "ESTGA": "Refeitório da ESTGA",
    "ESAN": "Refeitório da ESAN"
}

class Day:
    def __init__(self, date, place):
        self.date = date
        self.place = place
        self.locations = {}

    def __str__(self):
        res = bcolors.WARNING + '****************** ' + bcolors.HEADER + bcolors.BOLD + '{: ^22}'.format(self.date.strftime("%a, %d %b %Y")) + bcolors.WARNING + ' ******************\n\n' + bcolors.ENDC # Prints the day properly formatted. The space between the '=' must be 22 characters.
        for place in places[self.place]:
            location = replace[place] if place in replace else place
            res += bcolors.OKBLUE + '================== ' + '{: ^22}'.format(location) + ' ==================\n\n' + bcolors.ENDC # Prints the name of the canteen properly formatted. The space between the '=' must be 22 characters.
            if place in self.locations:
                res += str(self.locations[place]["Almoço"])
                res += str(self.locations[place]["Jantar"])
            else:
                res += bcolors.FAIL + "De momento não há informações sobre a ementa neste refeitório" + bcolors.ENDC + "\n\n"
        return res
    

class Meal:
    def __init__(self, period):
        self.period = period
        self.soup = ""
        self.options = []

    def __str__(self):
        if self.options != []:
            res = bcolors.UNDERLINE + self.period + '\n' + bcolors.ENDC
            res += bcolors.WARNING + "Sopa" + bcolors.ENDC + ': ' + bcolors.BOLD +  self.soup.capitalize() + bcolors.ENDC + "\n"
            for option in self.options:
                res += bcolors.WARNING + option[0].title() + bcolors.ENDC + ': ' + bcolors.BOLD + option[1].capitalize() + bcolors.ENDC + "\n"
            return res + "\n"
        return ""

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
    print(" " + bcolors.BOLD + "-l 1" + bcolors.ENDC + " devolve as ementas no Campus\n " + bcolors.BOLD + "-l 2" + bcolors.ENDC + " devolve as ementas na ESTGA\n "  + bcolors.BOLD + "-l 3" + bcolors.ENDC + " devolve as ementas na ESAN\n " + bcolors.BOLD + "-l 4" + bcolors.ENDC + " devolve as ementas no Restaurante Universitário")
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

def animate_loading():
    i = 0
    while True:
        sys.stdout.write('\r' + bcolors.WARNING + 'Por favor aguarde enquanto os serviços da UA processam o pedido' + ("." * i) + (" " * (3-i)) + bcolors.ENDC)
        i = (i + 1) % 4
        sys.stdout.flush()
        time.sleep(0.33)
        if done_loading:
            sys.stdout.write('\r' + (' ' * 66))
            sys.stdout.flush()
            sys.stdout.write('\r')
            sys.stdout.flush()
            break

# Query UA API for meal information and print it on the CLI
def query_UA_API(place, date):
    global done_loading

    try:
        today = datetime.combine(datetime.now().date(), datetime.min.time())
        dates = [today] if date == "day" else [(today + timedelta(days=i)) for i in range(0,7)]
        info = {d.isoformat(): Day(d, place) for d in dates}

        url = "https://wso2-gw.ua.pt/mysas_mysas/v1/Refeicoes/GetAgendaMenusEntreDatas?inicio=" + dates[0].date().isoformat() + "&fim=" + dates[-1].date().isoformat()
        headers = {
            'Content-Type': 'application/json',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept': '*/*'
        }

        t = threading.Thread(target=animate_loading)
        t.start()
        response = requests.request("GET", url, headers=headers, data={}).json()
        done_loading = True
        t.join()

        for i in range(len(response)-1):
            meal = response[i]
            location = meal["Refeitorios"][0]
            if location not in info[meal["Data"]].locations:
                info[meal["Data"]].locations[location] = {"Almoço": Meal("Almoço"), "Jantar": Meal("Jantar")}
            for component in meal["Componentes"]:
                if component["TipoString"] == "Sopa":
                    info[meal["Data"]].locations[location][meal["Periodo"]].soup = component["Nome"]
                else:
                    info[meal["Data"]].locations[location][meal["Periodo"]].options.append((meal["Nome"], component["Nome"]))

        for day in dates:
            print(info[day.isoformat()], end="")

    except:
        # Error has occured, print error message
        done_loading = True
        t.join()
        print(bcolors.FAIL + "Ocorreu um erro ao obter a informação das ementas na UA!\n  Por favor tente novamente. Se o erro persistir contacte o GLUA." + bcolors.ENDC + "\n")

# Scrap CMS website for meal information and print it on the CLI
def query_CMS(place, date):
    file = urllib.urlopen('https://cms.ua.pt/ementas/ementas')
    response = file.read()
    file.close()

    soup = BeautifulSoup(response, 'html.parser')

    # Get the table with the meal data div class view-content
    table = soup.find('div', {'class': 'view-content'})

    if table is None:
        handle_key_error(args.displayZone)

    # Get all the canteens of the table
    canteens = table.find_all('table', {'class': 'tabelahead views-table cols-3 tablesaw tablesaw-stack'})

    menu = {}

    # Loop through all the canteens
    for canteen in canteens:
        # Get the caption of the table (the name of the canteen)
        caption = canteen.find('caption').text.split(': ')[1]
        if (caption != "Restaurante Vegetariano"):
            continue
        # Get the meals of the canteen
        meals = canteen.find_all('tr')

        # Filter the first meal (the header of the table)
        meals = meals[1:]

        menu[caption] = {}

        # Loop through all the meals
        for meal in meals:
            # Get the meal header
            # header = meal.find('td', {'class': 'views-field views-field-title'}).text

            header = meal.find('td', {'class': 'views-field views-field-title'})
            if (header == None):
                continue
            header = header.text

            header = header.strip().split(' ')

            # Get the meal date and whether it is lunch or dinner
            if (caption == 'Restaurante Vegetariano'):
                lunchOrDinner = 'Almoço'
            else:
                lunchOrDinner = header[0]
            meal_date = header[-1]

            if meal_date not in menu[caption]:
                menu[caption][meal_date] = {}

            # Get the meal options if it isn't specified whether it is lunch or dinner
            if lunchOrDinner != 'Almoço' and lunchOrDinner != 'Jantar':
                # Get the meal options
                meal_name = meal.find('td', {'class': 'views-field views-field-body'})
                if (caption != "TrêsDê"):
                    items = meal_name.find_all('p')
                else:
                    items = meal_name.find_all('li')
                
                if (not items):
                    continue

                if "Almoço" not in menu[caption][meal_date]:
                    menu[caption][meal_date]["Almoço"] = {}

                if "Jantar" not in menu[caption][meal_date]:
                    menu[caption][meal_date]["Jantar"] = {}

                if "Almoço" not in items[0].text:
                    continue

                lunch = True
                # Loop through all the meal options
                for item in items:
                    if "Jantar" in item.text:
                        lunch = False

                    if "Almoço" in item.text or "Jantar" in item.text or item.text.rstrip() == "":
                        continue

                    plate = item.text.strip().replace(u'\xa0', u' ')

                    if plate == "":
                        continue

                    plate_name, plate_description = parse_plate(plate)
                    menu[caption][meal_date]["Almoço" if lunch else "Jantar"][plate_name] = plate_description

                continue

            # Get the meal options
            meal_name = meal.find('td', {'class': 'views-field views-field-body'})
            items = meal_name.find_all('p')

            if lunchOrDinner not in menu[caption][meal_date]:
                menu[caption][meal_date][lunchOrDinner] = {}

            # Loop through all the meal options
            num_plate = 0
            for plate in items:
                plate = plate.text.strip().replace(u'\xa0', u' ')

                if plate == '':
                    continue

                # Get the name and description of the meal option

                if (caption == "Restaurante Vegetariano"):
                    if (num_plate == 0):
                        plate_name = 'Sopa'
                        plate_description = plate
                        first_plate = False
                    else:
                        plate_name = f'Opção Buffet {num_plate}'
                        plate_description = plate
                    num_plate += 1
                else:
                    plate_name, plate_description = parse_plate(plate)
                print(plate_name)
                print(plate_description)

                # Add the meal option to the menu
                menu[caption][meal_date][lunchOrDinner][plate_name] = plate_description

    printCanteens = []
    printDates = []

    # Print the menu
    if place == 'campus':
        printCanteens.append('Santiago')
        printCanteens.append('Crasto')
        printCanteens.append('Grelhados')
    elif place == 'estga':
        printCanteens.append('ESTGA')
    elif place == 'rest': 
        printCanteens.append('Restaurante Universitário')
    elif place == 'vegetariano':
        printCanteens.append('Restaurante Vegetariano')

    # if place == 'vegetariano':
    #     printCanteens.append('Restaurante Vegetariano')

    if date == 'day':
        # Get the current date
        now = datetime.now().strftime('%d/%m/%Y')
        printDates.append(now)
    elif date == 'week':
        # Get all the dates of the current week
        now = datetime.now()
        
        start = now - timedelta(days=now.weekday())
        end = start + timedelta(days=6)

        for i in range((end - start).days + 1):
            printDates.append((start + timedelta(days=i)).strftime('%d/%m/%Y'))

    # Loop through all the canteens
    for canteen in menu:
        # Check if the canteen is one of the canteens to be printed
        if canteen not in printCanteens:
            continue

        # Loop through all the dates
        for meal_date in menu[canteen]:
            # Check if the date is one of the dates to be printed
            if meal_date not in printDates:
                continue

            print(bcolors.WARNING + '****************** ' + bcolors.HEADER + bcolors.BOLD + '{: ^22}'.format(meal_date) + bcolors.WARNING + ' ******************\n' + bcolors.ENDC)
            print(bcolors.OKBLUE + '================== ' + '{: ^22}'.format(canteen) + ' ==================\n' + bcolors.ENDC)

            # Loop through all the meals
            for meal in menu[canteen][meal_date]:
                print(bcolors.UNDERLINE + meal + '\n' + bcolors.ENDC) # Print what meal it is, i.e. Lunch or Dinner

                # Loop through all the meal options
                for plate in menu[canteen][meal_date][meal]:
                    print(bcolors.WARNING + plate + bcolors.ENDC + ': ' + bcolors.BOLD +  menu[canteen][meal_date][meal][plate] + bcolors.ENDC)

                print()

# Parse the meal option name and description
def parse_plate(plate):
    if '-' in plate:
        meal = plate.split(' - ')
        
        name = meal[0]
        description = meal[-1]
    else:
        name = plate.split(' ')[0]
        description = plate

    return name, description

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
                time_of_day = "Almoço" if t.hour in range(8, 15) else "Jantar"
                print(bcolors.UNDERLINE + time_of_day + bcolors.ENDC)
                print(f"(Post a {t.day}/{t.month} às {t.hour}h{t.minute})\n")
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
    print('By Grupo de Linux da Universidade de Aveiro (glua.ua.pt)\n')

    # Get arguments
    global args
    args = parser.parse_args()

    if args.showTutorial:
        show_tutorial()
        sys.exit()

    check_config()  

    #if not internet_on():  # If there is no internet print errors
    #    print(bcolors.FAIL +
    #        '=========================== ERRO ===========================' + bcolors.ENDC)
    #    print(bcolors.FAIL + 'Não existe conexão à internet.\nEste script necessita de uma ligação estável à internet para aceder ao API da UA.\n' + bcolors.ENDC)

    if args.showWeek:
        date = "week"
    else:
        date = "day"

    if args.displayZone == 2:
        place="ESTGA"
    elif args.displayZone == 3:
        place = "ESAN"
    elif args.displayZone == 4:
        place = "Restaurante"
    elif args.displayZone == 5:
        place = "vegetariano"
    else:
        # UA's Main Campus
        place = "Campus"

    # Query and print UA API data for selected location and time period
    # query_UA_API(place, date)
    query_CMS(place, date)

    # Query and print AFUAv data (only for UA's main campus and for the same day)
    #if(place == "santiago" and date == "day"):
    #    now = datetime.now().hour
    #    query_AFUAv(now)

    print(bcolors.UNDERLINE + 'Bom Apetite!\n' + bcolors.ENDC)

if __name__ == "__main__":
	main()
