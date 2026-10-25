# Crude oil / 原油

Use the user's requested instrument, window and language. Do not invent a current contract, data subscription, margin schedule or market observation.

## Evidence to establish before interpretation

Record the dated contract, exchange, quote unit/currency, relevant delivery or index definition, cutoff with offset, observation/publication/availability times, and original source. On a roll, keep both contracts and their overlap explicit; do not splice the move into a return.

## Chain-specific hypotheses and failure conditions

- Do not splice SC, Brent and WTI levels: grade, currency, location, freight, tax and delivery terms differ.
- Read dated spreads together with inventories, refinery runs and product demand; backwardation alone does not prove a physical shortage.
- Separate crude, products, strategic stocks, floating storage and transit volumes; weekly changes need comparable coverage and revisions.
- Trace an outage through lost production, export loadings, transit and refinery substitution. Announced cuts and realized exports are different evidence.
- Falsify a demand-led explanation if refinery throughput and product stocks deteriorate despite stronger flat prices. Signed prices disable ordinary return ratios.

## Representative evidence series

- `commercial_crude_inventory`: declare source coverage, native units, publication cadence and revision policy before comparing values.
- `refinery_runs`: declare source coverage, native units, publication cadence and revision policy before comparing values.
- `product_inventory`: declare source coverage, native units, publication cadence and revision policy before comparing values.

A missing series is a gap, not zero. Explain which claim it would support or contradict. Use `fundamentals.metric` names that distinguish region, grade and coverage; the engine does not infer these from a short label.

## Practical research delivery

1. Preserve the supplied files and source claims; state whether the evidence is synthetic, retrieved now or an archived vintage.
2. Run `scripts/run_desk.py` for daily observations, vintages, comparable basis/curve, declared processing recipes and hypothetical capacity. Use existing specialist commands where their native macro, breadth, route or curve inputs fit better.
3. Read the quality gates before interpreting numbers. Reject unit/identity contradictions. Describe unavailable calculations rather than hiding them.
4. Write the observed facts first, then the proposed transmission mechanism, the strongest contrary evidence, and the next publication/event that can falsify it. Cite the original source for substantive imported claims.
5. If the user requests a setup, retain their declared trigger, confirmation, invalidation and time limit; do not manufacture historical signals after seeing future data. Separate a scenario from a forecast.
6. If capacity is requested, require the user's budget and effective rule schedule; report stress beyond the stop plan and the model's single-position scope. Do not select risk parameters for the user.

## Next checks

- Confirm benchmark and delivery scope of every curve point.
- Compare the first published inventory release with later revisions.
- Update freight, outage realization and product cracks using explicit conversion recipes.

## 中文研究要点

- SC、Brent、WTI不能直接拼接价格：油种、币种、地点、运费、税费和交割条件不同。
- 月差须与库存、炼厂开工和成品需求一起研究；近强远弱不能单独证明实物短缺。
- 原油、成品油、战略库存、浮仓与在途分别统计；周变化须核对覆盖和修订。
- 从损失产量、装船、运输和炼厂替代逐段追踪停产；宣布减产与实际出口不是同一证据。
- 平价上涨但加工量和成品库存恶化时，应证伪需求拉动叙事；非正价格不使用普通收益率公式。

- 核对每个曲线点的基准和交割口径。
- 比较库存首次公布与后续修订。
- 使用显式转换配方更新运费、实际停产和成品裂解口径。

## Review exercises

- A user supplies a continuous contract and asks for a roll-period return: obtain dated contracts/overlap or label the result unavailable; do not reinterpret the continuous code as a deliverable contract.
- An inventory revision was published after the report cutoff: exclude that vintage and retain the previously available observation; show the exclusion count.
- A large calculated premium has asynchronous quotes or different tax/quality scope: block the comparison and identify the precise input needed.
- A user asks for the 'best trade' with no current data: supply conditional research questions and evidence gaps; do not invent a current market or implied confidence score.
- A simulated loss budget fits twelve lots but an adverse gap exceeds it: report both values and state why the stop cannot guarantee that budget.
