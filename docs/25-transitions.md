# Transitions

Asok provides a powerful, native transition system inspired by SvelteKit to add **ultra-smooth animations** to your UI. Transitions work seamlessly with the Reactive Engine, WebSockets, and SPA navigation.

## Overview

Transitions in Asok are **independent** and **opt-in**. The JavaScript and CSS required for animations are only injected into the page if the `asok-transition` attribute is detected in your template.

✨ **New in v0.1.6**: Enhanced transitions with professional easing curves, 3 new transition types, and full SPA page transitions!

## Usage

### Block Transitions

To animate an element during a swap, add the `asok-transition` attribute to it.

```html
<div id="content" asok-transition="fade">
    Initial Content
</div>

<button data-url="/update" data-block="content">
    Update
</button>
```

### Supported Types

Asok comes with 6 built-in transition types using optimized easing curves:

| Type | Description | Easing |
| :--- | :--- | :--- |
| `fade` | Smooth opacity transition (default). | `ease-out` |
| `slide` | Horizontal slide and fade effect. | `cubic-bezier(0.16, 1, 0.3, 1)` (expo) |
| `scale` | Subtle scale up/down with fade. | `cubic-bezier(0.25, 1, 0.5, 1)` (quart) |
| `fly` ⭐ **NEW** | Vertical fly in/out effect. | `cubic-bezier(0.16, 1, 0.3, 1)` (expo) |
| `blur` ⭐ **NEW** | Blur and fade (modern, subtle). | `ease-out` |
| `bounce` ⭐ **NEW** | Elastic bounce effect. | `cubic-bezier(0.68, -0.6, 0.32, 1.6)` (back) |

### Customizing Duration

You can specify the duration (in milliseconds) as a second parameter in the attribute:

```html
<!-- Slow fade -->
<div asok-transition="fade 600">...</div>

<!-- Fast slide -->
<div asok-transition="slide 150">...</div>

<!-- Elastic bounce -->
<div asok-transition="bounce 400">...</div>
```

## Page Transitions (SPA Navigation) ⭐ NEW

Add **fluid page transitions** during SPA navigation, just like SvelteKit! Simply add `data-asok-page-transition` to your main content container.

### Basic Usage

```html
<!-- In your base template (e.g., base.html) -->
<main data-asok-page-transition="page">
    {% block content %}{% endblock %}
</main>
```

Now every SPA navigation will have a smooth fade + scale transition!

### Available Page Transitions

```html
<!-- Default: Subtle scale + fade (recommended) -->
<main data-asok-page-transition="page">

<!-- Pure fade -->
<main data-asok-page-transition="fade">

<!-- Fly from bottom -->
<main data-asok-page-transition="fly">

<!-- Bounce effect -->
<main data-asok-page-transition="bounce">

<!-- Custom duration (250ms default) -->
<main data-asok-page-transition="page 400">
```

### Complete Example

```html
<!DOCTYPE html>
<html>
<head>
    <title>My App</title>
</head>
<body>
    <nav>
        <a href="/" data-block="content" data-push-url>Home</a>
        <a href="/about" data-block="content" data-push-url>About</a>
    </nav>

    <!-- Page transitions enabled -->
    <main id="content" data-asok-page-transition="page 300">
        {% block content %}{% endblock %}
    </main>
</body>
</html>
```

✨ **Result**: Smooth page transitions on every navigation, with automatic scroll-to-top!

## How it Works

When a swap is triggered (via `data-block`, `ws-*`, or `data-sse`), the framework:
1. Detects if the target element has an `asok-transition` attribute.
2. Applies a `leaving` class to the old content.
3. Performs the actual DOM swap after the "out" animation finishes.
4. Applies an `entering` class to the new content to trigger the "in" animation.

## WebSocket Support

Transitions work automatically with **Alive Components**. If your component root or any internal block has the attribute, updates pushed via WebSocket will be animated.

```python
# In a component or page
from asok import Request

def render(request: Request):
    return f"""
    <div id="live-clock" asok-transition="fade">
        {datetime.now()}
    </div>
    """
```

## Professional Easing Curves

Asok uses optimized cubic-bezier curves for ultra-smooth animations:

```css
:root {
  --ease-out-quart: cubic-bezier(0.25, 1, 0.5, 1);
  --ease-out-expo: cubic-bezier(0.16, 1, 0.3, 1);
  --ease-in-out-back: cubic-bezier(0.68, -0.6, 0.32, 1.6);
}
```

These are the same curves used by modern frameworks like SvelteKit and Framer Motion for buttery-smooth animations.

## CSS Customization

The framework injects standard CSS classes. You can override them in your own stylesheets for custom effects:

**Block transitions:**
- `.asok-fade-out`, `.asok-fade-in`
- `.asok-slide-out`, `.asok-slide-in`
- `.asok-scale-out`, `.asok-scale-in`
- `.asok-fly-out`, `.asok-fly-in` ⭐ NEW
- `.asok-blur-out`, `.asok-blur-in` ⭐ NEW
- `.asok-bounce-out`, `.asok-bounce-in` ⭐ NEW

**Page transitions:**
- `.asok-page-out`, `.asok-page-in` ⭐ NEW

**State classes:**
- `.is-leaving`, `.is-entering`

### Custom Transition Example

```css
/* Override slide transition with your own effect */
.asok-slide-out.is-leaving {
  transform: translateX(-50px) rotate(-5deg);
  opacity: 0;
  transition: all 400ms cubic-bezier(0.34, 1.56, 0.64, 1);
}

.asok-slide-in.is-entering {
  transform: translateX(0) rotate(0);
  opacity: 1;
  transition: all 400ms cubic-bezier(0.34, 1.56, 0.64, 1);
}
```

## Performance Tips

1. **Use `fade` or `page` for best performance** - they only animate opacity and scale (GPU-accelerated).
2. **Avoid `blur` on low-end devices** - filter effects can be CPU-intensive.
3. **Keep durations under 400ms** - users expect fast transitions in web apps.
4. **Test on mobile** - animations should feel just as smooth on phones.

## Comparison with SvelteKit

| Feature | SvelteKit | Asok v0.1.6 |
|---------|-----------|-------------|
| Built-in transitions | 7 types | 6 types |
| Custom easing | ✅ | ✅ |
| Duration control | ✅ | ✅ |
| Page transitions | ✅ | ✅ |
| GPU acceleration | ✅ | ✅ |
| Bundle size | ~15KB | ~3KB minified |

🎉 **Asok now matches SvelteKit's transition quality with 80% less code!**

---
[← Previous: Reactive Components](24-reactive-components.md) | [Documentation](README.md) | [Next: HTML Streaming →](26-html-streaming.md)
