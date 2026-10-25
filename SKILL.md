---
name: crude-oil-research-skill
description: 研究 WTI、Brent 和 SC 原油的供需、库存、航运风险、期限结构与多周期价格。用于原油研究和复盘，不将期货曲线直接作为价格预测或自动交易策略。
license: MIT
metadata:
  author: Serennity007
  version: "2.0.0"
---

# 原油研究 Skill

把“事件叙事”拆成供给、需求和物流三条传导链，再检查库存、期限结构与价格是否给出同一答案。

## 工作方式

1. 确认 WTI、Brent 或 SC，指定交易所/来源、合约月、币种与每桶口径。禁止把主连跳空当成真实可交易收益。
2. 分开研究供给损失、需求变化、物流绕行、库存与可用产能；对每个冲击写传导机制和反证。
3. 需要期限结构时读取 `references/domain-data.md`，用同一基准、币种和单位的跨月报价计算；检查异步报价及陈旧时间。
4. 以已收盘 K 线核验价格结构，写基准/上行/下行情景和撤销条件。近月升水可能反映当期紧张，不保证远月或现价上涨。
5. 原观点与后续复盘分开，记录数据公布时刻与换月/成本口径；如无成交记录，不输出实盘收益。

## 按任务读取

- 解释驱动、拆解情景或审核观点时，读 [研究方法](references/method.md)。
- 导入数据或解释指标时，读 [文件与时间契约](references/data-contract.md)。
- 运行领域工具前读 [领域数据与计算](references/domain-data.md)。
- 写研究报告和复盘时，读 [记录字段](references/report-template.md)。
- 核查外部口径时，使用 [官方来源入口](references/sources.md)，记录实际访问日期。

## 研究工作台

完整研究时先读 [工作台与高级数据](references/workbench.md)。使用者给了数据就核对来源、口径和截止时间，运行本地报告；只有问题没有当前数据时，给缺口清单和情景框架。

```bash
python scripts/run_research.py --config examples/workbench.json --out output
```

报告同时输出 HTML、Markdown、JSON，冻结输入并提供可重跑配置。保留陈旧数据、证据冲突、样本缺失和未就绪指标；不把工具生成的报告视为人工核验结论。若讨论当日计划，区分观察条件、确认条件、失效条件和下次检查事件；复盘追加记录，不改写原计划。

## 单项离线计算

在仓库根目录运行；其他目录运行时将脚本、输入和输出替换成对应绝对路径。

```bash
python scripts/analyze_structure.py --csv examples/bars.csv --instrument WTI_SYNTHETIC --timeframe H4 --as-of 2024-01-09T00:00:00+00:00 --data-kind synthetic --support 100 --out output/structure.json
```

附带数据全部为构造样例。更换真实数据后使用 `--data-kind imported_observations` 并填写来源，不因为标签变化而宣称实测收益。未提供当前数据时可以给研究框架和明确缺口，不能编造即时行情。

保留当时可知信息；未公布数据、未来 K 线不能进入历史结论。工具只做描述计算，不提供已验证的胜率、收益或自动执行。

<!-- futures-desk-v3 -->
## Versioned bilingual desk / 双语研究工作台

For historical vintages, explicit daily sessions, comparable basis/spreads, seasonal evidence and fee/margin stress, read [the input contract](docs/desk-data-contract.md) and [the chain playbook](references/research-playbook.md).

```bash
python scripts/run_desk.py run --config examples/desk-demo/crude-oil/config.json --out output --lang en
```

Both English and Chinese reports are generated. Read [the capacity model](docs/desk-risk-model.md) when sizing or stress is requested. Use `verify` and `replay` subcommands for the desk. The existing `run_research.py` command remains supported; new legacy bundles now hash every artifact and verify snapshots on reload. For old committed demonstrations, only the previously recorded input hashes can be verified with `scripts/legacy_bundle_integrity.py`; their original files remain unchanged.
