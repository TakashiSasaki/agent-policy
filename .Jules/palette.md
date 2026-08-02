## 2024-10-26 - Accessible Dialog Creation
**Learning:** Dynamically injected `<dialog>` elements require an explicit `aria-labelledby` attribute linked to their title element ID for screen readers to properly announce their context upon opening.
**Action:** Always link dialog headings with their container using `aria-labelledby` when generating modal components in JavaScript.
