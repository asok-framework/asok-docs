from asok import Request

SSG = True


def render(request: Request):
    return request.stream("page.asok")
