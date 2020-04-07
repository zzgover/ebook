class PageInfo(object):
    '''
    :param current_page 当前页
    :param all_count 数据库中记录的总个数
    :param per_page 每页显示多少条记录个数
    :param base_url 当前分页对象所处的 url 地址
    :param show_page 每页上显示前后共多少个页码，默认 11 个
    :param pk 用于接收商品列表页的 url 地址里 category_pk
    '''

    def __init__(self, current_page, all_count, per_page, base_url, pk=1, show_page=11):

        try:

            self.current_page = int(current_page)
        except Exception as e:
            self.current_page = 1  # 如果传递过来的 page 不是数字，则将当前页设置为第 1 页
        self.per_page = per_page
        a, b = divmod(all_count, per_page)
        if b:
            a = a + 1
        self.all_pager = a  # 总页数
        self.show_page = show_page
        self.base_url = base_url
        self.pk = pk

    def start(self):

        return (self.current_page - 1) * self.per_page

    def end(self):

        return self.current_page * self.per_page

    # 这个函数用于在模板上生成每一页中应该显示的 11 个页码
    def pager(self):

        page_list = []
        begin = 0
        stop = 0
        half = int((self.show_page - 1) / 2)
        if self.all_pager < self.show_page:

            begin = 1
            stop = self.all_pager + 1
        else:
            if self.current_page <= 5:
                begin = 1
                stop = self.show_page + 1
            else:
                if self.current_page + half > self.all_pager:
                    begin = self.all_pager - self.show_page + 1
                    stop = self.all_pager + 1
                else:
                    begin = self.current_page - half
                    stop = self.current_page + half + 1
        if self.current_page <= 1:
            prev = '<li><a href="#">上一页</a></li>'
        else:
            prev = '<li><a href="%s%s/%s/">上一页</a></li>' % (self.base_url, self.pk, self.current_page - 1)
        page_list.append(prev)
        for i in range(begin, stop):
            if i == self.current_page:
                temp = '<li class="active"><a href="%s%s/%s/">%s</a></li>' % (self.base_url, self.pk, i, i,)
            else:
                temp = '<li><a href="%s%s/%s/">%s</a></li>' % (self.base_url, self.pk, i, i,)
            page_list.append(temp)  # 添加列表里的元素

        if self.current_page >= self.all_pager:
            nex = '<li><a href="#">下一页</a></li>'
        else:
            nex = '<li><a href="%s%s/%s/">下一页</a></li>' % (self.base_url, self.pk, self.current_page + 1)
        page_list.append(nex)
        return ''.join(page_list)  # href="%s?page=%s,返回的结果是要填到页面中的字符串，用此方法拼接成字符串
