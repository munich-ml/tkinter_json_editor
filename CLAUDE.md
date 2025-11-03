# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Architecture Philosophy

TreeEditFrame is a **headless component** - it provides the tree editing UI but does NOT handle file I/O. Applications using it control data loading/saving. This separation allows the component to be used for any hierarchical data (JSON, YAML, XML, configs, etc.), not just JSON files.

## Code Architecture

### TreeEditFrame Component (tree_edit_frame.py)

**Module Structure**:
- Only `TreeEditFrame` is public (exported for external use)
- Internal classes prefixed with `_` (`_EntryPopup`, `_ComboPopup`, `_CheckPopup`) are implementation details

**Core Design Patterns**:

1. **Tag-based Type System**: The component uses Treeview tags to track data types ("int", "float", "bool", "str", "dict", "list", "NoneType"). Tags determine which popup editor to use and how to reconstruct Python objects.

2. **Popup Editor Pattern**: Editing happens via popup widgets that overlay tree cells. The popup is stored in `self.popup` and managed by:
   - `make_popup()` - Creates appropriate popup based on type/field
   - `close_cell_popup()` - Commits changes and destroys popup
   - Each popup class has an `update()` method that writes changes back to tree

3. **Bidirectional Conversion**:
   - `insert_tree_node()` - Recursively converts Python objects → Treeview structure
   - `extract_obj_from_tree()` - Recursively converts Treeview structure → Python objects
   - Type preservation happens through tags on tree nodes

4. **Event-Driven Editing**: Editing can be triggered by:
   - Double-click (`<Double-1>` event)
   - Return key (`<Return>` event)
   - Events are conditionally bound based on `editable` flag

5. **Combo Choices**: Field-specific dropdown options via `combo_choices` dict. When a field name matches a key in this dict, a `_ComboPopup` is used instead of `_EntryPopup`.

**Data Flow**:
```
set_data() → insert_tree_node() → Treeview with tags
User edits → make_popup() → _*Popup.update() → Treeview updated
get_data() → extract_obj_from_tree() → Python object
```

### Example Application (json_editor_example.py)

The example application shows how to wrap TreeEditFrame with application-specific functionality:
- Adds file I/O layer (JSON loading/saving) on top of headless component
- Demonstrates combo choices configuration (hardcoded for "pattern" field)
- Shows dynamic toggling of editable mode via checkbox

## Important Implementation Details

### Naming Conventions

- **Private classes**: Use leading underscore (`_EntryPopup`) for internal implementation details not meant for external use
- **Methods**: Use verb-based names (`set_data`, `get_data`, not `load_data`)

### Type Preservation

The component preserves Python types through the edit cycle:
- Integer fields validate and convert input to `int`
- Float fields validate and convert input to `float`
- Bool fields use checkboxes with "True"/"False" string representation in tree
- Validation failures keep original value unchanged

### Read-Only Mode

The `editable` flag controls editing behavior:
- When `False`: Event bindings are removed, `make_popup()` returns early
- Can be set via constructor parameter or `set_editable()` method
- Switching to read-only closes any open popup

### Backward Compatibility

All parameters default to maintain backward compatibility:
- `combo_choices=None` (defaults to empty dict)
- `editable=True` (defaults to editable mode)

## Git Commit Message Format

Follow this format for commits:
```
Brief summary of changes

- Detailed bullet points explaining changes
- Focus on "why" rather than "what"

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

## Testing

No formal test suite exists. Manual testing via `python json_editor_example.py`:
- Load `example.json` to test all data types (str, int, float, bool, list, dict, null)
- "pattern" field demonstrates combo dropdown functionality
- Toggle "Editable" checkbox to verify read-only mode works
- Save JSON to verify bidirectional conversion preserves types and structure

## Dependencies

Standard library only (tkinter, tkinter.ttk, json, os). No external dependencies.
