#!/usr/bin/env python3
"""
Create custom deck images from icon set.
Requirements: pip install Pillow

This script:
1. Finds appropriate icons for each deck type
2. Resizes to 147x104 with centered icons
3. Adds purple gradient background
4. Adds glow effect for visual appeal
"""
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
from pathlib import Path
import json

# Icon mapping for each deck type
ICON_MAPPINGS = {
    # Action/FPS template
    'Weapons': 'icons/ffffff/transparent/1x1/delapouite/ancient-sword.png',
    'Enemies': 'icons/ffffff/transparent/1x1/delapouite/skull-sabertooth.png',
    'Maps': 'icons/ffffff/transparent/1x1/delapouite/dungeon-gate.png',
    'Game Mechanics': 'icons/ffffff/transparent/1x1/delapouite/gears.png',

    # RPG template
    'Quests': 'icons/ffffff/transparent/1x1/delapouite/scroll-unfurled.png',
    'Items': 'icons/ffffff/transparent/1x1/delapouite/chest.png',
    'Creatures': 'icons/ffffff/transparent/1x1/delapouite/dragon-orb.png',
    'Core Mechanics': 'icons/ffffff/transparent/1x1/delapouite/gears.png',

    # Platformer template
    'Movement Abilities': 'icons/ffffff/transparent/1x1/delapouite/jump-across.png',
    'Levels': 'icons/ffffff/transparent/1x1/delapouite/castle.png',
    'Power-ups': 'icons/ffffff/transparent/1x1/delapouite/star-shuriken.png',

    # Puzzle template
    'Puzzle Mechanics': 'icons/ffffff/transparent/1x1/delapouite/puzzle.png',
    'Puzzle Elements': 'icons/ffffff/transparent/1x1/delapouite/key.png',
    'Puzzle Levels': 'icons/ffffff/transparent/1x1/delapouite/maze.png',
    'Tutorial System': 'icons/ffffff/transparent/1x1/delapouite/book-cover.png',

    # Roguelike template
    'Items & Power-ups': 'icons/ffffff/transparent/1x1/delapouite/round-potion.png',
    'Room Types': 'icons/ffffff/transparent/1x1/delapouite/dungeon-gate.png',
    'Meta-Progression': 'icons/ffffff/transparent/1x1/delapouite/level-four-advanced.png',

    # Sports template
    'Game Rules & Mechanics': 'icons/ffffff/transparent/1x1/delapouite/whistle.png',
    'Teams': 'icons/ffffff/transparent/1x1/delapouite/team-idea.png',
    'Players': 'icons/ffffff/transparent/1x1/delapouite/american-football-player.png',
    'Stadiums & Venues': 'icons/ffffff/transparent/1x1/sbed/arena.png',

    # Strategy template
    'Units': 'icons/ffffff/transparent/1x1/delapouite/swords-emblem.png',
    'Buildings': 'icons/ffffff/transparent/1x1/delapouite/castle.png',
    'Technologies': 'icons/ffffff/transparent/1x1/delapouite/enlightenment.png',

    # Simulation template
    'Core Systems': 'icons/ffffff/transparent/1x1/delapouite/gears.png',
    'Craftable Items': 'icons/ffffff/transparent/1x1/delapouite/anvil.png',
    'Events': 'icons/ffffff/transparent/1x1/delapouite/time-bomb.png',

    # Survival template
    'Resources': 'icons/ffffff/transparent/1x1/delapouite/wood-pile.png',
    'Crafting Recipes': 'icons/ffffff/transparent/1x1/delapouite/anvil.png',
    'Threats': 'icons/ffffff/transparent/1x1/delapouite/wolf-howl.png',
    'World Systems': 'icons/ffffff/transparent/1x1/delapouite/world.png',

    # Adventure template
    'Locations': 'icons/ffffff/transparent/1x1/delapouite/treasure-map.png',
    'Characters': 'icons/ffffff/transparent/1x1/delapouite/character.png',
    'Puzzles': 'icons/ffffff/transparent/1x1/delapouite/key.png',
    'Story Beats': 'icons/ffffff/transparent/1x1/delapouite/book.png',

    # Design Notes (all templates)
    'Design Notes': 'icons/ffffff/transparent/1x1/delapouite/notebook.png',
}

def create_gradient_background(width, height):
    """Create a deep purple gradient background with more range."""
    img = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(img)

    # Deeper, richer purple gradient with more range
    top_color = (30, 10, 60)       # Deep dark purple/navy
    bottom_color = (90, 40, 140)   # Rich medium purple

    for y in range(height):
        # Interpolate between top and bottom colors
        ratio = y / height
        r = int(top_color[0] + (bottom_color[0] - top_color[0]) * ratio)
        g = int(top_color[1] + (bottom_color[1] - top_color[1]) * ratio)
        b = int(top_color[2] + (bottom_color[2] - top_color[2]) * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    return img

def add_glow_effect(icon, glow_radius=3, glow_color=(255, 255, 255)):
    """Add a glow effect around the icon."""
    # Create a larger canvas for the glow
    glow_size = (icon.width + glow_radius * 4, icon.height + glow_radius * 4)
    glow_layer = Image.new('RGBA', glow_size, (0, 0, 0, 0))

    # Paste icon in center
    offset = (glow_radius * 2, glow_radius * 2)
    glow_layer.paste(icon, offset, icon if icon.mode == 'RGBA' else None)

    # Create glow by blurring
    glow = glow_layer.copy()
    glow = glow.filter(ImageFilter.GaussianBlur(radius=glow_radius))

    # Enhance the glow
    enhancer = ImageEnhance.Brightness(glow)
    glow = enhancer.enhance(1.5)

    # Composite glow with original icon
    result = Image.alpha_composite(glow, glow_layer)

    return result

def get_icon_author(icon_path):
    """Extract the author name from the icon path."""
    path_parts = Path(icon_path).parts
    # Path format: icons/ffffff/transparent/1x1/{author}/{icon-name}.png
    if len(path_parts) >= 6:
        return path_parts[4]
    return "Unknown"

def create_deck_image(icon_path, output_path, target_size=(147, 104)):
    """
    Create a deck image from an icon.

    Args:
        icon_path: Path to source icon (PNG)
        output_path: Where to save the result
        target_size: Final image size (width, height)

    Returns:
        Author name for attribution
    """
    # Load icon
    icon = Image.open(icon_path).convert('RGBA')

    # Scale icon to fit nicely (about 60% of target height)
    icon_height = int(target_size[1] * 0.6)
    aspect_ratio = icon.width / icon.height
    icon_width = int(icon_height * aspect_ratio)
    icon = icon.resize((icon_width, icon_height), Image.Resampling.LANCZOS)

    # Add glow effect
    icon_with_glow = add_glow_effect(icon, glow_radius=4)

    # Create gradient background
    background = create_gradient_background(target_size[0], target_size[1])
    background = background.convert('RGBA')

    # Center the icon
    x = (target_size[0] - icon_with_glow.width) // 2
    y = (target_size[1] - icon_with_glow.height) // 2

    # Composite icon onto background
    background.paste(icon_with_glow, (x, y), icon_with_glow)

    # Save as PNG
    background.save(output_path, 'PNG')
    print(f"✓ Created {output_path}")

    return get_icon_author(icon_path)

def find_icon(pattern):
    """Find an icon file matching the pattern."""
    base_path = Path('icons/ffffff/transparent/1x1')

    # Try exact match first
    for icon_file in base_path.rglob('*.png'):
        if pattern in str(icon_file):
            return str(icon_file)

    # Try partial match
    pattern_lower = pattern.lower()
    for icon_file in base_path.rglob('*.png'):
        if pattern_lower in icon_file.stem.lower():
            return str(icon_file)

    return None

def main():
    """Generate all deck images."""
    output_dir = Path('generated_deck_images')
    output_dir.mkdir(exist_ok=True)

    print("🎨 Creating custom deck images with purple gradient and glow effects...\n")

    created = 0
    missing = []
    attributions = {}  # Track which authors contributed which icons

    for deck_name, icon_path in ICON_MAPPINGS.items():
        # Check if icon exists
        if not Path(icon_path).exists():
            # Try to find it
            icon_name = Path(icon_path).stem
            found_icon = find_icon(icon_name)
            if found_icon:
                icon_path = found_icon
            else:
                missing.append((deck_name, icon_path))
                continue

        # Create output filename
        safe_name = deck_name.lower().replace(' ', '-').replace('/', '-')
        output_path = output_dir / f"{safe_name}.png"

        try:
            author = create_deck_image(icon_path, output_path)
            created += 1

            # Track attribution
            icon_name = Path(icon_path).stem
            if author not in attributions:
                attributions[author] = []
            attributions[author].append(f"{deck_name} ({icon_name})")

        except Exception as e:
            print(f"✗ Error creating {deck_name}: {e}")
            missing.append((deck_name, icon_path))

    # Create attribution file
    with open(output_dir / 'ATTRIBUTIONS.txt', 'w') as f:
        f.write("Deck Image Attributions\n")
        f.write("=" * 50 + "\n\n")
        f.write("All icons are from Game-Icons.net (https://game-icons.net)\n")
        f.write("Licensed under Creative Commons 3.0 BY or CC0\n\n")
        f.write("Icon authors:\n\n")

        for author in sorted(attributions.keys()):
            f.write(f"Icons by {author}:\n")
            for deck_info in sorted(attributions[author]):
                f.write(f"  - {deck_info}\n")
            f.write("\n")

        f.write("\nOriginal license file: icons/license.txt\n")
        f.write("\nPlease include: 'Icons made by {author}' in derivative works.\n")
        f.write("More info at https://game-icons.net\n")

    print(f"\n✅ Successfully created {created} deck images in '{output_dir}/'")
    print(f"✅ Created attribution file: {output_dir}/ATTRIBUTIONS.txt")

    if missing:
        print(f"\n⚠️  Could not find icons for:")
        for deck_name, icon_path in missing:
            print(f"   - {deck_name}: {icon_path}")

    print("\n💡 Next steps:")
    print("   1. Review images in 'generated_deck_images/' folder")
    print("   2. Check ATTRIBUTIONS.txt for proper credits")
    print("   3. Upload images to your CDN/storage")
    print("   4. Update templates with new image URLs")

    return 0 if not missing else 1

if __name__ == '__main__':
    exit(main())
