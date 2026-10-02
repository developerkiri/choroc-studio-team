# 초록 스튜디오 에이전트 팀

「혼자여도 괜찮아, 나만의 초록으로 채우다」 프로젝트용 AI 에이전트 팀이에요.
식물오브제 아이디어 하나를 넣으면 **리서치 → 컨셉 3안 → 시안 이미지 → 3D → 레드팀 검토 → 검증 키트**까지 한 번에 만들어 줘요.

전체 흐름은 `team-architecture.html`을 브라우저로 열어 보세요.

---

## 1. 처음 한 번만: 설치

```bash
git clone <이 저장소 주소>
cd choroc-studio-team
cp .env.example .env            # 키 채우기 (아래 2번)
cp .mcp.json.example .mcp.json  # MCP 주소 채우기 (아래 3번)
```

필요한 것: [Claude Code](https://claude.com/claude-code) (Claude Pro 이상), Python 3.10+ (추가 패키지 설치는 필요 없어요)

## 2. 키 (`.env`)

| 키 | 어디서 | 없으면 |
|---|---|---|
| `NAVER_CLIENT_ID`, `NAVER_CLIENT_SECRET` | developers.naver.com → 애플리케이션 등록 → 검색 API (무료) | 웹검색으로 대신해요 |
| `FAL_KEY` | fal.ai → Dashboard → Keys (사용량 과금) | Higgsfield가 없을 때만 필요해요 |

## 3. MCP 연결 (`.mcp.json`)

| 서버 | 쓰는 에이전트 | 연결 방법 |
|---|---|---|
| **higgsfield** (추천) | 3 비주얼 제너레이터 | Higgsfield 계정의 MCP/Connector 설정에서 주소를 복사해 `REPLACE_WITH_HIGGSFIELD_MCP_URL` 자리에 넣어요 |
| figma (선택) | 5 검증 설계자, 7 포트폴리오 | 없어도 돼요. 상세페이지는 `DESIGN.md` 기준 HTML로 만들어요. Starter 플랜은 MCP 호출 한도가 작아서 기본값에서 뺐어요 |
| notion | 6 아카이비스트, 7 포트폴리오 | 위와 같아요 |
| uibowl (선택) | 1 리서처 | 쓰지 않으면 `.mcp.json`에서 지워도 돼요 |

Claude Code에서 `/mcp`를 입력하면 연결 상태를 확인하고 로그인할 수 있어요.

**키나 MCP가 하나도 없어도 팀은 끝까지 돌아가요.** 이미지는 프롬프트로, 목업은 텍스트 와이어프레임으로, 기록은 md 파일로 대신 남겨요.

## 4. 실행

```bash
cp templates/input-brief.md input-brief.md   # 아이디어 채우기
claude
```
Claude Code 안에서:
```
초록 스튜디오 돌려줘
```
결과는 `runs/날짜-시각/` 폴더에 생겨요. `SUMMARY.md`부터 열어 보세요.

포트폴리오 정리는 실행 기록이 2회 이상 쌓인 뒤에:
```
포트폴리오 정리해줘. 최종 컨셉은 A안이야.
```

## 디자인 기준 (DESIGN.md)

화면으로 나오는 결과물은 모두 `DESIGN.md`(ZenGrid 디자인 시스템 + 한글 적용 메모)를 따라요. 상세페이지는 `templates/landing-zengrid.html`에 문구와 이미지만 채워서 `runs/…/landing.html`로 만들어요. 디자인을 바꾸고 싶으면 `DESIGN.md`와 이 템플릿만 고치면 다음 실행부터 반영돼요.

## 5. 에이전트와 모델

| # | 에이전트 | 모델 | 왜 이 모델인가 |
|---|---|---|---|
| 0 | 디렉터 (메인 세션) | Opus | 순서와 되돌림 판단 |
| 1 | 리서처 | Sonnet | 검색·요약이 많아서 빠르고 저렴하게 |
| 2 | 컨셉 디자이너 | Opus | 결과 품질을 좌우하는 창작 |
| 3 | 비주얼 제너레이터 | Sonnet | 프롬프트 작성과 툴 호출 반복 |
| 4 | 레드팀 | Opus | 이미지까지 보고 판정하는 게이트 |
| 5 | 검증 설계자 | Sonnet | 틀이 정해진 카피·설문 작성, DESIGN.md 템플릿 채우기 |
| 6 | 아카이비스트 | Haiku | 옮겨 적기만 하는 정리 |
| 7 | 포트폴리오 에디터 | Opus | 기록에서 스토리 뽑기 |

모델은 각 파일 맨 위 `model:` 줄에서 바꿀 수 있어요 (`opus` / `sonnet` / `haiku`). 디렉터 모델은 `.claude/settings.json`의 `"model"`이에요.

### Claude 앱(웹·데스크톱)에서 손으로 돌릴 때
Claude Code 없이도 따라 할 수 있어요. 새 프로젝트를 만들고 `TEAM.md`와 `.claude/agents/*.md`를 프로젝트 파일로 올린 다음, 단계마다 새 대화를 열어서 아래처럼 진행해요:
1. 모델 **Sonnet** 선택 → "01-researcher.md대로 이 브리프를 조사해줘" + 브리프 붙여넣기
2. 모델 **Opus** 선택 → "02-concept-designer.md대로 컨셉 3안" + 1번 결과 붙여넣기
3. 이미지는 Higgsfield 웹에서 `templates/prompt-template.md` 틀로 직접 생성해요
4. 모델 **Opus** 선택 → "04-red-team.md대로 검토해줘" + 컨셉과 이미지 첨부
5. 모델 **Sonnet** 선택 → "05-validation-designer.md대로 검증 키트"

## 6. 리허설 결과 (2026-10-03, 멘토 환경)

입력: "물 주기를 자주 잊는 자취생을 위한 저면관수 이끼 화분, 모니터 옆" → 전체 결과는 `examples/sample-run/`

| 항목 | 실측 |
|---|---|
| 걸린 시간 | 약 16분 (되돌림 1회 포함) |
| 되돌림 | 1회. 1차 레드팀에서 A·B가 REVISE를 받았어요 (A는 PLA 물탱크 누수, B는 막힌 유리 돔에 LED를 얹는 구조와 원가 문제) → v2에서 3개 모두 PASS |
| Higgsfield 크레딧 | **6.5** (이미지 10장 × 0.25 · 배경 제거 2회 · 3D 2개) |
| 산출물 | 리서치 · 컨셉 3안(v1·v2) · 이미지 10장 · 3D 2개 · 레드팀 2회 · Figma 검증 키트 · Notion 기록 1행 |

리허설에서 알게 된 점
- 3D는 `sam_3_3d`가 텍스처까지 1크레딧이라 기본값으로 정했어요. Meshy `image_to_3d`는 텍스처를 넣으면 30크레딧이에요.
- 이미지 여러 장을 한 번에 요청하면 일부가 rate limit(429)로 빠질 수 있어요. 빠진 것만 다시 요청하면 되고, 빠진 요청에는 과금이 없어요.
- 멘토 리허설은 클라우드 환경에서 돌려서 이미지 파일을 내려받지 못했어요 (네트워크 정책). 그래서 `examples/sample-run/`에는 이미지 대신 Higgsfield job id만 있고, 레드팀도 프롬프트 기준으로 판정했어요. **유나 님 PC에서 돌리면 `runs/…/images/`에 파일이 저장되고, 레드팀이 이미지를 직접 보고 판정해요.**

## 7. 폴더 구조

```
TEAM.md                         팀 정의와 파이프라인
team-architecture.html          한눈에 보는 도식
.claude/settings.json           디렉터(메인) 모델, 허용 명령
.claude/skills/choroc-studio/   0 디렉터
.claude/agents/                 1–7 서브에이전트
scripts/fal_generate.py         이미지·배경 제거·3D (fal.ai 대체 경로)
scripts/naver_shopping.py       경쟁 제품·가격 분포
templates/                      입력 브리프, 프롬프트 틀
examples/sample-run/            멘토링 때 돌린 예시 결과
runs/                           내 실행 결과 (git에 안 올라가요)
```

## 지키는 원칙
- 에이전트는 초안까지만 만들어요. SNS 게시, 판매, 메시지 발송은 하지 않아요.
- 이미지 생성은 실행 1회에 이미지 6장 + 3D 1개로 제한해요. 크레딧을 아끼기 위해서예요.
- 최종 선택은 언제나 사람이 해요.
