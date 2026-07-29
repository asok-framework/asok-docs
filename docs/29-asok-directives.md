# Asok Directives

> **Keywords:** client side reactivity, reactive directives, asok click, asok model, asok show, asok text, frontend directives

Asok includes native reactive directives for building interactive UIs without custom JavaScript. These directives are automatically processed by a lightweight, built-in runtime (~5KB).

## Production Requirements & Zero-Eval Security

Asok achieves **Zero-Eval Security** in production for all reactive directives:

*   **No `'unsafe-eval'` Required**: Unlike other lightweight reactive frameworks, Asok does not require the `'unsafe-eval'` directive in your Content Security Policy (CSP).
*   **Server-Side Precompilation**: All JavaScript expressions inside `asok-*` attributes are precompiled on the server into safe JavaScript functions.
*   **Cryptographically Nonced Injection**: Precompiled functions are registered in the browser using standard `<script>` tags protected by a cryptographically strong request `nonce` (both during initial render and dynamic WebSocket updates).
*   **Enterprise-Grade Protection**: Your production applications can enforce an exceptionally strict CSP that blocks `'unsafe-eval'` completely, keeping you fully protected against Cross-Site Scripting (XSS).

If you are using third-party libraries that require `eval()`, you can still manually force it by adding `CSP_UNSAFE_EVAL=true` to your `.env` file. Otherwise, no configuration is required!

## Directives & Islands Architecture (Selective Hydration)

With the introduction of the **Islands Architecture**, `asok-*` directives are integrated with selective client-side hydration:
* **Inside Islands**: Directives within components using `client:load`, `client:visible`, or `client:idle` are hydrated dynamically according to their respective triggers.
* **Outside Islands (Static)**: Directives outside of interactive islands are served statically as plain HTML, avoiding any overhead on the client side.
* **Zero JS Overhead**: If a page contains no interactive components or active directives, Asok skips injecting the directives runtime (`asok_directives.min.js`) completely.

## State Management


### `asok-state` — Component state

Define reactive local state for a component:

```html
<div asok-state="{ count: 0, name: 'Alice' }">
  <p asok-text="'Count: ' + count"></p>
  <p asok-text="'Name: ' + name"></p>
  <button asok-on:click="count++">Increment</button>
</div>
```

State is scoped to the component and its children. Changes trigger automatic re-renders.

### `$store` — Global state

Access shared state across all components:

```html
<!-- Component 1 -->
<div asok-state="{}">
  <button asok-on:click="$store.theme = 'dark'">Dark Mode</button>
</div>

<!-- Component 2 (updates automatically) -->
<div asok-state="{}" asok-class="$store.theme === 'dark' ? 'bg-black text-white' : ''">
  <span asok-text="'Current theme: ' + $store.theme"></span>
</div>
```

The store uses **dependency tracking** — only components that use a property are updated when it changes (10-20x faster than updating everything).

Access from JavaScript:

```javascript
window.Asok.store.theme = 'dark';
window.Asok.store.user = { name: 'Alice', role: 'admin' };
```

## Display & Visibility

### `asok-show` / `asok-hide`

Toggle element visibility with `display: none`:

```html
<div asok-state="{ visible: true }">
  <div asok-show="visible">I'm visible</div>
  <div asok-hide="visible">I'm hidden</div>
  <button asok-on:click="visible = !visible">Toggle</button>
</div>
```

### `asok-text`

Set text content reactively:

```html
<div asok-state="{ count: 0 }">
  <p asok-text="'Count: ' + count"></p>
  <button asok-on:click="count++">+</button>
</div>
```

## Class & Attribute Binding

### `asok-class` — Dynamic classes

Three syntaxes for maximum flexibility:

```html
<div asok-state="{ isOpen: false, status: 'success' }">
  <!-- 1. Toggle a single class -->
  <div asok-class:active="isOpen">Toggle</div>

  <!-- 2. Conditional expression -->
  <div asok-class="isOpen ? 'text-blue-500 font-bold' : 'text-red-500'">
    Conditional classes
  </div>

  <!-- 3. Object (multiple toggles) -->
  <div asok-class="{ 'active': isOpen, 'disabled': !enabled, 'success': status === 'success' }">
    Multiple classes
  </div>
</div>
```

Perfect for Tailwind CSS with long class lists:

```html
<div asok-class="isOpen ? 'bg-white px-4 py-2 border border-gray-300 rounded-md shadow-sm' : 'bg-gray-100'">
  ...
</div>
```

### `asok-bind:attr`

Bind any HTML attribute:

```html
<div asok-state="{ url: '/page', disabled: false }">
  <a asok-bind:href="url">Link</a>
  <button asok-bind:disabled="disabled">Button</button>
  <input asok-bind:placeholder="'Enter ' + fieldName">
</div>
```

## Forms & Input

### `asok-model`

Two-way data binding for form inputs:

```html
<div asok-state="{ name: '', email: '' }">
  <input asok-model="name" placeholder="Name">
  <input type="email" asok-model="email" placeholder="Email">

  <p asok-text="'Hello ' + name + '! Your email is ' + email"></p>
</div>
```

Works with:
- Text inputs (`<input type="text">`)
- Checkboxes (`<input type="checkbox">`)
- Radio buttons (`<input type="radio">`)
- Select dropdowns (`<select>`)
- Textareas (`<textarea>`)

## Event Handling

### `asok-on:event`

Listen to any DOM event:

```html
<div asok-state="{ count: 0 }">
  <button asok-on:click="count++" asok-text="'Clicked ' + count + ' times'"></button>
  <input asok-on:input="count = $event.target.value.length">
  <div asok-on:mouseenter="hovered = true">Hover me</div>
</div>
```

Event modifiers:

```html
<!-- Prevent default -->
<form asok-on:submit.prevent="handleSubmit()">...</form>

<!-- Stop propagation -->
<button asok-on:click.stop="doSomething()">Click</button>

<!-- Debounce (300ms default) -->
<input asok-on:input.debounce-500="search()">

<!-- Key filters -->
<input asok-on:keydown.enter="submit()">
<input asok-on:keydown.escape="close()">

<!-- Outside clicks -->
<div asok-on:click.outside="open = false">...</div>
```

## Conditional Rendering

### `asok-if` / `asok-elif` / `asok-else`

Conditional rendering (elements are removed from DOM):

```html
<div asok-state="{ role: 'admin', count: 5 }">
  <template asok-if="role === 'admin'">
    <p>Admin panel</p>
  </template>
  <template asok-elif="role === 'user'">
    <p>User dashboard</p>
  </template>
  <template asok-else>
    <p>Guest view</p>
  </template>
</div>
```

## Loops

### `asok-for`

Iterate over arrays:

```

### Keyed Reconciliation (`asok-key`)

To optimize DOM updates and preserve element state when list items are reordered, filtered, or mutated, use `asok-key` to specify a unique item identifier:

```html
<div asok-state="{ users: [{ id: 101, name: 'Alice' }, { id: 102, name: 'Bob' }] }">
  <ul>
    <template asok-for="u in users" asok-key="u.id">
      <li><span asok-text="u.name"></span></li>
    </template>
  </ul>
</div>
```

## Data Fetching

### `asok-fetch` — Declarative HTTP requests

Fetch JSON data automatically:

```html
<!-- Auto-fetch on mount -->
<div asok-state="{ users: null, loading: false, error: null }"
     asok-fetch="/api/users"
     asok-fetch-as="users">

  <div asok-show="loading">Loading...</div>
  <div asok-show="error" asok-text="'Error: ' + error"></div>

  <div asok-show="users">
    <p><span asok-text="users.length"></span> users loaded</p>
  </div>
</div>

<!-- Fetch on click -->
<button asok-fetch="/api/products"
        asok-fetch-as="products"
        asok-fetch-on="click">
  Load Products
</button>
```

**Attributes:**
- `asok-fetch="/url"` — URL to fetch (GET request)
- `asok-fetch-as="varname"` — Variable name (default: "data")
- `asok-fetch-on="event"` — Trigger event (default: "load")

Automatically sets `loading` and `error` in the component state.

### `asok-fetch-async` — Custom async expressions

For more control, use async JavaScript expressions:

```html
<div asok-state="{ data: null, loading: false, error: null }">
  <!-- Single fetch -->
  <button asok-fetch-async="data = await fetch('/api/users').then(r => r.json())">
    Load
  </button>

  <!-- Parallel fetches -->
  <button asok-fetch-async="[users, products] = await Promise.all([
    fetch('/api/users').then(r => r.json()),
    fetch('/api/products').then(r => r.json())
  ])">
    Load All
  </button>
</div>
```

**Attributes & Behavior:**
- **Trigger**: Defaults to `click` (ideal for buttons). You can set `asok-fetch-on="load"` to run it automatically when the component mounts/loads.
- **Assignment**: Unlike `asok-fetch`, it does **not** use `asok-fetch-as`. You must assign the returned data directly inside the expression (e.g. `my_var = await ...`).

### Choosing between `asok-fetch` and `asok-fetch-async`

| Use Case | `asok-fetch` | `asok-fetch-async` |
|---|---|---|
| **URL Type** | Static strings only (e.g., `"/api/users"`) | Dynamic expressions (e.g., `"/api/users/" + userId`) |
| **Default Trigger** | `load` (executes immediately on mount) | `click` (executes on click, customize with `asok-fetch-on`) |
| **Usage Style** | Declarative (zero custom JavaScript) | Code expression (using native `await fetch(...)`) |
| **HTTP Methods** | `GET` requests only | Any method (`GET`, `POST`, `PUT`, `DELETE`, headers, etc.) |
| **Capabilities** | ❌ Basic property binding only |  Can chain `.then()` or parallelize with `Promise.all()` |

## Advanced

### `asok-ref`

Get a reference to an element:

```html
<div asok-state="{}">
  <input asok-ref="emailInput">
  <button asok-on:click="$refs.emailInput.focus()">Focus Email</button>
</div>
```

### `asok-init`

Run code when component initializes:

```html
<div
  asok-state="{ time: null }"
  asok-init="
    time = new Date().toLocaleTimeString();

    setInterval(() => {
      time = new Date().toLocaleTimeString();
    }, 1000);
  "
>
  <p>Heure actuelle : <span asok-text="time"></span></p>
</div>

```

### `asok-teleport`

Render content in a different location:

```html
<template asok-teleport="#modal-container">
  <div class="modal">Modal content</div>
</template>

<!-- Elsewhere in the page -->
<div id="modal-container"></div>
```

### `asok-cloak`

Hide element until directives are initialized (prevents flash of unstyled content):

```html
<style>
  [asok-cloak] { display: none; }
</style>

<div asok-state="{ loaded: false, message: 'Hello' }" asok-cloak>
  <span asok-text="message"></span>
</div>
```

## Built-in Theme Management

Asok provides a zero-JS declarative theme toggle system with native anti-FOUC (Flash of Unstyled Content) protection:

```html
<!-- Toggle between dark and light mode -->
<button asok-theme-toggle>Toggle Theme</button>

<!-- Specific mode triggers -->
<button asok-theme-toggle="dark">Dark Mode</button>
<button asok-theme-toggle="light">Light Mode</button>
<button asok-theme-toggle="system">Follow OS Theme</button>

<!-- Reactive Store Binding -->
<div asok-bind:class="{ 'bg-dark text-white': $store.theme === 'dark' }">
  Current theme: <span asok-text="$store.theme"></span>
</div>
```

- **Anti-FOUC**: Injects a 3-line synchronous script in `<head>` that sets `color-scheme` and `data-theme` before the first browser paint.
- **Persistence**: Theme choice (`dark`, `light`, `system`) is saved under `localStorage.getItem('asok-theme')`.
- **JS API**: `window.Asok.setTheme('dark')`, `window.Asok.toggleTheme()`, `window.Asok.getTheme()`.

## RGPD / GDPR Cookie Consent

Manage cookie compliance declaratively with automatic script blocking:

```html
<!-- Cookie Consent Banner (auto-hidden once choice is saved) -->
<div asok-cookie-banner class="cookie-banner">
  <p>We use cookies to improve your experience.</p>
  <button asok-cookie-accept class="btn btn-primary">Accept</button>
  <button asok-cookie-reject class="btn btn-default">Decline</button>
</div>

<!-- Footer reset link -->
<a href="#" asok-cookie-reset>Manage cookie preferences</a>

<!-- Analytics script blocked until user accepts cookies -->
<script type="text/plain" asok-cookie-script src="https://www.googletagmanager.com/gtag/js?id=UA-XXXXX"></script>
```

- **Reactive Store**: `$store.cookieConsent` returns `'accepted'`, `'rejected'`, or `'pending'`.
- **JS API**: `window.Asok.acceptCookies()`, `window.Asok.rejectCookies()`, `window.Asok.resetCookieConsent()`.

## Dismissible Elements & Announcements

Per-element dismissals for announcements, alerts, and banners:

```html
{% for a in announcements %}
<div asok-dismiss="announcement-{{ a.id }}" class="alert">
  <span>{{ a.message }}</span>
  <button asok-dismiss-trigger class="close-btn">&times;</button>
</div>
{% endfor %}
```

- **Persistence**: Remembers dismissal per key in `localStorage` under `asok-dismiss:key`.
- **JS API**: `window.Asok.dismiss('key')`, `window.Asok.isDismissed('key')`.

## Zero-JS UI Directives

### `asok-copy` — Copy to Clipboard

Copy static text, input field contents, target elements (`#id`), or code blocks (`<pre>`) with rich visual feedback:

```html
<!-- 1. Copy explicit text -->
<button asok-copy="DISCOUNT20">Copy Code</button>

<!-- 2. Copy from target input or element selector -->
<button asok-copy="#input-field">Copy Input</button>

<!-- 3. Text label swap on copy (swaps to "Copied!" for 2 seconds) -->
<button asok-copy="SECRET" data-label="Copy" data-copied="Copied!">Copy</button>

<!-- 4. Inside code blocks (auto-finds <pre> tag in parent .code-block) -->
<div class="code-block">
  <button asok-copy data-label="Copy" data-copied="Copied!">Copy</button>
  <pre><code>print("Hello World")</code></pre>
</div>
```

- **Automatic Target Resolution**: If `asok-copy` is empty on a button inside a `.code-block`, Asok automatically locates and copies the content of the contained `<pre>` or `<code>` tag.
- **Visual Feedback**:
  - Adds `.asok-copied` class to the button for 2 seconds.
  - Automatically appends a `✓` checkmark via `.asok-copied::after` if no `data-copied` attribute is set.
  - If `data-copied` (or `asok-copied-text`) is set, temporarily swaps button text to the custom label for 2 seconds before restoring the original text (`data-label` or `textContent`).
- **Custom Event**: Dispatches `asok:copied` on `document` with `{ text, element }` details.

### `asok-modal` — Accessible Modals
Declarative modal management with automatic backdrop click and `Escape` key support:
```html
<button asok-modal-open="my-modal">Open Modal</button>

<dialog asok-modal="my-modal" class="modal">
  <h2>Modal Title</h2>
  <p>Modal content...</p>  <button asok-modal-close>Close</button>
</dialog>
```

### `asok-tabs` — Tabbed Interfaces
Zero-code tabs with ARIA attribute management:
```html
<div asok-tabs>
  <button asok-tab="tab1">Tab 1</button>
  <button asok-tab="tab2">Tab 2</button>

  <div asok-tab-panel="tab1">Content for Tab 1</div>
  <div asok-tab-panel="tab2" style="display: none">Content for Tab 2</div>
</div>
```

### `asok-scroll-top` & `asok-scroll-to` — Smooth Scrolling
Smart back-to-top button (automatically hidden if content fits on screen or scroll position is near top):
```html
<button asok-scroll-top="300">Back to top</button>
<button asok-scroll-to="#pricing">View Pricing</button>
```

### `asok-char-count` — Character Counter
Live remaining character counter for inputs and textareas:
```html
<textarea id="bio" maxlength="200"></textarea>
<span asok-char-count="#bio"></span>
```

### `asok-progress` — Top Navigation Progress Bar
Declarative top page-loading progress bar:
```html
<div asok-progress class="fixed top-0 left-0 right-0 z-70 h-0.5 opacity-0 pointer-events-none transition-opacity duration-200">
  <div class="h-full w-0 bg-accent shadow-[0_0_8px_var(--color-accent)] transition-[width] duration-700 ease-out"></div>
</div>
```

- **Automatic Navigation Tracking**: Listens to internal link clicks, form submissions, SPA page transitions, and `asok:before`/`asok:success`/`asok:error` events.
- **Smooth Fill**: Automatically animates fill width to 90% during request, and completes to 100% before fading out.
- **JS API**: `window.Asok.startProgress()`, `window.Asok.finishProgress()`.

## HTML Attribute Aliases & Data Attributes

All Asok UI directives support standard `data-asok-*` and `data-*` prefixes for strict HTML5 validation compliance:

| Feature / Utility | Primary Attribute | HTML5 `data-asok-*` Alias | HTML5 `data-*` Alias |
|---|---|---|---|
| **Theme Toggle** | `asok-theme-toggle` | `data-asok-theme-toggle` | `data-theme-toggle` |
| **Cookie Banner** | `asok-cookie-banner` | `data-asok-cookie-banner` | `data-cookie-banner` |
| **Cookie Accept** | `asok-cookie-accept` | `data-asok-cookie-accept` | `data-cookie-accept` |
| **Cookie Reject** | `asok-cookie-reject` | `data-asok-cookie-reject` | `data-cookie-reject` |
| **Cookie Reset** | `asok-cookie-reset` | `data-asok-cookie-reset` | `data-cookie-reset` |
| **Cookie Script** | `asok-cookie-script` | `data-asok-cookie-script` | `data-cookie-script` |
| **Dismissible UI** | `asok-dismiss` | `data-asok-dismiss` | `data-dismiss` |
| **Dismiss Trigger** | `asok-dismiss-trigger` | `data-asok-dismiss-trigger` | `data-dismiss-trigger` |
| **Copy Clipboard** | `asok-copy` | `data-asok-copy` | `data-copy` |
| **Modal Dialog** | `asok-modal` | `data-asok-modal` | `data-modal` |
| **Modal Open** | `asok-modal-open` | `data-asok-modal-open` | `data-modal-open` |
| **Modal Close** | `asok-modal-close` | `data-asok-modal-close` | `data-modal-close` |
| **Scroll Top** | `asok-scroll-top` | `data-asok-scroll-top` | `data-scroll-top` |
| **Scroll To** | `asok-scroll-to` | `data-asok-scroll-to` | `data-scroll-to` |
| **Char Counter** | `asok-char-count` | `data-asok-char-count` | `data-char-count` |
| **Tab Group** | `asok-tabs` | `data-asok-tabs` | `data-tabs` |
| **Tab Header** | `asok-tab` | `data-asok-tab` | `data-tab` |
| **Tab Panel** | `asok-tab-panel` | `data-asok-tab-panel` | `data-tab-panel` |
| **Page Progress** | `asok-progress` | `data-asok-progress` | `data-progress` |
| **Keyed List** | `asok-key` | `asok-key-ref` | `data-key` |

## Special Variables

Inside directive expressions, you have access to:

| Variable | Description |
|---|---|
| `$store` | Global store (shared across components) |
| `$el` | Current element |
| `$event` | Event object (in event handlers) |
| `$refs` | Object of referenced elements |
| `$nextTick(fn)` | Run function after next DOM update |

## Example: Complete Todo App

```html
<div class="todo-app" asok-state="{ todos: [], newTodo: '', filter: 'all' }">
  <h1>📝 Asok Todo List</h1>

  <!-- Add todo form -->
  <form asok-on:submit.prevent="todos.push({text: newTodo, done: false}); newTodo = ''">
    <input type="text" asok-model="newTodo" placeholder="What needs to be done?" required>
    <button type="submit">Add</button>
  </form>

  <!-- Filter buttons -->
  <div style="margin: 20px 0;">
    <button asok-on:click="filter = 'all'" asok-class:active="filter === 'all'">All</button>
    <button asok-on:click="filter = 'active'" asok-class:active="filter === 'active'">Active</button>
    <button asok-on:click="filter = 'done'" asok-class:active="filter === 'done'">Done</button>
  </div>

  <!-- Todo list -->
  <ul>
    <template asok-for="todo in todos.filter(t => filter === 'all' || (filter === 'active' && !t.done) || (filter === 'done' && t.done))">
      <li asok-class="{ 'line-through': todo.done }">
        <input type="checkbox" asok-model="todo.done">
        <span asok-text="todo.text"></span>
        <button class="delete-btn" asok-on:click="todos.splice(index, 1)">×</button>
      </li>
    </template>
  </ul>

  <!-- Stats -->
  <div class="stats">
    <p><span asok-text="todos.filter(t => !t.done).length"></span> items left</p>
    <p><span asok-text="todos.length"></span> total items</p>
  </div>
</div>
```
