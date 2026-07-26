## 2026-07-26 - [Add accessible names to dynamic dialogs]
**Learning:** Dynamically generated `<dialog>` components via JS need to receive explicit accessible names and descriptions via ARIA attributes that correspond to their generated internal content identifiers (e.g. `aria-labelledby` linking to a heading `id`).
**Action:** When inspecting JS files generating raw HTML string UI structures, explicitly look for lacking `id` tags in meaningful headers or descriptive elements that a parent `aria-*` element should point to, especially in modals and dialogs.
