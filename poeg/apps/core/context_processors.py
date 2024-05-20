from allauth.account.forms import LoginForm


def core(request):
    ctx = {}
    if request.user.is_anonymous:
        ctx['login_form'] = LoginForm()
    return ctx
