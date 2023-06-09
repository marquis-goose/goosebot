# GooseBot
> ℹ️ **This is a teaching resource.** GooseBot and this repo are meant to introduce concepts of software development, networking, design, and _making cool things_ rather than just using them. The code is not professional level nor production quality. Do not use this Discord bot for anything serious. 

## So you like Discord?!
Well, why don't we build our own bot? It will do whatever we want. How do we get started?

1. We need a place for the bot to live. I will leave that up to you and your parents (hosting can be expensive 😞).
2. We need the software environment. Make sure `git` is installed and type
```
git clone https://github.com/marquis-goose/goosebot.git
```
Chnage to the `goosebot` directory and make sure you have Python (at least version 3.9) installed, along with `pip`, then type
```
pip install -r requirements.txt
```
3. Remeber GooseBot needs some _secrets_. That's how Discord (and HuggingFace) know its OK to talk to it. So, you need to create that secrets file. Type
```
touch .env
```
Open up your favorite text editor and fill out that `.env` with your own secrets:
```
# .env
DISCORD_TOKEN=<your-discord-token>
DISCORD_GUILD=<your-favorite-guild>
HUGGINGFACE_TOKEN=<your-huggingface-token>
HUGGINGFACE_ENDPOINT=https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill
```
5. You should be ready to go! 👻 Type
```
python goosebot.py
```
and head on over to your favorite Discord server to start the fun.

## How did we get here?
Something very similar to GooseBot can be built by following along with this tutorial: https://realpython.com/how-to-make-a-discord-bot-python/ or following the examples presented in the Discord API: https://discordpy.readthedocs.io/en/stable/

## Where do we go from here?
I'm glad you asked. There's a lot wrong with GooseBot. First and foremost, it doesn't know your name?! Can you update the code in `goosebot.py` to make GooseBot respond to a `hi goosebot` message with your Discord name?

Here's some other things to try:
* GooseBot only chats in the most basic way (without remember what was said before), but the HuggingFace model being used _can_ do better. Can you update GooseBot to be a better chat buddy?
* GooseBot is really only about fun. Can you make it help with your homework? Can you make a new GooseBot command that acts as a simple calculator?
* GooseBot's code is messy. Can you think of ways to make it cleaner and easier to understand?
* Finally, wouldn't be cool if GooseBot had a buddy? Can you create another GooseBot (maybe HonkBot?) for GooseBot to interact with?

Don't be afraid to break GooseBot. It's a toy. It can always be put back together again. Half the fun in trying new things is seeing them fail.

🐦 🦢 🐔
