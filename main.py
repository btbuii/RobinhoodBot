import discord
import requests
import bs4
import csv
import os
from datetime import datetime
from discord import app_commands

"""| INITIALIZATION |"""
MY_GUILD = discord.Object(id = ID)

class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents = intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        self.tree.copy_global_to(guild = MY_GUILD)
        await self.tree.sync(guild = MY_GUILD)
    
intents = discord.Intents.all()
client = MyClient(intents = intents)

"""| ON READY |"""
@client.event
async def on_ready():
    await client.change_presence(status = discord.Status.online, activity = discord.Game("Analyzing market..."))
    print("----------")
    print(f"Logged in as {client.user} (ID: {client.user.id})...")
    print("----------")
    print("Bot initialized!")

"""| COMMAND: help |"""
@client.tree.command(name = "help", description = "Shows all commands for the Robinhood Bot!")
async def help(interaction: discord.Interaction):
    embed = discord.Embed(
        title = "Robinhood Bot Commands",
        description = "Here's a list of the available commands for the Robinhood Bot.",
        colour = discord.Colour.green()
    )
    embed.add_field(name = "!rhhelp", value = "Displays all commands for the Robinhood Bot.", inline = False)
    embed.add_field(name = "!price [stock]", value = "Gives the current price of a stock.", inline = False)
    embed.add_field(name = "!doge", value = "Gives the current price of Dogecoin.", inline = False)
    await interaction.response.send_message(embed = embed)

"""| COMMAND: price |"""
@client.tree.command(name = "price", description = "Shows the current price of a stock!")
async def price(interaction: discord.Interaction, stock: str):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'}
    url = "https://finance.yahoo.com/quote/" + stock
    stock = "$" + stock.upper()
    response = requests.get(url, headers = headers)
    soup = bs4.BeautifulSoup(response.text, "html.parser")

    stock_time = soup.find("div", {"class": "D(ib) Mend(20px)"}).find_all("span")[2].text
    stock_info = soup.find("div", {"class": "D(ib) Mend(20px)"}).find_all("fin-streamer")
    stock_price = stock_info[0].text
    dollar_change = stock_info[1].text
    percent_change = stock_info[2].text
    current_time = datetime.now().strftime("%m/%d/%Y %H:%M:%S")

    """| FORMAT & SEND EMBED |"""
    embed = discord.Embed(
        title = f"Finance data report for {stock}",
        description = f"*Data obtained from Yahoo Finance as of {current_time}.*",
        colour = discord.Colour.green()
    )

    embed.set_author(name = f"{stock}", icon_url = client.user.avatar)
    embed.add_field(name = "Price", value = f"${stock_price}", inline = True)
    embed.add_field(name = "Dollar change:", value = f"{dollar_change}", inline = True)
    embed.add_field(name = "Percent change:", value = f"{percent_change.strip('(').strip(')')}", inline = True)
    embed.add_field(name = "Time pulled", value = f"{stock_time}", inline = True)
    embed.set_footer(text = url)
    await interaction.response.send_message(embed = embed)

    """| FORMAT & SEND CSV |"""
    file_name = "stock.csv"
    file_path = "C:\\Users\\ipwnc\\Desktop\\Portfolio Projects"
    path = os.path.join(file_path, file_name)

    with open(path, "w", encoding = "utf-8") as f:
        file_writer = csv.writer(f)
        file_writer.writerow(["Stock", "Price", "Dollar change", "Percent change", "Time pulled"])
        file_writer.writerow([stock, stock_price, dollar_change, percent_change, stock_time])

    with open(path, "rb") as f:
        await interaction.followup.send(content = "Here's the data report in a CSV file!", file = discord.File(f, filename = "stock.csv"))

"""| COMMAND: doge |"""
@client.tree.command(name = "doge", description = "Shows the current price of $DOGECOIN!")
async def doge(interaction: discord.Interaction):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'}
    url = "https://finance.yahoo.com/quote/DOGE-USD"
    response = requests.get(url, headers = headers)
    soup = bs4.BeautifulSoup(response.text, "html.parser")

    stock_time = soup.find("div", {"class": "D(ib) Mend(20px)"}).find_all("span")[2].text
    stock_info = soup.find("div", {"class": "D(ib) Mend(20px)"}).find_all("fin-streamer")
    stock_price = stock_info[0].text
    dollar_change = stock_info[1].text
    percent_change = stock_info[2].text
    current_time = datetime.now().strftime("%m/%d/%Y %H:%M:%S")

    """| FORMAT & SEND EMBED |"""
    embed = discord.Embed(
        title = f"Finance data report for $DOGECOIN",
        description = f"*Data obtained from Yahoo Finance as of {current_time}.*",
        colour = discord.Colour.yellow()       
    )

    embed.set_author(name = f"$DOGECOIN", icon_url = client.user.avatar)
    embed.add_field(name = "Price", value = f"${stock_price}", inline = True)
    embed.add_field(name = "Dollar change:", value = f"{dollar_change}", inline = True)
    embed.add_field(name = "Percent change:", value = f"{percent_change.strip('(').strip(')')}", inline = True)
    embed.add_field(name = "Time pulled", value = f"{stock_time}", inline = True)
    embed.set_footer(text = url)
    await interaction.response.send_message(embed = embed)

    """| FORMAT & SEND CSV |"""
    file_name = "doge.csv"
    file_path = "C:\\Users\\ipwnc\\Desktop\\Portfolio Projects"
    path = os.path.join(file_path, file_name)

    with open(path, "w", encoding = "utf-8") as f:
        file_writer = csv.writer(f)
        file_writer.writerow(["Stock", "Price", "Dollar change", "Percent change", "Time pulled"])
        file_writer.writerow(["doge", stock_price, dollar_change, percent_change, stock_time])

    with open(path, "rb") as f:
        await interaction.followup.send(content = "Here's the data report in a CSV file!", file = discord.File(f, filename = "doge.csv"))

client.run("TOKEN")
