import discord
from discord.ext import commands, tasks
from config import DISCORD_TOKEN, ALERT_CHANNEL_ID, CHECK_EVERY_MINUTES
from checker import check_account

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

watch_list = {}
last_status = {}

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} - Abhiiyeee's Bot is LIVE!")
    check_loop.start()

@tasks.loop(minutes=CHECK_EVERY_MINUTES)
async def check_loop():
    channel = bot.get_channel(ALERT_CHANNEL_ID)
    if not channel:
        return
    for username in [u for u in watch_list.keys()]:
        status = check_account(username)
        print(f"{username} -> {status}")
        if username in last_status and last_status[username] != status:
            await channel.send(f"🚨 **UNBAN ALERT!**\nAccount: **@{username}**\nOld: {last_status[username]}\nNew: **{status}**\n\n@everyone Abhiiyeee, check it NOW!")
        last_status[username] = status

@bot.command()
async def add(ctx, username: str):
    username = username.replace("@", "")
    watch_list[username] = True
    status = check_account(username)
    last_status[username] = status
    await ctx.send(f"👀 Started monitoring **@{username}**\nCurrent Status: {status}")

@bot.command()
async def remove(ctx, username: str):
    username = username.replace("@", "")
    if username in watch_list:
        del watch_list[username]
        await ctx.send(f"Removed **@{username}** from watchlist.")
    else:
        await ctx.send(f"**@{username}** was not in watchlist.")

@bot.command()
async def status(ctx):
    if not watch_list:
        await ctx.send("Watchlist is empty. Use `!add username` to add one.")
        return
    msg = "**📊 UNBAN MONITOR STATUS**\n\n"
    for username in watch_list:
        s = check_account(username)
        msg += f"@{username} : {s}\n"
    await ctx.send(msg)

@bot.command(name="watchlist")
async def watchlist(ctx):
    if not watch_list:
        await ctx.send("No accounts being watched.")
    else:
        await ctx.send("Watching: " + ", ".join([f"@{u}" for u in watch_list]))

bot.run(DISCORD_TOKEN)