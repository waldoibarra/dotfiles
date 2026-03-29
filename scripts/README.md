# Scripts

This directory contains scripts to:

* Restart Brew service with a custom plist ([restart-brew-service-with-custom-plist.sh](restart-brew-service-with-custom-plist.sh))
* Update OpenCode configuration ([update-opencode-config.sh](update-opencode-config.sh))

## OpenCode Configuration

It will update the following:

- [AI Gentle Stack](https://github.com/Gentleman-Programming/gentle-ai)

### Usage

```bash
make update-oc
```

## Development

When modifying the setup scripts, make sure to use ShellCheck to analyze for bugs.

```bash
make check
```
