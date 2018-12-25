from helpers import fetch_paragraphs


url = "https://www.businessinsider.com/marine-corps-generals-leaving-trump-administration-mattis-resigns-2018-12"
paragraphs = fetch_paragraphs(url)
for text, is_h in paragraphs:
    print('---')
    print(text)
