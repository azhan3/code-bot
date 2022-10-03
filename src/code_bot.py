import discord
import pydoodle
import traceback
import json
from discord.utils import get

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

name_list = ["brainfuck", "java", "c_", "cpp", "csharp", "python"]
languages = ["Brainfuck", "Java", "C", "C++", "C#", "Python"]

res = dict(zip(name_list, languages))
messageID = 1025606561726464082


def check_blacklist(person):
    with open("resource.json", "r") as f:
        data = json.load(f)
        blacklist = data["Blacklist"]
        for i, j in enumerate(blacklist):
            if person == j["id"]:
                return True, i
        return False, -1


class bot(discord.Client):
    def __init__(self, **options):
        super().__init__(**options)
        self.lit = None
        self.cont = None
        self.ctx = None
        self.commands = {
            ".run": self.runcode,
            ".help": self.help,
            ".add": self.add_blacklist,
            ".remove": self.remove_blacklist
        }

    async def on_ready(self):

        print(self.user)

    async def delete_role(self, role_name, message):
        role_object = discord.utils.get(message.guild.roles, name=role_name)
        await role_object.delete()

    async def on_raw_reaction_add(self, payload):
        guild = await client.fetch_guild(payload.guild_id)
        user = await guild.fetch_member(payload.user_id)
        if user != client.user:
            if payload.message_id == messageID:
                try:
                    name = (str(payload.emoji).split(":")[1])
                    print(name)
                    role = get(guild.roles, name=res[name])
                    await user.add_roles(role)
                except (KeyError, IndexError) as e:
                    pass

    async def on_raw_reaction_remove(self, payload):
        if payload.message_id == messageID:
            try:
                name = (str(payload.emoji).split(":")[1])
                print(name)
                guild = await client.fetch_guild(payload.guild_id)
                role = get(guild.roles, name=res[name])
                user = await guild.fetch_member(payload.user_id)
                await user.remove_roles(role)
            except (KeyError, IndexError) as e:
                pass

    async def test(self, message):
        emojis = [discord.utils.get(message.guild.emojis, name=i) for i in name_list]
        me = await message.channel.send(f'''
        **Select the languages that you're learning/have learned:**

Brainfuck: {emojis[0]}

Java: {emojis[1]}

C: {emojis[2]}

C++: {emojis[3]}

C#: {emojis[4]}

Pyth:nauseated_face:n: {emojis[5]}

        ''')
        for i in name_list:
            emoji = discord.utils.get(message.guild.emojis, name=i)
            await me.add_reaction(emoji)

    async def on_message(self, message):
        if message.author == self.user: return
        self.lit = message.content
        self.cont = message.content.split()
        self.ctx = message
        if self.lit == "roles" and message.author.id == 420417488283500576 and message.channel.id == 1017956650948235305:
            await self.test(message)
        try:
            if self.cont[0].lower() in self.commands:
                await self.commands[self.cont[0]]()
        except:
            traceback.print_exc()

    async def add_blacklist(self):
        with open("resource.json", "r+") as f:
            data = json.load(f)
            if self.ctx.author.id not in data["Authorized"]:
                await self.ctx.reply("bad")
                return
            blacklist = data["Blacklist"]
            if check_blacklist(int(self.cont[1][2:-1]))[0]:
                await self.ctx.reply("Already on blacklist")
                return
            blacklist.append({"id": int(self.cont[1][2:-1])})
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()
            await self.ctx.reply(f"Successfully added {self.cont[1][2:-1]} to blacklist")

    async def remove_blacklist(self):
        with open("resource.json", "r+") as f:
            data = json.load(f)
            if self.ctx.author.id not in data["Authorized"]:
                await self.ctx.reply("bad")
                return
            blacklist = data["Blacklist"]
            check = check_blacklist(int(self.cont[1][2:-1]))
            if not check[0]:
                await self.ctx.reply("Not on blacklist")
                return
            blacklist.pop(check[1])
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()
            await self.ctx.reply(f"Successfully removed {self.cont[1][2:-1]} from blacklist")

    async def runcode(self):

        if check_blacklist(self.ctx.author.id)[0]:
            await self.ctx.reply("Lol you are blacklisted")
            return
        if self.cont[1] not in valid_languages:
            await self.ctx.reply("not a valid language")
            return
        print(self.lit.find("```\n"))

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
        image = "https://imgs.search.brave.com/m4P1brL9I7xBFICAbxS7ESRrlX5mNW3p0XPa6m3bND8/rs:fit:1200:1200:1/g:ce/aHR0cDovL2NsaXBh/cnQtbGlicmFyeS5j/b20vaW1hZ2VzX2sv/Y2hlY2stbWFyay10/cmFuc3BhcmVudC1i/YWNrZ3JvdW5kL2No/ZWNrLW1hcmstdHJh/bnNwYXJlbnQtYmFj/a2dyb3VuZC0zLnBu/Zw" if result.cpuTime is not None else "https://imgs.search.brave.com/1BMN3qa4HuvRjWweUmSGBSlMp4rrJnAGFLtdwVVYcnI/rs:fit:1200:1200:1/g:ce/aHR0cHM6Ly93d3cu/amluZy5mbS9jbGlw/aW1nL2Z1bGwvMTEt/MTEwODM2X2NsaXAt/YXJ0LWZyZWUtZG93/bmxvYWQtdHJhbnNw/YXJlbnQtYmFja2dy/b3VuZC1yZWQteC5w/bmc"
        code_embed = discord.Embed(title=f"Code Output - {status}", color=color)
        code_embed.add_field(name="CPU Runtime", value=f"{time}s.", inline=True)
        code_embed.add_field(name="Memory Usage", value=f"{space} kb.", inline=True)
        code_embed.add_field(name="Code Output",
                             value=f"```{result.output[0][0:1000].replace('jdoodle', 'code_bot')}```", inline=False)
        code_embed.set_thumbnail(url=image)
        await self.ctx.reply(embed=code_embed)

    async def help(self):
        emolist = [[discord.utils.get(i.emojis, name=name) for i in self.guilds if
                    discord.utils.get(i.emojis, name=name) is not None] for name in name_list]
        help_embed = discord.Embed(title="Commands", color=color)
        help_embed.add_field(name=".help", value="Sends this embed", inline=False)
        list_of_langs = '\n'.join(
            [f'\u2003 • {list(valid_languages)[i]} {emolist[i][0]}' for i in range(len(valid_languages))])
        help_embed.add_field(name=".run ```<Programming_Language>``` ```<Code Here>```",
                             value=f"Runs your code, make sure to put your code in plain code blocks ``` to run \nAvailable Programming Languages:\n{list_of_langs}",
                             inline=False)
        await self.ctx.reply(embed=help_embed)


client = bot()
client.run("MTAyMTg4NTU5ODY5NDM4MzY3Ng.GDzecT.sO1kS8jau4DaJgUxB_Krd30ZV8UnhGaR3BzFX0")
