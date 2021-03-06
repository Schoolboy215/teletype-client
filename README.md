# teletype-client

This client is meant to connect to a [TeleType server](https://github.com/Schoolboy215/teleType) and print messages on a thermal receipt printer.

## Installation

1. Start with a fresh installation of raspbian lite
2. Log in as the **pi** user and perform your typical setup (change password from default, run security updates, etc.)
    * **Setting your timezone is important! If you don't do this, all messages will show as UTC**
3. Run the following commands:
    1. `sudo apt-get install git`
    2. `sudo apt-get install libjpeg-dev`
    3. `sudo apt-get install python-pip`
    4. `git clone https://github.com/Schoolboy215/teletype-client`
    5. `cd teletype-client`
    6. `pip install -r requirements.txt`
    7. `python install.py`
        * **Note that at this stage you will be prompted to input a server and repository url. Get the server information from whoever is running your server. Leave the repository default unless you want to get updates from your own fork or something.**
4. Enable the serial hardware on the pi
    1. run the command 'sudo raspi-config'
    2. Select *Interfacing Options* and press `ENTER`
    3. Select *Serial* and press `ENTER`
    4. When asked if you'd like a login shell to be available over serial, select No
    5. When asked if you'd like to enable serial port hardware, select Yes
    6. Select OK to confirm the summary
    7. Select Finish and press `ENTER`
    8. If asked about rebooting, say Yes

  
