from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
def user_profile(request):
    user_initials = request.user.first_name[0] \
          if request.user.first_name else ''

    user_initials += request.user.last_name[0] \
          if request.user.last_name else user_initials

    context =  {'user_initials': user_initials}
    return render(request, 'user_accounts/user_profile.html', context)


def user_info_form(request):
    return render(request, 'user_accounts/user_info_form.html', {})