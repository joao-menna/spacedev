param (
    [string]$reload = ""
)

get-content ../.env | ForEach-Object {
    if ($_.Contains('=')) {
        $name, $value = $_.split('=')
        set-content env:\$name $value
    }
}

if ($reload -eq "") {
    uvicorn main:app --host 0.0.0.0 --port 8090
} else {
    uvicorn main:app --host 0.0.0.0 --port 8090 --reload
}