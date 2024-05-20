from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def render(context, snippet):
    t = template.Template(snippet, name='rendered-snippet')
    return t.render(context=context)
