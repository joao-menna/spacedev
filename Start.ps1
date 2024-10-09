
param (
    [string]$reload = ""
)

& .\.venv\Scripts\Activate.ps1

Set-Location ./backend

.\Start.ps1 $reload

Set-Location .\..
