#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Via Size Unifier Plugin for KiCad 10
------------------------------------

This Action Plugin modifies the Overall Diameter and Drill Diameter of all vias 
on the current board simultaneously. It provides a wxPython dialog for users to 
input the desired dimensions in millimeters.

Installation Instructions:
To install this plugin, save this file (and any accompanying files) into the 
KiCad plugins directory based on your operating system:

- Windows: %USERPROFILE%\\Documents\\KiCad\\10.0\\scripting\\plugins
- Linux:   ~/.local/share/kicad/10.0/scripting/plugins
- macOS:   ~/Documents/KiCad/10.0/scripting/plugins

After saving, restart KiCad or open the PCB Editor and click 'Tools > External Plugins > Refresh'.
The plugin will then appear in the 'Tools > External Plugins' menu.
"""

import os
import pcbnew
import wx

class ViaSizeDialog(wx.Dialog):
    def __init__(self, parent):
        # We use a simple wx.Dialog for the UI
        super(ViaSizeDialog, self).__init__(parent, title="Via Size Unifier", size=(350, 150))
        
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        # Diameter Input
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        st1 = wx.StaticText(panel, label="New Via Diameter (mm):")
        hbox1.Add(st1, flag=wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, border=8)
        self.tc_diameter = wx.TextCtrl(panel, value="0.8")
        hbox1.Add(self.tc_diameter, proportion=1)
        vbox.Add(hbox1, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)
        
        # Drill Input
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        st2 = wx.StaticText(panel, label="New Drill Diameter (mm):")
        hbox2.Add(st2, flag=wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, border=8)
        self.tc_drill = wx.TextCtrl(panel, value="0.4")
        hbox2.Add(self.tc_drill, proportion=1)
        vbox.Add(hbox2, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)
        
        # OK and Cancel Buttons
        btn_box = wx.BoxSizer(wx.HORIZONTAL)
        btn_ok = wx.Button(panel, wx.ID_OK, label="Apply")
        btn_cancel = wx.Button(panel, wx.ID_CANCEL, label="Cancel")
        btn_box.Add(btn_ok)
        btn_box.Add(btn_cancel, flag=wx.LEFT, border=5)
        vbox.Add(btn_box, flag=wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border=10)
        
        panel.SetSizer(vbox)

class ViaSizeUnifierPlugin(pcbnew.ActionPlugin):
    def defaults(self):
        self.name = "Via Size Unifier"
        self.category = "Modify PCB"
        self.description = "Unifies the size and drill diameter of all vias on the board."
        self.show_toolbar_button = True
        self.icon_file_name = os.path.join(os.path.dirname(__file__), 'icon.png')

    def Run(self):
        board = pcbnew.GetBoard()
        if not board:
            return

        # Attempt to find the PCB Editor main window to use as the parent for our dialog.
        # This keeps the dialog on top of the KiCad window.
        pcb_frame = None
        for win in wx.GetTopLevelWindows():
            if win.GetTitle().lower().startswith('pcb editor') or win.GetTitle().lower().startswith('pcbnew'):
                pcb_frame = win
                break
        
        dlg = ViaSizeDialog(pcb_frame)
        res = dlg.ShowModal()
        
        if res == wx.ID_OK:
            try:
                # Get values from text controls
                new_diameter_mm = float(dlg.tc_diameter.GetValue())
                new_drill_mm = float(dlg.tc_drill.GetValue())
            except ValueError:
                wx.MessageBox("Invalid input. Please enter valid numeric values.", 
                              "Error", wx.OK | wx.ICON_ERROR)
                dlg.Destroy()
                return

            # Convert millimeters to KiCad's internal units
            new_diameter = int(pcbnew.FromMM(new_diameter_mm))
            new_drill = int(pcbnew.FromMM(new_drill_mm))
            
            # Iterate through all routing objects to find vias
            for track in board.GetTracks():
                # We check the class name or duck typing to support multiple KiCad versions
                if type(track).__name__ in ['PCB_VIA', 'VIA'] or hasattr(track, 'SetDrill'):
                    # SetWidth changes the Overall Diameter of the via
                    track.SetWidth(new_diameter)
                    # SetDrill changes the Drill hole diameter of the via
                    track.SetDrill(new_drill)
            
            # Refresh the PCB editor canvas to show changes immediately
            pcbnew.Refresh()
            
        dlg.Destroy()

# Register the plugin so it appears in the KiCad menu
ViaSizeUnifierPlugin().register()
