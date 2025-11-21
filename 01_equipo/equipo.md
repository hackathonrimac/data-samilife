# 📋 Entregable 1: Información del equipo y propuesta inicial

## Nombre del equipo

**SamiLife**

---

## ¿Cuéntanos a grandes rasgos qué planean hacer?

> Describe brevemente la idea principal de tu solución. Incluye los componentes clave, la tecnología que planeas usar y cómo esperas que tu solución resuelva el reto planteado.

**Tu respuesta:**

Desarrollaremos **SamiLife**, una plataforma centralizada con una experiencia de usuario estilo "Airbnb" pero aplicada al sector salud. El objetivo es que cualquier usuario, ante una dolencia, pueda encontrar la clínica, hospital o posta más cercana que cuente con la **especialidad específica**, el **médico disponible** y el **stock de medicamentos** necesario.

Para lograrlo, implementaremos un sistema de **Web Scraping automatizado y ETL** que extraiga y cruce información de fuentes oficiales fragmentadas:
1.  **RENIPRESS:** Para geolocalización, imágenes, categorización y detalles de infraestructura de las IPRESS (Instituciones Prestadoras de Servicios de Salud).
2.  **DIGEMID:** Para verificar disponibilidad y precios referenciales de medicamentos por establecimiento.
3.  **SuSalud y Colegio Médico:** Para validar credenciales, especialidades y turnos laborales de los doctores.

La solución constará de una **API REST** que normaliza esta data y un **Frontend intuitivo** basado en mapas interactivos, permitiendo al paciente tomar decisiones rápidas basadas en cercanía, capacidad resolutiva (especialidad) y disponibilidad de insumos.

---

## ¿Qué retos/riesgos visualizan? (¿Con qué te podemos ayudar?)

> Identifica los principales desafíos o riesgos que podrían afectar el desarrollo de tu solución. Estos pueden ser técnicos, operativos o relacionados con la viabilidad de la idea. Además, menciona cualquier apoyo específico que necesites para superar estos obstáculos.

**Tu respuesta:**

* **Inconsistencia y Normalización de Datos:** El mayor reto técnico será cruzar la data de distintas fuentes (ej. unir un doctor de la base del CMP con un hospital en RENIPRESS) debido a diferencias en la escritura de nombres o direcciones.
* **Acceso a la Data (Anti-scraping/Performance):** Los portales gubernamentales suelen tener tiempos de respuesta lentos o captchas que dificultan la extracción en tiempo real.
* **Actualización de Turnos:** Obtener la disponibilidad *en tiempo real* de los turnos médicos es complejo si las clínicas no exponen esa data públicamente de forma dinámica.

**Ayuda requerida:** Nos sería de gran utilidad asesoría sobre librerías de Python optimizadas para limpieza de texto difuso (fuzzy matching) para mejorar el cruce de bases de datos, y acceso a endpoints oficiales si estuvieran disponibles para evitar scraping excesivo.

---

## Tecnologías planificadas

Lista las principales tecnologías, frameworks y herramientas que planean utilizar:

**Frontend:**
- Next.js (React) para la interfaz de usuario optimizada y SSR.
- Tailwind CSS y Shadcn/ui para el diseño estilo "Airbnb" (limpio y moderno).
- Leaflet o Google Maps API para la geolocalización de clínicas.

**Backend:**
- Python (FastAPI) para la creación de la API REST.
- PostgreSQL con extensiones espaciales (PostGIS) para búsquedas por geolocalización.

**IA/ML:**
- Scikit-learn / NLP para la normalización de nombres de especialidades y búsqueda semántica (ej. usuario busca "dolor de barriga" y el sistema sugiere "Gastroenterología").

**Cloud/DevOps:**
- AWS (EC2 o Lambda) para el despliegue de los scrapers y la API.
- Docker para la contenerización de servicios.

**Otras:**
- Selenium / Playwright y BeautifulSoup para el Web Scraping de RENIPRESS, DIGEMID y CMP.
- Pandas para el procesamiento y limpieza de datos (ETL).

---

## Notas adicionales

Espacio libre para cualquier información relevante sobre el equipo (experiencia previa, motivación, proyectos similares realizados, etc.).

**Tu respuesta:**

El equipo **SamiLife** está motivado por el impacto social de reducir la incertidumbre en momentos de emergencia médica. Creemos que la información de salud es un derecho, pero actualmente es inaccesible por su fragmentación. Nuestro enfoque no es solo técnico, sino humano: queremos que encontrar una cura sea tan fácil como reservar un alojamiento. Estamos combinando experiencia en scraping de datos públicos con diseño de interfaces centradas en el usuario para entregar un MVP funcional y escalable.

---
