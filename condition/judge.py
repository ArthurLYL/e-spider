# def turned_exist(url):
#     """
#     check whether turned page exists
#     :param url:
#     :return: this page exists => 1 else => 0
#     """
#     soup = get_content(url)
#     soup.find_all(class_='itg gltc')
#     if soup.find_all(class_='itg gltc')[0].td.text != 'No unfiltered results in this page range. You either requested an invalid page or used too aggressive filters.':
#         return 1
#     else:
#         return 0
#
#
# def search_exist(url):
#     """
#     check whether search content is valid
#     :param url:
#     :return: 1 => valid, 0=> invalid
#     """
#     soup = get_content(url)
#     if soup is False:
#         return 1
#     elif soup.find('p', style='text-align:center; font-style:italic; margin-bottom:10px') is None:
#         return True
#     else:
#         return False