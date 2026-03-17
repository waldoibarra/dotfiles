local wezterm = require 'wezterm'
local mux = wezterm.mux
local config = {}

-- ┌──────────────────────────────────────────────────────────────────────────────┐
-- │                                   FONT                                       │
-- └──────────────────────────────────────────────────────────────────────────────┘

-- config.font = wezterm.font 'IosevkaTerm NF'
-- config.font_size = 14.0

-- ┌──────────────────────────────────────────────────────────────────────────────┐
-- │                                  WINDOW                                      │
-- └──────────────────────────────────────────────────────────────────────────────┘

config.window_background_opacity = 0.7
config.macos_window_background_blur = 20

config.window_padding = {
    bottom = 111
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
-- config.cursor_blink_rate = 500
-- config.cursor_blink_ease_in = "Constant"
-- config.cursor_blink_ease_out = "Constant"

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
