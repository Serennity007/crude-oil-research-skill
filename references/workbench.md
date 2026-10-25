# 研究工作台与高级数据

## 一个命令生成一份完整研究快照

```bash
python scripts/run_research.py --config examples/workbench.json --out output
```

会创建新的 `output/run-…/`，重复运行保留之前的报告。可以从其他目录运行：把脚本、配置和输出参数换成相应绝对路径，CSV 路径仍相对配置文件解析。

| 文件 | 内容 |
|---|---|
| REPORT.html | 可直接打开的深色研究面板，含指标、价格折线、分歧、缺口、下次检查和可展开明细；无外部资源 |
| REPORT.md | 便于笔记、版本管理和分享的文字报告 |
| bundle.json | 结构计算、领域分析、高级分析、来源声明、输入哈希和生成时间 |
| inputs/ | 本次实际计算使用的 CSV 原始字节快照 |
| config.snapshot.json | 路径已改为 inputs/ 的重跑配置，摆脱原始输入位置 |
| COMPLETE.json | 只有所有输出写完才产生的完成标记；缺少时视为未完成导出 |

查看已运行的 [模拟报告](../examples/workbench/REPORT.md)、[完整 JSON](../examples/workbench/bundle.json)；下载 [HTML 文件](../examples/workbench/REPORT.html) 后在浏览器打开。GitHub 文件页展示源码，需要下载才能查看本地面板。

重跑一份冻结报告：

```bash
python scripts/run_research.py --config examples/workbench/config.snapshot.json --out output
```

## 换成自己的数据

复制 examples/workbench.json，修改 instrument、as_of、files 和 options，保持 skill 名及必需输入角色。`schema_version=1`；`data_kind` 使用 `imported_observations`；`max_bar_age_hours` 是使用者选择的陈旧阈值，周末和停市仍需按目标市场日历解释。面板工具的 `max_panel_age_days` 用日历日判断，不冒充交易日检查。

导入模式必须为每个文件角色填写来源名称和取数时间，可选真实来源链接。例如：

```json
"sources": {
  "bars": {
    "name": "实际使用的数据提供者与具体代码/合约、单位、周期",
    "retrieved_at": "2026-10-25T10:00:00+08:00",
    "url": "https://实际来源页面"
  }
}
```

上面是字段示意，使用时填实际信息；其余输入角色同样填写。历史研究还需保存当时可知版本与发布时间，下载时间不能代替公布时间。名称、哈希和来源链接记录来源声明，工具不认证它们为真。

旧的单项命令仍可用，新工作台复用相同计算函数。新的报告是结构化研究快照，不是仓位指令、收益回测或预测评分。

## 用在三种研究任务中

盘前计划：给明确数据截止时刻，记录当前背景、待确认条件、失效条件和下一次复查事件。尚未发生的观察结果留空。

事件研判：拆开事件事实、传导假设和价格反应。用同一截止时刻检查已公布数据，报告不能用后来的信息补强当时判断。

盘后复盘：从旧报告的冻结配置重跑以复核原计算，再用新输入产生新报告，逐项说明原假设是否被支持、反证或仍待观察。保留旧报告，不能用新结论覆盖旧计划。

## 原油：固定合约的曲线变化

`scripts/compare_curves.py` 复用已有曲线数据规范，分别按两次 cutoff 过滤前后 CSV，要求基准、币种和单位一致。相同合约的交割月不得变化，当前报价必须更新；至少两个共同合约才比较。

两期交集中最早和最晚的合约组成固定比较对，计算原价差、现价差和差值；同时列出移除、新增合约。整条曲线的 near−far 若端点变了不能直接作差，工具用固定合约对解决这个问题。移除合约不自动等于到期；脚本不核实交易所挂牌与到期日。

```bash
python scripts/compare_curves.py --before examples/previous-curve.csv --after examples/curve.csv --before-as-of 2024-01-08T00:00:00Z --as-of 2024-01-09T15:00:00+08:00 --data-kind synthetic --out output/curve-change.json
```

构造样例移除了 DEMO_OLD 端点，但固定比较 DEMO_NEAR/DEMO_FAR：价差1.5→3，变化+1.5美元/桶。这不是展期收益，也不证明同一期间库存下降。

复核供需时，可用 [EIA Weekly Petroleum Status Report](https://www.eia.gov/petroleum/supply/weekly/) 的统计期与发布时间；分别记录商业库存、交付位置、炼厂需求与进口变化，不将单个库存数值直接升级为方向确定性。
