# wowAutoFisher
A small script that automates manual fishing in World of Warcraft.

# Directions:
 
  * Stand by a body of water. Make sure that the water is not too bright, otherwise the contrast with the float may not be sufficient.
  * Scroll completely into the character so that the 1st. person view is active. Thus, the float is not covered by your body.
  * Make sure you have autolooting turned on.
  * Equip a fishing rod.
  * Make sure that no monsters swim by in the water, this would make float detection difficult.
  * You may have to adjust some parameters in the script manually. Such as the screen resolution and the position of the fishing icon.
  * Start the script. 
  * Attention, you should not leave the device. Unobserved fishing could lead to a ban from the server or the deletion of the account!

## Getting Started

These instructions will get you a copy of the project up and running on your local machine.

### Prerequisites

You need some software to run this script
  * Python 3.x
  * pyautogui
  * PIL

#### Recommend

  * I use Autokey to start and stop the script. The hotkey function is very useful.
  * The script can use two methods to perform mouse clicks in the wow clinet. Unfortunately, pyautogui does not work 100 percent reliably when catching the fish. That's why I added the possibility to use xte. This made it possible to achieve westward better stability.

### Installing 

#### Debian based 
```
sudo apt-get update 
sudo apt-get -y upgrade
apt-get install python3 python3-pip autokey-qt xte
cd your_project_folder
git clone https://github.com/StowasserH/wowAutoFisher.git
cd wowAutoFisher
pip install -r requirements.txt
```
#### tbd... 

Since I don't use Windows, someone else can do it ;-)

### running

#### autokey

  * Copy the 2 scripts to your autokey folder or just copy and paste the code into new files.
  * Give the two scripts a hotkey.
  * You can now start and stop the scripts in game using the hotkeys.

## Development

Feel free to use and modify it, but please help me to improve it.

### Coding style

If you commit code pls try to format it in [PEP8](https://www.python.org/dev/peps/pep-0008/)


## Authors

* **Harald Stowasser** - *Initial work* - [StowasserH](https://github.com/StowasserH)

See also the list of [contributors](https://github.com/StowasserH/wowAutoFisher/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details