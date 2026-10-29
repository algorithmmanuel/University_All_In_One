"""Explicit laptop-beta configuration, isolated from development settings."""
from urllib.parse import parse_qsl, quote, urlsplit

MAIL_KEYS = ('BREVO_API_KEY', 'EDUCYBER_EMAIL_SENDER', 'EDUCYBER_PUBLIC_WEB_URL')
BETA_BRANCH = 'feature/secure-password-recovery'
DEV_BRANCH = 'feature/beta-continuous-improvement'


def validate_beta_database(value):
    try:
        u = urlsplit(value)
        valid = (u.scheme == 'postgresql+psycopg' and u.hostname == '127.0.0.1'
            and u.port == 5433 and u.path == '/educyber' and u.username == 'educyber'
            and bool(u.password) and not u.fragment
            and parse_qsl(u.query, keep_blank_values=True) == [('connect_timeout', '5')]
            and not any(c.isspace() for c in value))
    except (TypeError, ValueError): valid = False
    if not valid: raise ValueError('Unexpected beta database target')


def application_environment(inherited, password, mail=None):
    """Keep system settings, build the fixed beta target, retain only named mail settings."""
    if not password: raise ValueError('Missing beta database password in root .env')
    prefixes = ('EDUCYBER_', 'NEXT_PUBLIC_', 'BREVO', 'SMTP', 'POSTGRES_', 'PG')
    excluded = {'DATABASE_URL', 'TEST_DATABASE_URL', 'PYTHONPATH', 'PYTHONHOME',
                'VIRTUAL_ENV', 'NODE_OPTIONS', 'NODE_PATH'}
    env = {k: v for k, v in inherited.items() if k.upper() not in excluded
           and not k.upper().startswith(prefixes)}
    env.update({'DATABASE_URL': 'postgresql+psycopg://educyber:' + quote(password, safe='')
        + '@127.0.0.1:5433/educyber?connect_timeout=5', 'EDUCYBER_ENV': 'beta',
        'EDUCYBER_PRIVATE_BETA': 'enabled', 'EDUCYBER_LOCAL_DEVELOPMENT': 'disabled', 'EDUCYBER_API_ORIGIN': 'http://127.0.0.1:8000',
        'EDUCYBER_WEB_ORIGIN': 'http://127.0.0.1:3000', 'NEXT_PUBLIC_API_BASE_URL': '',
        'EDUCYBER_CORS_ORIGINS': 'http://127.0.0.1:3000,http://localhost:3000'})
    for key in MAIL_KEYS:
        value = (mail or {}).get(key) or inherited.get(key)
        if value: env[key] = value
    validate_beta_database(env['DATABASE_URL'])
    return env


def validate_mail(env):
    u = urlsplit(env.get('EDUCYBER_PUBLIC_WEB_URL', '').rstrip('/'))
    valid = (all(env.get(k) for k in MAIL_KEYS) and u.hostname and not u.username
        and not u.password and not u.query and not u.fragment and u.path in ('', '/')
        and (u.scheme == 'https' or (u.scheme == 'http' and u.hostname in ('127.0.0.1', 'localhost'))))
    if not valid: raise ValueError('Configure beta recovery mail before starting the API')
