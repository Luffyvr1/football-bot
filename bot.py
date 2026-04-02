import discord
from discord.ext import commands, tasks
from datetime import datetime
import os

TOKEN = os.getenv("DISCORD_TOKEN")
USER_ID = 833473654800777216

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# -----------------------------
# DAY MAP
# -----------------------------
day_map = {
    0: 1, 1: 2, 2: 3, 3: 4, 4: 5, 5: 6, 6: 7
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
# SOLO SOCCER (YOUR PROGRAM)
# -----------------------------
solo_program = {
    1: [
        "FIFA 11 warmup",
        "1v1 shadow defending",
        "cone weave → sprint → turn → cone weave",
        "backpedal 10y → sprint 10y",
        "headers",
        "control out of sky → long ball"
    ],
    2: ["Juggling (light day)"],
    3: [
        "warmup", "ladder", "wall pass pressure breaks",
        "40 yd sprints", "footwork",
        "long pass target practice",
        "100x wall pass L/R",
        "5-10-5 shuttle"
    ],
    4: [
        "100x left", "100x right", "100 alternating"
    ],
    5: [
        "10m sprints", "lateral cone shuffles",
        "backpack push/pull", "burpees",
        "ladder", "Day 1 again"
    ],
    6: ["recovery touches", "light dribbling", "mobility"],
    7: ["match prep / recovery"]
}

# -----------------------------
# SPEED PROGRAM (YOUR EXACT)
# -----------------------------
speed_program = {
    1: """DAY 1:
- dynamic warmup
- 60 yd sprint
- broad jumps

WORK:
- broad jumps 3x3
- sprint 3x10m
- squat 4x4
- incline DB bench 3x6
- GHD hip ext 3x8
- DB row 3x8""",

    2: """RECOVERY:
- 2 min cardio
- 10 russian baby makers
- 5 cossack squats
- 3 rounds:
  - 90/90 (5 each)
  - down dog → pigeon""",

    3: """DAY 3:
- flying 10s
- single leg pogos
- push press
- hip thrust
- pull ups
- split squat""",

    4: """RECOVERY:
- 3 rounds:
  - calf iso 30s
  - 3 min conditioning
  - 8 hip flexor curls
  - 3 min conditioning""",

    5: """DAY 5:
- sprint 3x20m
- flying 10s
- box jumps
- DB bench
- leg extension
- DB row""",

    6: """RECOVERY:
- repeat recovery circuit""",

    7: """MATCH / LIGHT DAY"""
}

# -----------------------------
# BUILD PLAN
# -----------------------------
def build_plan():
    now = datetime.now()
    day_name = now.strftime("%A").lower()
    program_day = day_map[now.weekday()]

    msg = f"🏟️ DAILY PLAN ({day_name.upper()})\n\n"

    msg += "⚽ TEAM:\n"
    msg += team_training.get(day_name, "None") + "\n\n"

    msg += "🧠 SOLO:\n"
    for s in solo_program.get(program_day, []):
        msg += f"- {s}\n"

    msg += "\n⚡ SPEED:\n"
    msg += speed_program.get(program_day, "")

    return msg

# -----------------------------
# DM FUNCTION
# -----------------------------
async def send_dm(content):
    user = await bot.fetch_user(USER_ID)
    await user.send(content)

# -----------------------------
# SCHEDULER
# -----------------------------
triggered = set()

@tasks.loop(seconds=10)
async def scheduler():
    now = datetime.now().strftime("%H:%M")

    if now == "00:00":
        triggered.clear()

    if now == "05:00" and "5" not in triggered:
        await send_dm(build_plan())
        triggered.add("5")

    elif now == "12:00" and "12" not in triggered:
        await send_dm("🍽️ Lunch reminder")
        triggered.add("12")

    elif now == "14:00" and "14" not in triggered:
        await send_dm("🟡 Stay ready")
        triggered.add("14")

    elif now == "16:00" and "16" not in triggered:
        await send_dm("⚽ Pre-training prep")
        triggered.add("16")

    elif now == "21:00" and "21" not in triggered:
        await send_dm("🌙 Night routine + recovery")
        triggered.add("21")

# -----------------------------
# START
# -----------------------------
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    scheduler.start()

bot.run(TOKEN)
