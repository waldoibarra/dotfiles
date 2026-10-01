# Sources and Policy

Read when checking provenance or updating this skill. Consult local references during ordinary
work; use these primary links when validating platform details or refreshing guidance.

## Adopted principles

Marc van Neerven's [original PURE Manifesto][original] (May 29, 2024) and its
[Pure Web summary](https://pureweb.dev/manifesto) supply HTML/CSS first, progressive enhancement
before components, custom elements when justified, Light DOM preference, and deliberate Shadow DOM.
The original uses Lit, including a Light DOM render-root override; it does not address TypeScript
or Vite. Do not attribute bans on those tools or all runtime libraries to the manifesto.
The site's [component topics](https://pureweb.dev/pure-components) identify application concerns,
not a required architecture. Reviewed September 30, 2026.

## Skill policy and source limits

SKILL.md adapts the five ordered priorities to standards-first apps and ultra-light design systems.
Native HTML/CSS, no runtime dependencies, and no build are starting defaults, not universal bans.
Lit may be a justified runtime library; TypeScript/Vite may be justified tooling. None are mandatory
or override the priorities or explicit user constraints. The source's router and app-shell examples
are not prescribed architecture, and this skill does not substitute an application framework.

Testing, building, templating, and forms pages were incomplete when reviewed; this skill does not
represent supplemental guidance as Pure Web quotations. No site implementation is vendored.
Articles motivate engineering choices; specifications define platform behavior, MDN documents APIs
and compatibility, and APG supplies interaction guidance. Prose review is not runtime verification,
and historical case-study measurements are not universal performance guarantees.

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
- [MDN FormData][form-data] and [getAll()][form-values]: preserve repeated names during serialization.
- [MDN attachShadow()][attach-shadow]: reattaching clears an existing matching declarative root.
- [MDN ElementInternals][internals]: author-overridable accessibility defaults.
- [APG tabs][tabs] and [switch][switch]: roles, state, relationships, and keyboard behavior.
- [MDN JavaScript modules][modules] and [SyntaxError][syntax]: delivered loading and parsing failures.
- [Lit render roots][lit-roots]: choose Light DOM deliberately rather than inheriting Shadow DOM.
- [web.dev performance measurement][measurement] and [budgets][budgets]: journey-based evidence
  and audience-derived limits, not automatic speed claims.
- [MDN related-app detection][related-apps] and [installation prompts][install-prompts]:
  detection limits and the non-standard prompt API.
- [MDN service-worker registration][workers] and [same-origin policy][origins]: control scope
  and origin boundaries, including storage.

[original]: https://medium.com/p/d46f400853eb

[shadow]: https://developer.mozilla.org/en-US/docs/Web/API/Web_components/Using_shadow_DOM
[elements]: https://developer.mozilla.org/en-US/docs/Web/API/Web_components/Using_custom_elements
[navigation]: https://developer.mozilla.org/en-US/docs/Web/API/Navigation_API
[forms]: https://developer.mozilla.org/en-US/docs/Web/HTML/Guides/Constraint_validation
[form-data]: https://developer.mozilla.org/en-US/docs/Web/API/FormData
[form-values]: https://developer.mozilla.org/en-US/docs/Web/API/FormData/getAll
[attach-shadow]: https://developer.mozilla.org/en-US/docs/Web/API/Element/attachShadow
[internals]: https://developer.mozilla.org/en-US/docs/Web/API/ElementInternals
[tabs]: https://www.w3.org/WAI/ARIA/apg/patterns/tabs/
[switch]: https://www.w3.org/WAI/ARIA/apg/patterns/switch/
[modules]: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Modules
[syntax]: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/SyntaxError
[lit-roots]: https://lit.dev/docs/components/shadow-dom/#implementing-createrenderroot
[measurement]: https://web.dev/articles/how-to-measure-speed
[budgets]: https://web.dev/articles/performance-budgets-101
[related-apps]: https://developer.mozilla.org/en-US/docs/Web/API/Navigator/getInstalledRelatedApps
[install-prompts]: https://developer.mozilla.org/en-US/docs/Web/API/BeforeInstallPromptEvent/prompt
[workers]: https://developer.mozilla.org/en-US/docs/Web/API/ServiceWorkerContainer/register
[origins]: https://developer.mozilla.org/en-US/docs/Web/Security/Same-origin_policy

Use current compatibility data for the project's target browsers rather than treating this review
date as a browser support guarantee.
