from pylatex.utils import escape_latex
import validators

class AwesomeCVSanitizer():

    def sanitize_cv(cv):
        sanitized_cv = dict()
        for section_name, section_data in cv.items():
            sanitized_cv[escape_latex(section_name)] = section_data
        
        for section_name, section_data in sanitized_cv.items():
            assert isinstance(section_data, dict), f'Data of section "{section_name}" must be described using type dictionary!'
            AwesomeCVSanitizer.sanitize_section(section_name, section_data)
        
        return sanitized_cv

    def sanitize_section(section_name, section_data):
        assert not set(section_data.keys()).difference({'type', 'items', 'preamble'}), f'Section "{section_name}" contains invalid fields {set(section_data.keys()).difference({"type", "items", "preamble"})}!'
        assert {'type', 'items'}.issubset(set(section_data.keys())), f'Section "{section_name}" does not contain all required fields {str({"type", "items"})}!'
        if 'preamble' in section_data:
            assert isinstance(section_data['preamble'], str), f'Value of the "preamble" field of section "{section_name}" must be of type string!'
            section_data['preamble'] = escape_latex(section_data['preamble'])
        assert section_data['type'] in {'cvskills', 'cventries', 'cvhonors'}, f'Value of the "type" field of section "{section_name}" must be one of {str({"cvskills", "cventries", "cvhonors"})}!'
        assert isinstance(section_data['items'], list), f'Value of the "items" field of section "{section_name}" must be of type list!'
        for i, item in enumerate(section_data['items']):
            AwesomeCVSanitizer.sanitize_item(section_name, section_data['type'], i+1, item)
    
    def sanitize_item(section_name, section_type, i, item):
        assert isinstance(item, dict), f'Item {i} of section "{section_name}" must be of type dictionary!'

        if section_type == 'cvskills':
            assert len(item) == 1, f'Item {i} of section "{section_name}" can only have one key-value pair!'
            assert isinstance(list(item.values())[0], str), f'Value of item {i} of section "{section_name}" must be of type string!'
            sanitized_key = escape_latex(list(item.keys())[0])
            item[sanitized_key] = escape_latex(item.pop(list(item.keys())[0]))
        elif section_type == 'cventries':
            assert not set(item.keys()).difference({'botleft', 'topleft', 'topright', 'botright', 'content', 'url'}), f'Item {i} of section "{section_name}" contains invalid fields {set(item.keys()).difference({"botleft", "topleft", "topright", "botright", "content", "url"})}!'
            assert {'botleft', 'topleft', 'topright', 'botright', 'content'}.issubset(set(item.keys())), f'Item {i} of section "{section_name}" does not contain all required fields {str({"botleft", "topleft", "topright", "botright", "content"})}!'
            if 'url' in item:
                assert validators.url(item['url']), f'Value of the field "url" of item {i} of section "{section_name}" must be a valid URL of type string!'
            assert isinstance(item['botleft'], str), f'Value of field "botleft" of item {i} of section "{section_name}" must be of type string!'
            item['botleft'] = escape_latex(item['botleft'])
            assert isinstance(item['topleft'], str), f'Value of field "topleft" of item {i} of section "{section_name}" must be of type string!'
            item['topleft'] = escape_latex(item['topleft'])
            assert isinstance(item['topright'], str), f'Value of field "topright" of item {i} of section "{section_name}" must be of type string!'
            item['topright'] = escape_latex(item['topright'])
            assert isinstance(item['botright'], str), f'Value of field "botright" of item {i} of section "{section_name}" must be of type string!'
            item['botright'] = escape_latex(item['botright'])
            assert isinstance(item['content'], list), f'Value of field "content" of item {i} of section "{section_name}" must be of type list!'
            for j, point in enumerate(item['content']):
                AwesomeCVSanitizer.sanitize_point(section_name, section_type, i, j+1, item, point)
        elif section_type == 'cvhonors':
            assert len(item) == 1, f'Item {i} of section "{section_name}" can only have one key-value pair!'
            sanitized_key = escape_latex(list(item.keys())[0])
            item[sanitized_key] = item.pop(list(item.keys())[0])
            assert isinstance(list(item.values())[0], list), f'Value of item {i} of section "{section_name}" must be of type list!'
            for j, point in enumerate(list(item.values())[0]):
                AwesomeCVSanitizer.sanitize_point(section_name, section_type, i, j+1, item, point)
    
    def sanitize_point(section_name, section_type, i, j, item, point):
        if section_type == 'cventries':
            assert isinstance(point, str), f'Point {j} of item {i} of section "{section_name}" must be of type string!'
            item['content'][j-1] = escape_latex(point)
        elif section_type == 'cvhonors':
            assert isinstance(point, dict), f'Point {j} of item {i} of section "{section_name}" must be of type dictionary!'
            assert not set(point.keys()).difference({'leftmost', 'left', 'right', 'rightmost'}), f'Point {j} of item {i} of section "{section_name}" contains invalid fields {set(point.keys()).difference({"leftmost", "left", "right", "rightmost"})}!'
            assert {'leftmost', 'left', 'right', 'rightmost'}.issubset(set(point.keys())), f'Point {j} of item {i} of section "{section_name}" does not contain all required fields {str({"leftmost", "left", "right", "rightmost"})}!'
            assert isinstance(point['leftmost'], str), f'Value of field "leftmost" of point {j} of item {i} of section "{section_name}" must be of type string!'
            point['leftmost'] = escape_latex(point['leftmost'])
            assert isinstance(point['left'], str), f'Value of field "left" of point {j} of item {i} of section "{section_name}" must be of type string!'
            point['left'] = escape_latex(point['left'])
            assert isinstance(point['right'], str), f'Value of field "right" of point {j} of item {i} of section "{section_name}" must be of type string!'
            point['right'] = escape_latex(point['right'])
            assert isinstance(point['rightmost'], str), f'Value of field "rightmost" of point {j} of item {i} of section "{section_name}" must be of type string!'
            point['rightmost'] = escape_latex(point['rightmost'])