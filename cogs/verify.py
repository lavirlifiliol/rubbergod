from disnake.ext import commands
from config import cooldowns
from features import verification
from config.messages import Messages
import disnake
from config.app_config import config


class Verify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.verification = verification.Verification(bot)

    def is_valid_guild(ctx: disnake.ApplicationCommandInteraction) -> bool:
        return ctx.guild_id is None or ctx.guild_id == config.guild_id

    @cooldowns.default_cooldown
    @commands.command(brief=Messages.verify_brief)
    async def verify(self, ctx):
        await self.verification.verify(ctx.message)

    @cooldowns.default_cooldown
    @commands.check(is_valid_guild)
    @commands.slash_command(
        name="getcode", description=Messages.get_code_brief, dm_permission=True
    )
    async def get_code(
        self,
        inter: disnake.ApplicationCommandInteraction,
        login: str = commands.Param(description=Messages.get_code_login_parameter),
    ):
        await self.verification.send_code(login, inter)

    @get_code.error
    async def on_verification_error(
        self, inter: disnake.ApplicationCommandInteraction, error
    ):
        if isinstance(error, commands.CheckFailure):
            await inter.send(Messages.verify_invalid_channel, ephemeral=True)
            return True


def setup(bot):
    bot.add_cog(Verify(bot))
