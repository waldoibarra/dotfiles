# Components

Read before creating or modifying custom elements.

## Choose the smallest boundary

Use native elements when their semantics match. Use functions for reusable behavior without an
independent lifecycle. Introduce a custom element when a named, reusable unit owns behavior and
lifecycle. A hyphenated unregistered wrapper may organize markup, but supplies no native role.
Do not turn every layout container into a registered element.

Prefer Light DOM for application composition and shared styling. Preserve author-provided child
content during enhancement. Scope queries and listeners to the component; avoid document-wide
selectors that accidentally bind another instance.

## Lifecycle contract

Keep constructor work limited to instance setup; do not depend on parsed children or attributes
there. Initialize DOM-dependent behavior when available. Account for parser timing when upgrading
an element whose children may not yet exist.

Connection can happen repeatedly. Avoid duplicate listeners, timers, observers, and rendered nodes.
Release external subscriptions and pending work when disconnected. If using an AbortController for
listeners, create a new controller on reconnection; an aborted signal cannot be reused.
Guard registration where the loading arrangement can evaluate duplicate definitions.

Define property versus attribute behavior intentionally: attributes are strings; boolean attributes
use presence, not the string "false". Prevent reflection loops. Dispatch documented CustomEvents
with meaningful detail; choose bubbles and composed according to the public boundary, not by habit.

## Shadow DOM gate

Use Shadow DOM for justified internal isolation, not because a component tutorial does. Account
for slots, inherited properties, CSS custom properties/parts, event retargeting, focus, and accessible
names. Closed roots do not protect secrets or prevent hostile same-page code.

Prefer native form controls. A custom form-associated control needs ElementInternals and explicit
value, validity, reset, disabled, and restoration behavior where applicable. Verify the target
browsers and real form submission; a visually convincing input is not enough.
