Dim objShell
Dim PythonExe
Dim PythonScript

Set objShell = CreateObject("Wscript.shell")

PythonExe = "python "
PythonScript = """C:\Users\rlau0\Documents\Parselmouth\systools\window_logger\tracker4timesheet.py"""
objShell.Run "cmd /k " & PythonExe & PythonScript