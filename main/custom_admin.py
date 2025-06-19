# main/custom_admin.py
from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import redirect, get_object_or_404
from django.urls import path
from django.contrib import messages
from .models import Application, ConnectMessage

class CustomAdminSite(admin.AdminSite):
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('main/application/<int:pk>/process/', self.process_application, name='process_application'),
            path('main/connectmessage/<int:pk>/mark_read/', self.mark_message_read, name='mark_message_read'),
        ]
        return custom_urls + urls

    @staff_member_required
    def process_application(self, request, pk):
        app = get_object_or_404(Application, pk=pk)
        app.is_processed = True
        app.save()
        messages.success(request, f'Application from {app.name} marked as processed')
        return redirect('admin:main_application_changelist')

    @staff_member_required
    def mark_message_read(self, request, pk):
        msg = get_object_or_404(ConnectMessage, pk=pk)
        msg.is_read = True
        msg.save()
        messages.success(request, f'Message from {msg.name} marked as read')
        return redirect('admin:main_connectmessage_changelist')

custom_admin_site = CustomAdminSite(name='custom_admin')
