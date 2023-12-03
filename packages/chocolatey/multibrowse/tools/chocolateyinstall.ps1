$ErrorActionPreference = 'Stop'; # stop on all errors

$pp = Get-PackageParameters

$url        = 'https://github.com/foxxyz/multibrowse/releases/download/v3.0.0/multibrowse-v3.0.0-win11.zip'

$packageArgs = @{
  packageName   = $env:ChocolateyPackageName
  unzipLocation = if ($pp.installLocation) { $pp.installLocation } else { "$(Get-ToolsLocation)\multibrowse" }
  url           = $url
  checksum      = '5f305be82bdfc9022e59f03a00d65f16a458942a9cf3872d209e283a89be4c95'
  checksumType  = 'sha256'
}

Install-ChocolateyZipPackage @packageArgs
Install-ChocolateyPath $packageArgs.unzipLocation

# Save the install location for uninstalling
$config = @{
  destination = $packageArgs.unzipLocation
}

$configFile = Join-Path $env:chocolateyPackageFolder 'config.xml'
Export-Clixml -Path $configFile -InputObject $config
