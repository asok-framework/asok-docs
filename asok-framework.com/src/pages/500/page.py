from asok import Request

SSG = True


def render(request: Request):
    request.status_code(500)
    return request.stream("page.asok")