from aiohttp import web

import pymorphy2


MORPH = pymorphy2.MorphAnalyzer()


async def inf(request: web.Request) -> web.Response:
    """
    Возвращается список начальных форм,
    отсортированный по убыванию вероятности "правильности".
    """
    word = request.query['word']
    forms = []
    for parsed in MORPH.parse(word):
        form = parsed.normal_form
        if form not in forms:
            forms.append(form)
    return web.json_response(forms)


async def root(req: web.Request) -> web.Response:
    return web.json_response([])


class Application(web.Application):
    def __init__(self):
        super().__init__()

        self.router.add_get('/inf', inf)
        self.router.add_get('/', root)


def main():
    app = Application()
    web.run_app(app)


if __name__ == '__main__':
    main()
