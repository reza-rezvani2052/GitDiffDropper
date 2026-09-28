# GitDiffDropper

A small Windows desktop utility for quickly exporting the `git diff` of one or more files from a Git repository to text files on the Desktop.

GitDiffDropper is designed for a simple workflow: **drag files from a Git repository onto the application, and get their `git diff` output as text files immediately.**

> Application version: `1.0.0`

## Features

- Drag and drop multiple files at once.
- Automatically finds the Git repository containing each dropped file.
- Runs `git diff` for each file.
- Saves the result to the Windows Desktop as:
  - `diff-<filename>.txt`
- Works with files located anywhere inside the repository.
- Shows a summary of successful files and errors in the application window.
- Remembers the main window geometry and state between runs.
- Can be packaged as a standalone Windows executable with PyInstaller.

## Requirements

- Windows
- Git installed and available in `PATH`
- Python
- PySide6 `6.11.2` (installed through `requirements.txt`)

## How It Works

For every dropped file, GitDiffDropper:

1. Finds the nearest Git repository containing the file.
2. Converts the file path to a path relative to the repository root.
3. Executes:

```text
git -C <repository> diff -- <relative-file-path>
```

4. Writes the command output to:

```text
%USERPROFILE%\Desktop\diff-<filename>.txt
```

## Usage

### 1. Create a virtual environment

```powershell
python -m venv .venv
.venv\Scripts\activate
```

### 2. Install dependencies

```powershell
pip install -r requirements.txt
```

### 3. Run the application

```powershell
python main.py
```

You can also use the included batch file:

```text
run-normal.bat
```

### 4. Generate a diff

Drag one or more files from a Git repository and drop them onto the application window.

The generated files will appear on the Windows Desktop, for example:

```text
diff-main.py.txt
diff-mainwindow.py.txt
diff-dialogregister.py.txt
```

## Important Git Behavior

GitDiffDropper intentionally uses `git diff`, so it follows Git's normal diff semantics.

### Included

- Modifications that are currently in the working tree and are **not staged**.

### Not included

- Staged changes (`git add` changes).
- Untracked files that have not been added to Git.
- A file that has no diff produces an empty output file.

For example, if a file is staged, use the appropriate Git command manually when you need the staged diff, such as `git diff --cached`.

## Output Naming Limitation

The output filename is based only on the source file name:

```text
diff-<filename>.txt
```

Therefore, two different repository paths with the same filename can produce the same output filename. In that case, the later operation may overwrite the earlier output.

For example:

```text
repo1/src/main.py
repo2/tools/main.py
```

Both would produce:

```text
diff-main.py.txt
```

A future improvement could preserve part of the relative path or generate unique output names.

## Project Structure

```text
GitDiffDropper/
├── build_tools/
│   └── build_exe.py          # PyInstaller build script
├── RC/
│   ├── img/                  # Application images
│   ├── app-icon.ico
│   ├── app-icon.png
│   └── rc.qrc                # Qt resource definition
├── UI/
│   ├── mainwindow.ui
│   ├── dialogpopup.ui
│   └── dialogdraggable.ui
├── build_ui_qrc.py            # Generates Python files from .ui and .qrc
├── definitions.py             # Application metadata and runtime constants
├── dialogpopup.py             # Popup widget
├── main.py                    # Application entry point
├── mainwindow.py              # Main window and Git diff workflow
├── utility.py                 # Shared utilities
├── requirements.txt
├── run-normal.bat             # Run helper for the local virtual environment
└── TODO.txt
```

Generated files such as `ui_*.py` and `rc_rc.py` are intentionally excluded from Git. When the application is run directly from source, `main.py` automatically regenerates the required UI and Qt resource Python files.

## Building a Windows Executable

The project includes a PyInstaller build script:

```powershell
.venv\Scripts\activate
python build_tools\build_exe.py
```

The current build configuration uses PyInstaller's **onedir** mode.

The generated application is placed under:

```text
dist\GitDiffDropper\
```

with the main executable:

```text
dist\GitDiffDropper\GitDiffDropper.exe
```

## Technology Stack

- Python
- PySide6 / Qt
- Git command-line client
- PyInstaller

## Development Notes

The application is intentionally small and focused. The main Git operation is implemented in `mainwindow.py`, while UI/resource generation is handled by `build_ui_qrc.py`.

When launching the frozen executable, PyInstaller's `sys.frozen` state prevents development-time UI/resource regeneration.

## Possible Future Improvements

- Add an option for staged diffs using `git diff --cached`.
- Add support for untracked files through an explicit patch/diff mode.
- Prevent output collisions for files with identical names.
- Allow the output directory to be configured instead of always using the Desktop.
- Add an option to copy the generated diff to the clipboard.
- Add GitHub Actions for automated build/release generation.
- Add automated tests for repository detection, path handling, and Git command failures.

## License

This project is free and open source.
You are free to use, modify, copy, and distribute this software.