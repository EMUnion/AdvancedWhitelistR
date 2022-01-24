from mcdreforged.api.types import ServerInterface
from advanced_whitelist_r.utils import *


PLUGIN_METADATA = {
    "id": "advanced_whitelist_r",
    "version": "1.0.2",
    "name": "AdvancedWhitelistR",
    "description": "For outline-model Whitelist",
    "author": "noionion",
    "link": "https://github.com/EMUnion/AdvancedWhitelistR",
    "dependencies": {
        "mcdreforged": ">=2.1.0"
    }
}

help_msg = '''-------- §aAdvancedWhitelistR 高级白名单插件（猹的魔改版） §r--------
§b!!awr help §f- §c显示帮助消息
§b!!awr status §f- §c离线白名单启用状态
§b!!awr list §f- §c白名单列表
§b!!awr botlist §f- §cbot白名单列表

§a(以下是白名单管理员指令)
§b!!awr switch §f- §c开关白名单
§b!!awr botswitch §f- §c开关bot白名单
§b!!awr add <player> §f- §c添加白名单
§b!!awr remove <player> §f- §c删除白名单
-------- §bCurrent Version: §e{} §r--------
'''.format(PLUGIN_METADATA['version'])

global_server = ServerInterface.get_instance().as_plugin_server_interface()

# --------------------------------------------------------------------------

def help_info(server):
    for line in help_msg.splitlines():
        server.reply(line)

def player_add(commandsource, context):
    whitelist = load_whitelist()
    config = load_config()
    global global_server
    if commandsource.is_player:
        if commandsource.player in config['Admin']:
            if player_in_whitelist(whitelist, context['player']):
                commandsource.reply("§7[§3AWR§f/§cWARN§7] §b玩家已存在白名单")
            else:
                uuid = generate_offline_uuid(context['player'])
                dict = {"uuid": uuid, "name": context['player']}
                commandsource.reply("§7[§3AWR§f/§aINFO§7] §b玩家 §e{} §b已加入白名单".format(context['player']))
                if context['player'].startswith('bot_'):
                    config['bot_list'].append(context['player'])
                    save_config(config)
                else:
                    save_whitelist(whitelist, dict)
                    global_server.execute("whitelist reload")
        else:
            commandsource.reply("§7[§3AWR§f/§aINFO§7] §b不是管理员，没有操作权限")
    else:
        if player_in_whitelist(whitelist, context['player']):
            commandsource.reply("§7[§3AWR§f/§cWARN§7] §b玩家已存在白名单")
        else:
            uuid = generate_offline_uuid(context['player'])
            dict = {"uuid": uuid, "name": context['player']}
            commandsource.reply("§7[§3AWR§f/§aINFO§7] §b玩家 §e{} §b已加入白名单".format(context['player']))
            if context['player'].startswith('bot_'):
                config['bot_list'].append(context['player'])
                save_config(config)
            else:
                save_whitelist(whitelist, dict)
                global_server.execute("whitelist reload")


def player_remove(commandsource, context):
    whitelist = load_whitelist()
    config = load_config()
    global global_server
    if commandsource.is_player:
        if commandsource.player in config['Admin']:
            if player_in_whitelist(whitelist, context['player']):
                uuid = generate_offline_uuid(context['player'])
                dict = {"uuid": uuid, "name": context['player']}
                commandsource.reply("§7[§3AWR§f/§aINFO§7] §b玩家 §e{} §b已从白名单移除".format(context['player']))
                if context['player'].startswith('bot_'):
                    config['bot_list'].remove(context['player'])
                    save_config(config)
                else: 
                    save_whitelist(whitelist, dict, remove = True)
                    global_server.execute("whitelist reload")
            else:
                commandsource.reply("§7[§3AWR§f/§cWARN§7] §b玩家本就不在白名单内")
        else:
            commandsource.reply("§7[§3AWR§f/§aINFO§7] §b不是管理员，没有操作权限")
    else:
        if player_in_whitelist(whitelist, context['player']):
            uuid = generate_offline_uuid(context['player'])
            dict = {"uuid": uuid, "name": context['player']}
            commandsource.reply("§7[§3AWR§f/§aINFO§7] §b玩家 §e{} §b已从白名单移除".format(context['player']))
            if context['player'].startswith('bot_'):
                config['bot_list'].remove(context['player'])
                save_config(config)
            else:
                save_whitelist(whitelist, dict, remove = True)
                global_server.execute("whitelist reload")
        else:
            commandsource.reply("§7[§3AWR§f/§cWARN§7] §b玩家本就不在白名单内")


def status_switch(commandsource):
    whitelist = load_whitelist()
    config = load_config()
    if commandsource.is_player:
        if commandsource.player in config['Admin']:
            if config['enable']:
                config['enable'] = False
                global_server.execute("whitelist off")
                commandsource.reply("§7[§3AWR§f/§aINFO§7] §b离线白名单已关闭，所有玩家均可进入游戏")
                save_config(config)
            else:
                config['enable'] = True
                global_server.execute("whitelist on")
                commandsource.reply("§7[§3AWR§f/§aINFO§7] §b离线白名单已开启，玩家不在白名单将无法进入游戏")
                save_config(config)
        else:
            commandsource.reply("§7[§3AWR§f/§aINFO§7] §b不是管理员，没有操作权限")
    else:
        if config['enable']:
            config['enable'] = False
            global_server.execute("whitelist off")
            commandsource.reply("§7[§3AWR§f/§aINFO§7] §b离线白名单已关闭，所有玩家均可进入游戏")
            save_config(config)
        else:
            config['enable'] = True
            global_server.execute("whitelist on")
            commandsource.reply("§7[§3AWR§f/§aINFO§7] §b离线白名单已开启，玩家不在白名单将无法进入游戏")
            save_config(config)


def bot_status_switch(commandsource):
    whitelist = load_whitelist()
    config = load_config()
    if commandsource.is_player:
        if commandsource.player in config['Admin']:
            if config['bot_list_enable']:
                config['bot_list_enable'] = False
                commandsource.reply("§7[§3AWR§f/§aINFO§7] §bbot白名单已关闭")
                save_config(config)
            else:
                config['bot_list_enable'] = True
                commandsource.reply("§7[§3AWR§f/§aINFO§7] §bbot白名单已开启")
                save_config(config)
        else:
            commandsource.reply("§7[§3AWR§f/§aINFO§7] §b不是管理员，没有操作权限")
    else:
        if config['bot_list_enable']:
            config['bot_list_enable'] = False
            commandsource.reply("§7[§3AWR§f/§aINFO§7] §bbot白名单已关闭")
            save_config(config)
        else:
            config['bot_list_enable'] = True
            commandsource.reply("§7[§3AWR§f/§aINFO§7] §bbot白名单已开启")
            save_config(config)


def status_tell(server):
    whitelist = load_whitelist()
    config = load_config()
    if config['enable']:
        server.reply("§7[§3AWR§f/§aINFO§7] §b离线白名单已开启，玩家不在白名单将无法进入游戏")
    else:
        server.reply("§7[§3AWR§f/§aINFO§7] §b离线白名单已关闭，所有玩家均可进入游戏")


def aw_list(server):
    whitelist = load_whitelist()
    namelist = [massage['name'] for massage in whitelist]
    server.reply("§7[§3AWR§f/§aINFO§7] §b白名单玩家列表: " + str(namelist))


def aw_botlist(server):
    config = load_config()
    server.reply("§7[§3AWR§f/§aINFO§7] §bbot白名单列表: " + str(config['bot_list']))