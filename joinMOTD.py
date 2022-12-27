# -*- coding: utf-8 -*-
import json

from daycount import get_day

from cbr.plugin.cbrinterface import CBRInterface
from cbr.plugin.info import MessageInfo
from cbr.plugin.rtext import *

METADATA = {
    'id': 'joinmotd',
    'version': '0.0.1',
    'name': 'joinMOTD-CBR',
    'description': '##joinMOTD to get server join MOTD',
    'author': 'Ricky',
    'link': 'https://github.com/R1ckyH/joinMOTD-CBR'
}

prefix = '##joinMOTD'
config_path = 'config/.json'


def rtext_cmd(txt, msg, cmd):
    return RText(txt).h(msg).c(RAction.run_command, cmd)


def on_player_joined(server: CBRInterface, player, info: MessageInfo):
    with open(config_path, 'r') as f:
        server_name = str(json.load(f)["server_name"])
    msg = f'''§7===============§r Welcome back§7 ===============§r
§r今天是{server_name}§r开服的第§e{get_day()}§r天
§7---------------§r Server List §7---------------§r\n'''
    clients = sorted(server.get_online_mc_clients(), reverse=True)
    for i in clients:
        if i != info.source_client and i != "efficiency":
            msg += rtext_cmd(f"§r[§6{i}§r] ", f"§r点我前往 §6{i}§r", f"/server {i}")
    server.tell_message(info.source_client, player, msg)


def on_message(server, info: MessageInfo):
    if info.content == prefix and info.is_player():
        on_player_joined(server, info.sender, info)


def on_load(server):
    server.register_help_message(prefix, '显示欢迎消息')
