"""
Usage: build_tool CONFIG_XLSX OUT_HTML [--folder=WORKING_FOLDER]

Arguments:
    CONFIG_XLSX         Config excel file path
    OUT_HTML            Input html file path
    WORKING_FOLDER      Working folder

Options:
    -h --help
    -f --folder=WORKING_FOLDER

"""

from docopt import docopt

from html_template import CompeleteToolTemplate
from product_table_to_html import product_table_to_html
import pandas as pd
import os


def build_tool():

    args = docopt(__doc__)

    working_folder = ''
    if args['--folder']:
        working_folder = args['--folder']

    config_df = pd.read_excel(os.path.join(working_folder, args['CONFIG_XLSX']))

    config_df.fillna('',inplace=True)

    config_df.set_index('index')

    config_dict = config_df.to_dict('index')

    template = CompeleteToolTemplate()

    for i in config_dict:

        row = config_dict[i]

        row = {str(key): str(row[key]) for key in row}

        print(row)

        df = pd.read_excel(os.path.join(working_folder, row['input_xlsx']))

        table_html = product_table_to_html(
            df,
            row['category'],
            row['subcategory'],
            row['view'],
            row['main_topic'],
            row['tree'],
            row['attributes'],
            row['url_source'],
            row['exclude'],
            row['include_only'],
            row['match'],
            )

        template.add_table(table_html)

    out_html = template.make()

    with open(os.path.join(working_folder, args['OUT_HTML']), "w", encoding='utf-8') as out_html_file:
        out_html_file.write(out_html)


def build_tool_test():

    file_list = ["f1.html", "f2.html", "f3.html"]

    template = CompeleteToolTemplate()

    for file_name in file_list:
        with open(file_name, "r", encoding='utf-8') as html_file:
            html = html_file.read()
        template.add_table(html)

    out_html = template.make()

    with open("out.html", "w", encoding='utf-8') as out_html_file:
        out_html_file.write(out_html)

if __name__ == '__main__':
    build_tool()


