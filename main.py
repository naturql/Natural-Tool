import discord
import asyncio
import random
import string
from colorama import init, Fore

init(autoreset=True)
WHITE = Fore.WHITE
RED = Fore.RED

ascii_art = RED + """  
                                          $$\   $$\            $$\                                  $$\ 
                                          $$$\  $$ |           $$ |                                 $$ |
                                          $$$$\ $$ | $$$$$$\ $$$$$$\   $$\   $$\  $$$$$$\  $$$$$$\  $$ |
                                          $$ $$\$$ | \____$$\\_$$  _|  $$ |  $$ |$$  __$$\ \____$$\ $$ |
                                          $$ \$$$$ | $$$$$$$ | $$ |    $$ |  $$ |$$ |  \__|$$$$$$$ |$$ |
                                          $$ |\$$$ |$$  __$$ | $$ |$$\ $$ |  $$ |$$ |     $$  __$$ |$$ |
                                          $$ | \$$ |\$$$$$$$ | \$$$$  |\$$$$$$  |$$ |     \$$$$$$$ |$$ |
                                          \__|  \__| \_______|  \____/  \______/ \__|      \_______|\__|
"""
print(ascii_art)

TOKENS = [
    "Your_bot_token",
    "your_bot_token",
    "your_bot_token"
]

EMOJIS = ["🥹", "😂", "🤣", "😘", "😉", "🤨", "😤", "😜", "😭", "😊", "🥴", "😢", "🥰"]

def generate_fake_token():
    first_char = random.choice("0MN")
    return first_char + ''.join(random.choices(string.ascii_letters + string.digits, k=23))

def menu():
    print(RED + "[Channel ID] >> " + RED, end="")
    channel_id = int(input())

    print(RED + "[Message] >> " + RED, end="")
    spam_message = input()

    print(RED + "[Mass Ping] (y/n) >> " + RED, end="")
    do_mass_ping = input().lower().strip() == "y"

    print(RED + "[Emoji] (y/n) >> " + RED, end="")
    use_emoji = input().lower().strip() == "y"

    print(RED + "[VC Joiner] (y/n) >> " + RED, end="")
    vc_join = input().lower().strip() == "y"

    print()
    return channel_id, spam_message, use_emoji, do_mass_ping, vc_join

channel_id, spam_message, use_emoji, do_mass_ping, vc_join = menu()

class SpamBot(discord.Client):
    def __init__(self, token):
        intents = discord.Intents.all()
        super().__init__(intents=intents)
        self.token = token
        self.channel = None
        self.members = []
        self.vc_connection = None

    def obfuscate_token(self):
        return self.token[:24] + "******"

    async def on_ready(self):
        self.channel = self.get_channel(channel_id)
        if self.channel is None:
            return

        self.members = [m for m in self.channel.guild.members]

        if vc_join:
            await self.join_first_vc()

        self.loop.create_task(self.spam_loop())

    async def join_first_vc(self):
        for vc in self.channel.guild.voice_channels:
            try:
                self.vc_connection = await vc.connect(self_mute=True, self_deaf=True)
                break
            except:
                pass

    async def spam_loop(self):
        try:
            while True:
                message = spam_message
                fake_token = generate_fake_token()

                if do_mass_ping and self.members:
                    mentions = " ".join(member.mention for member in random.sample(self.members, min(3, len(self.members))))
                    message += f" -> {fake_token} -> {mentions}"

                    if use_emoji:
                        emojis = " ".join(random.sample(EMOJIS, 5))
                        message += f" -> {emojis}"

                elif use_emoji:
                    emojis = " ".join(random.sample(EMOJIS, 5))
                    message += f" -> {fake_token} -> {emojis}"

                else:
                    message += f" -> {fake_token}"

                try:
                    await self.channel.send(message)
                    print(RED + f"[SUCCESS] sent {spam_message}" + RED + " " + WHITE + f"[{self.obfuscate_token()}]")
                except:
                    pass

                await asyncio.sleep(0.4)
        finally:
            if self.vc_connection:
                try:
                    await self.vc_connection.disconnect(force=True)
                except:
                    pass

    async def start_bot(self):
        try:
            await self.start(self.token)
        except:
            pass
        finally:
            if self.vc_connection:
                try:
                    await self.vc_connection.disconnect(force=True)
                except:
                    pass

async def main():
    bots = [SpamBot(token) for token in TOKENS]
    await asyncio.gather(*(bot.start_bot() for bot in bots))

asyncio.run(main())
