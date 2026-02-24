#!/usr/bin/env bash
set -euo pipefail

FALLBACK_VERSION="0.5.0"
BASE_CACHE_DIR="${TMPDIR:-/tmp}/apps-in-toss/ax"
VERSION_FILE="${BASE_CACHE_DIR}/.latest-version"
VERSION_TTL=86400  # 24시간 (초)

# --- 최신 버전 조회 (캐시 + TTL) ---
resolve_version() {
  # 캐시 파일이 존재하고 TTL 이내이면 캐시 사용
  if [[ -f "$VERSION_FILE" ]]; then
    local age=$(( $(date +%s) - $(date -r "$VERSION_FILE" +%s 2>/dev/null || stat -c %Y "$VERSION_FILE" 2>/dev/null || echo 0) ))
    if (( age < VERSION_TTL )); then
      cat "$VERSION_FILE"
      return
    fi
  fi

  # GitHub API로 최신 릴리즈 태그 조회
  local latest
  latest=$(curl -fsSL --max-time 5 \
    "https://api.github.com/repos/toss/apps-in-toss-ax/releases/latest" 2>/dev/null \
    | grep '"tag_name"' | head -1 | sed 's/.*"v\([^"]*\)".*/\1/') || true

  if [[ -n "$latest" ]]; then
    mkdir -p "$BASE_CACHE_DIR"
    echo "$latest" > "$VERSION_FILE"
    echo "$latest"
  elif [[ -f "$VERSION_FILE" ]]; then
    # API 실패 시 만료된 캐시라도 사용
    cat "$VERSION_FILE"
  else
    echo "$FALLBACK_VERSION"
  fi
}

AX_VERSION="$(resolve_version)"
CACHE_DIR="${BASE_CACHE_DIR}/v${AX_VERSION}"
AX_BIN="${CACHE_DIR}/ax"

# --- OS/ARCH 감지 ---
OS="$(uname -s | tr '[:upper:]' '[:lower:]')"   # darwin / linux
ARCH="$(uname -m)"
case "$ARCH" in
  x86_64)  ARCH="amd64" ;;
  aarch64|arm64) ARCH="arm64" ;;
esac

# --- 캐시된 바이너리 없으면 다운로드 ---
if [[ ! -x "$AX_BIN" ]]; then
  mkdir -p "$CACHE_DIR"
  DOWNLOAD_URL="https://github.com/toss/apps-in-toss-ax/releases/download/v${AX_VERSION}/ax_${OS}_${ARCH}.tar.gz"
  curl -fsSL "$DOWNLOAD_URL" | tar -xz -C "$CACHE_DIR"
  chmod +x "$AX_BIN"
fi

# --- 전달받은 인자 그대로 ax에 전달 ---
exec "$AX_BIN" "$@"
