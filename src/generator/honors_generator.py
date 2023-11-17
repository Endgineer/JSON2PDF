def generate_honors(honors_name, honors_data):
    string = '' if not honors_name else '%-------------------------------------------------------------------------------\n%\tSUBSECTION TITLE\n%-------------------------------------------------------------------------------\n\\cvsubsection{'+honors_name+'}\n\n\n'
    string += '%-------------------------------------------------------------------------------\n%\tCONTENT\n%-------------------------------------------------------------------------------\n\\begin{cvhonors}\n\n'
    for point in honors_data:
        string += '%---------------------------------------------------------\n  \\cvhonor\n    {'+point['left']+'}\n    {'+point['right']+'}\n    {'+point['rightmost']+'}\n    {'+point['leftmost']+'}\n\n'
    string += '\\end{cvhonors}\n'
    
    return string