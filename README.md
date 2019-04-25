# Meals@UA

### A python script that presents the menus at all of the University of Aveiro's canteens.

![example](https://i.imgur.com/B0glhF6.png)

Migrated from [this repository](https://github.com/RodrigoRosmaninho/ementas-ua) and [this repository](https://github.com/tuxPT/ua-meals-script).
#### Requirements:

- Python 3
- Additional pip libraries installed automatically by [install.sh](https://github.com/GLUA-UA/meals-ua/blob/master/install.sh) or by running:
```
pip3 install -r requirements.txt
```

By default, the script presents the menus of the current day at the 3 canteens located on the main campus.

You can, however, use additional arguments such as **-w** or **-l** to show menus for the whole week, or in a different location.

#### Usage:

After cloning this repository, navigate to its directory, and run:
```
./install.sh
```
Which installs the necessary dependencies and places a symlink in **$HOME/.local/bin**

Now you can use the script by running:

```
ementas
```

##### Optional arguments:
                  
| Argument    | Function                           |
| ----------- | ---------------------------------- |
| -h, --help  | Show help message                  |
| -w          | Present menus for the current week |
| -t          | Present the initial tutorial       |
| -l number   | Specify canteens to present:<br>1 - Campus (Santiago, Crasto, Snack, and AFUAv)<br>2 - ESTGA<br>3 - University Restaurant<br>4 - ESAN |

           

##### Examples:
![loc](https://i.imgur.com/CVeWxIE.gif)
![help](https://i.imgur.com/7nbEmkl.gif)

#### Thanks:
- [Luís Silva](https://github.com/LudeeD)
- University of Aveiro's public API. More information about the specific menu API [here](http://api.web.ua.pt/en/services/universidade_de_aveiro/ementas).


#### Contributing:
GLUA welcomes pull requests from the community.
This section will soon be expanded
