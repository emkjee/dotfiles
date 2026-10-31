## ZSH Functions

A few small zsh functions I use all the time. They're short on purpose, so they're quick to use and easy to read.

| Function | What it does |
| --- | --- |
| [`seek`](#seek) | Fuzzy-find files and open them in Helix |
| [`crun`](#crun) | Compile and run a C file in one step |
| [`mkcd`](#mkcd) | Create a directory and move into it |
| [`help`](#help) | Open a man page in Helix |
| [`exst`](#exst) | Check whether a command exists |

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
    └── exst.zsh
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