# Codecks Template Library

The `/templates` directory contains json-formatted starter kits for new Codecks projects.

## Template Structure

A Codecks template is a JSON object with the following structure:

```
Template
├── meta (required, object)
│   ├── id (required)
│   ├── title (required)
│   ├── description (required)
│   ├── tags (required, array)
│   └── imageUrl (optional, nullable)
├── tags (optional, array)
└── spaces (required, array)
    └── Space
        ├── name (nullable)
        ├── icon (optional)
        ├── defaultDeckType (optional)
        └── decks (required, array)
            └── Deck
                ├── id (optional)
                ├── name (required)
                ├── description (optional)
                ├── coverFileUrl (optional)
                ├── deckType (optional)
                ├── preferredOrder (optional)
                ├── cards (optional, array)
                │   └── Card
                │       ├── id (optional)
                │       ├── content (required)
                │       ├── priority (optional)
                │       ├── effort (optional)
                │       ├── tags (optional)
                │       ├── subCards (optional)
                │       └── isDoc (optional)
                └── journey (optional)
                    └── steps (array)
                        └── JourneyStep
                            ├── content (required)
                            ├── targetDeck (nullable)
                            ├── priority (optional)
                            ├── effort (optional)
                            ├── tags (optional)
                            └── zoneLabel (optional)
```

## Field Definitions

### Template Level

- **meta** (object, required): Metadata about the template
  - **id** (string, required): Unique identifier for the template (e.g., "cdx/action", "myname/mytemplate")
  - **title** (string, required): The name of your template
  - **description** (string, required): A brief description of what this template is for
  - **tags** (string array, required): Categories for the template (e.g., ["gamedev"], ["marketing"])
  - **imageUrl** (string, optional, nullable): URL to a preview image for the template
- **tags** (string array, optional): Global tags that can be referenced by cards and journey steps
- **spaces** (array, required): One or more spaces containing decks

### Space

- **name** (string, nullable): The name of the space
- **icon** (enum, optional, nullable): Icon for the space
  - Valid values: `"default"`, `"journey"`, `"robot"`, `"gdd"`, `"tasks"`, `"knowledge"`, `"qa"`
- **decks** (array, required): One or more decks in this space
- **defaultDeckType** (enum, optional): Default type for decks in this space
  - Valid values: `"task"`, `"hero"`, `"doc"`, `"mixed"`

### Deck

- **id** (string, optional): Unique identifier for the deck such that you can reference it as targetDeck in journey steps
- **name** (string, required): The name of the deck
- **description** (string, optional): Description of the deck's purpose
- **coverFileUrl** (string, optional): URL to a cover image
- **deckType** (enum, optional): Type of deck
  - Valid values: `"task"`, `"hero"`, `"doc"`, `"mixed"`
- **cards** (array, optional): Pre-populated cards in this deck
- **journey** (object, optional): A journey with steps that create cards in other decks
- **preferredOrder** (object, optional): Default sorting configuration for this deck

### Card

- **id** (string, optional): Unique identifier for the card such that you can reference it within the subCards array
- **content** (string, required): Markdown content for the card
- **priority** (enum, optional, nullable): Priority level
  - Valid values: `"a"`, `"b"`, `"c"`
- **effort** (number, optional, nullable): Effort estimate
- **tags** (string array, optional): Tags assigned to this card (must be defined in template tags)
- **subCards** (string array, optional): Array of sub-card ids
- **isDoc** (boolean, optional, nullable): Whether this card is a document

### Journey Step

Journey steps create cards in target decks when the journey is activated.

- **content** (string, required): Markdown content for the card to be created
- **targetDeck** (string, nullable): The id of the deck where the card will be created (must exist in template)
- **priority** (enum, optional, nullable): Priority level (`"a"`, `"b"`, `"c"`)
- **effort** (number, optional, nullable): Effort estimate
- **tags** (string array, optional): Tags for the card (must be defined in template tags)
- **zoneLabel** (string, optional, nullable): Label for the zone grouping

### Preferred Order

- **prop** (enum, required): The property to sort by
  - Valid values: `"priority"`, `"effort"`, `"assignee"`, `"status"`, `"lastEdit"`, `"creationDate"`, `"tags"`, `"tagsPersonal"`, `"tagsProject"`, `"deck"`, `"milestone"`, `"sprint"`, `"project"`, `"changes"`, `"upvotes"`, `"title"`, `"accountSeq"`, `"timeTracked"`, `"dueDate"`, `"heroCard"`, `"beastLevel"`
- **isReversed** (boolean, optional): Whether to reverse the sort order
- **secondary** (array, optional): Additional sort properties
- **mode** (enum, optional): Display mode (`"tableView"` or `"miniCard"`)
- **isCompact** (boolean, optional): Whether to only have a single swimlane
- **hideEmpty** (boolean, optional): Whether to hide empty swim lanes

## Validation Rules

1. **Tag References**: All tags used in cards or journey steps must be defined in the template's `tags` array
2. **Deck References**: Non-null `targetDeck` values in journey steps must reference existing deck names within the template
3. **Required Fields**: All required fields must be present
4. **No Extra Properties**: Templates cannot include properties not defined in the schema
5. **SubCard References**: All `subCards` identifiers must reference existing card `id` values within the same deck

## Simple Template Example

```json
{
  "meta": {
    "id": "example/basic-game",
    "title": "Basic Game Project",
    "description": "A simple template for small game projects",
    "tags": ["gamedev"],
    "imageUrl": null
  },
  "tags": ["art", "code", "design"],
  "spaces": [
    {
      "name": "Development",
      "icon": "tasks",
      "decks": [
        {
          "name": "To Do",
          "deckType": "task",
          "cards": [
            {
              "content": "Set up project structure",
              "priority": "a",
              "effort": 2,
              "tags": ["code"]
            },
            {
              "content": "Create initial art assets",
              "priority": "b",
              "effort": 5,
              "tags": ["art"]
            }
          ]
        },
        {
          "name": "In Progress",
          "deckType": "task"
        },
        {
          "name": "Done",
          "deckType": "task"
        }
      ]
    }
  ]
}
```

## Extensive Template Example

```json
{
  "meta": {
    "id": "example/game-dev-pipeline",
    "title": "Complete Game Development Pipeline",
    "description": "A comprehensive template for professional game development teams with multiple disciplines",
    "tags": ["gamedev"],
    "imageUrl": null
  },
  "tags": ["programming", "art", "audio", "design", "qa", "marketing", "urgent", "blocked"],
  "spaces": [
    {
      "name": "Production",
      "icon": "tasks",
      "defaultDeckType": "task",
      "decks": [
        {
          "id": "1-backlog",
          "name": "Backlog",
          "description": "All upcoming tasks and features",
          "deckType": "task",
          "preferredOrder": {
            "prop": "priority",
            "isReversed": false,
            "secondary": [
              {
                "prop": "effort",
                "isReversed": false
              }
            ]
          },
          "cards": [
            {
              "content": "# Implement player movement\n\nCreate basic WASD movement with collision detection",
              "priority": "a",
              "effort": 5,
              "tags": ["programming"]
            },
            {
              "content": "# Design main character\n\nConcept art and 3D model for protagonist",
              "priority": "a",
              "effort": 8,
              "tags": ["art", "design"]
            },
            {
              "content": "Compose main theme",
              "priority": "b",
              "effort": 13,
              "tags": ["audio"]
            }
          ]
        },
        {
          "id": "2-sprint",
          "name": "Sprint",
          "description": "Current sprint tasks",
          "deckType": "task",
          "preferredOrder": {
            "prop": "assignee"
          }
        },
        {
          "name": "Review",
          "description": "Tasks awaiting review or testing",
          "deckType": "task"
        },
        {
          "name": "Done",
          "deckType": "task",
          "preferredOrder": {
            "prop": "lastEdit",
            "isReversed": true
          }
        }
      ]
    },
    {
      "name": "Documentation",
      "icon": "knowledge",
      "decks": [
        {
          "name": "Game Design Docs",
          "deckType": "doc",
          "cards": [
            {
              "content": "# Core Gameplay Loop\n\nDescribe the main gameplay mechanics here...",
              "isDoc": true,
              "tags": ["design"]
            },
            {
              "content": "# Technical Architecture\n\n## Engine\n- Unity 2023.1\n\n## Patterns\n- ECS for gameplay\n- MVC for UI",
              "isDoc": true,
              "tags": ["programming"]
            }
          ]
        },
        {
          "name": "Art Bible",
          "deckType": "doc",
          "cards": [
            {
              "content": "# Visual Style\n\n## Color Palette\n- Primary: #FF6B35\n- Secondary: #004E89\n\n## Art Direction\nLow-poly with hand-painted textures",
              "isDoc": true,
              "tags": ["art", "design"]
            }
          ]
        }
      ]
    },
    {
      "name": "Onboarding",
      "icon": "journey",
      "decks": [
        {
          "name": "Getting Started",
          "description": "Journey to set up a new team member",
          "deckType": "hero",
          "journey": {
            "steps": [
              {
                "content": "# Complete development environment setup\n\nInstall Unity, Git, and required SDKs. See Technical Architecture doc for versions.",
                "targetDeck": "2-sprint",
                "priority": "a",
                "effort": 3,
                "tags": ["programming"]
              },
              {
                "content": "# Read all design documentation\n\nReview Core Gameplay Loop and Visual Style Guide",
                "targetDeck": "2-sprint",
                "priority": "a",
                "effort": 2,
                "tags": ["design"]
              },
              {
                "content": "# Set up art pipeline\n\nConfigure Blender, Substance Painter, and export settings",
                "targetDeck": "2-sprint",
                "priority": "a",
                "effort": 3,
                "tags": ["art"]
              },
              {
                "content": "# First task: Create test level\n\nBuild a simple test level to familiarize yourself with the tools",
                "targetDeck": "1-backlog",
                "priority": "b",
                "effort": 5,
                "tags": ["design", "programming"]
              }
            ]
          }
        }
      ]
    }
  ]
}
```

## Common Mistakes to Avoid

- Missing the `meta` object or any of its required fields (`id`, `title`, `description`, `tags`)
- Using tags in cards/steps that aren't defined in the template `tags` array
- Referencing non-existent deck names in journey `targetDeck` fields
- Missing required fields like `content` (for cards and journey steps), `name` (for decks)
- Using invalid enum values for `priority`, `deckType`, `icon`, etc.
- Adding custom properties not defined in the schema
- Using `title` field on cards (use `content` instead)
- Referencing invalid card IDs in `subCards` arrays

## Adding Templates

- Create a pull request adding your files to `templates/[YOUR-HANDLE]/*.json`
- This repository has built-in validation checks
