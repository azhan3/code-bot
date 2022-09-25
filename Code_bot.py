import discord
from discord_slash import SlashCommand
from discord.ext import commands
from PIL import ImageColor
from discord.utils import get
import pymongo
import pydoodle
import traceback
import re

c = pydoodle.Compiler(clientId="f76e0eedaf35d2125e425e536d65481f",
                      clientSecret="42a08cbae4ba2d5d18389602e35c117945fd7d52df562a11bdce88070fb15120")

valid_languages = {
    "brainfuck": "brainfuck",
    "java": "java",
    "c": "c",
    "c++": "cpp17",
    "c#": "csharp",
    "python": "python3",
}

color = 0x7D3C98

class bot(discord.Client):
    def __init__(self, **options):
        super().__init__(**options)
        self.lit = None
        self.cont = None
        self.ctx = None
        self.commands = {
            ".run": self.runcode,
            ".help": self.help
        }

    async def on_ready(self):
        print(self.user)

    async def on_message(self, message):
        if message.author == self.user: return
        self.lit = message.content
        self.cont = message.content.split()
        self.ctx = message
        print(self.cont[0])
        try:
            if self.cont[0].lower() in self.commands:
                await self.commands[self.cont[0]]()
        except:
            traceback.print_exc()

    async def runcode(self):
        if self.cont[1] not in valid_languages:
            await self.ctx.reply("not a valid language")
            return
        run = self.lit[self.lit.find("```") + 3:-3]
        if self.lit.find("```") == -1:
            await self.ctx.reply("Please enter valid code")
            return
        result = c.execute(script=run, language=valid_languages[self.cont[1]])
        usage = c.usage()
        print(result.memory)
        time = result.cpuTime if result.cpuTime is not None else 0
        space = result.memory[2:-3] if result.memory != "(None,)" else 0
        status = "Success" if result.cpuTime is not None else "Failure"
        image = "https://imgs.search.brave.com/m4P1brL9I7xBFICAbxS7ESRrlX5mNW3p0XPa6m3bND8/rs:fit:1200:1200:1/g:ce/aHR0cDovL2NsaXBh/cnQtbGlicmFyeS5j/b20vaW1hZ2VzX2sv/Y2hlY2stbWFyay10/cmFuc3BhcmVudC1i/YWNrZ3JvdW5kL2No/ZWNrLW1hcmstdHJh/bnNwYXJlbnQtYmFj/a2dyb3VuZC0zLnBu/Zw"  if result.cpuTime is not None else "https://imgs.search.brave.com/1BMN3qa4HuvRjWweUmSGBSlMp4rrJnAGFLtdwVVYcnI/rs:fit:1200:1200:1/g:ce/aHR0cHM6Ly93d3cu/amluZy5mbS9jbGlw/aW1nL2Z1bGwvMTEt/MTEwODM2X2NsaXAt/YXJ0LWZyZWUtZG93/bmxvYWQtdHJhbnNw/YXJlbnQtYmFja2dy/b3VuZC1yZWQteC5w/bmc"
        code_embed = discord.Embed(title=f"Code Output - {status}", color=color)
        code_embed.add_field(name="CPU Runtime", value=f"{time}s.", inline=True)
        code_embed.add_field(name="Memory Usage", value=f"{space} kb.", inline=True)
        code_embed.add_field(name="Code Output", value=f"```{result.output[0][0:1000].replace('jdoodle', 'code_bot')}```", inline=False)
        code_embed.set_thumbnail(url=image)
        await self.ctx.reply(embed=code_embed)

    async def help(self):
        help_embed = discord.Embed(title="Commands", color=color)
        help_embed.add_field(name=".help", value="Sends this embed", inline=False)
        list_of_langs = '\n'.join([f'\u2003 • {i}' for i in valid_languages])
        help_embed.add_field(name=".run ```<Programming_Language>``` ```<Code Here>```", value=f"Runs your code, make sure to put your code in plain code blocks ``` to run \nAvailable Programming Languages:\n{list_of_langs}", inline=False)
        await self.ctx.reply(embed=help_embed)

client = bot()
client.run("MTAyMTg4NTU5ODY5NDM4MzY3Ng.GDzecT.sO1kS8jau4DaJgUxB_Krd30ZV8UnhGaR3BzFX0")
