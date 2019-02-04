#version 0.21

import discord
import sys
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
    if message.channel.is_private:
        logging.info("Ignoring direct message. :P")
        # ignore DMs
        return
    
    if message.content == "cleanse":
        # purge non-emoji messages
        logging.info("Cleansing... >-<")

        await client.delete_message(message)
        
        messagescleansed = 0
        reactionscleansed = 0

        async for message in client.logs_from(message.channel):
            if (not isvalid(message.content)) or message.embeds:
                await client.delete_message(message)
                messagescleansed += 1
                continue
            for reaction in message.reactions:
                #is this really the way to mass-remove specific reactions? it seems kind of bad
                if reaction.custom_emoji or not isvalid(reaction.emoji):
                    print(client.get_reaction_users(reaction))
                    for user in await client.get_reaction_users(reaction):
                        await client.remove_reaction(message, reaction.emoji, user)
                    reactionscleansed += 1

        logging.info("Done cleansing! :3\n  Messages deleted: {}\n  Reactions deleted: {}".format(messagescleansed, reactionscleansed))
        return
    
    if (not isvalid(message.content)) or message.embeds:
        # delete non-emoji messages
        logging.info("Invalid message! Deleting! >.<")
        logging.debug(message.content)
        await client.delete_message(message)

@client.event
async def on_message_edit(_, message): #we don't care about the before-message
    if message.channel.is_private:
        logging.info("Ignoring direct message edit. :P")
        # ignore DMs
        return
    if (not isvalid(message.content)) or message.embeds:
        logging.info("Invalid message edit! Deleting! >.<")
        logging.debug(message.content)
        await client.delete_message(message)

@client.event
async def on_reaction_add(reaction, user):
    #basically, no nitro reactions and no regional indicator reactions.
    if reaction.message.channel.is_private:
        logging.info("Ignoring direct message reaction. :P")
        # ignore DMs
        return
    logging.debug("Reaction added!")
    if reaction.custom_emoji or not isvalid(reaction.emoji):
        logging.info("That was a bad reaction! Removing...! >.<")
        logging.info(reaction.emoji)
        await client.remove_reaction(reaction.message, reaction.emoji, user)



@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('--------')

client.run(TOKEN)
