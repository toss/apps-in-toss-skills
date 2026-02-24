# Apps In Toss Skills

Claude, Codex에서 사용 가능한 앱인토스 에이전트 스킬 모음입니다.

## Plugin & Skills

- Plugin `knowledge-skills`
  - Description: Collection of Apps in Toss knowledge
  - Source: `./`
  - Strict mode: false
  - Bundled skills:
    - `./skills/docs-search`
    - `./skills/project-validator`

### Skills

- `docs-search`: Apps-in-Toss Developer Center, TDS React Native, TDS Web 문서를 검색하고 조회하는 스킬. 키워드로 관련 문서를 검색한 뒤, 결과의 ID로 문서 전체 내용을 가져올 수 있습니다. 별도 설치 없이 자동으로 동작합니다.
- `project-validator`: Apps-in-Toss 웹/React Native/Unity(WebGL) 프로젝트의 `granite.config.ts`, `package.json`, 빌드 산출물, 정책 준수 등을 점검하는 밸리데이터. Unity WebGL은 웹 프레임워크 스키마를 사용하며, 공식 포팅/최적화/디버깅 가이드를 기준으로 검증.

## Install

### Codex (skill-installer UI)
1. `$skill-installer` 실행
2. 프롬프트에 입력: `install github repo toss/apps-in-toss-skills`

### Claude Code (plugin)
```bash
/plugin marketplace add toss/apps-in-toss-skills
/plugin install knowledge-skills@apps-in-toss-skills
```

## Prompt Examples

- docs-search로 가이드 찾기: `Search guide with docs-search "How to develop Apps In Toss Mini App"`
- project-validator로 앱 구성 검증: `Validate granite.config.ts and package.json for a Unity WebGL game (appType: 'game')` 또는 `Check web granite.config.ts matches schema and required permissions`