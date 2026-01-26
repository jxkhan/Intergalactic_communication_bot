import uuid, re
from rest_framework.viewsets import ModelViewSet
from .models import Messages, ChatSession, Feedback
from .serializers import ChatSessionSerializer, MessagesSerializer, FeedbackSerializer
from rest_framework.response import Response
from rest_framework.permissions import  AllowAny, IsAdminUser
from rest_framework.decorators import action
from rest_framework import status
from django.shortcuts import get_object_or_404
from faq.models import FAQ
from rest_framework.views import APIView
from django.db.models import Count


class ChatSessionViewSet(ModelViewSet):
    serializer_class = ChatSessionSerializer
    queryset = ChatSession.objects.all()
    permission_classes = [AllowAny]



    def create(self, request, *args, **kwargs):
        session_id= str(uuid.uuid4())
        user=request.user if request.user.is_authenticated else None

        chat_session = ChatSession.objects.create(
            session_id=session_id,
            customer_id=user
        )
        Messages.objects.create(
            session_id=chat_session,
            message="Welcome to Intergalactic Chat! How can I help you today?",
            type="Bot",
            source="Bot"
        )
        serializer = self.get_serializer(chat_session)
        return Response(serializer.data, status= status.HTTP_201_CREATED)
        
    

class MessagesViewSet(ModelViewSet):
    serializer_class= MessagesSerializer
    queryset = Messages.objects.all()
    permission_classes = [AllowAny]
            
    def get_queryset(self):
        session_uuid = self.request.query_params.get('session_id')
        print("Querying messages for session:", session_uuid)
        qs = Messages.objects.filter(session_id__session_id=session_uuid)
        print("Found messages:", qs.count())
        return qs.order_by('timestamp')
        # return Messages.objects.none()

    def create(self, request, *args, **kwargs):
        session_uuid = request.data.get('session_id')
        message_text = request.data.get('message')

        if not session_uuid or not message_text:
            return Response(
                {"error": "session_id and message are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        session = get_object_or_404(ChatSession, session_id=session_uuid)

        if session.status != 'active':
            return Response(
                {"error": "Cannot add messages to a completed session."},
                status=status.HTTP_400_BAD_REQUEST
            )

        customer_message = Messages.objects.create(
            session_id=session,
            message=message_text,
            type='customer',
            source='customer'
        )

        words = set(re.findall(r'\w+', message_text.lower()))

        best_faq = None
        best_match_count = 0

        for f in FAQ.objects.all():
            faq_keywords = set(k.lower() for k in f.keywords)
            matching_keywords = words & faq_keywords
            match_count = len(matching_keywords)

            if match_count >= 2 and match_count > best_match_count:
                best_faq = f
                best_match_count = match_count

        if best_faq:
            bot_text = best_faq.answer
            confidence = best_match_count / len(best_faq.keywords)
            source = 'faq'
        else:
            bot_text = "I'm sorry, I don't have an answer for that right now."
            confidence = 0.0
            source = 'fallback'

        bot_message = Messages.objects.create(
            session_id=session,
            message=bot_text,
            type='bot',
            response=bot_text,
            confidence=confidence,
            source=source
        )

        return Response({
            "session_id": session.session_id,
            "customer_message": customer_message.message,
            "bot_response": bot_message.message,
            "confidence": confidence,
            "source": source
        }, status=status.HTTP_201_CREATED)
    
            

class FeedbackViewSet(ModelViewSet):
    queryset= Feedback.objects.all()
    serializer_class= FeedbackSerializer
    permission_classes= [AllowAny]
    http_method_names=['post','get']

    def create(self, request, *args, **kwargs):
        print("Requset data:", request.data)
        serializer= self.get_serializer(data = request.data)    
        serializer.is_valid(raise_exception=True)
        print("Validated data:", serializer.validated_data)
        feedback=self.perform_create(serializer)
        print("Saved feedback:", feedback)
        feedback = serializer.save() 
        return Response(FeedbackSerializer(feedback).data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        return Feedback.objects.all()
    


class PopularQuestionsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        faqs = FAQ.objects.order_by('-helpful_votes')[:10]

        data = [
            {
                "id": faq.id,
                "question": faq.question,
                "helpful_votes": faq.helpful_votes
            }
            for faq in faqs
        ]

        return Response(data)
    
class UnmatchedQuestionsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        unmatched = Messages.objects.filter(source='fallback').values('message').annotate(
            count=Count('id')
        ).order_by('-count')[:10]

        data = [
            {"question": q['message'], "occurrences": q['count']}
            for q in unmatched
        ]
        return Response(data)




