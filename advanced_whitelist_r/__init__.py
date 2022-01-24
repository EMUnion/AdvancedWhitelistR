from mcdreforged.api.command import Literal, Text
import os
import time
from advanced_whitelist_r.utils import *
from advanced_whitelist_r.instruction_set import *


config= {
    "bot_list": [],
    "enable": False,
    "bot_list_enable": True,
    "Admin": []
}

whitelist = []

def on_load(server, prev):
    global config
    global whitelist
    if not os.path.exists('./config/AdvancedWhitelistR.json'):
        save_config(config)
    else:
        config = load_config()
    if not os.path.exists('./server/whitelist.json'):
        save_whitelist(whitelist, {})
    else:
        whitelist = load_whitelist()
    server.register_help_message('!!awr', '离线服务器白名单管理')
    server.register_command(Literal('!!awr').runs(help_info)
        .then(Literal('add').then(Text('player').runs(player_add)))
        .then(Literal('remove').then(Text('player').runs(player_remove)))
        .then(Literal('switch').runs(status_switch))
        .then(Literal('status').runs(status_tell))
        .then(Literal('list').runs(aw_list))
        .then(Literal('botlist').runs(aw_botlist))
        .then(Literal('botswitch').runs(bot_status_switch))
        .then(Literal('help').runs(help_info)))


def on_player_joined(server, player, info):
    if config['bot_list_enable'] and player.startswith('bot_'):
        time.sleep(1)
        server.execute('kill {}'.format(player))
        server.broadcast('§7[§3AWR§f/§aINFO§7] {}不在白名单内，如有需要请向管理员说明用途并申请'.format(player))