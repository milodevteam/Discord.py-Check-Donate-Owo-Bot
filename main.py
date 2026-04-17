import discord
from discord.ext import commands
from colorama import Fore, Style
import re
import os
from dotenv import load_dotenv

load_dotenv()

RECEIVER_LIST = os.getenv("RECEIVER_LIST")
DONATE_CHANNEL = int(os.getenv("DONATE_CHANNEL"))
PREFIX = str(os.getenv("PREFIX"))
TOKEN = str(os.getenv("TOKEN"))

intents = discord.Intents.all()
intents.message_content = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents)

@bot.event
async def on_ready():
    print(f"{Fore.GREEN}[STATUS]{Style.RESET_ALL} Bot đã sẵn sàng!")

async def handle_donate(message):
    content = message.content

    # Lọc người chuyển, số cowoncy và người nhận

    pattern = r"<@!?(\d+)>.*?sent.*?([\d,]+).*?cowoncy.*?to.*?<@!?(\d+)>"
    match = re.search(pattern, content, re.IGNORECASE)

    if not match:
        return

    giver_id = int(match.group(1))
    amount = int(match.group(2).replace(",", ""))
    receiver_id = int(match.group(3))

    # Nếu người nhận thuộc danh sách người nhận

    if receiver_id in RECEIVER_LIST:
        try:
            # React ✅
            await message.add_reaction("✅")
        except Exception as e:
            print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Lỗi react (Handle Donate): {e}")

        # Print thông tin donate
        print(f"{Fore.WHITE}[INFO]{Style.RESET_ALL} {giver_id} đã donate {amount:,} cowoncy")

    # Nếu người nhận không thuộc danh sách người nhận
    
    else:
        try:
            # React ❌
            await message.add_reaction("❌")
        except Exception as e:
            print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Lỗi react (Handle Donate): {e}")

@bot.event
async def on_message_edit(before, after):
    # Nếu không phải là kênh donate thì bỏ qua

    if after.channel.id != DONATE_CHANNEL:
        return
    
    # Nếu người thực hiện (chỉnh sửa tin) không phải bot owo thì bỏ qua
    
    if after.author.id != 408785106942164992: # ID bot owo, không cần chỉnh
        return

    before_content = before.content.lower()
    after_content = after.content.lower()

    if ("sent" in after_content and "cowoncy" in after_content) and not ("sent" in before_content and "cowoncy" in before_content):
        await handle_donate(after)

    await bot.process_commands(after)

bot.run(TOKEN)