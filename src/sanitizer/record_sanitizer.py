from pylatex.utils import escape_latex

def sanitize_record(path_markers, record_data, ERRORS):
    RECORD = dict()

    require = {'botleft', 'topleft', 'topright', 'botright', 'content'}
    missing = set(require).difference(record_data.keys())
    invalid = set(record_data.keys()).difference(require)

    if missing: ERRORS.append(f'\t\tERROR in {" of ".join([f"{marker_type} {marker}" for marker_type, marker in path_markers.items()])}: Missing required props {missing}.')
    if invalid: ERRORS.append(f'\t\tERROR in {" of ".join([f"{marker_type} {marker}" for marker_type, marker in path_markers.items()])}: Found invalid props {invalid}.')

    for prop_name, prop_data in record_data.items():
        next_markers = dict(list({'prop': prop_name}.items())+list(path_markers.items()))
        if prop_name in {'botleft', 'topleft', 'topright', 'botright'}:
            if isinstance(prop_data, str): RECORD[prop_name] = sanitize_text(next_markers, prop_data, ERRORS)
            else: ERRORS.append(f'\t\tERROR in {" of ".join([f"{marker_type} {marker}" for marker_type, marker in next_markers.items()])}: Prop \'{prop_name}\' must point to a JSON string literal.')
        elif prop_name == 'content':
            if isinstance(prop_data, list): RECORD[prop_name] = sanitize_content(next_markers, prop_data, ERRORS)
            else: ERRORS.append(f'\t\tERROR in {" of ".join([f"{marker_type} {marker}" for marker_type, marker in next_markers.items()])}: Prop \'{prop_name}\' must point to a JSON array literal.')
    
    return RECORD

def sanitize_content(path_markers, content_data, ERRORS):
    CONTENT = list()

    for point_index, point_data in enumerate(content_data):
        next_markers = dict(list({'point': point_index+1}.items())+list(path_markers.items()))
        if isinstance(point_data, str): CONTENT.append(sanitize_text(next_markers, point_data, ERRORS))
        else: ERRORS.append(f'\t\t\tERROR in {" of ".join([f"{marker_type} {marker}" for marker_type, marker in next_markers.items()])}: All points that define the "content" prop of an item must be JSON string literals.')
    
    return CONTENT

def sanitize_text(path_markers, text_data, ERRORS):
    return escape_latex(text_data)