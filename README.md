# Discord Server Template
This is the Discord bot for [this Discord server template](https://discord.new/CTX2M8MF4mun).

## Creating a bot and inviting it
First, create a new application in the [Discord Developer Portal](https://discord.com/developers/applications).\
<img src="https://zip.lynix.me/u/eJzia0.png">
After that, go the "Bot" section on the left side and enable all Priviledged Gateway Intents.\
<img src="https://zip.lynix.me/u/LBYJGi.png">
Then, you have to get a bot token in order to log into your bot using code. You can get a bot token by pressing the "Reset Token" button.
<img src="https://zip.lynix.me/u/mHpyxQ.png">
Now, rename the `example.env` file to `.env` and paste the token.
```
TOKEN = 
```
Now, go to the "OAuth2" section and click the "bot" scope and then then click the "Administrator" permission.
<img src="https://zip.lynix.me/u/Jk1ZVa.png">
<img src="https://zip.lynix.me/u/OBjtfC.png">
The last step is to copy the generated URL, paste it into your browser search bar and choose the server you want to add the bot to. Please note that you need the `MANAGE_SERVER` permission to add the bot.
<img src="https://zip.lynix.me/u/krp3BO.png">
<img src="https://zip.lynix.me/u/ZPhWZ1.png">
Also, make the bot's role the highest in the server (as shown in the image below).
<img src="https://zip.lynix.me/u/mbWEB6.png">

## Required installations
> **_NOTE:_**  You can skip this section if you already have [Python](https://python.org) and [Git](https://git-scm.com) installed.

In order for the bot to work, you need the programming language [Python](https://python.org). This bot is written using [Python 3.10.8](https://www.python.org/downloads/release/python-3108). To install it, just scroll down and look for the installer for your [operating system](https://en.wikipedia.org/wiki/Operating_system). After that, just follow the setup process.\
You will also need [Git](https://git-scm.com) to clone this repository. Head over to the [downloads section](https://git-scm.com/downloads), choose the installer for your operating system and follow the setup process.\

## Setup
To make sure the bot is working, you need to rename the `example.config.json` file to `config.json` and replace the example values with yours. Explanation of the values:
```json
{
    "verification_channel_id": The channel ID of the channel for the verification message (NOT IN QUOTATION MARKS),
    "verified_role_id": The role ID of the role that is given to the user when verifying (NOT IN QUOTATION MARKS),
    "moderator_role_id": The role ID of the moderator role (NOT IN QUOTATION MARKS),
    "admin_role_id": The role ID of the admin role (NOT IN QUOTATION MARKS),
    "ticket_opening_channel_id": The channel ID of the channel for opening a ticket,
    "ticket_category_id": The category ID of the category for the ticket channels
}
```

## Cloning the repository
For cloning the repository, run:
```bash
git clone https://github.com/vxsualized/discord-server-template
```
You can then access the folder by using:
```bash
cd discord-server-template
```

## Installation of the dependencies
We are using [pip](https://en.wikipedia.org/wiki/Pip_(package_manager)), the Python package manager, for installing the dependencies. For simplicity, this repository contains a `requirements.txt` file that contains all required packages. To install all the packages, simply run:
```bash
pip install -r requirements.txt
```

## Final step: starting the bot
To start the bot, simply run:
```bash
python main.py
```
Please note that the command can vary depending on you operation system. Just use your favourite [search engine](https://en.wikipedia.org/wiki/Search_engine) and look it up for your operating system.