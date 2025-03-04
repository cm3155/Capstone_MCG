API_KEY = 'a827471cc41eb76abd6b4ef9c704e86bd503aa3d76a4c951c08fdb6dc0a5abbe'

from sec_api import ExtractorApi

extractorApi = ExtractorApi(API_KEY)

def pprint(text, line_length=100):
  words = text.split(' ')
  lines = []
  current_line = ''
  for word in words:
      if len(current_line + ' ' + word) <= line_length:
          current_line += ' ' + word
      else:
          lines.append(current_line.strip())
          current_line = word
  if current_line:
      lines.append(current_line.strip())
  print(''.join(lines))

filing_10_k_url = 'https://www.sec.gov/Archives/edgar/data/0000019617/000001961725000270/jpm-20241231.htm'


sections = extractorApi.get_section(filing_10_k_url, '15', "text")


print('Extracted Item 1 (Text)')
print('-----------------------')
pprint(sections[0:1500])
print('... cut for brevity')
print('-----------------------')