import os
import discord
import collections
from dotenv import load_dotenv

load_dotenv()
GUILD = os.getenv('DISCORD_GUILD')
# needs to be typecast as a string since getenv returns a string
WC_ID = int(os.getenv('DISCORD_WC_ID'))
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()


@client.event
async def on_ready():

    print(f'{client.user} has connected to Discord\n')
    guild = discord.utils.get(client.guilds, name=GUILD)
    print(
        f'{client.user} is connected to the following Guild:\n'
        f'\t{guild.name} id: {guild.id}'
    )


@client.event
async def on_member_join(member):
    welcome_message = f'Hello {member.name}, welcome to The Library.'

    await member.create_dm()
    await member.dm_channel.send(welcome_message)

    channel = client.get_channel(WC_ID)
    await channel.send(welcome_message)


previous_message = {
    'user': '',
    'consecutive_messages': 0
}


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.clean_content[0] == '!':
        #process for command 
        await process_command(message, message.channel.id)
        return


    # check message author
    if message.author.id == previous_message['user']:
        previous_message['consecutive_messages'] += 1
        if previous_message['consecutive_messages'] > 5:
            await message.author.create_dm()
            await message.author.dm_channel.send(
                f"{message.author.name}, you have sent {previous_message['consecutive_messages']} messages consecutively.\n"
                f'Cease your spam.'
            )
    else:
        previous_message['user'] = message.author.id
        previous_message['consecutive_messages'] = 0

    print(previous_message)


@client.event
async def on_member_update(before, after):
    if before.roles == after.roles or len(before.roles) > len(after.roles):
        return
    else:
        roles = []
        for role in after.roles:
            if role not in before.roles:
                roles.append(role)

        channel = client.get_channel(WC_ID)

        print('CHANNEL:' + str(channel))

        for role in roles:
            await channel.send(f'Congratulations {after.mention}, you have been promoted to:\n\t{role}')


async def process_command(message, channel):
    response = 'No valid command given. Try "!help" for a list of commands'
    content = message.clean_content[1:]
    arguments = content.split(' ')
    arguments.remove('')
    content = arguments.pop(0)

    print(f'RECIEVED COMMAND: {content} WITH ARGUMENTS: {arguments}')

    if content == 'tk':
        response = tk(message.mentions, arguments[1])
    if content == 'help':
        response = 'HELP'
    
    print('PROCESSING COMMAND RESPONSE: ' + response)
    channel = client.get_channel(channel)
    await channel.send(response)
    

def tk(person, amount=0):
    if len(person) > 1:
        return 'No valid command given. Try "!help" for a list of commands'
    person = person[0]
    newScore = {str(person.id): amount}
    name = person.name
    scoreboard = get_scoreboard()
    update_scoreboard(newScore)

    return f'{name} has {scoreboard[str(person.id)]} team kills'

def get_scoreboard():
    scoreboard = {}

    try: 
        with open("tk.txt", 'r+') as file:
            contents = file.read()

            lines = contents.split('\n')
            for line in lines:
                chunks = line.split('|')
                if len(chunks) == 2:
                    scoreboard[chunks[0]] = chunks[1]
            file.seek(0)
    except IOError as e:
        print('ERROR in get_scoreboard: ' + e)

    return scoreboard

def update_scoreboard(newScore):
    scoreboard = get_scoreboard()
    keys = newScore.keys()
    try:
        with open("tk.txt", 'r+') as file:
            for key in keys:
                if key in scoreboard:
                    print(newScore[key] + scoreboard[key])
                    scoreboard[key] = int(newScore[key]) + int(scoreboard[key]) 
                else:
                    scoreboard[key] = newSCore[key]
            
                file.seek(0)
                for userId in scoreboard:
                    file.write(f'{userId}|{scoreboard[userId]}\n')
                file.truncate()
    except IOError as e:
        print('ERROR in get_scoreboard: ' + e)

client.run(TOKEN)
