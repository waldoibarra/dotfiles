# Dotfiles

My personal OS configuration files, currently using MacOS.

## Setup

To install your dotfiles on a new machine or after updates:

```bash
git clone git@github.com:waldoibarra/dotfiles.git ~/.dotfiles
cd ~/.dotfiles
./install
```

The [Dotbot](https://github.com/anishathalye/dotbot)'s script is idempotent, can be ran many times.

## Customization

Edit the [install.conf.yaml](install.conf.yaml) file and re-run the [install](install) script.
