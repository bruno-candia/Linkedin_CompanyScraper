# bot.py
import os
from scrape_linkedin_OO import scraping_linkedin


import dataframe_image as dfi # EDIT: see deprecation warnings below
from table2ascii import table2ascii as t2a, PresetStyle, Alignment


import discord
from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
LOGIN = os.getenv('LOGIN')
PASSWORD = os.getenv('PASSWORD')
PATH = os.getenv('CHROME_PROFILE_PATH')

client = discord.Client()


def linkedin_data():
    linkedinConnection = scraping_linkedin(username=LOGIN, password=PASSWORD, chrome_profile_path=PATH)
    try:
        linkedinConnection.login()
        linkedinConnection.get_company_posts_data()
        df = linkedinConnection.plot_statistics()
        linkedinConnection.driver.quit()
        return df
    except Exception as e:
        linkedinConnection.driver.quit()
        return f'{e}'
   

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == '!social_data':
        await message.channel.send('AGUARDE UM MOMENTO...')
        df = linkedin_data()
        
        df_columns = list(df.columns)
        body = []
        for data in df.values:
            body.append(data)
        # In your command:
        output = t2a(
            header=df_columns,
            body=body,
            style=PresetStyle.thin_compact,
        )
        await message.channel.send(f"```\n{output}\n```")
        

client.run(TOKEN)