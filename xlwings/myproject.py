from pprint import pprint
import time

import xlwings as xw


@xw.sub  # only required if you want to import it or run it via UDF Server
def main():
    start = time.time()
    wb = xw.Book.caller()
    wb.app.screen_updating = False
    column1 = []
    row_count = 0
    all_data = {}
    child_desc_num = {}
    for each in wb.sheets['bom'].range("A1:A5000"):
        if each.value is None:
            break
        row_count += 1
    
    for row in wb.sheets['bom'].range((2, 1), (row_count, 6)).value:
        if not row or len(row) != 6:
            continue
        value = row[0]
        if isinstance(value, (float, int)):
            value = int(value)
            value = str(value)
        elif isinstance(value, str):
            if not value.isdigit():
                continue
        else:
            print('unknown type')
            continue

        parent_num = value
        all_data.setdefault(parent_num, {})
        all_data[parent_num].setdefault('nodes', [])
        parent_desp = row[1]
        child_desp = row[2]
        chart = row[3]
        usage = row[4]
        note = row[5]
        child_desc_num[child_desp] = parent_num
        column1.append(value)
        all_data[parent_num]['nodes'].append({
            'parent_num': parent_num,
            'parent_desp': parent_desp,
            'child_desp': child_desp,
            'chart': chart,
            'usage': usage,
            'note': note,
        })

    # print(child_desc_num)
    for _key, _value in all_data.items():
        for _each in _value['nodes']:
            # print(_each['parent_desp'])
            if _each['parent_desp'] in child_desc_num:
                _parent_num = child_desc_num[_each['parent_desp']]
                all_data[_parent_num].setdefault('child', [])
                if _each['parent_num'] not in all_data[_parent_num]['child']:
                    all_data[_parent_num]['child'].append(_each['parent_num'])

    # pprint(all_data)

    selection_data = []
    current_row = None
    old_col = None
    for selection in wb.app.selection:
        if current_row is None:
            current_row = selection.row
        if old_col is None:
            old_col = selection.column
        print(selection.value)

        value = selection.value

        if isinstance(value, (float, int)):
            value = int(value)
            value = str(value)
        elif isinstance(value, str):
            if not value.isdigit():
                continue
        else:
            print('unknown type')
            continue

        num = str(value)
        selection_data.append({
            'num': num,
        })

    end = time.time()
    print('time', end - start)

    nodes = []
    for _each in selection_data:

        num = _each['num']
        if num not in all_data:
            return
        tmp_data = [num]
        while 1:
            if not tmp_data:
                break
            curren_data = []
            for _num in tmp_data:
                nodes.extend(all_data[_num]['nodes'])
                children = all_data.get(_num, {}).get('child', [])
                for child in children:
                    nodes.extend(all_data[child]['nodes'])
                    new_child = all_data[child].get('child', [])
                    curren_data.extend(new_child)
            tmp_data = curren_data

    nodes = [list(each.values()) for each in nodes]

    xw.Range((current_row, old_col), (current_row + len(nodes), old_col + 5)).value = nodes
    # for node in nodes:
    #     xw.Range((current_row, old_col)).value = node['parent_num']
    #     xw.Range((current_row, old_col + 1)).value = node['parent_desp']
    #     xw.Range((current_row, old_col + 2)).value = node['child_desp']
    #     xw.Range((current_row, old_col + 3)).value = node['chart']
    #     xw.Range((current_row, old_col + 4)).value = node['usage']
    #     xw.Range((current_row, old_col + 5)).value = node['note']
    #     current_row += 1

    end = time.time()
    print('time2', end - start)


if __name__ == "__main__":
    # xw.books.active.set_mock_caller()
    # main()
    xw.serve()
