local wezterm = require 'wezterm'
local mux = wezterm.mux
local config = {}

-- ┌──────────────────────────────────────────────────────────────────────────────┐
-- │                                 SHORTCUTS                                    │
-- └──────────────────────────────────────────────────────────────────────────────┘

-- Defaults:
-- Split pane vertically (top/bottom): C-M-S-"
-- Split pane horizontally (left/right): C-M-S-%
-- Switch pane: C-S-<up/right/down/left>
-- Maximize a pane: C-S-z

-- ┌──────────────────────────────────────────────────────────────────────────────┐
-- │                                   FONT                                       │
-- └──────────────────────────────────────────────────────────────────────────────┘

config.font_size = 12.5

-- ┌──────────────────────────────────────────────────────────────────────────────┐
-- │                                  WINDOW                                      │
-- └──────────────────────────────────────────────────────────────────────────────┘

-- config.window_background_opacity = 0.7
-- config.macos_window_background_blur = 20

config.window_padding = {
    top = 0,
    right = 0,
    bottom = 0,
    left = 0
}

config.enable_scroll_bar = false
config.hide_tab_bar_if_only_one_tab = true
config.window_decorations = 'RESIZE | MACOS_FORCE_SQUARE_CORNERS'

wezterm.on('gui-startup', function(cmd)
  local tab, pane, window = mux.spawn_window(cmd or {})

  window:gui_window():maximize()
end)

-- ┌──────────────────────────────────────────────────────────────────────────────┐
-- │                                  CURSOR                                      │
-- └──────────────────────────────────────────────────────────────────────────────┘

config.default_cursor_style = "BlinkingBar"

-- ┌──────────────────────────────────────────────────────────────────────────────┐
-- │                            NEOVIM OPTIMIZATIONS                              │
-- └──────────────────────────────────────────────────────────────────────────────┘

-- Terminal & Colors
-- https://wezterm.org/config/lua/config/term.html?h=term
config.term = "wezterm"
-- config.enable_csi_u_key_encoding = true

-- Undercurl support (LSP diagnostics, spelling)
-- config.underline_thickness = 2
-- config.underline_position = -2

-- Scrollback
config.scrollback_lines = 11111

-- Performance
config.max_fps = 240

-- Input handling
-- config.use_dead_keys = false
-- config.send_composed_key_when_left_alt_is_pressed = false
-- config.send_composed_key_when_right_alt_is_pressed = false

return config
