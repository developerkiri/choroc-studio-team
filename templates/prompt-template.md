# 이미지 프롬프트 틀

비주얼 제너레이터가 컨셉마다 칸을 채워서 써요. 직접 툴에 넣어 볼 때도 같은 틀을 쓰면 결과를 비교하기 쉬워요.

## 칸
| 칸 | 설명 | 예시 |
|---|---|---|
| 제품 | 무엇인지 + 식물. 화분이 아니면 제품군 그대로 | small self-watering moss planter / modular steel desk tray with air plant |
| 형태 | 컨셉 보드의 형태 언어 | rounded rectangular, stepped edges |
| 소재·마감 | 소재 + 컬러 2개 | matte sage-green ceramic, frosted glass water tank |
| 크기 단서 | 책상 위 크기감 | palm-sized, next to a 24-inch monitor |
| 장면 | 단독컷 / 연출컷 | (아래 고정 문구 사용) |
| 키워드 | 컨셉 보드의 영문 5개 | calm, minimal, Japanese, soft, tidy |

## 고정 문구 (6장 모두 같게)
- **단독컷**: `product photo, 3/4 view, seamless white background, softbox lighting, sharp focus, no text, no logo`
- **연출컷**: `[장소], warm afternoon window light, shallow depth of field, no people, no text, no logo`
  - `[장소]`는 컨셉의 **사용 장면**을 그대로 영어로 옮겨요 (예: `on a desk to the left of an open 14-inch laptop`). 비어 있으면 `on a small studio-apartment desk beside a monitor and keyboard`.
  - 장소만 컨셉마다 다르고, 빛·심도 문구는 6장 모두 같게 둬요. (초기 버전은 장소까지 고정해서, 노트북 옆에 두는 컨셉도 모니터 옆으로 찍혔어요.)

## 조합 순서
```
[제품], [형태], [소재·마감], [크기 단서], [키워드 5개], [장면 고정 문구]
```

예:
```
small self-watering moss planter, rounded rectangular with stepped edges, matte sage-green ceramic with frosted glass water tank, palm-sized, calm minimal Japanese soft tidy, product photo, 3/4 view, seamless white background, softbox lighting, sharp focus, no text, no logo
```
