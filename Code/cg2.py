import urllib.request, re

def crawler(keyword, pages = 1):
    pattern1 = re.compile(r'href = "([^ ]*)"')
    pattern2 = re.compile(r'href="([^ ]*)"')
    links = []
    target = urllib.request.quote(keyword)
    opener = urllib.request.build_opener()
    opener.addheaders = [
                        ('Connection', 'Keep-Alive'),
                        ('Content-Type', 'text/html;charset=utf-8'),
                        ('Referer', 'https://www.baidu.com'),
                        ('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36 Edg/79.0.309.51')
                        ]
    for page in range(pages):
        url = f'https://www.baidu.com/s?wd={target}&pn={page}&oq={target}&ie=utf-8&usm=2&rsv_idx=1&rsv_pq=e4f7528300143ded&rsv_t=f9e5fE0a3Gy7yaLQX6JFJhnR6I1jYnAfL2t5SCcGSoJSAr3LogHutYZxP%2FY'
        data = opener.open(url)
##        print('当前网址：' + data.geturl())
        code = data.read().decode('utf-8')
        links.extend(link_filter(pattern1.findall(code)))
        links.extend(link_filter(pattern2.findall(code)))
    return links

def link_filter(links):
    return list(filter(lambda s: s.startswith('http'), links))

links = crawler('美女')
for link in links:
    print(link)
