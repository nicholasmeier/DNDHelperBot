import discord
import logging
import random

# TODO / Ideas
# create selenium func to read from fantasynamegenerator.com
# create a random event function maybe --> encounters etc
# dnd crafting command maybe ?
    # would be like !craft <skill> <player_level> <item_template> <roll_a> <roll_b> <roll_c> <ingr_1> <ingr_2> <ingr_3>
    # and prints out a cool item
# Maybe a DC generator
    # like maybe !DCGen <difficulty:easy|med|hard|extreme> <player_level>
# idk what else



intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

#for debug statements
debug = True

#get tokenfile without exposing token
tokenfile = open("token.txt", "r")
token = tokenfile.read().splitlines()[0]
if debug:
    print(token)
tokenfile.close()

#function for random member of a role in a server
#
# g = guild object
# r_name = role name
# return type : determine whether to return name, obj, id
#
def randmember(g, r_name, return_type):
    for role in g.roles:
        if role.name == r_name:
            users = role.members
            rand_m = random.choice(users)
            if debug:
                print("Picking from the following players: ")
                print(users)
            if return_type == "name":
                return rand_m.name
            if return_type == "id":
                return rand_m.id
            if return_type == "obj":
                return rand_m
    #return nothing if role not found
    return ""

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    # return nothing if message is from this bot
    if message.author == client.user:
        return

    #get guild
    guild = client.get_guild(message.guild.id)

    #
    # !pickplayer command
    # pick from Player role
    #
    if message.content.startswith('!pickplayer') or message.content.startswith('!pp'):
        #parse args for rolling for attribute
        pickplayer_args = message.content.split(" ")
        msg_str = " : Roll a d20"
        mention_p = False

        # arg 1 : skill <what skill you want them to roll>
        if len(pickplayer_args) >= 2:
            roll_for = pickplayer_args[1]
            msg_str = msg_str + " for " + roll_for

        # arg 2 : roll detail <a 1 word flair for your roll request>
        if len(pickplayer_args) >= 3:
            roll_detail = pickplayer_args[2]
            msg_str = msg_str + " " + roll_detail

        # arg 3 : mention | silent
        if len(pickplayer_args) >= 4:
            if pickplayer_args[3] == 'true':
                mention_p = True
            else:
                mention_p = False

        if mention_p:
            # message with mention
            player = randmember(guild, 'Player', "obj")
            await message.channel.send(f"{player.mention}" + msg_str)
        else:
            player = randmember(guild, 'Player', "name")
            await message.channel.send(player + msg_str)

    #
    #  !pickfromrole command
    #  pick from specified role
    #
    if message.content.startswith('!pickfromrole'):
        pickfromrole_args = message.content.split(" ")
        mention_p = False
        if len(pickfromrole_args) < 2:
            await message.channel.send("Incorrect Usage:\n!pickfromrole <role_name> <mention:true|false>")
            return
        role_name = pickfromrole_args[1]
        if len(pickfromrole_args) >= 3:
            if pickfromrole_args[2] == 'true':
                mention_p = True
        if mention_p:
            player = randmember(guild, role_name, "obj")
            await message.channel.send(f"{player.mention}" + " : You have been randomly picked from " + role_name)
        else:
            player = randmember(guild, role_name, "name")
            await message.channel.send(player + ": You have been randomly picked from " + role_name)

    #
    # help command
    #
    if message.content.startswith('!help'):
        help_args = message.content.split(" ")
        help_with = "NOCMD"
        if len(help_args) >= 2:
            help_with = help_args[1]
            if (help_with == "!pickplayer"):
                await message.channel.send("To use this you must have the role \"Player\"")
                await message.channel.send("Use !pickplayer (or !pp) to randomly pick a player for a roll")
                await message.channel.send("Example format:\n!pickplayer <Skill> <detail> <mention:true|false>")
                await message.channel.send("Args, seperated by a space:\nSkill: Roll for what skill check or save\nDetail: a detail about the roll, like \"Save\" or \"Check\"\nMention: true|false mention the random player")
            if (help_with == "!pickfromrole"):
                await message.channel.send("Randomly pick a member of specified role\nFORMAT: !pickplayer <role_name> <mention:true|false>")
        else:
            await message.channel.send("List of commands:")
            await message.channel.send("!pickplayer\n!pickfromrole")
            await message.channel.send("use !help <cmd> for more detailed help")

    #todo : add more commands (if needed)

client.run(token)
