# Codecks Template Creation Guide

This guide teaches Claude (and humans) how to create high-quality Codecks game project templates.

## Template Philosophy

Codecks templates should provide **immediate value** to game developers by:

1. Establishing a clear separation between **design/planning** (GDD space) and **production/execution** (Work/Production space)
2. Pre-defining asset pipelines using **Journeys** that automatically create production tasks
3. Including realistic example content that demonstrates best practices
4. Demonstrating hero cards with sub-cards to show asset-task relationships
5. Providing visual appeal through deck images that represent each deck's purpose
6. Reducing initial project setup friction while remaining flexible for customization

## Template Structure Overview

Every high-quality template MUST have:

### 1. Two Spaces (Required)

**Space 1: Game Design Documents (GDD)**

- `icon: "gdd"` - Use the GDD icon
- `defaultDeckType: "hero"` - This is crucial!
- Contains 3-5 hero decks representing major asset types or design systems
- **REQUIRED:** Contains exactly 1 doc deck for design documentation
- Each hero deck must have an `id` field for journey targeting
- Each hero deck should have a journey that creates production tasks
- Hero decks contain cards (assets) with example sub-cards demonstrating the journey output
- Doc deck contains design meeting notes and playtesting findings

**Space 2: Production/Work**

- `icon: "tasks"` - Use the tasks icon
- `defaultDeckType: "task"`
- Contains 4-7 task decks representing work departments
- Common departments: Coding, Art, Audio, Game Design, Writing, QA, UI/UX
- Each deck must have an `id` field (used as targetDeck in journeys)
- Each deck should have `preferredOrder: { "prop": "priority" }`
- These decks receive tasks from GDD journeys

**Standard Codecks Deck Images:**

Use these default images provided by Codecks for common deck types:

**Production/Work Decks:**

- **Coding:** `https://perma-assets-codecks.s3.eu-central-1.amazonaws.com/covers/ruth-2019/CD_Code.jpeg`
- **Art:** `https://perma-assets-codecks.s3.eu-central-1.amazonaws.com/covers/ruth-2019/CD_Art.jpeg`
- **Audio:** `https://perma-assets-codecks.s3.eu-central-1.amazonaws.com/covers/ruth-2019/CD_Audio.jpeg`
- **Game Design/LD:** `https://perma-assets-codecks.s3.eu-central-1.amazonaws.com/covers/ruth-2019/CD_LD.jpeg`
- **QA/Bugs:** `https://perma-assets-codecks.s3.eu-central-1.amazonaws.com/covers/ruth-2019/CD_QA.jpeg`
- **UI/UX:** `https://perma-assets-codecks.s3.eu-central-1.amazonaws.com/covers/ruth-2019/CD_UI.jpeg`
- **Writing/Docs:** `https://perma-assets-codecks.s3.eu-central-1.amazonaws.com/covers/ruth-2019/CD_Docs.jpeg`
- **Marketing:** `https://perma-assets-codecks.s3.eu-central-1.amazonaws.com/covers/ruth-2019/CD_Marketing.jpeg`
- **BizDev:** `https://perma-assets-codecks.s3.eu-central-1.amazonaws.com/covers/ruth-2019/CD_Bizdev.jpeg`
- **Production/Scheduling:** `https://perma-assets-codecks.s3.eu-central-1.amazonaws.com/covers/ruth-2019/CD_Production.jpeg`
- **Ideas/Brainstorming:** `https://perma-assets-codecks.s3.eu-central-1.amazonaws.com/covers/ruth-2019/CD_Ideas.jpeg`

**For Hero Decks (GDD):**
Choose images that visually represent the asset type:

- Weapons deck → image of iconic weapon
- Characters deck → character portrait
- Levels deck → environment/map view
- Items deck → iconic item or treasure chest

**For Doc Decks:**
Use a document/note-taking themed image to represent design documentation.

**Best Practices:**

- Images should be visually distinct and easily recognizable
- Use thematic images that match the template's game genre
- Maintain consistent visual style across all decks in a template
- Images should work at small sizes (147x104 recommended)

### 3. Tags (Required)

Tags serve multiple purposes:

- Categorizing assets by tier/rarity/type
- Visual organization using colors and emojis
- Filtering and searching

**Tag Format:**

```json
{
  "tag": "tag-name",
  "description": "Clear explanation of what this represents",
  "color": "#HEX" // OR
  "emoji": "🎯"
}
```

Common patterns:

- Tier tags: `tier-1`, `tier-2`, `tier-3` with emojis 1️⃣, 2️⃣, 3️⃣
- Rarity: `common`, `rare`, `epic`, `legendary` with colors
- Quest types: `main-quest`, `side-quest`, `daily-quest`
- Asset categories: specific to genre (e.g., `projectile`, `hitscan` for shooters)

### 3. Complete Example Cards

Every deck needs 2-4 example cards demonstrating:

**For Hero Decks (GDD Space):**

- Mix of complexity levels (at least one simple, one complex)
- Content starts with the title as plain text (NOT `# Title` markdown heading)
- Can include additional markdown content below the title
- Appropriate tags applied
- At least 1-2 hero cards MUST have sub-cards already created (using `subCards` array)
- Priority levels (a, b, or c)
- Cards referenced in `subCards` must have `id` fields

**For Task Decks (Production Space):**

- Typically populated by journeys, not manually (can be empty)
- Include descriptions explaining the department's role

**For Doc/Mechanic Cards:**

- Title as plain text, then markdown content
- Use `isDoc: true` for reference materials
- Include specifications, formulas, design rationale

## Journey Design

Journeys are the **killer feature** of Codecks templates. They codify production pipelines.

### Journey Best Practices

1. **Order matters**: List steps in chronological production order
2. **Appropriate effort estimates**: Use Fibonacci (1, 2, 3, 5, 8, 13, 21)
3. **Department mapping**: Each step's `targetDeck` can reference either:
   - The deck's `id` field (if specified), OR
   - The deck's `name` field (common practice)
4. **Priority inheritance**: High-priority assets → high-priority tasks (usually "a")
5. **Clear content**: Title as plain text, action verbs ("Create", "Implement", "Design"), optional details below
6. **Zone labels**: Optional `zoneLabel` field to group related steps

### Journey Step Anatomy

```json
{
  "content": "Action-oriented task name\n\nOptional details or sub-tasks",
  "targetDeck": "Deck Name", // Must match a deck's name or id field!
  "priority": "a", // or "b" or "c" (nullable)
  "effort": 5, // Fibonacci number (nullable)
  "tags": ["optional", "tags"], // Optional
  "zoneLabel": "Optional Zone" // Optional grouping label
}
```

**CRITICAL**:

- `targetDeck` can reference either the deck's `id` OR `name` field
- `content` should start with plain text title, NOT markdown heading `# Title`
- Best practice: Use deck names like "Coding", "Art", "Audio" for clarity

### Common Journey Patterns by Genre

**Action/FPS - Weapon Journey:**

```json
[
  {
    "content": "Create Weapon 3D Model & Textures",
    "targetDeck": "Art",
    "priority": "a",
    "effort": 8
  },
  {
    "content": "Create Weapon Animations\n\n- Fire\n- Reload\n- Inspect",
    "targetDeck": "Art",
    "priority": "a",
    "effort": 5
  },
  {"content": "Design Weapon SFX", "targetDeck": "Audio", "priority": "a", "effort": 3},
  {"content": "Implement Weapon Logic", "targetDeck": "Coding", "priority": "a", "effort": 5},
  {
    "content": "Balance & Tune Weapon Stats",
    "targetDeck": "Game Design",
    "priority": "b",
    "effort": 3
  }
]
```

**RPG - Quest Journey:**

```json
[
  {
    "content": "Write Quest Dialogue & Journal Text",
    "targetDeck": "Writing",
    "priority": "a",
    "effort": 5
  },
  {
    "content": "Script Quest Logic (Triggers, Objectives, Flags)",
    "targetDeck": "Coding",
    "priority": "a",
    "effort": 8
  },
  {
    "content": "Design & Populate Quest Location",
    "targetDeck": "Game Design",
    "priority": "a",
    "effort": 8
  },
  {"content": "Implement Quest Rewards", "targetDeck": "Game Design", "priority": "a", "effort": 2},
  {"content": "Test Quest (Start to Finish)", "targetDeck": "QA", "priority": "b", "effort": 3}
]
```

**Simulation - Building Journey:**

```json
[
  {"content": "Create Concept Art", "targetDeck": "Art", "priority": "a", "effort": 3},
  {"content": "Create 3D Model & Textures", "targetDeck": "Art", "priority": "a", "effort": 5},
  {
    "content": "Implement Logic (Cost, Function)",
    "targetDeck": "Coding",
    "priority": "a",
    "effort": 5
  },
  {
    "content": "Design SFX\n\n- Placement\n- Active Loop",
    "targetDeck": "Audio",
    "priority": "b",
    "effort": 2
  },
  {
    "content": "Balance Building Cost & Output",
    "targetDeck": "Game Design",
    "priority": "b",
    "effort": 2
  }
]
```

## Content Writing Guidelines

### Deck Descriptions

Every deck needs a clear, concise description explaining:

- What belongs in this deck
- When to create cards here
- (For hero decks) How the journey works

**Examples:**

- "The central quest log. Add a new quest as a card, then start its journey to create all production tasks."
- "Programming tasks, engine work, and technical feature implementation."
- "Database for all items: weapons, armor, potions, and quest objects. Add an item, then start its journey."

### Card Content

Card content format:

```
Title

Optional markdown content below the title describing what to consider:

**Consider:**
- What properties does this need?
- How does it behave?
- What are the key decisions to make?

## Related Systems
- Links to other cards
- Dependencies
```

**CRITICAL - NO SPECIFIC METRICS:**

- ❌ DON'T include specific numbers like "Damage: 80" or "Speed: 7.5 m/s"
- ❌ DON'T include exact stats, costs, or measurements
- ✅ DO describe what needs to be decided ("Define the damage value", "Determine movement speed")
- ✅ DO provide context and questions ("Should it be slow and powerful or fast and weak?")
- ✅ DO reference what the card represents in general terms

Include:

- **Clear title**: Start with plain text title (not markdown heading)
- **Guiding questions**: What needs to be decided/designed
- **Behavior descriptions**: How it works conceptually
- **Design considerations**: Tradeoffs and choices to make
- **References**: Links to other systems/cards

### Tone and Style

- **Practical**: Focus on implementable specifications
- **Specific**: Concrete numbers, not vague descriptions
- **Genre-appropriate**: Match the game type's conventions
- **Example-driven**: Show, don't just tell

## Template-Specific Patterns

### Action/Shooter Games

- Hero decks: Weapons, Enemies, Maps, Game Mechanics
- Focus on feel/juice specifications (recoil, fire rate, damage)
- Include movement specs in Core Mechanics
- Map decks should have layout/flow descriptions

### RPG Games

- Hero decks: Quests, Items, Creatures, Core Mechanics
- Rich narrative content in quest cards
- Item stats with tier/rarity tags
- Creature behavior and loot tables

### Strategy Games

- Hero decks: Units, Buildings, Technologies, Maps
- Cost/benefit balance specifications
- Tech trees and dependencies
- Resource economy details

### Simulation Games

- Hero decks: Buildings, Craftable Items, Events, Core Systems
- Detailed economy specifications
- Need/satisfaction systems
- Time/calendar mechanics

### Platformer Games

- Hero decks: Levels, Enemies, Power-ups, Core Mechanics
- Movement specifications (jump height, speed, etc.)
- Level flow and gating
- Collectible types

### Puzzle Games

- Hero decks: Mechanics, Levels, Puzzle Elements
- Rule interactions
- Difficulty curve planning
- Tutorial progression

### Survival Games

- Hero decks: Resources, Crafting Recipes, Threats, World Systems
- Gathering and crafting chains
- Threat escalation
- Player progression systems

### Horror Games

- Hero decks: Scares/Events, Environments, Enemies, Core Mechanics
- Tension and pacing specifications
- Resource scarcity design
- Audio design emphasis

## Validation Checklist

Before finalizing a template, verify:

**Structure:**

- [ ] Has 2 spaces (GDD + Production)
- [ ] GDD space has `icon: "gdd"` and `defaultDeckType: "hero"`
- [ ] Production space has `icon: "tasks"` and `defaultDeckType: "task"`
- [ ] **CRITICAL:** Every GDD hero deck MUST have `deckType: "hero"` explicitly set
- [ ] **CRITICAL:** GDD space MUST have exactly 1 doc deck with `deckType: "doc"`
- [ ] **CRITICAL:** Every Production deck MUST have `deckType: "task"` explicitly set
- [ ] 3-5 hero decks in GDD space (plus 1 doc deck = 4-6 total)
- [ ] 4-7 task decks in Production space
- [ ] Production decks have `id` fields (optional but recommended)
- [ ] Every hero deck has a journey with 4-6 steps (unless explicitly one-off assets)
- [ ] All journey `targetDeck` values reference existing Production deck names or IDs
- [ ] All tags used in cards are defined in the `tags` array

**Content Quality:**

- [ ] Every deck has a clear description
- [ ] Every deck has at least 1 example card (no empty decks!)
- [ ] **GDD deck card counts follow pattern:** First deck ~4 cards, middle decks ~3 cards, last deck ~2 cards
- [ ] **At least X-1 cards per GDD deck have sub-cards** (if deck has 3 cards, at least 2 should have sub-cards)
- [ ] Cards referenced in `subCards` have `id` fields
- [ ] Example cards have instructional, template-appropriate content (not overly specific)
- [ ] **NO specific metrics** in card content (no exact numbers for damage, speed, HP, etc.)
- [ ] Priority levels are set appropriately (mostly "a" and "b")
- [ ] Effort estimates use Fibonacci numbers

**Educational Elements (introduce once or twice across cards):**

- [ ] At least one card explains tags (e.g., "This card has the #tier-1 tag...")
- [ ] At least one card explains priority (e.g., in a blockquote: "> **Priority:** This is marked as 'a' priority...")
- [ ] At least one card explains effort (e.g., "> **Effort:** Estimated at 5 points...")
- [ ] At least one card demonstrates card linking (e.g., "**Unlocks:** [Card Name]")
- [ ] At least one card shows sub-cards concept (e.g., "See the sub-cards below for implementation tasks")
- [ ] Cards use conversational, instructional tone for newcomers

**Technical Validation:**

- [ ] All required fields are present
- [ ] No extra/invalid properties
- [ ] `content` field starts with plain text title (not markdown heading)
- [ ] Title and description are clear and genre-specific

## Common Mistakes to Avoid

1. **Empty decks**: Every deck must have at least 1 example card
2. **Missing deckType**: EVERY deck needs explicit `deckType: "hero"`, `deckType: "task"`, or `deckType: "doc"`
3. **Missing doc deck**: GDD space MUST have exactly 1 doc deck
4. **Specific metrics in cards**: NO exact numbers (no "Damage: 80", "Speed: 7.5 m/s")
5. **Markdown headings in content**: Use plain text titles, NOT `# Title`
6. **Missing journeys**: Hero decks without journeys lose their power (unless one-off)
7. **Broken targetDeck references**: All must point to existing Production deck names
8. **Undefined tags**: All tags in cards must be in the tags array
9. **Missing space icons**: GDD needs `icon: "gdd"`, Production needs `icon: "tasks"`
10. **No example sub-cards**: At least 1-2 hero cards should demonstrate journey output
11. **Missing descriptions**: Every deck needs its purpose explained

## Tips for Quality

1. **Research the genre**: Understand common asset types and pipelines
2. **Think in pipelines**: Every asset type needs a production pipeline
3. **Show, don't tell**: Example cards demonstrate patterns
4. **Be opinionated**: Show best practices, not just empty structures
5. **Consider team composition**: Map to real game dev roles
6. **Include complexity**: Mix simple and complex examples
7. **Use real game design**: Actual stats, meaningful descriptions
8. **Test the flow**: Mentally walk through creating an asset
9. **Balance breadth and depth**: Cover major systems without overwhelming
10. **Remember the user**: Templates should save time and teach patterns

## Example: Creating a New Template

Let's create a "Tower Defense" template step by step:

### 1. Identify Core Asset Types (GDD Hero Decks)

- Towers (defensive units)
- Enemies (waves/units)
- Maps/Levels
- Core Mechanics (rules/systems)

### 2. Identify Production Departments (Task Decks)

- Coding
- Art
- Game Design
- Audio
- VFX
- UI/UX

### 3. Define Tags

```json
[
  {"tag": "tier-1", "emoji": "1️⃣"},
  {"tag": "tier-2", "emoji": "2️⃣"},
  {"tag": "tier-3", "emoji": "3️⃣"},
  {"tag": "ground", "color": "#8B4513", "description": "Ground-based unit"},
  {"tag": "air", "color": "#87CEEB", "description": "Flying unit"},
  {"tag": "splash", "color": "#FF6347", "description": "Area-of-effect damage"}
]
```

### 4. Create Tower Journey

```json
{
  "steps": [
    {"content": "Create Tower Concept Art", "targetDeck": "Art", "priority": "a", "effort": 2},
    {
      "content": "Create Tower 3D Model & Textures",
      "targetDeck": "Art",
      "priority": "a",
      "effort": 5
    },
    {"content": "Animate Tower (Idle, Attack)", "targetDeck": "Art", "priority": "a", "effort": 3},
    {"content": "Implement Tower Logic", "targetDeck": "Coding", "priority": "a", "effort": 5},
    {"content": "Create Tower VFX", "targetDeck": "VFX", "priority": "b", "effort": 3},
    {"content": "Design Tower SFX", "targetDeck": "Audio", "priority": "b", "effort": 2},
    {"content": "Balance Tower Stats", "targetDeck": "Game Design", "priority": "b", "effort": 2}
  ]
}
```

### 5. Write Example Tower Card

```json
{
  "content": "Arrow Tower\n\n**Role:** Basic single-target anti-ground tower.\n\n**Stats:**\n- Damage: 20\n- Range: 5 tiles\n- Fire Rate: 1 attack/sec\n\n**Cost:** 100 Gold\n**Upgrades:** Yes (3 tiers)",
  "priority": "a",
  "tags": ["tier-1", "ground"]
}
```

## Maintenance and Updates

When updating templates:

1. Check that journeys still map to current Production decks
2. Update example content to reflect best practices
3. Add new asset types as genre conventions evolve
4. Keep descriptions current
5. Validate after every change

---

## Quick Reference: Required Fields

**Template Level:**

- `title` (string, required)
- `description` (string, required)
- `tags` (array, optional but strongly recommended)
- `spaces` (array, required - exactly 2)

**Space Level:**

- `name` (string, nullable)
- `icon` (enum, optional: "default", "journey", "robot", "gdd", "tasks", "knowledge", "qa")
- `decks` (array, required)
- `defaultDeckType` (enum, optional: "task", "hero", "doc", "mixed")

**Deck Level:**

- `id` (string, optional but strongly recommended for production decks)
- `name` (string, required)
- `description` (string, optional but strongly recommended)
- `image` (string, **REQUIRED** - URL or path to deck visual)
- `cards` (array, optional but should have 2-4 examples for hero decks)
- `journey` (object, optional - required for hero decks)
- `preferredOrder` (object, optional - recommended for task decks)
- `deckType` (enum, required: "hero", "task", or "doc")

**Card Level:**

- `id` (string, optional - required if referenced in subCards)
- `content` (string, required - starts with title as plain text)
- `priority` (enum, optional nullable: "a", "b", "c")
- `effort` (number, optional nullable)
- `tags` (array, optional)
- `subCards` (array, optional - array of card IDs)
- `isDoc` (boolean, optional nullable)

**Journey Step Level:**

- `content` (string, required - starts with title as plain text)
- `targetDeck` (string, nullable - must match deck id)
- `priority` (enum, optional nullable: "a", "b", "c")
- `effort` (number, optional nullable)
- `tags` (array, optional)
- `zoneLabel` (string, optional nullable)

---

Remember: A great template is both **a starting point** and **a teaching tool**. It should demonstrate patterns while remaining practical for real game development.
