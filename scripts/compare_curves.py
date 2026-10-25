#!/usr/bin/env python3
"""Compare oil curve snapshots using matching contracts rather than rolling front months."""
import argparse
from pathlib import Path
from analyze_curve import analyze as curve
from market_io import timestamp, emit, kind


def analyze(before_raw, after_raw, before_as_of, as_of, data_kind):
    if timestamp(before_as_of)>=timestamp(as_of):
        raise ValueError('before_as_of must be before as_of')
    before=curve(before_raw,before_as_of,data_kind)
    after=curve(after_raw,as_of,data_kind)
    for field in ('benchmark','currency','unit'):
        if before[field]!=after[field]:
            raise ValueError('curve snapshots must share benchmark/currency/unit')
    old={q['contract']:q for q in before['quotes']}
    new={q['contract']:q for q in after['quotes']}
    common=set(old)&set(new)
    if len(common)<2:
        raise ValueError('at least two matching contracts required; do not substitute a new front month')
    for contract in common:
        if old[contract]['delivery_month']!=new[contract]['delivery_month']:
            raise ValueError('same contract has a changed delivery month')
        if timestamp(new[contract]['quote_time'])<=timestamp(old[contract]['quote_time']):
            raise ValueError('matched current quotes must be newer than previous quotes')
    ordered=sorted(common,key=lambda code:old[code]['delivery_month'])
    near,far=ordered[0],ordered[-1]
    old_spread=old[near]['price']-old[far]['price']
    new_spread=new[near]['price']-new[far]['price']
    delta=new_spread-old_spread
    return {'schema_version':1,'data_kind':kind(data_kind),'before_as_of_utc':before['as_of_utc'],
            'as_of_utc':after['as_of_utc'],'benchmark':after['benchmark'],'currency':after['currency'],
            'unit':after['unit'],'previous_curve_shape':before['curve_shape'],'current_curve_shape':after['curve_shape'],
            'matched_contracts':[{'contract':code,'delivery_month':old[code]['delivery_month'],
                                   'previous_price':old[code]['price'],'current_price':new[code]['price'],
                                   'price_change':new[code]['price']-old[code]['price']} for code in ordered],
            'comparison_pair':[near,far],'previous_matched_spread':old_spread,'current_matched_spread':new_spread,
            'matched_spread_change':delta,'spread_move':'increased' if delta>0 else 'decreased' if delta<0 else 'unchanged',
            'dropped_contracts':sorted(set(old)-common),'added_contracts':sorted(set(new)-common),
            'snapshot_ages_seconds':{'before':before['oldest_quote_age_seconds'],'after':after['oldest_quote_age_seconds']},
            'source_sha256':{'before':before['source_sha256'],'after':after['source_sha256']},
            'scope':'Matched-contract curve change, not a roll return or causal inventory signal.',
            'limitations':['Full-curve shape can include different endpoints; spread change uses only the fixed comparison pair',
                           'Inventory and supply/demand corroboration are not inputs to this calculation']}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--before',type=Path,required=True)
    parser.add_argument('--after',type=Path,required=True)
    parser.add_argument('--before-as-of',required=True)
    parser.add_argument('--as-of',required=True)
    parser.add_argument('--data-kind',choices=('synthetic','imported_observations'),required=True)
    parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args()
    try:
        emit(analyze(args.before.read_bytes(),args.after.read_bytes(),args.before_as_of,args.as_of,args.data_kind),args.out,[args.before,args.after])
    except (ValueError,OSError,KeyError) as exc:
        parser.exit(2,f'ERROR: {exc}\n')
    print('Saved matched-contract curve comparison.')


if __name__=='__main__':
    main()
