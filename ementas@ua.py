# Rodrigo Rosmaninho - MIECT / Universidade de Aveiro
# 2018

import urllib.request as urllib
import xmltodict
import json
from pprint import pprint

print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n              Ementas na UA\n%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n')

file = urllib.urlopen('http://services.web.ua.pt/sas/ementas')
data = file.read()
file.close()

data = json.loads(json.dumps(xmltodict.parse(data)))
data = data['result']['menus']['menu']

for i in range(len(data)):
    pprint(data[i]['@canteen'])