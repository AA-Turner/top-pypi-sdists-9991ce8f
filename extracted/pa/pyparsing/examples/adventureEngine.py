# adventureEngine.py
# Copyright 2005-2006, Paul McGuire
#
# Updated 2012 - latest pyparsing API
# Updated 2023 - using PEP8 API names
#

import contextlib
import random
import string
import pyparsing as pp


def a_or_an(item):
    if item.desc.startswith(tuple("aeiou")):
        return "an " + item.desc
    else:
        return "a " + item.desc

def enumerate_items(items_list):
    if not items_list:
        return "nothing"
    *all_but_last, last = items_list
    out = []
    if all_but_last:
        out.append(", ".join(a_or_an(item) for item in all_but_last))
        if len(all_but_last) > 1:
            out[-1] += ','
        out.append("and")
    out.append(a_or_an(last))
    return " ".join(out)

def enumerate_doors(doors_list):
    if not doors_list:
        return ""
    *all_but_last, last = doors_list
    out = []
    if all_but_last:
        out.append(", ".join(all_but_last))
        if len(all_but_last) > 1:
            out[-1] += ','
        out.append("and")
    out.append(last)
    return " ".join(out)


class Room:
    def __init__(self, desc):
        self.desc = desc
        self.inv = []
        self.gameOver = False
        self.doors = [None, None, None, None]

    def __getattr__(self, attr):
        return {
            "n": self.doors[0],
            "s": self.doors[1],
            "e": self.doors[2],
            "w": self.doors[3],
        }[attr]

    def enter(self, player):
        if self.gameOver:
            player.gameOver = True

    def add_item(self, it):
        self.inv.append(it)

    def remove_item(self, it):
        self.inv.remove(it)

    def describe(self):
        print(self.desc)
        visibleItems = [it for it in self.inv if it.isVisible]
        if random.random() > 0.5:
            if len(visibleItems) > 1:
                is_form = "are"
            else:
                is_form = "is"
            print(f"There {is_form} {enumerate_items(visibleItems)} here.")
        else:
            print(f"You see {enumerate_items(visibleItems)}.")


class Exit(Room):
    def __init__(self):
        super().__init__("")

    def enter(self, player):
        player.gameOver = True


class Item:
    items = {}

    def __init__(self, desc):
        self.desc = desc
        self.isDeadly = False
        self.isFragile = False
        self.isBroken = False
        self.isTakeable = True
        self.isVisible = True
        self.isOpenable = False
        self.useAction = None
        self.usableConditionTest = None
        self.cantTakeMessage = "You can't take that!"
        Item.items[desc] = self

    def __str__(self):
        return self.desc

    def breakItem(self):
        if not self.isBroken:
            print("<Crash!>")
            self.desc = "broken " + self.desc
            self.isBroken = True

    def isUsable(self, player, target):
        if self.usableConditionTest:
            return self.usableConditionTest(player, target)
        else:
            return False

    def useItem(self, player, target):
        if self.useAction:
            self.useAction(player, self, target)


class OpenableItem(Item):
    def __init__(self, desc, contents=None):
        super().__init__(desc)
        self.isOpenable = True
        self.isOpened = False
        if contents is not None:
            if isinstance(contents, Item):
                self.contents = [
                    contents,
                ]
            else:
                self.contents = contents
        else:
            self.contents = []

    def open_item(self, player):
        if not self.isOpened:
            self.isOpened = not self.isOpened
            if self.contents is not None:
                for item in self.contents:
                    player.room.add_item(item)
                self.contents = []
            self.desc = "open " + self.desc

    def close_item(self, player):
        if self.isOpened:
            self.isOpened = not self.isOpened
            if self.desc.startswith("open "):
                self.desc = self.desc[5:]


class Command:
    "Base class for commands"

    def __init__(self, verb, verbProg):
        self.verb = verb
        self.verbProg = verbProg

    @staticmethod
    def help_description():
        return ""

    def _do_command(self, player):
        pass

    def __call__(self, player):
        print(self.verbProg.capitalize() + "...")
        self._do_command(player)


class MoveCommand(Command):
    def __init__(self, quals):
        super().__init__("MOVE", "moving")
        self.direction = quals.direction[0]

    @staticmethod
    def help_description():
        return """MOVE or GO - go NORTH, SOUTH, EAST, or WEST
          (can abbreviate as 'GO N' and 'GO W', or even just 'E' and 'S')"""

    def _do_command(self, player):
        rm = player.room
        nextRoom = rm.doors[
            {
                "N": 0,
                "S": 1,
                "E": 2,
                "W": 3,
            }[self.direction]
        ]
        if nextRoom:
            player.moveTo(nextRoom)
        else:
            print("Can't go that way.")


class TakeCommand(Command):
    def __init__(self, quals):
        super().__init__("TAKE", "taking")
        self.subject = quals.item

    @staticmethod
    def help_description():
        return "TAKE or PICKUP or PICK UP - pick up an object (but some are deadly)"

    def _do_command(self, player):
        rm = player.room
        subj = Item.items[self.subject]
        if subj in rm.inv and subj.isVisible:
            if subj.isTakeable:
                rm.remove_item(subj)
                player.take(subj)
            else:
                print(subj.cantTakeMessage)
        else:
            print(f"There is no {subj} here.")


class DropCommand(Command):
    def __init__(self, quals):
        super().__init__("DROP", "dropping")
        self.subject = quals.item

    @staticmethod
    def help_description():
        return "DROP or LEAVE - drop an object (but fragile items may break)"

    def _do_command(self, player):
        rm = player.room
        subj = Item.items[self.subject]
        if subj in player.inv:
            rm.add_item(subj)
            player.drop(subj)
        else:
            print(f"You don't have {a_or_an(subj)}.")


class InventoryCommand(Command):
    def __init__(self, quals):
        super().__init__("INV", "taking inventory")

    @staticmethod
    def help_description():
        return "INVENTORY or INV or I - lists what items you have"

    def _do_command(self, player):
        print(f"You have {enumerate_items(player.inv)}.")


class LookCommand(Command):
    def __init__(self, quals):
        super().__init__("LOOK", "looking")

    @staticmethod
    def help_description():
        return "LOOK or L - describes the current room and any objects in it"

    def _do_command(self, player):
        player.room.describe()


class ExamineCommand(Command):
    def __init__(self, quals):
        super().__init__("EXAMINE", "examining")
        self.subject = Item.items[quals.item]

    @staticmethod
    def help_description():
        return "EXAMINE or EX or X - look closely at an object"

    def _do_command(self, player):
        msg = random.choice(
            [
                "It's {}.",
                "It's just {}.",
                "It's a beautiful {1}.",
                "It's a rare and beautiful {1}.",
                "It's a rare {1}.",
                "Just {}, nothing special...",
                "{0}, just {0}."
            ]
        )
        print(msg.format(a_or_an(self.subject), self.subject).capitalize())


class DoorsCommand(Command):
    def __init__(self, quals):
        super().__init__("DOORS", "looking for doors")

    @staticmethod
    def help_description():
        return "DOORS - display what doors are visible from this room"

    def _do_command(self, player):
        rm = player.room
        numDoors = sum(1 for r in rm.doors if r is not None)
        if numDoors == 0:
            reply = "There are no doors in any direction."
        else:
            if numDoors == 1:
                reply = "There is a door to the "
            else:
                reply = "There are doors to the "
            doorNames = [
                {0: "north", 1: "south", 2: "east", 3: "west"}[i]
                for i, d in enumerate(rm.doors)
                if d is not None
            ]
            reply += enumerate_doors(doorNames)
            reply += "."
            print(reply)


class UseCommand(Command):
    def __init__(self, quals):
        super().__init__("USE", "using")
        self.subject = Item.items[quals.usedObj]
        if quals.targetObj:
            self.target = Item.items[quals.targetObj]
        else:
            self.target = None

    @staticmethod
    def help_description():
        return "USE or U - use an object, optionally IN or ON another object"

    def _do_command(self, player):
        rm = player.room
        availItems = rm.inv + player.inv
        if self.subject in availItems:
            if self.subject.isUsable(player, self.target):
                self.subject.useItem(player, self.target)
            else:
                print("You can't use that here.")
        else:
            print(f"There is no {self.subject} here to use.")


class OpenCommand(Command):
    def __init__(self, quals):
        super().__init__("OPEN", "opening")
        self.subject = Item.items[quals.item]

    @staticmethod
    def help_description():
        return "OPEN or O - open an object"

    def _do_command(self, player):
        rm = player.room
        availItems = rm.inv + player.inv
        if self.subject in availItems:
            if self.subject.isOpenable:
                if not self.subject.isOpened:
                    self.subject.open_item(player)
                else:
                    print("It's already open.")
            else:
                print("You can't open that.")
        else:
            print(f"There is no {self.subject} here to open.")


class CloseCommand(Command):
    def __init__(self, quals):
        super().__init__("CLOSE", "closing")
        self.subject = Item.items[quals.item]

    @staticmethod
    def help_description():
        return "CLOSE or CL - close an object"

    def _do_command(self, player):
        rm = player.room
        availItems = rm.inv + player.inv
        if self.subject in availItems:
            if self.subject.isOpenable:
                if self.subject.isOpened:
                    self.subject.close_item(player)
                else:
                    print("You can't close that, it's not open.")
            else:
                print("You can't close that.")
        else:
            print(f"There is no {self.subject} here to close.")


class QuitCommand(Command):
    def __init__(self, quals):
        super().__init__("QUIT", "quitting")

    @staticmethod
    def help_description():
        return "QUIT or Q - ends the game"

    def _do_command(self, player):
        print("Ok....")
        player.gameOver = True


class HelpCommand(Command):
    def __init__(self, quals):
        super().__init__("HELP", "helping")

    @staticmethod
    def help_description():
        return "HELP or H or ? - displays this help message"

    def _do_command(self, player):
        print("Enter any of the following commands (not case sensitive):")
        for cmd in [
            InventoryCommand,
            DropCommand,
            TakeCommand,
            UseCommand,
            OpenCommand,
            CloseCommand,
            MoveCommand,
            LookCommand,
            ExamineCommand,
            DoorsCommand,
            QuitCommand,
            HelpCommand,
        ]:
            print(f"  - {cmd.help_description()}")
        print()


class AppParseException(pp.ParseException):
    pass


class Parser:
    def __init__(self):
        self.bnf = self.make_bnf()

    def make_bnf(self):
        invVerb = pp.one_of("INV INVENTORY I", caseless=True)
        dropVerb = pp.one_of("DROP LEAVE", caseless=True)
        takeVerb = pp.one_of("TAKE PICKUP", caseless=True) | (
            pp.CaselessLiteral("PICK") + pp.CaselessLiteral("UP")
        )
        moveVerb = pp.one_of("MOVE GO", caseless=True) | pp.Empty()
        useVerb = pp.one_of("USE U", caseless=True)
        openVerb = pp.one_of("OPEN O", caseless=True)
        closeVerb = pp.one_of("CLOSE CL", caseless=True)
        quitVerb = pp.one_of("QUIT Q", caseless=True)
        lookVerb = pp.one_of("LOOK L", caseless=True)
        doorsVerb = pp.CaselessLiteral("DOORS")
        helpVerb = pp.one_of("H HELP ?", caseless=True).set_name("HELP | H | ?")

        itemRef = pp.OneOrMore(pp.Word(pp.alphas)).set_parse_action(self.validate_item_name).setName("item_ref")
        nDir = pp.one_of("N NORTH", caseless=True).set_parse_action(pp.replace_with("N"))
        sDir = pp.one_of("S SOUTH", caseless=True).set_parse_action(pp.replace_with("S"))
        eDir = pp.one_of("E EAST", caseless=True).set_parse_action(pp.replace_with("E"))
        wDir = pp.one_of("W WEST", caseless=True).set_parse_action(pp.replace_with("W"))
        moveDirection = nDir | sDir | eDir | wDir

        invCommand = invVerb
        dropCommand = dropVerb + itemRef("item")
        takeCommand = takeVerb + itemRef("item")
        useCommand = (
            useVerb
            + itemRef("usedObj")
            + pp.Opt(pp.one_of("IN ON", caseless=True))
            + pp.Opt(itemRef, default=None)("targetObj")
        )
        openCommand = openVerb + itemRef("item")
        closeCommand = closeVerb + itemRef("item")
        moveCommand = (moveVerb | "") + moveDirection("direction")
        quitCommand = quitVerb
        lookCommand = lookVerb
        examineCommand = pp.one_of("EXAMINE EX X", caseless=True) + itemRef("item")
        doorsCommand = doorsVerb.setName("DOORS")
        helpCommand = helpVerb

        # attach command classes to expressions
        invCommand.set_parse_action(InventoryCommand)
        dropCommand.set_parse_action(DropCommand)
        takeCommand.set_parse_action(TakeCommand)
        useCommand.set_parse_action(UseCommand)
        openCommand.set_parse_action(OpenCommand)
        closeCommand.set_parse_action(CloseCommand)
        moveCommand.set_parse_action(MoveCommand)
        quitCommand.set_parse_action(QuitCommand)
        lookCommand.set_parse_action(LookCommand)
        examineCommand.set_parse_action(ExamineCommand)
        doorsCommand.set_parse_action(DoorsCommand)
        helpCommand.set_parse_action(HelpCommand)

        # define parser using all command expressions
        parser = pp.ungroup(
            invCommand
            | useCommand
            | openCommand
            | closeCommand
            | dropCommand
            | takeCommand
            | moveCommand
            | lookCommand
            | examineCommand
            | doorsCommand
            | helpCommand
            | quitCommand
        )("command").set_name("command")

        with contextlib.suppress(Exception):
            parser.create_diagram(
                "adventure_game_parser_diagram.html",
                vertical=3,
                show_groups=True,
                show_results_names=True
            )

        return parser

    def validate_item_name(self, s, l, t):
        iname = " ".join(t)
        if iname not in Item.items:
            raise AppParseException(s, l, f"No such item '{iname}'.")
        return iname

    def parse_cmd(self, cmdstr):
        try:
            ret = self.bnf.parse_string(cmdstr)
            return ret
        except AppParseException as pe:
            print(pe.msg)
        except pp.ParseException as pe:
            print(
                random.choice(
                    [
                        "Sorry, I don't understand that.",
                        "Huh?",
                        "Excuse me?",
                        "???",
                        "What?",
                    ]
                )
            )


class Player:
    def __init__(self, name):
        self.name = name
        self.gameOver = False
        self.inv = []

    def moveTo(self, rm):
        self.room = rm
        rm.enter(self)
        if self.gameOver:
            if rm.desc:
                rm.describe()
            print("Game over!")
        else:
            rm.describe()

    def take(self, it):
        if it.isDeadly:
            print(f"Aaaagh!...., the {it} killed me!")
            self.gameOver = True
        else:
            self.inv.append(it)

    def drop(self, it):
        self.inv.remove(it)
        if it.isFragile:
            it.breakItem()


def createRooms(rm):
    """
    create rooms, using multiline string showing map layout
    string contains symbols for the following:
     A-Z, a-z indicate rooms, and rooms will be stored in a dictionary by
               reference letter
     -, | symbols indicate connection between rooms
     <, >, ^, . symbols indicate one-way connection between rooms
    """
    # start with empty dictionary of rooms
    ret = {}

    # look for room symbols, and initialize dictionary
    # - exit room is always marked 'Z'
    for c in rm:
        if c in string.ascii_letters:
            if c != "Z":
                ret[c] = Room(c)
            else:
                ret[c] = Exit()

    # scan through input string looking for connections between rooms
    rows = rm.split("\n")
    for row, line in enumerate(rows):
        for col, c in enumerate(line):
            if c in string.ascii_letters:
                room = ret[c]
                n = None
                s = None
                e = None
                w = None

                # look in neighboring cells for connection symbols (must take
                # care to guard that neighboring cells exist before testing
                # contents)
                if col > 0 and line[col - 1] in "<-":
                    other = line[col - 2]
                    w = ret[other]
                if col < len(line) - 1 and line[col + 1] in "->":
                    other = line[col + 2]
                    e = ret[other]
                if row > 1 and col < len(rows[row - 1]) and rows[row - 1][col] in "|^":
                    other = rows[row - 2][col]
                    n = ret[other]
                if (
                    row < len(rows) - 1
                    and col < len(rows[row + 1])
                    and rows[row + 1][col] in "|."
                ):
                    other = rows[row + 2][col]
                    s = ret[other]

                # set connections to neighboring rooms
                room.doors = [n, s, e, w]

    return ret


# put items in rooms
def putItemInRoom(i, r):
    if isinstance(r, str):
        r = rooms[r]
    r.add_item(Item.items[i])


def playGame(p, startRoom):
    # create parser
    parser = Parser()
    p.moveTo(startRoom)
    while not p.gameOver:
        cmdstr = input(">> ")
        cmd = parser.parse_cmd(cmdstr)
        if cmd is not None:
            cmd.command(p)
    print()
    print("You ended the game with:")
    for i in p.inv:
        print(" -", a_or_an(i))


if __name__ == '__main__':
    # start game definition
    roomMap = """
         d-Z
         |
       f-c-e
       . |
       q<b
         |
         A
    """
    rooms = createRooms(roomMap)
    rooms["A"].desc = "You are standing on the front porch of a wooden shack."
    rooms["b"].desc = "You are in a garden."
    rooms["c"].desc = "You are in a kitchen."
    rooms["d"].desc = "You are on the back porch."
    rooms["e"].desc = "You are in a library."
    rooms["f"].desc = "You are on the patio."
    rooms["q"].desc = "You are sinking in quicksand.  You're dead..."
    rooms["q"].gameOver = True

    # define global variables for referencing rooms
    frontPorch = rooms["A"]
    garden = rooms["b"]
    kitchen = rooms["c"]
    backPorch = rooms["d"]
    library = rooms["e"]
    patio = rooms["f"]

    # create items
    itemNames = (
        """sword.diamond.apple.flower.coin.shovel.book.mirror.telescope.gold bar""".split(
            "."
        )
    )
    for itemName in itemNames:
        Item(itemName)
    Item.items["apple"].isDeadly = True
    Item.items["mirror"].isFragile = True
    Item.items["coin"].isVisible = False
    Item.items["shovel"].usableConditionTest = lambda p, t: p.room is garden


    def use_shovel(p, subj, target):
        coin = Item.items["coin"]
        if not coin.isVisible and coin in p.room.inv:
            coin.isVisible = True


    Item.items["shovel"].useAction = use_shovel

    Item.items["telescope"].isTakeable = False


    def use_telescope(p, subj, target):
        print("You don't see anything.")


    Item.items["telescope"].useAction = use_telescope

    OpenableItem("treasure chest", Item.items["gold bar"])
    Item.items["chest"] = Item.items["treasure chest"]
    Item.items["chest"].isTakeable = False
    Item.items["chest"].cantTakeMessage = "It's too heavy!"

    OpenableItem("mailbox")
    Item.items["mailbox"].isTakeable = False
    Item.items["mailbox"].cantTakeMessage = "It's nailed to the wall!"

    putItemInRoom("mailbox", frontPorch)
    putItemInRoom("shovel", frontPorch)
    putItemInRoom("coin", garden)
    putItemInRoom("flower", garden)
    putItemInRoom("apple", library)
    putItemInRoom("mirror", library)
    putItemInRoom("telescope", library)
    putItemInRoom("book", kitchen)
    putItemInRoom("diamond", backPorch)
    putItemInRoom("treasure chest", patio)

    # create player
    plyr = Player("Bob")
    plyr.take(Item.items["sword"])

    # start game
    playGame(plyr, frontPorch)
