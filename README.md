# AdvancedWhitelistR: 离线白名单

一个 [MCDReforged](https://github.com/Fallen-Breath/MCDReforged) 的插件，用于控制给无正版验证的服务器提供白名单功能。

* 原0.x的插件仓库似乎进不去了，斗胆使用了原插件的名字+R以示尊重。
* 由于本人也是临时需要才写的插件，原先的IP白名单功能没有实现（之后有空会补上）

--------

初次加载时会在`MCDR/config/`生成一个配置文件`AdvancedWhitelistR.json`, 离线白名单默认启用状态

第一次使用，您需要改写配置文件并重载插件，以下是插件的配置项说明：

```json5
{
    "bot_list": [], //允许使用的bot列表
    "enable": false, //离线白名单开关（此处不要直接修改，请使用!!awr switch）
    "bot_list_enable": false, //bot白名单
    "Admin": [] //管理员名单
}
```

--------

您可以在控制台或者游戏内使用`!!awr`或者`!!awr help`来获取插件使用方法，指令如下：

```
!!awr help - 显示帮助消息
!!awr status - 离线白名单启用状态
!!awr list §f- 白名单列表
!!awr botlist - bot白名单列表

(以下是白名单管理员指令)
!!awr switch - 开关白名单
!!awr botswitch - 开关bot白名单
!!awr add <player> - 添加白名单
!!awr remove <player> - 删除白名单
```