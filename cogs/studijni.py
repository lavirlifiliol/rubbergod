import discord
from discord.ext import commands
from lxml import etree
import requests

from config.messages import Messages
from utils import add_author_footer

class Studijni(commands.Cog):

    @commands.command(aliases=["studijne", "študijné", "študijní"], brief=Messages.studijni_brief)
    async def studijni(self, ctx):
        link = "https://www.fit.vut.cz/fit/room/C109/.cs"
        htmlparser = etree.HTMLParser()
        session = requests.session()
        result = session.get(link)
        xDoc2 = etree.fromstring(result.text, htmlparser)
        hours_div = xDoc2.xpath("//*[b[contains(text(),'Úřední hodiny')]]//following-sibling::div")            
        embed = discord.Embed(title=Messages.studijni_title, url=link)
        if hours_div:
            hours = etree.tostring(hours_div[0], encoding=str, method="text")
            additional_info = xDoc2.xpath("//main//section/p")
            if additional_info:
                info = etree.tostring(additional_info[0], encoding=str, method="text").split(':', 1)
                if len(info) > 1: 
                    embed.add_field(name=info[0], value=info[1], inline=False)
        else:
            hours_div = xDoc2.xpath("//main//section")
            if len(hours_div):
                hours = ''.join(hours_div[0].itertext())
                hours = hours.strip()
            else:
                hours = Messages.studijni_web_error
        embed.add_field(name=Messages.studijni_office_hours, value=hours, inline=False)
        add_author_footer(embed, ctx.message.author)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Studijni(bot))