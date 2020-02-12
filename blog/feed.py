from django.contrib.syndication.views import Feed
from .models import Post


class AllPostsRssFeed(Feed):
    title = 'Zheng Tingyu'
    link = '/'
    description = 'Zheng tingyu 全部文章'

    def items(self):
        return Post.object.all()

    def item_title(self, item):
        return "[%s]%s" % (item.category, item.title)

    def item_description(self, item):
        return item.body_html
