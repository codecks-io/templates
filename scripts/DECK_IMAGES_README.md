# Creating Custom Deck Images

This guide explains how to generate custom deck images from the icon set.

## Prerequisites

You need Python 3 with Pillow installed:

```bash
pip install Pillow
```

## Quick Start

Run the image generation script:

```bash
python3 scripts/create_deck_images.py
```

This will:
1. ✅ Find appropriate icons for each deck type
2. ✅ Resize them to 147x104px
3. ✅ Add a purple gradient background
4. ✅ Add glow effects for visual appeal
5. ✅ Center the icons perfectly
6. ✅ Generate an ATTRIBUTIONS.txt file with proper credits

## Output

All generated images will be in: `generated_deck_images/`

### What Gets Created:

**Hero/GDD Deck Images:**
- `weapons.png` - Sword icon
- `enemies.png` - Skull icon
- `maps.png` - Dungeon gate icon
- `items.png` - Treasure chest icon
- `characters.png` - Character icon
- `levels.png` - Castle icon
- `power-ups.png` - Star icon
- `quests.png` - Scroll icon
- `creatures.png` - Dragon icon
- `puzzle-mechanics.png` - Puzzle icon
- `resources.png` - Wood pile icon
- `crafting-recipes.png` - Anvil icon
- `units.png` - Swords emblem
- `buildings.png` - Castle icon
- `technologies.png` - Enlightenment icon
- And more...

**Doc Deck Image:**
- `design-notes.png` - Notepad icon

## Customization

### Change the Purple Gradient

Edit the `create_gradient_background()` function in `create_deck_images.py`:

```python
# Current purple gradient
top_color = (75, 0, 130)      # Indigo
bottom_color = (147, 51, 234)  # Purple

# Try different colors:
# Blue: top_color = (0, 0, 139), bottom_color = (65, 105, 225)
# Green: top_color = (0, 100, 0), bottom_color = (50, 205, 50)
# Red: top_color = (139, 0, 0), bottom_color = (220, 20, 60)
```

### Adjust Glow Effect

Change the `add_glow_effect()` parameters:

```python
# Current: glow_radius=4
# More glow: glow_radius=6
# Less glow: glow_radius=2
# No glow: Skip the add_glow_effect() call
```

### Change Icon Size

Modify icon scaling in `create_deck_image()`:

```python
# Current: icon uses 60% of image height
icon_height = int(target_size[1] * 0.6)

# Larger icons: 0.7 or 0.8
# Smaller icons: 0.4 or 0.5
```

## Icon Mapping

The script uses the following icon mappings (from Game-Icons.net):

| Deck Type | Icon File | Author |
|-----------|-----------|---------|
| Weapons | ancient-sword.png | delapouite |
| Enemies | skull-sabertooth.png | darkzaitzev |
| Maps | dungeon-gate.png | delapouite |
| Items | chest.png | delapouite |
| Characters | character.png | delapouite |
| Quests | scroll-unfurled.png | delapouite |
| Power-ups | star-shuriken.png | delapouite |
| Resources | wood-pile.png | delapouite |
| And more... | | |

## Attribution

All icons are from **Game-Icons.net** (https://game-icons.net)

Licensed under **Creative Commons 3.0 BY** or **CC0** (see icons/license.txt)

When using these deck images, please include:
> "Icons made by {author name} from Game-Icons.net"

The script automatically generates a complete `ATTRIBUTIONS.txt` file in the output directory.

## Troubleshooting

### "No module named 'PIL'"

Install Pillow:
```bash
pip install Pillow
```

### "FileNotFoundError: icons/..."

Make sure you're running the script from the project root:
```bash
cd /mnt/c/projects/codecks-templates
python3 scripts/create_deck_images.py
```

### Icons look too small/large

Adjust the scaling factor in the script (see Customization section above).

### Want different icons?

Edit the `ICON_MAPPINGS` dictionary in `create_deck_images.py` to point to different icon files from the icons/ folder.

## Next Steps

After generating images:

1. ✅ Review images in `generated_deck_images/`
2. ✅ Check `ATTRIBUTIONS.txt` for proper credits
3. Upload images to your CDN/storage (e.g., S3)
4. Update templates to use new image URLs
5. Run validation: `python3 scripts/validate-templates.py`

## Example: Uploading to S3

```bash
# Upload all generated images
aws s3 cp generated_deck_images/ s3://your-bucket/deck-images/ --recursive

# Get public URLs
# https://your-bucket.s3.region.amazonaws.com/deck-images/weapons.png
# https://your-bucket.s3.region.amazonaws.com/deck-images/maps.png
# etc.
```

Then update templates with the new URLs!
