def get_closest(candidates, val):
    absolute_difference_function = lambda list_value: abs(list_value - val)
    closest_value = min(candidates, key=absolute_difference_function)
    return closest_value


def get_vis_type(vis):
    color = vis.get_attr_by_channel("color") != []
    # Special case for early pruning heatmap set as scatter
    if vis._postbin == True:
        mark = "heatmap"
    if vis.mark == "line":
        mark = "bar"
    else:
        mark = vis.mark
    if color:
        return "color_" + mark
    else:
        return mark


def estimate_vlist_cost(vlist, df_size):
    import pandas as pd
    import lux
    lookup = pd.DataFrame(
        [
            {
                "nPts": 499999,
                "heatmap": 2.2068469524,
                "color_heatmap": 0.0052669048,
                "bar": 0.0466229916,
                "color_bar": 0.1107158661,
                "histogram": 0.0249903202,
                "scatter": 0.0024390221,
                "color_scatter": 0.0050041676,
            },
            {
                "nPts": 711748,
                "heatmap": 3.3235881329,
                "color_heatmap": 0.009978056,
                "bar": 0.0868759155,
                "color_bar": 0.1800460815,
                "histogram": 0.0153999329,
                "scatter": 0.0093228817,
                "color_scatter": 0.1595010757,
            },
            {
                "nPts": 1013173,
                "heatmap": 4.4232890606,
                "color_heatmap": 0.0133640766,
                "bar": 0.1182601452,
                "color_bar": 0.2311317921,
                "histogram": 0.0181698799,
                "scatter": 0.002956152,
                "color_scatter": 0.1479649544,
            },
            {
                "nPts": 1442249,
                "heatmap": 6.0779635906,
                "color_heatmap": 0.0289850235,
                "bar": 0.1360299587,
                "color_bar": 0.2701251507,
                "histogram": 0.0246047974,
                "scatter": 0.0066239834,
                "color_scatter": 0.1732759476,
            },
            {
                "nPts": 2053039,
                "heatmap": 8.883202076,
                "color_heatmap": 0.035492897,
                "bar": 0.1580889225,
                "color_bar": 0.3884789944,
                "histogram": 0.0375738144,
                "scatter": 0.0080881119,
                "color_scatter": 0.2330970764,
            },
            {
                "nPts": 2922496,
                "heatmap": 12.4501621723,
                "color_heatmap": 0.0447099209,
                "bar": 0.211179018,
                "color_bar": 0.4963510036,
                "histogram": 0.0577516556,
                "scatter": 0.010613203,
                "color_scatter": 0.2662091255,
            },
            {
                "nPts": 4160167,
                "heatmap": 18.3932299614,
                "color_heatmap": 0.0606291294,
                "bar": 0.3007659912,
                "color_bar": 0.8055078983,
                "histogram": 0.0939221382,
                "scatter": 0.0175001621,
                "color_scatter": 0.3697118759,
            },
            {
                "nPts": 5921989,
                "heatmap": 24.7001810074,
                "color_heatmap": 0.068185091,
                "bar": 0.4237968922,
                "color_bar": 0.9230899811,
                "histogram": 0.0993611813,
                "scatter": 0.0236811638,
                "color_scatter": 0.450160265,
            },
            {
                "nPts": 8429939,
                "heatmap": 35.826841116,
                "color_heatmap": 0.0813331604,
                "bar": 0.5395438671,
                "color_bar": 1.2810769081,
                "histogram": 0.147039175,
                "scatter": 0.0320770741,
                "color_scatter": 0.7194211483,
            },
            {
                "nPts": 12000000,
                "heatmap": 52.7651646137,
                "color_heatmap": 0.116451025,
                "bar": 0.8801999092,
                "color_bar": 1.9412910938,
                "histogram": 0.2047970295,
                "scatter": 0.0455360413,
                "color_scatter": 0.9958539009,
            },
        ]
    )
    ref_size = get_closest(lookup["nPts"], df_size)
    ref_lookup = lookup[lookup["nPts"] == ref_size]
    vlist_cost = 0
    vis_count = 0
    for vis in vlist:
        vtype = get_vis_type(vis)
        vlist_cost += ref_lookup[vtype].values[0]
        vis_count+=1
        if lux.config.early_pruning:
            if vis_count>lux.config.topk:
                break
    return vlist_cost
