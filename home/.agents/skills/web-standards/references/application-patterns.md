# Application Patterns

Read before forms, rendering, state, or routing changes.

## Contents

- State and rendering
- Forms and requests
- Navigation
- Optional installation and origin boundaries

## State and rendering

- Keep transient state local.
- Put shareable navigation/filter state in the URL when appropriate.
- Keep server-authoritative data authoritative on the server.
- Share state only across actual owners through explicit functions or events.
- Do not duplicate state in DOM, storage, and a store without an ownership and synchronization
  rule.
- Ordinary DOM events notify; they do not retain state or replay past dispatches.
- Subscribers that connect or reconnect after a change must initialize from the current state
  owner.

Rendering and untrusted content:

- Prefer targeted DOM updates that preserve focus, selection, and control values.
- Clone trusted static templates when useful.
- Use textContent for untrusted text.
- Validate URL schemes for untrusted destinations.
- Template literals are not HTML escaping.
- Do not send untrusted strings to innerHTML, insertAdjacentHTML, or equivalent sinks.
- Rich HTML requires a separately justified, maintained sanitization policy, not a homemade
  sanitizer.

Do not introduce Proxy-based reactivity by default:

- A Proxy does not automatically solve nested updates, dependencies, scheduling, cleanup, or
  rendering identity.

## Forms and requests

- Start with form, label, name, appropriate types, and native constraints.
- Controls in the useful baseline need visible, programmatically associated labels in that HTML.
  - Labels generated only from data-label by an enhancer do not count.
  - Dynamically added controls still need appropriate labels.
- Preserve action/method where a real server endpoint exists.
- Enhance the submit event rather than just a button click.
- Preserve Enter submission and submitter semantics.
- Use FormData when it matches the endpoint.
- When repeated names matter, retain FormData, use getAll(name), or explicitly map values to
  endpoint-compatible arrays.
  - Object.fromEntries(formData) keeps only the last value for each repeated name.
  - That conversion is valid when names are known to be unique.

Responses and request state:

- Client validation improves feedback but does not replace server validation or authorization.
- Represent pending, success, empty, and error states as required by the flow.
- Check response.ok; fetch does not reject merely because the server returns an HTTP error.
- Prevent stale requests from overwriting newer state.
- Handle cancellation without reporting it as an application failure.
- Never persist secrets in client code.
- Never mistake client route guards for access control.

## Navigation

- Prefer real href values and ordinary page navigation.
- For same-document routing, choose the Navigation API only after checking target support.
  - Register its navigate event with navigation.addEventListener("navigate", handler).
  - navigation.navigate() is a method, not an event.
- Only intercept eligible app destinations.
- Preserve downloads, external links, fragments, and form semantics.
- The initial page load needs its own initialization or server-rendered content.

If the browser target requires History API routing, keep it narrowly scoped:

- pushState does not fire popstate.
- Render explicitly after pushes and handle history traversal separately.
- Do not intercept modified clicks, non-primary clicks, or links targeting another browsing
  context.

In either approach:

- Verify direct deep links, refresh, Back/Forward, query strings, and unknown routes.
- Verify focus, title, and scroll behavior.
- Configure the actual server's deep-link handling; client routing alone cannot fix a server 404.
- Do not add routing to a single-page form that does not need it.

## Optional installation and origin boundaries

Apply this section only to requested installation/PWA or related cross-origin functionality.

Do not add a PWA or service worker by default.

Installation detection:

- Without a supported, applicable installation-detection result, installed state is unknown, not
  uninstalled.
- beforeinstallprompt is non-standard and not a mandatory platform capability.
- getInstalledRelatedApps reports only supported, configured related apps, not a device inventory.
  - Check its relationship requirements and top-level secure-context restrictions.
- An ordinary canonical/open URL does not guarantee launching an installed app.

Origin boundaries:

- An origin is a scheme/host/port tuple.
- Different origins, including related subdomains, have separate Web Storage and IndexedDB.
- Cookies follow different domain rules.
- Service-worker registration script and scope must be same-origin with the registering page.
- Document control is scope-limited.
- These rules do not prohibit all cross-origin resource requests.
- Preserve intentional authentication and security boundaries rather than prescribe origin
  consolidation.
