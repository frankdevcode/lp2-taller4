# Lenguaje de Programación 2 - Taller 4: Web con React y Material UI desde Python y Flask

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.1.0-green.svg)
![ReactPy](https://img.shields.io/badge/ReactPy-1.0.0-61DAFB.svg)

## Autor

- Francisco Perlaza

## Descripción del Proyecto

Este proyecto es una aplicación web que muestra un catálogo de productos tecnológicos, utilizando Python con Flask en el backend y ReactPy para crear una interfaz de usuario interactiva. La aplicación permite a los usuarios explorar productos, buscar, filtrar y ordenar según sus preferencias.

La aplicación combina la potencia de Python para el backend con la flexibilidad de React para crear interfaces de usuario dinámicas, todo desde un único lenguaje de programación.

## Características

- **Catálogo de productos**: Visualización de productos tecnológicos con imágenes, nombres, descripciones, precios y calificaciones.
- **Sistema de búsqueda**: Búsqueda de productos por nombre o descripción.
- **Filtrado avanzado**: 
  - Filtrado por rango de precios (mínimo y máximo)
  - Filtrado por calificación mínima
- **Ordenamiento**: 
  - Por precio (ascendente y descendente)
  - Por mejor calificación
- **Panel de estadísticas**: 
  - Total de productos
  - Productos filtrados
  - Precio promedio
  - Calificación promedio
- **Diseño responsivo**: Interfaz adaptable a diferentes tamaños de pantalla

## Tecnologías Utilizadas

- **Backend**: Python, Flask
- **Frontend**: ReactPy (React en Python)
- **Datos**: Estructura de datos en Python (archivo datos.py)

## Instalación

1. Clonar o descargar el proyecto
```bash
git clone https://github.com/UR-CC/lp2-taller4.git
```

2. Crear y activar entorno virtual
```bash
cd lp2-taller4
python -m venv venv
# En Windows:
venv\Scripts\activate
# En macOS/Linux:
source venv/bin/activate
```

3. Instalar librerías y dependencias
```bash
pip install -r requirements.txt
```
    
## Ejecución

1. Ejecutar el proyecto
```bash
python main.py
```

2. Abrir el navegador web y acceder a la aplicación
```
http://127.0.0.1:5000
```

## Estructura del Proyecto

- **main.py**: Archivo principal que contiene la aplicación Flask y los componentes de React
- **datos.py**: Archivo con los datos de los productos
- **requirements.txt**: Lista de dependencias del proyecto

## Funcionalidades Implementadas

### Visualización de Productos
La aplicación muestra los productos en un formato de tarjetas con imágenes, nombres, descripciones, precios y un sistema visual de calificación por estrellas.

### Sistema de Búsqueda y Filtrado
- **Búsqueda por texto**: Permite encontrar productos por nombre o descripción
- **Filtrado por precio**: Permite establecer un rango de precios mínimo y máximo
- **Filtrado por calificación**: Permite filtrar productos con una calificación mínima
- **Ordenamiento**: Permite ordenar productos por precio (ascendente o descendente) o por mejor calificación

### Panel de Estadísticas
Muestra información resumida sobre los productos, incluyendo:
- Total de productos en la base de datos
- Número de productos que coinciden con los filtros actuales
- Precio promedio de todos los productos
- Calificación promedio de todos los productos

