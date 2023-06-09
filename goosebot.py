# goosebot.py
import os
import discord
from dotenv import load_dotenv
from loguru import logger as lg
import random
import json
import requests
import silly
from dinosay import dinostring, DINO_ALIAS
from art import randart

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
HF_TOKEN = os.getenv('HUGGINGFACE_TOKEN')
HF_ENDPOINT = os.getenv('HUGGINGFACE_ENDPOINT')
hf_model_name = HF_ENDPOINT.split('models/')[-1]

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

hf_headers = {"Authorization": f"Bearer {HF_TOKEN}"}

dino_types = ['trex', 'dim', 'anky', 'hypsi', 'stego', 'deino',
              'ptero', 'archa', 'maia', 'plei', 'brachio', 'cory',
              'para', 'trice']
dino_moods = ['normal', 'happy', 'joking', 'lazy', 'tired', 'nerd',
              'cyborg' ,'dead', 'trance', 'stoned']

automemes = {
    0: (['shit','dick'],'https://i.imgflip.com/1dash3.jpg'),
    1: (['fuck','cunt'], 'https://media1.giphy.com/media/3og0IN2YJFptu9DQAw/giphy.gif?cid=ecf05e47spqkpeeoe25uwfngckvukz0tgbu2whbqhtnuducm&ep=v1_gifs_search&rid=giphy.gif&ct=g'),
    2: (['donkeyballs','clam'], 'https://media2.giphy.com/media/KVKG8XoDvr1du/giphy.gif?cid=ecf05e47uthkxi11rsqzzkcjwwru4zmwv1g9o8w6vf8bhvs0&ep=v1_gifs_search&rid=giphy.gif&ct=g'),
    3: (['love'], 'https://media3.giphy.com/media/LWTxLvp8G6gzm/giphy.gif?cid=ecf05e47gz5eh8dqea32ckqzr29d3huzs7jsmnf2w3xmo440&ep=v1_gifs_search&rid=giphy.gif&ct=g'),
    4: (['disney'], 'https://media4.giphy.com/media/vLsy43kpku5pK/giphy.gif?cid=ecf05e47uvzlk8kk31veji9a80mwx4trphtc0oz0mh3gl7rx&ep=v1_gifs_search&rid=giphy.gif&ct=g'),
    5: (['goosebot', 'goose'], 'https://media4.giphy.com/media/see1sKEEvFNOzWDmee/giphy.gif?cid=ecf05e47cbc27mnqsyqc9kextzvv6w61yt4wikhvmefkpk37&ep=v1_stickers_search&rid=giphy.gif&ct=s'),
    6: (['mom', 'mother', 'mommy', 'mama'], 'https://media2.giphy.com/media/hBuS0iZaB2CamQqxBg/giphy.gif?cid=ecf05e47qe6d3d573oxk8eeolel12dhici8g3vi25s9qpqqw&ep=v1_gifs_search&rid=giphy.gif&ct=g'),
    7: (['ninja'], 'https://media3.giphy.com/media/kwCJA19mepUJSbAebj/giphy.gif?cid=ecf05e47kai7pcuz6alf9moq2991r5lerpdl6vjsaaww7x5v&ep=v1_gifs_search&rid=giphy.gif&ct=g')
}

command_descriptions = f"""
* chat : <your cool chat>
    * 🗣️ Send whatever you write for "<your cool chat>" to chatbot {hf_model_name}
* catfact
    * 🐱 Cool cat fact from *meowfacts* (https://github.com/wh-iterabb-it/meowfacts)
* catpic
    * 🐈 Cool cat picture from *CataaS* (https://cataas.com/#/)
* catgif
    * 🐈‍⬛ Cool cat gif from *CataaS* (https://cataas.com/#/)
* kitten
    * 😻 Same as `catpic`, so better than `puppy`
* puppy
    * 🐶 Dog picture from *DogCEO* (https://dog.ceo/) that probably isn't as cool as the cat pictures 
* fox
    * 🦊 Fox picture from *RandomFox* (https://randomfox.ca/) -- no, it's not a picture of your mom
* poop
    * 💩 Same as `fox`. LMAO
* advice
    * 📝 Advice from *AdviceSlip* (https://api.adviceslip.com/)
* momjoke
    * 💃🏽 Fun jokes from the sexist-named *ICanHazDadJoke* (https://icanhazdadjoke.com/)
* numfact : <your cool number>
    * 🔢 Fun facts about "<your cool number>" from *NumbersAPI* (http://numbersapi.com/#42)
* yesno : <your cool question>
    * 🔮 Provide a Yes or No answer to "<your cool question>" from *yesno.wtf* (https://yesno.wtf/)
* sillyname
    * 🤪 Provide a silly name and email address from *silly*(https://github.com/cube-drone/silly)
* sillystory
    * 🐵 Provide a silly story from *silly* (https://github.com/cube-drone/silly)
* dinosay : <your cool phrase>
    * 🦖 Dinosaur says "<your cool phrase>" from *dinosay* (https://github.com/MatteoGuadrini/dinosay)
* art
    * 🎨 Draw a random 1-line picture from *art* (https://github.com/sepandhaghighi/art)
"""

hello_message = f"""
Hi, folks!! 🎉 🎊 🥳

My name is GooseBot. I'm a bot for the original Goose. I will respond to some keywords (they're a surprise). I also have a list of commands to do fun things.  

🛎️ All commands must start with ***!gb***. For example, if you want to chat about cats with me, then you type something like
```
!gb chat : I sure love cats!
```
or, if you want a cat fact, the you type
```
!gb catfact
```
Try typing 
```
!gb list commands
```
to get started.

Have fun!!!!!111!!!11!!!11 🍕🍕🔥🔥🔥
"""

@client.event
async def on_ready():
    lg.info(f'{client.user} is connected to ...')
    for guild in client.guilds:
        lg.info(f'\t--> {guild.name} (id: {guild.id})')
        members = ', '.join([member.name for member in guild.members])
        lg.info(f'\t  --o party: {members}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if '!gb' != message.content[0:3].lower():
        if ("hi goosebot" in message.content.lower()) or ("hello goosebot" in message.content.lower()):
            await message.channel.send(hello_message)
        for ret in automemes:
            m_tup = automemes[ret]
            send_me = False
            for check in m_tup[0]:
                if check in message.content.lower():
                    send_me = True
            if send_me:
                await message.channel.send(m_tup[1])
    else:
        command = message.content[3:].lower()
        if 'list commands' in command:
            await message.channel.send(command_descriptions)
        else:
            if 'chat' in command:
                chat_prompt = command.split(":")[-1]
                hf_chat_log = {
                    'text' : f'"{chat_prompt.strip()}"'
                }
                data = json.dumps(hf_chat_log)
                response = requests.request("POST", HF_ENDPOINT,
                                            headers=hf_headers, data=data)
                m_rep = json.loads(response.content.decode("utf-8"))
                lg.info(f'{HF_ENDPOINT}:: {m_rep}')
                await message.channel.send(m_rep['generated_text'])
            if 'catfact' in command:
                response = requests.request("GET", 'https://meowfacts.herokuapp.com/')
                m_rep = json.loads(response.content.decode("utf-8"))
                lg.info(f'meow:: {m_rep}')
                m_message = m_rep['data'][0]
                await message.channel.send(m_message)
            if ('catpic' in command) or ('kitten' in command):
                response = requests.request("GET", 'https://cataas.com/cat?json=true')
                m_rep = json.loads(response.content.decode("utf-8"))
                await message.channel.send('https://cataas.com' + m_rep['url'])
            if 'catgif' in command:
                response = requests.request("GET", 'https://cataas.com/cat/gif?json=true')
                m_rep = json.loads(response.content.decode("utf-8"))
                await message.channel.send('https://cataas.com' + m_rep['url'])
            if 'puppy' in command:
                response = requests.request("GET", 'https://dog.ceo/api/breeds/image/random')
                m_rep = json.loads(response.content.decode("utf-8"))
                await message.channel.send(m_rep['message'])
            if ('fox' in command) or ('poop' in command):
                response = requests.request("GET", 'https://randomfox.ca/floof/')
                m_rep = json.loads(response.content.decode("utf-8"))
                await message.channel.send(m_rep['image'])
            if 'advice' in command:
                response = requests.request("GET", 'https://api.adviceslip.com/advice')
                m_rep = json.loads(response.content.decode("utf-8"))
                await message.channel.send(m_rep['slip']['advice'])
            if 'momjoke' in command:
                headers = {"Accept": "application/json"}
                response = requests.request("GET", 'https://icanhazdadjoke.com/',
                                            headers=headers)
                m_rep = json.loads(response.content.decode("utf-8"))
                lg.info(f'dadjoke:: {m_rep}')
                await message.channel.send(m_rep["joke"])
            if 'numfact' in command:
                num_prompt = command.split(":")[-1].strip()
                response = requests.request("GET", 'http://numbersapi.com/' + num_prompt)
                m_rep = response.content.decode("utf-8")
                await message.channel.send(m_rep)
            if 'yesno' in command:
                response = requests.request("GET", 'https://yesno.wtf/api')
                m_rep = json.loads(response.content.decode("utf-8"))
                await message.channel.send(m_rep['image'])
            if 'sillyname' in command:
                m_message = f'Name: {silly.name(capitalize=True)}\n'
                m_message += f'Tag: {silly.name(slugify=True)}\n'
                m_message += f'Email: {silly.email()}\n'
                m_message += f'DOB: {silly.datetime().year}-{silly.datetime().month}-{silly.datetime().day}\n'
                m_message += f'Homepage: {silly.domain()}\n'
                await message.channel.send(m_message)
            if 'sillystory' in command:
                await message.channel.send(silly.markdown())
            if 'dinosay' in command:
                dino_words = command.split(":")[-1]
                m_message = dinostring(dino_words,
                                       DINO_ALIAS[random.choice(dino_types)],
                                       random.choice(dino_moods))
                await message.channel.send(f"```\n{m_message}\n```")
            if 'art' in command:
                await message.channel.send(f"```\n{randart()}\n```")

@client.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise

client.run(TOKEN)
