get-content ../.env | foreach {
    $name, $value = $_.split('=')
    set-content env:\$name $value
}

uvicorn main:app --host 0.0.0.0 --port 8090 --reload