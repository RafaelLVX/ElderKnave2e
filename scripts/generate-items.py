"""
Generate separate category JSON files for Elder Knave compendium.
Outputs: packs/CoreKnave2e/items-{category}.json (6 files)
Run this to regenerate all items from scratch.
"""

import json
import os

# Define categories (no folders needed - separate packs handle categorization)
CATEGORIES = ["animals", "armor", "clothing", "light", "melee", "missile", "other"]

# Define all items with their properties and folder assignments
items_data = {
    # ============= MELEE WEAPONS =============
    "Axe": {"type": "weapon", "folder": "melee", "category": "melee", "slots": 2, "cost": 100, "ammoType": "none", "range": 5, "damageRoll": "1d8"},
    "Cleaver": {"type": "weapon", "folder": "melee", "category": "melee", "slots": 1, "cost": 50, "ammoType": "none", "range": 5, "damageRoll": "1d6"},
    "Crook": {"type": "weapon", "folder": "melee", "category": "melee", "slots": 1, "cost": 50, "ammoType": "none", "range": 5, "damageRoll": "1d6"},
    "Dagger": {"type": "weapon", "folder": "melee", "category": "melee", "slots": 1, "cost": 50, "ammoType": "none", "range": 5, "damageRoll": "1d6"},
    "Halberd": {"type": "weapon", "folder": "melee", "category": "melee", "slots": 2, "cost": 100, "ammoType": "none", "range": 5, "damageRoll": "1d8"},
    "Hatchet": {"type": "weapon", "folder": "melee", "category": "melee", "slots": 1, "cost": 50, "ammoType": "none", "range": 5, "damageRoll": "1d6"},
    "Longsword": {"type": "weapon", "folder": "melee", "category": "melee", "slots": 2, "cost": 100, "ammoType": "none", "range": 5, "damageRoll": "1d8"},
    "Mace": {"type": "weapon", "folder": "melee", "category": "melee", "slots": 1, "cost": 50, "ammoType": "none", "range": 5, "damageRoll": "1d6"},
    "Maul": {"type": "weapon", "folder": "melee", "category": "melee", "slots": 2, "cost": 100, "ammoType": "none", "range": 5, "damageRoll": "1d8"},
    "Morning Star": {"type": "weapon", "folder": "melee", "category": "melee", "slots": 1, "cost": 50, "ammoType": "none", "range": 5, "damageRoll": "1d6"},
    "Rapier": {"type": "weapon", "folder": "melee", "category": "melee", "slots": 1, "cost": 50, "ammoType": "none", "range": 5, "damageRoll": "1d6"},
    "Short Sword": {"type": "weapon", "folder": "melee", "category": "melee", "slots": 1, "cost": 50, "ammoType": "none", "range": 5, "damageRoll": "1d6"},
    "Sickle": {"type": "weapon", "folder": "melee", "category": "melee", "slots": 1, "cost": 50, "ammoType": "none", "range": 5, "damageRoll": "1d6"},
    "Spear": {"type": "weapon", "folder": "melee", "category": "melee", "slots": 1, "cost": 50, "ammoType": "none", "range": 5, "damageRoll": "1d6"},
    "Staff": {"type": "weapon", "folder": "melee", "category": "melee", "slots": 1, "cost": 50, "ammoType": "none", "range": 5, "damageRoll": "1d6"},
    "Whip": {"type": "weapon", "folder": "melee", "category": "melee", "slots": 1, "cost": 50, "ammoType": "none", "range": 5, "damageRoll": "1d6"},
    
    # ============= MISSILE WEAPONS =============
    "Bow": {"type": "weapon", "folder": "missile", "category": "missile", "slots": 2, "cost": 100, "ammoType": "arrow", "range": 120, "damageRoll": "1d6"},
    "Crossbow": {"type": "weapon", "folder": "missile", "category": "missile", "slots": 2, "cost": 100, "ammoType": "arrow", "range": 120, "damageRoll": "1d6"},
    "Sling": {"type": "weapon", "folder": "missile", "category": "missile", "slots": 1, "cost": 50, "ammoType": "stone", "range": 60, "damageRoll": "1d4"},
    
    # ============= ARMOR =============
    "Arm Plate": {"type": "armor", "folder": "armor", "category": "armPlate", "slots": 1, "cost": 500, "armorPoints": 1, "equipped": True},
    "Breastplate": {"type": "armor", "folder": "armor", "category": "breastplate", "slots": 1, "cost": 500, "armorPoints": 1, "equipped": True},
    "Gambeson": {"type": "armor", "folder": "armor", "category": "gambeson", "slots": 1, "cost": 100, "armorPoints": 1, "equipped": True},
    "Helmet": {"type": "armor", "folder": "armor", "category": "helmet", "slots": 1, "cost": 100, "armorPoints": 1, "equipped": True},
    "Leg Plate": {"type": "armor", "folder": "armor", "category": "legPlate", "slots": 1, "cost": 500, "armorPoints": 1, "equipped": True},
    "Mail Shirt": {"type": "armor", "folder": "armor", "category": "mailShirt", "slots": 1, "cost": 200, "armorPoints": 1, "equipped": True},
    "Shield": {"type": "armor", "folder": "armor", "category": "shield", "slots": 1, "cost": 100, "armorPoints": 1, "equipped": True},
    
    # ============= LIGHT SOURCES =============
    "Candle": {"type": "lightSource", "folder": "light", "category": "torch", "slots": 1, "cost": 5, "quantity": 10, "lit": False, "dimRadius": 10, "brightRadius": 5, "intensity": 2, "speed": 1},
    "Lantern": {"type": "lightSource", "folder": "light", "category": "torch", "slots": 1, "cost": 20, "lit": False, "dimRadius": 30, "brightRadius": 15, "intensity": 4, "speed": 2},
    "Torch": {"type": "lightSource", "folder": "light", "category": "torch", "slots": 1, "cost": 5, "lit": False, "dimRadius": 20, "brightRadius": 10, "intensity": 3, "speed": 3},
    
    # ============= ANIMALS =============
    "Cow": {"type": "equipment", "folder": "animals", "slots": 4, "cost": 100},
    "Dog": {"type": "equipment", "folder": "animals", "slots": 2, "cost": 20},
    "Falcon": {"type": "equipment", "folder": "animals", "slots": 1, "cost": 1000},
    "Goat": {"type": "equipment", "folder": "animals", "slots": 2, "cost": 20},
    "Pig": {"type": "equipment", "folder": "animals", "slots": 2, "cost": 20},
    "Poultry": {"type": "equipment", "folder": "animals", "slots": 1, "cost": 5},
    
    # ============= CLOTHING =============
    "Arcane Robes": {"type": "equipment", "folder": "clothing", "slots": 1, "cost": 240},
    "Costume": {"type": "equipment", "folder": "clothing", "slots": 1, "cost": 120},
    "Fancy Robe": {"type": "equipment", "folder": "clothing", "slots": 1, "cost": 300},
    "Fancy Shoes": {"type": "equipment", "folder": "clothing", "slots": 1, "cost": 300},
    "Gloves": {"type": "equipment", "folder": "clothing", "slots": 1, "cost": 10},
    "Hood": {"type": "equipment", "folder": "clothing", "slots": 1, "cost": 10},
    "Humble Clothes": {"type": "equipment", "folder": "clothing", "slots": 1, "cost": 120},
    "Major Noble Clothes": {"type": "equipment", "folder": "clothing", "slots": 1, "cost": 12000},
    "Minor Noble Clothes": {"type": "equipment", "folder": "clothing", "slots": 1, "cost": 2400},
    "Poor Clothes": {"type": "equipment", "folder": "clothing", "slots": 1, "cost": 60},
    "Respectable Clothes": {"type": "equipment", "folder": "clothing", "slots": 1, "cost": 240},
    "Ritual Robes": {"type": "equipment", "folder": "clothing", "slots": 1, "cost": 120},
    "Royal Clothes": {"type": "equipment", "folder": "clothing", "slots": 1, "cost": 120000},
    "Vestments (official)": {"type": "equipment", "folder": "clothing", "slots": 1, "cost": 200},
    "Wealthy Clothes": {"type": "equipment", "folder": "clothing", "slots": 1, "cost": 600},
    
    # ============= EQUIPMENT - COMMON (5c) =============
    "Bacon": {"type": "equipment", "folder": "other", "slots": 1, "cost": 5},
    "Balls": {"type": "equipment", "folder": "other", "slots": 1, "cost": 5},
    "Basket": {"type": "equipment", "folder": "other", "slots": 1, "cost": 5},
    "Bellows": {"type": "equipment", "folder": "other", "slots": 1, "cost": 5},
    "Black Grease": {"type": "equipment", "folder": "other", "slots": 1, "cost": 5},
    "Blanket": {"type": "equipment", "folder": "other", "slots": 1, "cost": 5},
    "Bones": {"type": "equipment", "folder": "other", "slots": 1, "cost": 5},
    "Box of Nails": {"type": "equipment", "folder": "other", "slots": 1, "cost": 5},
    "Bucket": {"type": "equipment", "folder": "other", "slots": 1, "cost": 5},
    "Candlestick": {"type": "equipment", "folder": "other", "slots": 1, "cost": 5},
    "Card Deck": {"type": "equipment", "folder": "other", "slots": 1, "cost": 5},
    "Chalk": {"type": "equipment", "folder": "other", "slots": 1, "cost": 5},
    "Clay": {"type": "equipment", "folder": "other", "slots": 1, "cost": 5},
    "Confetti": {"type": "equipment", "folder": "other", "slots": 1, "cost": 5},
    "Dice": {"type": "equipment", "folder": "other", "slots": 1, "cost": 5},
    "Dyes": {"type": "equipment", "folder": "other", "slots": 1, "cost": 5},
    "Firewood": {"type": "equipment", "folder": "other", "slots": 1, "cost": 5},
    "Flour Bag": {"type": "equipment", "folder": "other", "slots": 1, "cost": 5},
    "Fungi": {"type": "equipment", "folder": "other", "slots": 1, "cost": 5},
    "Glue": {"type": "equipment", "folder": "other", "slots": 1, "cost": 5},
    "Hammer": {"type": "equipment", "folder": "other", "slots": 1, "cost": 5},
    "Herbs": {"type": "equipment", "folder": "other", "slots": 1, "cost": 5},
    "Hops": {"type": "equipment", "folder": "other", "slots": 1, "cost": 5},
    "Incense": {"type": "equipment", "folder": "other", "slots": 1, "cost": 5},
    "Iron Spikes": {"type": "equipment", "folder": "other", "slots": 1, "cost": 5},
    "Ladle": {"type": "equipment", "folder": "other", "slots": 1, "cost": 5},
    "Lamp Oil": {"type": "equipment", "folder": "other", "slots": 1, "cost": 5},
    "Lard Block": {"type": "equipment", "folder": "other", "slots": 1, "cost": 5},
    "Leash": {"type": "equipment", "folder": "other", "slots": 1, "cost": 5},
    "Marbles": {"type": "equipment", "folder": "other", "slots": 1, "cost": 5, "quantity": 100},
    "Mash Paddle": {"type": "equipment", "folder": "other", "slots": 1, "cost": 5},
    "Oats": {"type": "equipment", "folder": "other", "slots": 1, "cost": 5},
    "Paddle": {"type": "equipment", "folder": "other", "slots": 1, "cost": 5},
    "Poker": {"type": "equipment", "folder": "other", "slots": 1, "cost": 5},
    "Quiver": {"type": "equipment", "folder": "other", "slots": 1, "cost": 5},
    "Ration": {"type": "equipment", "folder": "other", "slots": 1, "cost": 5},
    "Rolling Pin": {"type": "equipment", "folder": "other", "slots": 1, "cost": 5},
    "Rope, 50 ft": {"type": "equipment", "folder": "other", "slots": 1, "cost": 5},
    "Ruler": {"type": "equipment", "folder": "other", "slots": 1, "cost": 5},
    "Sack": {"type": "equipment", "folder": "other", "slots": 1, "cost": 5},
    "Salt": {"type": "equipment", "folder": "other", "slots": 1, "cost": 5},
    "Saw": {"type": "equipment", "folder": "other", "slots": 1, "cost": 5},
    "Sealing Wax": {"type": "equipment", "folder": "other", "slots": 1, "cost": 5},
    "Shoe Polish": {"type": "equipment", "folder": "other", "slots": 1, "cost": 5},
    "Shovel": {"type": "equipment", "folder": "other", "slots": 1, "cost": 5},
    "Skull": {"type": "equipment", "folder": "other", "slots": 1, "cost": 5},
    "Soap": {"type": "equipment", "folder": "other", "slots": 1, "cost": 5},
    "Soot Pot": {"type": "equipment", "folder": "other", "slots": 1, "cost": 5},
    "Sponge": {"type": "equipment", "folder": "other", "slots": 1, "cost": 5},
    "Stakes": {"type": "equipment", "folder": "other", "slots": 1, "cost": 5, "quantity": 10},
    "Stationery": {"type": "equipment", "folder": "other", "slots": 1, "cost": 5},
    "Tacks": {"type": "equipment", "folder": "other", "slots": 1, "cost": 5},
    "Tongs": {"type": "equipment", "folder": "other", "slots": 1, "cost": 5},
    "Twine, 300 ft": {"type": "equipment", "folder": "other", "slots": 1, "cost": 5},
    "Wax": {"type": "equipment", "folder": "other", "slots": 1, "cost": 5},
    "Whistle": {"type": "equipment", "folder": "other", "slots": 1, "cost": 5},
    
    # ============= EQUIPMENT - UNCOMMON (20c) =============
    "Acid": {"type": "equipment", "folder": "other", "slots": 1, "cost": 20},
    "Bear Trap": {"type": "equipment", "folder": "other", "slots": 1, "cost": 20},
    "Beer Keg": {"type": "equipment", "folder": "other", "slots": 2, "cost": 20},
    "Bird Cage": {"type": "equipment", "folder": "other", "slots": 1, "cost": 20},
    "Bullhorn": {"type": "equipment", "folder": "other", "slots": 1, "cost": 20},
    "Cage": {"type": "equipment", "folder": "other", "slots": 2, "cost": 20},
    "Calipers": {"type": "equipment", "folder": "other", "slots": 1, "cost": 20},
    "Caltrops": {"type": "equipment", "folder": "other", "slots": 1, "cost": 20},
    "Cannonball": {"type": "equipment", "folder": "other", "slots": 1, "cost": 20},
    "Cauldron": {"type": "equipment", "folder": "other", "slots": 2, "cost": 20},
    "Chain": {"type": "equipment", "folder": "other", "slots": 1, "cost": 20},
    "Chisel": {"type": "equipment", "folder": "other", "slots": 1, "cost": 20},
    "Chloroform": {"type": "equipment", "folder": "other", "slots": 1, "cost": 20},
    "Crowbar": {"type": "equipment", "folder": "other", "slots": 1, "cost": 20},
    "Drill": {"type": "equipment", "folder": "other", "slots": 1, "cost": 20},
    "File": {"type": "equipment", "folder": "other", "slots": 1, "cost": 20},
    "Fishing Tackle": {"type": "equipment", "folder": "other", "slots": 1, "cost": 20},
    "Flash Powder": {"type": "equipment", "folder": "other", "slots": 1, "cost": 20},
    "Garrote": {"type": "equipment", "folder": "other", "slots": 1, "cost": 20},
    "Grappling Hook": {"type": "equipment", "folder": "other", "slots": 1, "cost": 20},
    "Holy Water": {"type": "equipment", "folder": "other", "slots": 1, "cost": 20},
    "Horn": {"type": "equipment", "folder": "other", "slots": 1, "cost": 20},
    "Local Map": {"type": "equipment", "folder": "other", "slots": 1, "cost": 20},
    "Lockpicks": {"type": "equipment", "folder": "other", "slots": 1, "cost": 20},
    "Manacles": {"type": "equipment", "folder": "other", "slots": 1, "cost": 20},
    "Meat Hook": {"type": "equipment", "folder": "other", "slots": 1, "cost": 20},
    "Motley": {"type": "equipment", "folder": "other", "slots": 1, "cost": 20},
    "Needles": {"type": "equipment", "folder": "other", "slots": 1, "cost": 20},
    "Net": {"type": "equipment", "folder": "other", "slots": 1, "cost": 20},
    "Oilskin Bag": {"type": "equipment", "folder": "other", "slots": 1, "cost": 20},
    "Padlock": {"type": "equipment", "folder": "other", "slots": 1, "cost": 20},
    "Pickaxe": {"type": "equipment", "folder": "other", "slots": 1, "cost": 20},
    "Pigments": {"type": "equipment", "folder": "other", "slots": 1, "cost": 20},
    "Pliers": {"type": "equipment", "folder": "other", "slots": 1, "cost": 20},
    "Pulleys": {"type": "equipment", "folder": "other", "slots": 1, "cost": 20},
    "Quill/Ink": {"type": "equipment", "folder": "other", "slots": 1, "cost": 20},
    "Rat Traps": {"type": "equipment", "folder": "other", "slots": 1, "cost": 20},
    "Scales": {"type": "equipment", "folder": "other", "slots": 1, "cost": 20},
    "Scalpel": {"type": "equipment", "folder": "other", "slots": 1, "cost": 20},
    "Scissors": {"type": "equipment", "folder": "other", "slots": 1, "cost": 20},
    "Shears": {"type": "equipment", "folder": "other", "slots": 1, "cost": 20},
    "Smoke Bomb": {"type": "equipment", "folder": "other", "slots": 1, "cost": 20},
    "Tent": {"type": "equipment", "folder": "other", "slots": 2, "cost": 20},
    "Trumpet": {"type": "equipment", "folder": "other", "slots": 1, "cost": 20},
    "Tweezers": {"type": "equipment", "folder": "other", "slots": 1, "cost": 20},
    "Wig": {"type": "equipment", "folder": "other", "slots": 1, "cost": 20},
    "Wine Jug (full)": {"type": "equipment", "folder": "other", "slots": 1, "cost": 20},
    
    # ============= EQUIPMENT - RARE (100c+) =============
    "Astrolabe": {"type": "equipment", "folder": "other", "slots": 1, "cost": 150},
    "Hourglass": {"type": "equipment", "folder": "other", "slots": 1, "cost": 100},
    "Sextant": {"type": "equipment", "folder": "other", "slots": 1, "cost": 250},
    "Spyglass": {"type": "equipment", "folder": "other", "slots": 1, "cost": 100},
    "Telescope": {"type": "equipment", "folder": "other", "slots": 1, "cost": 120},
    "Vials (6)": {"type": "equipment", "folder": "other", "slots": 1, "cost": 100},
    
    # ============= EQUIPMENT - OTHER (Career/Lifestyle items) =============
    "Air Bladder": {"type": "equipment", "folder": "other", "slots": 1, "cost": 15},
    "Almanac": {"type": "equipment", "folder": "other", "slots": 1, "cost": 30},
    "Amulet": {"type": "equipment", "folder": "other", "slots": 1, "cost": 25},
    "Animal Scent": {"type": "equipment", "folder": "other", "slots": 1, "cost": 10},
    "Armor Polish": {"type": "equipment", "folder": "other", "slots": 1, "cost": 10},
    "Bag of Spice": {"type": "equipment", "folder": "other", "slots": 1, "cost": 25},
    "Banner": {"type": "equipment", "folder": "other", "slots": 1, "cost": 30},
    "Bear Pelt": {"type": "equipment", "folder": "other", "slots": 2, "cost": 40},
    "Bearskin": {"type": "equipment", "folder": "other", "slots": 2, "cost": 35},
    "Beeswax": {"type": "equipment", "folder": "other", "slots": 1, "cost": 10},
    "Bell": {"type": "equipment", "folder": "other", "slots": 1, "cost": 15},
    "Bomb": {"type": "equipment", "folder": "other", "slots": 1, "cost": 50},
    "Brushes": {"type": "equipment", "folder": "other", "slots": 1, "cost": 10},
    "Censer": {"type": "equipment", "folder": "other", "slots": 1, "cost": 25},
    "Certificate": {"type": "equipment", "folder": "other", "slots": 1, "cost": 20},
    "Crampons": {"type": "equipment", "folder": "other", "slots": 1, "cost": 25},
    "Crystal": {"type": "equipment", "folder": "other", "slots": 1, "cost": 30},
    "Degree (fake document)": {"type": "equipment", "folder": "other", "slots": 1, "cost": 20},
    "Donkey Head (costume)": {"type": "equipment", "folder": "other", "slots": 1, "cost": 10},
    "Fake Elixir": {"type": "equipment", "folder": "other", "slots": 1, "cost": 15},
    "Fan": {"type": "equipment", "folder": "other", "slots": 1, "cost": 15},
    "Flag": {"type": "equipment", "folder": "other", "slots": 1, "cost": 20},
    "Forged Papers": {"type": "equipment", "folder": "other", "slots": 1, "cost": 30},
    "Fossil": {"type": "equipment", "folder": "other", "slots": 1, "cost": 25},
    "Frying Pan": {"type": "equipment", "folder": "other", "slots": 1, "cost": 10},
    "Geode": {"type": "equipment", "folder": "other", "slots": 1, "cost": 20},
    "Hair Oil": {"type": "equipment", "folder": "other", "slots": 1, "cost": 10},
    "Herb Manual": {"type": "equipment", "folder": "other", "slots": 1, "cost": 30},
    "Honey": {"type": "equipment", "folder": "other", "slots": 1, "cost": 15},
    "Insect Case": {"type": "equipment", "folder": "other", "slots": 1, "cost": 20},
    "Instrument": {"type": "equipment", "folder": "other", "slots": 1, "cost": 30},
    "Journal": {"type": "equipment", "folder": "other", "slots": 1, "cost": 15},
    "Lady's Favor": {"type": "equipment", "folder": "other", "slots": 1, "cost": 10},
    "Law Book": {"type": "equipment", "folder": "other", "slots": 1, "cost": 40},
    "Level": {"type": "equipment", "folder": "other", "slots": 1, "cost": 15},
    "Linseed Oil": {"type": "equipment", "folder": "other", "slots": 1, "cost": 10},
    "Livery": {"type": "equipment", "folder": "other", "slots": 1, "cost": 30},
    "Locket": {"type": "equipment", "folder": "other", "slots": 1, "cost": 20},
    "Lockbox": {"type": "equipment", "folder": "other", "slots": 1, "cost": 35},
    "Lore Book": {"type": "equipment", "folder": "other", "slots": 1, "cost": 40},
    "Loupe": {"type": "equipment", "folder": "other", "slots": 1, "cost": 25},
    "Makeup": {"type": "equipment", "folder": "other", "slots": 1, "cost": 15},
    "Manual": {"type": "equipment", "folder": "other", "slots": 1, "cost": 30},
    "Mask": {"type": "equipment", "folder": "other", "slots": 1, "cost": 15},
    "Medal": {"type": "equipment", "folder": "other", "slots": 1, "cost": 25},
    "Mirror": {"type": "equipment", "folder": "other", "slots": 1, "cost": 20},
    "Mortar/Pestle": {"type": "equipment", "folder": "other", "slots": 1, "cost": 15},
    "Oilskin Coat": {"type": "equipment", "folder": "other", "slots": 1, "cost": 25},
    "Old Coin": {"type": "equipment", "folder": "other", "slots": 1, "cost": 1},
    "Olive Oil": {"type": "equipment", "folder": "other", "slots": 1, "cost": 10},
    "Pan": {"type": "equipment", "folder": "other", "slots": 1, "cost": 10},
    "Perfume": {"type": "equipment", "folder": "other", "slots": 1, "cost": 20},
    "Pet Canary": {"type": "equipment", "folder": "other", "slots": 1, "cost": 15},
    "Plumb Line": {"type": "equipment", "folder": "other", "slots": 1, "cost": 10},
    "Poison": {"type": "equipment", "folder": "other", "slots": 1, "cost": 30},
    "Prayer Book": {"type": "equipment", "folder": "other", "slots": 1, "cost": 25},
    "Puppet": {"type": "equipment", "folder": "other", "slots": 1, "cost": 15},
    "Relic": {"type": "equipment", "folder": "other", "slots": 1, "cost": 100},
    "Rope Ladder": {"type": "equipment", "folder": "other", "slots": 2, "cost": 15},
    "Scepter": {"type": "equipment", "folder": "other", "slots": 1, "cost": 30},
    "Signet Ring": {"type": "equipment", "folder": "other", "slots": 1, "cost": 50},
    "Signal Flags": {"type": "equipment", "folder": "other", "slots": 1, "cost": 15},
    "Silverware": {"type": "equipment", "folder": "other", "slots": 1, "cost": 20},
    "Soft Boots": {"type": "equipment", "folder": "other", "slots": 1, "cost": 20},
    "Spell Book": {"type": "spellbook", "folder": "other", "slots": 1, "cost": 250, "tier": "novice"},
    "Star Charts": {"type": "equipment", "folder": "other", "slots": 1, "cost": 30},
    "Straight Razor": {"type": "equipment", "folder": "other", "slots": 1, "cost": 10},
    "Strongbox": {"type": "equipment", "folder": "other", "slots": 2, "cost": 40},
    "Tarot Deck": {"type": "equipment", "folder": "other", "slots": 1, "cost": 25},
    "Tea Leaves": {"type": "equipment", "folder": "other", "slots": 1, "cost": 10},
    "Wax Tablet": {"type": "equipment", "folder": "other", "slots": 1, "cost": 10},
}

def generate_items():
    """Generate complete items array with proper formatting."""
    output = []
    
    # Generate items sorted alphabetically by name
    for name in sorted(items_data.keys()):
        props = items_data[name]
        
        # Generate ID from name
        item_id = "ck2e-items-{0}".format(
            name.lower()
                .replace(' ', '-')
                .replace(',', '')
                .replace('/', '-')
                .replace('(', '')
                .replace(')', '')
        )
        
        # Get category/folder for organization
        folder_key = props.get("folder", "other")  # Use "folder" field for categorization
        
        # Base item structure
        item = {
            "_id": item_id,
            "name": name,
            "type": props["type"],
            "img": get_icon(props["type"], props.get("category")),
            "folder": folder_key,  # Keep temporarily for categorization
            "system": {
                "quantity": props.get("quantity", 1),
                "slots": props["slots"],
                "cost": props["cost"],
                "description": "<p>{0}</p>".format(props.get('desc', '')),
                "relic": {"isRelic": False, "isActive": False}
            }
        }
        
        # Add type-specific properties
        if props["type"] == "weapon":
            item["system"].update({
                "category": props["category"],
                "ammoType": props["ammoType"],
                "range": props["range"],
                "attackBonus": 0,
                "damageRoll": props["damageRoll"]
            })
        elif props["type"] == "armor":
            item["system"].update({
                "category": props["category"],
                "armorPoints": props["armorPoints"],
                "equipped": props["equipped"]
            })
        elif props["type"] == "lightSource":
            item["system"].update({
                "category": props["category"],
                "lit": props["lit"],
                "dimRadius": props["dimRadius"],
                "brightRadius": props["brightRadius"],
                "intensity": props["intensity"],
                "speed": props["speed"]
            })
        elif props["type"] == "spellbook":
            item["system"]["tier"] = props["tier"]
        
        output.append(item)
    
    return output

def get_icon(item_type, category=None):
    """Return appropriate icon path for item type."""
    # Special handling for missile weapons
    if item_type == "weapon" and category == "missile":
        return "icons/svg/target.svg"
    
    icons = {
        "weapon": "icons/svg/sword.svg",
        "armor": "icons/svg/shield.svg",
        "lightSource": "icons/svg/light.svg",
        "spellbook": "icons/svg/book.svg",
        "equipment": "icons/svg/item-bag.svg"
    }
    return icons.get(item_type, "icons/svg/item-bag.svg")

def main():
    """Main execution function - generates separate category JSON files."""
    all_items = generate_items()
    
    # Organize items by category
    categories = {cat: [] for cat in CATEGORIES}
    
    for item in all_items:
        # Determine category from folder field (old structure compatibility)
        folder = item.get("folder", "other")
        # Map old folder IDs to categories
        if folder in ["animals", "armor", "clothing", "light", "melee", "missile", "other"]:
            category = folder
        else:
            category = "other"
        
        # Remove folder field (not needed with separate packs)
        if "folder" in item:
            del item["folder"]
        
        categories[category].append(item)
    
    # Determine output directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, "..", "packs", "CoreKnave2e")
    
    # Create directory if needed
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Write separate JSON files for each category
    total_items = 0
    for category, items in categories.items():
        if items:  # Only create file if there are items
            output_path = os.path.join(output_dir, "items-{}.json".format(category))
            with open(output_path, 'w') as f:
                json.dump(items, f, indent=2)
            print("Created {} with {} items".format(output_path, len(items)))
            total_items += len(items)
    
    print("\nTotal items: {}".format(total_items))
    print("\nTo build .db packs, run: npm run stage")

if __name__ == "__main__":
    main()

