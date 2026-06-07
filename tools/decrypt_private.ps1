param(
    [string]$BundlePath = "private_bundle.zip.dcb",
    [switch]$Overwrite
)

$ErrorActionPreference = "Stop"

function Get-PlainTextSecret {
    if ($env:DACHUANG_PRIVATE_KEY) {
        return $env:DACHUANG_PRIVATE_KEY
    }

    $secure = Read-Host "Enter decryption key" -AsSecureString
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

function Test-FixedTimeEquals {
    param(
        [byte[]]$Left,
        [byte[]]$Right
    )

    if ($Left.Length -ne $Right.Length) {
        return $false
    }

    $diff = 0
    for ($i = 0; $i -lt $Left.Length; $i++) {
        $diff = $diff -bor ($Left[$i] -bxor $Right[$i])
    }
    return $diff -eq 0
}

function Unprotect-Bytes {
    param(
        [byte[]]$EncryptedBytes,
        [string]$Passphrase
    )

    $magic = [Text.Encoding]::ASCII.GetBytes("DCBUNDLE1")
    $minLength = $magic.Length + 16 + 16 + 32
    if ($EncryptedBytes.Length -le $minLength) {
        throw "Encrypted bundle is too short or corrupted."
    }

    $actualMagic = New-Object byte[] $magic.Length
    [Buffer]::BlockCopy($EncryptedBytes, 0, $actualMagic, 0, $magic.Length)
    if (-not (Test-FixedTimeEquals -Left $actualMagic -Right $magic)) {
        throw "Invalid encrypted bundle format."
    }

    $salt = New-Object byte[] 16
    $iv = New-Object byte[] 16
    [Buffer]::BlockCopy($EncryptedBytes, $magic.Length, $salt, 0, 16)
    [Buffer]::BlockCopy($EncryptedBytes, $magic.Length + 16, $iv, 0, 16)

    $tag = New-Object byte[] 32
    [Buffer]::BlockCopy($EncryptedBytes, $EncryptedBytes.Length - 32, $tag, 0, 32)

    $bodyLength = $EncryptedBytes.Length - 32
    $body = New-Object byte[] $bodyLength
    [Buffer]::BlockCopy($EncryptedBytes, 0, $body, 0, $bodyLength)

    $cipherLength = $EncryptedBytes.Length - $magic.Length - 16 - 16 - 32
    $cipherBytes = New-Object byte[] $cipherLength
    [Buffer]::BlockCopy($EncryptedBytes, $magic.Length + 16 + 16, $cipherBytes, 0, $cipherLength)

    $kdf = New-Object Security.Cryptography.Rfc2898DeriveBytes($Passphrase, $salt, 200000)
    $keyMaterial = $kdf.GetBytes(64)
    $kdf.Dispose()

    $aesKey = New-Object byte[] 32
    $macKey = New-Object byte[] 32
    [Buffer]::BlockCopy($keyMaterial, 0, $aesKey, 0, 32)
    [Buffer]::BlockCopy($keyMaterial, 32, $macKey, 0, 32)

    $hmac = New-Object Security.Cryptography.HMACSHA256 -ArgumentList @(,$macKey)
    $expectedTag = $hmac.ComputeHash($body)
    $hmac.Dispose()
    if (-not (Test-FixedTimeEquals -Left $tag -Right $expectedTag)) {
        throw "Wrong key or corrupted encrypted bundle."
    }

    $aes = [Security.Cryptography.Aes]::Create()
    $aes.KeySize = 256
    $aes.Mode = [Security.Cryptography.CipherMode]::CBC
    $aes.Padding = [Security.Cryptography.PaddingMode]::PKCS7
    $aes.Key = $aesKey
    $aes.IV = $iv
    $decryptor = $aes.CreateDecryptor()
    try {
        return $decryptor.TransformFinalBlock($cipherBytes, 0, $cipherBytes.Length)
    }
    finally {
        $decryptor.Dispose()
        $aes.Dispose()
    }
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
$bundleFullPath = Resolve-InProjectPath -ProjectRoot $projectRoot -RelativePath $BundlePath
if (-not (Test-Path -LiteralPath $bundleFullPath)) {
    throw "Encrypted bundle not found: $bundleFullPath"
}

$passphrase = Get-PlainTextSecret
if ([string]::IsNullOrWhiteSpace($passphrase)) {
    throw "Decryption key cannot be empty."
}

$tempRoot = Join-Path $projectRoot ("tmp_decrypt_" + [Guid]::NewGuid().ToString("N"))
$zipPath = Join-Path $tempRoot "private_bundle.zip"
$extractRoot = Join-Path $tempRoot "extract"
New-Item -ItemType Directory -Force -Path $tempRoot | Out-Null
New-Item -ItemType Directory -Force -Path $extractRoot | Out-Null

$encryptedBytes = [IO.File]::ReadAllBytes($bundleFullPath)
$plainBytes = Unprotect-Bytes -EncryptedBytes $encryptedBytes -Passphrase $passphrase
[IO.File]::WriteAllBytes($zipPath, $plainBytes)
Expand-Archive -Path $zipPath -DestinationPath $extractRoot -Force

$payloadManifestPath = Join-Path $extractRoot "_private_bundle_manifest.json"
if (-not (Test-Path -LiteralPath $payloadManifestPath)) {
    throw "Bundle manifest is missing inside encrypted package."
}

$manifest = Get-Content -Raw -LiteralPath $payloadManifestPath | ConvertFrom-Json
foreach ($relative in $manifest.protected_paths) {
    $source = Join-Path $extractRoot $relative
    if (-not (Test-Path -LiteralPath $source)) {
        continue
    }

    $destination = Resolve-InProjectPath -ProjectRoot $projectRoot -RelativePath $relative
    if (Test-Path -LiteralPath $destination) {
        if (-not $Overwrite) {
            throw "Destination already exists. Re-run with -Overwrite: $destination"
        }
        Remove-Item -LiteralPath $destination -Recurse -Force
    }

    $destinationParent = Split-Path -Parent $destination
    New-Item -ItemType Directory -Force -Path $destinationParent | Out-Null
    Copy-Item -LiteralPath $source -Destination $destination -Recurse -Force
}

Remove-Item -LiteralPath $tempRoot -Recurse -Force
Write-Host "Decrypted protected files into: $projectRoot"
