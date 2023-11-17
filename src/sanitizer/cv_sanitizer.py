from pylatex.utils import escape_latex
from src.sanitizer.summary_sanitizer import sanitize_summary
from src.sanitizer.record_sanitizer import sanitize_record
from src.sanitizer.affiliation_sanitizer import sanitize_affiliation

def sanitize_cv(cv_json):
    ERRORS, CV = list(), dict()

    for section_name, section_data in cv_json.items():
        next_markers = dict(list({'section': section_name}.items()))
        if isinstance(section_data, dict):
            CV[escape_latex(section_name)] = sanitize_labeled_items(next_markers, section_data, ERRORS)
        elif isinstance(section_data, list):
            CV[escape_latex(section_name)] = sanitize_unlabeled_items(next_markers, section_data, ERRORS)
        else: ERRORS.append(f'ERROR in {" of ".join([f"{marker_type} {marker}" for marker_type, marker in next_markers.items()])}: A section must point to a JSON object literal or JSON array literal.')
    
    return CV, ERRORS

def sanitize_labeled_items(path_markers, section_data, ERRORS):
    ITEMS = dict()

    for item_name, item_data in section_data.items():
        next_markers = dict(list({'item': item_name}.items())+list(path_markers.items()))
        if isinstance(item_data, str): ITEMS[escape_latex(item_name)] = sanitize_summary(next_markers, item_data, ERRORS)
        elif isinstance(item_data, list): ITEMS[escape_latex(item_name)] = sanitize_affiliation(next_markers, item_data, ERRORS)
        else: ERRORS.append(f'\tERROR in {" of ".join([f"{marker_type} {marker}" for marker_type, marker in next_markers.items()])}: All items of an object-defined section must point to a JSON string literal or JSON array literal.')
    
    return ITEMS

def sanitize_unlabeled_items(path_markers, section_data, ERRORS):
    ITEMS = list()

    for item_index, item_data in enumerate(section_data):
        next_markers = dict(list({'item': item_index+1}.items())+list(path_markers.items()))
        if isinstance(item_data, dict): ITEMS.append(sanitize_record(next_markers, item_data, ERRORS))
        else: ERRORS.append(f'\tERROR in {" of ".join([f"{marker_type} {marker}" for marker_type, marker in next_markers.items()])}: All items of an array-defined section must point to a JSON object literal.')
    
    return ITEMS