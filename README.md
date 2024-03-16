# Discord Server Template
This is an easy-to-use Discord server template and a Discord bot for it. Just click [this link](https://discord.new/CTX2M8MF4mun)

## Required installations
> **_NOTE:_**  You can skip this section if you already have [Python](https://python.org) and [Git](https://git-scm.com) installed.

In order for the bot to work, you need the programming language [Python](https://python.org). This bot is written using [Python 3.10.8](https://www.python.org/downloads/release/python-3108). To install it, just scroll down and look for the installer for your [operating system](https://en.wikipedia.org/wiki/Operating_system). After that, just follow the setup process.\
You will also need [Git](https://git-scm.com) to clone this repository. Head over to the [downloads section](https://git-scm.com/downloads), choose the installer for your operating system and follow the setup process.\

## Setup
To make sure the bot is working, you need to rename the `example.config.json` file to `config.json` and replace the example values with yours. Explanation of the values:
```json
{
    "verification_channel_id": The channel ID of the channel for the verification message (NOT IN SPEECHMARKS),
    "verified_role_id": The role ID of the role that is given to the user when verifying (NOT IN SPEECHMARKS)
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
We are using [pip](https://en.wikipedia.org/wiki/Pip_(package_manager)), the Python package manager, for installing the dependencies. For simplicity, this repository contains a `.txt` file that contains all required packages. To install all the packages, simply run:
```bash
pip install -r requirements.txt
```

## Final step: starting the bot
To start the bot, simply run:
```bash
python main.py
```
Please note that the command can vary depending on you operation system. Just use your favourite [search engine](https://en.wikipedia.org/wiki/Search_engine) and look it up for your operating system.