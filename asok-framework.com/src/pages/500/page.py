from asok import Request


def render(request: Request):
    request.status_code(500)
    return request.stream("page.html")