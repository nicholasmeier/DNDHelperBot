import discord
import random

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)
tokenfile = open("token.txt", "r")
token = tokenfile.read().splitlines()
tokenfile.close()

def randplayer(g):
    print("TODO THIS")

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    # don't send a message if the bot sent the message
    if message.author == client.user:
        return

    playerRoleID = 0
    # get the users with the role : "Player"
    guild = client.get_guild(message.guild.id)

    if message.content.startswith('!pickplayer'):
        for role in guild.roles:
            if role.name == 'Player':
                user_names = ([m.name for m in role.members])
                await message.channel.send("Picking from the following players: ")
                await message.channel.send(user_names)
                randplayer = random.choice(user_names)
                await message.channel.send(randplayer + ": YOU MUST ROLL!")

client.run(token)
