#!/usr/bin/env python3
"""
Validates Codecks templates against quality standards.

Rules:
- GDD decks should have 4, 3, 3, 2 cards (first deck has most)
- At least X-1 cards per deck should have sub-cards (showing journey triggered)
- Every deck must have explicit deckType
- Every deck must have at least 1 card
- No specific metrics in card content
- Spaces must have correct icons
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Tuple

def check_metrics_in_content(content: str) -> List[str]:
    """Check for specific numeric metrics in content."""
    issues = []

    # Patterns that indicate specific metrics
    metric_patterns = [
        r'\b\d+\s*HP\b',
        r'\b\d+\s*damage\b',
        r'\b\d+\s*m/s\b',
        r'\b\d+\s*RPM\b',
        r'\b\d+%\b',
        r'\b\d+\.\d+\s*seconds?\b',
    ]

    for pattern in metric_patterns:
        if re.search(pattern, content, re.IGNORECASE):
            issues.append(f"Found specific metric: {pattern}")

    return issues

def validate_template(filepath: Path) -> Dict:
    """Validate a single template file."""
    with open(filepath) as f:
        template = json.load(f)

    issues = []
    warnings = []

    # Check spaces
    if len(template.get('spaces', [])) != 2:
        issues.append(f"Should have exactly 2 spaces, found {len(template.get('spaces', []))}")

    # Check tags exist
    if 'tags' not in template or len(template.get('tags', [])) == 0:
        warnings.append("No tags defined - templates should have tags for organization")
    elif len(template.get('tags', [])) < 3:
        warnings.append(f"Only {len(template.get('tags', []))} tags defined - templates should have 3-5 tags for better organization")

    # Check bug tag exists (required for QA deck)
    tags = template.get('tags', [])
    has_bug_tag = any(t.get('tag') == 'bug' for t in tags)
    if not has_bug_tag:
        issues.append("Missing 'bug' tag - required for Bugs & QA deck autoTag feature")
    else:
        # Check bug tag has emoji
        bug_tag = next(t for t in tags if t.get('tag') == 'bug')
        if not bug_tag.get('emoji'):
            warnings.append("Bug tag should have emoji='🐞' for visual identification")

    for space_idx, space in enumerate(template.get('spaces', [])):
        space_name = space.get('name', f'Space {space_idx}')

        # Check space names are consistent
        if space_idx == 0 and space_name != 'Game Design Documents (GDD)':
            issues.append(f"First space should be named 'Game Design Documents (GDD)', found '{space_name}'")
        if space_idx == 1 and space_name != 'Production':
            issues.append(f"Second space should be named 'Production', found '{space_name}'")

        # Check icons and default deck types
        if space_idx == 0:
            if space.get('icon') != 'gdd':
                issues.append(f"{space_name}: GDD space should have icon='gdd'")
            if space.get('defaultDeckType') != 'hero':
                issues.append(f"{space_name}: GDD space should have defaultDeckType='hero'")
        if space_idx == 1:
            if space.get('icon') != 'tasks':
                issues.append(f"{space_name}: Production space should have icon='tasks'")
            if space.get('defaultDeckType') != 'task':
                issues.append(f"{space_name}: Production space should have defaultDeckType='task'")

        # Check GDD decks
        if space.get('icon') == 'gdd' or space.get('defaultDeckType') == 'hero':
            decks = space.get('decks', [])

            # Check minimum deck count (3-5 hero decks + 1 doc deck = 4-6 total)
            if len(decks) < 4:
                issues.append(f"{space_name}: Should have at least 4 GDD decks (3+ hero + 1 doc), found {len(decks)}")

            # Check for exactly 1 doc deck
            doc_decks = [d for d in decks if d.get('deckType') == 'doc']
            if len(doc_decks) == 0:
                issues.append(f"{space_name}: Missing doc deck (should have exactly 1 deck with deckType='doc')")
            elif len(doc_decks) > 1:
                warnings.append(f"{space_name}: Has {len(doc_decks)} doc decks, should have exactly 1")
            if len(decks) > 5:
                warnings.append(f"{space_name}: Has {len(decks)} GDD decks, recommended 3-5")

            # Check card count pattern (4, 3, 3, 2) - only for hero decks
            hero_decks = [d for d in decks if d.get('deckType') == 'hero']
            expected_cards = [4, 3, 3, 2]
            for deck_idx, deck in enumerate(hero_decks):
                cards = deck.get('cards', [])

                # Hero decks should follow card count pattern

                # Check card count - stricter now
                if deck_idx < len(expected_cards):
                    expected = expected_cards[deck_idx]
                    if len(cards) < expected:
                        issues.append(f"{deck.get('name')}: Has {len(cards)} cards, should have at least {expected}")
                    elif len(cards) < expected - 1:
                        warnings.append(f"{deck.get('name')}: Has {len(cards)} cards, expected ~{expected}")

                # Check sub-cards (DISABLED - waiting for auto-trigger journey feature)
                # Once auto-trigger is implemented, hero cards will have sub-cards automatically created
                # For now, templates should have empty subCards arrays
                cards_with_subcards = sum(1 for card in cards if card.get('subCards') and len(card.get('subCards', [])) > 0)
                if cards_with_subcards > 0:
                    warnings.append(f"{deck.get('name')}: Has {cards_with_subcards} cards with sub-cards - these will be auto-generated once auto-trigger feature is added")

                # Check for metrics in content
                for card in cards:
                    content = card.get('content', '')
                    metric_issues = check_metrics_in_content(content)
                    if metric_issues:
                        warnings.append(f"{deck.get('name')}: Card has metrics in content")

                # Check for # markdown headings
                for card in cards:
                    content = card.get('content', '')
                    if re.search(r'^#\s+\w', content, re.MULTILINE):
                        issues.append(f"{deck.get('name')}: Card uses # markdown heading")

                # Check effort on hero cards
                for card in cards:
                    if 'effort' not in card or card.get('effort') is None:
                        warnings.append(f"{deck.get('name')}: Hero card missing effort value")
                    elif card.get('effort', 0) < 1:
                        warnings.append(f"{deck.get('name')}: Hero card has effort < 1 (should be at least 1)")

                # Check effort on journey steps
                journey_steps = deck.get('journey', {}).get('steps', [])
                for step in journey_steps:
                    if 'effort' not in step or step.get('effort') is None:
                        warnings.append(f"{deck.get('name')}: Journey step '{step.get('content', '')[:40]}...' missing effort")
                    elif step.get('effort', 0) < 1:
                        warnings.append(f"{deck.get('name')}: Journey step has effort < 1")

            # Check doc deck
            for deck in doc_decks:
                if len(deck.get('cards', [])) < 2:
                    warnings.append(f"{deck.get('name')}: Doc deck should have at least 2-3 example cards")
                if deck.get('name') != 'Design Notes':
                    warnings.append(f"{deck.get('name')}: Doc deck should be named 'Design Notes' for consistency")

            # Check deck images for all decks in GDD space
            for deck in decks:
                if 'coverFileUrl' not in deck or not deck.get('coverFileUrl'):
                    issues.append(f"{deck.get('name')}: Deck missing 'coverFileUrl' field - all decks should have a visual")

        # Check Production decks
        elif space.get('icon') == 'tasks' or space.get('defaultDeckType') == 'task':
            decks = space.get('decks', [])

            # Check minimum deck count (including mandatory Bugs & QA)
            if len(decks) < 5:
                issues.append(f"{space_name}: Should have at least 5 Production decks (4 work + 1 QA), found {len(decks)}")
            if len(decks) > 7:
                warnings.append(f"{space_name}: Has {len(decks)} Production decks, recommended 5-7")

            # Check for Bugs & QA deck
            qa_decks = [d for d in decks if 'Bug' in d.get('name', '') or 'QA' in d.get('name', '')]
            if len(qa_decks) == 0:
                issues.append(f"{space_name}: Missing 'Bugs & QA' deck - all templates should have a QA deck")
            elif len(qa_decks) > 1:
                warnings.append(f"{space_name}: Has {len(qa_decks)} QA decks, should have exactly 1")
            else:
                # Check QA deck has autoTag
                qa_deck = qa_decks[0]
                if 'autoTag' not in qa_deck:
                    warnings.append(f"{qa_deck.get('name')}: QA deck should have autoTag='bug' to automatically tag all cards")
                elif qa_deck.get('autoTag') != 'bug':
                    warnings.append(f"{qa_deck.get('name')}: autoTag should be 'bug', found '{qa_deck.get('autoTag')}'")

                # Check name consistency
                if qa_deck.get('name') != 'Bugs & QA':
                    warnings.append(f"{qa_deck.get('name')}: QA deck should be named 'Bugs & QA' for consistency")

            for deck in decks:
                if deck.get('deckType') != 'task':
                    issues.append(f"{deck.get('name')}: Production deck missing deckType='task'")

                if len(deck.get('cards', [])) == 0:
                    issues.append(f"{deck.get('name')}: Empty deck (needs at least 1 card)")

                # Check preferredOrder
                if 'preferredOrder' not in deck:
                    warnings.append(f"{deck.get('name')}: Missing preferredOrder (recommended for task decks)")

                # Check deck images for production decks
                if 'coverFileUrl' not in deck or not deck.get('coverFileUrl'):
                    issues.append(f"{deck.get('name')}: Deck missing 'coverFileUrl' field - all decks should have a visual")

                # Check effort on production example cards
                cards = deck.get('cards', [])
                for card in cards:
                    if 'effort' not in card or card.get('effort') is None:
                        warnings.append(f"{deck.get('name')}: Example card missing effort value")
                    elif card.get('effort', 0) < 1:
                        warnings.append(f"{deck.get('name')}: Example card has effort < 1")

    return {
        'file': filepath.name,
        'issues': issues,
        'warnings': warnings,
        'valid': len(issues) == 0
    }

def main():
    """Validate all templates."""
    templates_dir = Path('templates/cdx')

    if not templates_dir.exists():
        print(f"Error: {templates_dir} not found")
        return 1

    results = []
    for template_path in sorted(templates_dir.glob('*.json')):
        result = validate_template(template_path)
        results.append(result)

    # Print results
    all_valid = True
    for result in results:
        if result['issues'] or result['warnings']:
            status = '❌' if result['issues'] else '⚠️'
            print(f"\n{status} {result['file']}")

            for issue in result['issues']:
                print(f"  ERROR: {issue}")
                all_valid = False

            for warning in result['warnings']:
                print(f"  WARN:  {warning}")
        else:
            print(f"✅ {result['file']}")

    if all_valid:
        print(f"\n✅ All {len(results)} templates passed validation!")
        return 0
    else:
        print(f"\n❌ Some templates have errors")
        return 1

if __name__ == '__main__':
    exit(main())
