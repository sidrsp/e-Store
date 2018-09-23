from eStore import create_app

from eStore.utils.debug_sqlalchemy_queries import sql_debug
app = create_app()

# app.after_request(sql_debug)

if __name__ == '__main__':
    app.run(debug=True)






