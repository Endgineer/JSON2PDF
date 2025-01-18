import typing
import os

from compiler.routines.awesome_cv import *
from parser.constants.grammar import *
from compiler.logger.PhaseLogger import Document

class Flags:
  anonymize: bool
  filepath: str
  filename: str
  name: str
  position: str
  address: str
  mobile: str
  email: str
  linkedin: str
  github: str
  color: str
  website: str
  footer: str
  header: str
  spaced: bool
  darken: bool
  bolded: bool
  lettertitle: str
  letterclosing: str

  def __init__(self, args: typing.Sequence[str]):
    self.filepath = args.path
    self.filename = os.path.basename(self.filepath)
    self.anonymize = None in [args.name,  args.titles, args.address, args.mobile, args.email] or args.anon
    self.position = ''.join(['\\position{', '{\\enskip\\cdotp\\enskip}'.join( args.titles), '}']) if  args.titles else '\\position{Awesome Position}'
    self.color = args.color
    self.spaced = args.spaced
    self.darken = args.darken
    self.bolded = args.bold
    
    if self.anonymize:
      footer_name = f'First Last'
      self.name = f'\\name{{First}}{{Last}}'
      self.address = f'\\address{{City, Region}}'
      self.mobile = f'\\mobile{{000-000-0000}}'
      self.email = f'\\email{{first.last@email.com}}'
      self.linkedin = f'\\linkedin{{first-last}}' if args.linkedin else '% \\linkedin{}'
      self.github = f'\\github{{first-last}}' if args.github else '% \\github{}'
      self.website = f'\\homepage{{https://portfolio-website.io/}}' if args.website else '% \\homepage{}'
    else:
      footer_name = f'{args.name.split()[0]} {args.name.split()[1]}'
      self.name = f'\\name{{{args.name.split()[0]}}}{{{args.name.split()[1]}}}'
      self.address = f'\\address{{{args.address}}}'
      self.mobile = f'\\mobile{{{args.mobile}}}'
      self.email = f'\\email{{{args.email}}}'
      self.linkedin = f'\\linkedin{{{args.linkedin}}}' if args.linkedin else '% \\linkedin{}'
      self.github = f'\\github{{{args.github}}}' if args.github else '% \\github{}'
      self.website = f'\\homepage{{{args.website}}}' if args.website else '% \\homepage{}'
    
    self.footer = f'\\makecvfooter\n  {{\\today}}\n  {{{footer_name}{{\\enskip\\cdotp\\enskip}}DOCTYPE}}\n  {{\\thepage\\ / \\pageref*{{LastPage}}}}' if args.footer else '%\\makecvfooter\n  % {\\today}\n  % {Document Type}\n  % {\\thepage\\ / \\pageref*{LastPage}}'
    self.header = f'\\makecvheader' if args.header else f'%\\makecvheader'
  
  def init_letter(self, letter_company: str, letter_position: str, letter_reference: str, letter_opening: str, letter_closing: str, letter_attachments: str) -> None:
    attachments = f'\\letterenclosure[Attached]{{{letter_attachments}}}' if letter_attachments is not None else f'% \\letterenclosure[Attached]{{}}'

    self.letter_info = (
      f'%-------------------------------------------------------------------------------\n'
      f'%\tLETTER INFORMATION\n'
      f'%\tAll of the below lines must be filled out\n'
      f'%-------------------------------------------------------------------------------\n'
      f'% The company being applied to\n'
      f'\\recipient{{{letter_company}}}{{{letter_position}\\\\{letter_reference}}}\n'
      f'% The date on the letter, default is the date of compilation\n'
      f'\\letterdate{{\\today}}\n'
      f'% The title of the letter\n'
      f'% \\lettertitle{{}}\n'
      f'% How the letter is opened\n'
      f'\\letteropening{{{letter_opening},}}\n'
      f'% How the letter is closed\n'
      f'\\letterclosing{{{letter_closing},}}\n'
      f'% Any enclosures with the letter\n'
      f'{attachments}\n'
      f'\n'
      f'\n'
    )
  
  def wrap(self, tex: str, doctype: Document) -> str:
    if doctype == Document.CL:
      lettertitle = f'% Print the title with above letter information\n\\makelettertitle'
      letterclosing = f'% Print the signature and enclosures with above letter information\n\\makeletterclosing'
      letter_info = (
        f'%-------------------------------------------------------------------------------\n'
        f'%\tLETTER INFORMATION\n'
        f'%\tAll of the below lines must be filled out\n'
        f'%-------------------------------------------------------------------------------\n'
        f'% SOMETHING WENT WRONG WITH SYNTHESIZER GENERATOR\n'
        f'\n'
        f'\n'
      )
    else:
      lettertitle = f''
      letterclosing = f''
      letter_info = f''

    return (
      f'%!TEX TS-program = xelatex\n'
      f'%!TEX encoding = UTF-8 Unicode\n'
      f'% Awesome CV LaTeX Template for CV/Resume\n'
      f'%\n'
      f'% This template has been downloaded from:\n'
      f'% https://github.com/posquit0/Awesome-CV\n'
      f'%\n'
      f'% Author:\n'
      f'% Claud D. Park <posquit0.bj@gmail.com>\n'
      f'% http://www.posquit0.com\n'
      f'%\n'
      f'% Template license:\n'
      f'% CC BY-SA 4.0 (https://creativecommons.org/licenses/by-sa/4.0/)\n'
      f'%\n'
      f'\n'
      f'\n'
      f'%-------------------------------------------------------------------------------\n'
      f'% CONFIGURATIONS\n'
      f'%-------------------------------------------------------------------------------\n'
      f'% A4 paper size by default, use \'letterpaper\' for US letter\n'
      f'\\documentclass[11pt, a4paper]{{article}}\n'
      f'\n'
      f'\makeatletter\n'
      f'{load_class(self.spaced, self.darken)}\n'
      f'\makeatother\n'
      f'\n'
      f'% Configure page margins with geometry\n'
      f'\\geometry{{left=1.4cm, top=.8cm, right=1.4cm, bottom=1.8cm, footskip=.5cm}}\n'
      f'\n% Color for highlights\n'
      f'% Awesome Colors: awesome-emerald, awesome-skyblue, awesome-red, awesome-pink, awesome-orange\n'
      f'%                 awesome-nephritis, awesome-concrete, awesome-darknight\n'
      f'\\colorlet{{awesome}}{{awesome-red}}\n'
      f'% Uncomment if you would like to specify your own color\n'
      f'\\definecolor{{awesome}}{{HTML}}{{{self.color}}}\n'
      f'\n'
      f'% Colors for text\n'
      f'% Uncomment if you would like to specify your own color\n'
      f'% \\definecolor{{darktext}}{{HTML}}{{414141}}\n'
      f'% \\definecolor{{text}}{{HTML}}{{333333}}\n'
      f'% \\definecolor{{graytext}}{{HTML}}{{5D5D5D}}\n'
      f'% \\definecolor{{lighttext}}{{HTML}}{{999999}}\n'
      f'% \\definecolor{{sectiondivider}}{{HTML}}{{5D5D5D}}\n'
      f'\n'
      f'% Set false if you don\'t want to highlight section with awesome color\n'
      f'\\setbool{{acvSectionColorHighlight}}{{true}}\n'
      f'\n'
      f'% If you would like to change the social information separator from a pipe (|) to something else\n'
      f'\\renewcommand{{\\acvHeaderSocialSep}}{{\\quad\\textbar\\quad}}\n'
      f'\n'
      f'\n'
      f'%-------------------------------------------------------------------------------\n'
      f'%\tPERSONAL INFORMATION\n'
      f'%\tComment any of the lines below if they are not required\n'
      f'%-------------------------------------------------------------------------------\n'
      f'% Available options: circle|rectangle,edge/noedge,left/right\n'
      f'% \\photo{{./examples/profile.png}}\n'
      f'{self.name}\n'
      f'{self.position}\n'
      f'{self.address}\n'
      f'\n'
      f'{self.mobile}\n'
      f'{self.email}\n'
      f'% \\dateofbirth{{January 1st, 1970}}\n'
      f'{self.website}\n'
      f'{self.github}\n'
      f'{self.linkedin}\n'
      f'% \\gitlab{{gitlab-id}}\n'
      f'% \\stackoverflow{{SO-id}}{{SO-name}}\n'
      f'% \\twitter{{@twit}}\n'
      f'% \\skype{{skype-id}}\n'
      f'% \\reddit{{reddit-id}}\n'
      f'% \\medium{{medium-id}}\n'
      f'% \\kaggle{{kaggle-id}}\n'
      f'% \\hackerrank{{hackerrank-id}}\n'
      f'% \\googlescholar{{googlescholar-id}}{{name-to-display}}\n'
      f'%% \\firstname and \\lastname will be used\n'
      f'% \\googlescholar{{googlescholar-id}}{{}}\n'
      f'% \\extrainfo{{extra information}}\n'
      f'\n'
      f'% \\quote{{``Be the change that you want to see in the world."}}\n'
      f'\n'
      f'\n'
      f'{letter_info}'
      f'%-------------------------------------------------------------------------------\n'
      f'\\begin{{document}}\n'
      f'\n'
      f'% Print the header with above personal information\n'
      f'% Give optional argument to change alignment(C: center, L: left, R: right)\n'
      f'{self.header}\n'
      f'\n'
      f'% Print the footer with 3 arguments(<left>, <center>, <right>)\n'
      f'% Leave any of these blank if they are not needed\n'
      f'{self.footer.replace("DOCTYPE", "Curriculum Vitae" if doctype == Document.CV else "Cover Letter", 1)}\n'
      f'\n'
      f'{lettertitle}\n'
      f'\n'
      f'\n'
      f'%>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n'
      f'%\tBEGIN CONTENT\n'
      f'%>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n'
      f'\n'
      f'\n'
      f'{tex}\n'
      f'%<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n'
      f'%\tEND CONTENT\n'
      f'%<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n'
      f'{letterclosing}\n'
      f'\n'
      f'\n'
      f'\\end{{document}}\n'
      f'%-------------------------------------------------------------------------------\n'
    )
