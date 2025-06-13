🌐 GlobalTrade

**GlobalTrade** 
Es una aplicación educativa diseñada para simular procesos clave del comercio internacional. Permite gestionar productos, calcular aranceles y conversiones de divisas, generar documentación aduanera y rastrear envíos desde una interfaz gráfica amigable.

## 📌 Características principales

- 📦 **Gestión de productos** (perecibles, electrónicos e híbridos)
- 💰 **Conversión de monedas** basada en tasas predeterminadas
- 📄 **Cálculo automático de aranceles** según país de destino
- 🚚 **Creación y rastreo de envíos** paso a paso
- 📑 **Generación de documentación aduanera** e inventarios
- 🖥️ **Interfaz gráfica intuitiva** con menús y botones interactivos (Tkinter)

## 🚀 Requisitos

- Python 3.10 o superior
- Sistema operativo: Windows o Linux
- Librerías: ver sección de instalación

## 🛠️ Instalación

1. **Clona el repositorio:**
   ```bash
   git clone https://github.com/TBlackHoleR/GlobalTrade.git
   cd GlobalTrade

2. **Crea un entorno virtual**
    python -m venv venv
    venv\Scripts\activate  # En Windows
    source venv/bin/activate  # En Linux/Mac

3. **Instala las dependencias:**
    instrucciones en requeriments.txt

▶️ Cómo usar GlobalTrade
1. **Ejecuta el menú principal:**
    python Uno_main.py

2. **Se abrirá una ventana gráfica con varias opciones:**

    -Gestión de productos: agregar y visualizar productos.
    -Simulación de envíos: seleccionar productos, país de destino y generar seguimiento.
    -Conversión de monedas: convertir entre diferentes divisas.
    -Generación de documentación: visualizar detalles aduaneros o exportar.

3. **Puedes cerrar la aplicación en cualquier momento desde el menú o la “X”.**

## 📋 Ejemplo de uso
Abre el programa (Uno_main.py)

Agrega productos en la sección correspondiente

Ve a "Simular envío", selecciona productos y destino

Aplica conversión y calcula aranceles

Exporta la documentación o revisa el seguimiento del envío

## 📁 Estructura del proyecto
GlobalTrade/
│
│── docs/
│   └── Documentacion.pdf   # Docuentación del proyecto
│
│
├── src/                    # Código fuente organizado por módulos
│   ├── Dos_productos.py        # Clases de productos
│   ├── Tres_envios.py           # Clase Envio
│   ├── Cuatro_conversiones.py     # Cálculo de divisas y aranceles
│   └── Cinco_documentacion.py         # Generacion de Documentacion
│
├── venv/                   # Carpeta generada por la interfaz grafica
│   ├── Lib/
│   ├── Scripts/
│   └── pyvenv.cfg         
│
├── fdpd.py                 # Código para generar documentacion
├── README.md               # Manual de usuario
├── Uno_main.py             # Archivo principal (lanza la app)
└── requirements.txt        # Dependencias

## 👥 Créditos
Este proyecto fue desarrollado por estudiantes de la Universidad Regional de Guatemala como parte del curso de Programación II.

Equipo GlobalTrade:

Brayan Barreno (Coordinador y Documentación)

Carlos (Módulo de productos)

Melisa (Módulo de envíos)

Neytan (Conversión y aranceles)

Omar (Inventario y documentación)

