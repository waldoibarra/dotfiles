# Visual Studio Code — Default Settings Location (Global)

The settings are located in these paths:

- MacOS: `$HOME/Library/Application Support/Code/User/`
- Linux: `$HOME/.config/Code/User/`

> ⚠️ Since I'm using MacOS, I'll follow Linux directory structure in this project,
but will symlink the `settings.json` and `mcp.json` files to the MacOS path.

Doing this seems easier than using the CLI flag to change the default user
settings location, as I would have to do it every time I open the editor.

```bash
code --user-data-dir "$HOME/.config/Code/User/"
```
