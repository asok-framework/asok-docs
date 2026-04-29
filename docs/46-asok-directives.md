# Asok Directives

Asok Directives is a lightweight (< 3KB) client-side reactive engine built directly into the framework. It allows you to build interactive UI components (like dropdowns, modals, and tabs) using simple HTML attributes, without writing any custom JavaScript.

Inspired by Alpine.js, it provides a powerful "Zero JS" approach to frontend interactivity while being fully integrated with Asok's SPA and Component system.

## Basic Usage

To create a reactive scope, use the `asok-state` directive. All children of this element can access and mutate the defined state.

```html
<div asok-state="{ count: 0 }">
    <button asok-on:click="count--">-</button>
    <span asok-text="count"></span>
    <button asok-on:click="count++">+</button>
</div>
```

---

## Core Directives

| Directive | Description | Usage Example |
| :--- | :--- | :--- |
| `asok-state` | Defines a local reactive state scope. | `asok-state="{ count: 0 }"` |
| `asok-text` | Sets the text content of an element. | `asok-text="count"` |
| `asok-html` | Sets the inner HTML (scripts are stripped). | `asok-html="description"` |
| `asok-show` | Toggles visibility (sets `display: none` when false). | `asok-show="isOpen"` |
| `asok-hide` | Hides the element if the expression is truthy. | `asok-hide="isDone"` |
| `asok-model` | Two-way data binding for form elements. | `asok-model="username"` |
| `asok-on:[ev]` | Event listeners with modifiers (`.prevent`, `.stop`, `.outside`, etc.). | `asok-on:click="do()"` |
| `asok-bind:[attr]` | Dynamic HTML attribute binding. | `asok-bind:src="imgUrl"` |
| `asok-class:[cls]` | Conditional CSS class management. | `asok-class:active="tab === 1"` |
| `asok-for` | Reactive loops (must be used on `<template>`). | `asok-for="item in items"` |
| `asok-if` | Structural conditional rendering (must be used on `<template>`). | `asok-if="count > 0"` |
| `asok-teleport` | Moves content to another DOM node (must be used on `<template>`). | `asok-teleport="body"` |
| `asok-init` | Lifecycle hook: runs when the element is initialized. | `asok-init="fetch()"` |
| `asok-ref` | Marks an element for easy access via `$refs`. | `asok-ref="myInput"` |
| `asok-cloak` | Hides the element until the Asok engine is ready. | `asok-cloak` |

---

### `asok-state`
Initializes a new reactive scope with a JSON object.
```html
<div asok-state="{ open: false, title: 'Hello' }">...</div>
```

### `asok-on:[event]`
Attaches an event listener to the element. You can use any native DOM event (click, input, submit, change, mouseover, etc.).

**Modifiers:**
- `.prevent`: Calls `event.preventDefault()`
- `.stop`: Calls `event.stopPropagation()`
- `.outside`: Triggers only when clicking outside the element (perfect for modals).
- `.debounce`: Debounces the execution (default 300ms, or `.debounce-500`).
- **Keyboard Modifiers**: `.enter`, `.escape`, `.space`, `.tab` (e.g., `asok-on:keydown.enter="add()"`).

```html
<button asok-on:click.outside="open = false">Close</button>
<input asok-on:keydown.enter="submitForm()" placeholder="Press Enter to submit">
```

### `asok-text` & `asok-html`
Sets the text content or inner HTML of an element.
```html
<span asok-text="user.name"></span>
<div asok-html="formattedBio"></div>
```

### `asok-show` & `asok-hide`
Toggles visibility by setting `display: none`.
- `asok-show`: Visible when the expression is truthy.
- `asok-hide`: Hidden when the expression is truthy.

> [!TIP]
> When visible, `asok-show` adds a `data-show-active` attribute, allowing you to trigger CSS transitions or flexbox displays (e.g., `.modal[data-show-active] { display: flex; }`).

### `asok-class:[classname]`
Conditionally adds/removes a CSS class.
```html
<button asok-class:active="tab === 'home'">Home</button>
```

### `asok-bind:[attribute]`
Dynamically binds any HTML attribute.
```html
<input asok-bind:placeholder="myPlaceholder" asok-bind:disabled="!isFormValid">
```

### `asok-if`, `asok-elif`, `asok-else`
Conditionally renders parts of the DOM. These directives **must** be used on a `<template>` tag. They form a linked chain where only one branch is rendered at a time.

```html
<template asok-if="score > 90">🏆 Champion</template>
<template asok-elif="score > 50">🥈 Good</template>
<template asok-else>🥉 Keep trying</template>
```

### `asok-for`
Iterates over an array and renders a template for each item. Must be used on a `<template>` tag. 
Provides access to the item variable (e.g., `item`) and a magic `index` variable.

```html
<template asok-for="task in tasks">
    <li>
        <span asok-text="index + 1"></span>. <span asok-text="task"></span>
        <button asok-on:click="tasks.splice(index, 1)">x</button>
    </li>
</template>
```

### `asok-model`
Enables two-way data binding on form elements.
```html
<input type="text" asok-model="username">
```

---

## Advanced Features

### Lifecycle Hooks (`asok-init`)
Execute code as soon as the element is initialized.
```html
<div asok-state="{ data: null }" asok-init="data = 'Ready!'">...</div>
```

### References (`asok-ref`)
Mark an element to be accessed via the `$refs` magic variable within its parent scope.
```html
<input asok-ref="searchField">
<button asok-on:click="$refs.searchField.focus()">Focus</button>
```

### Teleportation (`asok-teleport`)
Moves content to a different part of the DOM while maintaining its reactive connection to the parent state. **Must be used on a `<template>` tag.**

```html
<template asok-teleport="body">
    <div class="modal" asok-show="open">...</div>
</template>
```

### Cloaking (`asok-cloak`)
Hides elements until Asok has finished processing them. Asok automatically injects the necessary CSS for `asok-cloak`.

```html
<div asok-cloak asok-state="{ count: 0 }">...</div>
```

---

## Magic Variables

Inside your expressions, you have access to several "magic" variables:

- **`$el`**: The current element.
- **`$event`**: The native DOM event object (only in `asok-on`).
- **`$refs`**: Access to all elements marked with `asok-ref` in the current scope.
- **`$store`**: Access to the [Global Store](#global-store).
- **`$nextTick`**: Execute a function after the next DOM update cycle.
    ```html
    <button asok-on:click="count++; $nextTick(() => { ... })">Update</button>
    ```

---

## Global Store

Asok provides a global reactive store accessible from any component on the page.

### Registering Store Data
You can initialize store data via JavaScript:
```javascript
window.Asok.store.theme = 'dark';
window.Asok.store.user = { name: 'Ludo' };
```

### Using Store Data in HTML
Access the store using the `$store` prefix in any directive.
```html
<body asok-class:dark-mode="$store.theme === 'dark'">
    <span asok-text="$store.user.name"></span>
</body>
```

Updating the store automatically triggers re-renders across all elements using that data.

---

[← Previous: Native Vector Search](45-vector-search.md) | [Documentation](README.md)

---

## Production Deployment

### `asok build`
Generates a production-ready, optimized distribution of your project in the `dist/` directory.

```bash
asok build
```

**What it does:**
- Clones your project into `dist/` (ignoring dev files).
- Minifies JS, CSS, and **HTML** assets in-place.
- Optimizes Tailwind CSS and removes the source `base.css`.
- Compiles Python code to bytecode (`.pyc`) and **removes source `.py` files** by default.
- Generates a `.env.production` template.

**Options:**
- `--keep-source`: Keeps the original `.py` files alongside the compiled bytecode.
- `--output [name]`: Custom name for the distribution directory (defaults to `dist`).

### `asok preview`
Starts a production-like server locally using the built project in `dist/`.

```bash
cd dist
asok preview
```
