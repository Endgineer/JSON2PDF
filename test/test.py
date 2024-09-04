import subprocess
import unittest
import os

EXP_LOG_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'expected_logs')
GEN_LOG_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'generated_logs')
IMG_JSN_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'image_jsons')



class LogEqualityTest(unittest.TestCase):
  def __init__(self, filename):
    super(LogEqualityTest, self).__init__()
    self.filebasename = os.path.splitext(os.path.basename(filename))[0]
  
  def assertGeneratedIsExpected(self):
    expected_log_filepath = os.path.join(EXP_LOG_DIR, f'{self.filebasename}.debug.log')
    generated_log_filepath = os.path.join(GEN_LOG_DIR, f'{self.filebasename}.debug.log')

    if not os.path.exists(expected_log_filepath):
      raise AssertionError(f'{self.filebasename}.json - Expected log file {expected_log_filepath} not found.')
    with open(generated_log_filepath, 'r', encoding='utf-8') as generated_log_file:
      with open(expected_log_filepath, 'r', encoding='utf-8') as expected_log_file:
        self.assertEqual(generated_log_file.read(), expected_log_file.read(), f'{self.filebasename}.json - Log files not identical.')
  
  def runTest(self):
    subprocess.call(f'python ../../src/main.py -cv "../image_jsons/{self.filebasename}" --anonymize --bolded --debug --interrupt', cwd=GEN_LOG_DIR)
    self.assertGeneratedIsExpected()



def test_all_suite() -> unittest.TestSuite:
  suite = unittest.TestSuite()
  if not os.path.isdir(GEN_LOG_DIR):
    os.mkdir(GEN_LOG_DIR)

  for filename in os.listdir(IMG_JSN_DIR):
    if os.path.isfile(os.path.join(IMG_JSN_DIR, filename)):
      suite.addTest(LogEqualityTest(filename))
  
  return suite



if __name__ == '__main__':
  unittest.TextTestRunner().run(test_all_suite())