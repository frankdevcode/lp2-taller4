from flask import Flask, render_template
from reactpy import component, html, web
from reactpy.backend.flask import configure
from datos import productos

# Crear componentes más simples para asegurar que la aplicación funcione correctamente
@component
def Tarjetas(productos):
    @component
    def Tarjeta(producto):
        return html.div(
            {"className": "card", "style": {"margin": "10px", "padding": "15px", "boxShadow": "0 4px 8px rgba(0,0,0,0.1)"}},
            html.img({
                "src": f"https://picsum.photos/id/{producto['id']}/400/200",
                "alt": producto["nombre"],
                "style": {
                    "width": "100%",
                    "height": "auto",
                    "borderRadius": "8px",
                    "marginBottom": "15px"
                },
            }),
            html.div(
                {"className": "card-body"},
                html.h3({"style": {"marginBottom": "10px"}}, producto['nombre']),
                html.div(
                    {"style": {"color": "gold", "fontSize": "24px", "marginBottom": "10px"}},
                    "★" * int(producto['rating']),
                    html.span(
                        {"style": {"color": "gray"}},
                        "★" * (5 - int(producto['rating']))
                    )
                ),
                html.p(
                    {"style": {"color": "#666", "marginBottom": "10px"}},
                    producto['descripcion']
                ),
                html.h4(
                    {"style": {"color": "#2a5885", "fontWeight": "bold"}},
                    producto['precio']
                ),
            ),
        )

    return html.div(
        {"className": "container", "style": {"maxWidth": "1200px", "margin": "0 auto", "padding": "20px"}},
        html.div(
            {"className": "row", "style": {"display": "flex", "flexWrap": "wrap", "margin": "0 -10px"}},
            [
                html.div(
                    {"className": "col", "style": {"flex": "0 0 25%", "maxWidth": "25%", "padding": "0 10px"}},
                    Tarjeta(producto)
                )
                for producto in productos
            ]
        )
    )

@component
def App():
    return html.div(
        {"style": {"fontFamily": "Arial, sans-serif", "backgroundColor": "#f5f5f5", "minHeight": "100vh", "padding": "20px 0"}},
        html.div(
            {"style": {"textAlign": "center", "marginBottom": "30px"}},
            html.h1(
                {"style": {"color": "#2a5885", "fontSize": "36px"}},
                "Catálogo de Productos"
            ),
            html.p(
                {"style": {"color": "#666"}},
                "Explora nuestra selección de productos tecnológicos"
            )
        ),
        Tarjetas(productos)
    )

app = Flask(__name__)
configure(app, App)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
