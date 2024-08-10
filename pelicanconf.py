SITENAME = "The Critical Section"
SITE_DESCRIPTION = "A personal blog for artificial intelligence and similar topics."
LINKEDIN_USERNAME = None

# SITEURL = ''

PATH = 'content'
OUTPUT_PATH = 'docs'
PAGE_PATHS = ['pages'] # Relative to PATH
PAGE_SAVE_AS = "{slug}.html" # How pages are saved
PAGE_URL = "{slug}.html"
TAGS_SAVE_AS = "tags.html"
ARTICLE_PATHS = ['articles']
ARTICLE_SAVE_AS = '{slug}.html' 
AUTHORS_SAVE_AS = '' # Prevent authors page from being generated
CATEGORIES_SAVE_AS = '' # Prevent category page from being generated
AUTHOR_SAVE_AS = ''
CATEGORY_SAVE_AS = ''
ARCHIVES_SAVE_AS = ''


TIMEZONE = 'Europe/Sofia'
DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('Pelican', 'https://getpelican.com/'),
         ('Python.org', 'https://www.python.org/'),
         ('Jinja2', 'https://palletsprojects.com/p/jinja/'),
         ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('You can add links in your config file', '#'),
          ('Another social link', '#'),)

DEFAULT_PAGINATION = False

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

PLUGINS = ['plugins.summary', 'plugins.render_math']

SUMMARY_USE_FIRST_PARAGRAPH = True

THEME = 'themes/minima'
STATIC_PATHS = ['images', 'assets']
EXTRA_PATH_METADATA = {
    # 'extra/custom.css': {'path': 'custom.css'},
    # 'extra/robots.txt': {'path': 'robots.txt'},
    # 'assets/favicon.ico': {'path': 'favicon.ico'},
    # 'extra/CNAME': {'path': 'CNAME'},
    # 'extra/LICENSE': {'path': 'LICENSE'},
    # 'extra/README': {'path': 'README'},
}

def sort_tags(tags):
    """
    A custom sorting function for enumerating (and filtering) the tags.

    tags: List[(str, [Articles]]
    """
    # Filter tags shown
    custom_order = ['cs', 'econ', 'ultra-rationalism', 'rl', 'ai']
    tags = list(filter(lambda x: x[0] in custom_order, tags))

    # Sort in custom order
    return sorted(tags, key=lambda x: custom_order.index(x[0]) if x[0] in custom_order else len(custom_order))

# Overwrite some of the Jinja commands using custom Python functions
JINJA_FILTERS = {'sort_tags': sort_tags}

TYPOGRIFY = False
SMART_QUOTES = False

if SMART_QUOTES:
    from typogrify.filters import smartypants
    def smart_quotes(text):
        """
        Turns straight vertical quotes into slanted vertical quotes. As well as other stylistic changes.
        """
        return smartypants(text)
else:
    smart_quotes = lambda x: x

JINJA_FILTERS['smart_quotes'] = smart_quotes

MATH_JAX = {"source": '"https://cdn.jsdelivr.net/npm/mathjax@2/MathJax.js?config=TeX-AMS-MML_HTMLorMML"'}
