# MediaBridge backend

## 环境与启动

- 虚拟环境固定用 `.venv`
- Python 路径：`.venv/bin/python`
- pip 路径：`.venv/bin/pip`
- 安装依赖：`.venv/bin/pip install -r requirements.txt`
- 本地启动：`.venv/bin/python -m uvicorn main:app --reload`

## 配置真源

- 真实配置结构看 `app/core/config.py` 和 `config.example.yaml`，不要盲信 `README.md`
- 当前代码读取 `config.yaml`；可用 `CONFIG_PATH` 覆盖路径
- cookies 可用 `P115_COOKIES` 环境变量覆盖
- 配置顶层键是 `cloud` 和 `media`
- 轮询配置真实字段是 `cloud.poll_interval_min` / `cloud.poll_interval_max`
- 旧结构 `p115.*`、`rotation_training_interval_*` 只做兼容迁移；新增或修改文档时不要继续扩散旧写法
- `config.yaml` 不存在时，`load_config()` 会生成同目录 `config.example.yaml` 并直接 `sys.exit(1)`

## 运行时结构

- 应用入口：`main.py`
- `main.py` 的 lifespan 启动时会按顺序：加载配置 → 初始化 SQLite → 创建/校验 115 client → 创建 `P115CloudService`、`FileOrganizer`、`TaskMonitor` → 启动后台监控
- 路由集中在 `app/api/`
- 配置与 DI 在 `app/core/`
- 业务逻辑主要在 `app/services/`
- 后台轮询在 `app/tasks/monitor.py`

## 持久化与副作用

- SQLite 路径写死为 `./db/data.db`（见 `app/core/database.py`）
- Docker Compose 挂载 `./config.yaml`、`./db`、`./logs`
- `PUT /api/config` 只改内存中的 `app.state.config`，不会写回 `config.yaml`
- 启动应用会校验 115 cookies，并启动后台监控；不是纯无副作用启动

## 测试与验证

- 全量测试：`.venv/bin/python -m pytest tests -v`
- 覆盖率：`.venv/bin/python -m pytest tests --cov=app --cov-report=html`
- 跑单文件：`.venv/bin/python -m pytest tests/test_api.py -v`
- 跑单测例：`.venv/bin/python -m pytest tests/test_monitor.py -k start_stop -v`
- 这个仓库未看到独立 lint/typecheck 配置；不要编造 `ruff`、`mypy`、`tox`、`nox`、`just`、`make` 命令

## 代码阅读提示

- `README.md` 有过时内容：示例里仍出现旧 `p115` 顶层结构和旧轮询字段；改配置相关代码/文档时以 `app/core/config.py` 为准
- API 测试大量通过 `app.state` 注入 mock 依赖；改依赖注入时先看 `app/core/dependencies.py` 和 `tests/test_api.py`
- 监控逻辑只处理数据库里状态为 `added`/`downloading` 的系统任务，再去比对 115 任务列表；相关回归先看 `tests/test_monitor.py`
