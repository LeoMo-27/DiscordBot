

import os
import discord
import youtube_dl
import json
import aiohttp
import asyncio
import requests
from random import random, choice, randint
from dotenv import load_dotenv
from discord.ext import commands
from discord import FFmpegPCMAudio
from discord.utils import get
from time import sleep

load_dotenv()
token = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")
bot = commands.Bot(command_prefix="!")
song_queue = []
FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        'options': '-vn',
    }
YDL_OPTIONS = {
        'format': 'bestaudio/best',
        'extractaudio': True,
        'audioformat': 'mp3',
        'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
        'restrictfilenames': True,
        'noplaylist': True,
        'nocheckcertificate': True,
        'ignoreerrors': False,
        'logtostderr': False,
        'quiet': True,
        'no_warnings': True,
        'default_search': 'auto',
        'source_address': '0.0.0.0',
    }


# Busca el video en youtube y retorna la informacion de este
def search(arg):
    try: requests.get("".join(arg))
    except: arg = " ".join(arg)
    else: arg = "".join(arg)
    with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(f"ytsearch:{arg}", download=False)['entries'][0]
    return {'source': info['formats'][0]['url'], 'title': info['title'], "url": info["webpage_url"]}

# Reproduce siguiente cancion en la cola
def play_next(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)
    if len(song_queue) > 1:
        del song_queue[0]
        voice.play(discord.FFmpegPCMAudio(song_queue[0]["source"], **FFMPEG_OPTIONS), after=lambda e: play_next(ctx))
        voice.is_playing()


@bot.event
async def on_ready():
    guild = discord.utils.get(bot.guilds, name=GUILD)
    print(f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})')

#@bot.event
#async def on_command_error(ctx, error):
#    if isinstance(error, commands.errors.CommandNotFound):
#        await ctx.send('Este comando no existe')

# Hace que el bot se desconecte del canal
@bot.command(pass_context=True, aliases=['l', 'le', 'lea'])
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.disconnect()
    else:
        await ctx.send("No estoy en ni una wea")


@bot.command(name = "rule34")
async def rule34(ctx, *, tags: str):
    await ctx.channel.trigger_typing()
    try:
        data = requests.get(
            "https://rule34.xxx/index.php?page=post&s=list&tags={}".format(tags))
        fotitos = json.loads(data.content)
    except json.JSONDecodeError:
        await ctx.send(("nsfw.no_results_found", ctx).format(tags))
        return
    data = data.json()
    count = len(data)
    if count == 0:
        await ctx.send(("nsfw.no_results_found", ctx).format(tags))
        return
    image_count = 4
    if count < 4:
        image_count = count
    images = []
    for i in range(image_count):
        image = data[randint(0, count)]
        images.append("http://img.rule34.xxx/images/{}/{}".format(image["directory"], image["image"]))
    await ctx.send(("nsfw.results", ctx).format(image_count, count, tags, "\n".join(images)))


@bot.command(pass_context=True)
async def gif(ctx, *, search):
    colores = [discord.Colour.red(), discord.Colour.blue(), discord.Colour.magenta(), discord.Colour.purple(), discord.Colour.green()]
    indice = randint(0, 4)
    urls = []
    apikey = "VT5PX2WB13NC"  
    lmt = 30
    search = search.split(" ")
    search_term = "+".join(search)
    r = requests.get(
        "https://api.tenor.com/v1/search?q=%s&key=%s&limit=%s" % (search_term, apikey, lmt))
    if r.status_code <= 200:
        top_8gifs = json.loads(r.content)
        for element in top_8gifs["results"]:
            urls.append(element["url"])
        if len(urls) == 0:
            await ctx.send("No hay ni una wea")
            return
        index = randint(0, len(urls))
        await ctx.send(urls[index])
    else:
        await ctx.send("No hay gifs :c")


@bot.command(name="pene")
async def tegusta(ctx):
    await ctx.send("Te gusta?")


@bot.command(name="korone")
async def korone_mi_amor(ctx):
    gifs_korone = ["https://thumbs.gfycat.com/CraftyBlaringErmine-max-1mb.gif", "https://media1.tenor.com/images/3e24165b429f551fe7cb6340405a3ee1/tenor.gif?itemid=16826357", \
        "https://media1.tenor.com/images/300e0bcd5a05deacee8bc29a38397469/tenor.gif?itemid=17365827", "https://media1.tenor.com/images/dafab2245ecf6294b08de68cfacc9d36/tenor.gif?itemid=16215859",\
            "https://thumbs.gfycat.com/JoyousCreamyChafer-size_restricted.gif", "https://media1.tenor.com/images/7efc5533c31980289f2f5487c353d2b6/tenor.gif?itemid=16276160",\
                "https://user-images.strikinglycdn.com/res/hrscywv4p/image/upload/c_limit,fl_lossy,h_9000,w_1200,f_auto,q_60/1369026/368714_768061.gif", "https://media1.tenor.com/images/093e7879bac3390019d3f1dc72c43e88/tenor.gif?itemid=16657947", \
                    "https://i.imgur.com/31NjDYX.gif", "https://i.kym-cdn.com/photos/images/newsfeed/001/861/311/5a7.gif", "https://i.imgur.com/SUF35hs.jpg"]
    link = choice(gifs_korone)
    await ctx.send(f"Aprecia la belleza\n{link}")


@bot.command(name="griffith")
async def nada_malo(ctx):
    await ctx.send("La verdad \nhttps://image-cdn.neatoshop.com/styleimg/74380/none/darkgray/default/388391-20;1529751611u.jpg")


@bot.command(pass_context=True, aliases = ["p"])
async def play(ctx, *arg):
    channel = ctx.message.author.voice.channel

    if channel:
        voice = get(bot.voice_clients, guild=ctx.guild)
        song = search(arg)
        song_queue.append(song)
        url = song["url"]

        if voice and voice.is_connected():
            await voice.move_to(channel)
        else: 
            voice = await channel.connect()

        if not voice.is_playing():
            if len(song_queue) > 1:
                del song_queue[0]
            voice.play(discord.FFmpegPCMAudio(song_queue[0]['source'], **FFMPEG_OPTIONS), after=lambda e: play_next(ctx))
            voice.is_playing()
            await ctx.send(f"Reproduciendo:\n{url}")
        else:
            await ctx.send(f"Añadido a la cola\n{url}")
    else:
        await ctx.send("No estay en un canal!")


@bot.command(pass_context = True, aliases = ["q"])
async def queue(ctx):
    
    colores = [discord.Colour.red(), discord.Colour.blue(), discord.Colour.magenta(), discord.Colour.purple(), discord.Colour.green()]
    if len(song_queue) == 0:
        ctx.send(f"No hay cola")
    else:
        contenido = []
        for element in song_queue:
            contenido.append(element["title"])
        string = ""
        for i in range(0, len(contenido)):
            string += f"{i + 1}.- {contenido[i]}\n"
        indice = randint(0, len(colores))
        embed = discord.Embed(colour = colores[indice])
        embed.add_field(name = "Queue 🎵:", value = f"{string}")
        await ctx.send(content = None, embed = embed)


@bot.command(pass_contex = True)
async def skip(ctx):

    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)
    voice.stop()
    if len(song_queue) == 1:
        del song_queue[0]
        voice.stop()
    else:
        voice.stop()
        play_next(ctx)


@bot.command(pass_context = True)
async def hola(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
    if not voice.is_playing():
        voice.play(discord.FFmpegPCMAudio("audio\hola.mp3"))
        voice.is_playing()


@bot.command(pass_context = True)
async def bd(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
    if not voice.is_playing():
        voice.play(discord.FFmpegPCMAudio("audio\dias.mp3"))
        voice.is_playing()


@bot.command(pass_context = True)
async def FUBUKI(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
    if not voice.is_playing():
        voice.play(discord.FFmpegPCMAudio("audio\suki.mp3"))
        voice.volume = 2
        voice.is_playing()

@bot.command(pass_context = True)
async def boquita(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
    if not voice.is_playing():
        voice.play(discord.FFmpegPCMAudio("audio\koroneboquita.mp3"))
        voice.is_playing()


@bot.command(pass_context = True)
async def hm(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
    if not voice.is_playing():
        voice.play(discord.FFmpegPCMAudio("audio\hm.mp3"))
        voice.is_playing()


@bot.command(pass_context = True)
async def ahoy(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
    if not voice.is_playing():
        voice.play(discord.FFmpegPCMAudio("audio\marine.mp3"))
        voice.is_playing()


@bot.command(pass_context = True)
async def botan(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
    if not voice.is_playing():
        voice.play(discord.FFmpegPCMAudio("audio\shishiro.mp3"))
        voice.is_playing()


@bot.command(pass_context = True)
async def scatman(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)
    video = search("https://www.youtube.com/watch?v=Y1So82y91Yw")
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
    if not voice.is_playing():
        voice.play(discord.FFmpegPCMAudio(video["source"], **FFMPEG_OPTIONS))
        voice.is_playing()


@bot.command(pass_context = True)
async def yahallo(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)
    video = search("https://www.youtube.com/watch?v=jyijnQFn5lA")
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
    if not voice.is_playing():
        voice.play(discord.FFmpegPCMAudio(video["source"], **FFMPEG_OPTIONS))
        voice.is_playing()



@bot.command(pass_context = True)
async def speingo(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
    if not voice.is_playing():
        voice.play(discord.FFmpegPCMAudio("audio\speingo.mp3"))
        voice.is_playing()


@bot.command(pass_context = True)
async def patas(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
    if not voice.is_playing():
        voice.play(discord.FFmpegPCMAudio("audio\patas.mp3"))
        voice.is_playing()


@bot.command(name="stop")
async def stop(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)
    song_queue.clear()
    voice.stop()


@bot.command(name="cazuela")
async def cazuela(ctx):
    await ctx.send("Sendo maricon el cacas jaja, si o no gente?")


@bot.command(pass_context = True, aliases = ["fj"])
async def feliz_jueves(ctx):
    await ctx.send("https://cdn.discordapp.com/attachments/341395373581008896/731967502174912592/unknown.png")


@bot.command(name="gracias")
async def gracias(ctx):
    await ctx.send("https://cdn.discordapp.com/attachments/732421491223822381/732451754779738152/123125.png")


@bot.command(name="howgay")
async def howgay(ctx):
    embed = discord.Embed(colour = discord.Colour.magenta())
    numero = round(100 * random())
    embed.add_field(name = "Gay Rate", value=f"You are {numero}% gay 🏳️‍🌈")
    await ctx.send(content = None, embed = embed)


@bot.command(name="waifu")
async def waifu(ctx):
    embed = discord.Embed(colour = discord.Colour.purple())
    numero = round(100 * random())
    embed.add_field(name = "Waifu", value=f"You are {numero}% waifu")
    await ctx.send(content = None, embed = embed)


@bot.command(name="penis")
async def penis(ctx):
    embed = discord.Embed(colour = discord.Colour.blue())
    numero = randint(0, 10)
    wea = "=" * numero
    usuario = ctx.author.name
    embed.add_field(name = f"{usuario}'s Penis", value=f"8{wea}D")
    await ctx.send(content = None, embed = embed)


@bot.command(name="epicgamer")
async def epicgamer(ctx):
    embed = discord.Embed(colour = discord.Colour.green())
    numero = round(100 * random())
    embed.add_field(name = "Epic Gamer Rate", value=f"You are {numero}% Epic Gamer")
    await ctx.send(content = None, embed = embed)


@bot.command(name="hentai")
async def hentai(ctx):
    await ctx.send("https://quebolu.com/uploads/meme1475153656gen.jpg")


bot.run(token)
