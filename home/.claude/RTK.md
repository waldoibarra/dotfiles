# RTK - Rust Token Killer

**Usage**: Token-optimized CLI proxy (60-90% savings on dev operations)

## Meta Commands (always use rtk directly)

```bash
rtk gain              # Show token savings analytics
rtk gain --history    # Show command usage history with savings
rtk gain --daily      # day-by-day breakdown
rtk gain --weekly     # weekly aggregation
rtk discover          # Analyze Claude Code history for missed opportunities
rtk proxy <cmd>       # Execute raw command without filtering (for debugging)
```

## Automatic Rewriting

All other commands are automatically rewritten by the active coding agent integration:
Claude Code uses a hook; OpenCode uses a plugin.
Example: `git status` → `rtk git status` (transparent, 0 tokens overhead)
