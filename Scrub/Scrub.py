import re
import discord

from redbot.core import checks, Config, commands

PATTERN = re.compile(r"w+h*[aou]+t+[?!]*", re.IGNORECASE)


class Scrub(commands.Cog):

    """Repeat messages when other users are having trouble hearing"""

    default_global_settings = {"channels_ignored": [], "guilds_ignored": []}

    def __init__(self, bot):
        self.bot = bot
        self.conf = Config.get_conf(self, identifier=527690525)
        self.conf.register_global(**self.default_global_settings)

    async def red_delete_data_for_user(self, **kwargs):
        """Nothing to delete."""
        return

    @commands.guild_only()
    @commands.group(name="scrubignore")
    @checks.admin_or_permissions(manage_guild=True)
    async def scrubignore(self, ctx):
        """Change Scrub cog ignore settings."""
        pass

    @scrubignore.command(name="server")
    @checks.admin_or_permissions(manage_guild=True)
    async def _scrubignore_server(self, ctx):
        """Ignore/Unignore the current server"""

        guild = ctx.message.guild
        guilds = await self.conf.guilds_ignored()
        if guild.id in guilds:
            guilds.remove(guild.id)
            await ctx.send("wot? Ok boss, I will no longer ignore this server.")
        else:
            guilds.append(guild.id)
            await ctx.send("what? Fine, I will ignore this server.")
        await self.conf.guilds_ignored.set(guilds)

    @scrubignore.command(name="channel")
    @checks.admin_or_permissions(manage_guild=True)
    async def _scrubignore_channel(self, ctx):
        """Ignore/Unignore the current channel"""

        chan = ctx.message.channel
        chans = await self.conf.channels_ignored()
        if chan.id in chans:
            chans.remove(chan.id)
            await ctx.send("wut? Ok, I will no longer ignore this channel.")
        else:
            chans.append(chan.id)
            await ctx.send("Really? Alright, I will ignore this channel.")
        await self.conf.channels_ignored.set(chans)

    @commands.Cog.listener()
    async def on_message_without_command(self, message):
        if message.guild is None:
            return
        if message.author.bot:
            return
        content = message.content.lower().split()
        if len(content) != 1:
            return
        if message.guild.id in await self.conf.guilds_ignored():
            return
        if message.channel.id in await self.conf.channels_ignored():
            return

        if PATTERN.fullmatch(content[0]):
            async for before in message.channel.history(limit=5, before=message):
                author = before.author
                if (
                    not author.bot
                ):
                    msg = f" **No U** "
                    await message.channel.send(msg, allowed_mentions=discord.AllowedMentions(users=False))
                    break
