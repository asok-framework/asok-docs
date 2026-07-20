# Extension System

> **Keywords:** custom packages, pluggable extensions, plugin system, add package routes, templates hook

Asok includes a modular extension system allowing the community and third-party packages to extend the framework's capabilities. With extensions, you can package and distribute reusable controllers, layout templates, static assets, and custom CLI commands.

## 1. The `AsokExtension` Base Class

Every extension must inherit from `AsokExtension`. It provides standard lifecycle hooks and methods to register paths with the application.

```python
from asok.core.extension import AsokExtension
from asok import Asok

class MyExtension(AsokExtension):
    def init_app(self, app: Asok) -> None:
        """Initialize the extension with the Asok application instance."""
        super().init_app(app)
        # Custom setup logic (e.g., configuring services, reading configurations)

    def get_pages_path(self) -> Optional[str]:
        """Return the absolute path to the extension's pages/controllers directory."""
        return "/path/to/my_extension/pages"

    def get_templates_path(self) -> Optional[str]:
        """Return the absolute path to the extension's templates directory."""
        return "/path/to/my_extension/templates"

    def get_static_path(self) -> Optional[str]:
        """Return the absolute path to the extension's static assets directory."""
        return "/path/to/my_extension/static"
```

## 2. Registering an Extension

Extensions are registered in `wsgi.py` (or your application bootstrapper) by passing them to the `register_extension` or `register_extensions` method of the `Asok` app instance.

```python
# wsgi.py
from asok import Asok
from my_extension import MyExtension

app = Asok()

# Register a single extension (supports class or instance)
app.register_extension(MyExtension) 

# Or register multiple extensions at once
app.register_extensions([
    MyExtension(),
    AnotherExtension()
])
```

## 3. Extension Directories & Integration

When you register paths via your extension, Asok integrates them dynamically into its resolution pipelines:

### 3.1 Routing & Pages (`get_pages_path`)
All Python controllers (`page.py` files) located in the directory returned by `get_pages_path()` are mounted into the routing system automatically. 
* *Note*: If a route defined in the extension conflicts with a route defined in the main project's `src/pages/` folder, the main project's page takes precedence.

### 3.2 Templates & Components (`get_templates_path`)
The directory returned by `get_templates_path()` is appended to Asok's internal template search paths. If you try to render a template using `request.html("my_template.html")` or use `{{ component("MyComponent") }}`, the framework will look into the extension template path if it's not found in the main project.

### 3.3 Static Assets (`get_static_path`)
The directory returned by `get_static_path()` is appended to static asset search paths. Files like `/static/js/my_ext.js` or `/static/css/my_ext.css` residing in the extension are resolved and served automatically.

## 4. Custom CLI Commands

Extensions can register new commands in the `asok` command-line utility. Asok uses standard Python `entry_points` to detect and load extension commands.

### 4.1 Registering Entry Points
In your extension's `pyproject.toml` or `setup.py`, define your command under the `"asok.commands"` group:

**Using `pyproject.toml`:**
```toml
[project.entry-points."asok.commands"]
my_extension_cmd = "my_extension.cli:register_commands"
```

**Using `setup.py`:**
```python
setup(
    ...
    entry_points={
        "asok.commands": [
            "my_extension_cmd = my_extension.cli:register_commands",
        ],
    },
)
```

### 4.2 Implementing the Registration Function
The entry point must point to a function that accepts an `argparse` subparsers object and registers a parser.

```python
# my_extension/cli.py
import argparse

def register_commands(subparsers: argparse._SubParsersAction) -> None:
    # Add parser under the main asok CLI subparsers
    parser = subparsers.add_parser(
        "my-extension-command", 
        help="Run custom commands from my extension"
    )
    parser.add_argument("--option", type=str, help="An optional argument")
    
    # Associate a handler function with the parser
    parser.set_defaults(func=handle_command)

def handle_command(args: argparse.Namespace) -> None:
    print(f"My Extension CLI is executing with option: {args.option}")
```

Once installed, running `asok --help` will show `my-extension-command` in the list of available commands, and it can be run like any native command:
```bash
asok my-extension-command --option "value"
```
