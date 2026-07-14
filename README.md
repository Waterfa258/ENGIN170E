# LabMind Backend

## My Task

I build the vision API and backend pipeline that converts a reagent-label image into structured OCR data, inventory and expiry results, and alternative recommendations for the Streamlit UI.

## How to Run

Clone the repository and enter the project folder:

```bash
git clone https://github.com/Waterfa258/ENGIN170E.git
cd ENGIN170E
```

Create and activate a virtual environment, install the dependencies, and create the local configuration in Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env.local
```

The default configuration uses mock mode, so it does not make a billable API request. Run the backend with any non-empty `.jpg`, `.jpeg`, `.png`, or `.webp` image:

```python
import json
from backend.pipeline import analyze_label

result = analyze_label("path/to/reagent-label.jpg", mode="mock")
print(json.dumps(result.to_dict(), indent=2))
```

Run the automated tests with:

```bash
python -m unittest discover -s tests
```

For live OCR, change `LABMIND_VISION_MODE` to `live` in `.env.local` and add the appropriate provider API key. Never commit `.env.local`.

## Current Progress

- The backend MVP is complete, including structured OCR, provider configuration, inventory lookup, expiry warnings, product enrichment, and alternative recommendations.
- The sample data currently contains 20 products, 20 inventory records, and 6 alternative mappings.
- All 43 automated backend tests are passing.
- The remaining work is Streamlit UI integration, OCR prompt evaluation with real label images, and end-to-end team testing.

---

# 中文版

## 我的任务

我负责开发 Vision API 和后端流程，将试剂标签图片转换为结构化 OCR 数据、库存与有效期结果以及替代产品推荐，并提供给 Streamlit 界面使用。

## 如何运行

克隆仓库并进入项目文件夹：

```bash
git clone https://github.com/Waterfa258/ENGIN170E.git
cd ENGIN170E
```

在 Windows PowerShell 中创建并激活虚拟环境、安装依赖，然后创建本地配置文件：

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env.local
```

默认配置使用 Mock 模式，因此不会产生 API 调用费用。使用任意非空的 `.jpg`、`.jpeg`、`.png` 或 `.webp` 图片运行后端：

```python
import json
from backend.pipeline import analyze_label

result = analyze_label("path/to/reagent-label.jpg", mode="mock")
print(json.dumps(result.to_dict(), indent=2))
```

运行自动化测试：

```bash
python -m unittest discover -s tests
```

如需使用实时 OCR，请在 `.env.local` 中将 `LABMIND_VISION_MODE` 改为 `live`，并添加相应服务商的 API Key。请勿提交 `.env.local`。

## 当前进度

- 后端 MVP 已完成，包括结构化 OCR、服务商配置、库存查询、到期预警、产品信息补充和替代品推荐。
- 示例数据目前包含 20 条产品记录、20 条库存记录和 6 条替代品映射。
- 43 个后端自动化测试已全部通过。
- 剩余工作包括 Streamlit 界面集成、使用真实标签图片评估 OCR Prompt，以及团队端到端测试。

---

# 한국어 버전

## 제 역할

저는 시약 라벨 이미지를 구조화된 OCR 데이터, 재고 및 유효기간 결과, 대체 제품 추천으로 변환하여 Streamlit UI에 전달하는 Vision API와 백엔드 파이프라인을 개발합니다.

## 실행 방법

저장소를 복제하고 프로젝트 폴더로 이동합니다:

```bash
git clone https://github.com/Waterfa258/ENGIN170E.git
cd ENGIN170E
```

Windows PowerShell에서 가상 환경을 생성 및 활성화하고, 의존성을 설치한 다음 로컬 설정 파일을 생성합니다:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env.local
```

기본 설정은 Mock 모드를 사용하므로 유료 API 요청이 발생하지 않습니다. 비어 있지 않은 `.jpg`, `.jpeg`, `.png` 또는 `.webp` 이미지로 백엔드를 실행합니다:

```python
import json
from backend.pipeline import analyze_label

result = analyze_label("path/to/reagent-label.jpg", mode="mock")
print(json.dumps(result.to_dict(), indent=2))
```

자동화 테스트를 실행합니다:

```bash
python -m unittest discover -s tests
```

실시간 OCR을 사용하려면 `.env.local`에서 `LABMIND_VISION_MODE`를 `live`로 변경하고 해당 제공업체의 API Key를 추가합니다. `.env.local`은 절대 커밋하지 마세요.

## 현재 진행 상황

- 구조화된 OCR, 제공업체 설정, 재고 조회, 유효기간 경고, 제품 정보 보강 및 대체 제품 추천을 포함한 백엔드 MVP가 완료되었습니다.
- 샘플 데이터에는 현재 제품 20개, 재고 레코드 20개, 대체 제품 매핑 6개가 포함되어 있습니다.
- 백엔드 자동화 테스트 43개가 모두 통과했습니다.
- 남은 작업은 Streamlit UI 통합, 실제 라벨 이미지를 사용한 OCR Prompt 평가, 팀 전체의 엔드투엔드 테스트입니다.
