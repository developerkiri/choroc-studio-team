---
name: choroc-studio-team
description: 초록 스튜디오 식물오브제 디자인 파이프라인. "초록 스튜디오 돌려줘", "시안 뽑아줘", "컨셉 3개 만들어줘" 같은 요청에 트리거해요. input-brief.md를 받으면 리서처 → 컨셉 디자이너 → 비주얼 제너레이터 → 레드팀 → 검증 설계자 → 아카이비스트 순서로 실행해요.
---

# 초록 스튜디오 에이전트 팀

**프로젝트**: 혼자여도 괜찮아, 나만의 초록으로 채우다 (1인가구용 데스크테리어 식물오브제)
**목표**: 아이디어 하나를 넣으면 리서치 → 시안 이미지 → 3D → 검증 키트까지 한 번에 받아보기
**도식**: `team-architecture.html`

## 팀 구성

| 순서 | 에이전트 | 파일 | 모델 | 툴 |
|------|----------|------|------|-----|
| 0 | 디렉터 | `.claude/skills/choroc-studio/SKILL.md` | Opus 5.5 (메인 세션) | 서브에이전트 호출, 파일 쓰기 |
| 1 | 리서처 | `.claude/agents/01-researcher.md` | Sonnet 5.5 | WebSearch, 네이버 쇼핑 API, uibowl MCP |
| 2 | 컨셉 디자이너 | `.claude/agents/02-concept-designer.md` | Opus 5.5 | 텍스트만 |
| 3 | 비주얼 제너레이터 | `.claude/agents/03-visual-generator.md` | Sonnet 5.5 | Higgsfield MCP, fal.ai API (대체) |
| 4 | 레드팀 | `.claude/agents/04-red-team.md` | Opus 5.5 | Read (이미지 확인) |
| 5 | 검증 설계자 | `.claude/agents/05-validation-designer.md` | Sonnet 5.5 | DESIGN.md + HTML 템플릿, Figma(선택) |
| 6 | 아카이비스트 | `.claude/agents/06-archivist.md` | Haiku 4.5 | Notion MCP |
| — | 포트폴리오 에디터 | `.claude/agents/07-portfolio-editor.md` | Opus 5.5 | Notion MCP, Figma MCP (따로 실행) |

> 디렉터가 서브에이전트가 아니라 메인 세션인 이유: Claude Code에서 서브에이전트는 다른 서브에이전트를 부를 수 없어요. 그래서 디렉터는 메인 세션이 맡고, `.claude/settings.json`에서 메인 모델을 Opus로 고정해 둬요.

## 파이프라인

```
입력: templates/input-brief.md 를 채운 파일 (기본: input-brief.md)

1. 리서처          → runs/<RUN>/01-research.md
2. 컨셉 디자이너    → runs/<RUN>/02-concepts.md        (컨셉 3안)
3. 비주얼 제너레이터 → runs/<RUN>/03-visuals.md + images/ (+ model.glb)
4. 레드팀          → runs/<RUN>/04-redteam.md         (PASS / REVISE)
   └ REVISE → 2번으로 1회 되돌림 (02-concepts-v2.md, 03-visuals-v2.md, 04-redteam-v2.md)
   └ 두 번째도 REVISE면 해당 컨셉을 "보류"로 표시하고 계속 진행
5. 검증 설계자      → runs/<RUN>/landing.html (ZenGrid) + 05-validation-kit.md (+ Figma, 템플릿 있을 때)
6. 아카이비스트     → runs/<RUN>/SUMMARY.md + Notion DB 1행

<RUN> = YYYY-MM-DD-HHMM
```

## 디자인 기준

- 화면 결과물(상세페이지, 포트폴리오)은 모두 `DESIGN.md`(ZenGrid + 한글 적용 메모)를 따라요.
- 상세페이지는 `templates/landing-zengrid.html`을 채워서 만들어요. 구조와 CSS는 고치지 않아요.
- **Figma 템플릿 (선택)**: ZenGrid 변수·스타일·컴포넌트가 들어 있는 파일이에요. 아래 값을 채우면 검증 설계자가 그 파일 안에서 v3 프레임을 복제해 써요. 비어 있으면 HTML만 만들어요.
  - 파일 키: (비어 있음)
  - 상세페이지 프레임 노드 ID: (비어 있음)

## 운영 원칙

- 에이전트는 초안까지만 만들어요. 게시, 판매, 메시지 발송처럼 바깥으로 내보내는 행동은 하지 않아요.
- 레드팀 PASS 전에는 검증 단계로 넘어가지 않아요.
- 연결된 툴이 없으면 다음 방법으로 내려가요 (MCP → API 스크립트 → 텍스트/프롬프트만). 툴이 없다는 이유로 파이프라인을 멈추지 않아요.
- 각 단계 산출물은 정해진 템플릿을 지키고, 다음 에이전트에게는 **파일 경로**로 넘겨요 (본문 복사 X).
