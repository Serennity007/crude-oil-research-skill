# 原油跨月曲线

脚本 `scripts/analyze_curve.py` 接受 `contract,delivery_month,price,quote_time,benchmark,currency,unit`。

- `contract`：原始合约标识；同一文件每个合约只取一条快照，不接受重复月。样例合约名为虚构标签。
- `delivery_month`：YYYY-MM，按此排序，不从代码推断交割月份；使用者核对交易所实际合约。
- `benchmark`：WTI、BRENT 或 SC，整个曲线必须相同。
- `currency`：三个大写英文字母，整个曲线相同；`unit` 固定为 `currency_per_barrel`。
- `price`：允许负值的有限数；`quote_time`：带时区，晚于截止时刻不参与。

near−far 是按月份排序后的首尾价差；逐段方向一致才标记 contango/backwardation，含折点则 mixed。百分比字段是价差/近月价，不是收益率。近月价非正时输出 null。

检查 `quote_span_seconds` 和 `oldest_quote_age_seconds`，工具不强行将异步报价称为同期曲线，也不认证合约是否挂牌/到期。没有库存、到期日历和成交信息时，结论保留相应缺口。

构造示例近中远月 80/78/77：backwardation，near−far=3，比例0.0375。它是计算例子，不是历史真实油价。
