import json
import hashlib
from uuid import UUID
from mcdreforged.api.types import ServerInterface


def save_config(config) -> None:
    with open('./config/AdvancedWhitelistR.json', 'w', encoding="utf-8") as f:
        f.write(json.dumps(config, indent=2, separators=(
            ',', ':'), ensure_ascii=False))


def load_config() -> dict:
    with open('./config/AdvancedWhitelistR.json', 'r', encoding="utf-8") as f:
        config = json.load(f)
    return config


def save_whitelist(whitelist, dict, remove=False, server: ServerInterface | None = None) -> None:
    if not remove:
        whitelist.append(dict)
        with open('./server/whitelist.json', 'w', encoding="utf-8") as f:
            f.write(json.dumps(whitelist, indent=2, separators=(',', ':'), ensure_ascii=False))    
    else:
        server.execute(f'whitelist remove {dict["name"]}')
        whitelist.remove(dict)
    # with open('./server/whitelist.json', 'w', encoding="utf-8") as f:
    #     f.write(json.dumps(whitelist, indent=2, separators=(',', ':'), ensure_ascii=False))


def load_whitelist() -> list:
    with open('./server/whitelist.json', 'r', encoding="utf-8") as f:
        whitelist = json.load(f)
    return whitelist


def generate_offline_uuid(player) -> str:
    def add_uuid_stripes(s):
        return str(UUID(s))
    string = "OfflinePlayer:" + player
    ha = hashlib.md5(string.encode('utf-8')).digest()
    byte_array = [byte for byte in ha]
    byte_array[6] = ha[6] & 0x0f | 0x30
    byte_array[8] = ha[8] & 0x3f | 0x80
    hash_modified = bytes(byte_array)
    return add_uuid_stripes(hash_modified.hex())


def player_in_whitelist(whitelist, player) -> bool:
    namelist = [massage['name'] for massage in whitelist]
    if player in namelist:
        return True
    else:
        return False
