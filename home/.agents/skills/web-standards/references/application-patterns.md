# Application Patterns

Read before forms, rendering, state, or routing changes.

## State and rendering

Keep transient state local. Put shareable navigation/filter state in the URL when appropriate;
keep server-authoritative data authoritative on the server. Share state only across actual owners
through explicit functions or events. Do not duplicate state in DOM, storage, and a store without
an ownership and synchronization rule.

Prefer targeted DOM updates that preserve focus, selection, and control values. Clone trusted
static templates when useful. Use textContent for untrusted text and validate URL schemes for
untrusted destinations. Template literals are not HTML escaping. Do not send untrusted strings to
innerHTML, insertAdjacentHTML, or equivalent sinks. Rich HTML requires a separately justified,
maintained sanitization policy, not a homemade sanitizer.

Do not introduce Proxy-based reactivity by default. A Proxy does not automatically solve nested
updates, dependencies, scheduling, cleanup, or rendering identity.

## Forms and requests

Start with form, label, name, appropriate types, and native constraints. Preserve action/method
where a real server endpoint exists. Enhance the submit event rather than just a button click;
preserve Enter submission and submitter semantics. Use FormData when it matches the endpoint.

Client validation improves feedback but does not replace server validation or authorization.
Represent pending, success, empty, and error states as required by the flow. Check response.ok;
fetch does not reject merely because the server returns an HTTP error. Prevent stale requests
from overwriting newer state and handle cancellation without reporting it as an application failure.
Never persist secrets in client code or mistake client route guards for access control.

## Navigation

Prefer real href values and ordinary page navigation. For same-document routing, choose the
Navigation API only after checking target support. Its navigate event is registered with
navigation.addEventListener("navigate", handler); navigation.navigate() is a method, not an event.
Only intercept eligible app destinations. Preserve downloads, external links, fragments, and form
semantics. The initial page load needs its own initialization or server-rendered content.

If the browser target requires History API routing, keep it narrowly scoped: pushState does not
fire popstate; render explicitly after pushes and handle history traversal separately. Do not
intercept modified clicks, non-primary clicks, or links targeting another browsing context.

In either approach verify direct deep links, refresh, Back/Forward, query strings, unknown routes,
focus, title, and scroll behavior. Configure the actual server's deep-link handling; client routing
alone cannot fix a server 404. Do not add routing to a single-page form that does not need it.
