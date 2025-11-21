# Compendium Pack Development

This system uses a source-to-build pipeline for compendium packs to maintain readable, version-controlled content.

## Structure

```
packs/                         # Source files (version controlled)
├── CoreKnave2e/
│   ├── bestiary.json         # Array of all monsters
│   └── [other-packs].json
└── ...

build/elderknave2e/packs/     # Built files (generated, gitignored)  
├── CoreKnave2e/
│   └── bestiary.db
└── ...
```

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
    "_id": "coreknave2e-new-monster",
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
echo '[]' > packs/CoreKnave2e/items.json
# Add entries to the array
# Update system.json to register the new pack:
{
  "name": "coreknave2e-items",
  "label": "Items",
  "path": "packs/CoreKnave2e/items.db",
  "type": "Item",
  ...
}
```

## Commands

- `npm run stage` - **Main workflow**: Build CSS, packs, and stage entire system
- Source files use readable JSON formatting with proper indentation
- Built `.db` files contain one JSON object per line (Foundry format)

## Benefits

- ✅ **Version Control**: Source files are readable and diffable
- ✅ **Programmatic**: Easy to generate large arrays of content with scripts
- ✅ **Maintainable**: All pack content in one place, easy to edit
- ✅ **Automated**: Build process handles Foundry format conversion and metadata
- ✅ **Safe**: Built files are gitignored, preventing conflicts

## Notes

- The build script automatically adds `_stats` metadata required by Foundry v12
- Pack names should match the JSON filename (e.g., `bestiary.json` → `bestiary.db`)
- Actor references use `pack:name` format for compendium actors (e.g., `elderknave2e.coreknave2e-bestiary:Orc`)
- Embedded items in actors also receive proper `_stats` metadata automatically