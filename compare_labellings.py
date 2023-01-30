#!/usr/bin/env python

from granatum_sdk import Granatum
import pandas as pd

def invert_dict(my_map):
    inv_map = {}
    for k, v in my_map.items():
        inv_map[v] = inv_map.get(v, []) + [k]
    return inv_map

def main():
    gn = Granatum()

    toplevel = gn.get_import("toplevel")
    secondlevel = gn.get_import("secondlevel")

    all_keys = set(toplevel.keys()).intersection(secondlevel.keys())
    dict_1 = {k:toplevel[k] for k in all_keys}
    dict_2 = {k:secondlevel[k] for k in all_keys}

    dict_1_inv = invert_dict(dict_1)
    dict_2_inv = invert_dict(dict_2)
    init_df = pd.DataFrame(0.0, index=dict_2_inv.keys(), columns=dict_1_inv.keys()).apply(lambda col: pd.Series([len(set(dict_1_inv[col.name]).intersection(set(dict_2_inv[row])))/len(dict_1_inv[col.name]) for row in col.index]), axis=0, result_type="broadcast")
    df = 100.0*init_df
    df.loc['Column_Total (100 expected)']= df.sum(numeric_only=True, axis=0)
    df.loc[:,'Row_Total'] = df.sum(numeric_only=True, axis=1)

    gn.add_pandas_df(df.reset_index())
    gn.export(df.to_csv(), 'labelpercentages.csv', kind='raw', meta=None, raw=True)

    gn.commit()


if __name__ == "__main__":
    main()
