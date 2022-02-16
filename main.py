import discord
from discord.client import Client
from discord.ext import commands, tasks
import json
import asyncio
import time
import random

client = commands.Bot(command_prefix=commands.when_mentioned_or("!"), case_insensitive=True,
    allowed_mentions=discord.AllowedMentions(everyone=True), intents=discord.Intents.all(),
    help_command=None)

filename = 'main.json'
filename2= 'users.json'

@client.event
async def on_ready():
    
    global data
    with open(filename, "r") as file:
        data = json.load(file)

    global data2
    with open(filename2, "r") as file:
        data2 = json.load(file)

    check_time.start()

    await client.wait_until_ready()
    await client.change_presence(activity=discord.Game(name="!help - Wordle (" + str(len(client.guilds)) + ")"))
    print(f"Bot Running as {client.user}")


async def create_profile(ctx):
    data2[f'{ctx.author.id}'] = {"timesplayed":0, "correctguesses":0, "incorrectguesses":0, "completed": False, "guess1":None, "guess2":None, "guess3":None, "guess4":None, "guess5":None}
    with open(filename2, "w") as file:
        json.dump(data2,file, indent=2)
    

async def emotes(guess):
    word = ""
    for i in guess:
        if i == "a":
            word = word + ("<:regional_indicator_a:943333399286911058>")
        if i == "b":
            word = word + ("<:regional_indicator_b:943333399286911058>")
        if i == "c":
            word = word + ("<:regional_indicator_c:943333399286911058>")
        if i == "d":
            word = word + ("<:regional_indicator_d:943333399286911058>")
        if i == "e":
            word = word + ("<:regional_indicator_e:943333399286911058>")
        if i == "f":
            word = word + ("<:regional_indicator_f:943333399286911058>")
        if i == "g":
            word = word + ("<:regional_indicator_g:943333399286911058>")
        if i == "h":
            word = word + ("<:regional_indicator_h:943333399286911058>")
        if i == "i":
            word = word + ("<:regional_indicator_i:943333399286911058>")
        if i == "j":
            word = word + ("<:regional_indicator_j:943333399286911058>")
        if i == "k":
            word = word + ("<:regional_indicator_k:943333399286911058>")
        if i == "l":
            word = word + ("<:regional_indicator_l:943333399286911058>")
        if i == "m":
            word = word + ("<:regional_indicator_m:943333399286911058>")
        if i == "n":
            word = word + ("<:regional_indicator_n:943333399286911058>")
        if i == "o":
            word = word + ("<:regional_indicator_o:943333399286911058>")
        if i == "p":
            word = word + ("<:regional_indicator_p:943333399286911058>")
        if i == "q":
            word = word + ("<:regional_indicator_q:943333399286911058>")
        if i == "r":
            word = word + ("<:regional_indicator_r:943333399286911058>")
        if i == "s":
            word = word + ("<:regional_indicator_s:943333399286911058>")
        if i == "t":
            word = word + ("<:regional_indicator_t:943333399286911058>")
        if i == "u":
            word = word + ("<:regional_indicator_u:943333399286911058>")
        if i == "v":
            word = word + ("<:regional_indicator_v:943333399286911058>")
        if i == "w":
            word = word + ("<:regional_indicator_w:943333399286911058>")
        if i == "x":
            word = word + ("<:regional_indicator_x:943333399286911058>")
        if i == "y":
            word = word + ("<:regional_indicator_y:943333399286911058>")
        if i == "z":
            word = word + ("<:regional_indicator_z:943333399286911058>")

    print(word)
    return(word)


@tasks.loop(seconds=60)
async def check_time():
    if data["time"] < time.time() - 86400:
        amount = len(data["possiblewords"])
        number = random.randint(0, amount)
        word = data["possiblewords"][number-1]
        data["word"] = word
        data["time"] = time.time()

        
        with open(filename, "w") as file:
            json.dump(data,file, indent=2)

        print(f"Todays word is {word}")

    else:
        print("not time")
        

@client.command()
async def guess(ctx, word=None):
    if str(ctx.author.id) not in data2:
        await create_profile(ctx)

    try:
        word = str(word).lower()
    except ValueError:
        await ctx.reply("Error")
    print(word)

    if len(word) == 5:
        if data2[f'{ctx.author.id}']["completed"] == False:
            if word in data["wordlist"]:
                if data2[f'{ctx.author.id}']["guess5"] != None:
                    await ctx.reply("You have already played the game!")
                else:
                    if data2[f'{ctx.author.id}']["guess1"] == None:
                        data2[f'{ctx.author.id}']["guess1"] = word
                    elif data2[f'{ctx.author.id}']["guess2"] == None:
                        data2[f'{ctx.author.id}']["guess2"] = word
                    elif data2[f'{ctx.author.id}']["guess3"] == None:
                        data2[f'{ctx.author.id}']["guess3"] = word
                    elif data2[f'{ctx.author.id}']["guess4"] == None:
                        data2[f'{ctx.author.id}']["guess4"] = word
                    elif data2[f'{ctx.author.id}']["guess5"] == None:
                        data2[f'{ctx.author.id}']["guess5"] = word
                    


                    if word == data["word"]:
                        await ctx.reply("You got the word!")
                        data2[f'{ctx.author.id}']["correctguesses"] += 1
                        data2[f'{ctx.author.id}']["completed"] = True

                        guess1 = data2[f'{ctx.author.id}']["guess1"]
                        guess2 = data2[f'{ctx.author.id}']["guess2"]
                        guess3 = data2[f'{ctx.author.id}']["guess3"]
                        guess4 = data2[f'{ctx.author.id}']["guess4"]
                        guess5 = data2[f'{ctx.author.id}']["guess5"]
                        square = "<:black_large_square:943336927367684167>"
                        if guess1 != None:
                            word1 = await emotes(guess1)
                        else:
                            word1 = square + square + square + square + square

                        if guess2 != None:
                            word2 = await emotes(guess2)
                        else:
                            word2 = square + square + square + square + square

                        if guess3 != None:
                            word3 = await emotes(guess3)
                        else:
                            word3 = square + square + square + square + square

                        if guess4 != None:
                            word4 = await emotes(guess4)
                        else:
                            word4 = square + square + square + square + square

                        if guess5 != None:
                            word5 = await emotes(guess5)
                        else:
                            word5 = square + square + square + square + square



                        embedVar = discord.Embed(title="Wordle | Info", description=f"Your Guesses; \n{word1}\n{word2}\n{word3}\n{word4}\n{word5}", color=0xfbff00, timestamp=ctx.message.created_at)
                        embedVar.set_footer(text=f"Wordle")
                        embedVar.set_thumbnail(url=ctx.author.avatar_url)       
                        await ctx.send(embed=embedVar)




                    else:
                        await ctx.reply("Your guess is incorrect!")
                        if data2[f'{ctx.author.id}']["guess5"] != None:
                            data2[f'{ctx.author.id}']["incorrectguesses"] += 1
                            data2[f'{ctx.author.id}']["completed"] = True

                        guess1 = data2[f'{ctx.author.id}']["guess1"]
                        guess2 = data2[f'{ctx.author.id}']["guess2"]
                        guess3 = data2[f'{ctx.author.id}']["guess3"]
                        guess4 = data2[f'{ctx.author.id}']["guess4"]
                        guess5 = data2[f'{ctx.author.id}']["guess5"]
                        square = "<:black_large_square:943336927367684167>"
                        if guess1 != None:
                            word1 = await emotes(guess1)
                        else:
                            word1 = square + square + square + square + square

                        if guess2 != None:
                            word2 = await emotes(guess2)
                        else:
                            word2 = square + square + square + square + square

                        if guess3 != None:
                            word3 = await emotes(guess3)
                        else:
                            word3 = square + square + square + square + square

                        if guess4 != None:
                            word4 = await emotes(guess4)
                        else:
                            word4 = square + square + square + square + square

                        if guess5 != None:
                            word5 = await emotes(guess5)
                        else:
                            word5 = square + square + square + square + square



                        embedVar = discord.Embed(title="Wordle | Info", description=f"Your Guesses; \n{word1}\n{word2}\n{word3}\n{word4}\n{word5}", color=0xfbff00, timestamp=ctx.message.created_at)
                        embedVar.set_footer(text=f"Wordle")
                        embedVar.set_thumbnail(url=ctx.author.avatar_url)       
                        await ctx.send(embed=embedVar)
                    with open(filename2, "w") as file:
                        json.dump(data2,file, indent=2)
        

            else:
                await ctx.reply("That word is not in the word list!")
        else:
            await ctx.reply("You have already completed todays game!")
    else:
        await ctx.reply("Your guess has to be 5 characters!")
        
@client.command()
async def info(ctx):
    if str(ctx.author.id) not in data2:
        await create_profile(ctx)
    

    guess1 = data2[f'{ctx.author.id}']["guess1"]
    guess2 = data2[f'{ctx.author.id}']["guess2"]
    guess3 = data2[f'{ctx.author.id}']["guess3"]
    guess4 = data2[f'{ctx.author.id}']["guess4"]
    guess5 = data2[f'{ctx.author.id}']["guess5"]
    square = "<:black_large_square:943336927367684167>"
    if guess1 != None:
        word1 = await emotes(guess1)
    else:
        word1 = square + square + square + square + square

    if guess2 != None:
        word2 = await emotes(guess2)
    else:
        word2 = square + square + square + square + square

    if guess3 != None:
        word3 = await emotes(guess3)
    else:
        word3 = square + square + square + square + square

    if guess4 != None:
        word4 = await emotes(guess4)
    else:
        word4 = square + square + square + square + square

    if guess5 != None:
        word5 = await emotes(guess5)
    else:
        word5 = square + square + square + square + square

    completed = data2[f'{ctx.author.id}']["timesplayed"]
    wins = data2[f'{ctx.author.id}']["correctguesses"]
    losses = data2[f'{ctx.author.id}']["incorrectguesses"]

    embedVar = discord.Embed(title="Wordle | Info", description=f"Your Guesses; \n{word1}\n{word2}\n{word3}\n{word4}\n{word5}\n\n<:joystick:943332198893883434>**Game Stats**" + 
    f" \nPlayed Games: {completed}\nWins: {wins}\nLosses: {losses}", color=0xfbff00, timestamp=ctx.message.created_at)
    embedVar.set_footer(text=f"Wordle")
    embedVar.set_thumbnail(url=ctx.author.avatar_url)       
    await ctx.send(embed=embedVar)


@client.group(invoke_without_command=True, case_insensitive=True)
async def help(ctx):
    embedVar = discord.Embed(title="Wordle | Help :bar_chart:", description=f"!quess <word> - Guess a word!", color=0xfbff00, timestamp=ctx.message.created_at)
    embedVar.set_footer(text=f"Wordle")
    embedVar.set_thumbnail(url=ctx.author.avatar_url)       
    await ctx.send(embed=embedVar)



loop = asyncio.get_event_loop()
loop.set_debug(True)
loop.create_task(client.start("OTQzMzE3NDkzNTAwNDk3OTUz.YgxS4A.qdYYfgPx8MROKDdsLVkOgQFHnnc"))
loop.run_forever()
