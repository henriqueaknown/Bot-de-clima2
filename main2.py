import discord
from discord.ext import commands
import requests
import pyttsx3
import random


# ==========================================
# CONFIGURAÇÕES
# ==========================================

TOKEN = "YOUR_BOT_TOKEN"

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

engine = pyttsx3.init()


# ==========================================
# FUNÇÃO DE CLIMA ATUAL
# ==========================================

def get_weather(city: str):
    url = f"https://wttr.in/{city}?format=j1"

    try:
        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            return None

        return response.json()

    except requests.RequestException:
        return None


# ==========================================
# COMANDO DE CLIMA
# ==========================================

@bot.command()
async def weather(ctx, *, city: str):

    data = get_weather(city)

    if data is None:
        await ctx.send(
            "❌ Não foi possível obter os dados meteorológicos."
        )
        return

    try:
        current = data["current_condition"][0]

        temperature = current["temp_C"]
        feels_like = current["FeelsLikeC"]
        humidity = current["humidity"]
        wind = current["windspeedKmph"]
        condition = current["weatherDesc"][0]["value"]

        message = (
            f"🌦️ **Tempo em {city}**\n\n"
            f"🌡️ Temperatura: **{temperature}°C**\n"
            f"🤚 Sensação térmica: **{feels_like}°C**\n"
            f"☁️ Condição: **{condition}**\n"
            f"💧 Umidade: **{humidity}%**\n"
            f"💨 Vento: **{wind} km/h**"
        )

        await ctx.send(message)

        speak(
            f"Tempo em {city}. "
            f"Temperatura de {temperature} graus. "
            f"Sensação térmica de {feels_like} graus. "
            f"Condição: {condition}. "
            f"Umidade de {humidity} por cento."
        )

    except (KeyError, IndexError):
        await ctx.send(
            "❌ Não foi possível interpretar os dados meteorológicos."
        )


# ==========================================
# PREVISÃO DO TEMPO
# ==========================================

@bot.command()
async def forecast(ctx, *, city: str):

    data = get_weather(city)

    if data is None:
        await ctx.send(
            "❌ Não foi possível obter a previsão."
        )
        return

    try:
        forecasts = data["weather"]

        message = f"📅 **Previsão para {city}**\n\n"

        for day in forecasts[:3]:

            date = day["date"]
            max_temp = day["maxtempC"]
            min_temp = day["mintempC"]
            condition = day["hourly"][4]["weatherDesc"][0]["value"]

            message += (
                f"📆 **{date}**\n"
                f"🌡️ Máxima: {max_temp}°C\n"
                f"🥶 Mínima: {min_temp}°C\n"
                f"☁️ {condition}\n\n"
            )

        await ctx.send(message)

    except (KeyError, IndexError):
        await ctx.send(
            "❌ Não foi possível obter a previsão."
        )


# ==========================================
# FUNÇÃO DE SÍNTESE DE VOZ
# ==========================================

def speak(text: str):

    engine.say(text)
    engine.runAndWait()


# ==========================================
# COMANDO DE VOZ
# ==========================================

@bot.command()
async def speaktext(ctx, *, text: str):

    speak(text)

    await ctx.send(
        "🔊 Texto reproduzido com sucesso."
    )


# ==========================================
# ALTERAR VELOCIDADE DA VOZ
# ==========================================

@bot.command()
async def voicespeed(ctx, speed: int):

    if speed < 50 or speed > 300:
        await ctx.send(
            "❌ Escolha uma velocidade entre 50 e 300."
        )
        return

    engine.setProperty("rate", speed)

    await ctx.send(
        f"🔊 Velocidade da voz definida para **{speed}**."
    )


# ==========================================
# LISTAR VOZES DISPONÍVEIS
# ==========================================

@bot.command()
async def voices(ctx):

    available_voices = engine.getProperty("voices")

    message = "🗣️ **Vozes disponíveis:**\n\n"

    for index, voice in enumerate(available_voices):
        message += f"**{index}** - {voice.name}\n"

    await ctx.send(message[:2000])


# ==========================================
# PING
# ==========================================

@bot.command()
async def ping(ctx):

    latency = round(bot.latency * 1000)

    await ctx.send(
        f"🏓 Pong!\n"
        f"📡 Latência: **{latency} ms**"
    )


# ==========================================
# INFORMAÇÕES DO SERVIDOR
# ==========================================

@bot.command()
async def serverinfo(ctx):

    guild = ctx.guild

    message = (
        f"🖥️ **Informações do servidor**\n\n"
        f"📛 Nome: **{guild.name}**\n"
        f"👥 Membros: **{guild.member_count}**\n"
        f"🆔 ID: **{guild.id}**\n"
        f"📅 Criado em: **{guild.created_at.strftime('%d/%m/%Y')}**"
    )

    await ctx.send(message)


# ==========================================
# INFORMAÇÕES DO USUÁRIO
# ==========================================

@bot.command()
async def userinfo(ctx, member: discord.Member = None):

    if member is None:
        member = ctx.author

    message = (
        f"👤 **Informações do usuário**\n\n"
        f"🏷️ Nome: **{member.name}**\n"
        f"🆔 ID: **{member.id}**\n"
        f"📅 Conta criada em: "
        f"**{member.created_at.strftime('%d/%m/%Y')}**\n"
        f"📥 Entrou no servidor em: "
        f"**{member.joined_at.strftime('%d/%m/%Y')}**"
    )

    await ctx.send(message)


# ==========================================
# CARA OU COROA
# ==========================================

@bot.command()
async def coinflip(ctx):

    result = random.choice(
        ["🪙 Cara!", "🪙 Coroa!"]
    )

    await ctx.send(result)


# ==========================================
# DADOS
# ==========================================

@bot.command()
async def dice(ctx):

    result = random.randint(1, 6)

    await ctx.send(
        f"🎲 Você tirou **{result}**!"
    )


# ==========================================
# NÚMERO ALEATÓRIO
# ==========================================

@bot.command()
async def roll(ctx, minimum: int = 1, maximum: int = 100):

    if minimum >= maximum:
        await ctx.send(
            "❌ O valor mínimo deve ser menor que o máximo."
        )
        return

    result = random.randint(
        minimum,
        maximum
    )

    await ctx.send(
        f"🎲 Número sorteado: **{result}**"
    )


# ==========================================
# 8 BALL
# ==========================================

@bot.command(name="8ball")
async def eightball(ctx, *, question: str):

    answers = [
        "🎱 Com certeza!",
        "🎱 Sim.",
        "🎱 Provavelmente.",
        "🎱 Talvez.",
        "🎱 Não sei.",
        "🎱 Provavelmente não.",
        "🎱 Não.",
        "🎱 De jeito nenhum!"
    ]

    answer = random.choice(answers)

    await ctx.send(
        f"❓ **Pergunta:** {question}\n"
        f"🔮 **Resposta:** {answer}"
    )


# ==========================================
# COMANDO DE AJUDA
# ==========================================

@bot.command()
async def commandslist(ctx):

    message = """
🤖 **COMANDOS DO BOT**

🌦️ **CLIMA**
`!weather cidade`
`!forecast cidade`

🔊 **VOZ**
`!speaktext texto`
`!voicespeed velocidade`
`!voices`

⚙️ **UTILIDADES**
`!ping`
`!serverinfo`
`!userinfo`

🎮 **DIVERSÃO**
`!coinflip`
`!dice`
`!roll`
`!8ball pergunta`
"""

    await ctx.send(message)


# ==========================================
# EVENTO DE INICIALIZAÇÃO
# ==========================================

@bot.event
async def on_ready():

    print(
        f"Bot conectado como {bot.user}"
    )


# ==========================================
# INICIA O BOT
# ==========================================

bot.run(TOKEN)
