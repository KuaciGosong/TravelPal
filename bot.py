import discord
from discord.ext import commands
import pandas as pd
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Load Discord token from environment variable
TOKEN = os.getenv('DISCORD_TOKEN')

# Load data from CSV files
destinasi_wisata_df = pd.read_csv('destinasi-wisata-indonesia-gambar.csv')

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot {bot.user} telah online')

@bot.command()
async def hello(ctx):
    await ctx.send('Hello! Aku TravelPal\nAku akan membantu kamu dalam mencari rekomendasi tempat wisata yang akan kamu kunjungi\n')
    await ctx.send('https://media1.tenor.com/m/wPudCfjCrD8AAAAC/penguin-hello.gif')
    await ctx.send(f'Berikut adalah daftar kota yang terdaftar di sistem kami: \n \n{'\n'.join([f"- {kota}" for kota in destinasi_wisata_df["City"].unique()])}')
    await ctx.send('Ketikkan nama kota tempat tujuan wisata kamu. Contoh "kota Jakarta"')

@bot.command()
async def kota(ctx, city_name: str):
    # Search for places based on city name
    city_places = destinasi_wisata_df[destinasi_wisata_df['City'].str.lower() == city_name.lower()]

    if len(city_places) == 0:
        await ctx.send(f"Maaf, destinasi tempat wisata di kota {city_name} masih belum terdaftar dalam sistem kami :(\n\nCoba cari destinasi tempat wisata lainnya.")
    else:
        # Send recommendations to user
        i = 0
        response = ""
        for index, place in city_places.iterrows():
            if i == 10:
                break
            response += f"- {place['Place_Name']}\n"
            i += 1
        await ctx.send(f"Berikut adalah rekomendasi tempat wisata di {city_name}:\n{response}")
        await ctx.send('Ketikkan nama tempat wisata yang ingin kamu ketahui detailnya. Contoh "detail Monumen Nasional"')

@bot.command()
async def detail(ctx, *, place_name: str):
    # Search for place based on place name
    place_info = destinasi_wisata_df[destinasi_wisata_df['Place_Name'].str.lower() == place_name.lower()]

    if len(place_info) == 0:
        await ctx.send(f"Maaf, destinasi tempat wisata dengan nama {place_name} tidak ditemukan dalam sistem kami :(")
    else:
        # Send place information to user
        place = place_info.iloc[0]
        image_info = destinasi_wisata_df[destinasi_wisata_df['Place_Name'].str.lower() == place_name.lower()]
        image_link = image_info.iloc[0]['Gambar']
        embed = discord.Embed(title=place['Place_Name'], description=place['Description'], color=discord.Color.blue())
        embed.add_field(name="Kategori", value=place['Category'], inline=True)
        embed.add_field(name="Harga Tiket Masuk", value=place['Price'], inline=True)
        embed.set_image(url=image_link)
        await ctx.send(embed=embed)

# Run the bot
bot.run(TOKEN)
