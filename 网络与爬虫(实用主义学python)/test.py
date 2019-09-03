from lxml.html import fromstring

with open('C:\\Users\\shine小小昱\\Desktop\\test_page.txt', 'r', encoding='utf-8') as f:
    page_source = f.read()
    tree = fromstring(page_source)
    urls = tree.xpath('//table[@class=\'tbimg\']/tbody/tr/td[2]/a[1]')
    for url in urls:
        print(url)