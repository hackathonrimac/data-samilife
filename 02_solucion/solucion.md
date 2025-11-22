# 📋 Entregable 2: Avances y hallazgos

## 1. ¿Qué hallazgos han tenido?

> Describe los principales descubrimientos y aprendizajes que tu equipo ha realizado hasta ahora.

**Tu respuesta:**

Durante la estructuración de **SamiLife**, hemos validado la complejidad de unificar la data de salud en Perú:

1.  **Fragmentación en RENIPRESS y DIGEMID:** Confirmamos que aunque la data es pública, no es interoperable. Las direcciones en RENIPRESS son texto plano (no coordenadas), lo que nos obligó a implementar un proceso de geocodificación para poder mostrarlas en el mapa tipo "Airbnb".
2.  **Disparidad en Nomenclaturas:** Detectamos que las especialidades médicas no están estandarizadas entre clínicas (ej: "Gastro" vs "Gastroenterología"), lo cual requiere una capa de normalización semántica para que el buscador funcione correctamente.
3.  **Validación de Stock:** Descubrimos que la data de DIGEMID sobre stock de medicamentos es referencial y varía rápidamente, por lo que nuestro modelo debe priorizar la visualización de "disponibilidad probable" basada en la categoría del establecimiento (I, II, III) más que en el stock en tiempo real absoluto.

## 2. ¿En qué se van a enfocar para el cierre?

> Explica en qué aspectos de tu proyecto se concentrará tu equipo durante la fase final.

**Tu respuesta:**

Nos concentraremos en cerrar el MVP para la demostración en vivo:

1.  **Frontend "Look & Feel":** Pulir la interfaz en Next.js para garantizar que la experiencia de usuario sea idéntica a la de reservar un alojamiento (mapa interactivo + tarjetas de clínicas limpias).
2.  **Flujo "Happy Path":** Asegurar que una búsqueda específica (ej: "Pediatría en San Isidro") devuelva resultados coherentes cruzando data de ubicación y especialidad.
3.  **Presentación de Negocio:** Estructurar el pitch deck enfocándonos en el impacto social y la viabilidad comercial, demostrando cómo **SamiLife** reduce el tiempo de atención en emergencias.
4.  **Despliegue del Demo:** Dejar operativa la URL pública del proyecto para que los jueces puedan interactuar con el buscador.
