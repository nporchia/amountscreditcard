from calendar import month
import nextcord as discord
from discord.ext import commands, tasks
from discord.utils import get
import asyncio
import random
import datetime
import pymongo
from pymongo import MongoClient
from datetime import timedelta
from dateutil.relativedelta import relativedelta


intents= discord.Intents.default()
intents.message_content = True
client = discord.Client()
client = commands.Bot(command_prefix = "!", intents =intents)

@client.event
async def on_ready():
    print('Me conecte con el nombre de {0.user}'.format(client))
    eliminarvencido.start()

@tasks.loop(hours=2)
async def eliminarvencido():
    cluster = pymongo.MongoClient("mongodb+srv://nporchi:PASSWORD@cluster0.wm8rg.mongodb.net/awardsbot?retryWrites=true&w=majority")
    db = cluster["awardsbot"]
    collection=db["tarj"]
    a=collection.find({})
    your_datetime = datetime.datetime.now()
    fechafin = your_datetime.strftime('%m-%Y')
    fechasplit=fechafin.split("-")
    meshoy=fechasplit[0]
    añohoy=fechasplit[1]
    for resultado in a:
        mes=resultado["Mesfin"]
        año=resultado["Añofin"]

        if meshoy>mes or añohoy>año:
            collection.delete_one({"Mesfin":mes})

@client.command()
async def pago(ctx):
    await ctx.send("Nombre de la operacion")
    nombre=await client.wait_for("message")
    nombre=nombre.content

    await ctx.send("Tarjeta VISA 1 Mastercard 2")
    tarjeta=await client.wait_for("message")
    tarjeta=int(tarjeta.content)

    await ctx.send("Monto $")
    monto=await client.wait_for("message")
    monto=int(monto.content)

    await ctx.send("Cuotas")
    cuotas=await client.wait_for("message")
    cuotas=int(cuotas.content)


    cluster = pymongo.MongoClient("mongodb+srv://nporchi:PASSWORD@cluster0.wm8rg.mongodb.net/awardsbot?retryWrites=true&w=majority")
    db = cluster["awardsbot"]
    collection=db["tarj"]
    your_datetime = datetime.datetime.now()
    your_datetime + relativedelta(months=cuotas) 
    fechafin = your_datetime.strftime('%m-%Y')
    fecha=fechafin.split("-")
    mes=fecha[0]
    año=fecha[1]
    valorcuota=monto/cuotas
    mydict ={"Producto":nombre,"Monto":monto,"Tarjeta":tarjeta,"Cuotas":cuotas,"Mesfin":mes,"Añofin":año,"Valorcuota":valorcuota}
    collection.insert_one(mydict)
    embed= discord.Embed(
        title='Tarjeta Master',
        colour=discord.Colour.from_rgb(255,0,130)
    )
    embed.add_field(name='Nombre',value=nombre)
    embed.add_field(name='Monto',value=monto)
    if tarjeta==1:
        tarjeta="Visa"
    elif tarjeta==2:
        tarjeta="Mastercard"
    embed.add_field(name='Tarjeta',value=tarjeta)
    embed.add_field(name='Cuotas',value=cuotas)
    embed.add_field(name='Mesfin',value=mes)
    embed.add_field(name='Añofin',value=año)
    embed.add_field(name='Valorcuota',value=valorcuota)
    embed.set_author(name="Cuotasbot",icon_url="https://i.blogs.es/b3a45a/dineroefectivo/1366_2000.jpg")
    await ctx.send(embed=embed)
    

@client.command()
async def platavisa(ctx):
    cluster = pymongo.MongoClient("mongodb+srv://nporchi:PASSWORD@cluster0.wm8rg.mongodb.net/awardsbot?retryWrites=true&w=majority")
    db = cluster["awardsbot"]
    collection=db["tarj"]
    a=collection.find({"Tarjeta":1})
    embed= discord.Embed(
        title='Tarjeta Visa',
        colour=discord.Colour.from_rgb(255,0,130)
    )
    contador=0
    pagos= ""
    for pago in a:
        nombre=pago["Producto"]
        cuotas=pago["Cuotas"]
        monto=pago["Monto"]
        valorcuota=pago["Valorcuota"]
        mesfin=pago["Mesfin"]
        añofin=pago["Añofin"]
        pagito=f"```Nombre:{nombre} Cuotas:{cuotas} Monto Total:{monto}  Valor Cuota:{valorcuota} Mes y año fin:{mesfin}{añofin}```"
        await ctx.send(pagito)
        contador=contador+pago["Valorcuota"]
    contador=int(contador)
    embed.add_field(name='Monto total',value=contador)
    embed.set_author(name="Cuotasbot",icon_url="https://seranoticia.com/wp-content/uploads/2019/01/visa.jpg")
    await ctx.send(embed=embed)

@client.command()
async def platamaster(ctx):
    cluster = pymongo.MongoClient("mongodb+srv://nporchi:PASSWORD@cluster0.wm8rg.mongodb.net/awardsbot?retryWrites=true&w=majority")
    db = cluster["awardsbot"]
    collection=db["tarj"]
    a=collection.find({"Tarjeta":2})
    embed= discord.Embed(
        title='Tarjeta Master',
        colour=discord.Colour.from_rgb(255,0,130)
    )
    contador=0
    pagos= ""
    for pago in a:
        nombre=pago["Producto"]
        cuotas=pago["Cuotas"]
        monto=pago["Monto"]
        valorcuota=pago["Valorcuota"]
        mesfin=pago["Mesfin"]
        añofin=pago["Añofin"]
        pagito=f"```Nombre:{nombre} Cuotas:{cuotas} Monto Total:{monto}  Valor Cuota:{valorcuota} Mes y año fin:{mesfin}{añofin}```"
        await ctx.send(pagito)
        contador=contador+pago["Valorcuota"]
    contador=int(contador)
    embed.add_field(name='Monto total',value=contador)
    embed.set_author(name="Cuotasbot",icon_url="https://play-lh.googleusercontent.com/jMECkIn97zzMi1IoWlb9SYjtbYolSPmgdLmylwIwo3pbhQ_omkRMzM0bS-PnN461hg")
    await ctx.send(embed=embed)

client.run()