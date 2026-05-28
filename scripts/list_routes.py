from app import create_app

app = create_app('development')
with app.app_context():
    rules = sorted([(r.endpoint, str(r)) for r in app.url_map.iter_rules()])
    for e, r in rules:
        print(e, r)
