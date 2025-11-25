# Script para compilar todos los programas C++ generados por FunLang
# Uso: .\compile_all.ps1

$GCC_PATH = "C:\Program Files\CodeBlocks\MinGW\bin\g++.exe"
$OUTPUT_DIR = Join-Path $PSScriptRoot "output"
$CPP_FLAGS = @("-std=c++14", "-O2", "-static")

Write-Host "======================================================================"
Write-Host "  Compilador de programas FunLang -> C++ Ejecutable"
Write-Host "======================================================================"
Write-Host ""

# Verificar que existe g++
if (-not (Test-Path $GCC_PATH)) {
    Write-Host "ERROR: No se encontro g++ en: $GCC_PATH"
    exit 1
}

# Obtener todos los archivos .cpp en output
$cppFiles = Get-ChildItem -Path $OUTPUT_DIR -Filter "*.cpp" -ErrorAction SilentlyContinue

if ($cppFiles.Count -eq 0) {
    Write-Host "No se encontraron archivos .cpp en $OUTPUT_DIR"
    exit 0
}

$exitosos = 0
$fallidos = 0

foreach ($file in $cppFiles) {
    $baseName = $file.BaseName
    $cppPath = $file.FullName
    $exePath = Join-Path $OUTPUT_DIR ($baseName + ".exe")
    
    Write-Host "[$baseName.cpp] " -NoNewline
    
    # Compilar
    $errorFile = Join-Path $env:TEMP "gcc_error.txt"
    $args = $CPP_FLAGS + @($cppPath, "-o", $exePath)
    $proceso = Start-Process -FilePath $GCC_PATH -ArgumentList $args -Wait -PassThru -NoNewWindow -RedirectStandardError $errorFile
    
    if ($proceso.ExitCode -eq 0) {
        Write-Host "OK -> $baseName.exe"
        $exitosos++
    } else {
        Write-Host "ERROR"
        $errorMsg = Get-Content $errorFile -Raw -ErrorAction SilentlyContinue
        if ($errorMsg) {
            Write-Host $errorMsg
        }
        $fallidos++
    }
}

Write-Host ""
Write-Host "======================================================================"
Write-Host "  Resumen: $exitosos exitosos, $fallidos fallidos"
Write-Host "======================================================================"

# Listar ejecutables generados
if ($exitosos -gt 0) {
    Write-Host ""
    Write-Host "Ejecutables generados:"
    $exeFiles = Get-ChildItem -Path $OUTPUT_DIR -Filter "*.exe"
    foreach ($exe in $exeFiles) {
        $nombre = $exe.Name
        Write-Host "  - $nombre"
    }
}
