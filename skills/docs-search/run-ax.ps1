$ErrorActionPreference = "Stop"

$FallbackVersion = "0.5.0"
$BaseCacheDir = Join-Path $env:TEMP "apps-in-toss\ax"
$VersionFile = Join-Path $BaseCacheDir ".latest-version"
$VersionTTL = 86400  # 24시간 (초)

# --- 최신 버전 조회 (캐시 + TTL) ---
function Resolve-AxVersion {
    # 캐시 파일이 존재하고 TTL 이내이면 캐시 사용
    if (Test-Path $VersionFile) {
        $age = ((Get-Date) - (Get-Item $VersionFile).LastWriteTime).TotalSeconds
        if ($age -lt $VersionTTL) {
            return (Get-Content $VersionFile -Raw).Trim()
        }
    }

    # GitHub API로 최신 릴리즈 태그 조회
    try {
        $response = Invoke-RestMethod -Uri "https://api.github.com/repos/toss/apps-in-toss-ax/releases/latest" -TimeoutSec 5
        $latest = $response.tag_name -replace '^v', ''
        if ($latest) {
            New-Item -ItemType Directory -Path $BaseCacheDir -Force | Out-Null
            $latest | Set-Content $VersionFile
            return $latest
        }
    } catch {}

    # API 실패 시 만료된 캐시라도 사용
    if (Test-Path $VersionFile) {
        return (Get-Content $VersionFile -Raw).Trim()
    }
    return $FallbackVersion
}

$AxVersion = Resolve-AxVersion
$CacheDir = Join-Path $BaseCacheDir "v$AxVersion"
$AxBin = Join-Path $CacheDir "ax.exe"

# --- ARCH 감지 ---
$Arch = if ($env:PROCESSOR_ARCHITECTURE -eq "ARM64") { "arm64" } else { "amd64" }

# --- 캐시된 바이너리 없으면 다운로드 ---
if (-not (Test-Path $AxBin)) {
    New-Item -ItemType Directory -Path $CacheDir -Force | Out-Null
    $DownloadUrl = "https://github.com/toss/apps-in-toss-ax/releases/download/v${AxVersion}/ax_windows_${Arch}.tar.gz"
    $TarGz = Join-Path $CacheDir "ax.tar.gz"
    Invoke-WebRequest -Uri $DownloadUrl -OutFile $TarGz
    tar -xzf $TarGz -C $CacheDir
    Remove-Item $TarGz -ErrorAction SilentlyContinue
}

# --- 전달받은 인자 그대로 ax에 전달 ---
& $AxBin @args
