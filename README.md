# 图斑审查预检系统

本项目面向国土图斑审查场景，目标是构建一套“规则库 + Prompt 推理 + 结构化输出 + 批量评测”的多模态预检原型系统。当前版本已经不再只是目录骨架，而是完成了规则驱动链路、规则覆盖样本集和批量评测闭环。

## 当前状态

- 已建立结构化规则库：`data/rules/rule_template.json`，当前包含图文一致性、耕地疑似建筑占用、举证完整性、举证真实性、林地疑似占用、建设用地用途异常等规则。
- 已建立格式约束：`data/rules/rule_schema.json` 和 `data/samples/sample_schema.json`，用于固定规则和样本字段。
- 已建立样本集：`data/samples/sample_set.json`，当前包含 26 条规则覆盖样本和标准答案，覆盖 R001-R006 以及正常样本。
- 已接通 Prompt 链路：`prompt_builder.py` 会读取结构化规则字段，生成带规则 ID、触发条件、证据要求和输出约束的 Prompt。
- 已接入代码辅助视觉预检：`vision_precheck` 会先提取图片状态、尺寸和 EXIF 等低成本证据，再注入 `metadata.vision_precheck`。
- 已建立 Qwen-VL 接入骨架：`QwenVLClient` 支持通过配置文件接入 OpenAI-compatible 图文接口。
- 已新增本地开源模型入口：`LocalQwenVLClient` 可通过 `Qwen/Qwen2.5-VL-3B-Instruct` 进行低成本本地原型验证。
- 已支持结果追溯：输出结果包含 `rule_hits`，可以说明命中了哪些规则。
- 已接通批量评测：`scripts/evaluate_samples.py` 可以批量运行样本并生成评测报告。
- 已保留 Web 和 CLI 演示入口：支持单条样本演示和页面展示。

当前仍然需要注意：`MockModelClient` 只是用于验证流程的模拟模型，还不是真实多模态模型；`sample_set.json` 中的图片路径仍是占位路径，后续需要补充真实或脱敏样例图片。

## 当前目录

```text
大创多模态/
├─ README.md
├─ configs/
├─ data/
│  ├─ rules/
│  ├─ samples/
│  ├─ raw/
│  ├─ interim/
│  └─ processed/
├─ docs/
├─ examples/
├─ materials/
├─ outputs/
│  ├─ logs/
│  └─ reports/
├─ scripts/
├─ src/
└─ tests/
```

## 模块对应关系

- `src/modules/rule_engine`：加载规则库，筛选启用规则，并按优先级提供给推理流程。
- `src/modules/vision_precheck`：在调用多模态模型前提取图片可读性、尺寸、EXIF 等辅助证据。
- `src/modules/prompt_engine`：根据地块输入和结构化规则生成审查 Prompt。
- `src/modules/model_gateway`：模型接入层；当前保留 `MockModelClient`，并已新增 `QwenVLClient` API 骨架和 `LocalQwenVLClient` 本地开源模型入口。
- `src/modules/postprocess`：解析模型输出，统一转换为结构化结果。
- `src/modules/evaluation`：提供字段完整率等基础评测函数。
- `scripts/evaluate_samples.py`：批量读取样本集，运行 pipeline，并输出评测报告。
- `src/app`：Web 演示入口。

## 运行方式

### 开发前解密

公开仓库会把重点源码、规则和样本放进加密包。继续推进项目之前，先运行：

```bat
tools\decrypt_private.bat
```

输入项目共享 key 后，会恢复 `src/`、`scripts/`、`tests/`、`data/rules/`、`data/samples/` 等受保护内容。

如果你想用环境变量避免重复输入，可以先在当前终端设置：

```bat
set DACHUANG_PRIVATE_KEY=你的共享key
```

不要把 key 写进仓库、文档或提交记录。

### 网页演示

```bash
python run_web.py
```

然后打开：

```text
http://127.0.0.1:5000
```

也可以双击运行：

```text
run_web.bat
```

### 模型审查 API

网页服务同时提供可复用的模型审查接口，方便后续接入其他已经写好的前端页面。

健康检查：

```bash
GET http://127.0.0.1:5000/api/v1/health
```

图片上传审查：

```bash
POST http://127.0.0.1:5000/api/v1/inspect
Content-Type: multipart/form-data
```

表单字段：

- `image_file`：图片文件
- `parcel_id`：图斑编号
- `land_type`：地类信息
- `text_description`：举证说明
- `rules`：可选，每行一条补充规则
- `metadata`：可选，JSON 字符串

接口会返回结构化 JSON，其中 `result` 字段与后端统一的 `InspectionResult` 保持一致，包含 `is_abnormal`、`issue_type`、`reason`、`confidence`、`requires_manual_review`、`evidence` 和 `rule_hits`。

如果其他前端不方便传文件，也可以用 JSON 请求传 `image_path` 或 `image_base64`。接口兼容路径：

```text
/api/v1/inspect
/api/inspect
```

### 单条 Demo

```bash
python run_demo.py
python -m src.app.cli_demo
```

如需切换到配置化真实模型，可先设置：

```bat
set DACHUANG_MODEL_CONFIG=configs\model.example.json
set DASHSCOPE_API_KEY=你的DashScopeKey
python run_demo.py
```

不设置 `DACHUANG_MODEL_CONFIG` 时，系统默认继续使用 Mock 模型。

如需先用低成本开源模型跑通本地流程，可使用：

```bat
pip install torch torchvision transformers accelerate pillow qwen-vl-utils
set DACHUANG_MODEL_CONFIG=configs\model.local_qwen25vl.example.json
python run_demo.py
```

该路线默认使用 `Qwen/Qwen2.5-VL-3B-Instruct`，适合先验证“图片输入 -> 模型理解 -> 规则 JSON -> 前端展示”的完整链路。

### 批量评测

```bash
python scripts/evaluate_samples.py
```

默认读取：

```text
data/samples/sample_set.json
```

默认输出：

```text
outputs/reports/evaluation_summary.json
outputs/reports/evaluation_details.json
outputs/reports/evaluation_details.csv
```

其中 `evaluation_summary.json` 包含总体准确率和 `rule_metrics`，可查看 R001-R006 各规则的样本覆盖、召回率和精确率。

说明：`outputs/reports/` 是本地生成目录，当前在 `.gitignore` 中，适合每次运行后重新生成。

### 测试

```bash
python -m unittest discover -s tests -t . -p "test*.py"
```

当前冒烟测试覆盖：

- 单条 pipeline 运行
- 正常样本不被规则库误触发
- Web 页面渲染与表单提交
- 批量评测脚本生成报告

## 当前评测结果

在当前 26 条规则覆盖样本和 `MockModelClient` 下，批量评测链路可以生成 summary、details 和 CSV 三类报告；summary 中已经包含按规则统计的 `rule_metrics`。

当前 1.0 指标只代表“Mock 环境下流程闭环正确”，不代表真实多模态模型效果。后续接入真实模型后，需要使用同一批样本重新评测并对比结果。

## 下一步建议

1. 设置真实 Qwen-VL API key，使用 `configs/model.example.json` 跑通一条真实模型调用。
2. 准备真实或脱敏图片，将 `image_path` 从占位路径替换为可读取文件。
3. 使用同一套样本集重新运行 `scripts/evaluate_samples.py`，对比 Mock 与真实模型结果。
4. 继续增强 `vision_precheck`，补充 EXIF 时间/GPS 对比、OpenCV 质量检测、YOLO/SAM 证据提取。
5. 将评测结果整理成中期检查或答辩展示材料。

## 公开仓库加密工作流

由于仓库需要公开，重点源码和真实数据不直接以明文上传。当前加密清单位于：

```text
.private-bundle-manifest.json
```

受保护内容包括：

- `src/`
- `scripts/`
- `tests/`
- `configs/`
- `data/rules/`
- `data/samples/`
- `data/raw/images/`
- `data/raw/uploads/`
- `run_demo.py`
- `run_web.py`
- `run_web.bat`

手动加密：

```bat
tools\encrypt_private.bat --remove-plaintext
```

上传到 GitHub：

```bat
post_github.bat "你的提交说明"
```

`post_github.bat` 会在 `git add` 前自动调用加密脚本，生成：

```text
private_bundle.zip.dcb
```

加密成功后，受保护的明文路径会从工作区删除，然后再提交和推送。下一次继续开发时，运行 `tools\decrypt_private.bat` 并输入同一个 key 即可恢复。

加密实现说明：当前机器没有安装 `age`，所以项目内置了 PowerShell/.NET 加密工具，使用 `PBKDF2 + AES-256-CBC + HMAC-SHA256`。key 只从交互输入或 `DACHUANG_PRIVATE_KEY` 环境变量读取，不会写入文件。
