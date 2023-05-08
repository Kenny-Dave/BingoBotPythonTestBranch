# EchoRidge BingoBot for Discord

BingoBot is a Discord bot that generates random character profiles for a fictional colony.

## Getting Started
### Prerequisites
- Python 3.8 or later
- Discord account

### Installation
1. Clone the repository:

```bash
git clone https://github.com/exampleuser/BingoBot.git
```

2. Enable the python virtual env:

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install the dependencies:
```bash
pip install -r requirements.txt
```

4. Set up a new Discord bot account and get a token from the Discord Developer Portal.

5. Create a .env file in the root directory of the project and add the following line with your bot token:

```makefile
DISCORD_TOKEN=<your-bot-token>
```

## Usage
To start the bot, run the following command:

```bash
python3 Bot.py
```

Once the bot is running, you can interact with it in your Discord server by typing commands that start with `!bingo`.

### Available Commands

See /obj/HelpStrings

## Contributing
Contributions to BingoBot are welcome! If you would like to contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch with a descriptive name: git checkout -b my-new-feature.
3. Make changes and commit them: git commit -am 'Add new feature'.
4. Push to the branch: git push origin my-new-feature.
5. Create a pull request.

## Authors
- Kenny-Dave

## License
This project is licensed under the Apache 2.0 License - see the [license](license) file for details.