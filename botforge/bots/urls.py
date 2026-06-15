from django.urls import path

from . import views


urlpatterns = [

    path('',views.bot_list,name='bot_list'),
    path('create/',views.bot_create,name='bot_create'),
    path("chat_bot/<int:bot_id>/",views.bot_workspace,name="bot_workspace"),
    path("train/<int:bot_id>/",views.train_bot,name="train_bot"),
    path("recrawl/<int:bot_id>/",views.recrawl_bot,name="recrawl_bot"),
    path("knowledge/add/<int:bot_id>/",views.add_knowledge,name="add_knowledge"),
    path("knowledge/delete/<int:id>/",views.delete_knowledge,name="delete_knowledge"),
    path("knowledge/update/<int:id>/",views.update_knowledge,name="update_knowledge"),
    path("test-chat/<int:bot_id>/",views.test_chat_api,name="test_chat_api"),
    path("save-widget-settings/<int:bot_id>/",views.save_widget_settings,name="save_widget_settings"),
    path("install-bot/<int:bot_id>/",views.install_bot,name="install_bot"),
    path("widget/chat/<uuid:widget_key>/",views.widget_chat_api,name="widget_chat_api"),
    path("widget/config/<uuid:widget_key>/",views.widget_config,name="widget_config"),
    path("conversation/<int:session_id>/",views.conversation_detail_ajax,name="conversation_detail_ajax"),
    path("clear-chat-history/<int:bot_id>/",views.clear_chat_history,name="clear_chat_history"),
    path("delete-knowledge-base/<int:bot_id>/",views.delete_knowledge_base,name="delete_knowledge_base"),
    path("delete-chatbot/<int:bot_id>/",views.delete_chatbot,name="delete_chatbot"),
    path("documention",views.documention,name="documention"),

]