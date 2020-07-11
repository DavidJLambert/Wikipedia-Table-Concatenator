""" Wikipedia-Table-Contactenator.py
REPOSITORY:
  https://github.com/DavidJLambert/Wikipedia-Table-Contactenator

SUMMARY:
  Copies Wikipedia page, but with tables "joined" (as in SQL "join").

VERSION:
  0.1.1

AUTHOR:
  David J. Lambert

DATE:
  July 10, 2020

DESCRIPTION:
  https://en.wikipedia.org/wiki/Comparison_of_file_comparison_tools
  https://en.wikipedia.org/wiki/Comparison_of_shopping_cart_software
  https://en.wikipedia.org/wiki/Comparison_of_programming_languages_(basic_instructions)
  https://en.wikipedia.org/wiki/Comparison_of_source-code-hosting_facilities
  https://en.wikipedia.org/wiki/Comparison_of_virtual_private_network_services
  https://en.wikipedia.org/wiki/Comparison_of_web_browsers
  https://en.wikipedia.org/wiki/Comparison_of_webmail_providers
  https://en.wikipedia.org/wiki/Comparison_of_CRM_systems

"""
import io
from bs4 import BeautifulSoup
import re


def main() -> None:
    """ Main program."""

    # Get page text, "soup" it.
    if True:
        # in_file = './data/Comparison of file comparison tools - Wikipedia.html'
        in_file = './data/Comparison of source-code-hosting facilities - Wikipedia.html'
        with io.open(in_file, mode='rt', encoding='utf-8') as f:
            page_html = f.read()
    # else:
    #     page_url = 'https://en.wikipedia.org/wiki/Comparison_of_file_comparison_tools'
    #     page_html = requests.get(page_url).text
    soup = BeautifulSoup(page_html, 'lxml')

    # Find all source wikitables to concatenate.
    wts = soup.find_all('table', class_='wikitable')

    # Pieces of new wikitable we're creating, one piece/wikitable.
    list_wt_dicts = list()
    # Empty rows available to put into wikitables, one empty table/wikitable.
    empty_rows = list()
    # First and last rows, one row/wikitable.
    first_rows = list()
    last_rows = list()

    # Contents of the first column.
    column1_html = dict()

    # Extract rows from each wikitable.
    for wt in wts:
        # Get all rows.
        rows = wt.find_all('tr')

        # Create an empty row for each wikitable, may need later.
        num_td = len(rows[1].find_all('td'))
        empty_rows.append('<td></td>'*num_td)

        # First row of the wikitable.
        stuff = tag_contents(rows[0], 'tr').strip()
        first_rows.append(stuff)

        # Last row of the wikitable, if not a data row.
        # TODO: any row can be a non-data row.
        if last_and_first_rows_same(rows):
            last_index = -1
            stuff = tag_contents(rows[last_index], 'tr').strip()
            last_rows.append(stuff)
        else:
            last_index = len(rows)

        # Other rows in the wikitable.
        list_wt_dicts.append(dict())
        for row in rows[1:last_index]:
            row_html = tag_contents(row, 'tr').strip()
            for text, html in get_pieces(row.find('th')).items():
                column1_html[text] = html
                # Replace column 1 by "html" if it contains multiple items.
                row_html = re.sub('^.*?</th>', html, row_html, flags=re.DOTALL)
                if text in list_wt_dicts[-1].keys():
                    list_wt_dicts[-1][text] += row_html
                else:
                    list_wt_dicts[-1][text] = row_html

    # Set of all keys in all wikitables: sometimes they have different keys.
    all_keys = set()
    for wt_dict in list_wt_dicts:
        all_keys.update(wt_dict.keys())

    # Find location of start of "See also" section, and divide page in two.
    see_also = '<h2><span class="mw-headline" id="See_also">See also</span>'
    location = page_html.find(see_also)
    before = page_html[0:location-1]
    after = page_html[location:]

    # Print original page + concatenated wikitable above "See also" section.
    out_file = './data/output.html'
    with io.open(out_file, mode='w', encoding='utf-8') as f:
        f.write(before)
        f.write('<h2><span class="mw-headline" id="Concatenated_table">Concatenated table</span></h2>')
        f.write('<table class="wikitable sortable">')
        f.write('<tbody>')
        f.write('<tr>')
        # TODO: first_rows for each group.
        [f.write(first_row) for first_row in first_rows]
        f.write('</tr>')
        # TODO: all_keys, list_wt_dicts, column1_html, empty_rows? for each group.
        for key in all_keys:
            f.write('<tr>')
            for wt_dict, empty_row in zip(list_wt_dicts, empty_rows):
                if key in wt_dict.keys():
                    f.write(wt_dict[key])
                else:
                    f.write(column1_html[key] + empty_row)
            f.write('</tr>')
        if last_index == -1:
            f.write('<tr>')
            [f.write(last_row) for last_row in last_rows]
            f.write('</tr>')
        f.write('</tbody>')
        f.write('</table>')
        f.write(after)

    # Break wikitables into groups, where groups share no common keys.
    groups = list()
    wt_dict = list_wt_dicts[0]
    wt_keys = set(wt_dict.keys())
    groups.append(wt_keys)
    for wt_dict in list_wt_dicts[1:]:
        wt_keys = set(wt_dict.keys())
        for group in groups:
            if group.isdisjoint(wt_keys):
                groups.append(wt_keys)
            else:
                group.update(wt_keys)
    for group in groups:
        print(group)
        for item in group:
            for wt_dict in list_wt_dicts:
                if item in wt_dict.keys():
                    print(item)
    exit(0)
# End of function main.


def get_pieces(column1) -> dict:
    """

    Args:
        column1 (object): beautifulSoup object for column 1 of wikitable row.
    Returns:
        get_pieces (dict) = {text1:HTML1, text2:HTML2, ...}
                If column1 has no commas, then get_pieces = {text1:HTML1}, where
            HTML1 is the HTML for column1, including <th> tags, and text1 is
            the text of HTML1.
                If column1 contains a comma-separated list of items, then the
            HTML for column1 is converted into a list of items HTML1, HTML2,
            etc., where each HTML item is the equivalent HTML for each list
            item, including <th> tags, and text1, text2, etc., are the text for
            HTML1, HTML2, etc.
    Raises:
        none.
    """
    column1_text = column1.get_text().split(',')
    if len(column1_text) == 1:
        return {column1_text[0].strip(): str(column1)}
    else:
        tag = '<th'
        for key, value in column1.attrs.items():
            if isinstance(value, list):
                tag += ' ' + key + '="' + value[0] + '"'
            else:
                tag += ' ' + key + '="' + value + '"'
        tag += '>'
        column1_html = list()
        for item in column1.contents[0::2]:
            column1_html.append(tag + str(item) + '</th>')
        return {text.strip(): html
                for text, html in zip(column1_text, column1_html)}
# End of function get_pieces.


def last_and_first_rows_same(rows) -> bool:
    """ Find if last and first rows of a wikitable are the same (apart from
        unimportant details).

    Args:
        rows (object): list of beautifulSoup HTML row objects.
    Returns:
        same (boolean): last row == first row (apart from unimportant details).
    Raises:
        none.
    """
    first_row = rows[0].find_all('th')
    first_row_labels = [elem.get_text().casefold() for elem in first_row]
    last_row = rows[-1].find_all('th')
    last_row_labels = [elem.get_text().casefold() for elem in last_row]
    return first_row_labels == last_row_labels
# End of function last_and_first_rows_same.


def tag_contents(obj, tag: str) -> str:
    """ Get everything between an opening tag and its closing tag.

    Args:
        obj (object): beautifulSoup object that begins with an opening tag
                      and ends with the corresponding closing tag.
        tag (string): the HTML tag we want everything inside of.
    Returns:
        tag_contents (string): everything in obj between the opening tag and its closing tag.
    Raises:
        none.
    """
    contents = obj.prettify()  # The newlines below depend on using prettify.
    contents = re.sub("<{}.*?>\n".format(tag), "", contents)
    contents = re.sub("\n</{}>".format(tag), "", contents)
    return contents
# End of function tag_contents.


if __name__ == '__main__':
    main()
