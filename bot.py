import os
import discord
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

client.run(TOKEN)
