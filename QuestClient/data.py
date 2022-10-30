
from __future__ import annotations
import typing
from QuestClient.classes import Art, Badge, Shop as classesShop, Creature, CreatureType, CreatureCategory
import QuestClient as qc

from discord.ext import commands
import discord
from bot_commands import buy

if typing.TYPE_CHECKING:
    from QuestClient.classes import Quest as QuestFr
    from QuestClient import Client as ClientFr
    import QuestClient as qcFr

class FakeContext():
    def __init__(self, user : discord.User, channel : discord.TextChannel):
        self.channel = channel 
        self.user = user 
        self.author = user 
        self.send = channel.send
        self.guild = channel.guild

class FakeCog():
    def __init__(self, client : ClientFr):
        self.client = client 
        self.bot = client.bot

class LevelReward():
    def __init__(self, 
                level : int, 
                stars : int = None, 
                item : typing.Union[list, str] = None, 
                crate : str = None, 
                command : str = None,
                shards : int = None,
                amount : int = 1,
                badge : str = None,
                role : str = None,
                custom : str = None,
                art : str = None
    ):
        self.stars = stars 
        self.shards = shards
        self.level = level
        self.crate = crate
        self.command = command
        self.amount = amount
        self.badge = badge
        self.role = role
        self.custom = custom
        self.art = art

        self.item : list = item 

        if type(item) == str:
            self.item = [item]
    
    async def redeem(self, client: ClientFr, user : qcFr.classes.User, channel : discord.TextChannel):
        if self.stars:
            await user.economy.addBal(bank=self.stars, guild=qc.var.allowed_guilds[0])
            await channel.send(embed=discord.Embed(color=qc.var.embedSuccess, title="Gained Stars!", description=f"You levelled up to level {self.level} and gained {self.stars}{qc.var.currency}"))
        if self.shards:
            user.addShards(self.shards)
            await channel.send(embed=discord.Embed(color=qc.var.embedSuccess, title="Gained Shards!", description=f"You levelled up to level {self.level} and gained {self.shards}{qc.var.shards_currency}"))
        
        if self.crate:
            if self.crate == "creature":
                cost = qc.classes.Zoo().crates.creature.cost
            if self.crate == "shiny":
                cost = qc.classes.Zoo().crates.shiny.cost
            if self.crate == "collectors":
                cost = qc.classes.Zoo().crates.collectors.cost

            await user.economy.addBal(cost * self.amount)
            await buy.crate(client, FakeContext(user.user, channel), self.crate, FakeCog(client), self.amount)
        
        if self.command:
            await channel.send(embed=discord.Embed(color=qc.var.embedSuccess, title="Unlocked new command!", description=f"Unlocked **{self.command}** command. Try it now!"))
        if self.badge:
            await channel.send(embed=discord.Embed(color=qc.var.embedSuccess, title="Unlocked new badge!", description=f"Unlocked **{self.badge}** badge. See your profile with **/profile**!"))
        if self.role:
            await channel.send(embed=discord.Embed(color=qc.var.embedSuccess, title="Gained role!", description=f"Unlocked **{self.role}** role. Edit your roles with **/roles**"))
        if self.custom:
            await channel.send(embed=discord.Embed(color=qc.var.embedSuccess, title="Reward!", description=f"You have won: {self.custom}"))

            if "Custom role" in self.custom:
                await (client.bot.get_user(342136746944757760)).send(f"{user.user} won custom role j")
                await (client.bot.get_user(368071242189897728)).send(f"{user.user} won custom role j")
        if self.item:

            for item_name in self.item:
                item = classesShop().items[item_name]

                user.item.buy_item(item, free=True)
            nl = '\n - '
            await channel.send(
                embed=discord.Embed(
                    color=qc.var.embedSuccess, 
                    title="Gained item!", 
                    description=f"You have been given: **{nl.join(f'{self.item.count(i)}x {i}' for i in list(dict.fromkeys(self.item)))}**. Activate them with **/item activate item**"
                )
            )
        if self.art:
            await channel.send(embed=discord.Embed(color=qc.var.embedSuccess, title="Reward!", description=f"You have gotten the **{self.art}** profile art pair! View/edit your profile with **/profile**"))

        return False
        
    @property 
    def name(self) -> str:
        name = ""

        if self.stars:
            name += f"{self.stars} stars "
        if self.shards:
            name += f"{self.shards} shards "
        if self.crate:
            name += f"{self.amount} {self.crate} crate "
        if self.command:
            name += f"{self.command} command "
        if self.badge:
            name += f"{self.badge} badge "
        if self.role:
            name += f"{self.role} role "
        if self.custom:
            name += self.custom + " "
        if self.art:
            name += f"{self.art} art "
        if self.item:
            nl = ' - '
            name += f"{nl.join(f'{self.item.count(i)}x {i}' for i in list(dict.fromkeys(self.item)))} item(s) "
        
        return name

class ShopItem():
    def __init__(self, name : str):
        self.name = name 
    
    def get(self, user : qcFr.User):
        pass

class Shop():

    mushroom = ShopItem("mushroom")

    def __init__(self):
        pass 
    
    @property
    def reward(self):
        return self

class StarReward():
    def __init__(self, amount : int):
        self.amount = amount 
    
    def __str__(self):
        return f"{self.amount} stars"
    
    async def redeem(self, user : qcFr.User):

        await user.economy.addBal(bank=self.amount)

questXPLevels = [None,
    StarReward(8000),
    Shop().reward.mushroom
]

profile_art : typing.Dict[str, Art] = {
    "background_2":Art("Geometry Dash Background", "Not unlockable", "background_2.png"), #Bought
    "background_3":Art("Dash Lounge background", "Reach Quest XP level 12!", "background_3.png", level=12),
    "background_4":Art("Stripe background", "Reach Quest XP level 2!", "background_4.png", level=2),
    "background_5":Art("Roomba background", "Reach Quest XP level 6!", "background_5.png", level=6),
    "background_6":Art("Sky background", "Reach Quest XP level 9!", "background_6.png", level=9),
    "background_7":Art("Diogenes background", "Reach Quests XP level 18!", "background_7.png", level=18),
    "background_8":Art("Tragedy background", "Reach Quest XP level 45!", "background_8.png", level=45),
    "banner_2":Art("Geometry Dash Banner", "Not unlockable", "banner_2.png"), #Bought
    "banner_3":Art("Dash Lounge banner", "Reach Quest XP level 12!", "banner_3.png", level=12),
    "banner_4":Art("Stripe banner", "Reach Quest XP level 2!", "banner_4.png", level=2),
    "banner_5":Art("Roomba banner", "Reach Quest XP level 6!", "banner_5.png", level=6),
    "banner_6":Art("Sky banner", "Reach Quest XP level 9!", "banner_6.png", level=9),
    "banner_7":Art("Diogenes banner", "Reach Quest XP level 18!", "banner_7.png", level=18),
    "banner_8":Art("Tragedy banner", "Reach Quest XP level 45!", "banner_8.png", level=45)
}
pa = profile_art

badges = {
    "messenger":Badge("Messenger", "Complete tier 6 of message quest", quest="message"),
    "pixel":Badge("Pixel", "Complete tier 6 of pixel quest", quest="pixel"),
    "item":Badge("Item", "Complete tier 6 of item quest", quest="item"),
    "count":Badge("Count", "Complete tier 6 of count quest", quest="count"),
    "star":Badge("Star", "Complete tier 6 of money maker quest", quest="money_maker"),
    "creature":Badge("Creature", "Complete tier 6 of creature quest", quest="creature"),
    "shard":Badge("Shard", "Complete tier 6 of shard quest", quest="shard"),
    "voice":Badge("Voice", "Complete tier 6 of voice quest", quest="voice"),
    "hoarder":Badge("Hoarder", "Complete tier 6 of hoarder quest", quest="hoarder"),
    "quest":Badge("Quest", "Complete tier 6 of quest quest", quest="quest"),
    "miniature":Badge("Miniature", "Complete all mini quests"),
    "polaris_i":Badge("Polaris I", "Reach level 3", polaris_level=3),
    "polaris_ii":Badge("Polaris II", "Reach level 5", polaris_level=5),
    "polaris_iii":Badge("Polaris III", "Reach level 10", polaris_level=10),
    "polaris_iv":Badge("Polaris IV", "Reach level 20", polaris_level=20),
    "polaris_v":Badge("Polaris V", "Reach level 30", polaris_level=30),
    "quest_i":Badge("Quest I", "Reach Quest XP level 10", quest_xp_level=10),
    "quest_ii":Badge("Quest II", "Reach Quest XP level 20", quest_xp_level=20),
    "quest_iii":Badge("Quest III", "Reach Quest XP level 30", quest_xp_level=30),
    "quest_iv":Badge("Quest IV", "Reach Quest XP level 40", quest_xp_level=40),
    "quest_v":Badge("Quest V", "Reach Quest XP level 50 (max)", quest_xp_level=50),
    "shard_producer_i":Badge("Shard Producer I", "Get a daily shard production of 10 shards per day", shard_production_day=10),
    "shard_producer_ii":Badge("Shard Producer II", "Get a daily shard production of 35 shards per day", shard_production_day=35),
    "shard_producer_iii":Badge("Shard Producer III", "Get a daily shard production of 100 shards per day", shard_production_day=100),
    "shard_producer_iv":Badge("Shard Producer IV", "Get a daily shard production of 300 shards per day", shard_production_day=300),
    "shard_producer_v":Badge("Shard Producer V", "Get a daily shard production of 1000 shards per day", shard_production_day=1000)
}

levels : typing.List[LevelReward] = [
    LevelReward(1, stars=1000),
    LevelReward(2, item="mushroom"),
    LevelReward(3, crate="creature", art="Striped"),
    LevelReward(4, stars=1500),
    LevelReward(5, command="compliment"),
    LevelReward(6, shards=3, art="Roomba"),
    LevelReward(7, stars=2000),
    LevelReward(8, crate="creature", amount=2),
    LevelReward(9, stars=3000, art="Sky"),
    LevelReward(10, badge="Quest I"),
    LevelReward(11, shards=5),
    LevelReward(12, crate="shiny", art="Dash Lounge"),
    LevelReward(13, item=["mushroom", "mushroom", "mushroom"]),
    LevelReward(14, stars=5000),
    LevelReward(15, role="camo"), # Profile art
    LevelReward(16, item="fire_flower"),
    LevelReward(17, stars=6000),
    LevelReward(18, shards=10, art="Diogenes"),
    LevelReward(19, crate="creature", amount=5),
    LevelReward(20, badge="Quest II"),
    LevelReward(21, stars=8000),
    LevelReward(22, item="double_cherry"),
    LevelReward(23, shards=15),
    LevelReward(24, item="mask"),
    LevelReward(25, role="light_camo"),
    LevelReward(26, crate="shiny", amount=2),
    LevelReward(27, stars=10000),
    None, # DSi command
    LevelReward(29, item=["double_cherry", "double_cherry"]),
    LevelReward(30, badge="Quest III"),
    LevelReward(31, item=["bubble", "bubble"]),
    LevelReward(32, crate="creature", amount=10),
    LevelReward(33, shards=20),
    LevelReward(34, stars=15000),
    LevelReward(35, role="amoled_camo"),
    LevelReward(36, item=["fire_flower", "fire_flower", "fire_flower"]), 
    LevelReward(37, stars=20000),
    LevelReward(38, shards=25),
    LevelReward(39, item="thunder_cloud"),
    LevelReward(40, badge="Quest IV"),
    LevelReward(41, crate="collectors"),
    LevelReward(42, item=["mushroom", "fire_flower", "bubble"]), 
    LevelReward(43, stars=40000),
    LevelReward(44, crate="creature", amount=20),
    LevelReward(45, role="bot", art="Tragedy"),
    LevelReward(46, shards=30),
    LevelReward(47, item="mega_mushroom"),
    LevelReward(48, stars=100000),
    LevelReward(49, crate="collectors", amount=3),
    LevelReward(50, custom="Custom role (DM Dash) and Quest V badge!")
]


creatures : typing.List[Creature] = [
                Creature("camel", "🐫", CreatureType.STANDARD, CreatureCategory.MAMMAL, ['It better not be Wednesday.', 'What does the hump contain?', 'Quite the slow ride.']),
                Creature("cat", "🐈", CreatureType.STANDARD, CreatureCategory.MAMMAL, ['...meow?', 'Keep all furniture away.', "Hopefully this won't become a loaf."]),
                Creature("chipmunk", "🐿️", CreatureType.STANDARD, CreatureCategory.MAMMAL, ['Alvin would make a great name.', 'Rat of the trees!', 'Those cheeks are HUGE.']),
                Creature("cow", "🐄", CreatureType.STANDARD, CreatureCategory.MAMMAL, ['Mooo!', 'Enjoy your infinite milk supply.', 'You cannot use wheat to breed.']),
                Creature("dinosaur", "🦕", CreatureType.STANDARD, CreatureCategory.MAMMAL, ['I thought these went extinct years ago!', 'Not to be confused with the discord user ', '', 'Might find one in an office.']),
                Creature("dog", "🐕", CreatureType.STANDARD, CreatureCategory.MAMMAL, ["Who's a good boy?", 'Pet the dog. Now.', 'The cutest creature!']),
                Creature("elephant", "🐘", CreatureType.STANDARD, CreatureCategory.MAMMAL, ['Look at that trunk!', 'Feet are big enough to cause earthquakes.', 'I wonder how many people could fit on top of one of these...']),
                Creature("giraffe", "🦒", CreatureType.STANDARD, CreatureCategory.MAMMAL, ['Stretch out your neck!', 'Do not feed meat.', "Didn't Supercheme send one of these?"]),
                Creature("goat", "🐐", CreatureType.STANDARD, CreatureCategory.MAMMAL, ['Have mercy on your ears.', 'Stay away from these on mountains.', 'STEVE WATCH OUT']),
                Creature("hedgehog", "🦔", CreatureType.STANDARD, CreatureCategory.MAMMAL, ['Has an insatiable appetite for chili dogs.', 'Watch out for thorns.', 'Roll!']),
                Creature("hippo", "🦛", CreatureType.STANDARD, CreatureCategory.MAMMAL, ['too op pls nerf', "Don't get on its bad side.", 'Strong on land and water? How overpowered!']),
                Creature("kangaroo", "🦘", CreatureType.STANDARD, CreatureCategory.MAMMAL, ['That pouch could have anything!', 'Boing, boing, boing', 'Get yourself a baby kangaroo.']),
                Creature("leopard", "🐆", CreatureType.STANDARD, CreatureCategory.MAMMAL, ['Look at those spots!', 'Large. Cat.', 'Good luck outrunning one of these!']),
                Creature("llama", "🦙", CreatureType.STANDARD, CreatureCategory.MAMMAL, ['Watch out for spit.', 'Warning: Might mutate and evolve.', 'How silly!']),
                Creature("mammoth", "🦣", CreatureType.STANDARD, CreatureCategory.MAMMAL, ['Could survive an ice age.', 'Look at those tusks!', 'A big, furry beast.']),
                Creature("monkey", "🐒", CreatureType.STANDARD, CreatureCategory.MAMMAL, ['MONKE', 'Be careful! It will take your banana, even behind bars!', 'run.']),
                Creature("mouse", "🐁", CreatureType.STANDARD, CreatureCategory.MAMMAL, ['Do they really like cheese?', 'Keep away from cats.', 'Otherwise known as Jerry.']),
                Creature("pig", "🐖", CreatureType.STANDARD, CreatureCategory.MAMMAL, ["They don't have money inside, trust me.", 'Oink Oink.', 'Can a pig make my house?']),
                Creature("rabbit", "🐇", CreatureType.STANDARD, CreatureCategory.MAMMAL, ["All the world's a rabbit.", 'Used for potions.', 'Going down the rabbit hole.']),
                Creature("rhino", "🦏", CreatureType.STANDARD, CreatureCategory.MAMMAL, ['Are they stomping the ground?!', 'Stay out of sight.', 'I have no ideas for the rhino.']),
                Creature("sheep", "🐑", CreatureType.STANDARD, CreatureCategory.MAMMAL, ['You could make a bed with its wool!', 'Bounce.', 'Get enough of these and you can count them to sleep.']),
                Creature("skunk", "🦨", CreatureType.STANDARD, CreatureCategory.MAMMAL, ['I hope you have some spare tomato juice around.', 'Blinky would make for a great name.', 'Good at repelling people away from your collection.']),
                Creature("tiger", "🐅", CreatureType.STANDARD, CreatureCategory.MAMMAL, ["Hey, that's a pretty big cat...", 'Surprisingly good at swimming.', 'Just wanted to say, congratulations! You just got a Tiger! What a great creature!']),
                Creature("t-rex", "🦖", CreatureType.STANDARD, CreatureCategory.MAMMAL, ['Commonly found in the deep woods...', "Go on. Do dino skip. It'll save so much time!", '', '']),
                Creature("wolf", "🐺", CreatureType.STANDARD, CreatureCategory.MAMMAL, ['Hope you have some bones.', 'Good at huffing and puffing.', 'Watch out! He could be disguised as your grandma.']),
                Creature("zebra", "🦓", CreatureType.STANDARD, CreatureCategory.MAMMAL, ['Striped to perfection.', 'Can sleep while standing... somehow.', 'Grayscale?']),
                Creature("bat", "🦇", CreatureType.STANDARD, CreatureCategory.WINGED, ['Wow! A bat! I sure hope nobody decides to eat it and cause a worldwide pandemic!', 'Can be found in chimneys.', 'The Spookiest Creature!']),
                Creature("bird", "🐦", CreatureType.STANDARD, CreatureCategory.WINGED, ['wavedash.ppt', 'Guys, look!', 'Ready to fly!']),
                Creature("chick", "🐣", CreatureType.STANDARD, CreatureCategory.WINGED, ['Just hatched!', 'Aww!', 'Be gentle!']),
                Creature("dodo", "🦤", CreatureType.STANDARD, CreatureCategory.WINGED, ['please dont react with one of these im begging you', 'Look who decided to come back from extinction!', 'Be ready to board your flight.']),
                Creature("dove", "🕊️", CreatureType.STANDARD, CreatureCategory.WINGED, ['Not to be confused with like soap or something.', 'So elegant!', 'Fly, Dove! Fly!']),
                Creature("duck", "🦆", CreatureType.STANDARD, CreatureCategory.WINGED, ['quack', 'Might wanna keep some bread on you.', 'Beak and all!']),
                Creature("eagle", "🦅", CreatureType.STANDARD, CreatureCategory.WINGED, ['...no', 'Freedom!', 'King of the skies!']),
                Creature("flamingo", "🦩", CreatureType.STANDARD, CreatureCategory.WINGED, ['How many shrimps do you have to eat\nBefore you make your skin turn pink?', 'Zen Master!', "They're supposed to be pink, right?"]),
                Creature("flying_fish", "<:flying_fish:880463657308397588>", CreatureType.STANDARD, CreatureCategory.WINGED, ["Shouldn't this be in the ocean category?", 'What an incredible design!', 'The new dominant species.']),
                Creature("owl", "🦉", CreatureType.STANDARD, CreatureCategory.WINGED, ['Would probably make a good house', 'Hoot hoot!', "But he can't hold a pen!!!"]),
                Creature("parrot", "🦜", CreatureType.STANDARD, CreatureCategory.WINGED, ['Quick! Grab some seeds!', '♩Now Playing - Cat', 'Squawk!']),
                Creature("peacock", "🦚", CreatureType.STANDARD, CreatureCategory.WINGED, ['Hehe... peacock...', 'What beautiful feathers!', 'Try not to be mesmerized...']),
                Creature("pigeon", "<:pigeon:880464170154340394>", CreatureType.STANDARD, CreatureCategory.WINGED, ['Run.', 'Stocked reference?', 'Baby pigeons? No way those are real!']),
                Creature("swan", "🦢", CreatureType.STANDARD, CreatureCategory.WINGED, ['Not an ugly duckling, contrary to popular belief.', 'Bigger than you think.', 'How graceful!']),
                Creature("turkey", "🦃", CreatureType.STANDARD, CreatureCategory.WINGED, ['Gobble gobble!', 'Thanksgiving! What a great time! ...except for these guys.', 'Actually has pretty good eyesight.']),
                Creature("ant", "<:ant:880465372413845504>", CreatureType.STANDARD, CreatureCategory.BUG, ["Admit it. You're guilty. You've killed countless amounts of these guys. You BETTER take good care of this one...", 'So tiny!', 'Great at digging tunnels.']),
                Creature("bee", "🐝", CreatureType.STANDARD, CreatureCategory.BUG, ['Honey!!!', 'Bzzzzz!', 'Loves jazz.']),
                Creature("beetle", "🪲", CreatureType.STANDARD, CreatureCategory.BUG, ["Hopefully there's no beetle catchers nearby...", 'Might be a gem in disguise.', "Be careful! They're sensitive!"]),
                Creature("bug", "🐛", CreatureType.STANDARD, CreatureCategory.BUG, ['Seems very, very hungry.', "Don't mind him. Just crawlin' around.", "The only creature to have the same name as it's own category!"]),
                Creature("butterfly", "🦋", CreatureType.STANDARD, CreatureCategory.BUG, ['Would make a great bossfight!', 'What beautiful wings...', 'Be careful who you call ugly in middle school.']),
                Creature("cricket", "🦗", CreatureType.STANDARD, CreatureCategory.BUG, ['*awkward cricket chirps*', 'Those wings can sing!', 'Is it night time already?']),
                Creature("fly", "🪰", CreatureType.STANDARD, CreatureCategory.BUG, ['Someone get the flyswatter.', 'Bro.', 'Do these things feed off of annoying people??']),
                Creature("ladybug", "🐞", CreatureType.STANDARD, CreatureCategory.BUG, ['How Lucky!', "Shouldn't be too hard to draw one of these...", 'Ladybug? Interesting name...']),
                Creature("lizard", "🦎", CreatureType.STANDARD, CreatureCategory.BUG, ['Keep away from dogs.', 'You should put one of these in a hamster cage.', 'Put it in a lamp and rub it!']),
                Creature("mosquito", "🦟", CreatureType.STANDARD, CreatureCategory.BUG, ["You could've gotten a cool creature, yet here you are, stuck with this. I hope you're happy.", 'A mosquito?? Really??', 'Certified blood sucker.']),
                Creature("roach", "🪳", CreatureType.STANDARD, CreatureCategory.BUG, ['glue. on. roach.', 'They are INVINCIBLE. Run while you can.', 'Can fit through pretty tight gaps...']),
                Creature("scorpion", "🦂", CreatureType.STANDARD, CreatureCategory.BUG, ["You're lucky it's not venomous!", 'Quite the stinger!', 'Glows in the dark!']),
                Creature("snail", "🐌", CreatureType.STANDARD, CreatureCategory.BUG, ['Keep away from salt.', "he's super fast trust me", 'Look at that shell!']),
                Creature("snake", "🐍", CreatureType.STANDARD, CreatureCategory.BUG, ['SSSSSsssss...', 'Quite the long creature!', '*slithers into your creature collection*']),
                Creature("spider", "🕷️", CreatureType.STANDARD, CreatureCategory.BUG, ['The itsy bitsy spider crawls into your creature collection...', 'Good night!', 'Hopefully not radioactive!']),
                Creature("worm", "🪱", CreatureType.STANDARD, CreatureCategory.BUG, ['Might grow wings soon, just like an eagle.', "We've all got a worm in our brain!", "Don't underestimate these fellas, they can breakdance!"]),
                Creature("axolotl", "<:axolotl:881258133920555079>", CreatureType.STANDARD, CreatureCategory.OCEAN, ['Small enough to fit in a bucket.', 'A-X-O-L-O-T-L', 'A very powerful creature...']),
                Creature("crab", "🦀", CreatureType.STANDARD, CreatureCategory.OCEAN, ['Might start a rave.', '...wheatley crab?', '*snip snip*']),
                Creature("crocodile", "🐊", CreatureType.STANDARD, CreatureCategory.OCEAN, []),
                Creature("dolphin", "🐬", CreatureType.STANDARD, CreatureCategory.OCEAN, []),
                Creature("fish", "🐟", CreatureType.STANDARD, CreatureCategory.OCEAN, []),
                Creature("frog", "🐸", CreatureType.STANDARD, CreatureCategory.OCEAN, []),
                Creature("jellyfish", "<:jellyfish:881258828560224287>", CreatureType.STANDARD, CreatureCategory.OCEAN, []),
                Creature("octopus", "🐙", CreatureType.STANDARD, CreatureCategory.OCEAN, ['Could be your dad.']),
                Creature("seahorse", "<:seahorse:881259655123304488>", CreatureType.STANDARD, CreatureCategory.OCEAN, []),
                Creature("seal", "🦭", CreatureType.STANDARD, CreatureCategory.OCEAN, ['Dogs of the sea!']),
                Creature("shark", "🦈", CreatureType.STANDARD, CreatureCategory.OCEAN, ['Pretty sure he can pog.', 'Monster of the sea!', '*jaws theme starts playing*']),
                Creature("shrimp", "🦐", CreatureType.STANDARD, CreatureCategory.OCEAN, []),
                Creature("squid", "🦑", CreatureType.STANDARD, CreatureCategory.OCEAN, ['SQUID GA-', 'Could start glowing...']),
                Creature("tadpole", "<:tadpole:822191561706045460>", CreatureType.STANDARD, CreatureCategory.OCEAN, ['Found all across Tadpole Pond!']),
                Creature("turtle", "🐢", CreatureType.STANDARD, CreatureCategory.OCEAN, ['Always wins the race.']),
                Creature("wave", "<:wave:881260627920822292>", CreatureType.STANDARD, CreatureCategory.OCEAN, ['Could cause a tsunami.', 'One with the ocean!', 'Grab your surfboard.']),
                Creature("whale", "🐳", CreatureType.STANDARD, CreatureCategory.OCEAN, ['Keep away from all gacha games.']),
                Creature("apple", "<:apple:881263814077739098>", CreatureType.STANDARD, CreatureCategory.FOOD, ['Keeps all the doctors away.', 'A classic fruit!', 'Comes in multiple colors!']),
                Creature("banana", "<:Banana:881267940702453871>", CreatureType.STANDARD, CreatureCategory.FOOD, ['Potassium.', "hope you're a naner enjoyer", 'Just a peel of one of these can be deadly.']),
                Creature("berries", "<:berries:881268843228577854>", CreatureType.STANDARD, CreatureCategory.FOOD, ['Travels in a pack!', 'What kind of berries are these, anyways?', '3 in 1!']),
                Creature("breadstick", "🥖", CreatureType.STANDARD, CreatureCategory.FOOD, ['Seems to take a liking to stock photos.', "A stick. Made of bread. What isn't there to like?", "It's supposed to have a face... right?"]),
                Creature("burger", "<:burger:881270170839023706>", CreatureType.STANDARD, CreatureCategory.FOOD, ["Hasn't slept in WEEKS."]),
                Creature("cherry", "<:cherry:882024990705352774>", CreatureType.STANDARD, CreatureCategory.FOOD, ["Why's he so mad?", 'Twins!']),
                Creature("coconut", "<:coconut:882025857940590642>", CreatureType.STANDARD, CreatureCategory.FOOD, ['This could be useful if you ever get stranded on a deserted island.']),
                Creature("coffee", "☕", CreatureType.STANDARD, CreatureCategory.FOOD, []),
                Creature("cookie", "<:cookie:882027484688830514>", CreatureType.STANDARD, CreatureCategory.FOOD, []),
                Creature("cupcake", "<:cupcake:883397220496470028>", CreatureType.STANDARD, CreatureCategory.FOOD, []),
                Creature("dippin'_dots", "<:dippin_dots:821799824985948190>", CreatureType.STANDARD, CreatureCategory.FOOD, ["Let's eat Dippin' Dots!", 'Exclusive to water parks.', "Can you imagine if someone made a server with just a single image of dippin' dots? That would be insane!"]),
                Creature("fries", "<:fries:904851591822196786>", CreatureType.STANDARD, CreatureCategory.FOOD, []),
                Creature("grapes", "<:grape:883780769191952466>", CreatureType.STANDARD, CreatureCategory.FOOD, []),
                Creature("hot_dog", "<:hotdog:904852492574146672>", CreatureType.STANDARD, CreatureCategory.FOOD, []),
                Creature("lemon", "<:lemon:884963801915621416>", CreatureType.STANDARD, CreatureCategory.FOOD, []),
                Creature("marshmallow", "<:marshmallow:1030216791097610281>", CreatureType.STANDARD, CreatureCategory.FOOD, []),
                Creature("orange", "<:orange:883779327370592277>", CreatureType.STANDARD, CreatureCategory.FOOD, []),
                Creature("peanut", "<:peanut:904853275780718652>", CreatureType.STANDARD, CreatureCategory.FOOD, []),
                Creature("pear", "<:pear:904853980486721557>", CreatureType.STANDARD, CreatureCategory.FOOD, ['Shhh!!!']),
                Creature("pineapple", "<:pineapple:904854811965538315>", CreatureType.STANDARD, CreatureCategory.FOOD, ['Goes great on pizza!', 'Does NOT go on pizza.', 'Obligatory pineapple message not relating to pizza.']),
                Creature("pizza", "<:pizza:883171283364356207>", CreatureType.STANDARD, CreatureCategory.FOOD, ["Honestly though, who DOESN'T like pizza??", 'Pie up!', "Listen kid, I don't have much time left. The best pizza place iṡ̵͐ ̶̝̔m̷̮̀j̷̋͠h̵́͊j̶͝͝ȃ̶͠#̷͖̋$̴̀͝@̷͗͌%̶̋͋&̷́̍"]),
                Creature("potato", "<:potato:904855450128900156>", CreatureType.STANDARD, CreatureCategory.FOOD, []),
                Creature("pretzel", "<:pretzel:883176189211058206>", CreatureType.STANDARD, CreatureCategory.FOOD, ['What a gentleman!']),
                Creature("rice_ball", "🍙", CreatureType.STANDARD, CreatureCategory.FOOD, ['Makes for a great baseball.']),
                Creature("sandwich", "<:sandwich:904856590321070080>", CreatureType.STANDARD, CreatureCategory.FOOD, ['this is a.    sandwich', 'Stacked to perfection!']),
                Creature("spoon", "<:spoon:904857292007178270>", CreatureType.STANDARD, CreatureCategory.FOOD, ["Not a food, but hey, I won't judge you for eating it.", 'Ready to scoop!']),
                Creature("strawberry", "<:strawberry:904861657665273936>", CreatureType.STANDARD, CreatureCategory.FOOD, ["Shhh... They're sleeping...", 'What an interesting name for a fruit.']),
                Creature("salt", "<:salt:883784378642214922>", CreatureType.STANDARD, CreatureCategory.FOOD, ['Could you pass the salt?']),
                Creature("tomato", "<:tomato:883395084626825216>", CreatureType.STANDARD, CreatureCategory.FOOD, ['Hey, no swearing! Strike 1!']),
                Creature("watermelon", "<:watermelon:883782738770034739>", CreatureType.STANDARD, CreatureCategory.FOOD, ['Packed with seeds!']),
                Creature("alien", "👽", CreatureType.STANDARD, CreatureCategory.MAGIC, ['Out of this world!', 'bogos binted?', 'What if WE are the aliens?']),
                Creature("bomb", "<:bomb:883552735088226324>", CreatureType.STANDARD, CreatureCategory.MAGIC, ['Kaboom!', 'Loaded with gunpowder.', 'Finally... the weakness for the Flyfish has been found...']),
                Creature("brain", "<:brain:883564375993118760>", CreatureType.STANDARD, CreatureCategory.MAGIC, ['How smart!', 'Genius!', 'You looked like you needed one of these.']),
                Creature("controller", "<:controller:883557383891198012>", CreatureType.STANDARD, CreatureCategory.MAGIC, ['Prepare for intense gaming sessions.', 'Covered in cheeto dust and hand grease.', 'Controller > Keyboard']),
                Creature("diamond", "<:diamond:883554235793412097>", CreatureType.STANDARD, CreatureCategory.MAGIC, ["Whatever you do, DON'T mine the diamond with your hand.", 'Ooh! Shiny!', 'I hope you have a patent.']),
                Creature("dragon", "🐉", CreatureType.STANDARD, CreatureCategory.MAGIC, ["Shouldn't this be a bigger deal?", 'thats a dragon.', 'Ever heard of the dragon task?']),
                Creature("ghost", "👻", CreatureType.STANDARD, CreatureCategory.MAGIC, ['Up for a ghost choir?', 'Quite the spooky creature!', 'BOO']),
                Creature("goblin", "👺", CreatureType.STANDARD, CreatureCategory.MAGIC, ["Wait, they're real?", 'Can turn trees into gold.', 'Lurks in haunted forests...']),
                Creature("heart", "<:heart:883561248686473246>", CreatureType.STANDARD, CreatureCategory.MAGIC, ['What a lovely creature!', '<3', 'The heart has heart eyes? Makes sense.']),
                Creature("invader", "👾", CreatureType.STANDARD, CreatureCategory.MAGIC, ['A great ticket farmer!', 'An arcade classic.']),
                Creature("jack_o_lantern", "🎃", CreatureType.STANDARD, CreatureCategory.MAGIC, ['What a spooky creature!', 'Carved to perfection.']),
                Creature("ninja", "🥷", CreatureType.STANDARD, CreatureCategory.MAGIC, ['A master of stealth.']),
                Creature("shadow", "<:shadow:883780111567052871>", CreatureType.STANDARD, CreatureCategory.MAGIC, ['...Do you see anything?', 'What he looks like is still a mystery...']),
                Creature("shield", "<:shield:883562479064608878>", CreatureType.STANDARD, CreatureCategory.MAGIC, ['Can tank a ton of hits!', 'Protects you from all danger!', 'Poor guy, must have been through a lot...']),
                Creature("skull", "💀", CreatureType.STANDARD, CreatureCategory.MAGIC, ['Noop!', "They're spooky, scary and skeletons!", 'Surprisingly good at chess.']),
                Creature("snowman", "⛄", CreatureType.STANDARD, CreatureCategory.MAGIC, []),
                Creature("robot", "🤖", CreatureType.STANDARD, CreatureCategory.MAGIC, ['Beep boop.']),
                Creature("unicorn", "🦄", CreatureType.STANDARD, CreatureCategory.MAGIC, ['Their horns can play rave music.']),
                Creature("bamboo", "<:bamboo:905203057934094427>", CreatureType.STANDARD, CreatureCategory.NATURE, ['A great fuel source!', 'Always watching...']),
                Creature("bolt", "<:bolt:904911694030073866>", CreatureType.STANDARD, CreatureCategory.NATURE, ['Full of positive energy!', 'Bzzzzt!']),
                Creature("cactus", "<:cactus:903364437451350037>", CreatureType.STANDARD, CreatureCategory.NATURE, ['Keep away from corrupted cubes.', 'Might not want to ram into this with full force...', 'Available in a select few states.']),
                Creature("cloud", "<:cloud:906240218967986176>", CreatureType.STANDARD, CreatureCategory.NATURE, []),
                Creature("clover", "<:clover:906240201360285757>", CreatureType.STANDARD, CreatureCategory.NATURE, ['Lucky you!']),
                Creature("flame", "<:flame:906261548027215874>", CreatureType.STANDARD, CreatureCategory.NATURE, ['So cool... uh.. wait, I mean hot.']),
                Creature("sun", "🌞", CreatureType.STANDARD, CreatureCategory.NATURE, []),
                Creature("moon", "🌚", CreatureType.STANDARD, CreatureCategory.NATURE, []),
                Creature("palm_tree", "<:palm_tree:906320492095483954>", CreatureType.STANDARD, CreatureCategory.NATURE, []),
                Creature("planet", "<:planet:906318169818427413>", CreatureType.STANDARD, CreatureCategory.NATURE, []),
                Creature("rainbow", "<:rainbow:906414070721314827>", CreatureType.STANDARD, CreatureCategory.NATURE, []),
                Creature("rose", "<:rose:906264511080697916>", CreatureType.STANDARD, CreatureCategory.NATURE, []),
                Creature("shell", "<:shell:906263985383432293>", CreatureType.STANDARD, CreatureCategory.NATURE, []),
                Creature("star", "<:star:903362240068063282>", CreatureType.STANDARD, CreatureCategory.NATURE, []),
                Creature("tornado", "<:tornado:906241237433061376>", CreatureType.STANDARD, CreatureCategory.NATURE, ['Caused by the flap of a butterfly wing.', 'Alabama.']),
                Creature("tree", "<:tree:906243206977560616>", CreatureType.STANDARD, CreatureCategory.NATURE, []),
                Creature("tulip", "<:tulip:906262428638121994>", CreatureType.STANDARD, CreatureCategory.NATURE, []),
                Creature("square", "<:square:883557014960242738>", CreatureType.STANDARD, CreatureCategory.JSAB, ['Player 1!']),
                Creature("triangle", "<:triangle:883557024703610891>", CreatureType.STANDARD, CreatureCategory.JSAB, ['Player 2!']),
                Creature("pentagon", "<:pentagon:883557043666055188>", CreatureType.STANDARD, CreatureCategory.JSAB, ['Player 3!']),
                Creature("circle", "<:circle:883557034774114304>", CreatureType.STANDARD, CreatureCategory.JSAB, ['Player 4!', "Don't let cheme see this."]),
                Creature("cube", "<:jsb_smile:822846079351521321>", CreatureType.STANDARD, CreatureCategory.JSAB, []),
                Creature("helicopter", "<:helicopter:883559156521529345>", CreatureType.STANDARD, CreatureCategory.JSAB, []),
                Creature("sailboat", "<:sailboat:883557995831754823>", CreatureType.STANDARD, CreatureCategory.JSAB, []),
                Creature("blixer", "<:JSB_Boss:822846027555667978>", CreatureType.STANDARD, CreatureCategory.JSAB, ['Long live the new fresh']),
                Creature("specter", "<:specter:883561142633521162>", CreatureType.STANDARD, CreatureCategory.JSAB, ['Beware of scythes!', 'Is that hair or a hoodie?', 'La dance macabre']),
                Creature("shape_sun", "<:sun:883561404345495552>", CreatureType.STANDARD, CreatureCategory.JSAB, ['Ready to dance!']),
                Creature("beat_bird", "<:bird:883560582110908427>", CreatureType.STANDARD, CreatureCategory.JSAB, ['Learn how to dash from one of these!']),
                Creature("beat_plant", "<:plant:883560339050999819>", CreatureType.STANDARD, CreatureCategory.JSAB, []),
                Creature("beat_spider", "<:spider:883557450333192223>", CreatureType.STANDARD, CreatureCategory.JSAB, []),
                Creature("shroom", "<:shroom:883561872756998164>", CreatureType.STANDARD, CreatureCategory.JSAB, []),
                Creature("dash", "<:dash:822848193460568076>", CreatureType.STANDARD, CreatureCategory.GEOMETRY_DASH, ['Might start rambling about liminal spaces or something.', "Doesn't this guy own the server??", 'not rASH0101, you should sell']),
                Creature("solargress", "<:Solargress:822848170479452182>", CreatureType.STANDARD, CreatureCategory.GEOMETRY_DASH, ['Not to be confused with Solacress.', 'Well acquainted with google translating Paper Mario games.']),
                Creature("dino", "<:Dino:900868719612403772>", CreatureType.STANDARD, CreatureCategory.GEOMETRY_DASH, ['Me too! Hey, are those cookies?', 'Also known as gringle.', 'Valorant enjoyer.']),
                Creature("supercheme", "<:supercheme:900869160609931305>", CreatureType.STANDARD, CreatureCategory.GEOMETRY_DASH, ["Quick, come in! We're playing Wii Party U!", 'Cookie Run Kingdom Enthusiast.', 'Ready to race around the world!']),
                Creature("yellow_meat_boy", "<:yellowmeatboy:822849178853572649>", CreatureType.STANDARD, CreatureCategory.GEOMETRY_DASH, ["Don't let him send you to the meat realm!", 'You wield... something... powerful...', 'فتى اللحم الأصفر']),
                Creature("corrupted_cube", "<:corrupted_cube:822168762694238299>", CreatureType.STANDARD, CreatureCategory.GEOMETRY_DASH, ['I hope you brought your ban hammer.', 'Spawned from the corrupted core!', 'Easily hypnotized.']),
                Creature("coolo2", "<:coolo2:900871313034453072>", CreatureType.STANDARD, CreatureCategory.GEOMETRY_DASH, ["Obsessed with Solargress O's", "I hope you've been refilling that bowl...", 'It all started a long time ago. A deadly virus started to spread all across the Dashlands.']),
                Creature("spuse", "<:spuse:901058450627366942>", CreatureType.STANDARD, CreatureCategory.GEOMETRY_DASH, ['Just ram into the cactus with full force!', 'An amazing artist.', 'WILL leave a pipe bomb at your front door.']),
                Creature("easy_demon", "<:EasyDemon:902617520631058442>", CreatureType.STANDARD, CreatureCategory.GEOMETRY_DASH, ['The Nightmare by JAX???', 'Usually just insane rated levels with intrusive decoration.', 'Wack.']),
                Creature("medium_demon", "<:MediumDemon:902617527564242985>", CreatureType.STANDARD, CreatureCategory.GEOMETRY_DASH, ['B.', 'Yep, sure is a difficulty.', 'Either really long or really short.']),
                Creature("hard_demon", "<:HardDemon:901058547180249119>", CreatureType.STANDARD, CreatureCategory.GEOMETRY_DASH, ['Fast, eye-straining waves.', "What's a future funk?", 'Most common rating for unknown demons.']),
                Creature("insane_demon", "<:InsaneDemon:901058559960309811>", CreatureType.STANDARD, CreatureCategory.GEOMETRY_DASH, ["Can't wait for dash to post another one of these!", 'The best difficulty.', "It's game time!"]),
                Creature("extreme_demon", "<:ExtremeDemon:901058568348901396>", CreatureType.STANDARD, CreatureCategory.GEOMETRY_DASH, ['Beware of straight fly and unforgiving timings.', 'giVeS tHe SaMe AmOuNt oF sTaRs As bLaSt pRoCeSsiNg!!', '♩Now Playing - At the speed of light']),
                Creature("grimace", "<:grimace:902617873598517329>", CreatureType.STANDARD, CreatureCategory.GEOMETRY_DASH, ['Is this the creature you wanted?', 'Frankensteined together for your creature collecting pleasure.', 'D-Day has arrived.']),
                Creature("baby_yoshi", "<:68_BabyYoshi:822848655831597096>", CreatureType.STANDARD, CreatureCategory.MARIO, ['Comes in three different colors!']),
                Creature("yoshi", "<:yoshi:902619594764746803>", CreatureType.STANDARD, CreatureCategory.MARIO, []),
                Creature("piranha_plant", "<:plant:822849640298709022>", CreatureType.STANDARD, CreatureCategory.MARIO, ["No way he'll make it into smash bros."]),
                Creature("mole", "<:montymole:822850128439279639>", CreatureType.STANDARD, CreatureCategory.MARIO, []),
                Creature("chain_chomp", "<:chain:821794493514776578>", CreatureType.STANDARD, CreatureCategory.MARIO, ['Bark Bark!']),
                Creature("goomba", "<:goomba:822850295184359448>", CreatureType.STANDARD, CreatureCategory.MARIO, ["You're gonna turn into a goomba!", 'Weak to stomping.', 'Has a genius plan for defeating his enemies: Walking forward.']),
                Creature("koopa", "<:koopa:821795146307469312>", CreatureType.STANDARD, CreatureCategory.MARIO, ['Koopa the Quick?']),
                Creature("boo", "<:boo:821799407132344321>", CreatureType.STANDARD, CreatureCategory.MARIO, []),
                Creature("magikoopa", "<:magikoopa:906411892082368523>", CreatureType.STANDARD, CreatureCategory.MARIO, []),
                Creature("bullet_bill", "<:bullet_bill:902622225797107793>", CreatureType.STANDARD, CreatureCategory.MARIO, []),
                Creature("thwomp", "<:thwomp:902622254368714793>", CreatureType.STANDARD, CreatureCategory.MARIO, []),
                Creature("hammer_bro", "<:hammer_bro:902622287956684850>", CreatureType.STANDARD, CreatureCategory.MARIO, ['Meticulously designed to be annoying.', 'Get ready for a hammer bros surprise!', 'Near unstoppable in pairs.']),
                Creature("pokey", "<:pokey:902622335629140008>", CreatureType.STANDARD, CreatureCategory.MARIO, []),
                Creature("blooper", "<:blooper:902622372354478130>", CreatureType.STANDARD, CreatureCategory.MARIO, []),
                Creature("fuzzy", "<:fuzzy:902622386560573471>", CreatureType.STANDARD, CreatureCategory.MARIO, ['I rate this creature with 5 Fuzzies!']),
                Creature("shy_guy", "<:shy:902622445800935474>", CreatureType.STANDARD, CreatureCategory.MARIO, []),
                Creature("spike", "<:spike:902622622574063707>", CreatureType.STANDARD, CreatureCategory.MARIO, ['Commonly referred to as ', '']),
                Creature("dry_bones", "<:dry_bones:902622979962322965>", CreatureType.STANDARD, CreatureCategory.MARIO, ['Dry bones for smash!']),
                Creature("bob-omb", "<:bob_omb:902622999151259719>", CreatureType.STANDARD, CreatureCategory.MARIO, ['Sharpen those sorting skills!']),
                Creature("muncher", "<:muncher:902623029669003305>", CreatureType.STANDARD, CreatureCategory.MARIO, ['Up for a game of knat attack?']),
                Creature("cheep_cheep", "<:cheep_cheep:902623076972367922>", CreatureType.STANDARD, CreatureCategory.MARIO, ['Enemies of the sea!']),
                Creature("note", "<:note:902623193540460565>", CreatureType.STANDARD, CreatureCategory.RHYTHM, ['Looks more like a turnip than a note.', '♩ ♫ ♪ ♬', "I'll let you decide what note this is."]),
                Creature("huebird", "<:81_Huebird:822194477690781796>", CreatureType.STANDARD, CreatureCategory.RHYTHM, ['Tweet, twe-twe-tweet, tweet, squawk!', 'Travels in a pack!', 'Comes in many different colors!']),
                Creature("chorus_kid", "<:chorus_kid:822196950299967528>", CreatureType.STANDARD, CreatureCategory.RHYTHM, ['Together now!', 'In Skellybones favorite rhythm heaven game!', 'Part of a Glee Club.']),
                Creature("screwbot", "<:screwbot:822202459836907580>", CreatureType.STANDARD, CreatureCategory.RHYTHM, ['Oh yeah!', 'Might wanna finish screwing.', 'Bigger than a skyscraper!']),
                Creature("rhythm_monkey", "<:rhythm_monkey:822203631121334332>", CreatureType.STANDARD, CreatureCategory.RHYTHM, ['Have you seen those monkey watches??', 'Makes for a great golf trainer.', 'Ook ook!']),
                Creature("tibby", "<:tibby:902623950461354035>", CreatureType.STANDARD, CreatureCategory.RHYTHM, ["Let's we go, amigo!", 'Comes from Heaven world. (H-E-V-V-E-N)', 'Pretty good at restoring flow.']),
                Creature("virus", "<:virus:902624526305747054>", CreatureType.STANDARD, CreatureCategory.RHYTHM, ['Weakness: Forks', "Thank goodness it's just the one.", 'Dangerous in packs!']),
                Creature("spirit", "<:spirit:902624837690875906>", CreatureType.STANDARD, CreatureCategory.RHYTHM, ['I hope you know how to count to 8.', "Not evil, but pretty mean, that's for sure.", 'Weak to arrows.']),
                Creature("barista", "<:barista:902624973334671361>", CreatureType.STANDARD, CreatureCategory.RHYTHM, ['Ready to brew!', 'The barista... is a dog?', 'Coffee enjoyer.']),
                Creature("love_lizard", "<:love_lizard:902625405742223420>", CreatureType.STANDARD, CreatureCategory.RHYTHM, ['Looking for his partner...', 'I hope you can match the rhythm!', 'Easily impressed by music.']),
                Creature("hungry_goat", "<:hungry_goat:902625833846452305>", CreatureType.STANDARD, CreatureCategory.RHYTHM, ['Really likes hairy onions.', 'FEVER!!!', 'A goat that... lays golden eggs?']),
                Creature("ufo", "<:ufo:906418166668861451>", CreatureType.STANDARD, CreatureCategory.RHYTHM, ['Are you ready for Space Ball?', "Welcome to the remix! Here, you'll see multiple games... from earlier all *mixed together*.", 'Works surprisingly well as a baseball.']),
                Creature("drummer", "<:drummer:902625529725878343>", CreatureType.STANDARD, CreatureCategory.RHYTHM, ['Hosts some pretty brutal drumming lessons.', "...so you're telling me this ISN'T an inkling?", 'Get ready to start drumming!']),
                Creature("onion", "<:onion:902625439296680006>", CreatureType.STANDARD, CreatureCategory.RHYTHM, ['You might want to shave it daily.', 'Hair clippers highly recommended.', 'A great snack for goats.']),
                Creature("figure_fighter", "<:figure_fighter:902626083613069372>", CreatureType.STANDARD, CreatureCategory.RHYTHM, ['Go Go Go!!!', "It's even in Mint Condition!", "Now you're ready for the tournament!"]),
                Creature("peashooter", "<:peashooter:821797022445076530>", CreatureType.STANDARD, CreatureCategory.PLANTS_VS_ZOMBIES, ['A classic plant.', 'This thing uses PEAS as a weapon??', 'Can solo a cone head zombie.']),
                Creature("sunflower", "<:sunflower:821797093609439243>", CreatureType.STANDARD, CreatureCategory.PLANTS_VS_ZOMBIES, ['You better place these symmetrically!', '1 row or 2 rows?', "There's a zombie on your lawn!"]),
                Creature("wallnut", "<:wallnut:821797151390564393>", CreatureType.STANDARD, CreatureCategory.PLANTS_VS_ZOMBIES, ['Up for a game of bowling?', 'Huma... er, Plant Shield!', 'Poor guy, made to be eaten.']),
                Creature("puffshroom", "<:puffshroom:821797213193371768>", CreatureType.STANDARD, CreatureCategory.PLANTS_VS_ZOMBIES, ['Costs 0 sun! ...but still costs stars.', 'The strongest plant...', 'Might wanna get some coffee beans!']),
                Creature("potato_mine", "<:potato:821797348824186890>", CreatureType.STANDARD, CreatureCategory.PLANTS_VS_ZOMBIES, ['Just a measly 25 sun!', 'Watch your step...']),
                Creature("squash", "<:squash:821797447902822420>", CreatureType.STANDARD, CreatureCategory.PLANTS_VS_ZOMBIES, ["Don't get too close...", 'You better give him space!']),
                Creature("garlic", "<:garlic:902626577483960322>", CreatureType.STANDARD, CreatureCategory.PLANTS_VS_ZOMBIES, ['BEST PLANT NO CONTEST']),
                Creature("starfruit", "<:starfruit:902626752289992724>", CreatureType.STANDARD, CreatureCategory.PLANTS_VS_ZOMBIES, []),
                Creature("tangle_kelp", "<:tangle_kelp:902627190963847188>", CreatureType.STANDARD, CreatureCategory.PLANTS_VS_ZOMBIES, []),
                Creature("cabbage_pult", "<:cabbage_pult:902627292197556314>", CreatureType.STANDARD, CreatureCategory.PLANTS_VS_ZOMBIES, []),
                Creature("magnet", "<:magnet:902627432580923503>", CreatureType.STANDARD, CreatureCategory.PLANTS_VS_ZOMBIES, []),
                Creature("doom_shroom", "<:doom:902627518446714961>", CreatureType.STANDARD, CreatureCategory.PLANTS_VS_ZOMBIES, ['WILL leave a crater in your creature catalog.', 'STAY BACK!!!', "You're lucky he's on your side."]),
                Creature("marigold", "<:marigold:902627583093534780>", CreatureType.STANDARD, CreatureCategory.PLANTS_VS_ZOMBIES, ['If only it could produce stars...', 'Free coins!', 'This.. flower.. produces coins? How does that make any sense??']),
                Creature("plantern", "<:plantern:902627678551670794>", CreatureType.STANDARD, CreatureCategory.PLANTS_VS_ZOMBIES, ['LET THERE BE LIGHT', "So you're telling me this plant can produce electricity?"]),
                Creature("blover", "<:blover:902627734268813322>", CreatureType.STANDARD, CreatureCategory.PLANTS_VS_ZOMBIES, ['Fog is no more!']),
                Creature("jalapeno", "<:jalapeno:902627827600474183>", CreatureType.STANDARD, CreatureCategory.PLANTS_VS_ZOMBIES, ['Warning: EXTREMELY spicy.', 'Could start a forest fire.', "Why's he so mad?"]),
                Creature("chomper", "<:chomper:902627910068867133>", CreatureType.STANDARD, CreatureCategory.PLANTS_VS_ZOMBIES, ["Stay away from it's mouth.", 'Even with those teeth, he still chews pretty slowly.', "Hey, isn't that the plant from mario?"]),
                Creature("lily_pad", "<:lily_pad:902628036824936458>", CreatureType.STANDARD, CreatureCategory.PLANTS_VS_ZOMBIES, ["Yep, it's alive!", 'Makes for a great pool float.', 'Outdoor use only.']),
                Creature("zombie", "<:96_Zombie:822166015336644628>", CreatureType.STANDARD, CreatureCategory.MINECRAFT, ['Brains...', 'A classic mob.', "You're lucky it isn't a baby..."]),
                Creature("skeleton", "<:skeleton:822167956027998278>", CreatureType.STANDARD, CreatureCategory.MINECRAFT, ['i swear this thing has aimbot', 'Certified Bow Wielder.', 'b o n e s']),
                Creature("creeper", "<:Creeper:822168050891489320>", CreatureType.STANDARD, CreatureCategory.MINECRAFT, ['BOOM BOOM BOOM', "Minecraft's grim reaper.", 'Aww man!']),
                Creature("slime", "<:slime:902628695594893392>", CreatureType.STANDARD, CreatureCategory.MINECRAFT, ['Not the slimer.', 'Watch out for splitting!', "You didn't even have to dig out a slime chunk for this!"]),
                Creature("iron_golem", "<:iron_golem:902628865996890232>", CreatureType.STANDARD, CreatureCategory.MINECRAFT, ["You better take care of this creature! Don't go and make a three block tower or anything like that.", 'The ancestor of the copper golem.', 'Guardian of the villagers.']),
                Creature("enderman", "<:enderman:902628943365034044>", CreatureType.STANDARD, CreatureCategory.MINECRAFT, ["Look into its eyes! You'll get free stars!", 'Teleportation expert.', 'Found in every biome!']),
                Creature("villager", "<:villager:902629175268110377>", CreatureType.STANDARD, CreatureCategory.MINECRAFT, ['Loves to trade!', "Won't trade you stars, contrary to popular belief.", 'Keep away from zombies.']),
                Creature("pillager", "<:pillager:902629382730952714>", CreatureType.STANDARD, CreatureCategory.MINECRAFT, ['Get ready for a raid!', 'Can wield a variety of weapons!', 'Owner of the ravagers...']),
                Creature("ghast", "<:ghast:902629471574704199>", CreatureType.STANDARD, CreatureCategory.MINECRAFT, ['JUST RUN', 'Spits out fireballs at unfairly fast rates.', "IT'S A FLOATING WHITE CUBE."]),
                Creature("piglin", "<:piglin:902629758716747776>", CreatureType.STANDARD, CreatureCategory.MINECRAFT, ['I hope you checked your mods folder before recording...', 'Quick! Put on some gold boots!', "You either barter with em', or slaughter em'."]),
                Creature("wither", "<:wither:902629845341724742>", CreatureType.STANDARD, CreatureCategory.MINECRAFT, ['Just three wither skeleton heads, and voila!', "A wither! ...oh, it's not hostile.", 'You could craft a beacon by killing one of these.']),
                Creature("shulker", "<:shulker:902934568682811454>", CreatureType.STANDARD, CreatureCategory.MINECRAFT, ['*unintelligible shulker noises*', 'Get ready to float!', 'Found in the ancient end cities.']),
                Creature("magma_cube", "<:magma_cube:902934655894962237>", CreatureType.STANDARD, CreatureCategory.MINECRAFT, ["I hope you aren't in a basalt delta biome...", 'Good at splitting!', "Careful! They're hot!"]),
                Creature("silverfish", "<:silverfish:902934796819394630>", CreatureType.STANDARD, CreatureCategory.MINECRAFT, ["The only real animal mob that's hostile...", 'Could be hiding anywhere!', 'Make sure to break the spawner!']),
                Creature("guardian", "<:guardian:902934970866212884>", CreatureType.STANDARD, CreatureCategory.MINECRAFT, ['/summon minecraft:guardian', 'Beware of lasers!', 'Guards of the ocean monuments!']),
                Creature("mooshroom", "<:mooshroom:902935045520629894>", CreatureType.STANDARD, CreatureCategory.MINECRAFT, ['Found in the mysterious mushroom fields...', 'Just make sure not to use shears on him...', 'MUSHROOMS!!!']),
                Creature("popbob", "<:trollpopbob:902935189284597790>", CreatureType.STANDARD, CreatureCategory.MINECRAFT, ['The infamous 2b2t griefer!', "Don't let him get your base coordinates!", 'Go on. Build a base.']),
                Creature("skellybone", "<:unknown:904850861673566250>", CreatureType.STANDARD, CreatureCategory.MINECRAFT, ['There it is! The Skellybone head!', 'Certified MC Party coder.', "Half skelly, half bone!   ...wait, that doesn't make sense..."]),
                Creature("mammott", "<:Mammott:822180701398761562>", CreatureType.STANDARD, CreatureCategory.MY_SINGING_MONSTERS, ['Bom!', "It's with two T's!!!"]),
                Creature("toe_jammer", "<:Toe_Jammer:822180799356076042>", CreatureType.STANDARD, CreatureCategory.MY_SINGING_MONSTERS, ['Doo wop!']),
                Creature("noggin", "<:noggin:822181106165350470>", CreatureType.STANDARD, CreatureCategory.MY_SINGING_MONSTERS, ['How has he not had a concussion yet?']),
                Creature("tweedle", "<:tweedle:902936137155362847>", CreatureType.STANDARD, CreatureCategory.MY_SINGING_MONSTERS, ['Laa lala la laaaa!']),
                Creature("potbelly", "<:potbelly:902936233146220634>", CreatureType.STANDARD, CreatureCategory.MY_SINGING_MONSTERS, ['Owner of the famous restaurant, Potbelly.']),
                Creature("cybop", "<:cybop:902936405687304222>", CreatureType.STANDARD, CreatureCategory.MY_SINGING_MONSTERS, ["He's the scatman... but not a man!"]),
                Creature("quibble", "<:quibble:902936487941800027>", CreatureType.STANDARD, CreatureCategory.MY_SINGING_MONSTERS, ['2 beaks are better than one, maybe...']),
                Creature("pango", "<:pango:902936567964893185>", CreatureType.STANDARD, CreatureCategory.MY_SINGING_MONSTERS, []),
                Creature("shrubb", "<:shrubb:902936628539064370>", CreatureType.STANDARD, CreatureCategory.MY_SINGING_MONSTERS, ['Master at beatboxing.']),
                Creature("furcorn", "<:furcorn:822180968642642022>", CreatureType.STANDARD, CreatureCategory.MY_SINGING_MONSTERS, ['Has the voice of an angel.']),
                Creature("fwog", "<:fwog:902936696696471604>", CreatureType.STANDARD, CreatureCategory.MY_SINGING_MONSTERS, []),
                Creature("maw", "<:maw:822180873838657567>", CreatureType.STANDARD, CreatureCategory.MY_SINGING_MONSTERS, ['Dee dee!']),
                Creature("drumpler", "<:drumpler:902936777688485968>", CreatureType.STANDARD, CreatureCategory.MY_SINGING_MONSTERS, ['Professional drummer.']),
                Creature("reedling", "<:reedling:902936878003650580>", CreatureType.STANDARD, CreatureCategory.MY_SINGING_MONSTERS, []),
                Creature("thumpies", "<:thumpies:902936929178357840>", CreatureType.STANDARD, CreatureCategory.MY_SINGING_MONSTERS, []),
                Creature("scups", "<:scups:902937007955796048>", CreatureType.STANDARD, CreatureCategory.MY_SINGING_MONSTERS, []),
                Creature("bowgart", "<:bowgart:902937247853191230>", CreatureType.STANDARD, CreatureCategory.MY_SINGING_MONSTERS, []),
                Creature("pummel", "<:pummel:902937582084702209>", CreatureType.STANDARD, CreatureCategory.MY_SINGING_MONSTERS, ['That drum in its mouth has to be painful...']),
                Creature("entbrat", "<:entbrat:902937640175829032>", CreatureType.STANDARD, CreatureCategory.MY_SINGING_MONSTERS, []),
                Creature("deedge", "<:deedgee:902937703975374910>", CreatureType.STANDARD, CreatureCategory.MY_SINGING_MONSTERS, ['Pro DJ!', "What's it even supposed to be??"]),
                Creature("riff", "<:riff:902937755045220373>", CreatureType.STANDARD, CreatureCategory.MY_SINGING_MONSTERS, []),
                Creature("shellbeat", "<:shellbeat:902937928026705990>", CreatureType.STANDARD, CreatureCategory.MY_SINGING_MONSTERS, []),
                Creature("quarrister", "<:quarrister:902937992509927474>", CreatureType.STANDARD, CreatureCategory.MY_SINGING_MONSTERS, []),
                Creature("ghazt", "<:ghazt:902938137515425792>", CreatureType.STANDARD, CreatureCategory.MY_SINGING_MONSTERS, []),
                Creature("grumpyre", "<:grumpyre:902938242020671519>", CreatureType.STANDARD, CreatureCategory.MY_SINGING_MONSTERS, []),
                Creature("reebro", "<:reebro:902938303182041088>", CreatureType.STANDARD, CreatureCategory.MY_SINGING_MONSTERS, []),
                Creature("humbug", "<:humbug:902938388162818129>", CreatureType.STANDARD, CreatureCategory.MY_SINGING_MONSTERS, ['Buzz...']),
                Creature("brump", "<:brump:902938666245173281>", CreatureType.STANDARD, CreatureCategory.MY_SINGING_MONSTERS, ['Wake up the wublins!', "You won't need 6 furcorns and 2 fwogs for this one!", 'Produces a variety of rewards... if only shards is variety.']),
                Creature("dipster", "<:dipster:902938468529889412>", CreatureType.STANDARD, CreatureCategory.MY_SINGING_MONSTERS, ['Dip!', 'One for every note!', 'You unlock these from... keys?']),
                Creature("wubbox", "<:wubbox:902938566672416828>", CreatureType.STANDARD, CreatureCategory.MY_SINGING_MONSTERS, ["Doesn't need the other creatures to power up! (Thankfully)", 'Master of dubstep.', 'bwomp']),
                Creature("julius", "<:Julius:903000291497115648>", CreatureType.STANDARD, CreatureCategory.MISC, ['1 yr old', 'You just copped Julius!', 'Commonly found on Ebay.']),
                Creature("waddle_dee", "<:waddle_dee:822192409047203871>", CreatureType.STANDARD, CreatureCategory.MISC, ['Surprisingly good at building towns.', '5/5 Red Tulips found!', 'Would look good with a bandana.']),
                Creature("bronto_burt", "<:bronto_burt:822193190739116103>", CreatureType.STANDARD, CreatureCategory.MISC, ['Usually come in groups... but not this time.', 'Equipped with wings!', 'Might try to chase you.']),
                Creature("scarfy", "<:scarfy:822192583924908032>", CreatureType.STANDARD, CreatureCategory.MISC, ['You better not pick up that key.', 'Make for great guards.', "How cute! I'm sure nothing would change that!"]),
                Creature("kabu", "<:kabu:822193043380633620>", CreatureType.STANDARD, CreatureCategory.MISC, ['WARP STAR', 'Spinning... Spinning...', 'Looks ancient.']),
                Creature("cappy", "<:cappy:822192814099398668>", CreatureType.STANDARD, CreatureCategory.MISC, ['Not to be confused with a different cappy...', 'Equipped with a mushroom cap!', 'Totally not a haniwa statue in disguise.']),
                Creature("gordo", "<:gordo:822192253975920650>", CreatureType.STANDARD, CreatureCategory.MISC, ['Can you imagine if one of these things was long?', 'Covered in spikes!', 'Might not want to pet one of these...']),
                Creature("small_guy", "<:FG_smallguy:822846481291673650>", CreatureType.STANDARD, CreatureCategory.MISC, ['An abomination.', 'Ready to take on the blunderdome!', 'Fall guy... goomba?']),
                Creature("fall_guy", "<:FG_pinkhype:822846554749927434>", CreatureType.STANDARD, CreatureCategory.MISC, ['Woo woo woo!', 'Ready to win!', 'Keep away from slime.']),
                Creature("chained", "<:Player:902999086448394312>", CreatureType.STANDARD, CreatureCategory.MISC, ['Can chain a ton of enemies!', 'Kind of looks like this other red guy...', 'A character lost to time...']),
                Creature("enemy", "<:GroundEnemy1:902999159638986802>", CreatureType.STANDARD, CreatureCategory.MISC, ['Could honestly be interchangeable with a vegetable or something.', 'An enemy lost to time...', 'Weak to stomps.']),
                Creature("fast_enemy", "<:GroundEnemy2:902999204543213638>", CreatureType.STANDARD, CreatureCategory.MISC, ['An enemy lost to time... but fast', 'Ready to run a marathon!', 'These things can get FAST.']),
                Creature("diogenes", "<:diogenes:902999548471967805>", CreatureType.STANDARD, CreatureCategory.MISC, ['Can climb any mountain!', 'Adobe stock man 1', 'You got sooooo close, but this is past mending. You got the bad ending.']),
                Creature("slurpee", "<:slurpee:903000058855845928>", CreatureType.STANDARD, CreatureCategory.MISC, ["Let's hope this slurpee doesn't end up being lethal.", 'Available at your local 7/11 for only $1.79!', 'Comes in many flavors!']),
                Creature("baldness", "<:baldness:903000109430751283>", CreatureType.STANDARD, CreatureCategory.MISC, ['10/14', 'Bald is beautiful.', "He's bald! This is incredible!"]),
                Creature("smallfry", "<:smallfry:1026576000588447754>", CreatureType.STANDARD, CreatureCategory.MISC, ["IT'S HIM", 'Professional Flyfish pilot.', 'Loves power eggs!']),
                Creature("blob", "<:blob:822845680170041404>", CreatureType.STANDARD, CreatureCategory.MISC, ['Bedtime for blobby.', 'Keep all goo away!', 'zzzzzzzzz...']),
                Creature("impostor", "<:crewmate_red:822846201271418941>", CreatureType.STANDARD, CreatureCategory.MISC, ['Will use your vents.', 'looking kinda sus ngl', 'Can and will shapeshift.']),
                Creature("crewmate", "<:crewmate_blue:822846167959994408>", CreatureType.STANDARD, CreatureCategory.MISC, ['What an innocent little crewmate!', 'Completes tasks on the daily.', 'Go watch it scan!']),
                Creature("brainslug", "<:brainslug:822846224440754217>", CreatureType.STANDARD, CreatureCategory.MISC, ['May or may not suck your brains out.', 'Could be a hat or a pet. You decide.', 'Look at this little guy! Must be completely harmless!']),
                Creature("trollget", "<:trollgetHD:822848784957702164>", CreatureType.STANDARD, CreatureCategory.MISC, ['oh my god.', 'Now in HD!', 'I hope this was worth the stars.']),
                Creature("nugget", "<:nugget:822848764477046794>", CreatureType.STANDARD, CreatureCategory.MISC, ['Printed and taped all over!', '...you kidnapped nugget!', "What an innocent child! I sure hope they don't make any rude hand gestures!"]),
                Creature("bloon", "<:red_bloon:822848835432349727>", CreatureType.STANDARD, CreatureCategory.MISC, ["Don't let it reach the end of the track!", 'Weak to darts.', "Ever think you're useless? You should see one of the red bloons with regen."]),
                Creature("cheems", "<:cheems:822849570924920853>", CreatureType.STANDARD, CreatureCategory.MISC, ['Owie!', 'The bonk man.', 'An original character, created by cheme himself!']),
                Creature("tack_shooter", "<:tack_btd6:822849596416983050>", CreatureType.STANDARD, CreatureCategory.MISC, ['Commonly placed in the corner of maps.', 'Shoots in 8 directions!', 'laugh.']),
                Creature("mover", "<:move_or_die:822850410317873222>", CreatureType.STANDARD, CreatureCategory.MISC, ['Mooooove!', "Whatever you do, DON'T pick ghostly jumps!", '*readys and unreadys at rapid speeds*']),
                Creature("jackbox", "<:jackbox:902939403134074901>", CreatureType.STANDARD, CreatureCategory.MISC, ['Need a safety quip?', "IT'S FREE YOU DON'T NEED TO BUY IT TO PLAY", 'Try to have a few people in vc before pinging!']),
                Creature("troll", "<:troll:821796703896076318>", CreatureType.STANDARD, CreatureCategory.MISC, ['Get trolled!', 'Trololololololololol', 'You can find this face on pretty much anything if you look hard enough.']),
                Creature("meebling", "<:meebling:821796521351315507>", CreatureType.STANDARD, CreatureCategory.MISC, ['Comes in all different colors!', 'TO ME!!!', 'Expired January 12th, 2021.']),
                Creature("sad_guy", "<:uuu:822850969619922944>", CreatureType.STANDARD, CreatureCategory.MISC, ['uuu', "Why's he so sad?", 'You better cheer him up!']),
                Creature("clown", "🤡", CreatureType.STANDARD, CreatureCategory.MISC, ['Did you just collect yourself as a creature?', 'Quite the jokester.', 'Laugh.']),
                Creature("shiny_camel", "<a:cam:825848294068453386>", CreatureType.SHINY, CreatureCategory.MAMMAL, ["That's a lot of humps..."]),
                Creature("shiny_cat", "<a:ca:1029440166038863902>", CreatureType.SHINY, CreatureCategory.MAMMAL, ['HI PI']),
                Creature("shiny_chipmunk", "<a:ALVIN:825851263686148169>", CreatureType.SHINY, CreatureCategory.MAMMAL, ['ALVIIIIIIIN!!!!!!!!']),
                Creature("shiny_cow", "<a:cow:825848170474766376>", CreatureType.SHINY, CreatureCategory.MAMMAL, ['Provides the best food source.']),
                Creature("shiny_dinosaur", "<a:dino:825842214486802474>", CreatureType.SHINY, CreatureCategory.MAMMAL, ['Seems pretty stressed out.']),
                Creature("shiny_dog", "<a:alex:824401217878622208>", CreatureType.SHINY, CreatureCategory.MAMMAL, ['A Shiny Alex Appears!']),
                Creature("shiny_elephant", "<a:el:825847177695068191>", CreatureType.SHINY, CreatureCategory.MAMMAL, ['Now orange!']),
                Creature("shiny_giraffe", "<a:gir:825847373791100958>", CreatureType.SHINY, CreatureCategory.MAMMAL, ["This is real and there's nothing you can do about it."]),
                Creature("shiny_goat", "<a:go:825849600010223656>", CreatureType.SHINY, CreatureCategory.MAMMAL, ['*aggressively screams*']),
                Creature("golden_bird", "<a:goldenb:1032673419084439662>", CreatureType.GOLDEN, CreatureCategory.GOLDEN, []),
                Creature("golden_strawberry", "<:strawberry:904861657665273936>", CreatureType.GOLDEN, CreatureCategory.GOLDEN, []),
                Creature("golden_dragon", "🐉", CreatureType.GOLDEN, CreatureCategory.GOLDEN, []),
                Creature("golden_blob", "<:blob:822845680170041404>", CreatureType.GOLDEN, CreatureCategory.GOLDEN, []),
                Creature("golden_fuzzy", "<:fuzzy:902622386560573471>", CreatureType.GOLDEN, CreatureCategory.GOLDEN, []),
]
