$configFile = Join-Path (Get-ChocolateyPath -PathType 'PackagePath') 'config.xml'
$config = Import-CliXml $configFile

Remove-Item $config.destination -Recurse -Force

$PathToRemove = $config.destination
foreach ($path in [Environment]::GetEnvironmentVariable("PATH", "User").split(';'))
{
  If ($Path)
  {
    If (($path -ine "$PathToRemove") -AND ($path -ine "$PathToRemove\"))
    {
      [string[]]$Newpath += "$path"
    }
  }
}
$AssembledNewPath = ($newpath -join(';')).trimend(';')

[Environment]::SetEnvironmentVariable("PATH",$AssembledNewPath, "User")
