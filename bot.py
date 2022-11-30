import interactions
import random
import requests
import json
import secrets

bot = interactions.Client(token=secrets.bot_token)
api_key = secrets.weather_token
base_url = "http://api.openweathermap.org/data/2.5/weather?"

@bot.command(name="randomnumber", description="Get a random number by providing an upper limit")
@interactions.option()
async def randomnumber(ctx: interactions.CommandContext, limit: int):
    await ctx.send(f"{random.randint(1, limit)}")

@bot.command(name="forecast", description="Gets weather report for the chosen city using openweather api")
@interactions.option()
async def forecast(ctx: interactions.CommandContext, city: str):
    city_name = city
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name
    response = requests.get(complete_url)
    print(response)
    weatherdict = response.json()
    print(weatherdict)
    current_temperature = weatherdict["main"]["temp"]
    current_temperature_celsiuis = str(round(current_temperature - 273.15))
    weather_description = weatherdict["weather"][0]["description"]
    embed = interactions.Embed(title=f"Current weather in {city_name}")
    embed.add_field(name="Weather Description:", value=f"**{weather_description}**", inline=False)
    embed.add_field(name="Temperature(°C)", value=f"**{current_temperature_celsiuis}°C**", inline=False)
    embed.set_footer(text=f"Requested by {ctx.author.name}")
    await ctx.send(embeds=embed)

@bot.command(name='userimage', description="Grab's the profile picture of the chosen user")
@interactions.option()
async def userimage(ctx: interactions.CommandContext, username:interactions.Member):
    embed = interactions.Embed(title=f"{username.name}'s Profile Picture")
    embed.set_image(username.user.avatar_url)
    embed.add_field(name="Profile Picture URL", value=f"{username.user.avatar_url}", inline=False)
    await ctx.send(embeds=embed)

@bot.command(name='sourcecode', description='Provides source code for this bot')
async def sourcecode(ctx: interactions.CommandContext):
    embed = interactions.Embed(title='Source code for penguin bot')
    embed.add_field(name='Github Repository:', value='https://github.com/conrad-mo/penguin-bot', inline=False)
    await ctx.send(embeds=embed)

bot.start()