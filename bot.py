from dotenv import load_dotenv
import os
import discord
from discord.ext import commands

# تحميل المتغيرات من ملف .env
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# أيديهات الملكين (تأكد من إضافة ID الملكين هنا)
KING_IDS = ["ID_الملك1", "ID_الملك2"]

@bot.event
async def on_ready():
    print(f'✅ Logged in as {bot.user}')

# التحقق مما إذا كان المستخدم هو الملك أو الملك الثاني
def is_king(ctx):
    return str(ctx.author.id) in KING_IDS

# أمر للانضمام إلى الروم الصوتي
@bot.command()
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
        await ctx.send(f"🎶 Joined {channel}")
    else:
        await ctx.send("❌ لازم تكون في روم صوتي")

# أمر لمغادرة الروم الصوتي
@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("📤 Left the voice channel")
    else:
        await ctx.send("❌ البوت مو في أي روم صوتي")

# أمر لتغيير اسم البوت (فقط للملكين)
@bot.command()
async def set_name(ctx, *, new_name):
    if is_king(ctx):
        await bot.user.edit(username=new_name)
        await ctx.send(f"🎤 تم تغيير اسم البوت إلى {new_name}")
    else:
        await ctx.send("❌ فقط الملكين يمكنهم تغيير اسم البوت!")

# أمر لتغيير صورة البوت (فقط للملكين)
@bot.command()
async def set_avatar(ctx, url: str):
    if is_king(ctx):
        try:
            # تحميل الصورة من الرابط وتحديث صورة البوت
            async with ctx.session.get(url) as response:
                avatar = await response.read()
                await bot.user.edit(avatar=avatar)
            await ctx.send("🎨 تم تغيير صورة البوت بنجاح!")
        except Exception as e:
            await ctx.send(f"❌ حدث خطأ أثناء تغيير الصورة: {e}")
    else:
        await ctx.send("❌ فقط الملكين يمكنهم تغيير صورة البوت!")

# أمر للبوت للبقاء في الروم الصوتي فقط دون تشغيل أغاني
@bot.command()
async def play(ctx, *, url=None):
    if not ctx.voice_client:
        await ctx.invoke(bot.get_command('join'))

    # البوت سيبقى فقط في الروم الصوتي دون تشغيل أغاني الآن
    await ctx.send("🎵 سأبقى في الروم الصوتي ولكن لن أشغل أغاني في الوقت الحالي.")

# أمر لإيقاف تشغيل الموسيقى
@bot.command()
async def stop(ctx):
    if ctx.voice_client:
        ctx.voice_client.stop()
        await ctx.send("⏹️ Stopped playing")
    else:
        await ctx.send("❌ البوت مشغول حاليًا في الروم الصوتي فقط.")

# تشغيل البوت باستخدام التوكن من ملف .env
bot.run(os.getenv("DISCORD_TOKEN"))
