Write-Host "--- VENV ---"
if (Test-Path -Path .\.venv) {
    Write-Host "Activating Venv"
    & .\.venv\Scripts\Activate.ps1
} else {
    Write-Host "Creating Venv"
    python -m venv .venv
}

Write-Host "--- DEPS ---"

Write-Host "Entering backend folder"
Set-Location .\backend

Write-Host "Installing dependencies"
pip install -r .\requirements.txt

Write-Host "Going to root folder"
Set-Location .\..

Write-Host "--- .ENV ---"
if (Test-Path -Path .\.env) {
    Write-Host "Skipping .env creation"
} else {
    Write-Host "Creating .env"
    Copy-Item .\.env.example .\.env
}

Write-Host "--- FRONT DEPS ---"

Set-Location .\frontend

Write-Host "Changing NVM"
nvm use 20

Write-Host "Installing Yarn"
npm i -g yarn

Write-Host "Installing dependencies"
yarn
