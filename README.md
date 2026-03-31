# Scraper_jiankong

# Scraper_jiankong

基于 Thordata Web Scraper API 的抓取任务监控与告警项目。  
核心能力：任务创建、状态轮询、结果分析、健康评分、钉钉告警、历史记录落盘。

---

## 1. 功能说明

- 创建抓取任务（`tasks-create`）
- 轮询任务状态（`tasks-status`）
- 读取任务指标（`tasks-list` / `tasks-download`）
- 异常分析（成功率、错误次数、文件大小、API回调）
- 健康评分与分级（normal / warning / critical）
- 钉钉机器人告警推送
- 任务历史记录持久化（JSONL）

---

## 2. 项目结构（建议）

```text
Scraper_jiankong/
├─ README.md
├─ requirements.txt
├─ .env.example
└─ src/
   └─ scraper_monitor/
      ├─ __init__.py
      ├─ config.py
      ├─ models.py
      ├─ client.py
      ├─ analyzer.py
      ├─ alerter.py
      ├─ storage.py
      ├─ monitor.py
      └─ main.py


3. 环境要求
Python 3.10+

可访问 Thordata API

可访问钉钉 webhook（如需告警）

4. 安装依赖
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
5. 配置 .env
复制 .env.example 为 .env，按实际值填写：

THORDATA_BASE_URL=https://openapi.thordata.com/api
THORDATA_TOKEN=your_token
THORDATA_AUTHORIZATION=your_bearer_token

POLL_INTERVAL=10
MAX_RUNNING_TIME=1800

SUCCESS_RATE_THRESHOLD=0.95
SEVERE_RATE_THRESHOLD=0.8

DINGTALK_WEBHOOK=https://oapi.dingtalk.com/robot/send?access_token=xxx
HISTORY_FILE=data/history.jsonl
注意：

tasks-create 需要 token + Authorization: Bearer ...

其他接口主要需要 token

6. 启动方式
6.1 单任务运行
python -m src.scraper_monitor.main \
  --spider-name amazon.com \
  --spider-id amazon_product_by-url \
  --spider-parameters '{"url":"https://www.amazon.com/dp/B0..."}' \
  --file-name "v1_{{TasksID}}.json"
6.2 参数说明
--spider-name：目标站点，例如 amazon.com

--spider-id：爬虫ID，例如 amazon_product_by-url

--spider-parameters：JSON 字符串，具体字段由 spider_id 决定

--file-name：输出文件命名模板，可用 {{TasksID}}

7. 运行流程
创建任务：/web-scraper-api/tasks-create

轮询状态：/web-scraper-api/tasks-status（直到 Ready/Failed）

读取结果：/web-scraper-api/tasks-list 或 tasks-download

执行分析与评分

warning/critical 发送钉钉告警

结果写入历史文件

8. 告警规则（V1）
success_rate < 0.95 -> warning

success_rate < 0.8 -> critical

error_number > 0 -> warning

file_size 异常 -> warning

api_code != 200 或 api_error_msg 非空 -> warning/critical

状态 Failed 或运行超时 -> critical

9. 输出与日志
标准输出：任务果 JSON（task_id、metrics、analysis）

历史文件：HISTORY_FILE（默认 data/history.jsonl）

告警通道：钉钉 webhook（warning/critical）

10. 常见问题
Q1：tasks-download 返回 download 为空？
任务可能未完成，请继续轮询 tasks-status 直到 Ready。

Q2：创建任务报鉴权错误？
检查：

THORDATA_TOKEN 是否正确

THORDATA_AUTHORIZATION 是否带对应 API 的 Bearer token

Q3：钉钉没收到消息？
检查：

webhook 地址是否可用

机器人安全策略（关键字/IP 白名单）是否满足

程序是否进入 warning/critical 分支

11. 后续规划
多任务并发轮询

趋势告警（连续下降）

数据库存储（PostgreSQL/MySQL）

可视化仪表盘（Grafana）
