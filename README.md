<p align="center">
	<b>CMD Block Relative Calculator</b>
	<br>
 	<i>A lightweight desktop application for calculating relative coordinates for Minecraft command blocks.</i>
	<br><br><br>
	<img src="https://github.com/user-attachments/assets/c59e5f49-e607-49ba-8326-a2b852473d1f">
</p>

# CMD Block Relative Calculator

A lightweight desktop application for calculating relative coordinates for Minecraft command blocks. Designed to assist with commands like `/setblock`, `/fill`, `/clone` by converting absolute coordinates into relative ones.

Built with [Python](https://www.python.org/) and [Tkinter](https://docs.python.org/3/library/tkinter.html).

# Features

- Calculate relative coordinates between command block and destination
- Smart coordinates extraction using RegEx
- Compute `/setblock` command relative coordinates
- Compute full `/fill` and `/clone` command relative coordinates from two source corners and a destination
- Copy results to clipboard with a single click
- Automatically save logs to preserve previous calculations
- Light & dark theme

# Installation

## Option 1: Download precompiled Windows version

For Windows users, a standalone .exe file is available — no Python installation required.

1. Go to the [Releases page](https://github.com/hXR16F/commandblock-relative-calculator/releases).
2. Download the latest .exe version from the Assets section.
3. Run the file — no setup needed.

> [!NOTE]
> This program was compiled using [Nuitka](https://nuitka.net/) with the following parameters:
> ```bash
> python -m nuitka "commandblock-relative-calculator.py" --windows-icon-from-ico=icon.ico --onefile --enable-plugin=tk-inter --windows-console-mode=disable
> ```

## Option 2: Run from source (cross-platform)

Tested on Python 3.11.

1. Clone the repository:
```bash
git clone https://github.com/hXR16F/commandblock-relative-calculator
```
2. Install dependencies:

```bash
pip install -r requirements.txt
```
3. Launch the app:
```bash
python commandblock-relative-calculator.py
```

# Support
If you support my work or like my projects, [you can donate me some money](https://github.com/hXR16F/donate/blob/master/README.md). Thank you 💙
