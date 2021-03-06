#!/usr/bin/python
# -*- coding: utf8 -*-

# Done
from crawler.parser import *


class GiaoDucThoiDaiVnParser(SubBaseParser):
    def __init__(self):
        # Bắt buộc phải gọi đầu tiên
        super().__init__()

        # Chứa tên miền không có http://www dùng cho parser tự động nhận dạng
        self._domain = 'giaoducthoidai.vn'

        # Chứa tên miền đầy đủ và không có / cuối cùng dùng để tìm url tuyệt đối
        self._full_domain = 'http://giaoducthoidai.vn'

        # Custom các regex dùng để parse một số trang dùng subdomain (ví dụ: *.vnexpress.net)
        # self._domain_regex =

        # Biến vars có thể được sử dụng cho nhiều mục đích khác
        # self._vars[''] =

        # THAY ĐỔI CÁC HÀM TRONG VARS ĐỂ THAY ĐỔI CÁC THAM SỐ CỦA HÀM CHA

        # Tìm danh sách các chuyên mục con trong chuyên mục cha dùng cho trường hợp duyệt đệ qui
        # Gán bằng con trỏ hàm hoặc biểu thức lambda
        # self._vars['get_child_category_section_func'] =

        # Tìm URL của trang kế
        # Gán bằng con trỏ hàm hoặc biểu thức lambda
        # Lưu ý hàm gồm 2 tham số (html, url)
        def get_next_url_func(html, url):
            a_tag = html.find('a', attrs={'id': 'ctl00_mainContent_ContentList1_pager_nextControl', 'href': True})
            return None if a_tag is None else a_tag.get('href')

        self._vars['get_next_url_func'] = get_next_url_func

        # Trả về danh sách các urls của các bài viết có trong trang
        # Nếu có thể lấy được thời gian trực tiếp luôn thì mỗi phần tử trong danh sách phải là (url, time)
        # Gán bằng con trỏ hàm hoặc biểu thức lambda
        def get_post_urls_func(html):
            urls = []

            # Child posts
            posts = html.find_all('article', class_='story')
            for post in posts:
                a_tag = post.find('a', attrs={'href': True})
                if a_tag is not None:
                    urls.append(a_tag.get('href'))

            return urls

        self._vars['get_post_urls_func'] = get_post_urls_func

        # Sử dụng trong trường hợp không thể lấy được thời gian trực tiếp trên trang
        # Hàm này sẽ trả về thẻ chứa thời gian trong html của bài viết
        # Gán bằng con trỏ hàm hoặc biểu thức lambda
        def get_time_tag_func(html):
            div_tag = html.find('div', class_='toolbar')
            if div_tag is None:
                matcher = regex.search(r'<div class="time-social clearfix">\s*<time>([^>]+) GMT\+7<\/time>', str(html),
                                       regex.IGNORECASE)
                if matcher is None:
                    return None
                return matcher.group(1)
            return div_tag.find('span', class_='time')

        self._vars['get_time_tag_func'] = get_time_tag_func

        # Hàm này sẽ chuyển chuỗi thời gian có được ở hàm trên về đối tượng datetime (phụ thuộc time format mỗi trang)
        # Gán bằng con trỏ hàm hoặc biểu thức lambda
        def get_datetime_func(string):
            string = string.split(',')[1]
            return datetime.strptime(string.strip(), '%d/%m/%Y %H:%M')

        self._vars['get_datetime_func'] = get_datetime_func

    # Sử dụng khi muốn xóa gì đó trên trang chứa danh sách các bài viết
    def _pre_process(self, html):
        # Chỉ định main content
        section_tag = html.find('section', class_='browsing-focus')
        if section_tag is None:
            return None
        section_tag = section_tag.find('div', class_='pull-left')
        if section_tag is None:
            return None
        return super()._pre_process(section_tag)
