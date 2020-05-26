import discord
import logging
from asyncio import Lock, Event

from bot_blackjack import BlackjackBot
from typer import MessageTyper
from inventory import InventoryTracker
from bot_gamble import GambleBot


class TheBot(discord.Client):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.log = logging.getLogger("bot")
        self.bots = []
        self.owner_id = config["owner_id"]
        self.notify_id = config["notify_id"]
        self.exclusive_lock = Lock()
        self.typer = MessageTyper(config["type_url"])
        self.inventory = InventoryTracker()
        self.notify_channel = None
        self.notify_channel_event = Event()
        self.typer.start()
        self.started_bots = False

    def add_bot(self, bot):
        self.bots.append(bot)

    def stop(self):
        self.typer.stop()
        pass

    def get_prefixed_cmd(self, cmd):
        return self.config["bot_prefix"] + " " + cmd

    async def send_notify(self, msg):
        self.log.info(f"Sending notification: {msg}")
        await self.notify_channel_event.wait()
        await self.notify_channel.send(f"<@!{self.notify_id}> {msg}")

    async def on_ready(self):
        self.log.info(f"Logged on as {self.user}")

        self.notify_channel = self.get_channel(self.config["notify_channel_id"])
        self.notify_channel_event.set()

        if not self.started_bots:
            self.started_bots = True
            for b in self.bots:
                b.queue_run(0)

    async def on_message(self, message):
        if message.channel.id == self.config["type_channel_id"]:
            self.log.info(f"Message from {message.author}: {message.content}")
            for e in message.embeds:
                self.log.info(f"Embed {e.title}: {e.description}")
        if message.author.id == self.owner_id:
            for b in self.bots:
                await b.on_self_message(message)
        if message.author.id == self.config["bot_id"]:
            for b in self.bots:
                await b.on_bot_message(message)

        if message.content.startswith("say "):
            await message.channel.send(message.content[4:])

        if message.content.startswith("plz "):
            args = message.content[4:].split(" ")
            if args[0] == "inv":
                e = discord.Embed(title='Grinded stuff')
                e.add_field(name="Coins", value=str(self.inventory.total_coins))
                inv = "; ".join(f"{k}: {v}" for k, v in self.inventory.items.items())
                if inv != "":
                    e.add_field(name="Inventory", value=inv)
                await message.channel.send("", embed=e)
            if args[0] == "stat" or args[0] == "stats":
                e = discord.Embed(title='The Stats')
                e.add_field(name="Coins", value="; ".join(f"{k}: {v}" for k, v in self.inventory.coins_stats.items()))
                await message.channel.send("", embed=e)
            if args[0] == "gamble":
                gamble_bot = next((b for b in self.bots if isinstance(b, GambleBot)), None)
                if gamble_bot is None:
                    return
                e = discord.Embed(title='Gamble Stats')
                e.add_field(name="Won", value=f"{gamble_bot.won} games, {gamble_bot.won_money} coins")
                e.add_field(name="Lost", value=f"{gamble_bot.lost} games, {gamble_bot.lost_money} coins")
                e.add_field(name="Drew", value=f"{gamble_bot.draw} games, {gamble_bot.draw_lost_money} coins")
                await message.channel.send("", embed=e)
            if args[0] == "bj" or args[0] == "blackjack":
                blackjack_bot = next((b for b in self.bots if isinstance(b, BlackjackBot)), None)
                if blackjack_bot is None:
                    return
                e = discord.Embed(title='Blackjack Stats')
                e.add_field(name="Won", value=str(blackjack_bot.total_won))
                e.add_field(name="Lost", value=str(blackjack_bot.total_lost))
                e.add_field(name="Outcomes", value="; ".join(f"{k}: {v}" for k, v in blackjack_bot.outcomes.items()))
                await message.channel.send("", embed=e)

    async def on_message_edit(self, before, after):
        if after.channel.id == self.config["type_channel_id"]:
            self.log.info(f"Edited message from {after.author}: {after.content}")
            for e in after.embeds:
                self.log.info(f"Embed {e.title}: {e.description}")
        if after.author.id == self.config["bot_id"]:
            for b in self.bots:
                await b.on_bot_message_edit(after)

