from modules import settings

import discord
import os
import requests
from discord.ext import commands
from datetime import datetime

bot = commands.Bot(command_prefix=settings.prefix(),
                   case_insensitive=True, help_command=None)


def load_modules():
    for file in os.listdir("modules"):
        if file.endswith(".py"):
            try:
                temp_file = open(f"modules/{file}", encoding='utf-8').read()
                exec(temp_file)
            except Exception as e:
                print(e)


load_modules()


@bot.event
async def on_command(ctx):
    await ctx.message.delete()
    return print("Command used: {}".format(str(ctx.command)))


@bot.event
async def on_connect():
    print("Connected: {}".format(str(bot.user)))


@bot.event
async def on_command_error(ctx, error):
    print("Error: " + str(error))
    return await ctx.send("Error: {}".format(str(error)))


@bot.command(usage="help", description="This message", help="This message")
async def help(ctx):
    list(bot.commands).reverse()
    message = ""
    for cmd in bot.commands:
        message += f"**{bot.command_prefix}{cmd.usage}** | {cmd.description}\n"
    return await ctx.send(embed=discord.Embed(description=message, color=settings.hex_color()).set_footer(icon_url=settings.footer_icon_url(), text=settings.footer()).set_thumbnail(url=settings.thumbnail_image()).set_author(name="Help"))

bot.run(settings.discord_token())
