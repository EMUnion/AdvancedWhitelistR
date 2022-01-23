# AdvancedWhitelistR: 离线白名单

一个 [MCDReforged](https://github.com/Fallen-Breath/MCDReforged) 的插件，用于控制给无正版验证的服务器提供白名单功能。

* 原0.x的插件仓库似乎进不去了，斗胆使用了原插件的名字+R以示尊重。
* 由于本人也是临时需要才写的插件，原先的IP白名单功能没有实现（之后有空会补上）

--------

初次加载时会在`MCDR/config/`生成一个配置文件`AdvancedWhitelistR.json`, 离线白名单默认启用状态

第一次使用，您需要改写配置文件并重载插件，以下是插件的配置项说明：

```json
{
    "Kick_reason": "你并不在本服务器白名单内，请联系管理员处理。", //踢出原因
    "Whitelist_player": [], //白名单列表
    "enable": True, //是否启用离线白名单，注意首字母大写: True/False
    "Admin": [] //游戏内修改白名单权限所有者列表
}
```

--------

您可以在控制台或者游戏内使用`!!awr`或者`!!awr help`来获取插件使用方法，指令如下：

```
!!awr (help)                    显示帮助消息
!!awr status                    离线白名单启用状态查看
!!awr list                      白名单列表

// 以下是白名单管理员/控制台指令
!!awr switch                    开关白名单
!!awr add <player>              添加白名单
!!awr remove <player>           删除白名单
```
