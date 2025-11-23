# 🏆 Entregable Final: Resultados y demo - SamiLife

> **⚠️ Importante:** Este entregable debe completarse antes del **domingo 23 de noviembre a las 11:45 AM** para poder presentar tu proyecto.

---

## ✅ Cómo entregar este documento

1. **Completa todas las secciones** de este archivo con tu solución final, demo y resultados
2. **Asegúrate de incluir:**
   - Link al deck compartido de presentación (Google Slides)
   - Link a tu código (carpeta `/src` de este repo o enlace externo)
   - Link a demo en vivo (si aplica)
3. **Guarda los cambios:**
   - Desde GitHub: Presiona "Commit changes" al terminar de editar
   - Localmente: Ejecuta `git add .` y `git commit -m "Entregable final completo"`
4. **Sube a GitHub:** 
   - Desde GitHub: Automático al hacer commit
   - Localmente: Ejecuta `git push`
5. **Verifica:** Refresca este repositorio en GitHub y confirma que todo esté visible y los enlaces funcionen

> 💡 **Importante:** Este es tu último entregable. Revisa que todos los enlaces funcionen antes de la hora límite.

---

## Integrantes Finales

| Nombre completo | Usuario GitHub | Rol | Especialidad |
|-----------------|----------------|-----|--------------|
| [Diva Stewart Maquera Bobadilla] | @stewartmb | PM | Agile Methodologies |
| [Rodrigo Li Chumpitaz] | @RodrigoLiC | Cloud Engineer + Data Engineer + Backend | AWS + Seaborn + FastAPI |
| [Sergio Sebastián Lezama Orihuela] | @SergioSLO  | DBA & Backend | Postgres + FastAPI |
| [Jorge Alexander Leon Villarreyes] | @JorgeL2005 | Data Engineer & Frontend | Next.js + React |
| [Valentina Celeste Alvarez Beraun] | @vvalentina-alvarez | Data Engineer & UX/UI | Figma + React |
---

## 1. ¿Qué hace tu proyecto?

> Describe de manera breve y clara la funcionalidad principal de tu proyecto. ¿Qué problema resuelve y cómo lo hace?

**Ejemplo para Reto 1 - Data:**  
*"Nuestro proyecto es un buscador inteligente de doctores y clínicas que consolida información dispersa de múltiples fuentes públicas. Permite a cualquier ciudadano encontrar médicos por especialidad, ubicación y disponibilidad en menos de 30 segundos. También muestra medicamentos referenciales por especialidad, facilitando el acceso a información de salud confiable."*

**Tu respuesta:**

Nosotros somos SamiLife, una plataforma diseñada para ayudar a los usuarios a encontrar centros de salud y médicos especializados según su ubicación geográfica. Nuestro objetivo es facilitar el acceso a servicios médicos cercanos y adecuados a las necesidades de cada persona, mejorando así su experiencia al buscar y seleccionar atención médica.

La selección de profesionales se realiza considerando la aseguradora del usuario, ofreciendo información relevante, actualizada y confiable sobre los médicos disponibles en su zona. Además, brindamos detalles sobre los servicios que ofrece cada centro de salud, permitiendo tomar decisiones informadas sobre su atención.

Por otra parte, contamos con información unificada sobre medicamentos referenciales asociados a distintas especialidades médicas, ayudando a los usuarios a comprender mejor sus opciones de tratamiento. También incorporamos un buscador de medicamentos por nombre o por especialidad, proporcionando datos claros y precisos sobre las alternativas disponibles.
---

## 2. ¿Cómo lo construyeron?

> Explica brevemente las tecnologías y herramientas que utilizaste para construir tu proyecto. ¿Qué frameworks o plataformas empleaste y cómo se integraron?

**Ejemplo:**  
*"Construimos la solución con:"*
- *Web scrapers en Python (Selenium + BeautifulSoup) para extraer datos de 15 sitios web de clínicas*
- *Pipeline ETL con Pandas para limpiar y normalizar información de 5,000+ médicos*
- *Base de datos PostgreSQL para almacenamiento estructurado*
- *API REST con FastAPI para consultas rápidas*
- *Frontend en Next.js con diseño responsivo*
- *Búsqueda semántica con Sentence Transformers para mejorar resultados*
- *Deploy en AWS usando Lambda, RDS y CloudFront*

**Tu respuesta:**

Contruimos la solución con:
- Web scrapping en Python usando request de apis de susalud 
- Pipeline ETL con Pandas para unificar, limpiar y normalizar la información de los médicos, centros de salud y medicinas.
- Base de datos Aurora RDS para almacenamiento estructurado.
- API REST con FastAPI para consultas rápidas.
- Frontend en React con diseño responsivo.
- Búsqueda por proximidad geográfica utilizando PostGIS para mejorar los resultados basados en la ubicación del usuario.
- Deploy en AWS usando App Runner para el backend y frontend, y Aurora RDS para la base de datos.
- Integración de Google Maps API para mostrar la ubicación de los centros de salud en un mapa interactivo.

---

## 3. ¿Qué desafíos enfrentaron?

> Describe los principales retos y dificultades que encontraron durante el desarrollo del proyecto. ¿Cómo los abordaron y qué soluciones implementaron?

**Tu respuesta:**

Enfrentamos tres desafíos técnicos críticos debido a la naturaleza fragmentada de la salud pública:

1.  **Inconsistencia Geoespacial (RENIPRESS):** La base de datos oficial de establecimientos de salud (RENIPRESS) proporciona direcciones en formato de texto libre, muchas veces con errores tipográficos o referencias ambiguas, y no incluye coordenadas GPS precisas.
    * *Solución:* Implementamos un pipeline de **Geocodificación inversa**, utilizando librerías espaciales para traducir direcciones textuales en coordenadas (latitud/longitud) exactas, permitiendo la visualización correcta en nuestro mapa interactivo.

2.  **Fragmentación Semántica en Especialidades:** Cada clínica y fuente de datos nombra las especialidades de forma distinta (ej. "Gastro", "Gastroenterología", "Digestivo").
    * *Solución:* Desarrollamos una **capa de normalización** en nuestro proceso ETL. Creamos diccionarios de sinónimos y algoritmos de coincidencia de texto (fuzzy matching) para agrupar todas las variantes bajo categorías estándar unificadas.

3.  **Heterogeneidad de Fuentes de Datos:** Integrar fuentes tan dispares como DIGEMID (precios/stock) y el Colegio Médico (datos de doctores) requería manejar estructuras de datos incompatibles.
    * *Solución:* Diseñamos una arquitectura de **"Ingesta Modular"**. En lugar de un solo scraper gigante, creamos módulos independientes para cada fuente que limpian y transforman la data a un esquema común (JSON estandarizado) antes de ingresarla a nuestra base de datos central.
    * 
---

## 4. Demo y presentación

### 🎯 Instrucciones para la presentación (Deck compartido)

Usaremos un deck de Google Slides con permisos de edición por equipos. Tu deck ya fue creado con un template.

Por favor sigue estas indicaciones:
- Usa este link (no crees uno nuevo): **https://docs.google.com/presentation/d/1X82o1Qgh3WIPbX1sa081FSTSO21RKsKsmiIWsWWYBac/edit?usp=drivesdk**

Si prefieres hacer tus propias diapositivas fuera del deck, igual transpórtalas al deck compartido antes de la hora límite.

### 📊 Link a tu presentación (solo referencia)

Si tuviste un deck alterno de trabajo: **[URL opcional de tu copia de trabajo]**

### 💻 Link a tu código

Indica dónde vive el código final:
- Si usaste este mismo repositorio: escribe "Código en carpeta `/src` de este repo".
- Si usaste otro repositorio o servicio (Kaggle, GitHub extra, HuggingFace, Vercel, etc.): lista cada enlace claramente.

**Ejemplo (interno):** Código en `/src` + notebooks de exploración en `src/notebooks/`.

**Ejemplo (externo):**
- Repo principal: https://github.com/tu-equipo/proyecto-rimac2025
- Kaggle notebook: https://www.kaggle.com/tuusuario/notebook-procesamiento
- HuggingFace Space (demo): https://huggingface.co/spaces/tu-equipo/app

### 🌐 Link a la demo en vivo (si aplica)

Si desplegaste tu aplicación, comparte el enlace aquí.

**Demo URL:** (https://kfgm7mgsa3.us-east-1.awsapprunner.com/)

**Ejemplo:** https://buscador-doctores.vercel.app

### 🎥 Video de demostración (opcional)

Si crearon un video demo, compártelo aquí.

**Video:** [URL de YouTube / Loom / Google Drive]

---

## (opcional) ¿De qué logros están orgullosos?

> Menciona los logros más significativos de tu proyecto. ¿Qué resultados obtuvieron que consideran importantes o destacables?

**Tu respuesta:**

Estamos orgullosos de:
- **Desfragmentar la salud pública:** Logramos unificar y cruzar con éxito 3 fuentes de datos gubernamentales totalmente desconectadas (RENIPRESS, DIGEMID y CMP) en una sola estructura coherente.
- **Georreferenciación masiva:** Convertimos miles de direcciones en formato texto (con errores tipográficos) en coordenadas precisas para visualizarlas en un mapa interactivo.
- **Validación del Business Case:** Estructuramos una propuesta de valor sólida donde demostramos cómo Rimac puede reducir siniestralidad y costos operativos mediante la autogestión del usuario.
- **Resiliencia Técnica:** A pesar de los desafíos complejos en la limpieza de datos, logramos desplegar un MVP funcional con una experiencia de usuario (UX) limpia y moderna tipo "Airbnb".

---

## (opcional) ¿Qué aprendieron?

> Comparte los aprendizajes más importantes que adquirieron durante el desarrollo del proyecto. ¿Qué nuevas habilidades o conocimientos obtuvieron?

**Aprendizajes técnicos:**

**Tu respuesta:**

- **La realidad de la "Data Sucia":** Aprendimos que el mayor reto no es obtener los datos, sino normalizarlos. Implementamos técnicas de limpieza para estandarizar nombres de especialidades médicas.
- **Geocoding a escala:** Dominamos el uso de librerías geoespaciales para transformar direcciones textuales ambiguas en puntos exactos en el mapa.
- **Arquitectura de Scraping:** Entendimos la importancia de crear scrapers modulares y resilientes para manejar las inconsistencias de los portales del estado.

**Aprendizajes de trabajo en equipo:**

**Tu respuesta:**

- **Estrategia sobre Código:** Aprendimos que dedicar tiempo inicial al diseño de la arquitectura de datos nos ahorró horas de refactorización posterior.
- **Adaptabilidad ante imprevistos:** Comprendimos que en una Hackathon, "hecho es mejor que perfecto". Priorizamos cerrar el ciclo de búsqueda principal (Happy Path) sobre funcionalidades secundarias.
- **Visión de Negocio:** Aprendimos a traducir código técnico en métricas de valor (ahorro de costos y retención) para una corporación como Rimac.

---

## (opcional) ¿Qué harían con más tiempo? opcional

> Ideas de mejora o próximos pasos si tuvieran 1-3 meses adicionales.

**Tu visión:**

**Expansión de funcionalidades:**
- **Integración "Rimac Connect":** Conectar con las APIs internas de la aseguradora para mostrar copagos exactos y deducibles personalizados por usuario.

**Mejoras técnicas (Roadmap V3.0):**
- **IA Inclusiva (SamiBot Voice):** Implementar un asistente de voz basado en LLMs optimizado para adultos mayores y personas con discapacidad visual, justificando el costo de la IA en casos de accesibilidad.
- **Data Pipeline en Tiempo Real:** Automatizar los scrapers para que corran cada mes y detecten cambios en turnos o stock al instante.
