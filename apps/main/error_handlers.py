from django.utils.http import quote
from django.http import HttpResponseNotFound, HttpResponseServerError
from django.template import loader
from django.views.decorators.csrf import requires_csrf_token


@requires_csrf_token
def page_not_found(request, exception):
    template_name = 'errors/404.html'
    template = loader.get_template(template_name)
    exception_repr = exception.__class__.__name__
    try:
        message = exception.args[0]
    except (AttributeError, IndexError):
        pass
    else:
        if isinstance(message, str):
            exception_repr = message
    context = {
        'request_path': quote(request.path),
        'exception': exception_repr,
        'user': request.user,
    }
    return HttpResponseNotFound(template.render(context))


@requires_csrf_token
def server_error(request, *args, **kwargs):
    template_name = 'errors/500.html'
    template = loader.get_template(template_name)
    context = {
        'user': request.user,
    }
    return HttpResponseServerError(template.render(context))
