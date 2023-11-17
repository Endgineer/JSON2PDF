def generate_record(record_name, record_data):
    string = '%---------------------------------------------------------\n  \\cventry\n    {'+record_data['botleft']+'}\n    {'+record_data['topleft']+'}\n    {'+record_data['topright']+'}\n    {'+record_data['botright']+'}\n    {'
    
    if record_data['content']:
        string += '\n      \\begin{cvitems}'
        for point in record_data['content']:
            string += '\n        \\item {'+point+'}'
        string += '\n      \\end{cvitems}\n    '
    string += '}\n\n'

    return string