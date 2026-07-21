# LabMind Backend (English)

> This README is available in [English](#labmind-backend-english), [中文](#中文版), and [한국어](#한국어-버전).

## My CSA Task

I maintain the shared LabMind backend that converts reagent-label OCR output into structured inventory, expiry-warning, product, and alternative-recommendation results. The final OCR provider is owned by the AI teammate, while the backend result contract remains stable for CS B.

## AI Teammate Handoff

The latest backend handoff is commit `b741aa7` on the `labmind-backend` branch and [PR #3](https://github.com/Waterfa258/ENGIN170E/pull/3).

Important updates:

- Added the shared `data_loader.py` for `products.csv`, `inventory.csv`, and `alternatives.csv`.
- The incoming inventory field `sku` is standardized to `catalog_number`.
- Month-only expiry values such as `2027-10` are normalized to the final day of that month.
- The new inventory contains 20 validated records with no duplicate identifiers, missing cells, or unmatched product identifiers.
- Fixed a quoted-comma issue in `alternatives.csv` so pandas can parse all six mappings.
- Added a direct pandas dependency and data-loader tests.

The final Gemini integration should replace only the vision-provider layer and preserve this interface:

```python
from backend.pipeline import analyze_label

result = analyze_label(image_path)
payload = result.to_dict()
```

The response must continue using the existing `OCRResult` and `AnalysisResult` schemas so CS B does not need to rewrite the UI. The same shared backend/data-loader changes have already entered the latest `frontend` branch through PR #4. An older Gemini feature branch should be synchronized with the latest `frontend` before final integration.

## How to Run

```powershell
git clone https://github.com/Waterfa258/ENGIN170E.git
cd ENGIN170E
git switch labmind-backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env.local
```

Check all three shared data files:

```powershell
python data_loader.py
```

Run the backend in non-billable mock mode:

```python
import json
from backend.pipeline import analyze_label

result = analyze_label("path/to/reagent-label.jpg", mode="mock")
print(json.dumps(result.to_dict(), indent=2))
```

Run the automated tests:

```powershell
python -m unittest discover -s tests
```

For live OCR, configure the selected provider in the Git-ignored `.env.local` file. Never commit or send an API key through GitHub or ordinary chat.

## Current Progress

- Shared backend pipeline, structured OCR handling, inventory lookup, expiry warnings, product enrichment, and alternative recommendations are complete.
- The repository contains 20 products, 20 inventory records, and 6 reviewed alternative mappings.
- Five real label evaluations and failure records are included.
- All 47 backend tests pass.
- Remaining team work: port the AI teammate's final Gemini provider onto the latest `frontend`, run end-to-end acceptance tests, and deploy with platform Secrets.

---

# 中文版

## 我的 CSA 任务

我负责维护 LabMind 的共享后端，将试剂标签 OCR 输出转换成结构化的库存、有效期预警、产品信息和替代品推荐结果。最终 OCR 服务由 AI 队友负责，但提供给 CS B 的后端结果结构保持稳定。

## 给 AI 队友的交接说明

最新后端交接版本是 `labmind-backend` 分支的提交 `b741aa7`，对应 [PR #3](https://github.com/Waterfa258/ENGIN170E/pull/3)。

重要更新：

- 新增共享的 `data_loader.py`，用于读取 `products.csv`、`inventory.csv` 和 `alternatives.csv`。
- 新库存中的 `sku` 会自动转换为后端使用的 `catalog_number`。
- `2027-10` 这样的月份有效期会转换为该月最后一天。
- 新库存包含 20 条已验证记录，没有重复编号、空值或无法匹配产品的编号。
- 修复了 `alternatives.csv` 中逗号未加引号的问题，pandas 可以正确读取全部 6 条映射。
- 增加 pandas 正式依赖和数据加载器测试。

最终 Gemini 集成只应替换视觉识别服务层，并保留以下接口：

```python
from backend.pipeline import analyze_label

result = analyze_label(image_path)
payload = result.to_dict()
```

返回结果必须继续使用现有的 `OCRResult` 和 `AnalysisResult` 结构，这样 CS B 不需要重写界面。相同的后端和数据加载器改动已经通过 PR #4 进入最新的 `frontend`。较旧的 Gemini 功能分支应先同步最新 `frontend`，再进行最终集成。

## 如何运行

```powershell
git clone https://github.com/Waterfa258/ENGIN170E.git
cd ENGIN170E
git switch labmind-backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env.local
```

检查三个共享数据文件：

```powershell
python data_loader.py
```

使用不会产生 API 费用的 Mock 模式运行后端：

```python
import json
from backend.pipeline import analyze_label

result = analyze_label("path/to/reagent-label.jpg", mode="mock")
print(json.dumps(result.to_dict(), indent=2))
```

运行自动测试：

```powershell
python -m unittest discover -s tests
```

如需实时 OCR，请在 Git 忽略的 `.env.local` 中配置所选服务商。不要将 API Key 提交到 GitHub，也不要通过普通聊天发送。

## 当前进度

- 共享后端流程、结构化 OCR、库存查询、有效期预警、产品信息和替代品推荐均已完成。
- 仓库包含 20 条产品、20 条库存和 6 条已审核的替代品映射。
- 已包含 5 张真实标签的评估结果和失败记录。
- 47 项后端测试全部通过。
- 团队剩余工作：把 AI 队友的最终 Gemini 服务移植到最新 `frontend`，完成端到端验收，并通过部署平台 Secrets 上线。

---

# 한국어 버전

## 제 CSA 역할

저는 시약 라벨 OCR 출력을 구조화된 재고, 유효기간 경고, 제품 정보 및 대체품 추천 결과로 변환하는 LabMind 공용 백엔드를 유지합니다. 최종 OCR 공급자는 AI 팀원이 담당하며, CS B에 제공되는 백엔드 결과 형식은 그대로 유지됩니다.

## AI 팀원 인수인계

최신 백엔드 인수인계 버전은 `labmind-backend` 브랜치의 커밋 `b741aa7`이며 [PR #3](https://github.com/Waterfa258/ENGIN170E/pull/3)에 포함되어 있습니다.

주요 업데이트:

- `products.csv`, `inventory.csv`, `alternatives.csv`를 읽는 공용 `data_loader.py`를 추가했습니다.
- 새 재고 데이터의 `sku` 필드는 백엔드의 `catalog_number`로 자동 변환됩니다.
- `2027-10`과 같은 월 단위 유효기간은 해당 월의 마지막 날짜로 정규화됩니다.
- 새 재고에는 중복 식별자, 누락 셀 또는 제품과 일치하지 않는 식별자가 없는 20개의 검증된 레코드가 있습니다.
- pandas가 6개의 대체품 매핑을 모두 읽을 수 있도록 `alternatives.csv`의 따옴표 누락 문제를 수정했습니다.
- pandas 직접 의존성과 데이터 로더 테스트를 추가했습니다.

최종 Gemini 통합에서는 비전 공급자 계층만 교체하고 다음 인터페이스를 유지해야 합니다:

```python
from backend.pipeline import analyze_label

result = analyze_label(image_path)
payload = result.to_dict()
```

CS B가 UI를 다시 작성하지 않도록 응답은 기존 `OCRResult` 및 `AnalysisResult` 스키마를 계속 사용해야 합니다. 동일한 백엔드 및 데이터 로더 변경 사항은 PR #4를 통해 최신 `frontend` 브랜치에 이미 반영되었습니다. 이전 Gemini 기능 브랜치는 최종 통합 전에 최신 `frontend`와 동기화해야 합니다.

## 실행 방법

```powershell
git clone https://github.com/Waterfa258/ENGIN170E.git
cd ENGIN170E
git switch labmind-backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env.local
```

세 개의 공용 데이터 파일을 확인합니다:

```powershell
python data_loader.py
```

비용이 발생하지 않는 Mock 모드로 백엔드를 실행합니다:

```python
import json
from backend.pipeline import analyze_label

result = analyze_label("path/to/reagent-label.jpg", mode="mock")
print(json.dumps(result.to_dict(), indent=2))
```

자동 테스트를 실행합니다:

```powershell
python -m unittest discover -s tests
```

실시간 OCR을 사용하려면 Git에서 제외된 `.env.local`에 선택한 공급자를 설정하세요. API Key를 GitHub에 커밋하거나 일반 채팅으로 보내지 마세요.

## 현재 진행 상황

- 공용 백엔드 파이프라인, 구조화 OCR 처리, 재고 조회, 유효기간 경고, 제품 정보 보강 및 대체품 추천이 완료되었습니다.
- 저장소에는 제품 20개, 재고 레코드 20개, 검토된 대체품 매핑 6개가 포함되어 있습니다.
- 실제 라벨 5장의 평가 결과와 실패 기록이 포함되어 있습니다.
- 백엔드 테스트 47개가 모두 통과했습니다.
- 남은 팀 작업은 AI 팀원의 최종 Gemini 공급자를 최신 `frontend`에 이식하고, 엔드투엔드 승인 테스트를 실행한 뒤, 배포 플랫폼 Secrets를 사용해 배포하는 것입니다.
