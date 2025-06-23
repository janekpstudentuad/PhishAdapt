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
`db.session.commit()`