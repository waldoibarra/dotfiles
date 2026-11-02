# macOS default applications

**Keep the desired file association in Git and let the installer apply it.**

Read this before changing which app opens local Markdown links.
[`home/.config/duti/markdown.duti`](/home/.config/duti/markdown.duti) selects Cursor for the
Markdown file type. Dotbot links the single mapping into `~/.config/duti/markdown.duti`.
Homebrew owns `duti`; the installer applies the mapping after OS packages are installed.

The [application script](/scripts/configure-markdown-app.sh) skips non-macOS systems and
unavailable applications. It queries LaunchServices without launching the app.
Missing configuration, missing `duti`, and query/setter errors fail visibly.
If the current handler cannot be queried, the script stops without submitting a change.
The installer supplies the supported Apple Silicon Homebrew PATH for fresh-machine setup.

Apply only this setting from the repository root, then inspect the registered handler:

```sh
PATH="/opt/homebrew/bin:$PATH" ./scripts/configure-markdown-app.sh
duti -x md
```

Expect Cursor's name, application path, and bundle ID.
Already-correct state is a no-op: the script does not submit another change request.

macOS may ask permission for Markdown files, including `.md` and `.markdown`.

The script requests a change once.
It checks the effective handler before reporting success.
If the handler is not active, respond to any existing OS prompt before rerunning.
Do not queue repeated requests.
A successful duti exit alone does not prove the association changed.

This changes the current user's Markdown association across applications, not just Pi.
It does not change `EDITOR`, `VISUAL`, or Pi's external prompt editor.
Terminal-specific editor overrides and per-file choices can still affect a click; test a real link.

To choose another app, change the mapping's bundle ID and rerun the script.
Use the same process to undo this preference.
An OS-only manual change will be overwritten by the next installer run.
Keep the desired mapping in Git; never copy the machine's LaunchServices database into dotfiles.
