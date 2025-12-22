# Apps In Toss Skills

Claude, Codex에서 사용 가능한 앱인토스 에이전트 스킬 모음입니다.

## Skills

- `docs-search`: Toss / Apps-in-Toss `llms-full.txt` 문서를 다운로드·캐시하여 키워드+유사도 기반으로 스니펫을 검색하는 유틸리티.

## Install

### Codex (skill-installer UI)
1. `$ skill-installer` 실행
2. 프롬프트에 입력: `install GitHub repo toss/apps-in-toss-skills path apps-in-toss`

### Claude Code (plugin)
```bash
/plugin marketplace add toss/apps-in-toss-skills
/plugin install apps-in-toss-skill@docs-search
```

## Prompt Examples

- docs-search로 가이드 찾기: `Search guide with docs-search "How to develop Apps In Toss Mini App"`