from mcdreforged.api.decorator import new_thread
from mcdreforged.api.command import Literal, Text
import json
import os

PLUGIN_METADATA = {
    'id': 'advanced_whitelist_r',
    'version': '1.0.0',
    'name': 'AdvancedWhitelistR',
    'description': 'For outline-model Whitelist',
    'author': 'noionion',
    'link': 'https://github.com/2X-ercha/AdvancedWhitelistR',
    'dependencies': {
        'mcdreforged': '>=2.1.0'
    }
}

help_msg = '''-------- §aAdvancedWhitelistR 高级白名单插件（猹的魔改版） §r--------
§b!!awr help §f- §c显示帮助消息
§b!!awr status §f- §c离线白名单启用状态
§b!!awr list §f- §c白名单列表

§a(以下是白名单管理员指令)
§b!!awr switch §f- §c开关白名单
§b!!awr add <player> §f- §c添加白名单
§b!!awr remove <player> §f- §c删除白名单
-------- §bCurrent Version: §e{} §r--------
'''.format(PLUGIN_METADATA['version'])

config= {
    "Kick_reason": "你并不在本服务器白名单内，请联系管理员处理。",
    "Whitelist_player": [],
    "enable": True,
    "Admin": []
}


def save_config():
    global config
    with open('./config/AdvancedWhitelistR.json', 'w', encoding="utf-8") as f:
        f.write(json.dumps(config, indent=2, separators=(',', ':'), ensure_ascii=False))


def load_config():
    global config
    with open('./config/AdvancedWhitelistR.json', 'r', encoding="utf-8") as f:
        config = json.load(f)


def on_load(server, prev):
    global config
    if not os.path.exists('./config/AdvancedWhitelistR.json'):
        save_config()
    else:
        load_config()
    server.register_help_message('!!awr', '离线服务器白名单管理')
    server.register_command(Literal('!!awr').runs(help_info). \
        then(
            Literal('add'). \
                then(
                    Text('player').runs(player_add)
                )
        ). \
        then(
            Literal('remove'). \
                then(
                    Text('player').runs(player_remove)
                )
        ). \
        then(
            Literal('switch').runs(status_switch)
        ). \
        then(
            Literal('status').runs(status_tell)
        ). \
        then(
            Literal('list').runs(aw_list)
        ). \
        then(
            Literal('help').runs(help_info)
        ))


def on_player_joined(server, player, info):
    if config['enable']:
        if player not in config['Whitelist_player']:
            server.execute('kick {} {}'.format(player, '§7[§3AdvancedWhitelist§7] '+ config['Kick_reason']))
            server.say('§7[§3AW§f/§aINFO§7] 玩家因不在白名单被踢出游戏')


# 指令表
def help_info(server):
    for line in help_msg.splitlines():
        server.reply(line)

def player_add(commandsource, context):
    if commandsource.is_player:
        if commandsource.player in config['Admin']:
            if context['player'] in config['Whitelist_player']:
                commandsource.reply("§7[§3AW§f/§cWARN§7] §b玩家已存在白名单")
            else:
                config['Whitelist_player'].append(context['player'])
                commandsource.reply("§7[§3AW§f/§aINFO§7] §b玩家 §e{} §b已加入白名单".format(context['player']))
                save_config()
        else:
            commandsource.reply("§7[§3AW§f/§aINFO§7] §b不是管理员，没有操作权限")
    else:
        if context['player'] in config['Whitelist_player']:
            commandsource.reply("§7[§3AW§f/§cWARN§7] §b玩家已存在白名单")
        else:
            config['Whitelist_player'].append(context['player'])
            commandsource.reply("§7[§3AW§f/§aINFO§7] §b玩家 §e{} §b已加入白名单".format(context['player']))
            save_config()

def player_remove(commandsource, context):
    if commandsource.is_player:
        if commandsource.player in config['Admin']:
            if context['player'] in config['Whitelist_player']:
                config['Whitelist_player'].remove(context['player'])
                commandsource.reply("§7[§3AW§f/§aINFO§7] §b玩家 §e{} §b已从白名单移除".format(context['player']))
                save_config()
            else:
                commandsource.reply("§7[§3AW§f/§cWARN§7] §b玩家本就不在白名单内")
        else:
            commandsource.reply("§7[§3AW§f/§aINFO§7] §b不是管理员，没有操作权限")
    else:
        if context['player'] in config['Whitelist_player']:
            config['Whitelist_player'].remove(context['player'])
            commandsource.reply("§7[§3AW§f/§aINFO§7] §b玩家 §e{} §b已从白名单移除".format(context['player']))
            save_config()
        else:
            commandsource.reply("§7[§3AW§f/§cWARN§7] §b玩家本就不在白名单内")

def status_switch(commandsource):
    if commandsource.is_player:
        if commandsource.player in config['Admin']:
            if config['enable']:
                config['enable'] = False
                commandsource.reply("§7[§3AW§f/§aINFO§7] §b离线白名单已关闭，所有玩家均可进入游戏")
                save_config()
            else:
                config['enable'] = True
                commandsource.reply("§7[§3AW§f/§aINFO§7] §b离线白名单已开启，玩家不在白名单将无法进入游戏")
                save_config()
        else:
            commandsource.reply("§7[§3AW§f/§aINFO§7] §b不是管理员，没有操作权限")
    else:
        if config['enable']:
            config['enable'] = False
            commandsource.reply("§7[§3AW§f/§aINFO§7] §b离线白名单已关闭，所有玩家均可进入游戏")
            save_config()
        else:
            config['enable'] = True
            commandsource.reply("§7[§3AW§f/§aINFO§7] §b离线白名单已开启，玩家不在白名单将无法进入游戏")
            save_config()

def status_tell(server):
    if config['enable']:
        server.reply("§7[§3AW§f/§aINFO§7] §b离线白名单已开启，玩家不在白名单将无法进入游戏")
    else:
        server.reply("§7[§3AW§f/§aINFO§7] §b离线白名单已关闭，所有玩家均可进入游戏")

def aw_list(server):
    server.reply("§7[§3AW§f/§aINFO§7] §b白名单玩家列表: " + str(config['Whitelist_player']))
