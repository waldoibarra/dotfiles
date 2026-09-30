# Sources and Policy

Read when checking provenance or updating this skill. Consult local references during ordinary
work; use these primary links when validating platform details or refreshing guidance.

## Adopted principles

The [Pure Web Manifesto](https://pureweb.dev/manifesto) supplies HTML/CSS first, progressive
enhancement before components, custom elements when justified, Light DOM preference, and deliberate
Shadow DOM use. Its [component topics](https://pureweb.dev/pure-components) identify application
concerns, not a required architecture. Reviewed September 30, 2026.

## Deliberate differences

This skill implements Waldo's stricter frameworkless policy. The site's
[data-binding page](https://pureweb.dev/pure-components/data-binding) also recommends Lit; that
recommendation and its UI-library catalog are not adopted. Testing, building, templating, and forms
pages were incomplete when reviewed; this skill does not represent its supplemental guidance as
quotations from Pure Web. SKILL.md adapts the five manifesto priorities; no site implementation is
vendored. The ultra-light design-system guidance applies those priorities to Waldo's requested scope.

Shadow DOM is encapsulation, not a security boundary. Navigation guidance uses the actual navigate
event and does not assume every target browser supports it. No claims of automatic accessibility,
security, or performance follow merely from choosing standards.

## Technical authorities

- [HTML standard](https://html.spec.whatwg.org/multipage/): semantics, forms, custom elements.
- [DOM standard](https://dom.spec.whatwg.org/): events and tree behavior.
- [MDN Shadow DOM][shadow]: encapsulation limits.
- [MDN custom elements][elements]: lifecycle.
- [MDN Navigation API][navigation]: navigation and interception.
- [MDN constraint validation][forms]: form behavior.

[shadow]: https://developer.mozilla.org/en-US/docs/Web/API/Web_components/Using_shadow_DOM
[elements]: https://developer.mozilla.org/en-US/docs/Web/API/Web_components/Using_custom_elements
[navigation]: https://developer.mozilla.org/en-US/docs/Web/API/Navigation_API
[forms]: https://developer.mozilla.org/en-US/docs/Web/HTML/Guides/Constraint_validation

Use current compatibility data for the project's target browsers rather than treating this review
date as a browser support guarantee.
