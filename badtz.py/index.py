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

# ⌨️ SPEED TYPING — FILIPINO TONGUE TWISTERS
TWISTERS = [
    "Pinaikot-ikot ni Kiko ang kanyang kotse.",
    "Minekaniko ng mekaniko si Monico.",
    "Bababa ba? Bababa.",
    "Ang relo ni Lolo Rolly ay galing pa Roma.",
    "Pitongput pitong puting tupa.",
    "Nakakapagpabagabag ang nakakapagpabagabag na balita.",
    "Usong-uso ang suso ni Susan sa Lunes.",
    "Ang aso ni Oslo ay nasa loob ng asul na kahon.",
    "Pinagpapalit-palit ni Pete ang plato at platito.",
    "Si Tetang nakatikim ng tatlong tutong na tinapay.",
    "Kakakanta-kanta ka pa rin pala kahapon.",
    "Si Pepe pumipili ng pinakapipiling pinya.",
    "Tatlong tukong matatakaw, tumakbong tatlo sa takipsilim.",
    "Naka pang-ilalim na panyo si Pinang.",
    "Bumili ako ng bituka ng butiki sa Bulacan.",
    "Kakakaway-kaway ng kakaibang kawayan ni Kakay.",
    "Si Ising isang nag-iisang isda sa Iloilo.",
    "Ang lalaking maraming alaga ay laging nagaalaga ng alaga.",
    "Si Lorna naglalaba ng lalabhanin sa lababo.",
    "Pulang pulis sa pulang pader nakapulupot na pulang panyolito.",
    "Kalbo ang kalabaw ni Kabesang Kanor.",
    "Tagaytay, Tuktok, Tagbilaran, Tagaytay ulit.",
    "Mama, mamamamamamamamamamayan na po ako.",
    "Ang ampalaya ni Aling Lyana ay laging maasim na maasim.",
    "Sinusuyod ng suyod si Seyong sa Sabado.",
    "Pakulputin mo ang kulot na pakulot ni Pekto.",
    "Ang batang batugan ay nag-bababatibot sa batuhan.",
]

def _normalize(text: str) -> str:
    return ''.join(ch.lower() for ch in text if ch.isalnum())

DIFFICULTIES = {
    "easy":   {"memorize": 8,   "mult": 1.0, "cap": 8000,  "label": "🟢 EASY",   "color": 0x2ECC71},
    "normal": {"memorize": 5,   "mult": 1.5, "cap": 12000, "label": "🟣 NORMAL", "color": 0x9B59B6},
    "hard":   {"memorize": 3,   "mult": 2.5, "cap": 20000, "label": "🟠 HARD",   "color": 0xE67E22},
    "insane": {"memorize": 1.5, "mult": 4.0, "cap": 40000, "label": "🔴 INSANE", "color": 0xC0392B},
}
DIFFICULTY_ALIASES = {
    "e": "easy", "easy": "easy",
    "n": "normal", "normal": "normal", "norm": "normal", "med": "normal", "medium": "normal",
    "h": "hard", "hard": "hard",
    "i": "insane", "insane": "insane", "imposible": "insane", "impossible": "insane",
}

@bot.command(name='twister', aliases=['type', 'tw'])
async def twister(ctx, difficulty: str = "normal"):
    """Memorize a Filipino tongue twister, then type it from memory!
    Difficulty: easy / normal / hard / insane"""
    diff_key = DIFFICULTY_ALIASES.get(difficulty.lower())
    if not diff_key:
        await ctx.send(
            "❌ **Pick a difficulty:** `!twister easy` `!twister normal` `!twister hard` `!twister insane`"
        )
        return
    diff = DIFFICULTIES[diff_key]

    phrase = random.choice(TWISTERS)
    memorize_secs = diff["memorize"]

    # Typing window AFTER the phrase disappears
    time_limit = max(8, min(30, int(len(phrase) * 0.45)))

    # STEP 1: Reveal phrase for memorize_secs only
    embed = discord.Embed(
        title=f"⌨️ **TONGUE TWISTER — {diff['label']}**",
        description=f"🧠 **Memorize this in {memorize_secs}s!** It will disappear...",
        color=diff["color"],
    )
    embed.add_field(name="🌀 Phrase", value=f"```{phrase}```", inline=False)
    embed.add_field(name="⏱️ Memorize", value=f"**{memorize_secs}s**", inline=True)
    embed.add_field(name="💰 Reward", value=f"**up to {diff['cap']:,} coins** ({diff['mult']}x)", inline=True)
    embed.set_footer(text="Tandaan mo! Mawawala na 'yan ⚡")

    msg = await ctx.send(embed=embed)
    await asyncio.sleep(memorize_secs)

    # STEP 2: Hide the phrase, open typing window
    hidden = discord.Embed(
        title=f"🫥 **PHRASE HIDDEN — TYPE NOW! ({diff['label']})**",
        description="Type the tongue twister **from memory** before time runs out!",
        color=0xE67E22,
    )
    hidden.add_field(name="🌀 Phrase", value="```???  HIDDEN  ???```", inline=False)
    hidden.add_field(name="⏱️ Type", value=f"**{time_limit}s**", inline=True)
    hidden.add_field(name="💰 Reward", value=f"**up to {diff['cap']:,} coins** ({diff['mult']}x)", inline=True)
    hidden.set_footer(text="Bilis! Type it back as your next message ⚡")
    await msg.edit(embed=hidden)

    start = asyncio.get_event_loop().time()

    def check(m):
        return m.channel == ctx.channel and m.author == ctx.author

    try:
        ans = await bot.wait_for('message', timeout=time_limit, check=check)
        elapsed = asyncio.get_event_loop().time() - start

        target_norm = _normalize(phrase)
        user_norm = _normalize(ans.content)

        if user_norm == target_norm:
            # Reward scales with phrase length, remaining time, and difficulty multiplier
            base = 500 + len(phrase) * 40
            speed_bonus = int(((time_limit - elapsed) / time_limit) * 3000)
            raw_reward = int((base + speed_bonus) * diff["mult"])
            reward = min(diff["cap"], raw_reward)
            update_balance(ctx.author.id, reward)

            result = discord.Embed(title=f"🏆 **paldo — {diff['label']}**", color=0x00FF00)
            result.add_field(name="⚡ Time", value=f"**{elapsed:.2f}s**", inline=True)
            result.add_field(name="🪙 Reward", value=f"**{reward:,} coins** ({diff['mult']}x)", inline=True)
            result.add_field(name="✅ Phrase", value=f"```{phrase}```", inline=False)
            await ctx.send(embed=result)
        else:
            # Partial credit: count correct characters in order (LCS-lite via prefix match)
            matched = 0
            for a, b in zip(user_norm, target_norm):
                if a == b:
                    matched += 1
                else:
                    break
            accuracy = (matched / len(target_norm)) * 100 if target_norm else 0

            result = discord.Embed(title="❌ **tanga mo naman**", color=0xFF0000)
            result.add_field(name="🎯 Accuracy", value=f"**{accuracy:.0f}%**", inline=True)
            result.add_field(name="⏱️ Time", value=f"**{elapsed:.2f}s**", inline=True)
            result.add_field(name="✅ Tama", value=f"```{phrase}```", inline=False)
            result.add_field(name="📝 Sagot mo", value=f"```{ans.content[:200]}```", inline=False)
            await ctx.send(embed=result)
    except asyncio.TimeoutError:
        result = discord.Embed(title="⏰ **overtime tanga mo naman**", color=0xFFA500)
        result.add_field(name="✅ Phrase", value=f"```{phrase}```", inline=False)
        await ctx.send(embed=result)

# 🔀 FILIPINO WORD SCRAMBLE
SCRAMBLE_WORDS = [
    ("adobo", "national dish"),
    ("sampaguita", "national flower"),
    ("jeepney", "iconic public transport"),
    ("balikbayan", "returning kababayan"),
    ("kalabaw", "national animal"),
    ("bayanihan", "community spirit"),
    ("halohalo", "iced dessert"),
    ("sinigang", "sour soup"),
    ("kamatis", "tomato in tagalog"),
    ("mabuhay", "filipino greeting"),
    ("pinoy", "slang for filipino"),
    ("pasalubong", "homecoming gift"),
    ("kuya", "older brother"),
    ("ate", "older sister"),
    ("lola", "grandma"),
    ("lolo", "grandpa"),
    ("kapamilya", "family / abs-cbn"),
    ("kapuso", "one heart / gma"),
    ("manananggal", "mythical creature"),
    ("aswang", "shape-shifting monster"),
    ("tikbalang", "horse demon"),
    ("kapre", "tree-dwelling giant"),
    ("nuno", "small old man (sa punso)"),
    ("salamat", "thank you"),
    ("kumusta", "how are you"),
    ("paalam", "goodbye"),
    ("magandangaraw", "good day"),
    ("payong", "umbrella"),
    ("tsinelas", "slippers"),
    ("kalye", "street"),
    ("simbahan", "church"),
    ("palengke", "wet market"),
    ("eskwelahan", "school"),
    ("pamilya", "family"),
    ("kaibigan", "friend"),
    ("puso", "heart"),
    ("luzon", "northern island group"),
    ("visayas", "central island group"),
    ("mindanao", "southern island group"),
    ("manila", "national capital"),
    ("baguio", "summer capital"),
    ("boracay", "famous beach"),
    ("palawan", "underground river"),
    ("pacquiao", "boxing legend"),
    ("rizal", "national hero"),
    ("bonifacio", "katipunan founder"),
    ("lapulapu", "datu of mactan"),
    ("tinikling", "bamboo dance"),
    ("karaoke", "videoke"),
    ("balut", "duck embryo snack"),
]

def _scramble(word: str) -> str:
    if len(word) <= 2:
        return word
    chars = list(word)
    for _ in range(20):
        random.shuffle(chars)
        scrambled = ''.join(chars)
        if scrambled.lower() != word.lower():
            return scrambled
    return scrambled

@bot.command(name='scramble', aliases=['scram', 'sc'])
async def scramble(ctx):
    """Unscramble a Filipino word before the timer runs out!"""
    word, hint = random.choice(SCRAMBLE_WORDS)
    scrambled = _scramble(word)

    # Time scales with length: ~2s per letter, min 10s, max 30s
    time_limit = max(10, min(30, int(len(word) * 2)))

    embed = discord.Embed(
        title="🔀 **WORD SCRAMBLE**",
        description="Unscramble the Filipino word before the timer runs out!",
        color=0x1ABC9C,
    )
    embed.add_field(name="🔀 Scrambled", value=f"```{scrambled.upper()}```", inline=False)
    embed.add_field(name="💡 Hint", value=f"_{hint}_", inline=True)
    embed.add_field(name="⏱️ Time", value=f"**{time_limit}s**", inline=True)
    embed.add_field(name="💰 Reward", value="**up to 10,000 coins**", inline=True)
    embed.set_footer(text="Type the unscrambled word as your next message ⚡")

    msg = await ctx.send(embed=embed)
    start = asyncio.get_event_loop().time()

    def check(m):
        return m.channel == ctx.channel and m.author == ctx.author

    try:
        ans = await bot.wait_for('message', timeout=time_limit, check=check)
        elapsed = asyncio.get_event_loop().time() - start

        guess = ''.join(ch.lower() for ch in ans.content if ch.isalpha())
        target = word.lower()

        if guess == target:
            base = 400 + len(word) * 200
            speed_bonus = int(((time_limit - elapsed) / time_limit) * 3000)
            reward = min(10000, base + speed_bonus)
            update_balance(ctx.author.id, reward)

            result = discord.Embed(title="🏆 **tanginamo galing mo**", color=0x00FF00)
            result.add_field(name="⚡ Time", value=f"**{elapsed:.2f}s**", inline=True)
            result.add_field(name="🪙 Reward", value=f"**{reward:,} coins**", inline=True)
            result.add_field(name="✅ Word", value=f"**{word.upper()}**", inline=False)
            await ctx.send(embed=result)
        else:
            result = discord.Embed(title="❌ **MALI! tanga mo**", color=0xFF0000)
            result.add_field(name="📝 Sagot mo", value=f"`{ans.content[:60]}`", inline=True)
            result.add_field(name="✅ Tama", value=f"**{word.upper()}**", inline=True)
            await ctx.send(embed=result)
    except asyncio.TimeoutError:
        result = discord.Embed(title="⏰ **TIME'S UP!**", color=0xFFA500)
        result.add_field(name="✅ Word", value=f"**{word.upper()}**", inline=False)
        await ctx.send(embed=result)

# 🎲 DAILY RANDOM REWARDS + STREAKS
STREAK_MILESTONES = [
    (3,   1000,  "🔥 3-DAY STREAK"),
    (7,   5000,  "🔥🔥 7-DAY STREAK"),
    (14,  12000, "🔥🔥🔥 14-DAY STREAK"),
    (30,  25000, "👑 30-DAY STREAK"),
    (60,  60000, "🌟 60-DAY LEGEND"),
    (100, 150000, "💎 100-DAY DIYAMANTE"),
]

@bot.command(name='daily')
async def daily(ctx):
    now = datetime.now()
    user_str = str(ctx.author.id)
    today = now.date()
    today_iso = today.isoformat()

    # Ensure user record exists
    get_balance(ctx.author.id)
    user_rec = currency_data[user_str]

    last_claim = user_rec.get('daily_date')
    if last_claim == today_iso:
        streak = user_rec.get('streak', 0)
        await ctx.send(f"⏰ **Daily na-claim mo na** Tomorrow ulit\n🔥 Current streak: **{streak} day(s)**")
        return

    streak = user_rec.get('streak', 0)
    if last_claim:
        try:
            last_date = datetime.fromisoformat(last_claim).date()
            delta = (today - last_date).days
            if delta == 1:
                streak += 1
            elif delta > 1:
                streak = 1
            else:
                streak = max(streak, 1)
        except Exception:
            streak = 1
    else:
        streak = 1

    best = max(user_rec.get('best_streak', 0), streak)

    base_reward = random.randint(100, 15000)

    milestone_bonus = 0
    milestone_label = None
    for days, bonus, label in STREAK_MILESTONES:
        if streak == days:
            milestone_bonus = bonus
            milestone_label = label
            break

    total = base_reward + milestone_bonus
    update_balance(ctx.author.id, total)
    user_rec['daily_date'] = today_iso
    user_rec['streak'] = streak
    user_rec['best_streak'] = best
    save_data()

    rarity = "JACKPOT" if base_reward > 10000 else "EPIC" if base_reward > 5000 else "LUCKY" if base_reward > 2000 else "Good"
    color = 0xFFD700 if milestone_bonus else 0x00FF00
    title = f"**daily roll: {rarity}!**"
    if milestone_label:
        title = f"**{milestone_label} — {rarity}!**"

    embed = discord.Embed(title=title, color=color)
    embed.add_field(name="🪙 Daily", value=f"**{base_reward:,}**", inline=True)
    if milestone_bonus:
        embed.add_field(name="🎁 Streak bonus", value=f"**+{milestone_bonus:,}**", inline=True)
    embed.add_field(name="💰 Total", value=f"**{total:,} coins**", inline=True)
    embed.add_field(name="🔥 Streak", value=f"**{streak} day(s)** (best: {best})", inline=False)

    next_ms = next(((d, b, l) for d, b, l in STREAK_MILESTONES if d > streak), None)
    if next_ms:
        days_left = next_ms[0] - streak
        embed.set_footer(text=f"⏭️ {days_left} day(s) until {next_ms[2]} (+{next_ms[1]:,} bonus)")
    else:
        embed.set_footer(text="👑 You've hit the highest streak tier — keep it up!")

    await ctx.send(embed=embed)
# 🪙 COIN FLIP BETTING
@bot.command(name='flip', aliases=['cf', 'coinflip'])
async def coinflip(ctx, amount: str = None, side: str = None):
    """Coin flip. Usage: !flip <amount|all> [h|t]"""
    user_id = ctx.author.id
    balance = get_balance(user_id)

    try:
        if not amount:
            await ctx.send(f"💡 `!flip 100 heads` `!flip all t` `!flip 500 t`\n🪙 **{balance:,}** available")
            return
        if amount.lower() in ('all', 'allin', 'max'):
            if balance < 10:
                await ctx.send(f"❌ **Need at least 10 coins to go all-in.** You have 🪙**{balance:,}**.")
                return
            bet = balance
        else:
            bet = int(amount.replace('k', '000').replace(',', ''))
            if bet > balance or bet < 10:
                await ctx.send(f"❌ **Bet 10-{balance:,}** only!")
                return
    except Exception:
        return

    if side and side.lower() not in ['h', 'heads', 't', 'tails']:
        await ctx.send("🎯 **`h`eads or `t`ails**")
        return

    msg = await ctx.send(f"🪙 **Flipping {bet:,} coins...**")
    await asyncio.sleep(2.5)

    result = random.choice(['Heads', 'Tails'])
    if side:
        won = (side.lower().startswith('h') and result == 'Heads') or \
              (side.lower().startswith('t') and result == 'Tails')
    else:
        won = random.choice([True, False])

    payout = bet if won else -bet
    update_balance(user_id, payout)
    new_bal = get_balance(user_id)

    all_in = (bet == balance)
    title = f"🪙 **{result}**"
    if all_in:
        title += "  — all in tapang"
    embed = discord.Embed(title=title, color=0x00FF00 if won else 0xFF0000)
    embed.add_field(name="Bet", value=f"**{bet:,}**", inline=True)
    embed.add_field(name="📊", value=("**WIN**" if won else "**LOST**") + (" " if all_in else ""), inline=True)
    if all_in and not won:
        embed.add_field(name="", value="**Wala ka nang pera, tanga kasi.**", inline=False)
    elif all_in and won:
        embed.add_field(name="", value="**PALDOO**", inline=False)
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
@bot.command(name='streak', aliases=['str'])
async def streak_cmd(ctx, user: discord.Member = None):
    """View daily-claim streak (yours or another user's)."""
    target = user or ctx.author
    user_str = str(target.id)
    get_balance(target.id)
    rec = currency_data[user_str]
    cur = rec.get('streak', 0)
    best = rec.get('best_streak', 0)
    last = rec.get('daily_date', 'never')

    next_ms = next(((d, b, l) for d, b, l in STREAK_MILESTONES if d > cur), None)
    embed = discord.Embed(title=f"🔥 **{target.display_name}'s streak**", color=0xFF6B35)
    embed.add_field(name="Current", value=f"**{cur} day(s)**", inline=True)
    embed.add_field(name="Best", value=f"**{best} day(s)**", inline=True)
    embed.add_field(name="Last claim", value=f"`{last}`", inline=False)
    if next_ms:
        embed.set_footer(text=f"⏭️ {next_ms[0] - cur} day(s) until {next_ms[2]} (+{next_ms[1]:,} bonus)")
    else:
        embed.set_footer(text="👑 Highest streak tier reached!")
    await ctx.send(embed=embed)


LB_CATEGORIES = {
    "rich":    {"label": "RICHEST PINOY",       "key": "balance",     "emoji": "👑", "color": 0xFFD700, "unit": "coins",   "default": 0},
    "balance": {"label": "RICHEST PINOY",       "key": "balance",     "emoji": "👑", "color": 0xFFD700, "unit": "coins",   "default": 0},
    "streak":  {"label": "ACTIVE STREAKS",      "key": "streak",      "emoji": "🔥", "color": 0xFF6B35, "unit": "day(s)",  "default": 0},
    "best":    {"label": "ALL-TIME BEST STREAK","key": "best_streak", "emoji": "🏆", "color": 0xE91E63, "unit": "day(s)",  "default": 0},
    "broke":   {"label": "BROKEST PINOY",       "key": "balance",     "emoji": "💸", "color": 0x607D8B, "unit": "coins",   "default": 0, "ascending": True},
}
LB_ALIASES = {
    "rich": "rich", "r": "rich", "money": "rich", "balance": "rich", "bal": "rich",
    "streak": "streak", "s": "streak", "fire": "streak",
    "best": "best", "b": "best", "all": "best", "alltime": "best",
    "broke": "broke", "poor": "broke", "low": "broke",
}

def _medal(rank):
    return {1: "🥇", 2: "🥈", 3: "🥉"}.get(rank, f"`#{rank:>2}`")

async def _name_for(uid):
    """Resolve a Discord user's display name, fetching from API if not cached."""
    try:
        user = bot.get_user(int(uid))
        if user is None:
            user = await bot.fetch_user(int(uid))
        if user is not None:
            return (user.display_name or user.name)[:18]
    except Exception:
        pass
    return f"User-{uid[-4:]}"

@bot.command(name='leaderboard', aliases=['lb', 'top', 'rich'])
async def leaderboard(ctx, category: str = "rich"):
    """Top 10 across multiple categories. Usage: !lb [rich|streak|best|broke]"""
    cat_key = LB_ALIASES.get(category.lower())
    if not cat_key:
        await ctx.send(
            "❌ **Pick a category:** `!lb rich` `!lb streak` `!lb best` `!lb broke`"
        )
        return
    cat = LB_CATEGORIES[cat_key]
    field = cat["key"]
    ascending = cat.get("ascending", False)

    # Build full ranking (only include users with non-default values, except for broke we want everyone)
    entries = []
    for uid, rec in currency_data.items():
        val = rec.get(field, cat["default"])
        if isinstance(val, (int, float)):
            entries.append((uid, val))
    entries.sort(key=lambda x: x[1], reverse=not ascending)

    if not entries:
        await ctx.send("📭 **Walang laman ang leaderboard.** Be the first to play!")
        return

    total_players = len(entries)
    me_id = str(ctx.author.id)
    my_rank = next((i + 1 for i, (uid, _) in enumerate(entries) if uid == me_id), None)

    # Build a row for EVERY player (with medals on top 3, #N for the rest)
    lines = []
    for rank, (uid, val) in enumerate(entries, 1):
        medal = _medal(rank)
        name = await _name_for(uid)
        marker = " ⭐" if uid == me_id else ""
        if isinstance(val, float):
            val_str = f"{val:,.1f}"
        else:
            val_str = f"{val:,}"
        lines.append(f"{medal}  {name:<18} {val_str:>10} {cat['unit']}{marker}")

    # Chunk lines into pages so each embed stays under Discord's 4096-char description limit
    pages = []
    current = []
    current_len = 0
    MAX = 3800  # leave headroom for code fence + formatting
    for line in lines:
        # +1 for newline
        if current and current_len + len(line) + 1 > MAX:
            pages.append(current)
            current = []
            current_len = 0
        current.append(line)
        current_len += len(line) + 1
    if current:
        pages.append(current)

    total_pages = len(pages)
    for page_idx, page_lines in enumerate(pages, 1):
        table = "```\n" + "\n".join(page_lines) + "\n```"
        suffix = f" — page {page_idx}/{total_pages}" if total_pages > 1 else ""
        embed = discord.Embed(
            title=f"{cat['emoji']} **{cat['label']} — ALL PLAYERS**{suffix}",
            description=table,
            color=cat["color"],
        )
        # Show requester's rank on the LAST page if not visible elsewhere
        if page_idx == total_pages and my_rank:
            my_val = next(v for u, v in entries if u == me_id)
            my_str = f"{my_val:,}"
            embed.add_field(
                name="👤 Your rank",
                value=f"**#{my_rank}** — {my_str} {cat['unit']}",
                inline=False,
            )
        if page_idx == total_pages:
            embed.set_footer(text=f"👥 {total_players} players  •  Try: !lb rich / streak / best / broke")
        await ctx.send(embed=embed)

# 🎮 HELP & STATUS
@bot.command(name='help')
async def help_all(ctx):
    embed = discord.Embed(title="**casino ni paysen**", description="**casino ni paysen**", color=0xFF6B35)
    embed.add_field(name="🧐 Trivia", value="`!trivia` - filipino trivia's", inline=True)
    embed.add_field(name="⌨️ Twister", value="`!twister easy/normal/hard/insane`", inline=True)
    embed.add_field(name="🔀 Scramble", value="`!scramble` - Filipino word scramble", inline=True)
    embed.add_field(name="🎲 Daily", value="`!daily` + streaks `!streak`", inline=True)
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
