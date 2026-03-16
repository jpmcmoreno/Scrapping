import scrapy
from scrapy_playwright.page import PageMethod
from news_scraper.items import NewsItem
import re
from datetime import datetime, timedelta
from urllib.parse import urlparse, urljoin
 
# === LIBRERÍA OPCIONAL ===
try:
    import trafilatura
    TRAFILATURA_DISPONIBLE = True
except ImportError:
    trafilatura = None
    TRAFILATURA_DISPONIBLE = False
 
class NewsSpider(scrapy.Spider):
    name = 'news'
   
    # === CONFIGURACIÓN DE FECHAS (OPCIONAL) ===
    USAR_FILTRO_FECHAS = True
    DIAS_ATRAS = 3
   
    # === CONFIGURACIÓN DE PAGINACIÓN ===
    MAX_PAGINAS = 3
    DETENER_SI_ARTICULOS_VIEJOS = 10
   
    AUTO_DETECT_JAVASCRIPT = True
    USAR_PLAYWRIGHT_PARA_TODOS = False
 
    endpoints = {
#        "Trome": [
#            "https://trome.com/ultimas-noticias/",
#            "https://trome.com/actualidad/",
#            "https://trome.com/actualidad/politica/",
#            "https://trome.com/actualidad/policiales/",
#            "https://trome.com/actualidad/nacional/"
#
#        ],
       
 
        "Radio Nacional": [
            "https://www.radionacional.gob.pe/noticias/ultimas-noticias"
        ],
 
        "Diario El Pueblo": [
            "https://diarioelpueblo.com.pe/category/noticias/local/",
            "https://diarioelpueblo.com.pe/category/noticias/regional/",
            "https://diarioelpueblo.com.pe/category/noticias/nacional/",
            "https://diarioelpueblo.com.pe/category/actualidad/",
            "https://diarioelpueblo.com.pe/category/policiales/",
            "https://diarioelpueblo.com.pe/category/politica/"
 
        ],
       
        "Diario Viral": [
            "https://diarioviral.pe/actualidad/",
            "https://diarioviral.pe/arequipa/",
            "https://diarioviral.pe/politica/"
            ],
 
                "Diario del cusco": [
            "https://diariodelcusco.pe/category/actualidad/",
            "https://diariodelcusco.pe/category/regionales/",
            "https://diariodelcusco.pe/category/tendencias/peru/"
        ],
 
     "Andina_Peru": [
            "https://andina.pe/agencia/loultimo",
            "https://andina.pe/agencia/seccion-politica-17.aspx",
            "https://andina.pe/agencia/seccion-locales-3.aspx",
            "https://andina.pe/agencia/seccion-regionales-4.aspx"
        ],
           
          "Mundo": [
            "https://ansabrasil.com.br/brasil/noticias/mundo/index.shtml"
        ],
       
        "Semana": [
            "https://www.semana.com/nacion/",
            "https://www.semana.com/politica/",
            "https://www.semana.com/economia/",
            "https://www.semana.com/nacion/bogota/",
            "https://www.semana.com/nacion/medellin/",
            "https://www.semana.com/nacion/cali/",
            "https://www.semana.com/nacion/barranquilla/",
            "https://www.semana.com/nacion/cucuta/,"
            "https://www.semana.com/nacion/pereira/",
            "https://www.semana.com/nacion/bucaramanga/",
            "https://www.semana.com/nacion/cartagena/"
        ],
 
          "Confilegal": [
            "https://confilegal.com/mundo-judicial/",
            "https://confilegal.com/tribunales/",
            "https://confilegal.com/politica/"
        ],
       
        "Que pasa Venezuela": [
            "https://quepasaenvenezuela.org/category/sucesos/",
            "https://quepasaenvenezuela.org/category/nacionales/",
            "https://quepasaenvenezuela.org/category/politica/",
            "https://quepasaenvenezuela.org/category/internacionales/"
        ],
       
        "Andina_Peru": [
            "https://andina.pe/agencia/loultimo",
            "https://andina.pe/agencia/seccion-politica-17.aspx",
            "https://andina.pe/agencia/seccion-locales-3.aspx",
            "https://andina.pe/agencia/seccion-regionales-4.aspx"
        ],
       
       
        "El Periodico": [
            "https://www.elperiodico.com/es/ultimas-noticias/",
            "https://www.elperiodico.com/es/internacional/",
            "https://www.elperiodico.com/es/economia/",
            "https://www.elperiodico.com/es/politica/"
        ],
       
        "Diario El Pueblo": [
            "https://diarioelpueblo.com.pe/category/noticias/local/",
            "https://diarioelpueblo.com.pe/category/noticias/regional/",
            "https://diarioelpueblo.com.pe/category/noticias/nacional/",
            "https://diarioelpueblo.com.pe/category/actualidad/"
        ],
       
        "Antilavado de dinero": [
            "https://antilavadodedinero.net/news/",
            "https://antilavadodedinero.net/casos/"
        ],
       
        "TV Peru": [
            "https://www.tvperu.gob.pe/noticias/ultimas-noticias",
            "https://www.tvperu.gob.pe/noticias/seccion/politica",
            "https://www.tvperu.gob.pe/noticias/seccion/locales",
            "https://www.tvperu.gob.pe/noticias/seccion/nacionales"
        ],
       
        "Radio Madre de Dios": [
            "https://noticias.madrededios.com/blog/section/local/",
            "https://noticias.madrededios.com/blog/section/nacional-internacional/"
        ],
       
        "Reina de la selva": [
            "https://reinadelaselva.pe/noticias/"
        ],
       
        "Frontera digital": [
            "https://fronteradigital.com.ve/categoria/Sucesos"
        ],
       
        "La verdad de vargas": [
            "https://laverdaddevargas.com/category/sucesos/"
        ],
       
        "NTN 24": [
            "https://www.ntn24.com/noticias-judicial"
        ],
       
        "EL Periodico v": [
            "https://elperiodicodemonagas.com.ve/sucesos/"
        ],
       
        "KOB 4": [
            "https://www.kob.com/new-mexico-news/"
        ],
       
       
        "Cronica viva": [
            "https://www.cronicaviva.com.pe/categoria/regional/"
        ],
       
        "HUANCA YORK": [
            "https://hytimes.pe/policiales/"
        ],
       
        "La Rotativa": [
            "https://larotativa.pe/ultimas-noticias/"]
}
 
 
    JAVASCRIPT_BUTTON_PATTERNS = [
        '__doPostBack',
        'WebForm_DoPostBackWithOptions',
        'WebForm_PostBackOptions',
    ]
 
    PAGINATION_SELECTORS = {
         # ─── Links estándar "siguiente" ───────────────────────────────────────
        'normal_links': [
            # rel="next" (el más semántico y confiable)
            'a[rel="next"]',
            'link[rel="next"]',
 
            # Clases comunes en inglés
            'a.next',
            'a.next-page',
            'a.nextpage',
            'a.next_page',
            'li.next > a',
            'li.next-page > a',
            '.pagination-next a',
            '.pagination-next > a',
            '.pager-next a',
            '.pager__next a',
            'button.next',
            'button[class*="next"]',
 
            # Clases en español / portugués
            'a.siguiente',
            'a.proxima',
            'a.proxima-pagina',
            'li.siguiente > a',
 
            # Clases genéricas con "next" en el nombre
            'a[class*="next"]',
            'a[id*="next"]',
            'li[class*="next"] a',
            'div[class*="next"] a',
 
            # Texto visible del enlace
            '.pagination a:contains("Next")',
            '.pagination a:contains("Siguiente")',
            '.pagination a:contains("Próxima")',
            '.pagination a:contains("Próximo")',
            '.pagination a:contains("›")',
            '.pagination a:contains(">")',
            '.pagination a:contains(">>")',
            '.pagination a:contains("→")',
            '.pagination a:contains("»")',
 
            # Frameworks populares (Bootstrap, WP, Materialize…)
            'nav.pagination a[href*="page"]',
            '.wp-pagenavi a.nextpostslink',
            '.nav-links a.next',
            '.posts-navigation a[rel="next"]',
            '.entry-navigation a[rel="next"]',
            'a.page-link[aria-label*="Next"]',
            'a.page-link[aria-label*="next"]',
            'li.page-item:last-child a.page-link',  # Bootstrap último item
 
            # ARIA accesibilidad
            'a[aria-label="Next"]',
            'a[aria-label="Next page"]',
            'a[aria-label="next"]',
            'a[aria-label*="siguiente"]',
            'a[aria-label*="próxima"]',
            '[role="navigation"] a[href*="page"]:last-of-type',
 
            # Iconos dentro de links (Font Awesome, Material Icons…)
            'a:has(i.fa-chevron-right)',
            'a:has(i.fa-angle-right)',
            'a:has(i.fa-arrow-right)',
            'a:has(.material-icons)',
        ],
 
        # ─── Botones JavaScript / PostBack ───────────────────────────────────
        'javascript_buttons': [
            # ASP.NET WebForms
            'a[id*="lnkbtnPaging"]',
            'a[href*="__doPostBack"]',
            'a[onclick*="__doPostBack"]',
            'input[onclick*="__doPostBack"]',
            'button[onclick*="__doPostBack"]',
 
            # onclick genérico con "next" o "page"
            'a[onclick*="next"]',
            'button[onclick*="next"]',
            'a[onclick*="goToPage"]',
            'button[onclick*="goToPage"]',
            'a[onclick*="loadPage"]',
            'button[onclick*="loadPage"]',
 
            # data-* attributes (SPA / React / Vue / Angular)
            '[data-page="next"]',
            '[data-action="next"]',
            '[data-direction="next"]',
            '[data-testid*="next"]',
            '[data-cy*="next"]',
        ],
 
        # ─── URL con parámetros de página ─────────────────────────────────────
        'url_based': [
            'a[href*="page="]',
            'a[href*="/page/"]',
            'a[href*="?p="]',
            'a[href*="&page="]',
            'a[href*="paged="]',
            'a[href*="pg="]',
            'a[href*="pagina="]',
            'a[href*="pageno="]',
            'a[href*="pagenum="]',
            'a[href*="offset="]',
            'a[href*="start="]',
        ],
 
        # ─── Botones "Load More" / scroll infinito ────────────────────────────
        'load_more_buttons': [
            'button:contains("Load More")',
            'button:contains("Ver más")',
            'button:contains("Cargar más")',
            'button:contains("Show More")',
            'button:contains("More")',
            'a:contains("Load More")',
            'a:contains("Ver más")',
            '[class*="load-more"]',
            '[class*="loadmore"]',
            '[id*="load-more"]',
            '[id*="loadMore"]',
            '[data-action="load-more"]',
        ],
 
        # ─── Paginación numérica (último número visible) ──────────────────────
        'numbered_pagination': [
            '.pagination li:last-child a',
            '.pagination .active + li a',  # número después del activo
            '.pager li:last-child a',
            'ul.page-numbers li:last-child a',
            'ol.pagination li:last-child a',
        ],
    }
 
    SITIOS_JAVASCRIPT_CONOCIDOS = {
        'andina.pe',
        'trome.com',
        'www.trome.com',
    }
 
    DOMAIN_CONFIGS = {
        'notifalcon.com': {
            'listing_selectors': [
                'article h2 a::attr(href)',
                'article h3 a::attr(href)',
                '.post h2 a::attr(href)',
                'a[href*="/2026/"]::attr(href)',
            ],
            'content_selectors': [
                'article p::text',
                '.entry-content p::text',
                '.post-content p::text',
            ],
        },
 
        'diarioviral.pe': {
        'pagination': 'url_pattern',  # indica que usa /{num}/ al final
        },
 
        'diarioelpueblo.com.pe': {
            'listing_selectors': [
                'h4.news-title a::attr(href)',
                '.archive-section-content a::attr(href)',
                ],
        }
    }
 
    custom_settings = {
        'DOWNLOAD_HANDLERS': {
            "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
            "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
        },
        'TWISTED_REACTOR': "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
        'PLAYWRIGHT_BROWSER_TYPE': 'chromium',
        'PLAYWRIGHT_LAUNCH_OPTIONS': {
            'headless': True,
            'timeout': 30000,
        },
        'PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT': 30000,
        'PLAYWRIGHT_CONTEXTS': {
            "default": {
                "viewport": {"width": 1920, "height": 1080},
                "ignore_https_errors": True,
            },
        },
        'PLAYWRIGHT_ABORT_REQUEST': lambda request: (
            request.resource_type == "media"
            or request.resource_type == "font"
        ),
    }
 
    def __init__(self, *args, **kwargs):
        super(NewsSpider, self).__init__(*args, **kwargs)
        self.page_counter = {}
        self.old_articles_counter = {}
        self.sitios_con_javascript = set(self.SITIOS_JAVASCRIPT_CONOCIDOS)
        self.sitios_sin_javascript = set()
 
        if self.USAR_FILTRO_FECHAS:
            self.fecha_limite = datetime.now() - timedelta(days=self.DIAS_ATRAS)
            self.logger.info(f"📅 Filtrando noticias de los últimos {self.DIAS_ATRAS} días")
 
        if self.AUTO_DETECT_JAVASCRIPT:
            self.logger.info("🤖 Detección automática de JavaScript ACTIVADA")
 
    def start_requests(self):
        self.logger.info(f"🚀 Iniciando scraping a las {datetime.now().strftime('%H:%M:%S')}")
 
        for site_name, urls in self.endpoints.items():
            for url in urls:
                key = f"{site_name}_{url}"
                self.page_counter[key] = 1
                self.old_articles_counter[key] = 0
 
                dominio = urlparse(url).netloc
                usar_playwright = dominio in self.sitios_con_javascript
 
                if usar_playwright:
                    self.logger.info(f"🌐 [PLAYWRIGHT] {dominio}")
 
                yield scrapy.Request(
                    url,
                    callback=self.parse_listing,
                    errback=self.errback_httpbin,
                    meta={
                        'site_name': site_name,
                        'page_num': 1,
                        'playwright': usar_playwright,
                        'playwright_include_page': usar_playwright,
                        'playwright_page_methods': [
                            PageMethod('wait_for_selector', 'a', timeout=10000),
                            ] if usar_playwright else []
                    }
                )
 
    def parse_listing(self, response):
        site_name = response.meta.get('site_name', 'Desconocido')
        page_num = response.meta.get('page_num', 1)
        dominio = urlparse(response.url).netloc
 
        self.logger.info(f"🔍 [{site_name}] Página {page_num} ({response.url})")
 
        domain_config = self.DOMAIN_CONFIGS.get(dominio, {})
        listing_selectors = domain_config.get('listing_selectors', [])
 
        all_selectors = listing_selectors + [
            'a[href*="/noticia"]::attr(href)',
            'a[href*="/noticias"]::attr(href)',
            'a[href*="/news/"]::attr(href)',
            'article a::attr(href)',
            '.post a::attr(href)',
            '.entry a::attr(href)',
            'h2 a::attr(href)',
            'h3 a::attr(href)',
            '.article-title a::attr(href)',
        ]
 
        enlaces = []
        for selector in all_selectors:
            found = response.css(selector).getall()
            enlaces.extend(found)
 
        enlaces_unicos = []
        seen = set()
 
        for link in enlaces:
            full_url = urljoin(response.url, link.strip())
            if not full_url.startswith('http'):
                continue
            if full_url in seen:
                continue
            if any(x in full_url.lower() for x in ['#', 'javascript:', 'mailto:', '.jpg', '.png', '.pdf']):
                continue
            if '/category/' in full_url or '/tag/' in full_url or '/autor/' in full_url:
                continue
 
            link_domain = urlparse(full_url).netloc
            if dominio not in link_domain:
                continue
 
            # ✅ Si la URL tiene patrón de fecha, es casi seguro una noticia
            if re.search(r'/\d{4}/\d{2}/\d{2}/', full_url):
                seen.add(full_url)
                enlaces_unicos.append(full_url)
                continue
 
            seen.add(full_url)
            enlaces_unicos.append(full_url)
 
        if enlaces_unicos:
            self.logger.info(f"✅ [{site_name}] {len(enlaces_unicos)} artículos encontrados")
        else:
            self.logger.warning(f"⚠️ NO se encontraron enlaces en {response.url}")
 
        for link in enlaces_unicos:
            yield scrapy.Request(
                link,
                callback=self.parse_article,
                errback=self.errback_httpbin,
                meta={
                    'site_name': site_name,
                    'link': link,
                    'dominio': dominio,
                    'page_num': page_num
                }
            )
 
        url_base = response.url.split('?')[0].split('/page/')[0]
        url_base = re.sub(r'/\d+/?$', '/', url_base)
        key = f"{site_name}_{url_base}"
 
        if self.page_counter.get(key, 1) >= self.MAX_PAGINAS:
            self.logger.info(f"🏁 [{site_name}] Límite de {self.MAX_PAGINAS} páginas alcanzado")
            return
 
        if self.old_articles_counter.get(key, 0) >= self.DETENER_SI_ARTICULOS_VIEJOS:
            self.logger.info(f"🏁 [{site_name}] Muchos artículos viejos detectados")
            return
 
        next_page_info = self.find_next_page(response, dominio)
 
        if next_page_info:
            self.page_counter[key] = self.page_counter.get(key, 1) + 1
 
            if next_page_info['is_javascript']:
                self.sitios_con_javascript.add(dominio)
                selector_boton = next_page_info['button_selector']
                self.logger.info(f"🔄 [{site_name}] JavaScript detectado - Usando Playwright")
 
                yield scrapy.Request(
                    response.url,
                    callback=self.parse_listing,
                    errback=self.errback_httpbin,
                    meta={
                        'site_name': site_name,
                        'page_num': page_num + 1,
                        'playwright': True,
                        'playwright_include_page': True,
                        'playwright_page_methods': [
                            PageMethod('click', selector_boton),
                            PageMethod('wait_for_load_state', 'networkidle'),
                        ]
                    },
                    dont_filter=True
                )
            else:
                next_url = next_page_info['url']
                self.logger.info(f"➡️ [{site_name}] Siguiente: {next_url}")
 
                yield scrapy.Request(
                    url=next_url,
                    callback=self.parse_listing,
                    errback=self.errback_httpbin,
                    meta={
                        'site_name': site_name,
                        'page_num': page_num + 1,
                        'playwright': False,
                    },
                    dont_filter=True
                )
        else:
            self.logger.info(f"🏁 [{site_name}] No hay más páginas")
 
    def find_next_page(self, response, dominio):
        for selector in self.PAGINATION_SELECTORS['normal_links']:
            elementos = response.css(selector)
            if not elementos:
                continue
            href = elementos[0].css('::attr(href)').get()
            if href and 'javascript:' not in href.lower():
                next_url = urljoin(f"https://{dominio}/", href)  # ← fix urljoin
                return {'url': next_url, 'is_javascript': False, 'button_selector': None}
 
        for selector in self.PAGINATION_SELECTORS['javascript_buttons']:
            elementos = response.css(selector)
            if not elementos:
                continue
            elemento_html = elementos[0].get()
            if any(pattern in elemento_html for pattern in self.JAVASCRIPT_BUTTON_PATTERNS):
                return {'url': response.url, 'is_javascript': True, 'button_selector': selector.split('::')[0]}
 
        current_url = response.url
       
        match = re.search(r'/page/(\d+)/?', current_url)
        if match:
            current_page = int(match.group(1))
            next_page_url = re.sub(r'/page/\d+/?', f'/page/{current_page + 1}/', current_url)
            return {'url': next_page_url, 'is_javascript': False, 'button_selector': None}
 
        # 4. Parámetros ?page=N
        for param in ['page', 'p', 'pagina', 'pag']:
            match = re.search(rf'[?&]{param}=(\d+)', current_url)
            if match:
                current_page = int(match.group(1))
                next_page_url = re.sub(rf'{param}=\d+', f'{param}={current_page + 1}', current_url)
                return {'url': next_page_url, 'is_javascript': False, 'button_selector': None}
 
        # ❌ ELIMINA el bloque que generaba /page/2/ automáticamente
        return None
 
    def parse_article(self, response):
        site_name = response.meta.get('site_name', 'Desconocido')
        link = response.meta.get('link', response.url)
        dominio = response.meta.get('dominio', urlparse(link).netloc)
 
        if response.status != 200:
            return
 
        titular = self.extract_title(response)
        cuerpo = self.extract_body(response, dominio)
        categoria = self.extract_category(response, link)
        autor = self.extract_author(response)
        resumen = self.extract_summary(response)
 
        # ✅ Extraer TODAS las fechas encontradas en la página
        todas_las_fechas = self.extract_all_dates(response)
        fecha_principal = todas_las_fechas[0] if todas_las_fechas else None
 
        item = NewsItem(
            medio=site_name,
            titular=titular,
            fecha=fecha_principal,
            fechas=todas_las_fechas,
            link=link,
            cuerpo=cuerpo,
            categoria=categoria,
            autor=autor,
            resumen=resumen
        )
 
        if not self.validate_article(item):
            return
 
        if self.USAR_FILTRO_FECHAS and fecha_principal:
            try:
                fecha_articulo = datetime.strptime(fecha_principal, '%Y-%m-%d')
                if fecha_articulo < self.fecha_limite:
                    key = f"{site_name}_{response.url.split('?')[0]}"
                    self.old_articles_counter[key] = self.old_articles_counter.get(key, 0) + 1
                    return
            except:
                pass
 
        titulo_corto = titular[:60] + "..." if len(titular) > 60 else titular
        self.logger.info(f"📰 [{site_name}] {titulo_corto}")
        yield item
 
    # ============================================================
    # ✅ Extrae TODAS las fechas que encuentre en la página
    # ============================================================
    def extract_all_dates(self, response):
        fechas_encontradas = []
 
        # 1. Metaetiquetas (las más confiables)
        meta_selectores = [
            'meta[property="article:published_time"]::attr(content)',
            'meta[property="article:modified_time"]::attr(content)',
            'meta[name="date"]::attr(content)',
            'meta[name="pubdate"]::attr(content)',
            'meta[name="lastmod"]::attr(content)',
            'meta[itemprop="datePublished"]::attr(content)',
            'meta[itemprop="dateModified"]::attr(content)',
        ]
        for selector in meta_selectores:
            val = response.css(selector).get()
            if val:
                normalizada = self.normalizar_fecha(val.strip())
                if normalizada and normalizada not in fechas_encontradas:
                    fechas_encontradas.append(normalizada)
 
        # 2. Elementos HTML comunes
        html_selectores = [
            'time::attr(datetime)',
            'time::text',
            '[itemprop="datePublished"]::attr(content)',
            '[itemprop="dateModified"]::attr(content)',
            '[itemprop="datePublished"]::text',
            '[itemprop="dateModified"]::text',
            '.date::text',
            '.published::text',
            '.post-date::text',
            '.entry-date::text',
            '.fecha::text',
            '.update::text',
            '[class*="date"]::text',
            '[class*="fecha"]::text',
            '.post-meta-info li::text',  # cubre "23 febrero, 2026" de Tu Diario Huánuco
        ]
        for selector in html_selectores:
            valores = response.css(selector).getall()
            for val in valores:
                val = val.strip()
                if not val or len(val) < 5:
                    continue
                normalizada = self.normalizar_fecha(val)
                if normalizada and normalizada not in fechas_encontradas:
                    fechas_encontradas.append(normalizada)
 
        return fechas_encontradas
 
    def normalizar_fecha(self, fecha_str):
        """Normaliza diferentes formatos de fecha a YYYY-MM-DD"""
        if not fecha_str:
            return None
 
        fecha_str = fecha_str.strip()
 
        # ISO 8601: 2026-02-23 o 2026-02-23T10:30:00
        match = re.search(r'(\d{4})-(\d{2})-(\d{2})', fecha_str)
        if match:
            return match.group(0)
 
        # DD/MM/YYYY o DD-MM-YYYY
        match = re.search(r'(\d{2})[-/](\d{2})[-/](\d{4})', fecha_str)
        if match:
            dia, mes, año = match.groups()
            return f"{año}-{mes}-{dia}"
 
        meses_es = {
            'enero': '01', 'febrero': '02', 'marzo': '03', 'abril': '04',
            'mayo': '05', 'junio': '06', 'julio': '07', 'agosto': '08',
            'septiembre': '09', 'octubre': '10', 'noviembre': '11', 'diciembre': '12'
        }
 
        # "23 febrero, 2026" o "23 de febrero de 2026" (día primero)
        match = re.search(
            r'(\d{1,2})\s+(?:de\s+)?(' + '|'.join(meses_es.keys()) + r')[,\s]+(?:de\s+)?(\d{4})',
            fecha_str.lower()
        )
        if match:
            dia, mes_nombre, año = match.groups()
            return f"{año}-{meses_es[mes_nombre]}-{int(dia):02d}"
 
        # "febrero 25, 2026" (mes primero - estilo radiouno.pe)
        match = re.search(
            r'(' + '|'.join(meses_es.keys()) + r')\s+(\d{1,2})[,\s]+(\d{4})',
            fecha_str.lower()
        )
        if match:
            mes_nombre, dia, año = match.groups()
            return f"{año}-{meses_es[mes_nombre]}-{int(dia):02d}"
 
        return None
 
    def extract_title(self, response):
        selectors = [
            'h1::text',
            '.article-title::text',
            '.entry-title::text',
            '.post-title::text',
            'meta[property="og:title"]::attr(content)',
            'meta[name="twitter:title"]::attr(content)',
            'title::text'
        ]
        for selector in selectors:
            title = response.css(selector).get()
            if title:
                title = self.limpiar_texto(title.strip())
                if len(title) > 10:
                    return title
        return "Título no encontrado"
 
    def extract_body(self, response, dominio):
        domain_config = self.DOMAIN_CONFIGS.get(dominio, {})
        content_selectors = domain_config.get('content_selectors', [])
 
        if TRAFILATURA_DISPONIBLE:
            try:
                contenido = trafilatura.extract(
                    response.text,
                    include_comments=False,
                    include_tables=False,
                    favor_precision=True,
                    include_formatting=False
                )
                if contenido and len(contenido.strip()) > 100:
                    return self.limpiar_texto(contenido)
            except Exception as e:
                self.logger.debug(f"Trafilatura falló: {e}")
 
        for selector in content_selectors:
            if '::text' in selector:
                paragraphs = response.css(selector).getall()
            else:
                paragraphs = response.css(f'{selector} p::text').getall()
            if paragraphs and len(paragraphs) >= 2:
                cuerpo = ' '.join([p.strip() for p in paragraphs if p.strip()])
                if len(cuerpo) > 100:
                    return self.limpiar_texto(cuerpo)
 
        general_selectors = [
            'article p::text', '.article-content p::text', '.post-content p::text',
            '.entry-content p::text', '.news-content p::text', '.story-content p::text',
            '.content p::text', '.text p::text', '.body p::text',
            'div[itemprop="articleBody"] p::text'
        ]
        for selector in general_selectors:
            paragraphs = response.css(selector).getall()
            if paragraphs and len(paragraphs) >= 2:
                cuerpo = ' '.join([p.strip() for p in paragraphs if p.strip()])
                if len(cuerpo) > 100:
                    return self.limpiar_texto(cuerpo)
 
        all_paragraphs = response.css('p::text').getall()
        if all_paragraphs:
            filtered = []
            noise_keywords = [
                'publicidad', 'anuncio', '©', 'copyright', 'seguir leyendo',
                'suscríbete', 'newsletter', 'compartir', 'comentarios',
                'derechos reservados', 'todos los derechos'
            ]
            for p in all_paragraphs:
                text = p.strip()
                if len(text) < 20:
                    continue
                if any(keyword in text.lower() for keyword in noise_keywords):
                    continue
                if text.startswith(('http://', 'https://', 'www.')):
                    continue
                filtered.append(text)
            if len(filtered) >= 2:
                cuerpo = ' '.join(filtered)
                if len(cuerpo) > 100:
                    return self.limpiar_texto(cuerpo)
 
        return "Contenido no disponible"
 
    def extract_category(self, response, link):
        url_categories = {
            '/actualidad/': 'Actualidad',
            '/politica/': 'Política',
            '/deportes/': 'Deportes',
            '/economia/': 'Economía',
            '/cultura/': 'Cultura',
            '/tecnologia/': 'Tecnología',
            '/salud/': 'Salud',
            '/internacional/': 'Internacional',
            '/internacionales/': 'Internacional',
            '/sucesos/': 'Sucesos',
            '/justicia/': 'Justicia',
        }
        for pattern, category in url_categories.items():
            if pattern in link.lower():
                return category
 
        selectors = [
            'meta[property="article:section"]::attr(content)',
            '.category::text', '.post-category::text', '.section::text',
        ]
        for selector in selectors:
            cat = response.css(selector).get()
            if cat and len(cat.strip()) > 1:
                return cat.strip()
 
        return "General"
 
    def extract_author(self, response):
        selectors = [
            '.author-name::text', '.post-author::text',
            'meta[name="author"]::attr(content)',
            'a[rel="author"]::text',
        ]
        for selector in selectors:
            author = response.css(selector).get()
            if author:
                author = author.strip()
                author = re.sub(r'^(por|by)[:|\s]+', '', author, flags=re.IGNORECASE)
                if author and len(author) > 2:
                    return author
        return "No especificado"
 
    def extract_summary(self, response):
        selectors = [
            'meta[name="description"]::attr(content)',
            'meta[property="og:description"]::attr(content)',
        ]
        for selector in selectors:
            summary = response.css(selector).get()
            if summary and len(summary.strip()) > 30:
                return self.limpiar_texto(summary.strip()[:200])
        return ""
 
    def validate_article(self, item):
        if not item['titular'] or item['titular'] == "Título no encontrado":
            return False
        if len(item['titular']) < 10:
            return False
        if not item['cuerpo'] or item['cuerpo'] == "Contenido no disponible":
            return False
        if len(item['cuerpo']) < 150:
            return False
        return True
 
    def limpiar_texto(self, texto):
        if not texto:
            return ""
        texto = re.sub(r'\s+', ' ', texto)
        texto = re.sub(r'http\S+', '', texto)
        texto = re.sub(r'\S+@\S+', '', texto)
        texto = re.sub(r'[\.\?\!]{2,}', '.', texto)
        texto = re.sub(r'[\x00-\x1F\x7F-\x9F]', '', texto)
        return texto.strip()
 
    def errback_httpbin(self, failure):
        self.logger.error(f'❌ Error en {failure.request.url}: {failure.value}')
 
    def closed(self, reason):
        if self.sitios_con_javascript:
            self.logger.info(f"📊 Sitios con JavaScript: {', '.join(self.sitios_con_javascript)}")
        if self.sitios_sin_javascript:
            self.logger.info(f"📊 Sitios sin JavaScript: {', '.join(self.sitios_sin_javascript)}")
