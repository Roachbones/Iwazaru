#version 1.0

import discord
import logging

logging.basicConfig(level=logging.INFO)

client = discord.Client()

with open("token.txt", "r", encoding="utf-8") as opened:
    TOKEN = opened.read().strip()
with open("emojisurrogates.txt", "r", encoding="utf-8") as opened:
    EMOJISURROGATES = [i.strip() for i in opened.readlines()]
    #note: this might be harsh to regional pairs who lack ZWJs
    #they are supposed to be ZWJed but i think sometimes they aren't
with open("emojinames.txt", "r", encoding="utf-8") as opened:
    EMOJINAMES = [":"+i.strip()+":" for i in opened.readlines()]
BONUSCHARS = [" ", "\n"]

MORPHEMES = EMOJISURROGATES + EMOJINAMES + BONUSCHARS

def isvalid(text): #it's a tree! it's recursion! it's beautiful!
    """Check if text is a valid emoji message (can be composed of substrings in MORPHEMES)."""
    if text == "":
        return True
    for m in MORPHEMES:
        if text.startswith(m):
            if isvalid(text[len(m):]):
                return True
    return False

@client.event
async def on_message(message):
    if not (message.guild and message.channel.permissions_for(message.guild.me).manage_messages):
        logging.info("Ignoring message in restricted channel. u_u")
        return
    
    if message.content == "cleanse":
        # purge non-emoji messages
        logging.info("Cleansing... >-<")

        await message.delete()
        
        messagescleansed = 0
        reactionscleansed = 0

        async for message in message.channel.history():
            if (not isvalid(message.content)) or message.embeds:
                await message.delete()
                messagescleansed += 1
                continue
            for reaction in message.reactions:
                #is this really the way to mass-remove specific reactions? it seems kind of bad
                if reaction.custom_emoji or not isvalid(reaction.emoji):
                    for user in await reaction.users().flatten():
                        await reaction.remove(user)
                    reactionscleansed += 1

        logging.info("Done cleansing! :3\n  Messages deleted: {}\n  Reactions deleted: {}".format(messagescleansed, reactionscleansed))
        return
    
    if (not isvalid(message.content)) or message.embeds:
        # delete non-emoji messages
        logging.info("Invalid message! Deleting! >.<")
        logging.debug(message.content)
        await message.delete()

@client.event
async def on_message_edit(_, message): #we don't care about the before-message
    if not (message.guild and message.channel.permissions_for(message.guild.me).manage_messages):
        logging.info("Ignoring message edit in restricted channel. u_u")
        # ignore DMs
        return
    if (not isvalid(message.content)) or message.embeds:
        logging.info("Invalid message edit! Deleting! >.<")
        logging.debug(message.content)
        await message.delete()

@client.event
async def on_reaction_add(reaction, user):
    #basically, no nitro reactions and no regional indicator reactions.
    logging.debug("Reaction added!")
    if not (reaction.message.guild and reaction.message.channel.permissions_for(reaction.message.guild.me).manage_messages):
        logging.info("Ignoring reaction in restricted channel. u_u")
        # ignore DMs
        return
    if reaction.custom_emoji or not isvalid(reaction.emoji):
        logging.info("That was a bad reaction! Removing...! >.<")
        logging.info(reaction.emoji)
        await reaction.remove(user)

@client.event
async def on_ready():
    logging.info('Logged in as')
    logging.info(client.user.name)
    logging.info(client.user.id)
    logging.info('--------')

client.run(TOKEN)