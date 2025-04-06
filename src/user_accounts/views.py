from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.db import DatabaseError


@login_required(login_url='login')
def user_profile(request):
    user_initials = request.user.first_name[0] \
          if request.user.first_name else ''

    user_initials += request.user.last_name[0] \
          if request.user.last_name else user_initials

    context =  {'user_initials': user_initials}
    return render(request, 'user_accounts/user_profile.html', context)


@login_required(login_url='login')
def user_info_form(request):
    return render(request, 'user_accounts/user_info_form.html', {})


@login_required(login_url='login')
@require_POST
def update_user_info(request):
    user = request.user
    first_name = request.POST.get("first_name", "").strip()
    last_name = request.POST.get("last_name", "").strip()

    try:
        if len(first_name) > 20 or len(last_name) > 20:
            messages.error(request, 'Bad Reqest')
            return redirect('profile')
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        return redirect('profile')

    except DatabaseError as e:
        return redirect('profile')
