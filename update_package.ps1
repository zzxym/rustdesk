Get-ChildItem -Path "d:/code/rustdesk/flutter/android/app/src/main/kotlin/com/carriez/xldesk" -Filter "*.kt" | ForEach-Object {
    $file = $_.FullName
    (Get-Content $file) -replace 'package com\.carriez\.flutter_hbb', 'package com.carriez.xldesk' | Set-Content $file
    Write-Host "Updated $file"
}