import discord
from discord.ext import tasks
from datetime import datetime
import pytz
import os

# ===== CONFIG =====
DISCORD_BOT_TOKEN = os.environ["DISCORD_BOT_TOKEN"]
DISCORD_CHANNEL_ID = int(os.environ["DISCORD_CHANNEL_ID"])

intents = discord.Intents.default()
client = discord.Client(intents=intents)

tz = pytz.timezone("Asia/Ho_Chi_Minh")

# ===== CHECK MÙA =====
def is_summer(date):
    year = date.year
    start = tz.localize(datetime(year, 3, 8))
    end = tz.localize(datetime(year, 11, 1))
    return start <= date <= end

# ===== READY =====
@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    scheduler.start()

# ===== SCHEDULER =====
@tasks.loop(minutes=1)
async def scheduler():
    now = datetime.now(tz)
    weekday = now.weekday()  # 0=Mon ... 6=Sun
    time_str = now.strftime("%H:%M")

    channel = client.get_channel(DISCORD_CHANNEL_ID)
    if channel is None:
        return

    if is_summer(now):
        check_in_time = "18:35"
        check_out_time = "04:10"
    else:
        check_in_time = "19:35"
        check_out_time = "05:10"

    # ===== CHECK IN =====
    if weekday != 6 and time_str == check_in_time:
        embed = discord.Embed(
            description="✅ [Hey bro! check in!](https://intranet.cennext.com/basic/web/index.php?r=timekeep%2Findex)",
            color=0x00ff00
        )
        await channel.send(embed=embed)

    # ===== CHECK OUT =====
    if weekday != 0 and time_str == check_out_time:
        embed = discord.Embed(
            description="🔻 [End time, check out now!](https://intranet.cennext.com/basic/web/index.php?r=timekeep%2Findex)",
            color=0xff0000
        )
        await channel.send(embed=embed)

# ===== RUN =====
client.run(DISCORD_BOT_TOKEN)
