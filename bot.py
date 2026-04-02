import discord
from discord.ext import commands, tasks
from datetime import datetime

TOKEN = "MTQ4ODk5MTY1ODMwNDYwNjQ1OQ.GZB5bl.ZftHNX8-8fkve8eh9vyy4bK3V4ZGVVMH_EzjEw"
USER_ID = 833473654800777216

# -----------------------------
# INTENTS
# -----------------------------
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# -----------------------------
# DAY MAPPING (Mon = Day 1)
# -----------------------------
day_map = {
    0: 1,  # Monday
    1: 2,  # Tuesday
    2: 3,  # Wednesday
    3: 4,  # Thursday
    4: 5,  # Friday
    5: 6,  # Saturday
    6: 7   # Sunday
}

# -----------------------------
# TEAM TRAINING
# -----------------------------
team_training = {
    "monday": "6:00–7:30 (leave 5:15)",
    "tuesday": "6:30–8:00 (leave 5:45)",
    "thursday": "5:00–6:30 (leave 4:15)"
}

# -----------------------------
# YOUR SOLO SOCCER PROGRAM (YOU WANTED THIS BACK)
# -----------------------------
solo_program = {
    1: [
        "FIFA 11 warmup",
        "1v1 shadow defending",
        "cone weave → sprint → turn → cone weave",
        "backpedal 10y → sprint 10y",
        "headers"
    ],

    2: ["Juggling (light technical day)"],

    3: [
        "Warmup",
        "Ladder footwork",
        "Wall passes (both feet)",
        "40y sprint mechanics",
        "1v1 ball control under pressure"
    ],

    4: [
        "100x wall passes (left/right/alternate)",
        "first touch drills",
        "turning under pressure"
    ],

    5: [
        "10m acceleration sprints",
        "lateral cone shuffles",
        "reaction drills",
        "small sided intensity touches"
    ],

    6: [
        "Recovery touches",
        "light dribbling",
        "mobility + ball feel"
    ],

    7: [
        "MATCH DAY / GAME DAY PREP",
        "light touches only",
        "activation + mental prep"
    ]
}

# -----------------------------
# YOUR EXACT SPEED PROGRAM (UNCHANGED)
# -----------------------------
speed_program = {
    1: """DAY 1 TESTING (every 3 weeks)
- dynamic warmup
- 60 yard sprint
- max effort broad jumps

DAY 1 WORK DAY
- broad jumps
- 3x3 sprint
- 3x10m
- safety bar box squat 4x4 @75%
- incline DB bench press 3x6
- GHD hip extension 3x8
- chest supported DB row 3x8
""",

    2: """DAY 2 SPEED RECOVERY
- biking or walking
- circuit 1""",

    3: """DAY 3 SPEED WORK
- flying 10s 2x10m
- rear foot elevated pogos
- push press 4x4 @75%
- hip thrust 3x8
- pull ups 3x6
- DB split squat 3x8
""",

    4: """DAY 4 SPEED RECOVERY
- biking or walking
- circuit 2""",

    5: """DAY 5 SPEED WORK
- sprint 3x20m
- flying 10s 3x10m
- box jumps 4x2
- DB bench press 3x8
- DB row 3x8
""",

    6: """DAY 6 SPEED RECOVERY
- biking or walking
- circuit 1""",

    7: """DAY 7 MATCH / LIGHT DAY
- full recovery or match prep
"""
}

# -----------------------------
# ISOMETRICS / PLYOS
# -----------------------------
isometrics = ["hip iso", "groin iso", "hamstring iso", "soleus iso"]
plyos = ["squat jumps", "pogos", "chair jumps"]

# -----------------------------
# NIGHT ROUTINE
# -----------------------------
def night_routine():
    return """🌙 NIGHT ROUTINE
- stretch 10 min
- foam roll
- ankle/hip mobility
- hydrate
- visualize tomorrow session
- sleep early
"""

# -----------------------------
# BUILD DAILY PLAN (FULL SYSTEM)
# -----------------------------
def build_plan():
    now = datetime.now()
    day_name = now.strftime("%A").lower()
    date = now.strftime("%Y-%m-%d")

    program_day = day_map[now.weekday()]

    msg = f"🏟️ **DAILY FOOTBALL PLAN ({day_name.upper()})**\n\n"

    # TEAM TRAINING
    msg += "⚽ TEAM TRAINING:\n"
    msg += team_training.get(day_name, "No team training today") + "\n\n"

    # SOLO SOCCER
    msg += "🧠 SOLO SOCCER SESSION:\n"
    for s in solo_program.get(program_day, []):
        msg += f"- {s}\n"
    msg += "\n"

    # SPEED PROGRAM
    msg += "⚡ SPEED PROGRAM:\n"
    msg += speed_program.get(program_day, "No speed session") + "\n\n"

    # ISOMETRICS
    msg += "🧊 ISOMETRICS:\n"
    for i in isometrics:
        msg += f"- {i}\n"

    msg += "\n⚡ PLYOMETRICS:\n"
    for p in plyos:
        msg += f"- {p}\n"

    return msg


# -----------------------------
# DM SYSTEM
# -----------------------------
async def send_dm(content):
    try:
        user = await bot.fetch_user(USER_ID)
        await user.send(content)
    except Exception as e:
        print("DM ERROR:", e)


# -----------------------------
# SCHEDULER
# -----------------------------
triggered_today = set()

@tasks.loop(seconds=10)
async def scheduler():
    global triggered_today

    now = datetime.now()
    time_str = now.strftime("%H:%M")

    if time_str == "00:00":
        triggered_today.clear()

    if time_str == "05:00" and "05:00" not in triggered_today:
        await send_dm("🌅 5 AM FULL FOOTBALL PLAN\n\n" + build_plan())
        triggered_today.add("05:00")

    elif time_str == "12:00" and "12:00" not in triggered_today:
        await send_dm("🍽️ LUNCH CHECK")
        triggered_today.add("12:00")

    elif time_str == "14:00" and "14:00" not in triggered_today:
        await send_dm("🟡 2 PM ACTIVATION")
        triggered_today.add("14:00")

    elif time_str == "16:00" and "16:00" not in triggered_today:
        await send_dm("⚽ PRE-TRAINING CHECK")
        triggered_today.add("16:00")

    elif time_str == "21:00" and "21:00" not in triggered_today:
        await send_dm(night_routine())
        triggered_today.add("21:00")


# -----------------------------
# START BOT
# -----------------------------
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

    if not scheduler.is_running():
        scheduler.start()


# -----------------------------
# TEST
# -----------------------------
@bot.command()
async def test(ctx):
    await send_dm("✅ SYSTEM WORKING")


bot.run(TOKEN)