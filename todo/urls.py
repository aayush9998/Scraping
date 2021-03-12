from django.urls import path
from . import views


urlpatterns=[
    path('', views.index, name='index' ),
    path('search', views.search, name='search' ),
    path('scrape', views.scrape, name='scrape'),
    path('add_item', views.add_item, name='add_item'),
    path('sastodeal_item', views.sastodeal_item, name='sastodeal_item')

    # path('delete_todo/<int:item_id>', views.delete_item, name='delete_item')
]