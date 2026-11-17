"""Fail-closed WSL2/C: admission; no measurement code or source-file mutations."""
import json
import os
from pathlib import Path
import re
import subprocess
import sys

import gse252892_drvfs as drvfs

POWERSHELL = '/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe'
# Only read the current user's WSL registry. Reject reparse points rather than
# infer physical placement from a drive letter through a junction/symlink.
QUERY = r'''
$ErrorActionPreference = 'Stop'
$rows = @(Get-ChildItem 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Lxss' |
  Get-ItemProperty | Where-Object { $_.DistributionName -ceq __DISTRO__ })
if ($rows.Count -ne 1 -or $rows[0].Version -ne 2) { throw 'Unique WSL2 registration required' }
$r = $rows[0]
$base = [string]$r.BasePath
if ($base.StartsWith('\\?\')) { $base = $base.Substring(4) }
if ($base -notmatch '^C:\\') { throw 'Only verified C: VHD placement supported' }
$name = [string]$r.VhdFileName
if (!$name) { $name = 'ext4.vhdx' }
if ($name -notmatch '^[a-zA-Z0-9_.-]+\.vhdx$') { throw 'Invalid VHD filename' }
$vhd = Get-Item -LiteralPath (Join-Path $base $name)
if ($vhd.PSIsContainer -or $vhd.Length -le 0) { throw 'Existing VHD required' }
$item = $vhd
while ($null -ne $item) {
  if ($item.Attributes -band [IO.FileAttributes]::ReparsePoint) { throw 'Reparse point refused' }
  if ($item -is [IO.FileInfo]) { $item = $item.Directory } else { $item = $item.Parent }
}
@{distribution=[string]$r.DistributionName; registry_key=[string]$r.PSChildName;
  base_path=$base; vhd_name=$name; version=[int]$r.Version} | ConvertTo-Json -Compress
'''


def is_wsl():
    return 'microsoft' in Path('/proc/sys/kernel/osrelease').read_text().lower()


def placement(parent):
    """Return stable plan identity, never changing free-space observations."""
    if sys.platform != 'linux':
        raise ValueError('Linux or verified WSL2 required')
    if not is_wsl():
        return {'kind': 'native-linux'}
    distro = os.environ.get('WSL_DISTRO_NAME', '')
    if not distro or len(distro) > 100 or not re.fullmatch(r'[A-Za-z0-9_. -]+', distro):
        raise ValueError('Verifiable WSL distribution name required')
    mount = json.loads(subprocess.check_output(
        ['findmnt', '--json', '--target', str(parent), '--output', 'TARGET,FSTYPE,SOURCE'],
        text=True, timeout=10))['filesystems']
    if (len(mount) != 1 or mount[0]['target'] != '/' or mount[0]['fstype'] != 'ext4'
            or not re.fullmatch(r'/dev/sd[a-z]+', mount[0]['source'])):
        raise ValueError('WSL output must be on the distribution root ext4 VHD')
    query = QUERY.replace('__DISTRO__', "'"+distro+"'")
    result = subprocess.run([POWERSHELL, '-NoProfile', '-NonInteractive', '-Command', query],
                            capture_output=True, text=True, check=True, timeout=15)
    row = json.loads(result.stdout.strip().lstrip('\ufeff'))
    if (row.get('distribution') != distro or type(row.get('version')) is not int
            or row['version'] != 2 or not isinstance(row.get('base_path'), str)
            or not re.match(r'^C:\\', row['base_path'], re.I)
            or not re.fullmatch(r'\{[0-9a-fA-F-]{36}\}', row.get('registry_key', ''))
            or not re.fullmatch(r'[A-Za-z0-9_.-]+\.vhdx', row.get('vhd_name', ''))):
        raise ValueError('Invalid WSL registry/VHD identity')
    physical_free()
    return dict(kind='wsl2-c-vhd', **row)


def physical_free():
    value = drvfs.free_bytes()
    if type(value) is not int or value < 0:
        raise ValueError('Verified physical C: drvfs availability required')
    return value


def check(parent, threshold, admission=False):
    """The caller also checks guest space; never substitute virtual for host."""
    if not is_wsl():
        return None
    value = physical_free()
    if value < threshold:
        raise ValueError('Insufficient physical C: free reserve')
    if admission:
        mem = dict(line.split(':', 1) for line in Path('/proc/meminfo').read_text().splitlines())
        if int(mem['MemAvailable'].split()[0])*1024 < 7*1024**3:
            raise ValueError('WSL admission requires 7 GiB available guest RAM')
    return value
