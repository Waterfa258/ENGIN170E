# LabMind Backend Refactor — Phase 1

> This README is available in [English](#english), [中文](#中文), and [한국어](#한국어).

## English

### Current Scope

This phase starts the new LabMind backend workflow. It currently covers CAS number validation, the local database foundation, and validated reagent inventory operations; the previous expiry-warning and alternative-recommendation workflow is being replaced.

### Completed

- Added strict CAS format and checksum validation with UI-ready error details.
- Added a SQLite schema for reagent lots and human-reviewed storage suggestions.
- Added a repeatable database initializer with stable project paths and explicit connection cleanup.
- Added human-confirmed reagent insertion, CAS lookup, and newest-first inventory listing.
- Added input checks for CAS numbers, quantities, dates, and JSON tag fields before database writes.
- Removed pending-order automation from the new schema because it is outside the revised MVP.
- Added 22 focused CAS/database tests; all 78 repository tests pass.

CAS checksum validation catches formatting and digit errors, but it does not prove that a CAS number belongs to the chemical shown on a label.

### Run This Phase

Create the environment and install dependencies:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Initialize the local development database:

```powershell
python -m backend.db_init
```

Run the new focused tests:

```powershell
python -m unittest tests.test_cas_validator tests.test_db_init tests.test_db_utils -v
```

Run the complete repository test suite:

```powershell
python -m unittest discover -s tests -v
```

The generated `inventory.db` is for local development and is ignored by Git. A persistent hosted database is still required before public deployment.

### Next

The next backend step is to connect Gemini field extraction to the validated intake data structure, followed by chemical classification and deterministic storage suggestions. Natural-language queries and the revised Streamlit workflow will be integrated in later phases.

---

## 中文

### 当前范围

本阶段开始重构 LabMind 的新后端流程。目前已完成 CAS 号校验、本地数据库基础和经过校验的试剂库存读写；之前的过期预警与替代品推荐流程正在被替换。

### 已完成

- 新增严格的 CAS 格式与校验位检查，并提供可供界面显示的错误信息。
- 新增用于记录试剂批次和人工确认存储建议的 SQLite Schema。
- 新增可重复运行的数据库初始化程序，使用稳定项目路径并正确关闭连接。
- 新增必须经人工确认的试剂入库、按 CAS 查询和按最新记录优先显示的库存列表功能。
- 在写入数据库前校验 CAS、数量、日期和 JSON 标签字段。
- 从新 Schema 中移除不属于新版 MVP 的待收货订单自动化。
- 新增 22 项 CAS 与数据库专项测试；仓库全部 78 项测试通过。

CAS 校验位可以发现格式和数字识别错误，但不能证明该 CAS 号一定属于标签上的化学品。

### 运行本阶段

创建环境并安装依赖：

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

初始化本地开发数据库：

```powershell
python -m backend.db_init
```

运行本阶段测试：

```powershell
python -m unittest tests.test_cas_validator tests.test_db_init tests.test_db_utils -v
```

运行仓库全部测试：

```powershell
python -m unittest discover -s tests -v
```

生成的 `inventory.db` 只用于本地开发，并且已被 Git 忽略。公开部署前仍需接入可持久保存的托管数据库。

### 下一步

下一步将把 Gemini 字段提取接入经过校验的入库数据结构，然后实现化学分类和确定性的存储建议。自然语言查询和新版 Streamlit 流程将在后续阶段接入。

---

## 한국어

### 현재 범위

이 단계에서는 LabMind의 새로운 백엔드 워크플로 리팩터링을 시작합니다. 현재 CAS 번호 검증, 로컬 데이터베이스 기반, 검증된 시약 재고 작업을 완료했으며, 기존 유효기간 경고 및 대체 제품 추천 흐름은 교체 중입니다.

### 완료된 작업

- 엄격한 CAS 형식 및 검사 숫자 검증과 UI용 오류 정보를 추가했습니다.
- 시약 로트와 사람이 검토하는 보관 위치 제안을 위한 SQLite 스키마를 추가했습니다.
- 안정적인 프로젝트 경로를 사용하고 연결을 명시적으로 종료하는 반복 실행 가능한 데이터베이스 초기화 기능을 추가했습니다.
- 사용자 확인 후 시약 추가, CAS 조회, 최신순 재고 목록 기능을 추가했습니다.
- 데이터베이스에 기록하기 전에 CAS 번호, 수량, 날짜, JSON 태그 필드를 검증하도록 했습니다.
- 개정된 MVP 범위에 포함되지 않는 입고 대기 주문 자동화를 새 스키마에서 제거했습니다.
- CAS 및 데이터베이스 집중 테스트 22개를 추가했으며, 저장소의 전체 테스트 78개가 모두 통과합니다.

CAS 검사 숫자 검증은 형식 및 숫자 인식 오류를 찾을 수 있지만, 해당 CAS 번호가 라벨의 화학물질과 실제로 일치함을 증명하지는 않습니다.

### 이 단계 실행 방법

환경을 만들고 의존성을 설치합니다:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

로컬 개발 데이터베이스를 초기화합니다:

```powershell
python -m backend.db_init
```

새 테스트를 실행합니다:

```powershell
python -m unittest tests.test_cas_validator tests.test_db_init tests.test_db_utils -v
```

저장소의 전체 테스트를 실행합니다:

```powershell
python -m unittest discover -s tests -v
```

생성된 `inventory.db`는 로컬 개발용이며 Git에서 제외됩니다. 공개 배포 전에는 데이터를 영구 보존할 수 있는 호스팅 데이터베이스가 필요합니다.

### 다음 단계

다음 백엔드 단계에서는 Gemini 필드 추출을 검증된 입고 데이터 구조에 연결한 뒤, 화학 분류와 결정론적 보관 위치 제안을 구현합니다. 자연어 조회와 개정된 Streamlit 흐름은 이후 단계에서 통합합니다.
