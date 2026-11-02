' Start the local FOMO Radar stack with no console window (used by the logon task).
Set fso = CreateObject("Scripting.FileSystemObject")
Set sh = CreateObject("WScript.Shell")
dir = fso.GetParentFolderName(WScript.ScriptFullName)
sh.Run """" & dir & "\start-local.cmd""", 0, False
