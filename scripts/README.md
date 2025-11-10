# Template Scripts

## validate-templates.py

Validates all templates against quality standards.

### Usage

```bash
python3 scripts/validate-templates.py
```

### What it checks

**Structure (ERRORS - Must Fix):**
- Exactly 2 spaces (GDD + Production)
- GDD space: `icon: "gdd"`, `defaultDeckType: "hero"`
- Production space: `icon: "tasks"`, `defaultDeckType: "task"`
- Every GDD hero deck: `deckType: "hero"`
- **GDD space must have exactly 1 doc deck with `deckType: "doc"`**
- Every Production deck: `deckType: "task"`
- No `#` markdown headings in card content
- No empty decks
- Minimum deck counts:
  - GDD space: At least 4 total decks (3+ hero decks + 1 doc deck)
  - Production space: At least 4 task decks
- Hero deck card counts: First deck needs 4+ cards, middle decks 3+, last deck 2+

**Content Quality (WARNINGS - Recommended):**
- GDD hero deck card count pattern: 4, 3, 3, 2 (first deck most, last deck least)
- At least X-1 cards per deck should have sub-cards (shows journey was triggered)
- No specific metrics in card content (no "Damage: 80", "Speed: 7.5 m/s")
- Doc deck should have 2-3 example cards

### Exit codes

- 0: All templates valid (no ERROR messages)
- 1: One or more templates have errors

### Output Format

- ✅ = Template passed with no issues
- ⚠️ = Template passed but has warnings (quality improvements recommended)
- ❌ = Template failed with errors (must be fixed)

**IMPORTANT:** Every template change should be validated before committing.

## Running validation in CI

The validation script can be integrated into GitHub workflows:

```yaml
- name: Validate templates
  run: python3 scripts/validate-templates.py
```
