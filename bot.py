from dotenv import load_dotenv
import os
import discord
from discord.ext import commands
import yt_dlp

# تحميل المتغيرات من ملف .env
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'✅ Logged in as {bot.user}')

@bot.command()
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
        await ctx.send(f"🎶 Joined {channel}")
    else:
        await ctx.send("❌ لازم تكون في روم صوتي")

@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("📤 Left the voice channel")
    else:
        await ctx.send("❌ البوت مو في أي روم صوتي")

@bot.command()
async def play(ctx, *, url):
    if not ctx.voice_client:
        await ctx.invoke(bot.get_command('join'))

    ydl_opts = {
        'format': 'bestaudio',
        'quiet': True,
        'noplaylist': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        audio_url = info['url']

        # مسار ffmpeg الصحيح
        ffmpeg_path = "C:\\Users\\LENOVO\\Desktop\\ffmpeg-7.1.1-essentials_build\\bin\\ffmpeg.exe"

        source = discord.FFmpegPCMAudio(audio_url, executable=ffmpeg_path)
        ctx.voice_client.stop()
        ctx.voice_client.play(source, after=lambda e: print('✅ Done'))

    await ctx.send(f"🎵 Now playing: {info['title']}")

@bot.command()
async def stop(ctx):
    if ctx.voice_client:
        ctx.voice_client.stop()
        await ctx.send("⏹️ Stopped playing")

# تشغيل البوت باستخدام التوكن من ملف .env
bot.run(os.getenv("DISCORD_TOKEN"))
