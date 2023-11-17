from pylatex.utils import escape_latex
from src.sanitizer.summary_sanitizer import sanitize_summary
from src.sanitizer.record_sanitizer import sanitize_record
from src.sanitizer.honors_sanitizer import sanitize_honors

def sanitize_cv(cv_json):
    ERRORS, CV = list(), dict()

    for section_name, section_data in cv_json.items():
        next_markers = dict(list({'section': section_name}.items()))
        if not section_name: ERRORS.append(f'ERROR in {" of ".join([f"{marker_type} {marker}" for marker_type, marker in next_markers.items()])}: A section must have a name.')
        if isinstance(section_data, dict):
            CV[escape_latex(section_name)] = sanitize_section(next_markers, section_data, ERRORS)
        elif isinstance(section_data, list):
            CV[escape_latex(section_name)] = sanitize_section(next_markers, {i+1: data for i, data in enumerate(section_data)}, ERRORS)
        else: ERRORS.append(f'ERROR in {" of ".join([f"{marker_type} {marker}" for marker_type, marker in next_markers.items()])}: A section must point to a JSON object literal or JSON array literal.')
    
    return CV, ERRORS

def sanitize_section(path_markers, section_data, ERRORS):
    ITEMS = dict()

    item_types = {type(item_data) for item_data in section_data.values()}
    if len(item_types) > 1:
        ERRORS.append(f'\tERROR in {" of ".join([f"{marker_type} {marker}" for marker_type, marker in path_markers.items()])}: All items of a section must point to or be of the same type of JSON literal.')
        return ITEMS
    
    for item_name, item_data in section_data.items():
        next_markers = dict(list({'item': item_name}.items())+list(path_markers.items()))
        if isinstance(item_data, str): ITEMS[escape_latex(item_name)] = sanitize_summary(next_markers, item_data, ERRORS)
        elif isinstance(item_data, list): ITEMS[escape_latex(item_name)] = sanitize_honors(next_markers, item_data, ERRORS)
        elif isinstance(item_data, dict): ITEMS[item_name] = sanitize_record(next_markers, item_data, ERRORS)
        else: ERRORS.append(f'\tERROR in {" of ".join([f"{marker_type} {marker}" for marker_type, marker in next_markers.items()])}: Items of a section must either point to a JSON string literal or JSON array literal, or must be JSON object literals.')
    
    return ITEMS