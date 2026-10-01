# Verification

Read before browser verification. Choose checks that exercise changed behavior, not every row
for every task. Use the project's existing tools; no specific agent host or browser tool is required.

| Changed surface | Exercise | Expected evidence |
| --- | --- | --- |
| Native UI | Keyboard, labels, focus, narrow viewport | Intended action is reachable and understandable |
| Enhancement | Block enhancement loading or fail its request | Useful baseline content and labels remain, or JS dependency is explicit |
| Form | Invalid, valid, Enter, repeated names, server error, repeat submission | Endpoint-compatible payload preserves required repeated values; feedback is recoverable |
| Component | Two instances, disconnect, reconnect after state changes | Independent behavior, current owned state, and one action per event |
| Async rendering | Slow earlier request finishes last | Current user intent is not overwritten |
| Untrusted data | Render HTML-shaped user text | Text remains inert; no injected element or execution |
| Routing | Direct URL, refresh, Back/Forward, external/modified link | URL and content agree; browser conventions survive |
| Shadow DOM | Accessible name, focus, events, styles, form if applicable | Boundary does not break consumer behavior |

Serve over HTTP and interact with the actual page. Observe rendered output and console/network
failures. Automated tests supplement this smoke run, not substitute for it. Run relevant existing
tests after edits; add regression tests for real behavioral risks, not source-string checks.

Record tested browser, commands/scenarios, outcomes, and untested browser targets. A single
Chromium run is not proof of Safari or Firefox compatibility.

When performance is in scope or a comparative claim is made, measure rather than infer improvement
from fewer dependencies. Use audience-representative devices/CPU and network conditions; record
cache state. Distinguish initial loading, interactions, and later navigation for the relevant
journeys. Measure transferred bytes and main-thread work alongside user-visible outcomes.
Identify lab measurements versus field evidence and report comparable conditions and limitations.
Derive any budgets from the audience and journey; impose no universal byte limits or scores.
