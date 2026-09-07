# Slack

Not a file format — a comma-separated hex string you paste into the app.

- `grafana-dark.txt`, `grafana-light.txt` — the 8-value string
- `themes.json` — both, plus the 10-value variant and per-slot labels

## Install

**Preferences → Themes**, scroll past the bundled themes to the custom theme
field, and paste the contents of the `.txt`. It applies immediately and syncs
to your other desktop and mobile clients on the same account.

Pasting the string into a Slack message renders an inline "switch to this
theme" card, which is a convenient way to share it.

## Slot order

| # | slot | controls |
|---|---|---|
| 1 | Column BG | sidebar background |
| 2 | Menu BG Hover | hovering the workspace-name menu |
| 3 | Active Item | selected channel or DM row background |
| 4 | Active Item Text | text on that row |
| 5 | Hover Item | hovering a channel row |
| 6 | Text Color | default sidebar text |
| 7 | Active Presence | the online presence dot |
| 8 | Mention Badge | unread mention count badge |

Positions 1–8 are consistently documented. A **ten**-value string adding
`Top Nav BG` and `Top Nav Text` also parses in current clients, and is in
`themes.json` as `value_with_top_nav` — but it is poorly documented, so the
`.txt` ships the safe eight.

## Notes

- A Slack theme is **sidebar only**. The message pane, code blocks and
  composer are not themeable, so this cannot make Slack match your editor —
  only its sidebar.
- Uppercase 6-digit hex, comma-separated, no spaces. No alpha, no 3-digit
  shorthand.
- It is a per-user setting. Workspace admins can set a default for new
  members but cannot force it on existing ones.
- Mobile has no custom-theme field, but a theme set on desktop syncs down.
