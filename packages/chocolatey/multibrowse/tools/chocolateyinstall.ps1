$ErrorActionPreference = 'Stop'; # stop on all errors

$pp = Get-PackageParameters

$url        = 'https://github.com/foxxyz/multibrowse/releases/download/v2.1.0/multibrowse-2.1.0-win10.zip'

$packageArgs = @{
  packageName   = $env:ChocolateyPackageName
  unzipLocation = if ($pp.installLocation) { $pp.installLocation } else { Get-ToolsLocation }
  url           = $url
  checksum      = '27BD15B39A8802063DA19E7CC6AF1794D31793B4B172D198523EC01A5CD165D3'
  checksumType  = 'sha256'
}

Install-ChocolateyZipPackage @packageArgs
Install-ChocolateyPath "$($packageArgs.unzipLocation)\multibrowse"

# Save the install location for uninstalling
$config = @{
  destination = "$($packageArgs.unzipLocation)\multibrowse"
}

$configFile = Join-Path $env:chocolateyPackageFolder 'config.xml'
Export-Clixml -Path $configFile -InputObject $config
