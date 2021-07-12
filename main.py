import keepalive
#No touch above
from discord.ext import commands
import time,calendar,os,json,discord,requests
from fuzzywuzzy import fuzz
activators=['->tb ','->tb']
client = commands.Bot(command_prefix=activators)
traindex = []

#Commenting in progress
#Contact me on discord at Nurglwe#8387 if you want 


'''
BELOW IS EVENTS
'''


@client.event
async def on_ready():
  print("Ready")
  #Makes testing over and over easier
  no = len(client.guilds)
  await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=" trains in {} servers || prefix is ->tb ||".format(no)))
  guild=discord.utils.get(client.guilds,id=int(os.getenv("GUILD")))
  channel=discord.utils.get(guild.channels,id=int(os.getenv("DELC")))
  guilds=[i.name for i in client.guilds]
  await channel.send("Ready and in: \n"+str(guilds))


'''
BELOW IS FOR COMMANDS
'''

@client.command(brief="Invite me to your server!")
async def invite (ctx):
  await ctx.channel.send('https://discord.com/api/oauth2/authorize?client_id=856117195162910740&permissions=52224&scope=bot')


#intended to be main attraction
@client.command(brief="Call a train from the Traindex!",aliases=['Traindex'])
async def traindex(ctx, *args):
  train = ' '.join(args)
  train=train.lower()
  with open('traindex.csv') as f:
    traindexs = f.read().splitlines()
  values = []
  trains = []
  for line in traindexs:
    traincontents = line.split(',')
    sim = fuzz.ratio(train, traincontents[0]) #fuzzy words to help finds similar trains
    if sim >= 90:
      if traincontents[4] == '':
        traincontents[4] ='https://media.discordapp.net/attachments/615271081514893324/793798996846051378/Image_not_found.png'
    #finds picture, if none then it will replace it with a normal photo (helps bc I don't have to worry about finding a photo for now)
      embed = discord.Embed(title="Traindex", color=0x0c1a96)
      embed.add_field(name="Name:", value =traincontents[0].capitalize())
      embed.add_field(name = "Power type:", value = traincontents[1] )
      embed.add_field(name = "Power:", value = traincontents [2])
      embed.add_field(name= "Dimensions (M) Length-Width-Height: ", value = traincontents[3])
      embed.set_image(url=traincontents[4])
      embed.set_footer(text = "Trains are sacred", icon_url = "https://media.discordapp.net/attachments/739458979381379072/752158619428061244/IMG_0063.JPG?width=624&height=468")
      await ctx.channel.send(embed=embed)
      return  
    values.append(sim)
    trains.append(traincontents[0])
  top3 = list(sorted(zip(values, trains), reverse=True))[:3]
  embed=discord.Embed(title='Error: Train not found', colour = 0x990000)
  embed.add_field(name='Oops',value = 'The number is the % match to your requested train and name of that train')
  embed.add_field(name='Sorry, the train was not found, possible trains you requested could be:',value = top3[0],inline= False)
  embed.add_field(name='Train 2', value =top3[1],inline=False)
  embed.add_field(name='Train 3',value = top3[2],inline= False)
  await ctx.channel.send(embed=embed)

  
@client.command(brief="Gets the response time of the bot!")
async def ping(ctx):
    await ctx.send('Pong, {} Ms'.format(round(client.latency * 1000,2)))

@client.command(brief="Call someone a spanner")
async def spanner(ctx,user:discord.User):
  #Sort of an insult, but sort of train related...
  e = 'https://media1.tenor.com/images/e01b325c047d38e4968b17a52aae0186/tenor.gif?itemid=5148623'
  e=str(e)
  await ctx.channel.send('<@{}> is an absolute spanner'.format(user.id))
  embed=discord.Embed(title="You spanner!")
  embed.set_image(url=e)
  await ctx.channel.send(embed=embed)

@client.command(brief='Tells me to leave the server')
async def leave(ctx):
  if ctx.author.id == int(os.getenv("ME")):
    try:
      guild=discord.utils.get(client.guilds,id=ctx.message.guild.id)
      print(guild)
      await guild.leave()
    except:
      await ctx.channel.send("Error, guild not found")
  else:
    await ctx.channel.send("Error, insufficient permissions (Only <@{}> can use the leave command)".format(int(os.getenv("ME"))))

@client.command(brief="About me",aliases=["about"])
async def info(ctx):
  embed=discord.Embed(title="About me!",colour=discord.Colour(0x990033))
  me= ctx.message.guild.get_member(int(os.getenv("ME")))
  botid=ctx.message.guild.get_member(int(os.getenv("BOTID")))
  embed.set_author(name="Developer", url="https://discordapp.com/users/{}".format(int(os.getenv("ME"))), icon_url=me.avatar_url)
  embed.add_field(name="Owner:",value="Nurglwe#8387")
  await ctx.channel.send(embed=embed)


keepalive.keep_alive()



token=os.getenv("TOKEN")    
client.run(token)

