
import urllib.request
import chardet
import ssl
import pymysql
import re
import matplotlib.pyplot as plt
import time

from pyecharts import Bar
from pyquery import PyQuery as pq

# 通过指定的字符集对页面进行解码(不是每个网站都将字符集设置为utf-8)
def decode_page(page_bytes, charset='utf-8'):
    page_html = None
    try:
        page_html = page_bytes.decode(charset)

    except UnicodeDecodeError:
        pass
        # logging.error('Decode:', error)
    return page_html

# 获取页面的HTML代码(通过递归实现指定次数的重试操作)
def get_page_html(seed_url, header_url, retry_times=3, charset='utf-8'):
    page_html = None
    try:
        page_bytes = urllib.request.urlopen(urllib.request.Request(seed_url, headers = header_url)).read()
        page_html = decode_page(page_bytes, charset)
    except URLError:
        # logging.error('URL:', error)
        if retry_times > 0:
            return get_page_html(seed_url, header_url, retry_times=retry_times - 1, charset=charset)
    return page_html

# 获得页面的编码格式
def get_page_encode(seed_url, header_url):
    page_encode = None
    try:
        page_bytes = urllib.request.urlopen(urllib.request.Request(seed_url, headers=header_url)).read()
        #file_store('./baidupan.html', page_bytes)
        page_encode = chardet.detect(page_bytes)
    except EncodeError:
        pass
    if page_encode.get('encoding') != 'utf-8':
        return -1
    return page_encode.get('encoding')

# open file and save HTML for debug
def file_store(file_path, page_bytes):
    fhandle = open(file_path, "wb")
    fhandle.write(page_bytes)
    fhandle.close()

# analyze data with pyquery
def collect_data(page_html, start_index):
    html_query = pq(page_html)
    query_index = start_index
    while (1):
        href_list = html_query('a').eq(query_index).attr('href')
        book_name = pq(html_query('a').eq(query_index)).find('.hanghang-list-name').text()
        re_book_name = re.sub(r'\'+', ' ', book_name)
        final_book_name = re.sub(r'\"+', ' ', re_book_name)
        book_download_num = pq(html_query('a').eq(query_index)).find('.hanghang-list-num').text()
        book_author = pq(html_query('a').eq(query_index)).find('.hanghang-list-zuozhe').text()
        re_book_author = re.sub(r'\'+', ' ', book_author)
        final_book_author = re.sub(r'\"+', ' ', re_book_author)
        if book_name:
            query_index = query_index + 1
            print ("book_name: %s ,book num: %s ,book_author: %s, book link: %s" %(book_name, book_download_num, book_author, href_list))
            store_data(final_book_name, final_book_author, book_download_num, href_list)
        else:
            break

# store data into pymysql
def store_data(g_name, g_author, g_downloadcount, g_link):
    db = pymysql.connect(host = "localhost", user = "root", password = "123456",  database= "testdb", charset="utf8")
    cursor = db.cursor()
    insert_sql = """INSERT INTO ireadlist (name, author, downloadcount, link) \
            VALUES ("%s", "%s", "%s", "%s")""" % (g_name, g_author, g_downloadcount, g_link)
    update_sql = """UPDATE ireadlist SET downloadcount="%s" WHERE (name="%s")""" % (g_downloadcount, g_name)
    try:
        # 执行sql语句
        cursor.execute(insert_sql)
        # 提交到数据库执行
        db.commit()
    except:
        # 如果发生错误则回滚
        db.rollback()
        # update sql
        cursor.execute(update_sql)
        db.commit()
    db.close()

def get_whole_page_url(header_url, header):
    list_url = []
    page_number = 1
    while(1):
        test_url = header_url + 'index.php/index/' + str(page_number) + '.html'
        test_header = header
        try:
            test_html = urllib.request.urlopen(urllib.request.Request(test_url, headers=test_header)).read()
            test_query = pq(test_html)
            test_name = pq(test_query('a').eq(7)).find('.hanghang-list-name').text()
            if test_name:
                page_number = page_number + 1
                list_url.append(test_url)
                #print ("list name ", test_name)
                #time.sleep(2)
            else:
                break
        except URLError:
            break
    return list_url

# select mysql data to chart
def select_data_from_mysql():
    select_db = pymysql.connect(host="localhost", user="root", password="123456", database="testdb", charset="utf8")
    select_cursor = select_db.cursor()
    select_sql = "SELECT * FROM ireadlist WHERE downloadcount > 6000"
    try:
        # 执行sql语句
        select_cursor.execute(select_sql)
        select_results = select_cursor.fetchall()
    except:
        print ("select error msg")
    select_db.close()
    return select_results

# draw data matplot
def draw_data_matplot(select_results):
    list_name = []
    list_count = []
    for select_list in select_results:
        list_name.append(select_list[0])
        list_count.append(int(select_list[2]))
        #print ("select name: %s, select count: %d" % (select_list[0], int(select_list[2])))
    #plt.plot(list_count, 'bs')
    quick_sort(list_count, 0, len(list_count)-1)
    for i in list_count:
        print ("quick sort: ", i)
    plt.plot(list_count, 'bs')
    plt.show()

# draw data echart
def draw_data_echart(select_results):
    list_name = []
    list_count = []
    for select_list in select_results:
        list_name.append(select_list[0])
        list_count.append(int(select_list[2]))
        #print ("select name: %s, select count: %d" % (select_list[0], int(select_list[2])))
    bar = Bar("read weekly", "download count")
    bar.use_theme('light')
    bar.add("book download count", list_name, list_count, is_more_utils = True, is_label_show = True, is_datazoom_show = True)
    bar.render("downloadcount.html")

def get_final_url(select_results):
    for final_list in select_results:
        final_url = 'http://www.ireadweek.com' + final_list[3]
        final_page_encode = get_page_encode(final_url, header)
        final_page_html = get_page_html(final_url, header, 3, final_page_encode)
        final_html_query = pq(final_page_html)
        final_link_list = final_html_query('.hanghang-shu-content-btn')
        download_link = final_link_list.find('a').attr('href')
        write_file = final_list[0] + ' --- ' + download_link
        file_handle = open("./panlink.txt", 'a+')
        file_handle.write(write_file)
        file_handle.write('\n')
        file_handle.close()

def sub_sort(array,low,high):
    key = array[low]
    while low < high:
        while low < high and array[high] >= key:
            high -= 1
        while low < high and array[high] < key:
            array[low] = array[high]
            low += 1
            array[high] = array[low]
    array[low] = key
    return low

def quick_sort(array,low,high):
    if low < high:
        key_index = sub_sort(array,low,high)
        quick_sort(array,low,key_index)
        quick_sort(array,key_index+1,high)


if __name__ == "__main__":
    #url = 'https://www.671cf.com/htm/index.htm'
    #url = 'https://www.gavbus.com/'
    url = 'http://www.ireadweek.com/'
    header = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36'}
    ssl._create_default_https_context = ssl._create_unverified_context

    # get all page url list
    search_list = []
    search_list = get_whole_page_url(url, header)
    cycle_flag = 0
    for url_unit in search_list:
        print ("---------url-------", url_unit)
        if cycle_flag:
            queue_num = 7
        else:
            cycle_flag = 1
            queue_num = 9
        # get page encode
        page_encode = get_page_encode(url_unit, header)
        # get page html
        page_html = get_page_html(url_unit, header, 3, page_encode)
        # get html data
        collect_data(page_html, queue_num)

    results = select_data_from_mysql()
    #draw_data_matplot(results)
    get_final_url(results)
    draw_data_echart(results)

    '''
    # test mysql update
    #test_url = 'http://www.ireadweek.com/index.php/index/16.html'
    #test_url = 'http://pan.baidu.com/s/1qY91y0G'
    test_url = 'http://www.ireadweek.com/index.php/bookInfo/11043.html'

    page_encode = get_page_encode(test_url, header)
    page_html = get_page_html(test_url, header, 3, page_encode)
    #collect_data(page_html, 9)
    html_query = pq(page_html)
    link_list = html_query('.hanghang-shu-content-btn')
    print (link_list.find('a').attr('href'))
    print (type(link_list.find('a').attr('href')))
    '''




