import aiohttp
from aiohttp import web
from lxml import html
from settings import HABR_URL_HOST, HABR_LINKS, SIX_WORDS_RE


class IndexView(web.View):
    def update_link(self, link):
        found = list(filter(lambda item: link.startswith(item), HABR_LINKS))

        if len(found) == 1:
            new_link = link[len(found[0]):]
            return new_link if len(link) > 0 else '/'

        return link

    def process_html(self, html_content):
        tree = html.fromstring(html_content)

        if tree is not None:
            body = tree.find('body')

            if body is not None:
                self.process_body_content(body)
                return html.tostring(tree, encoding='utf-8')

        return html_content

    def process_body_content(self, body):
        for element in body.iter():
            if element.tag in ['style', 'script']:
                continue

            if element.tag == 'a':
                link = element.attrib.get('href')

                if link:
                    element.attrib['href'] = self.update_link(link)

            if element.text is not None:
                element.text = SIX_WORDS_RE.sub(r'\1\2™', element.text)

            if element.tail is not None:
                element.tail = SIX_WORDS_RE.sub(r'\1\2™', element.tail)


    async def get(self):
        url = self.request.match_info.get('url', '')
        proxy_url = HABR_URL_HOST + url

        async with aiohttp.ClientSession() as session:
            async with session.get(proxy_url) as r:
                bytes_html = await r.read()

                if r.headers.get('Content-Type', '').startswith('text/html'):
                    processed_html = self.process_html(bytes_html)
                    return web.Response(body=processed_html, content_type='text/html')

                else:
                    return web.Response(body=bytes_html)