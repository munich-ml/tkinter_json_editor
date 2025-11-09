# Development TODO

## Testing & Quality
- [ ] Add formal test suite
  - Unit tests for TreeEditFrame methods
  - Tests for type conversion (int, float, bool preservation)
  - Tests for bidirectional conversion (Python ↔ Treeview)
  - Tests for editable mode toggling
- [ ] Standardize docstring format
  - Choose style (Google/NumPy/Sphinx)
  - Apply consistently across all methods
  - Document internal classes if needed

## Performance
- [ ] Generate large JSON test files for performance testing
  - 1000+ nodes
  - Deep nesting (10+ levels)
  - Mixed data types
- [ ] Test and improve responsiveness with large datasets
  - Profile `insert_tree_node()` performance
  - Profile `extract_obj_from_tree()` performance
  - Consider lazy loading for large trees
  - Consider virtual scrolling if needed


## Future Enhancements (Optional)
- [ ] Add/delete nodes functionality
- [ ] Undo/redo support
- [ ] Search/filter capability
- [ ] Context menu (right-click)
- [ ] Keyboard shortcuts (Ctrl+S, Ctrl+O, Ctrl+F)
- [ ] Horizontal scrollbar
- [ ] Column width resizing
