from bs4 import BeautifulSoup

import pprint

pp = pprint.PrettyPrinter(indent=4, width=180)


def get_page_num(soup: BeautifulSoup):
    page = soup.find('div', class_='pg')
    label = page.find('span')['title']
    page_num = int(label.split(' ')[1])
    return page_num


def gen_post(soup: BeautifulSoup):
    table = soup.find('table', summary='forum_0')
    tbodys = table.find_all('tbody')
    for tbody in tbodys:
        a = tbody.th.find('a', class_='s xst')
        if a:
            yield a['href']


def gen_post_page(soup: BeautifulSoup, url):
    div = soup.find('div', class_='pg')
    if not div:
        return None
    url_split = url.split('-')
    title = div.label.span['title']
    page_num = int(title.split(' ')[1])
    for i in range(2, page_num + 1):
        url_split[2] = str(i)
        yield '-'.join(url_split)


def gen_item(soup: BeautifulSoup):
    try:
        postlist = soup.find('div', id='postlist', recursive=True)
        title = postlist.find('span', id='thread_subject').text
        ids = postlist.find_all('div', class_=False, id=True, recursive=False)
    except IndexError as err:
        pass
    else:
        for id in ids:
            result = {}
            info = id.find('tr', class_='floor-border')
            try:
                usr_info = info.find('td', class_='pls')
                usr_basic_info = usr_info.find_all('dl')[1].find_all('dd')
            except IndexError:
                continue
            result['postnum'] = usr_basic_info[0].text
            result['regstime'] = usr_basic_info[3].text
            result['location'] = usr_basic_info[4].text
            result['user_id'] = usr_info.find('div', class_='authi').a.text

            comment_info = info.find('td', class_='plc')
            result['sequence'] = comment_info.find('em', id=False).text.rstrip('#')
            result['title'] = title if result['sequence'] == '楼主' else ''
            result['created_time'] = comment_info.find('em', id=True).text.lstrip('发表于 ')

            content = ''
            content_info = comment_info.find('td', class_='t_f')
            if content_info:
                content = content_info.text.lstrip()
                if content_info.div:
                    content = content.lstrip('\n{}'.format(content_info.div.text))

            result['content'] = content

            reply_info = id.find('a', class_='toggle-replay')
            result['num_reply'] = '0'
            if reply_info:
                result['num_reply'] = reply_info['data-count']
            yield result


if __name__ == '__main__':
    with open('luntan.html', 'rb') as file:
        soup = BeautifulSoup(file.read(), 'lxml')

    get_page_num(soup)
    gen_post(soup)
    with open('post_no_user.html', 'rb') as file:
        soup = BeautifulSoup(file.read(), 'lxml')

    gen_item(soup)
