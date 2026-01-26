from rest_framework.routers import DefaultRouter
from .viewset import ChatSessionViewSet, MessagesViewSet, FeedbackViewSet, PopularQuestionsView , UnmatchedQuestionsView
from django.urls import path , include 



router = DefaultRouter()
router.register(r'chat-sessions', ChatSessionViewSet, basename='chat-session')
router.register(r'messages', MessagesViewSet)
router.register(r'feedback' , FeedbackViewSet, basename='feedback')


urlpatterns = [
    path('', include(router.urls)),
    path('analytics/popularquestions', PopularQuestionsView.as_view()),
    path('analytics/unmatchquestions', UnmatchedQuestionsView.as_view())
]


