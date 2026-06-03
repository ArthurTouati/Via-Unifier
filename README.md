# KiCad 10 Via Size Unifier Plugin

This KiCad Action Plugin modifies the Overall Diameter and Drill Diameter of all vias on the current board simultaneously. It provides a simple wxPython dialog to input your desired dimensions in millimeters.

## Features
- Updates all vias (`pcbnew.VIA` items) across the PCB in a single action.
- Simple GUI to input custom via size and drill hole diameters.
- Configured defaults: 0.8 mm via diameter / 0.4 mm drill diameter.
- Seamless unit conversion to KiCad's internal units.
- Refreshes the PCB editor canvas automatically so changes appear immediately.

## Installation

1. Download or copy the entire `Via size Unifier` directory.
2. Place the directory into your KiCad plugins folder based on your operating system:
   - **Windows:** `%USERPROFILE%\Documents\KiCad\10.0\scripting\plugins`
   - **Linux:** `~/.local/share/kicad/10.0/scripting/plugins`
   - **macOS:** `~/Documents/KiCad/10.0/scripting/plugins`
3. Restart KiCad, or go to the PCB Editor and click `Tools > External Plugins > Refresh`.

The plugin will now appear in the `Tools > External Plugins` menu, and also as a button on your top Action Plugins toolbar.

## Usage
1. Open a board in the KiCad PCB Editor.
2. Click the "Via Size Unifier" icon in the toolbar, or run it from `Tools > External Plugins`.
3. Enter your desired Via Diameter and Drill Diameter (in mm) in the dialog.
4. Click Apply. All vias on the board will be resized.

## Compatibility
This script is built for the KiCad 10 Python API (`pcbnew`).
