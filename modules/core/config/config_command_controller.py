from core.decorators import instance, command
from core.db import DB
from core.text import Text
from core.chat_blob import ChatBlob
from core.command_param_types import Const, Any, Options


@instance()
class ConfigCommandController:
    def inject(self, registry):
        self.db: DB = registry.get_instance("db")
        self.text: Text = registry.get_instance("text")
        self.access_service = registry.get_instance("access_service")
        self.command_service = registry.get_instance("command_service")

    @command(command="config", params=[Const("cmd"), Any("cmd_name"), Options(["enable", "disable"]), Any("channel")], access_level="admin",
             description="Enable or disable a command")
    def config_cmd_status_cmd(self, request, _, cmd_name, action, cmd_channel):
        cmd_name = cmd_name.lower()
        action = action.lower()
        cmd_channel = cmd_channel.lower()
        command_str, sub_command_str = self.command_service.get_command_key_parts(cmd_name)
        enabled = 1 if action == "enable" else 0

        if cmd_channel != "all" and not self.command_service.is_command_channel(cmd_channel):
            return "Unknown command channel <highlight>%s<end>." % cmd_channel

        sql = "UPDATE command_config SET enabled = ? WHERE command = ? AND sub_command = ?"
        params = [enabled, command_str, sub_command_str]
        if cmd_channel != "all":
            sql += " AND channel = ?"
            params.append(cmd_channel)

        count = self.db.exec(sql, params)
        if count == 0:
            return "Could not find command <highlight>%s<end> for channel <highlight>%s<end>." % (cmd_name, cmd_channel)
        else:
            if cmd_channel == "all":
                return "Command <highlight>%s<end> has been <highlight>%sd<end> successfully." % (cmd_name, action)
            else:
                return "Command <highlight>%s<end> for channel <highlight>%s<end> has been <highlight>%sd<end> successfully." % (cmd_name, cmd_channel, action)

    @command(command="config", params=[Const("cmd"), Any("cmd_name"), Const("access_level"), Any("channel"), Any("access_level")], access_level="admin",
             description="Change access_level for a command")
    def config_cmd_access_level_cmd(self, request, _1, cmd_name, _2, cmd_channel, access_level):
        cmd_name = cmd_name.lower()
        cmd_channel = cmd_channel.lower()
        access_level = access_level.lower()
        command_str, sub_command_str = self.command_service.get_command_key_parts(cmd_name)

        if cmd_channel != "all" and not self.command_service.is_command_channel(cmd_channel):
            return "Unknown command channel <highlight>%s<end>." % cmd_channel

        if self.access_service.get_access_level_by_label(access_level) is None:
            return "Unknown access level <highlight>%s<end>." % access_level

        sql = "UPDATE command_config SET access_level = ? WHERE command = ? AND sub_command = ?"
        params = [access_level, command_str, sub_command_str]
        if cmd_channel != "all":
            sql += " AND channel = ?"
            params.append(cmd_channel)

        count = self.db.exec(sql, params)
        if count == 0:
            return "Could not find command <highlight>%s<end> for channel <highlight>%s<end>." % (cmd_name, cmd_channel)
        else:
            if cmd_channel == "all":
                return "Access level <highlight>%s<end> for command <highlight>%s<end> has been set successfully." % (access_level, cmd_name)
            else:
                return "Access level <highlight>%s<end> for command <highlight>%s<end> on channel <highlight>%s<end> has been set successfully." % (access_level, cmd_name, cmd_channel)

    @command(command="config", params=[Const("cmd"), Any("cmd_name")], access_level="admin",
             description="Show command configuration")
    def config_cmd_show_cmd(self, request, _, cmd_name):
        cmd_name = cmd_name.lower()
        command_str, sub_command_str = self.command_service.get_command_key_parts(cmd_name)

        blob = ""
        for command_channel, channel_label in self.command_service.channels.items():
            cmd_configs = self.command_service.get_command_configs(command=command_str,
                                                                   sub_command=sub_command_str,
                                                                   channel=command_channel,
                                                                   enabled=None)
            if len(cmd_configs) > 0:
                cmd_config = cmd_configs[0]
                if cmd_config.enabled == 1:
                    status = "<green>Enabled<end>"
                else:
                    status = "<red>Disabled<end>"

                blob += "<header2>%s<end> %s (Access Level: %s)\n" % (channel_label, status, cmd_config.access_level.capitalize())

                # show status config
                blob += "Status:"
                enable_link = self.text.make_chatcmd("Enable", "/tell <myname> config cmd %s enable %s" % (cmd_name, command_channel))
                disable_link = self.text.make_chatcmd("Disable", "/tell <myname> config cmd %s disable %s" % (cmd_name, command_channel))

                blob += "  " + enable_link + "  " + disable_link

                # show access level config
                blob += "\nAccess Level:"
                for access_level in self.access_service.access_levels:
                    # skip "None" access level
                    if access_level["level"] == 0:
                        continue

                    label = access_level["label"]
                    link = self.text.make_chatcmd(label.capitalize(), "/tell <myname> config cmd %s access_level %s %s" % (cmd_name, command_channel, label))
                    blob += "  " + link
                blob += "\n\n\n"

        if blob:
            # include help text
            blob += "\n\n".join(map(lambda handler: handler["help"], self.command_service.get_handlers(cmd_name)))
            return ChatBlob("Command (%s)" % cmd_name, blob)
        else:
            return "Could not find command <highlight>%s<end>." % cmd_name
