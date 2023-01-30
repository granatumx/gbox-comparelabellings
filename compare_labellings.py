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
    secondlevel = gn.get_import("toplevel")

    dict_1_inv = invert_dict(toplevel)
    dict_2_inv = invert_dict(secondlevel)
    init_df = pd.DataFrame(0.0, index=dict_2_inv.keys(), columns=dict_1_inv.keys()).apply(lambda col: pd.Series([len(set(dict_1_inv[col.name]).intersection(set(dict_2_inv[row])))/len(dict_1_inv[col.name]) for row in col.index]), axis=0, result_type="broadcast")

    gn.add_pandas_df(init_df)

    gn.commit()


if __name__ == "__main__":
    main()
