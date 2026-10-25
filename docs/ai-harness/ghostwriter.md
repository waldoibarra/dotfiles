# Ghostwriter writing profiles

[`home/.config/ghostwriter/soul.md`](/home/.config/ghostwriter/soul.md) owns shared writing defaults
and routes drafting by audience and purpose, not app.
Dotbot links these four files individually into `~/.config/ghostwriter/`; the directory stays real.

| Source | Scope |
| --- | --- |
| [soul.md](/home/.config/ghostwriter/soul.md) | Shared style defaults and profile selection |
| [professional.md](/home/.config/ghostwriter/professional.md) | Work communication outside DMs and social content; client-facing documents |
| [personal.md](/home/.config/ghostwriter/personal.md) | Every DM, including work-related messages, plus personal correspondence |
| [social-media.md](/home/.config/ghostwriter/social-media.md) | Social content outside DMs: bios, stories, reels, posts, captions, comments, and replies |

## Choose the profile

Follow the audience-based routing in `soul.md`, rather than choosing a profile by app.
Every DM uses `personal.md`, including Slack work messages.
Social posts use `social-media.md`, including LinkedIn posts.
This routing takes precedence over Ghostwriter's surface-based filenames.
These files contain generic defaults, not learned voices for Waldo or Lluvia.
Personal examples and measured habits are excluded; the current writer's stated preferences
guide individual voice.
No person-specific learned profile is configured by these files.

## Protect local writing data

Private samples, evaluations, backups, and other unlisted profiles remain local.
Dotbot cleans broken Ghostwriter links pointing into this checkout.
Unrelated local files are not deleted.
Edit repository sources; changes through installed links also change dotfiles.
Keep individual samples and learned preferences outside these shared defaults.
These profiles are publishable configuration, not private storage.
`GHOSTWRITER_HOME` overrides the default directory, bypassing these links unless it names the same
location.

Read [Sync the workstation](/docs/tooling.md#sync-the-workstation) before applying links on an
existing workstation.
