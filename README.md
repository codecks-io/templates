# Codecks Template Library

The `/templates` directory contains json-formatted starter kits for new Codecks projects.

## Template Structure

A Codecks template is a JSON object with the following structure:

```
Template
├── title (required)
├── description (required)
├── tags (optional)
└── spaces (required, array)
    └── Space
        ├── name (required)
        ├── defaultDeckType (optional)
        └── decks (required, array)
            └── Deck
                ├── name (required)
                ├── description (optional)
                ├── coverFileUrl (optional)
                ├── deckType (optional)
                ├── preferredOrder (optional)
                ├── cards (optional, array)
                │   └── Card
                │       ├── title (required)
                │       ├── content (optional)
                │       ├── priority (optional)
                │       ├── effort (optional)
                │       ├── tags (optional)
                │       └── isDoc (optional)
                └── journey (optional)
                    └── steps (array)
                        └── JourneyStep
                            ├── title (required)
                            ├── targetDeck (required)
                            ├── content (optional)
                            ├── priority (optional)
                            ├── effort (optional)
                            └── tags (optional)
```

## Field Definitions

### Template Level

- **title** (string, required): The name of your template
- **description** (string, required): A brief description of what this template is for
- **tags** (string array, optional): Global tags that can be referenced by cards and journey steps
- **spaces** (array, required): One or more spaces containing decks

### Space

- **name** (string, required): The name of the space
- **decks** (array, required): One or more decks in this space
- **defaultDeckType** (enum, optional): Default type for decks in this space
  - Valid values: `"task"`, `"hero"`, `"doc"`, `"mixed"`

### Deck

- **name** (string, required): The name of the deck
- **description** (string, optional): Description of the deck's purpose
- **coverFileUrl** (string, optional): URL to a cover image
- **deckType** (enum, optional): Type of deck
  - Valid values: `"task"`, `"hero"`, `"doc"`, `"mixed"`
- **cards** (array, optional): Pre-populated cards in this deck
- **journey** (object, optional): A journey with steps that create cards in other decks
- **preferredOrder** (object, optional): Default sorting configuration for this deck

### Card

- **title** (string, required): The card title
- **content** (string, optional): Markdown content for the card
- **priority** (enum, optional): Priority level
  - Valid values: `"a"`, `"b"`, `"c"`
- **effort** (number, optional): Effort estimate
- **tags** (string array, optional): Tags assigned to this card (must be defined in template tags)
- **isDoc** (boolean, optional): Whether this card is a document

### Journey Step

Journey steps create cards in target decks when the journey is activated.

- **title** (string, required): The title for the card to be created
- **targetDeck** (string, required): The name of the deck where the card will be created (must exist in template)
- **content** (string, optional): Markdown content for the card
- **priority** (enum, optional): Priority level (`"a"`, `"b"`, `"c"`)
- **effort** (number, optional): Effort estimate
- **tags** (string array, optional): Tags for the card (must be defined in template tags)

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
2. **Deck References**: All `targetDeck` values in journey steps must reference existing deck names within the template
3. **Required Fields**: All required fields must be present
4. **No Extra Properties**: Templates cannot include properties not defined in the schema

## Simple Template Example

```json
{
  "title": "Basic Game Project",
  "description": "A simple template for small game projects",
  "tags": ["art", "code", "design"],
  "spaces": [
    {
      "name": "Development",
      "decks": [
        {
          "name": "To Do",
          "deckType": "task",
          "cards": [
            {
              "title": "Set up project structure",
              "priority": "a",
              "effort": 2,
              "tags": ["code"]
            },
            {
              "title": "Create initial art assets",
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
  "title": "Complete Game Development Pipeline",
  "description": "A comprehensive template for professional game development teams with multiple disciplines",
  "tags": ["programming", "art", "audio", "design", "qa", "marketing", "urgent", "blocked"],
  "spaces": [
    {
      "name": "Production",
      "defaultDeckType": "task",
      "decks": [
        {
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
              "title": "Implement player movement",
              "content": "Create basic WASD movement with collision detection",
              "priority": "a",
              "effort": 5,
              "tags": ["programming"]
            },
            {
              "title": "Design main character",
              "content": "Concept art and 3D model for protagonist",
              "priority": "a",
              "effort": 8,
              "tags": ["art", "design"]
            },
            {
              "title": "Compose main theme",
              "priority": "b",
              "effort": 13,
              "tags": ["audio"]
            }
          ]
        },
        {
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
      "decks": [
        {
          "name": "Game Design Docs",
          "deckType": "doc",
          "cards": [
            {
              "title": "Core Gameplay Loop",
              "content": "# Core Gameplay Loop\n\nDescribe the main gameplay mechanics here...",
              "isDoc": true,
              "tags": ["design"]
            },
            {
              "title": "Technical Architecture",
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
              "title": "Visual Style Guide",
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
      "decks": [
        {
          "name": "Getting Started",
          "description": "Journey to set up a new team member",
          "deckType": "hero",
          "journey": {
            "steps": [
              {
                "title": "Complete development environment setup",
                "targetDeck": "Sprint",
                "content": "Install Unity, Git, and required SDKs. See Technical Architecture doc for versions.",
                "priority": "a",
                "effort": 3,
                "tags": ["programming"]
              },
              {
                "title": "Read all design documentation",
                "targetDeck": "Sprint",
                "content": "Review Core Gameplay Loop and Visual Style Guide",
                "priority": "a",
                "effort": 2,
                "tags": ["design"]
              },
              {
                "title": "Set up art pipeline",
                "targetDeck": "Sprint",
                "content": "Configure Blender, Substance Painter, and export settings",
                "priority": "a",
                "effort": 3,
                "tags": ["art"]
              },
              {
                "title": "First task: Create test level",
                "targetDeck": "Backlog",
                "content": "Build a simple test level to familiarize yourself with the tools",
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

- Using tags in cards/steps that aren't defined in the template `tags` array
- Referencing non-existent deck names in journey `targetDeck` fields
- Missing required fields like `title`, `description`, `name`
- Using invalid enum values for `priority`, `deckType`, etc.
- Adding custom properties not defined in the schema

## Adding Templates

- Create a pull request adding your files to `templates/[YOUR-HANDLE]/*.json`
- This repository has built-in validation checks
