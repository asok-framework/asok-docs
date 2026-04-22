from asok import Request


def render(request: Request):
    return request.stream("page.html")