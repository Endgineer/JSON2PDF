from pylatex.utils import escape_latex

def sanitize_affiliation(path_markers, affiliation_data, ERRORS):
    AFFILIATION = list()

    for honor_index, honor_data in enumerate(affiliation_data):
        next_markers = dict(list({'honor': honor_index+1}.items())+list(path_markers.items()))
        if isinstance(honor_data, dict): AFFILIATION.append(sanitize_honor(next_markers, honor_data, ERRORS))
        else: ERRORS.append(f'\t\tERROR in {" of ".join([f"{marker_type} {marker}" for marker_type, marker in next_markers.items()])}: All honors within an affiliation must be JSON object literals.')
    
    return AFFILIATION

def sanitize_honor(path_markers, honor_data, ERRORS):
    HONOR = dict()

    require = {'leftmost', 'left', 'right', 'rightmost'}
    missing = set(require).difference(honor_data.keys())
    invalid = set(honor_data.keys()).difference(require)

    if missing: ERRORS.append(f'\t\t\tERROR in {" of ".join([f"{marker_type} {marker}" for marker_type, marker in path_markers.items()])}: Missing required props {missing}.')
    if invalid: ERRORS.append(f'\t\t\tWARNING in {" of ".join([f"{marker_type} {marker}" for marker_type, marker in path_markers.items()])}: Ignoring invalid props {invalid}.')

    for prop_name, prop_data in honor_data.items():
        next_markers = dict(list({'prop': prop_name}.items())+list(path_markers.items()))
        if prop_name in require:
            if isinstance(prop_data, str): HONOR[prop_name] = sanitize_text(next_markers, prop_data, ERRORS)
            else: ERRORS.append(f'\t\t\tERROR in {" of ".join([f"{marker_type} {marker}" for marker_type, marker in next_markers.items()])}: Prop \'{prop_name}\' must point to a JSON string literal.')
    
    return HONOR

def sanitize_text(path_markers, text_data, ERRORS):
    return escape_latex(text_data)