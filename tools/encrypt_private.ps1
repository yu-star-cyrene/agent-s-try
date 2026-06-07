param(
    [string]$ManifestPath = ".private-bundle-manifest.json",
    [string]$OutputPath = "",
    [switch]$RemovePlaintext
)

$ErrorActionPreference = "Stop"

function Get-PlainTextSecret {
    if ($env:DACHUANG_PRIVATE_KEY) {
        return $env:DACHUANG_PRIVATE_KEY
    }

    $secure = Read-Host "Enter encryption key" -AsSecureString
    $ptr = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($secure)
    try {
        return [Runtime.InteropServices.Marshal]::PtrToStringBSTR($ptr)
    }
    finally {
        [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($ptr)
    }
}

function Join-Bytes {
    param([byte[][]]$Arrays)

    $length = 0
    foreach ($array in $Arrays) {
        $length += $array.Length
    }

    $result = New-Object byte[] $length
    $offset = 0
    foreach ($array in $Arrays) {
        [Buffer]::BlockCopy($array, 0, $result, $offset, $array.Length)
        $offset += $array.Length
    }
    return $result
}

function Protect-Bytes {
    param(
        [byte[]]$PlainBytes,
        [string]$Passphrase
    )

    $magic = [Text.Encoding]::ASCII.GetBytes("DCBUNDLE1")
    $salt = New-Object byte[] 16
    $iv = New-Object byte[] 16
    $rng = [Security.Cryptography.RandomNumberGenerator]::Create()
    $rng.GetBytes($salt)
    $rng.GetBytes($iv)
    $rng.Dispose()

    $kdf = New-Object Security.Cryptography.Rfc2898DeriveBytes($Passphrase, $salt, 200000)
    $keyMaterial = $kdf.GetBytes(64)
    $kdf.Dispose()

    $aesKey = New-Object byte[] 32
    $macKey = New-Object byte[] 32
    [Buffer]::BlockCopy($keyMaterial, 0, $aesKey, 0, 32)
    [Buffer]::BlockCopy($keyMaterial, 32, $macKey, 0, 32)

    $aes = [Security.Cryptography.Aes]::Create()
    $aes.KeySize = 256
    $aes.Mode = [Security.Cryptography.CipherMode]::CBC
    $aes.Padding = [Security.Cryptography.PaddingMode]::PKCS7
    $aes.Key = $aesKey
    $aes.IV = $iv
    $encryptor = $aes.CreateEncryptor()
    $cipherBytes = $encryptor.TransformFinalBlock($PlainBytes, 0, $PlainBytes.Length)
    $encryptor.Dispose()
    $aes.Dispose()

    $header = Join-Bytes -Arrays @($magic, $salt, $iv)
    $body = Join-Bytes -Arrays @($header, $cipherBytes)

    $hmac = New-Object Security.Cryptography.HMACSHA256 -ArgumentList @(,$macKey)
    $tag = $hmac.ComputeHash($body)
    $hmac.Dispose()

    return Join-Bytes -Arrays @($body, $tag)
}

function Resolve-InProjectPath {
    param(
        [string]$ProjectRoot,
        [string]$RelativePath
    )

    $combined = Join-Path $ProjectRoot $RelativePath
    return [IO.Path]::GetFullPath($combined)
}

$projectRoot = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot ".."))
$manifestFullPath = Resolve-InProjectPath -ProjectRoot $projectRoot -RelativePath $ManifestPath
if (-not (Test-Path -LiteralPath $manifestFullPath)) {
    throw "Manifest not found: $manifestFullPath"
}

$manifest = Get-Content -Raw -LiteralPath $manifestFullPath | ConvertFrom-Json
if (-not $OutputPath) {
    $OutputPath = $manifest.bundle
}
$outputFullPath = Resolve-InProjectPath -ProjectRoot $projectRoot -RelativePath $OutputPath

$tempRoot = Join-Path $projectRoot ("tmp_encrypt_" + [Guid]::NewGuid().ToString("N"))
$payloadRoot = Join-Path $tempRoot "private_payload"
$zipPath = Join-Path $tempRoot "private_bundle.zip"
New-Item -ItemType Directory -Force -Path $payloadRoot | Out-Null

$copiedPaths = New-Object System.Collections.Generic.List[string]
foreach ($relative in $manifest.protected_paths) {
    $source = Resolve-InProjectPath -ProjectRoot $projectRoot -RelativePath $relative
    if (-not (Test-Path -LiteralPath $source)) {
        continue
    }

    if (-not $source.StartsWith($projectRoot, [StringComparison]::OrdinalIgnoreCase)) {
        throw "Refusing to copy path outside project: $source"
    }

    $destination = Join-Path $payloadRoot $relative
    $destinationParent = Split-Path -Parent $destination
    New-Item -ItemType Directory -Force -Path $destinationParent | Out-Null
    Copy-Item -LiteralPath $source -Destination $destination -Recurse -Force
    $copiedPaths.Add($relative) | Out-Null
}

if ($copiedPaths.Count -eq 0) {
    Remove-Item -LiteralPath $tempRoot -Recurse -Force
    if (Test-Path -LiteralPath $outputFullPath) {
        Write-Host "No protected plaintext paths were found. Existing encrypted bundle is kept: $outputFullPath"
        exit 0
    }
    throw "No protected paths were found to encrypt, and no encrypted bundle exists yet."
}

($manifest | ConvertTo-Json -Depth 10) | Set-Content -LiteralPath (Join-Path $payloadRoot "_private_bundle_manifest.json") -Encoding UTF8
Compress-Archive -Path (Join-Path $payloadRoot "*") -DestinationPath $zipPath -Force

$passphrase = Get-PlainTextSecret
if ([string]::IsNullOrWhiteSpace($passphrase)) {
    Remove-Item -LiteralPath $tempRoot -Recurse -Force
    throw "Encryption key cannot be empty."
}

$plainBytes = [IO.File]::ReadAllBytes($zipPath)
$encryptedBytes = Protect-Bytes -PlainBytes $plainBytes -Passphrase $passphrase
$outputParent = Split-Path -Parent $outputFullPath
if ($outputParent) {
    New-Item -ItemType Directory -Force -Path $outputParent | Out-Null
}
[IO.File]::WriteAllBytes($outputFullPath, $encryptedBytes)
Remove-Item -LiteralPath $tempRoot -Recurse -Force

if ($RemovePlaintext) {
    foreach ($relative in $copiedPaths) {
        $target = Resolve-InProjectPath -ProjectRoot $projectRoot -RelativePath $relative
        if (-not $target.StartsWith($projectRoot, [StringComparison]::OrdinalIgnoreCase)) {
            throw "Refusing to remove path outside project: $target"
        }
        if ($target -match "\\.git($|\\)" -or $target -match "\\tools($|\\)") {
            throw "Refusing to remove protected tooling path: $target"
        }
        if (Test-Path -LiteralPath $target) {
            Remove-Item -LiteralPath $target -Recurse -Force
        }
    }
}

Write-Host "Encrypted bundle written to: $outputFullPath"
if ($RemovePlaintext) {
    Write-Host "Protected plaintext paths were removed from the working tree."
}
else {
    Write-Host "Plaintext paths were kept. Use -RemovePlaintext before publishing."
}
