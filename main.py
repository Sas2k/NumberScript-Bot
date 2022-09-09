from discord.ext import commands
from dotenv import load_dotenv
from NumberScript.interpreter import Interpreter

import discord
import os
import io
import sys

class custom_stdout:
    def __init__(self):
        self.real_stdout = sys.stdout
        self.new_stdout = io.StringIO()

    def write(self, s):
        self.real_stdout.write(s)
        self.new_stdout.write(s)

    def getvalue(self):
        return self.new_stdout.getvalue()

load_dotenv(".env")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

@bot.command(name="ping")
async def ping(ctx):
    await ctx.send("Pong!")

@bot.command(name="eval")
async def eval(ctx, *, program):
    new_stdout = custom_stdout()
    sys.stdout = new_stdout
    Interpreter.interpret(Interpreter, code=program)
    await ctx.send(new_stdout.getvalue())

bot.run(os.environ["token"])