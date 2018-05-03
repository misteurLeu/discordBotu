# -*- coding: utf-8  -*-

# A lire si vous faîtes une mise à jour et si vous avez ajouté ou modifié les commandes du bot :
# 1) Copiez vos commandes (pas les commandes par défaut) que vous avez créer dans votre ancienne version dans la nouvelle version.
# 2) Si vous avez modifié une commande de NextBot par défaut, supprimez la commande de la nouvelle version puis copiez le code de la commande de l'ancienne version dans la nouvelle version.

import asyncio, discord, os

user_bot = "LouveBot"  # Mettez dans cette variable le pseudo du bot.
token = os.environ['BOT_TOKEN']  # Mettez dans cette variable le token du bot
trust = os.environ['TRUST_USER'].split(',')  # admins du bot
ranks = False
f = open('streamers.txt', 'w+', encoding='utf-8')
streamers = f.read().split("\n")
f.close()

client = discord.Client()
ver = "1.0.0"
lang = "fr"

print("LouveBot " + ver + " " + lang)


@client.event
@asyncio.coroutine
def on_member_update(before, after):
    streamChannel = [chan for chan in after.server.channels if chan.id == "405352007302643712"][0]
    if after.game is not None and after.game.url is not None:
        if str(after).split('#')[1] in streamers and 'twitch.tv' in after.game.url:
            yield from client.send_message(streamChannel, str(after).split('#')[0] + ' est en live GOGOGOGO :\n' + str(
                after.game) + ' ' + after.game.url)


@client.event
@asyncio.coroutine
def on_message(message):
    rep = text = msg = message.content
    rep2 = text2 = msg2 = rep.split()
    user = str(message.author)
    trusted = user in trust
    try:
        memberList = ['#' + member.discriminator for member in message.server.members]
        server_msg = str(message.channel.server)
        chan_msg = str(message.channel.name)
        membersName = [str(member.name) + '#' + str(member.discriminator) for member in message.server.members]
        pm = False
    except AttributeError:
        server_msg = user
        chan_msg = user
        pm = True
    try:
        command = rep2[0].lower()
        params = rep2[0:]
    except IndexError:
        command = ""
        params = ""

    print(user + " (" + server_msg + ") [" + chan_msg + "] : " + rep)

    if ranks and not pm:
        open("msgs_user_" + server_msg + ".txt", "a").close()
        msgs = open("msgs_user_" + server_msg + ".txt", "r")
        msgs_r = msgs.read()
        if user not in msgs_r:
            msgs_w = open("msgs_user_" + server_msg + ".txt", "a")
            msgs_w.write(user + ":0\n")
            msgs_w.close()
            msgs.close()
            msgs = open("msgs_user_" + server_msg + ".txt", "r")
            msgs_r = msgs.read()
        msgs_user = msgs_r.split(user + ":")[1]
        msgs.close()
        user_msgs_n = int(msgs_user.split("\n")[0])
        user_msgs_n += 1
        msgs_r = msgs_r.replace(user + ":" + str(user_msgs_n - 1), user + ":" + str(user_msgs_n))
        msgs = open("msgs_user_" + server_msg + ".txt", "w")
        msgs.write(msgs_r)
        msgs.close()

    # Début des commandes

    if command == "!members_list":
            yield from client.send_message(message.channel, '\n'.join(membersName))

    if command == "!test":
        yield from client.send_message(message.channel, user)
        yield from client.send_message(message.channel, trust)

    if command == "!whereami":
        yield from client.send_message(message.channel, message.server)
        yield from client.send_message(message.channel, message.channel.id)

    if command == "!commandtest":  # Copiez ce code pour créer une commande
        yield from client.send_message(message.channel, "Texte à envoyer.")

    if command == "!saymyname":  # Copiez ce code pour créer une commande
        yield from client.send_message(message.channel, user)

    if command == "!ban" and trusted and not pm:  # Cette commande sert à bannir un utilisateur, and trusted veux dire que la commande est restreinte et que seuls les utilisateurs en trust peuvent utiliser la commande et and not pm veux dire que la commande n'est pas utilisable en PM.
        id_user = message.server.get_member_named(params[
                                                      1])  # La variable params[1] est le premier paramètre entré par l'utilisateur, cette ligne sert à donner l'identifiant de l'utilisateur à partir du pseudo. Pour avoir l'identifiant d'un utilisateur, un serveur ou d'autre chose, vous devez activer le mode développeur
        try:
            yield from client.ban(id_user, int(params[
                                                   2]))  # cette ligne sert à bannir l'utilisateur grâce à la variable id_user qui représente l'identifiant de l'utilisateur à bannir
        except IndexError:  # si le nombre de messages à supprimer n'est pas mis (en tapant juste !ban utilisateur), le bot bannira l'utilisateur mais ne supprimera aucun message
            yield from client.ban(id_user, 0)

    if command == "!google":  # Voir la commande !bing
        yield from client.send_message(message.channel, "https://www.google.com/#q=" + "+".join(params[1:]))

    if command == "!kick" and trusted and not pm:  # Voir la commande !ban
        id_user = message.server.get_member_named(params[1])
        yield from client.kick(id_user)

    if (
            command == "!purge" or command == "!clear") and trusted and not pm:  # Cette commande sert à effacer les messages, en tapant !purge 10, le bot supprimera les 10 derniers messages.
        yield from client.purge_from(message.channel, limit=int(params[
                                                                    1]))  # Cette ligne sert à supprimer les messages avec params[1] qui est le premier paramètre (le nombre de messages), il y a int(params[1]) car le paramètre doit être converti en un nombre.

    if (command == "!quit" or command == "!exit") and trusted:  # Cette commande sert à fermer le bot
        yield from client.close()

    if command == "!role_user_add" and trusted and not pm:  # Cette commande sert à ajouter un rôle à un utilisateur
        member = message.server.get_member_named(params[1])
        role = discord.utils.get(message.server.roles, name=" ".join(params[
                                                                     2:]))  # cette ligne sert à récupérer le rôle de l'utilisateur à ajouter, " ".join(params[2:]) est le nom du rôle
        yield from client.add_roles(member,
                                    role)  # cette ligne sert à appliquer l'ajout du rôle à l'utilisateur et member est l'identifiant de l'utilisateur et role est l'identifiant du rôle

    if command == "!role_user_remove" and trusted and not pm:  # Cette commande sert à retirer un rôle à un utilisateur
        member = message.server.get_member_named(params[1])
        role = discord.utils.get(message.server.roles, name=" ".join(params[2:]))
        yield from client.remove_roles(member,
                                       role)  # cette ligne sert à retirer le rôle d'un utilisateur, son fonctionnement est quasi-identique à part qu'elle fait l'inverse (elle retire le rôle au lieu de l'ajouter)

    if command == "!roles" and trusted and not pm:  # Cette commande sert à lister les rôles sur le serveur
        for role in message.server.roles:  # cette ligne est une boucle et sert à mettre dans la variable role la liste des rôles du serveur avec message.server.roles
            yield from client.send_message(message.channel, role.id + " : " + role.name)

    if command == "!unban" and trusted and not pm:  # Cette commande sert à débannir un utilisateur
        id_user = message.server.get_member_named(params[1])
        yield from client.unban(message.server,
                                id_user)  # pour débannir un utilisateur, il faut l'identifiant du serveur avec message.serveur et l'identifiant de l'utilisateur (voir !ban)

    if command == "!say" and trusted:  # Cette commande sert à envoyer un message sur un channel du serveur, le paramètre 1 doit être l'identifiant du channel et après, on doit mettre le message (exemple : !say 1234567890 Bonjour !)
        yield from client.send_message(client.get_channel(params[1]), " ".join(params[2:]))

    if command == "!say_user" and trusted:
        if params[2].lower() == params[2].upper():
            yield from client.send_message(client.get_server(params[1]).get_member(params[2]), " ".join(params[3:]))
        else:
            yield from client.send_message(client.get_server(params[1]).get_member_named(params[2]),
                                           " ".join(params[3:]))

    if command == "!ver":  # Cette commande envoit la version du bot.
        yield from client.send_message(message.channel, "NextBot " + ver + " " + lang)

    if command == "!streamadd" and trusted:
        if len(params) == 1:
            yield from client.send_message(message.channel, "utilisation: !streamadd + #usertag")
        for userToAdd in params[1:]:
            if userToAdd not in streamers and userToAdd in memberList:
                f2 = open('streamers.txt', 'a', encoding='utf-8')
                f2.write(userToAdd + "\n")
                f2.close()
                streamers.append(userToAdd)
                yield from client.send_message(message.channel,
                                               userToAdd + " a bien été ajouté a la liste des streams a afficher")
            elif userToAdd in memberList:
                yield from client.send_message(message.channel,
                                               userToAdd + " fais déjàs partie de la liste des streams a afficher")
            else:
                yield from client.send_message(message.channel, "Erreur dans le nom d'utilisateur")

    if command == "!streamrm" and trusted:
        if len(params) == 1:
            yield from client.send_message(message.channel, "utilisation: !streamrm + usertag")
        for userToRm in params[1:]:
            if userToRm in streamers:
                newStreamList = [user for user in streamers if userToRm != user]
                f2 = open('streamers.txt', 'r+', encoding='utf-8')
                f2.truncate()
                f2.write("\n".join(newStreamList))
                f2.close()
                streamers.clear()
                for s in newStreamList:
                    streamers.append(s)
                yield from client.send_message(message.channel,
                                               userToRm + " a bien été supprimé a la liste des streams a afficher")
            else:
                yield from client.send_message(message.channel, "Erreur dans le nom d'utilisateur")


# Fin des commandes

client.run(token)
