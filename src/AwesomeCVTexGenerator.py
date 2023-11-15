import os

from src.utils.AwesomeCVSanitizer import AwesomeCVSanitizer

class AwesomeCVTexGenerator():
    
    def generate_cv(cv, args):
        anonymize = not (args.name and args.position and args.address and args.mobile and args.email and args.linkedin)
        cv = AwesomeCVSanitizer.sanitize_cv(cv)
        string = {'first': 'First', 'last': 'Last', 'position': 'Software Engineer', 'address': 'City, PA', 'mobile': '000-000-0000', 'email': 'identifier@domainname.tld', 'linkedin': 'linkedin.com/'} if anonymize else {'first': args.name.split()[0], 'last': args.name.split()[1], 'position': args.position, 'address': args.address, 'mobile': args.mobile, 'email': args.email, 'linkedin': args.linkedin, 'github': args.github}

        string = '%!TEX TS-program = xelatex\n%!TEX encoding = UTF-8 Unicode\n% Awesome CV LaTeX Template for CV/Resume\n%\n% This template has been downloaded from:\n% https://github.com/posquit0/Awesome-CV\n%\n% Author:\n% Claud D. Park <posquit0.bj@gmail.com>\n% http://www.posquit0.com\n%\n% Template license:\n% CC BY-SA 4.0 (https://creativecommons.org/licenses/by-sa/4.0/)\n%\n\n\n%-------------------------------------------------------------------------------\n% CONFIGURATIONS\n%-------------------------------------------------------------------------------\n% A4 paper size by default, use \'letterpaper\' for US letter\n\\documentclass[11pt, a4paper]{awesome-cv}\n\n% Configure page margins with geometry\n\\geometry{left=1.4cm, top=.8cm, right=1.4cm, bottom=1.8cm, footskip=.5cm}\n\n% Color for highlights\n% Awesome Colors: awesome-emerald, awesome-skyblue, awesome-red, awesome-pink, awesome-orange\n%                 awesome-nephritis, awesome-concrete, awesome-darknight\n\\colorlet{awesome}{awesome-red}\n% Uncomment if you would like to specify your own color\n% \\definecolor{awesome}{HTML}{CA63A8}\n\n% Colors for text\n% Uncomment if you would like to specify your own color\n% \\definecolor{darktext}{HTML}{414141}\n% \\definecolor{text}{HTML}{333333}\n% \\definecolor{graytext}{HTML}{5D5D5D}\n% \\definecolor{lighttext}{HTML}{999999}\n% \\definecolor{sectiondivider}{HTML}{5D5D5D}\n\n% Set false if you don\'t want to highlight section with awesome color\n\\setbool{acvSectionColorHighlight}{true}\n\n% If you would like to change the social information separator from a pipe (|) to something else\n\\renewcommand{\\acvHeaderSocialSep}{\\quad\\textbar\\quad}\n\n%-------------------------------------------------------------------------------\n%\tPERSONAL INFORMATION\n%\tComment any of the lines below if they are not required\n%-------------------------------------------------------------------------------\n% Available options: circle|rectangle,edge/noedge,left/right\n% \\photo{./examples/profile.png}\n\\name{'+string['first']+'}{'+string['last']+'}\n\\position{'+string['position']+'}\n\\address{'+string['address']+'}\n\n\\mobile{'+string['mobile']+'}\n\\email{'+string['email']+'}\n%\\dateofbirth{January 1st, 1970}\n%\\homepage{www.posquit0.com}\n\\github{'+string['github']+'}\n\\linkedin{'+string['linkedin']+'}\n% \\gitlab{gitlab-id}\n% \\stackoverflow{SO-id}{SO-name}\n% \\twitter{@twit}\n% \\skype{skype-id}\n% \\reddit{reddit-id}\n% \\medium{medium-id}\n% \\kaggle{kaggle-id}\n% \\hackerrank{hackerrank-id}\n% \\googlescholar{googlescholar-id}{name-to-display}\n%% \\firstname and \\lastname will be used\n% \\googlescholar{googlescholar-id}{}\n% \\extrainfo{extra information}\n\n%\\quote{``Be the change that you want to see in the world."}\n\n\n%-------------------------------------------------------------------------------\n\\begin{document}\n\n% Print the header with above personal information\n% Give optional argument to change alignment(C: center, L: left, R: right)\n\\makecvheader\n\n% Print the footer with 3 arguments(<left>, <center>, <right>)\n% Leave any of these blank if they are not needed\n\\makecvfooter\n  {\\today}\n  {'+string['first']+' '+string['last']+'~~~Â·~~~Curriculum Vitae}\n  {\\thepage\\ / \\pageref*{LastPage}}\n\n\n%-------------------------------------------------------------------------------\n%\tCV/RESUME CONTENT\n%\tEach section is imported separately, open each file in turn to modify content\n%-------------------------------------------------------------------------------'
        for section_name, section_data in cv.items():
            string += '\n'+AwesomeCVTexGenerator.generate_section(section_name, section_data)
        string += '\n\n\n%-------------------------------------------------------------------------------\n\\end{document}\n'

        with open('tex/'+args.cv_blueprint_json_filepath.replace('.json', '.tex'), 'w') as cv_file:
            cv_file.write(string)
    
    def generate_section(section_name, section_data):
        string = '%-------------------------------------------------------------------------------\n%\tSECTION TITLE\n%-------------------------------------------------------------------------------\n\\cvsection{'+section_name+'}\n\n\n'

        if section_data['type'] == 'cvskills':
            if 'preamble' in section_data: string += '%-------------------------------------------------------------------------------\n%\tPREAMBLE\n%-------------------------------------------------------------------------------\n'+section_data['preamble']+'\n'
            if section_data['items']:
                string += '%-------------------------------------------------------------------------------\n%\tCONTENT\n%-------------------------------------------------------------------------------\n\\begin{cvskills}\n\n'
                for item in section_data['items']:
                    string += AwesomeCVTexGenerator.generate_item(section_data['type'], item)
                string += '\\end{cvskills}\n'
        elif section_data['type'] == 'cventries':
            if section_data['items']:
                string += '%-------------------------------------------------------------------------------\n%\tCONTENT\n%-------------------------------------------------------------------------------\n\\begin{cventries}\n\n'
                for item in section_data['items']:
                    string += AwesomeCVTexGenerator.generate_item(section_data['type'], item)
                string += '\\end{cventries}\n'
        elif section_data['type'] == 'cvhonors':
            if section_data['items']:
                for item in section_data['items']:
                    string += AwesomeCVTexGenerator.generate_item(section_data['type'], item)
        
        return string
    
    def generate_item(section_type, item):
        string = ''
        
        if section_type == 'cvskills':
            string += '%---------------------------------------------------------\n  \\cvskill\n    {'+list(item.keys())[0]+'}\n    {'+str(item[list(item.keys())[0]])+'}\n\n%---------------------------------------------------------\n'
        elif section_type == 'cventries':
            string += '%---------------------------------------------------------\n  \\cventry\n    {'+item['botleft']+'}\n    {'+item['topleft']+'}\n    {'+item['topright']+'}\n    {'+item['botright']+'}\n    {'
            if item['content']:
                string += '\n      \\begin{cvitems}'
                for point in item['content']:
                    string += AwesomeCVTexGenerator.generate_point(section_type, point)
                string += '\n      \\end{cvitems}\n    '
            string += '}\n\n'
        elif section_type == 'cvhonors':
            if '' not in item.keys(): string += '%-------------------------------------------------------------------------------\n%\tSUBSECTION TITLE\n%-------------------------------------------------------------------------------\n\\cvsubsection{'+list(item.keys())[0]+'}\n\n\n'
            if list(item.values())[0]:
                string += '%-------------------------------------------------------------------------------\n%\tCONTENT\n%-------------------------------------------------------------------------------\n\\begin{cvhonors}\n\n'
                for point in list(item.values())[0]:
                    string += AwesomeCVTexGenerator.generate_point(section_type, point)
                string += '\\end{cvhonors}\n'
        
        return string
    
    def generate_point(section_type, point):
        if section_type == 'cventries':
            return '\n        \\item {'+point+'}'
        elif section_type == 'cvhonors':
            return '%---------------------------------------------------------\n  \\cvhonor\n    {'+point['left']+'}\n    {'+point['right']+'}\n    {'+point['rightmost']+'}\n    {'+point['leftmost']+'}\n\n'