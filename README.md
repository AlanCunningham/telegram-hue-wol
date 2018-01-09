# Telegram SAM

A simple [Telegram bot](https://github.com/python-telegram-bot/python-telegram-bot) that allows control to:
- Philips Hue lights - on/off
- Wake on LAN packets to turn your computer on remotely

# Requirements
- [python-telegram-bot]((https://github.com/python-telegram-bot/python-telegram-bot)
- [Qhue](https://github.com/quentinsf/qhue) - Philips Hue python wrapper
- [wakeonlan](https://pypi.python.org/pypi/wakeonlan/0.2.2) - To send Wake on LAN packets to your computer

# Setup
- Update config.txt with the following:

[telegram]
api_token: your_telegram_api_token
auth_user: your_telegram_user_id - Used to prevent other users from calling WakeOnLan/Philips Hue commands

[computer]  
mac_address: your_computer_mac_address  
ip_address: your_computer_ip_address  

[hue]  
bridge_ip: your_hue_bridge_ip  
user_token: bridge_user_id  
