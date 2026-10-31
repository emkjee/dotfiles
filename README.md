## Zsh Functions

A few small zsh functions I use all the time. They're short on purpose, so they're quick to use and easy to read.

| Function | What it does |
| --- | --- |
| [`seek`](#seek) | Fuzzy-find files and open them in Helix |
| [`crun`](#crun) | Compile and run a C file in one step |
| [`mkcd`](#mkcd) | Create a directory and move into it |
| [`help`](#help) | Open a man page in Helix |
| [`exst`](#exst) | Check whether a command exists |
| [`avir`](#avir) | Activate the Python venv in the current directory |
| [`dvir`](#dvir) | Deactivate the active Python venv |
| [`femp`](#femp) | Find empty directories |
| [`demp`](#demp) | Trash empty directories |
| [`pset`](#pset) | Switch the Starship prompt preset |

---

### Setup

**Where they live**

Every function gets its own file in `functions/`, named after the function:

```
dotfiles/
└── functions/
    ├── seek.zsh
    ├── crun.zsh
    ├── mkcd.zsh
    ├── help.zsh
    ├── exst.zsh
    ├── avir.zsh
    ├── dvir.zsh
    ├── femp.zsh
    ├── demp.zsh
    └── pset.zsh
```

**Include them**

Put this in your `~/.zshrc` and it'll load every `.zsh` file in that folder:

```zsh
for f in ~/dotfiles/functions/*.zsh; do
  source "$f"
done
```

Change the path if your dotfiles are somewhere else. If you only want a few of them, source those directly:

```zsh
source ~/dotfiles/functions/seek.zsh
```

**Activate them**

Open a new terminal, or reload the config in the one you're in:

```zsh
source ~/.zshrc
```

After that they work like any other command. If you're not sure one loaded, run `type seek`.

**Add a new one**

Just drop a `<name>.zsh` file into `functions/` and reload the shell. The loop picks it up, so there's nothing to change in `~/.zshrc`.

---

### Functions

#### `seek`

Fuzzy-find files and open them in Helix. Source: [`functions/seek.zsh`](functions/seek.zsh)

```zsh
seek            # browse all files, pick one or more
seek config     # start with "config" already in the search box
```

- Opens an fzf picker with a preview, syntax-highlighted if you have bat.
- Tab marks several files, Enter opens them all in Helix.
- If only one file matches, it opens right away.
- If nothing matches, or you hit Esc, nothing happens.

**Requires:** [fzf](https://github.com/junegunn/fzf), [Helix](https://helix-editor.com) (`hx`), and optionally [bat](https://github.com/sharkdp/bat). Without bat the preview falls back to `cat`.

> **Tip:** the list of files comes from fzf's default finder. If you want `.gitignore` respected, set `FZF_DEFAULT_COMMAND` to something like `fd --type f` or `rg --files`.

---

#### `crun`

Compile and run a C file in one step. Source: [`functions/crun.zsh`](functions/crun.zsh)

```zsh
crun hello.c    # compiles to ./hello and runs it
```

- Compiles with `clang -Wall`.
- The binary is named after the source file (minus the extension) and stays in the same directory.
- It only runs if the compile worked.

**Requires:** [clang](https://clang.llvm.org)

> **Limitations:** it's deliberately minimal. One file, no extra flags, no program arguments. If you need more than that (linking libraries, optimization, C++, a different output name), just run `clang` yourself.

---

#### `mkcd`

Create a directory and move into it. Source: [`functions/mkcd.zsh`](functions/mkcd.zsh)

```zsh
mkcd projects/new-app     # makes the directory (and any parents), then cd's into it
```

- Uses `mkdir -p`, so missing parent directories get created and an existing directory isn't an error.
- Only does the `cd` if the directory was created.
- Handles names with spaces fine.

> **Note:** if you pass more than one directory (`mkcd a b c`), they all get created and you end up in the last one.

---

#### `help`

Open a man page in Helix instead of the pager. Source: [`functions/help.zsh`](functions/help.zsh)

```zsh
help printf       # man page for printf, in a Helix buffer
help 3 printf     # same as man, so sections work too
```

- Renders the page to plain text in a temp file, so you can search, jump around and yank text with Helix.
- If the page doesn't exist, you just get man's usual error and Helix never starts.
- The temp file is deleted when you quit, or if you hit Ctrl-C.
- Running `help` with no arguments prints a usage line.

**Requires:** [Helix](https://helix-editor.com) (`hx`), and `man` and `col`, which are on macOS and most Linux systems already.

> **Note:** the section number goes before the page name, same as `man`. Also, the page is wrapped to your terminal width at the moment you run it, so it won't reflow if you resize the window later.

---

#### `exst`

Check whether a command exists, and where it comes from. Source: [`functions/exst.zsh`](functions/exst.zsh)

```zsh
exst git      # Command 'git' is available, followed by every match
exst nope     # Command 'nope' is NOT available
```

- Uses `type -a`, so it finds aliases, functions, builtins and executables, and lists every match, not just the first one on your `PATH`.
- Exits with `0` if the command exists and `1` if it doesn't, so you can use it in scripts: `exst fzf && seek`.
- Running it with no argument prints a message and exits with `2`.

> **Note:** it only looks at the first argument.

---

#### `avir`

Activate the Python virtual environment in the current directory. Source: [`functions/avir.zsh`](functions/avir.zsh)

```zsh
avir      # activates ./.venv
```

- Looks for `.venv/bin/activate` in the current directory and sources it.
- If there's no `.venv` there, it prints an error and returns `1`.

> **Note:** it only looks in the current directory, so run it from the project root.

---

#### `dvir`

Deactivate the active Python virtual environment. Source: [`functions/dvir.zsh`](functions/dvir.zsh)

```zsh
dvir      # deactivates whatever venv is active
```

- Only calls `deactivate` if a venv is active, so you don't get a "command not found" when none is.
- If nothing is active, it just prints "No venv active."

---

#### `femp`

Find empty directories below the current one. Source: [`functions/femp.zsh`](functions/femp.zsh)

```zsh
femp                # list empty directories here
femp some/path      # look somewhere else
```

- Only lists, never deletes. Run it before `demp` to see what's about to go.
- Extra arguments go straight to `fd`.
- Hidden and gitignored directories are skipped, same as `fd` does by default.

**Requires:** [fd](https://github.com/sharkdp/fd)

> **Note:** it only shows directories that are empty right now. If a directory only holds empty ones, it shows up after those are gone.

---

#### `demp`

Trash the empty directories below the current one. Source: [`functions/demp.zsh`](functions/demp.zsh)

```zsh
femp      # preview what's empty
demp      # trash it
```

- Everything goes to the Trash in a single call, so a mistake is recoverable.
- Hidden and gitignored directories are skipped, so `.git` is safe.
- It does one sweep, nothing more.

**Requires:** [fd](https://github.com/sharkdp/fd), [trash](https://github.com/ali-rantakari/trash)

> **Note:** one run clears one layer. If a directory only held empty ones, it shows up on the next run, so repeat until `femp` prints nothing.

> **Careful:** it works on everything below where you run it, so keep an eye on where you are. Run `cds` first, because a `.DS_Store` makes a directory count as non-empty.

---

#### `pset`

Pick a Starship prompt preset and link it as the active config. Source: [`functions/pset.zsh`](functions/pset.zsh)

```zsh
pset      # choose a preset from the list, with a preview
```

- Lists the `.toml` files in `$DOTDIR/starship`, with a syntax-highlighted preview.
- Symlinks `~/.config/starship.toml` straight to the one you pick, so there's no extra hop.
- If you hit Esc, nothing changes.
- Starship picks up the change on the next prompt, so no reload is needed.

**Requires:** [fzf](https://github.com/junegunn/fzf), [fd](https://github.com/sharkdp/fd), [bat](https://github.com/sharkdp/bat) for the preview, and `$DOTDIR` set to your dotfiles directory.

> **Note:** it refuses to run if `~/.config/starship.toml` is a real file instead of a symlink, so it can't overwrite a config you wrote by hand. Move that file into `$DOTDIR/starship` first. Every `.toml` in that folder shows up as a preset, so keep other `.toml` files out of it.

> **Note:** if `STARSHIP_CONFIG` is set to some other file, Starship reads that one and `pset` will appear to do nothing. Check with `echo $STARSHIP_CONFIG`; it should be empty or point at `~/.config/starship.toml`.

---

## Aliases

The short ones I type all day. They live in one block in my `~/.zshrc`, under a `## setup_aliases` header, so they're easy to find and easy to trim.

### Shell

| Alias | What it does |
| --- | --- |
| `rm` | `rm -I`, asks once before deleting more than three files or a directory |
| `rz` | Reload the shell with `exec zsh` |
| `trail` | Print `$PATH` one entry per line |

### Navigation

`auto_cd` is on, so typing a directory name (or just `..`) takes you there. The dots are global aliases, so they work anywhere in a command, not only with `cd`:

| Alias | Expands to |
| --- | --- |
| `...` | `../..` |
| `....` | `../../..` |
| `.....` | `../../../..` |

```zsh
cd ...            # up two levels
ls ....           # list three levels up
```

> **Note:** a standalone `...` always expands, so `echo ...` prints `../..`. Ranges like `git diff main...feature` are fine, since the dots are part of a longer word.

### Editing

Everything goes through `e`, so switching editors later is a one-line change.

| Alias | Opens |
| --- | --- |
| `e` | Helix (`hx`) |
| `ek` | `~/.config/kitty` |
| `eh` | `~/.config/helix` |
| `ez` | `~/.zshrc` |
| `es` | `~/.config/starship.toml` |

### Listing

| Alias | What it does |
| --- | --- |
| `ls` | `lsd` with git status |
| `ll` | Long list, hidden files included, newest at the bottom |
| `lt` | Tree view |

### Cleanup

These use `fd` and `trash`, so nothing is deleted for good. For empty directories, see `femp` and `demp` above.

| Alias | What it does |
| --- | --- |
| `cds` | Trash every `.DS_Store` below the current directory |
| `fbl` | Find broken symlinks |

> **Careful:** `cds` walks everything below where you run it, so don't run it from `~` or `/`.

**Requires:** [lsd](https://github.com/lsd-rs/lsd), [fd](https://github.com/sharkdp/fd), [trash](https://github.com/ali-rantakari/trash), [Helix](https://helix-editor.com)

### Homebrew

| Alias | What it does |
| --- | --- |
| `brc` | Clean up, pruning the whole cache |
| `brl` | List installed packages |
| `bro` | Show outdated packages |
| `bru` | Update, then upgrade everything |
