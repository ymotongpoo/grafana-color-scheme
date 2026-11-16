# Slack

Not a file format — a comma-separated hex string you paste into the app.

- `grafana-{dark,light}.txt`, `grafana-{dark,light}-dim.txt` — the 8-value string
- `themes.json` — all four, plus the 10-value variant and per-slot labels

## Install

**Preferences → Themes**, scroll past the bundled themes to the custom theme
field, and paste the contents of the `.txt`. It applies immediately and syncs
to your other desktop and mobile clients on the same account.

Pasting the string into a Slack message renders an inline "switch to this
theme" card, which is a convenient way to share it.

## Slot order

| # | slot | current Slack field | controls |
|---|---|---|---|
| 1 | Column BG | System navigation | workspace rail, top bar, base of the sidebar |
| 2 | Menu BG Hover | *(ignored)* | |
| 3 | Active Item | Selected items | selected channel or DM row |
| 4 | Active Item Text | *(ignored)* | |
| 5 | Hover Item | *(ignored)* | |
| 6 | Text Color | *(ignored)* | |
| 7 | Active Presence | Presence indication | the online presence dot |
| 8 | Mention Badge | Notifications | unread mention count badge |

Current clients have a four-color custom theme and keep only positions 1,
3, 7 and 8 of an imported string. **Slack chooses every text color itself**,
so `Text Color` no longer has any effect. The other positions are still
written so older clients get a complete theme.

A **ten**-value string adding `Top Nav BG` and `Top Nav Text` also parses,
and is in `themes.json` as `value_with_top_nav`, but the `.txt` ships the
safe eight.

## The frame color

Every theme puts the brand orange (`#FF671D`) in position 1. Slack keeps
its hue but chooses the lightness itself for the current color mode, so the
frame never shows the exact brand orange:

| color mode | frame (measured) | sidebar (measured) |
|---|---|---|
| light | `#FF8669`, a soft orange | `#FFF4EE` |
| dark | `#561B00`, a deep burnt orange | `#2C160D` |

A darker input does not change this. `#FF3B00` was tried in light mode and
the frame came out at the same lightness. The selected row (position 3) is
rendered exactly as given.

## Light themes: turn off "Darker sidebars"

After importing `grafana-light.txt` or `grafana-light-dim.txt`, open
**Preferences → Themes → Custom theme** and **untick "Darker sidebars"**.
With it ticked, Slack draws white sidebar text over a light sidebar and the
channel list becomes unreadable.

## Notes

- A Slack theme is **sidebar only**. The message pane, code blocks and
  composer are not themeable, so this cannot make Slack match your editor —
  only its sidebar.
- Uppercase 6-digit hex, comma-separated, no spaces. No alpha, no 3-digit
  shorthand.
- It is a per-user setting. Workspace admins can set a default for new
  members but cannot force it on existing ones.
- Mobile has no custom-theme field, but a theme set on desktop syncs down.
