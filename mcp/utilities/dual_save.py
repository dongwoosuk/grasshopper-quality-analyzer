"""Grasshopper Dual Save Utility
Saves the current GH document as both .gh and .ghx formats

Inputs:
    x: bool  # Press to trigger dual save
    prompt: bool  # True = always ask for location, False = use current file path

Outputs:
    a: string  # Save status message
"""

import os
import sys
import clr
import Grasshopper as gh
from Grasshopper.Kernel import GH_DocumentIO

# File dialog
try:
    import System
    clr.AddReference("System.Windows.Forms")
    from System.Windows.Forms import SaveFileDialog, DialogResult
except:
    SaveFileDialog = None

# Get current Grasshopper document
doc = ghenv.Component.OnPingDocument()

if not x: 
    ghenv.Component.Message = "Ready: press to save"
    a = "idle"
else:
    base_no_ext = None
    
    # If prompt is True or no file path exists, show dialog
    if prompt or not doc.FilePath or not os.path.isfile(doc.FilePath):
        if SaveFileDialog is None:
            raise Exception("No UI available for file dialog.")
        
        sfd = SaveFileDialog()
        sfd.Title = "Choose save location (will save as .gh and .ghx)"
        sfd.Filter = "Grasshopper File (*.gh)|*.gh|All Files (*.*)|*.*"
        sfd.FileName = "untitled" if not doc.FilePath else os.path.basename(doc.FilePath)
        sfd.AddExtension = True
        
        if sfd.ShowDialog() == DialogResult.OK:
            base_no_ext = os.path.splitext(sfd.FileName)[0]
        else:
            a = "Cancelled by user"
            ghenv.Component.Message = "Cancelled"
    else:
        # Use current file path
        base_no_ext = os.path.splitext(doc.FilePath)[0]
    
    if base_no_ext:
        # Define both file paths
        gh_path  = base_no_ext + ".gh"
        ghx_path = base_no_ext + ".ghx"
        
        # Save to both formats
        try:
            # Method 1: Try with GH_DocumentIO
            io = GH_DocumentIO()
            io.Document = doc
            
            ok1 = io.SaveQuiet(gh_path)
            ok2 = io.SaveQuiet(ghx_path)
            
        except:
            # Method 2: Fallback - use GH_Archive
            try:
                archive = gh.Kernel.GH_Archive()
                archive.AppendObject(doc, "Definition")
                ok1 = archive.WriteToFile(gh_path, True, False)
                ok2 = archive.WriteToFile(ghx_path, True, True)
            except Exception as e:
                a = "Error: " + str(e)
                ghenv.Component.Message = "Error"
                ok1 = False
                ok2 = False
        
        # Build status message
        msg = []
        if ok1:
            msg.append("✔ Saved .gh: " + os.path.basename(gh_path))
        else:
            msg.append("✖ Failed .gh: " + os.path.basename(gh_path))
            
        if ok2:
            msg.append("✔ Saved .ghx: " + os.path.basename(ghx_path))
        else:
            msg.append("✖ Failed .ghx: " + os.path.basename(ghx_path))
        
        msg.append("\nLocation: " + os.path.dirname(gh_path))
        
        a = "\n".join(msg)
        ghenv.Component.Message = "Dual-Saved!" if (ok1 and ok2) else "Check output"
