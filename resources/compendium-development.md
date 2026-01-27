# Compendium Pack Development

This system uses a source-to-build pipeline for compendium packs to maintain readable, version-controlled content.

- **Version Control**: Source files are readable and diffable
- **Programmatic**: Easy to generate large arrays of content with scripts
- **Maintainable**: All pack content in one place, easy to edit
- **Automated**: Build process handles Foundry format conversion and metadata

## Structure

```
packs/                      # Source files (version controlled)
├── CoreKnave2e/
│   ├── bestiary.json       # 34 monsters with embedded attacks
│   ├── items-melee.json    # ~11 melee weapons
│   ├── items-missile.json  # ~4 missile weapons
│   ├── items-armor.json    # 7 armor pieces
│   ├── items-clothing.json # 7 clothing sets
│   ├── items-animals.json  # 6 animals
│   └── items-other.json    # ~200 equipment items
└── (future pack groups)

build/elderknave2e/packs/   # Built files (generated, gitignored)  
├── CoreKnave2e/
│   ├── bestiary.db
│   ├── items-melee.db
│   └── ...
└── ...
```

The build script reads all `.json` files from `packs/**/` recursively.

## File Format

Each pack is a **single JSON file** containing an array of entries:

```json
[
  {
    "_id": "unique-id-1",
    "name": "Monster Name",
    "type": "monster",
    "system": { ... },
    "items": [ ... ]
  },
  {
    "_id": "unique-id-2",
    "name": "Another Monster",
    ...
  }
]
```

This format makes it easy to generate content programmatically - just build an array and save it as JSON.

## ID Conventions

Use deterministic, human-readable IDs:
- **Core Knave 2e Items**: `ck2e-items-{name}` (e.g., `ck2e-items-short-sword`)
- **Core Knave 2e Bestiary**: `ck2e-bestiary-{name}` (e.g., `ck2e-bestiary-goblin`)
- **Elder Knave Items**: `ek-items-{name}` (e.g., `ek-items-mystic-robe`)

Generate from name: lowercase, replace spaces with hyphens, remove special characters.

## Workflow

1. **Edit source files** in `packs/CoreKnave2e/[pack-name].json`
2. **Stage system** with `npm run stage` (builds packs + stages entire system)
3. **Copy to Foundry** - copy `build/elderknave2e/` to your Foundry `systems/` folder
4. **Test in Foundry** - reload to see changes

The `npm run stage` command automatically builds compendium packs as part of the staging process.

## Adding New Content

### New Entry to Existing Pack
```json
// Edit packs/CoreKnave2e/bestiary.json
// Add new object to the array:
[
  { "_id": "existing-1", ... },
  { "_id": "existing-2", ... },
  {
    "_id": "ck2e-bestiary-new-monster",
    "name": "New Monster",
    "type": "monster",
    "system": {
      "level": 1,
      "armorClass": 11,
      ...
    }
  }
]
```

### New Pack
```bash
# Create new pack file
echo '[]' > packs/CoreKnave2e/spells.json
# Add entries to the array
# Update system.json to register the new pack:
{
  "name": "elderknave2e.coreknave2e-spells",
  "label": "Core Knave 2e - Spells",
  "path": "packs/CoreKnave2e/spells.db",
  "type": "Item",
  "system": "elderknave2e"
}
```

## Commands

- `npm run stage` - **Main workflow**: Build CSS, packs, and stage entire system
  - Source files use readable JSON formatting with proper indentation
  - Built `.db` files contain one JSON object per line (Foundry format)

## Notes

- The build script automatically adds `_stats` metadata required by Foundry v12
- Built `.db` files use simple newline-delimited JSON format (one object per line)
- **Do not use LevelDB compilation** - we tried it and it caused embedded item errors (doable but needs work)
- Pack names should match the JSON filename (e.g., `bestiary.json` → `bestiary.db`)
- Actor references use `pack:name` format (e.g., `elderknave2e.coreknave2e-bestiary.ck2e-bestiary-orc`)
- Embedded items in actors also receive proper `_stats` metadata automatically
- `scripts/generate-items.py` can regenerate all item packs from hardcoded data if needed