from django.db import models
from faq.models import Customer



class ChatSession(models.Model):
    
    session_id = models.CharField(max_length=255, unique=True)
    customer_id = models.ForeignKey(Customer, on_delete=models.SET_NULL, related_name='chat_sessions', null=True, blank=True)
    status = models.CharField(max_length=50, choices=[('active', 'Active'), ('completed', 'Completed'),('transferred', 'Transferred')], default='active')
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Session {self.session_id} - {self.status}"
    

class Messages(models.Model):
    session_id = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    message=models.TextField()
    type=models.CharField(max_length=50, choices=[('customer', 'Customer'), ('bot', 'Bot'), ('agent', 'Agent')])
    response=models.TextField(null=True, blank=True)
    confidence=models.FloatField(null=True, blank=True)
    source=models.CharField(max_length=50 , choices=[('faq', 'FAQ'), ('agent', 'Agent'), ('fallback', 'Fallback')], null=False, blank=False)
    timestamp=models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Message {self.id} in Session {self.session_id.session_id}"



class Feedback(models.Model):
    message_id=models.ForeignKey(Messages, on_delete=models.CASCADE, related_name='feedbacks')
    helpful=models.BooleanField()
    feedback= models.TextField(null=True, blank=True)
    timestamp=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback {self.id} for Message {self.message_id.id}"