from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages  
from .models import Message
from .forms import MessageForm, MessageEditForm

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login
from .models import Message

def register_view(request):
    if request.method == 'POST':
        name = request.POST.get('username', '').strip()
        
        if name:

            user, created = User.objects.get_or_create(username=name)
            
            login(request, user)
            return redirect('chat')
            
    return render(request, 'register.html')


def chat_view(request):
    user = request.user  
    
    
    if not user.is_authenticated:
        return redirect('register')

    
    queryset = Message.objects.filter(is_archived=False)
    date_filter = request.GET.get('date')
    if date_filter:
        queryset = queryset.filter(timestamp__date=date_filter)
    messages_list = queryset.order_by('-timestamp')

    archived_messages = Message.objects.filter(user=user, is_archived=True).order_by('-timestamp')

    if request.method == 'POST':

        if 'edit_message_id' in request.POST:
            message_id = request.POST.get('edit_message_id')
            message = get_object_or_404(Message, id=message_id)
            if message.user == user:
                form = MessageEditForm(request.POST, instance=message)
                if form.is_valid():
                    form.save()
            
                    messages.success(request, "Сообщение успешно изменено!")
                    return redirect('chat')

        elif 'delete_message_id' in request.POST:
            message_id = request.POST.get('delete_message_id')
            message = get_object_or_404(Message, id=message_id)
            if message.user == user:
                message.is_archived = True  
                message.save()
                
                messages.warning(request, "Сообщение перемещено в архив.")
                return redirect('chat')

        elif 'restore_message_id' in request.POST:
            message_id = request.POST.get('restore_message_id')
            message = get_object_or_404(Message, id=message_id)
            if message.user == user:
                message.is_archived = False  
                message.save()
                
                messages.success(request, "Сообщение успешно восстановлено!")
                return redirect('chat')

        else:
            form = MessageForm(request.POST)
            if form.is_valid():
                message = form.save(commit=False)
                message.user = user
                message.save()
                return redirect('chat')
    else:
        form = MessageForm()

    return render(request, 'chat.html', {
        'messages': messages_list,
        'form': form,
        'archived_messages': archived_messages,  
        'user': user
    }) 
