import discord
from discord import app_commands
from discord.ext import commands
import os
import asyncio

class DeepHatBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.members = True
        intents.message_content = True
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        print("Sincronizando comandos...")
        await self.tree.sync()

class ProfileBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="perfil", description="Busca informações de perfil por ID")
    async def perfil(self, interaction: discord.Interaction, user_id: str):
        await interaction.response.defer()
        try:
            uid = int(user_id)
            user = await self.bot.fetch_user(uid)
            
            embed = discord.Embed(
                title=f"🔍 Perfil de {user.name}",
                description=f"**ID:** `{user.id}`",
                color=discord.Color.random()
            )

            # Avatar (Suporta GIF)
            embed.set_thumbnail(default=user.display_avatar.url)

            # Banner
            banner_url = user.banner if hasattr(user, 'banner') and user.banner else None
            if banner_url:
                embed.set_image(url=banner_url)
            else:
                embed.set_image(url=user.display_avatar.url)

            # Cor baseada no ID
            embed.color = discord.Color.from_str(f"#{uid % 0xFFFFFF:06x}")
            embed.add_field(name="Status", value="✅ Online via GitHub Actions", inline=True)
            embed.set_footer(text="DeepHat Engine")

            await interaction.followup.send(embed=embed)
        except Exception as e:
            await interaction.followup.send(f"❌ Erro: `{str(e)}`")

async def main():
    bot = DeepHatBot()
    await bot.add_cog(ProfileBot(bot))
    TOKEN = os.environ.get('DISCORD_TOKEN')
    if not TOKEN:
        print("ERRO: DISCORD_TOKEN não configurado nos Secrets!")
        return
    await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
