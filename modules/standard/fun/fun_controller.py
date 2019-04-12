from core.command_param_types import Int
from core.db import DB
from core.decorators import command, instance
import random


@instance()
class FunController:
    """
        Port of Budabot fun module
    """

    def inject(self, registry):
        self.db: DB = registry.get_instance("db")
        self.command_alias_service = registry.get_instance("command_alias_service")

    def start(self):
        self.command_alias_service.add_alias("pinky", "brain")
        self.command_alias_service.add_alias("norris", "chuck")
        self.command_alias_service.add_alias("chucknorris", "chuck")
        self.command_alias_service.add_alias("cyb0r", "cybor")
        self.command_alias_service.add_alias("cyber", "cybor")
        self.command_alias_service.add_alias("office", "dwight")
        self.command_alias_service.add_alias("funcom", "fc")
        self.command_alias_service.add_alias("simpsons", "homer")

    @command(command="beer", params=[Int("item_id", is_optional=True)],
             access_level="member", description="Shows a random beer message")
    def beer_command(self, request, item_id):
        return self.get_fun_message("beer", request, item_id)

    @command(command="brain", params=[Int("item_id", is_optional=True)],
             access_level="member", description="Shows a random pinky and the brain quote")
    def brain_command(self, request, item_id):
        return self.get_fun_message("brain", request, item_id)

    @command(command="chuck", params=[Int("item_id", is_optional=True)],
             access_level="member", description="Shows a random Chuck Norris joke")
    def chuck_command(self, request, item_id):
        return self.get_fun_message("chuck", request, item_id)

    @command(command="cybor", params=[Int("item_id", is_optional=True)],
             access_level="member", description="Shows a random cybor message Caution: HOT!")
    def cybor_command(self, request, item_id):
        return self.get_fun_message("cybor", request, item_id)

    @command(command="dwight", params=[Int("item_id", is_optional=True)],
             access_level="member", description="Shows a random Dwight quote")
    def dwight_command(self, request, item_id):
        return self.get_fun_message("dwight", request, item_id)

    @command(command="fc", params=[Int("item_id", is_optional=True)],
             access_level="member", description="Shows a random FC quote")
    def fc_command(self, request, item_id):
        return self.get_fun_message("fc", request, item_id)

    @command(command="homer", params=[Int("item_id", is_optional=True)],
             access_level="member", description="Shows a random homer quote")
    def homer_command(self, request, item_id):
        return self.get_fun_message("homer", request, item_id)

    @command(command="pirates", params=[Int("item_id", is_optional=True)],
             access_level="member", description="Shows a random Pirates of the Caribbean quote")
    def pirates_command(self, request, item_id):
        return self.get_fun_message("pirates", request, item_id)

    def get_fun_message(self, quote_type, request, number):
        if number is None:
            number = -1
        data = self.db.query("SELECT f.content FROM fun f WHERE type = ?", [str(quote_type)])
        if number == -1:
            row = random.choice(data)
        else:
            try:
                row = data[number]
                dmg = random.randint(100, 999)
                creds = random.randint(10000, 9999999)
                msg = row.content
                msg = msg.replace("*name*", request.sender.name)
                msg = msg.replace("*dmg*", str(dmg))
                msg = msg.replace("*creds*", str(creds))
                return msg;
            except IndexError:
                return "There is no item with that id."
        return row.content;
