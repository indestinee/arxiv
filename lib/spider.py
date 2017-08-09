import re, requests

def reach_url(url):
    return requests.get(url, headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    })

def extract_data(content, a = '', b = '', words = ''):
    pattern = re.compile((r'%s(.*?)%s' % (a, b)) if len(words) == 0 else words, re.S)
    return pattern.findall(content)

def get_information(url):
    response = reach_url(url)
    data = extract_data(response.text, 'Title:</span>\\n', '</h1>')
    title = data[0]
            
    data = extract_data(response.text, '<span class="descriptor">Abstract:</span> ', '\\n</blockquote>')
    abstract = data[0].replace('\n', ' ')

    data = extract_data(response.text, '<span class="descriptor">Authors:</span>', '</div>')
    data = extract_data(data[0], words = '<a href=(.*?)>(.*?)</a>')
    author = []
    for each in data:
        author.append(each[-1])

    data = extract_data(response.text, '<div class="submission-history">', '</div>')
    data = extract_data(data[0], words = '<b>(.*?)</b> (.*?)\(')
    last_submission = data[-1][-1]
    last_submission = last_submission[:-2]
    last_submission = time.strptime(last_submission, '%a, %d %b %Y %H:%M:%S %Z')

    data = extract_data(response.text, '<td class="tablecell comments">', '</td>')
    comments = data[0] if len(data) > 0 else ''

    return {'title': title, 'abstract': abstract, 'author': author, 'last_submission': last_submission, 'comments': comments}


def fetch(arxiv_id):
    information = get_information(preffix + 'abs/' + arxiv_id)
    return information

def update(data_base, update_all):
    data_arxiv = data_base['arxiv_id']
    url = 'https://arxiv.org/list/cs.CV/recent'
    response = reach_url(url)
    data = extract_data(response.text, '<a href="/list/cs.CV/pastweek\?show=', '">all</a>')
    assert len(data) == 2 and data[0] == data[1], data
    num = int(data[0])
    remain = (num - len(data_base)) if not update_all else num
    count = 0
    if remain == 0:
        return count, remain
    url = 'https://arxiv.org/list/cs.CV/pastweek?show=%d' % remain
    response = reach_url(url)
    data = extract_data(response.text, words = '<dt>(.*?)</dt>(.*?)<dd>(.*?)</dd>')
    cnt = 0
    for each in data:
        cnt += 1
        try:
            data_0 = extract_data(each[0], '<a href="/abs/', '" title="Abstract">')
            arxiv_id = data_0[0]

            if arxiv_id not in data_arxiv:
                data_arxiv[arxiv_id] = {}

            if 'succeed' in data_arxiv[arxiv_id] and data_arxiv[arxiv_id]['succeed']:
                continue

            information = fetch(arxiv_id)
            information.update({'arxiv_id': arxiv_id, 'download': False, 'succeed': True, 'pdf': preffix + 'pdf/' + arxiv_id})
            data_arxiv[information['arxiv_id']] = information.copy()

            tt = time.strftime('%Y-%m-%d', information['last_submission'])
            if tt not in data_base['time']:
                data_base['time'][tt] = []
            data_base['time'][tt].append(arxiv_id)
            data_base['title'][information['title']] = arxiv_id
            for each in information['author']:
                if each not in data_base['author']:
                    data_base['author'][each] = []
                data_base['author'][each].append(arxiv_id)
            count += 1
        except:
            data_arxiv[arxiv_id]['succeed'] = False
            print('Fail to reach arxiv_id %s' % arxiv_id)
        print('Done [%d/%d]..' % (cnt, remain))
    return count, remain




