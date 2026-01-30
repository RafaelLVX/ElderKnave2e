---
applyTo: "**"
---
# Basic project information

- This project is named Elder Knave 2e, a system for Foundry VTT.
- It is a fork of Knave Second Edition for FoundryVTT by Lee Talman (version 0.5.4 originally).
- The system is based on Knave 2nd Edition by Ben Milton and Questing Beast, LLC.
- The system is built with Node.js and uses Gulp/SCSS for CSS compilation.
- Build system: `npm run stage` compiles SCSS (`scss/` → `css/knave2e.css`) and creates .db pack files in `build/elderknave2e/`.
- Foundry VTT version: v12 (minimum v10, verified/maximum v12).
- Testing: Copy `build/elderknave2e/` to Foundry's `Data/systems/elderknave2e/` directory.
- Refer to `README.md` for an overview of the project, its purpose and technologies used.

# Compendium Pack System

## Pack Architecture
- We use **simple .db format** (newline-delimited JSON), NOT LevelDB binary format.
- Each .db file is a text file with one JSON object per line.
- Build script (`scripts/system-package.mjs`) reads JSON arrays from `packs/**`, adds `_stats` metadata, and writes as .db files.
- No `_key` fields needed, no temp directories, no binary compilation.
- This approach is simpler and more maintainable than LevelDB.
- **Important**: We tried LevelDB with @foundryvtt/foundryvtt-cli but it caused "The   does not exist" errors with embedded items. Don't go back to LevelDB for now.

## Pack Structure
We have two main pack folders organized in `system.json`:
- **CoreKnave2e/** - Core Knave 2nd Edition content (items, bestiary, transport)
- **ElderKnave/** - Elder Knave custom content (spellbooks, future additions)

Packs are organized using `packFolders` in system.json for clear UI separation in Foundry.

Examples:
- **bestiary.db** - monsters with embedded monster attacks
- **items-melee.db** - Melee weapons
- **items-missile.db** - Missile weapons
- **items-armor.db** - Armor pieces
- **items-clothing.db** - Clothing sets
- **items-animals.db** - Animals
- **items-other.db** - Other items
- **spellbooks.db** - Elder Magic spellbooks

## Source Files
- Any and all JSON source files in folder `packs/**` are used to build compendium packs.
- Each source file is a **JSON array** of documents (no folders, no special structure).
- Separate packs provide natural categorization, as dbs, while simple, do not support folders.

## Document ID Conventions
- **Core Knave 2nd Ed Items**: `ck2e-items-{name}` (e.g., `ck2e-items-short-sword`)
- **Core Knave 2nd Ed Bestiary**: `ck2e-bestiary-{name}` (e.g., `ck2e-bestiary-goblin`)
- **Core Knave 2nd Ed Transport**: `ck2e-transport-{name}` (e.g., `ck2e-transport-mule`)
- **Elder Knave Spellbooks**: `ek-spellbooks-{name}` (e.g., `ek-spellbooks-fireball`)
- **Elder Knave Items** (future): `ek-items-{name}` (e.g., `ek-items-mystic-robe`)
- **Elder Knave Bestiary** (future): `ek-bestiary-{name}` (e.g., `ek-bestiary-shadow-beast`)
- IDs are deterministic, human-readable, and derived from document names.
- Convert name to lowercase, replace spaces with hyphens, remove special chars.

## Embedded Items (Monster Attacks)
- Monsters have `items: []` array with attack objects nested directly.
- Build script automatically adds `_stats` to embedded items.
- No special handling needed - they just work as nested JSON.

## Build Workflow
1. Edit source JSON files in `packs/**`.
2. Run `npm run stage` to build .db packs.
3. Output: `build/elderknave2e/packs/**/*.db`.
4. Copy `build/elderknave2e/` to Foundry Data directory for testing.

## Item Generation Script
- `scripts/generate-items.py` - Python script with all 200+ items hardcoded.
- Generates separate category JSON files directly (no intermediate files).
- Only run when adding/modifying items or regenerating from scratch.
- Current JSON files are already populated and maintained.

# Elder Magic System

- Spellbook items use type `spellbook` with data model `Knave2eSpellbook`.
- **Tiers**: Use string IDs ("novice", "apprentice", "adept", "master"), not numbers.
- **Categories**: Use string IDs ("alteration", "conjuration", "destruction", "illusion", "restoration").
- Spellbook configuration: `module/config/spellbook.mjs` defines CATEGORIES and TIERS.
- Each spell has: tier, category, slots (1), cost (100/500/2000/5000 by tier), description.
- Refer to `resources/elder-magic.md` for complete spell mechanics and design philosophy.

# Project general coding standards

- Prefer Javascript over Python when writing new util scripts for the project. You CAN use Python for one-off scripts or if that is the only option available, but try to keep project utilities in Javascript for consistency.
- The build system (`scripts/system-package.mjs`) is in Node.js/JavaScript.
- Python 2 compatibility is maintained for generator scripts (if needed).
- Please be concise and clear in code comments and documentation. Do not embellish unnecessarily in documentation or oversell.
- Do not make stuff up. If unsure about rules or mechanics, ask.
- Do not make stuff up about Foundry's "known bugs", limitations or features. If you can't back up a claim, don't make it.

# Module Structure

- `module/data/` - Data models (character.mjs, weapon.mjs, armor.mjs, etc.)
- `module/sheets/` - Actor/Item sheets (actor-sheet.mjs, item-sheet.mjs)
- `module/documents/` - Document classes extending Foundry base (actor.mjs, item.mjs)
- `templates/` - Handlebars templates for sheets
- `scss/` - Styles source (compiles to `css/knave2e.css`)