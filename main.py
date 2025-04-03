from flask import Flask, render_template
from reactpy import component, html, web, hooks
from reactpy.backend.flask import configure
from datos import productos

# Función para formatear el precio como número para ordenamiento
def extract_price_value(price_str):
    # Elimina el símbolo de moneda y las comas, luego convierte a float
    return float(price_str.replace('$', '').replace(',', ''))

@component
def App():
    # Estados para la búsqueda, filtros y ordenamiento
    search_query, set_search_query = hooks.use_state("")
    min_price, set_min_price = hooks.use_state(0)
    max_price, set_max_price = hooks.use_state(15000000)  # Precio máximo predeterminado alto
    min_rating, set_min_rating = hooks.use_state(0)
    sort_by, set_sort_by = hooks.use_state("none")  # Opciones: none, price_asc, price_desc, rating_desc
    
    # Función para filtrar y ordenar productos
    def filter_and_sort_products():
        # Primero filtramos por búsqueda
        filtered = [p for p in productos if search_query.lower() in p['nombre'].lower() or 
                                           search_query.lower() in p['descripcion'].lower()]
        
        # Filtramos por precio
        price_filtered = [p for p in filtered if 
                         extract_price_value(p['precio']) >= min_price and 
                         extract_price_value(p['precio']) <= max_price]
        
        # Filtramos por calificación
        rating_filtered = [p for p in price_filtered if p['rating'] >= min_rating]
        
        # Ordenamos según la opción seleccionada
        if sort_by == "price_asc":
            return sorted(rating_filtered, key=lambda p: extract_price_value(p['precio']))
        elif sort_by == "price_desc":
            return sorted(rating_filtered, key=lambda p: extract_price_value(p['precio']), reverse=True)
        elif sort_by == "rating_desc":
            return sorted(rating_filtered, key=lambda p: p['rating'], reverse=True)
        else:
            return rating_filtered
    
    # Aplicar filtros y ordenamiento
    filtered_products = filter_and_sort_products()
    
    # Manejadores de eventos
    def handle_search_change(event):
        set_search_query(event['target']['value'])
    
    def handle_min_price_change(event):
        try:
            value = float(event['target']['value'])
            set_min_price(value)
        except ValueError:
            pass
    
    def handle_max_price_change(event):
        try:
            value = float(event['target']['value'])
            set_max_price(value)
        except ValueError:
            pass
    
    def handle_min_rating_change(event):
        set_min_rating(float(event['target']['value']))
    
    def handle_sort_change(event):
        set_sort_by(event['target']['value'])
    
    def handle_reset_filters():
        set_search_query("")
        set_min_price(0)
        set_max_price(15000000)
        set_min_rating(0)
        set_sort_by("none")
    
    # Componente para el panel de filtros
    def FilterPanel():
        return html.div(
            {"className": "filter-panel", "style": {
                "backgroundColor": "#fff",
                "padding": "20px",
                "borderRadius": "8px",
                "boxShadow": "0 2px 4px rgba(0,0,0,0.1)",
                "marginBottom": "20px"
            }},
            html.h2(
                {"style": {"marginBottom": "15px", "color": "#2a5885"}},
                "Filtros y Búsqueda"
            ),
            # Búsqueda
            html.div(
                {"style": {"marginBottom": "15px"}},
                html.label(
                    {"htmlFor": "search", "style": {"display": "block", "marginBottom": "5px", "fontWeight": "bold"}},
                    "Buscar productos:"
                ),
                html.input({
                    "id": "search",
                    "type": "text",
                    "value": search_query,
                    "onChange": handle_search_change,
                    "placeholder": "Nombre o descripción...",
                    "style": {
                        "width": "100%",
                        "padding": "8px",
                        "borderRadius": "4px",
                        "border": "1px solid #ddd"
                    }
                })
            ),
            # Filtro de precio
            html.div(
                {"style": {"marginBottom": "15px"}},
                html.label(
                    {"style": {"display": "block", "marginBottom": "5px", "fontWeight": "bold"}},
                    "Rango de precio:"
                ),
                html.div(
                    {"style": {"display": "flex", "gap": "10px"}},
                    html.div(
                        {"style": {"flex": "1"}},
                        html.label(
                            {"htmlFor": "min-price", "style": {"display": "block", "marginBottom": "5px"}},
                            "Mínimo:"
                        ),
                        html.input({
                            "id": "min-price",
                            "type": "number",
                            "value": min_price,
                            "onChange": handle_min_price_change,
                            "min": "0",
                            "style": {
                                "width": "100%",
                                "padding": "8px",
                                "borderRadius": "4px",
                                "border": "1px solid #ddd"
                            }
                        })
                    ),
                    html.div(
                        {"style": {"flex": "1"}},
                        html.label(
                            {"htmlFor": "max-price", "style": {"display": "block", "marginBottom": "5px"}},
                            "Máximo:"
                        ),
                        html.input({
                            "id": "max-price",
                            "type": "number",
                            "value": max_price,
                            "onChange": handle_max_price_change,
                            "min": "0",
                            "style": {
                                "width": "100%",
                                "padding": "8px",
                                "borderRadius": "4px",
                                "border": "1px solid #ddd"
                            }
                        })
                    )
                )
            ),
            # Filtro de calificación
            html.div(
                {"style": {"marginBottom": "15px"}},
                html.label(
                    {"htmlFor": "min-rating", "style": {"display": "block", "marginBottom": "5px", "fontWeight": "bold"}},
                    f"Calificación mínima: {min_rating}"
                ),
                html.input({
                    "id": "min-rating",
                    "type": "range",
                    "min": "0",
                    "max": "5",
                    "step": "0.5",
                    "value": min_rating,
                    "onChange": handle_min_rating_change,
                    "style": {
                        "width": "100%"
                    }
                })
            ),
            # Ordenamiento
            html.div(
                {"style": {"marginBottom": "15px"}},
                html.label(
                    {"htmlFor": "sort-by", "style": {"display": "block", "marginBottom": "5px", "fontWeight": "bold"}},
                    "Ordenar por:"
                ),
                html.select({
                    "id": "sort-by",
                    "value": sort_by,
                    "onChange": handle_sort_change,
                    "style": {
                        "width": "100%",
                        "padding": "8px",
                        "borderRadius": "4px",
                        "border": "1px solid #ddd"
                    }
                },
                    html.option({"value": "none"}, "Sin ordenar"),
                    html.option({"value": "price_asc"}, "Precio: menor a mayor"),
                    html.option({"value": "price_desc"}, "Precio: mayor a menor"),
                    html.option({"value": "rating_desc"}, "Mejor calificación")
                )
            ),
            # Botón para resetear filtros
            html.button({
                "onClick": handle_reset_filters,
                "style": {
                    "backgroundColor": "#2a5885",
                    "color": "white",
                    "border": "none",
                    "padding": "10px 15px",
                    "borderRadius": "4px",
                    "cursor": "pointer",
                    "fontWeight": "bold",
                    "width": "100%"
                }
            }, "Resetear filtros")
        )
    
    # Componente para mostrar estadísticas
    def Statistics():
        total_products = len(productos)
        filtered_count = len(filtered_products)
        avg_price = sum(extract_price_value(p['precio']) for p in productos) / total_products if total_products > 0 else 0
        avg_rating = sum(p['rating'] for p in productos) / total_products if total_products > 0 else 0
        
        return html.div(
            {"style": {
                "backgroundColor": "#f0f7ff",
                "padding": "15px",
                "borderRadius": "8px",
                "marginBottom": "20px",
                "textAlign": "center"
            }},
            html.div(
                {"style": {"display": "flex", "justifyContent": "space-around", "flexWrap": "wrap"}},
                html.div(
                    {"style": {"margin": "10px"}},
                    html.div({"style": {"fontWeight": "bold"}}, "Total de productos:"),
                    html.div({"style": {"fontSize": "24px", "color": "#2a5885"}}, str(total_products))
                ),
                html.div(
                    {"style": {"margin": "10px"}},
                    html.div({"style": {"fontWeight": "bold"}}, "Productos filtrados:"),
                    html.div({"style": {"fontSize": "24px", "color": "#2a5885"}}, str(filtered_count))
                ),
                html.div(
                    {"style": {"margin": "10px"}},
                    html.div({"style": {"fontWeight": "bold"}}, "Precio promedio:"),
                    html.div({"style": {"fontSize": "24px", "color": "#2a5885"}}, f"${avg_price:,.0f}")
                ),
                html.div(
                    {"style": {"margin": "10px"}},
                    html.div({"style": {"fontWeight": "bold"}}, "Calificación promedio:"),
                    html.div({"style": {"fontSize": "24px", "color": "#2a5885"}}, f"{avg_rating:.1f} ★")
                )
            )
        )
    
    @component
    def Tarjetas(productos_list):
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

        # Mensaje cuando no hay productos que coincidan con los filtros
        if len(productos_list) == 0:
            return html.div(
                {"style": {
                    "textAlign": "center",
                    "padding": "50px",
                    "backgroundColor": "#f8f8f8",
                    "borderRadius": "8px",
                    "margin": "20px 0"
                }},
                html.h3({"style": {"color": "#666"}}, "No se encontraron productos que coincidan con los filtros"),
                html.p({}, "Intenta ajustar los criterios de búsqueda")
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
                    for producto in productos_list
                ]
            )
        )

    # Renderizado principal
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
        html.div(
            {"style": {"maxWidth": "1200px", "margin": "0 auto", "padding": "0 20px"}},
            # Estadísticas
            Statistics(),
            # Estructura de dos columnas: filtros y productos
            html.div(
                {"style": {"display": "flex", "flexWrap": "wrap", "gap": "20px"}},
                # Columna de filtros
                html.div(
                    {"style": {"flex": "0 0 250px"}},
                    FilterPanel()
                ),
                # Columna de productos
                html.div(
                    {"style": {"flex": "1"}},
                    Tarjetas(filtered_products)
                )
            )
        )
    )

app = Flask(__name__)
configure(app, App)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
