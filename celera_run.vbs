Set oShell = CreateObject ("Wscript.Shell") 
Dim strArgs
strArgs = "cmd /c celera.bat"
oShell.Run strArgs, 0, false