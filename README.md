# 图斑审查预检系统初步架构

这个目录是根据现有申报材料先搭起来的第一版项目骨架，目标不是一步到位，而是先把后续开发、申报整理、演示验证三条线放到同一个工作区里。

## 材料提炼

- 项目主题已经比较明确：围绕“多模态大模型驱动的图斑审查预检系统”展开。
- 核心问题来自人工审查压力大、图文不一致、异地拍照、旧图新用、死角漏拍、耕地疑似违规占用等场景。
- 前期内部草稿已经把任务拆成了五个天然模块：业务规则与样本、多模态模型接入、提示词与推理设计、结果结构化、系统集成与评测。
- 项目目录按“五模块协作”去设计，便于多人并行推进。

## 当前目录

```text
大创多模态/
├─ README.md
├─ configs/
├─ data/
├─ docs/
├─ examples/
├─ materials/
├─ outputs/
├─ scripts/
├─ src/
└─ tests/
```

## 模块对应关系

- `src/modules/rule_engine`：业务规则、字段定义、规则加载。
- `src/modules/model_gateway`：多模态模型接口层，后续可接 OpenAI、Qwen、Gemini 或本地模型。
- `src/modules/prompt_engine`：审查提示词、Few-shot、审查流程编排。
- `src/modules/postprocess`：模型输出解析、结构化、容错修补。
- `src/modules/evaluation`：评测指标、字段完整率、结果对比。
- `src/app`：演示入口，后面可以扩成 CLI、Web Demo 或答辩展示版本。

## 现在已经放进去的内容

- 公开仓库只保留代码骨架、脱敏说明和示例数据。
- 含真实姓名与申报细节的原始材料已移出仓库，单独保存在本地私密目录。
- 已写好一版可运行的 Python 骨架，先用 `MockModelClient` 打通流程。
- 已补了目录说明、材料梳理和初步工作分工文档。

## 运行方式

### 网页版

推荐直接启动本地网页：

```bash
python run_web.py
```

然后打开：

```text
http://127.0.0.1:5000
```

如果你更想直接双击启动，也可以用根目录下的：

```text
run_web.bat
```

它会自动：

- 切换到项目根目录
- 启动 Flask 网页服务
- 自动打开浏览器访问 `http://127.0.0.1:5000`

### 终端版

如果只是临时看结构化输出，也保留了命令行入口：

```bash
python run_demo.py
python -m src.app.cli_demo
```

如果你当前就在 `src/app` 目录下，也可以直接运行：

```bash
python cli_demo.py
```

### 测试

```bash
python -m unittest discover -s tests -t . -p "test*.py"
```

注意：

- `python -m src.app.cli_demo` 只能在项目根目录 `大创多模态/` 下运行。
- 现在更推荐你直接用 `python run_web.py`，这样就是网页入口，不用盯着终端看 JSON。

## 下一步建议

1. 先补 `data/rules/rule_template.json`，把审查规则写细。
2. 再把 `MockModelClient` 替换成真实多模态模型接口。
3. 按 `docs/初步工作分工.md` 认领模块后，开始并行推进。
