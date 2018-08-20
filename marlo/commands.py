from lxml import etree
import argparse


class CommandHandlerException(Exception):
    """For reporting errors in parsing Agent Command Handlers"""
    def __init__(self, message):
        self.message = message


class CommandParser:
    """Parse Agent Command Handlers to a list"""
    continuousMovementCommands = "ContinuousMovement"
    absoluteMovementCommands = "AbsoluteMovement"
    discreteMovementCommands = "DiscreteMovement"
    inventoryCommands = "Inventory"
    chatCommands = "Chat"
    simpleCraftCommands = "SimpleCraft"
    missionQuitCommands = "MissionQuit"
    humanLevelCommands = "HumanLevel"

    ns = "{http://ProjectMalmo.microsoft.com}"

    all_continuous = ["jump", "move", "pitch", "strafe", "turn", "crouch", "attack", "use"]
    all_absolute = ["tpx", "tpy", "tpz", "tp", "setYaw", "setPitch"]
    all_discrete = ["move", "jumpmove", "strafe", "jumpstrafe", "turn", "movenorth", "moveeast",
                    "movesouth", "movewest", "jumpnorth", "jumpeast", "jumpsouth", "jumpwest",
                    "jump", "look", "attack", "use", "jumpuse"]
    all_inventory = ["swapInventoryItems", "combineInventoryItems", "discardCurrentItem",
                     "hotbar.1", "hotbar.2", "hotbar.3", "hotbar.4", "hotbar.5", "hotbar.6",
                     "hotbar.7", "hotbar.8", "hotbar.9"]
    all_chat = ["chat"]
    all_simplecraft = ["craft"]
    all_mission_quit = ["quit"]
    all_human_level = ["forward", "left", "right", "jump", "sneak", "sprint", "inventory",
                       "swapHands", "drop", "use", "attack", "moveMouse",
                       "hotbar.1", "hotbar.2", "hotbar.3", "hotbar.4", "hotbar.5",
                       "hotbar.6", "hotbar.7", "hotbar.8", "hotbar.9"]

    def __init__(self, comp_all_commands=None):
        self.comp_all_commands = comp_all_commands
        pass

    def get_commands(self, mission_xml, role):
        """Get commands from xml string as a list of (command_type:int, turnbased:boolean, command:string)"""
        mission = etree.fromstring(mission_xml)
        return self._get_commands(mission, role)

    def get_commands_from_file(self, mission_file, role):
        """Get commands from xml file as a list of (command_type:int, turnbased:boolean, command:string)"""
        doc = etree.parse(mission_file)
        mission = doc.getroot()
        return self._get_commands(mission, role)

    def _get_commands(self, mission, role):
        handlers = mission.findall(CommandParser.ns + "AgentSection" + "/" + CommandParser.ns + "AgentHandlers")
        if len(handlers) <= role:
            raise CommandHandlerException("Not enough agents sections in XML")
        commands = []
        self._command_hander(handlers[role], False, commands)
        return commands

    def _command_hander(self, handlers, turnbased, commands):
        for ch in handlers:
            if ch.tag == CommandParser.ns + "TurnBasedCommands":
                self._command_hander(ch, True, commands)
            elif ch.tag == CommandParser.ns + "ContinuousMovementCommands":
                if turnbased:
                    raise CommandHandlerException("ContinuouMovementCommands not allowed in TurnBased")
                commands.extend(self._add_commands(CommandParser.continuousMovementCommands, turnbased, ch))
            elif ch.tag == CommandParser.ns + "AbsoluteMovementCommands":
                commands.extend(self._add_commands(CommandParser.absoluteMovementCommands, turnbased, ch))
            elif ch.tag == CommandParser.ns + "DiscreteMovementCommands":
                commands.extend(self._add_commands(CommandParser.discreteMovementCommands, turnbased, ch))
            elif ch.tag == CommandParser.ns + "InventoryCommands":
                commands.extend(self._add_commands(CommandParser.inventoryCommands, turnbased, ch))
            elif ch.tag == CommandParser.ns + "ChatCommands":
                commands.extend(self._add_commands(CommandParser.chatCommands, turnbased, ch))
            elif ch.tag == CommandParser.ns + "SimpleCraftCommands":
                commands.extend(self._add_commands(CommandParser.simpleCraftCommands, turnbased, ch))
            elif ch.tag == CommandParser.ns + "MissionQuitCommands":
                commands.extend(self._add_commands(CommandParser.missionQuitCommands, turnbased, ch))
            elif ch.tag == CommandParser.ns + "HumanLevelCommands":
                if turnbased:
                    raise CommandHandlerException("HumanLevelCommands not allowed in TurnBased")
                commands.extend(self._add_commands(CommandParser.humanLevelCommands, turnbased, ch))

    def _add_commands(self, command_type, turnbased, elem):
        deny = []
        allow = []
        for ml in elem:
            if ml.tag == CommandParser.ns + "ModifierList":
                # print("**ModifierList**", ml.attrib['type'])
                for cmd in ml:
                    if cmd.tag == CommandParser.ns + "command":
                        # print("Command", cmd.text)
                        if ml.attrib['type'] == 'deny-list':
                            deny.append((command_type, turnbased, cmd.text))
                        if ml.attrib['type'] == 'allow-list':
                            allow.append((command_type, turnbased, cmd.text))
        # print("allow", allow)
        # print("deny", deny)
        return self._fill_command_list(command_type, turnbased, allow, deny)

    def _fill_command_list(self, command_type, turnbased, allow, deny):
        # Add allow defaults for empty allow list.
        if not allow:
            if command_type == CommandParser.discreteMovementCommands:
                allow = [(command_type, turnbased, c) for c in CommandParser.all_discrete]
            elif command_type == CommandParser.continuousMovementCommands:
                allow = [(command_type, turnbased, c) for c in CommandParser.all_continuous]
            elif command_type == CommandParser.absoluteMovementCommands:
                allow = [(command_type, turnbased, c) for c in CommandParser.all_absolute]
        # Remove all denied.
        for d in deny:
            while d in allow:
                allow.remove(d)
        # Restrict to (optional) competition commands.
        if self.comp_all_commands:
            comp_all = [(command_type, turnbased, c) for c in self.comp_all_commands]
            return [a for a in allow if a in comp_all]
        else:
            return allow


def main():
    xml_file = "mission.xml"
    parser = argparse.ArgumentParser(description='Command handler xml parsing test')
    parser.add_argument('--mission_file', type=str, default=xml_file, help='the mission xml')
    parser.add_argument('--role', type=int, default=0, help='the agent role')
    args = parser.parse_args()

    xml_file = args.mission_file
    role = args.role

    print(xml_file)
    # All commands restricted to competition set:
    comp_commands = ["turn", "move", "use", "attack"]
    c = CommandParser(comp_commands)
    command_list = c.get_commands_from_file(xml_file, role)
    print(command_list)


if __name__ == "__main__":
    main()
