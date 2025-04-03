from flask import Flask
from reactpy import component, web, html
from reactpy.backend.flask import configure
from datos import productos

mui = web.module_from_template("react", "@mui/material", fallback="🔥")
Container = web.export(mui, "Container")
Grid = web.export(mui, "Grid")
Paper = web.export(mui, "paper")

def Tarjetas(productos):
    def Tarjeta(producto):
        return Grid(
            {"item": True, "sm": 6, "md": 3, "lg": 3},
            Paper(
                {"elevation": 4},
                html.h1(producto["nombre"]),
            )
        ),

    return Grid(
        {"container": True, "spacing": 8},
        [Tarjeta(producto) for producto in productos]       
    )

@component
def App():
    return Container(
        { "maxWidth": "md" },
        Tarjetas(productos)
    )

app = Flask(__name__)
configure(app, App)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
