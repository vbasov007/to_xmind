
def parse_filter_arguments(arg):

    col_name = arg.split('=')[0].strip().strip('"').strip("'")
    val_list = arg.split('=')[1].split(',')
    val_list = [v.strip().strip('"').strip("'") for v in val_list]

    return col_name, val_list


def turn_to_list(arg):
    res = []
    for item in arg:
        try_split = item.split()
        res.extend(try_split)
    return res

