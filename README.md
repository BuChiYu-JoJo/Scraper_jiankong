# Scraper_jiankong

基于 Thordata Web Scraper API 的抓取任务监控与告警工具。

## 功能概览

- 根据 `spider_name + spider_id + spider_parameters` 创建抓取任务。
- 自动轮询任务状态（`Running / Ready / Failed`）。
- 拉取任务指标并健康分级（`healthy / warning / severe`）。
- 异常时支持钉钉 webhook 告警。
- 可将监控结果落盘为 JSON 文件，便于审计和二次分析。

## 项目结构

```text
src/scraper_monitor/
├── __init__.py
├── alerter.py      # 告警发送
├── analyzer.py     # 健康分级与指标分析
├── client.py       # Thordata API 客户端
├── config.py       # 环境变量配置
├── main.py         # CLI 入口
├── models.py       # 数据模型
├── monitor.py      # 监控主流程
└── storage.py      # 文件落盘
```

## 环境要求

- Linux（Ubuntu/CentOS/Debian 均可）
- Python 3.10+
- 可访问 `https://openapi.thordata.com`

## 配置说明

运行前需要设置以下环境变量：

### 必填

- `THORDATA_TOKEN`：Thordata 平台 token
- `THORDATA_AUTHORIZATION`：创建任务时的 Bearer token（示例：`Bearer xxx`）

### 可选

- `THORDATA_BASE_URL`（默认 `https://openapi.thordata.com/api`）
- `POLL_INTERVAL`（默认 `10` 秒）
- `MAX_RUNNING_TIME`（默认 `1800` 秒）
- `SUCCESS_RATE_THRESHOLD`（默认 `0.95`）
- `SEVERE_RATE_THRESHOLD`（默认 `0.8`）
- `DINGTALK_WEBHOOK`（默认空，不告警）

> 约束：`0 <= SEVERE_RATE_THRESHOLD <= SUCCESS_RATE_THRESHOLD <= 1`。

## Linux 部署与运行教程

### 1) 拉取代码

```bash
git clone <your_repo_url> Scraper_jiankong
cd Scraper_jiankong
```

### 2) 创建虚拟环境并安装依赖

当前实现仅使用 Python 标准库，无第三方依赖，可直接运行。推荐仍使用虚拟环境隔离：

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

### 3) 配置环境变量

```bash
export THORDATA_TOKEN='your_token'
export THORDATA_AUTHORIZATION='Bearer your_bearer_token'

# 可选项
export POLL_INTERVAL=10
export MAX_RUNNING_TIME=1800
export SUCCESS_RATE_THRESHOLD=0.95
export SEVERE_RATE_THRESHOLD=0.8
export DINGTALK_WEBHOOK='https://oapi.dingtalk.com/robot/send?access_token=xxx'
```

### 4) 启动监控

```bash
python -m src.scraper_monitor.main \
  --spider-name amazon.com \
  --spider-id amazon_product_by-url \
  --spider-parameters '{"url":"https://www.amazon.com/dp/B0..."}' \
  --file-name './output/result.json'
```

### 5) 输出说明

程序会输出：

- `task_id`
- `status`（最终分级）
- `raw_status`（Thordata 原始状态）
- `success_rate`
- `download_url`（任务 Ready 时可能有值）
- `updated_at`

如果传入 `--file-name`，会写入完整监控结果 JSON。

## 常见问题

1. **状态一直 Running**  
   检查 `MAX_RUNNING_TIME` 是否过小，或任务参数是否正确。

2. **创建任务失败（鉴权）**  
   检查 `THORDATA_TOKEN` 和 `THORDATA_AUTHORIZATION` 是否正确、是否过期。

3. **未收到钉钉告警**  
   检查 webhook 地址与安全策略（关键词/IP 白名单）。
