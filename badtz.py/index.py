import discord
from discord.ext import commands
import random
import asyncio
import os
import json
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
PREFIX = os.getenv('BOT_PREFIX', '!')

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=PREFIX, intents=intents, help_command=None)

DATA_FILE = 'casino_data.json'
currency_data = {}
TRIVIA_COOLDOWN = {}

#  - UNLIMITED GENERATION
TRIVIA_DB = {
    "history": [
        ("national hero", "Jose Rizal", ["Andres Bonifacio", "Emilio Aguinaldo", "Lapu-Lapu"]),
        ("independence from Spain", "1898", ["1896", "1946", "1521"]),
        ("first president", "Emilio Aguinaldo", ["Manuel Quezon", "Jose Laurel", "Sergio Osmena"]),
        ("EDSA Revolution", "1986", ["1972", "1983", "1989"]),
        ("Magellan arrived", "1521", ["1492", "1600", "1700"]),
        ("Philippine flag first waved", "1898", ["1896", "1946", "1521"]),
        ("Blood Compact", "1565", ["1521", "1898", "1945"]),
        ("First Republic", "1899", ["1946", "1935", "1986"]),
        ("Martial Law declared", "1972", ["1986", "1965", "1983"]),
        ("People Power Revolution", "1986", ["1972", "1983", "1989"]),
        ("Lapulapu killed Magellan", "1521", ["1565", "1898", "1945"]),
        ("Pact of Biak-na-Bato", "1897", ["1898", "1946", "1521"])
    ],
    "geography": [
        ("capital city", "Manila", ["Cebu", "Davao", "Quezon City"]),
        ("largest island", "Mindanao", ["Luzon", "Palawan", "Negros"]),
        ("highest mountain", "Mt. Apo", ["Mt. Mayon", "Mt. Pinatubo", "Taal"]),
        ("most populated city", "Quezon City", ["Manila", "Davao", "Caloocan"]),
        ("number of islands", "7,641", ["7,000", "8,000", "over 10k"]),
        ("longest river", "Cagayan River", ["Agusan", "Pampanga", "Pasig"]),
        ("deepest lake", "Lake Mainit", ["Taal Lake", "Lanao", "Danao"]),
        ("Chocolate Hills location", "Bohol", ["Cebu", "Leyte", "Samar"]),
        ("Mayon Volcano province", "Albay", ["Camarines Sur", "Sorsogon", "Catanduanes"]),
        ("Taal Volcano location", "Batangas", ["Cavite", "Laguna", "Quezon"]),
        ("Rice terraces location", "Ifugao", ["Benguet", "Mt. Province", "Kalinga"]),
        ("Underground river", "Palawan", ["Mindoro", "Romblon", "Antique"])
    ],
    "food": [
        ("national dish", "Adobo", ["Lechon", "Sinigang", "Kare-Kare"]),
        ("national fruit", "Mango", ["Calamansi", "Durian", "Pineapple"]),
        ("famous dessert", "Halo-Halo", ["Leche Flan", "Bibingka", "Maja Blanca"]),
        ("BBQ street food", "Chicken Inasal", ["Pork BBQ", "Isaw", "Betamax"]),
        ("sour soup", "Sinigang", ["Tinola", "Nilaga", "Bulalo"]),
        ("Iloilo specialty", "Chicken Inasal", ["Batchoy", "KBL", "Pancit Molo"]),
        ("Pampanga dish", "Sisig", ["Kare-Kare", "Bringhe", "Tortang Talong"]),
        ("lechon city", "Cebu", ["Manila", "Pampanga", "Iloilo"]),
        ("Balut origin", "Pateros", ["Candaba", "Pulilan", "Llanera"]),
        ("Longganisa capital", "Lucban", ["Vigan", "Guagua", "Cabanatuan"]),
        ("Batchoy origin", "Iloilo", ["La Paz", "Aklan", "Capiz"]),
        ("Kare-Kare meat", "Oxtail", ["Pork", "Beef", "Chicken"]),
        ("fav food ni dyuki", "laing", ["Adobro", "Sinigang", "Paksiw"])
    ],
    "culture": [
        ("national language", "Filipino", ["Tagalog", "Cebuano", "Ilocano"]),
        ("national flower", "Sampaguita", ["Gumamela", "Jasmine", "Rose"]),
        ("national bird", "Philippine Eagle", ["Mayna", "Kingfisher", "Swift"]),
        ("biggest festival", "Sinulog", ["Ati-Atihan", "Pahiyas", "Dinagyang"]),
        ("traditional dance", "Tinikling", ["Pandanggo", "Cariñosa", "Itik-Itik"]),
        ("Ati-Atihan location", "Kalibo", ["Caticlan", "Ibajay", "Nabas"]),
        ("Pahiyas festival", "Lucban", ["Tayabas", "Majayjay", "Pila"]),
        ("Parol origin", "Pampanga", ["Bataan", "Bulacan", "Tarlac"]),
        ("Santacruzan", "May", ["June", "April", "July"]),
        ("Barong Tagalog", "Formal wear", ["Casual", "Sports", "Work"]),
        ("Salakot material", "Palm", ["Bamboo", "Nipa", "Coconut"]),
        ("Kipot twins festival", "Janui", ["Tampakan", "T'boli", "Lake Sebu"])
    ],
    "celebrities": [
        ("Pacman", "Manny Pacquiao", ["Nonito Donaire", "Pancho Villa", "Ceferino Garcia"]),
        ("Broadway star", "Lea Salonga", ["Regine Velasquez", "Sarah Geronimo", "Pilar Cawal"]),
        ("Eat Bulaga host", "Vic Sotto", ["Jose Manalo", "Ryan Agoncillo", "Allan K"]),
        ("PBA legend", "Robert Jaworski", ["Ramon Fernandez", "Braulio Lim", "Lim Eng Beng"]),
        ("Miss Universe", "Gloria Diaz", ["Margaret Moran", "Melba Jorge", "Shamcey Supsup"]),
        ("Miss Universe 2018", "Catriona Gray", ["Gazini Ganados", "Kylie Verzosa", "Pia Wurtzbach"]),
        ("OPM King", "Regine Velasquez", ["Martin Nievera", "Gary Valenciano", "Ogie Alcasid"]),
        ("Asia's Songbird", "Regine Velasquez", ["Lea Salonga", "Sarah Geronimo", "Regine Velasquez"]),
        ("Popstar Royalty", "Sarah Geronimo", ["Regine Velasquez", "Lea Salonga", "Moira Dela Torre"]),
        ("Concert Queen", "Regine Velasquez", ["Sarah Geronimo", "Martin Nievera", "Gary V"]),
        ("8-division champ", "Manny Pacquiao", ["Nonito Donaire", "Charly Magnefald", "Donnie Nietes"]),
        ("Miss Earth 2017", "Karla Henry", ["Angelia Ong", "Jamie Herrell", "Catriona Gray"])
    ],
    "sports": [
        ("basketball GOAT", "Robert Jaworski", ["Ramon Fernandez", "Samboy Lim", "Benjie Paras"]),
        ("8-division boxing champ", "Manny Pacquiao", ["Nonito Donaire", "Ceferino Garcia", "Pancho Villa"]),
        ("UAAP 1st championship", "Ateneo", ["UP", "NU", "FEU"]),
        ("PBA most championships", "San Miguel", ["Barangay Ginebra", "Purefoods", "Alaska"]),
        ("Slam Dunk Contest 1998", "Alley-oop", ["Power dunk", "360", "Windmill"]),
        ("FIBA Asia Cup wins", "3", ["2", "4", "1"]),
        ("Southeast Asian Games gold", "Philippines", ["Thailand", "Indonesia", "Vietnam"])
    ],
    "movies": [
        ("highest grossing PH film", "Hello, Love, Goodbye", ["The Hows of Us", "One More Chance", "Starting Over Again"]),
        ("MMFF 2018 Best Picture", "Miracle in Cell No. 7", ["Sin Island", "Kita Kita", "Finally Found Someone"]),
        ("Direk Olivia Lamasan film", "Starting Over Again", ["One More Chance", "Bridging the Gap", "Insomnia"]),
        ("Kathniel first movie", "She's Dating the Gangster", ["Got to Believe", "La Luna Sangre", "Pangako Sa'Yo"]),
        ("JaDine movie", "This Time", ["Surprise Again", "He's Into Her", "Forever in Time"])
    ]
}

def generate_trivia():
    # MORE RANDOM: Pick category by weight + random fact + dynamic options
    categories = list(TRIVIA_DB.keys())
    weights = [len(TRIVIA_DB[cat]) for cat in categories]  # Bigger categories more likely
    
    cat = random.choices(categories, weights=weights)[0]
    fact, answer, wrongs = random.choice(TRIVIA_DB[cat])
    
    # Dynamic options: 3-4 choices, always include correct + 2-3 random wrongs
    num_options = random.randint(3, 4)
    options = [answer]
    available_wrongs = wrongs[:]
    random.shuffle(available_wrongs)
    
    for _ in range(num_options - 1):
        if available_wrongs:
            options.append(available_wrongs.pop(0))
        else:
            # Fallback: repeat random wrong
            options.append(random.choice(wrongs))
    
    random.shuffle(options)
    correct_idx = options.index(answer)
    correct = chr(65 + correct_idx)
    
    cats = {
        "history": "🇵🇭 History", "geography": "🗺️ Geography", "food": "🍜 Food", 
        "culture": "🎭 Culture", "celebrities": "⭐ Stars", "sports": "🏀 Sports",
        "movies": "🎬 Movies"
    }
    
    return {
        "q": f"**{fact.title()}?**",
        "options": [f"{chr(65+i)}. {opt}" for i, opt in enumerate(options)],
        "answer": correct,
        "full": answer,
        "cat": cats.get(cat, cat.title())
    }

# 💾 DATA MANAGEMENT
def load_data():
    global currency_data
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as f:
                currency_data = json.load(f)
        except:
            currency_data = {}
    else:
        currency_data = {}

def save_data():
    with open(DATA_FILE, 'w') as f:
        json.dump(currency_data, f, indent=2)

def get_balance(user_id):
    user_str = str(user_id)
    if user_str not in currency_data:
        currency_data[user_str] = {"balance": 1000, "daily_date": None}
    return currency_data[user_str].get("balance", 1000)

def update_balance(user_id, amount):
    user_str = str(user_id)
    if user_str not in currency_data:
        currency_data[user_str] = {"balance": 1000, "daily_date": None}
    currency_data[user_str]["balance"] = max(0, currency_data[user_str].get("balance", 1000) + amount)
    save_data()

autosave_started = False

@bot.event
async def on_ready():
    load_data()
    print(f'🇵🇭 {bot.user} - FULL FILIPINO CASINO!')
    activity = discord.Game(name=f"{PREFIX}game | casino ni paysen")
    await bot.change_presence(status=discord.Status.online, activity=activity)

    global autosave_started
    if not autosave_started:
        asyncio.create_task(autosave())
        autosave_started = True

# 🇵🇭 TRIVIA - Unlimited Filipino Questions
@bot.command(name='trivia')
async def trivia(ctx):
    """ph trivia questions 500-10k coins"""
    trivia = generate_trivia()
    embed = discord.Embed(title="🇵🇭 **PINOY BRAIN TEASER**", color=0xFF6B35)
    embed.add_field(name="❓", value=trivia["q"], inline=False)
    embed.add_field(name="📋", value="\n".join(trivia["options"]), inline=False)
    embed.add_field(name="💰", value="**500-10,000 Coins!**", inline=True)
    embed.add_field(name="🏷️", value=trivia["cat"], inline=True)
    embed.set_footer(text="Reply **A/B/C/D**! 30s ⏱️")
    
    msg = await ctx.send(embed=embed)

    def check(m):
        return m.channel == ctx.channel and m.author == ctx.author and m.content.upper() in 'ABCD'

    try:
        ans = await bot.wait_for('message', timeout=30, check=check)
        if ans.content.upper() == trivia["answer"]:
            reward = random.randint(500, 10000)
            update_balance(ctx.author.id, reward)
            embed = discord.Embed(title="**may tama ka**", color=0x00FF00)
            embed.add_field(name="🥇", value=f"{ctx.author.mention}", inline=True)
            embed.add_field(name="🪙", value=f"**{reward:,} Coins!**", inline=True)
            embed.add_field(name="✅", value=f"**{trivia['full']}**", inline=False)
            await msg.edit(embed=embed)
            await ctx.send(f"**{ctx.author.display_name}** wins 🪙{reward:,}!")
        else:
            embed = discord.Embed(title="**bobo mali**", color=0xFF0000)
            embed.add_field(name="✅", value=f"**{trivia['answer']}. {trivia['full']}**", inline=False)
            await msg.edit(embed=embed)
            await ctx.send("isa pa tanga")
    except asyncio.TimeoutError:
        embed = discord.Embed(title="**oras mona**", color=0xFFA500)
        embed.add_field(name="✅", value=f"**{trivia['answer']}. {trivia['full']}**")
        await msg.edit(embed=embed)

# 🎲 DAILY RANDOM REWARDS
@bot.command(name='daily')
async def daily(ctx):
    now = datetime.now()
    user_str = str(ctx.author.id)
    today = now.date().isoformat()
    
    if currency_data.get(user_str, {}).get('daily_date') == today:
        await ctx.send("⏰ **Daily na-claim mo na** Tomorrow ulit")
        return
    
    reward = random.randint(100, 15000)
    update_balance(ctx.author.id, reward)
    currency_data[user_str]['daily_date'] = today
    save_data()
    
    rarity = "JACKPOT" if reward > 10000 else "EPIC" if reward > 5000 else "LUCKY" if reward > 2000 else "Good"
    embed = discord.Embed(title=f"**daily roll: {rarity}!**", color=0x00FF00)
    embed.add_field(name="🪙", value=f"**{reward:,} Coins**")
    await ctx.send(embed=embed)

# 🪙 COIN FLIP BETTING
@bot.command(name='flip', aliases=['cf'])
async def coinflip(ctx, amount: str = None, side: str = None):
    user_id = ctx.author.id
    balance = get_balance(user_id)
    
    try:
        if not amount:
            await ctx.send(f"💡 `!flip 100 heads` `!flip 500 t`\n🪙 **{balance:,}** available")
            return
        bet = int(amount.replace('k', '000').replace(',', ''))
        if bet > balance or bet < 10:
            await ctx.send(f"❌ **Bet 10-{balance:,}** only!")
            return
    except:
        await ctx.send("❌ **Numbers only!**")
        return
    
    if side and side.lower() not in ['h', 'heads', 't', 'tails']:
        await ctx.send("🎯 **`h`eads or `t`ails**")
        return
    
    msg = await ctx.send(f"🪙 **Flipping {bet:,} coins...** {'' if side and side.lower().startswith('h') else ''}")
    await asyncio.sleep(2.5)
    
    result = random.choice(['Heads', 'Tails'])
    won = (side and side.lower().startswith('h') and result == 'Heads') or \
          (side and side.lower().startswith('t') and result == 'Tails') or \
          random.choice([True, False])
    
    payout = bet * 2 if won else -bet
    update_balance(user_id, payout)
    new_bal = get_balance(user_id)
    
    embed = discord.Embed(title=f"🪙 **{result}**", color=0x00FF00 if won else 0xFF0000)
    embed.add_field(name="spent", value=f"**{bet:,}**", inline=True)
    embed.add_field(name="📊", value="**win**" if won else "**lost**", inline=True)
    embed.add_field(name="Balance", value=f"**{new_bal:,}**", inline=False)
    await msg.edit(embed=embed)

# 🎁 GIFTING SYSTEM
@bot.command(name='gift', aliases=['give', 'tip'])
async def gift(ctx, user: discord.Member = None, amount: str = None, *, note=""):
    if not user or not amount:
        await ctx.send("`!gift @user 500 [note]`\n`!gift @user all`")
        return
    
    sender_id = ctx.author.id
    sender_bal = get_balance(sender_id)
    
    try:
        if amount.lower() == 'all':
            gift_amt = sender_bal - 1 if sender_bal > 1 else 0
        else:
            gift_amt = int(amount.replace('k', '000').replace(',', ''))
            if gift_amt > sender_bal or gift_amt < 1:
                await ctx.send(f"❌ You have 🪙**{sender_bal:,}**")
                return
    except:
        await ctx.send("❌ **number or `all`**")
        return
    
    if user.id == sender_id:
        await ctx.send("❌ **tanga bawal sa sarili**")
        return

    # STEP 1: Show confirmation with reactions
    embed = discord.Embed(title="**sent you moni**", color=0xFFD700)
    embed.add_field(name=f" {ctx.author.display_name}", value=f"**-🪙{gift_amt:,}**", inline=True)
    embed.add_field(name=f" {user.display_name}", value=f"**+🪙{gift_amt:,}**", inline=True)
    embed.add_field(name="", value=note[:40], inline=False)
    embed.set_footer(text="**React ✅ to send or ❌ to cancel**")
    
    msg = await ctx.send(embed=embed)
    await msg.add_reaction("✅")
    await msg.add_reaction("❌")

    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in ["✅", "❌"] and reaction.message.id == msg.id

    try:
        reaction, user = await bot.wait_for('reaction_add', timeout=None, check=check)
        
        if str(reaction.emoji) == "✅":
            # STEP 2: Process gift
            update_balance(sender_id, -gift_amt)
            update_balance(user.id, gift_amt)
            
            embed.color = 0x00FF00
            embed.title = "✅ **sent**"
            embed.set_footer(text="")
            await msg.edit(embed=embed)
            
        else:
            embed.color = 0xFF0000
            embed.title = "❌ **cancelled**"
            embed.set_footer(text="")
            await msg.edit(embed=embed)
            
    except asyncio.TimeoutError:
        pass  # No timeout, so this won't trigger

# 💰 BALANCE & LEADERBOARD
@bot.command(name='balance', aliases=['bal'])
async def balance(ctx):
    """Only shows YOUR currency amount"""
    bal = get_balance(ctx.author.id)
    await ctx.send(f"🪙 **{bal:,}**")

@bot.command(name='leaderboard', aliases=['lb', 'top', 'rich'])
async def leaderboard(ctx):
    top = sorted([(k, v['balance']) for k, v in currency_data.items()], 
                key=lambda x: x[1], reverse=True)[:10]
    
    embed = discord.Embed(title="👑 **Riches list**", color=0x0099FF)
    for i, (uid, bal) in enumerate(top, 1):
        user = bot.get_user(int(uid))
        name = user.display_name[:14] if user else uid[-4:]
        medal = "🥇🥈🥉" if i <= 3 else f"{i}."
        embed.add_field(name=f"{medal} {name}", value=f"🪙 **{bal:,}**", inline=False)
    await ctx.send(embed=embed)

# 🎮 HELP & STATUS
@bot.command(name='help')
async def help_all(ctx):
    embed = discord.Embed(title="**casino ni paysen**", description="**casino ni paysen**", color=0xFF6B35)
    embed.add_field(name="🧐 Trivia", value="`!trivia` - Unlimited questions", inline=True)
    embed.add_field(name="🎲 Daily", value="`!daily` - 100-15k coins", inline=True)
    embed.add_field(name="🪙 Flip", value="`!flip 100 h/t` - 2x payout", inline=True)
    embed.add_field(name="🎁 Gift", value="`!gift @user 500`", inline=True)
    embed.add_field(name="💰 Info", value="`!balance` `!lb`", inline=True)
    await ctx.send(embed=embed)

# Auto-save
async def autosave():
    while True:
        await asyncio.sleep(60)
        save_data()

if __name__ == "__main__":
    load_data()
    print("**casino ni paysen** Starting...")
    print("Commands: !trivia !daily !flip !gift !balance !lb")
    bot.run(TOKEN)