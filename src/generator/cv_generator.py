from src.generator.summary_generator import generate_summary
from src.generator.record_generator import generate_record
from src.generator.honors_generator import generate_honors

def generate_cv(cv_sanitized, args):
    string = {
        'name': '\\name{'+args.name.split()[0]+'}{'+args.name.split()[1]+'}' if args.name else 'Curriculum Vitae',
        'position': '\\position{'+args.position+'}' if args.position else '% \\position{}',
        'address': '\\address{'+args.address+'}' if args.address else '% \\address{}',
        'mobile': '\\mobile{'+args.mobile+'}' if args.mobile else '% \\mobile{}',
        'email': '\\email{'+args.email+'}' if args.email else '% \\email{}',
        'github': '\\github{'+args.github+'}' if args.github else '% \\github{}',
        'linkedin': '\\linkedin{'+args.linkedin+'}' if args.linkedin else '% \\linkedin{}',
        'footer': '\\makecvfooter\n  {\\today}\n  {'+args.name+'~~~Â·~~~Curriculum Vitae}\n  {\\thepage\\ / \\pageref*{LastPage}}' if args.footer else '%\\makecvfooter\n  % {\\today}\n  % {Curriculum Vitae}\n  % {\\thepage\\ / \\pageref*{LastPage}}',
        'color': args.color if args.color else '000000'
    }
    
    string = '''%!TEX TS-program = xelatex\n%!TEX encoding = UTF-8 Unicode\n% Awesome CV LaTeX Template for CV/Resume\n%\n% This template has been downloaded from:\n% https://github.com/posquit0/Awesome-CV\n%\n% Author:\n% Claud D. Park <posquit0.bj@gmail.com>\n% http://www.posquit0.com\n%\n% Template license:\n% CC BY-SA 4.0 (https://creativecommons.org/licenses/by-sa/4.0/)\n%\n\n\n%-------------------------------------------------------------------------------\n% CONFIGURATIONS\n%-------------------------------------------------------------------------------\n% A4 paper size by default, use \'letterpaper\' for US letter\n\\documentclass[11pt, a4paper]{awesome-cv}\n\n% Configure page margins with geometry\n\\geometry{left=1.4cm, top=.8cm, right=1.4cm, bottom=1.8cm, footskip=.5cm}\n\n% Color for highlights\n% Awesome Colors: awesome-emerald, awesome-skyblue, awesome-red, awesome-pink, awesome-orange\n%                 awesome-nephritis, awesome-concrete, awesome-darknight\n\\colorlet{awesome}{awesome-red}\n% Uncomment if you would like to specify your own color\n\\definecolor{awesome}{HTML}{'''+string['color']+'''}\n\n% Colors for text\n% Uncomment if you would like to specify your own color\n% \\definecolor{darktext}{HTML}{414141}\n% \\definecolor{text}{HTML}{333333}\n% \\definecolor{graytext}{HTML}{5D5D5D}\n% \\definecolor{lighttext}{HTML}{999999}\n% \\definecolor{sectiondivider}{HTML}{5D5D5D}\n\n% Set false if you don\'t want to highlight section with awesome color\n\\setbool{acvSectionColorHighlight}{true}\n\n% If you would like to change the social information separator from a pipe (|) to something else\n\\renewcommand{\\acvHeaderSocialSep}{\\quad\\textbar\\quad}\n\n%-------------------------------------------------------------------------------\n%\tPERSONAL INFORMATION\n%\tComment any of the lines below if they are not required\n%-------------------------------------------------------------------------------\n% Available options: circle|rectangle,edge/noedge,left/right\n% \\photo{./examples/profile.png}\n'''+string['name']+'''\n'''+string['position']+'''\n'''+string['address']+'''\n\n'''+string['mobile']+'''\n'''+string['email']+'''\n%\\dateofbirth{January 1st, 1970}\n%\\homepage{www.posquit0.com}\n'''+string['github']+'''\n'''+string['linkedin']+'''\n% \\gitlab{gitlab-id}\n% \\stackoverflow{SO-id}{SO-name}\n% \\twitter{@twit}\n% \\skype{skype-id}\n% \\reddit{reddit-id}\n% \\medium{medium-id}\n% \\kaggle{kaggle-id}\n% \\hackerrank{hackerrank-id}\n% \\googlescholar{googlescholar-id}{name-to-display}\n%% \\firstname and \\lastname will be used\n% \\googlescholar{googlescholar-id}{}\n% \\extrainfo{extra information}\n\n%\\quote{``Be the change that you want to see in the world."}\n\n\n%-------------------------------------------------------------------------------\n\\begin{document}\n\n% Print the header with above personal information\n% Give optional argument to change alignment(C: center, L: left, R: right)\n\\makecvheader\n\n% Print the footer with 3 arguments(<left>, <center>, <right>)\n% Leave any of these blank if they are not needed\n'''+string['footer']+'''\n\n\n%-------------------------------------------------------------------------------\n%\tCV/RESUME CONTENT\n%\tEach section is imported separately, open each file in turn to modify content\n%-------------------------------------------------------------------------------'''
    
    for section_name, section_data in cv_sanitized.items():
        string += '\n'+generate_section(section_name, section_data)
    string += '\n\n\n%-------------------------------------------------------------------------------\n\\end{document}\n'

    with open(f'{args.cv_blueprint_json_filepath}.tex', 'w') as cv_file:
        cv_file.write(string)

def generate_section(section_name, section_data):
    string = '%-------------------------------------------------------------------------------\n%\tSECTION TITLE\n%-------------------------------------------------------------------------------\n\\cvsection{'+section_name+'}\n\n\n'

    section_type = list(section_data.values())[0] if section_data else None
    if isinstance(section_type, str):
        if '' in section_data: string += '%-------------------------------------------------------------------------------\n%\tPREAMBLE\n%-------------------------------------------------------------------------------\n'+section_data.pop('')+'\n'
        string += '%-------------------------------------------------------------------------------\n%\tCONTENT\n%-------------------------------------------------------------------------------\n\\begin{cvskills}\n\n'
    elif isinstance(section_type, dict):
        string += '%-------------------------------------------------------------------------------\n%\tCONTENT\n%-------------------------------------------------------------------------------\n\\begin{cventries}\n\n'

    for item_name, item_data in section_data.items():
        if isinstance(item_data, str): string += generate_summary(item_name, item_data)
        elif isinstance(item_data, dict): string += generate_record(item_name, item_data)
        elif isinstance(item_data, list): string += generate_honors(item_name, item_data)
    
    if isinstance(section_type, str): string += '\\end{cvskills}\n'
    elif isinstance(section_type, dict): string += '\\end{cventries}\n'
    
    return string