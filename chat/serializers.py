from rest_framework import serializers
from .models import Messages, ChatSession, Feedback


class ChatSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatSession
        fields = ['session_id', 'customer_id', 'status', 'started_at', 'ended_at']
        read_only_fields = ['session_id','customer_id', 'started_at']

class MessagesSerializer(serializers.ModelSerializer):
    session_id = serializers.PrimaryKeyRelatedField(queryset=ChatSession.objects.all())
    customer_id = serializers.PrimaryKeyRelatedField(source='session_id.customer_id', read_only=True)

    class Meta:
        model = Messages
        fields = ['id', 'session_id', 'customer_id','message', 'type', 'response', 'confidence', 'source', 'timestamp']
        read_only_fileds=['id', 'timestamp' , 'response' , 'confidence']


class FeedbackSerializer(serializers.ModelSerializer):
    message_id = serializers.PrimaryKeyRelatedField(queryset=Messages.objects.all())

    class Meta:
        model = Feedback
        fields = ['id', 'message_id', 'helpful', 'feedback', 'timestamp']
