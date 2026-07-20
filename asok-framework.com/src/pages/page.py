from asok import Request

#SSG = True

def render(request: Request):
    request.meta.title = "Asok : Ultra-Lightweight & Reactive Python Framework"
    return request.stream("page.asok")