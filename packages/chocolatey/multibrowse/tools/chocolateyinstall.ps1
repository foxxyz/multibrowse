$ErrorActionPreference = 'Stop'; # stop on all errors

$pp = Get-PackageParameters

$url        = 'https://github.com/foxxyz/multibrowse/releases/download/v3.0.2/multibrowse-v3.0.2-win11.zip'

$packageArgs = @{
  packageName   = $env:ChocolateyPackageName
  unzipLocation = if ($pp.installLocation) { $pp.installLocation } else { "$(Get-ToolsLocation)\multibrowse" }
  url           = $url
  checksum      = 'db1e956b53e5080dd7acf68c4bb094313ce9870d4f3e707c3a61f60fc3001187'
  checksumType  = 'sha256'
}

Install-ChocolateyZipPackage @packageArgs
Install-ChocolateyPath $packageArgs.unzipLocation

# Save the install location for uninstalling
$config = @{
  destination = $packageArgs.unzipLocation
}

$configFile = Join-Path (Get-ChocolateyPath -PathType 'PackagePath') 'config.xml'
Export-Clixml -Path $configFile -InputObject $config
