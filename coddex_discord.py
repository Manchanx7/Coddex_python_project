# bot.py - All-in-one Discord Meme Bot (single file)
# -------------------------------------------------
# 1. Install required packages (run once):
#    pip install discord.py aiohttp
# 2. Replace 'YOUR_TOKEN_HERE' with your bot token.
# 3. Run: python bot.py
# -------------------------------------------------

import discord
import aiohttp
import asyncio

# === CONFIG ===
TOKEN = 'YOUR_TOKEN_HERE'  # <<<--- REPLACE THIS WITH YOUR BOT TOKEN
COMMAND_PREFIX = '$'
# ==============

intents = discord.Intents.default()
intents.message_content = True  # Required to read message content

bot = discord.Client(intents=intents)

async def get_meme():
    """Fetch a random meme URL from meme-api.com"""
    url = 'https://meme-api.com/gimme'
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data.get('url')
    except Exception as e:
        print(f"Meme API error: {e}")
    return None

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    print('Meme bot is ready! Type $meme in any channel.')

@bot.event
async def on_message(message):
    # Ignore bot's own messages
    if message.author == bot.user:
        return

    # Respond to $meme
    if message.content.strip().lower() == f'{COMMAND_PREFIX}meme':
        meme_url = await get_meme()
        if meme_url:
            embed = discord.Embed()
            embed.set_image(url=meme_url)
            await message.channel.send(embed=embed)
        else:
            await message.channel.send("Sorry, couldn't fetch a meme right now.")

    # Allow other commands/bots to work
    await bot.process_commands(message)

# === START THE BOT ===
bot.run(TOKEN)