To get latest repo onto PhishAdapt machine:
* Close folder in VS Code
* Delete folder
* Clone folder in VS code: https://github.com/janekpstudentuad/PhishAdapt
* Delete migrations folder if necessary

`python3 -m venv venv`

`source venv/bin/activate`

`pip install -r requirements`

`flask db init`

`flask db migrate -m "users table"`

`flask db upgrade`

`flask shell`

`u = User(username='phishadaptadmin', firstname='PhishAdapt', lastname='Admin', email='phishadaptadmin@phishadapt.msc', jobtitle='PhishAdapt Administrator', team='PhishAdapt', department='Cyber Security', is_admin=True)`

`u.set_password('Abertay123')`

`db.session.add(u)`

```
rows = [
    {"department": "Executive Leadership", "team": "CEO"},
    {"department": "Internal Services", "team": "HR"},
    {"department": "Internal Services", "team": "Finance & Accounting"},
    {"department": "Internal Services", "team": "IT"},
    {"department": "Internal Services", "team": "Legal & Compliance"},
    {"department": "Internal Services", "team": "Administration/Facilities"},
    {"department": "External-Facing Services", "team": "Sales & Business Development"},
    {"department": "External-Facing Services", "team": "Marketing & Communications"},
    {"department": "External-Facing Services", "team": "Customer Services / Support"},
    {"department": "External-Facing Services", "team": "Product/Service Delivery"},
    {"department": "Strategy & Innovation", "team": "Strategy and Planning"},
    {"department": "Strategy & Innovation", "team": "Innovation & R&D"},
]
```

`for row in rows:`
    `r=Organisation(**row)`
    `db.session.add(r)`

`db.session.commit()`