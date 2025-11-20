# Código fuente del proyecto

Esta carpeta puedes poner el código fuente de tu solución.

## 📁 Estructura sugerida

### Para aplicaciones web full-stack:
```
src/
├── frontend/           # Código del frontend
│   ├── components/     # Componentes React/Vue
│   ├── pages/          # Páginas de la aplicación
│   ├── styles/         # Estilos CSS/Tailwind
│   └── utils/          # Utilidades del frontend
├── backend/            # Código del backend
│   ├── api/            # Endpoints de la API
│   ├── models/         # Modelos de datos
│   ├── services/       # Lógica de negocio
│   └── utils/          # Utilidades del backend
└── shared/             # Código compartido
    ├── types/          # Tipos TypeScript compartidos
    └── constants/      # Constantes
```

### Para proyectos de Data Science / ML:
```
src/
├── data/               # Scripts de obtención/procesamiento de datos
│   ├── scraping/       # Web scrapers
│   ├── etl/            # Pipelines ETL
│   └── preprocessing/  # Limpieza y normalización
├── models/             # Modelos de ML
│   ├── training/       # Scripts de entrenamiento
│   └── inference/      # Scripts de predicción
├── api/                # API para servir el modelo
└── notebooks/          # Jupyter notebooks para análisis
```

### Para aplicaciones móviles:
```
src/
├── screens/            # Pantallas de la app
├── components/         # Componentes reutilizables
├── navigation/         # Configuración de navegación
├── services/           # Servicios (APIs, auth, etc.)
├── store/              # Estado global (Redux, Context)
├── assets/             # Assets de la app (íconos, fonts)
└── utils/              # Utilidades y helpers
```

## 📝 Buenas prácticas

### 1. README.md en src/
Crea un README.md dentro de `src/` explicando:
- Cómo instalar dependencias
- Cómo ejecutar el proyecto localmente
- Variables de entorno necesarias
- Comandos principales

### 2. Configuración
Incluye archivos de configuración necesarios:
- `package.json` (Node.js)
- `requirements.txt` o `pyproject.toml` (Python)
- `.env.example` (template de variables de entorno)
- `docker-compose.yml` (si usas Docker)

### 3. Documentación del código
- Comenta funciones complejas
- Usa nombres descriptivos para variables y funciones
- Documenta la API con Swagger/OpenAPI si aplica

### 4. Testing
Si tienes tiempo, incluye tests:
```
src/
├── __tests__/          # Tests unitarios
├── e2e/                # Tests end-to-end
└── coverage/           # Reportes de cobertura
```

## 🚀 Ejemplo de README.md para tu proyecto

Crea un archivo `src/README.md` con este template:

```markdown
# [Nombre del Proyecto]

## Descripción
[Breve descripción de tu solución]

## Tecnologías
- Frontend: [Next.js, React, etc.]
- Backend: [FastAPI, Node.js, etc.]
- Base de datos: [PostgreSQL, MongoDB, etc.]
- Cloud: [AWS, Azure, etc.]

## Instalación

### Prerrequisitos
- Node.js 18+
- Python 3.11+
- Docker (opcional)

### Backend
```bash
cd src/backend
pip install -r requirements.txt
python main.py
```

### Frontend
```bash
cd src/frontend
npm install
npm run dev
```

## Variables de entorno
Copia `.env.example` a `.env` y configura:
```
DATABASE_URL=postgresql://...
OPENAI_API_KEY=sk-...
AWS_ACCESS_KEY_ID=...
```

## Uso
1. Inicia el backend: `python src/backend/main.py`
2. Inicia el frontend: `npm run dev --prefix src/frontend`
3. Abre http://localhost:3000

## API Endpoints
- `GET /api/doctors` - Lista de doctores
- `POST /api/search` - Búsqueda inteligente
- `GET /api/clinics` - Lista de clínicas

## Estructura del proyecto
[Describe la estructura de carpetas]

## Contribuciones
[Nombres de los miembros del equipo y sus contribuciones]
```

## 💡 Tips importantes

1. **Commits descriptivos:** Usa mensajes claros como "Añade endpoint de búsqueda de doctores" en lugar de "fix"

2. **Gitignore:** Asegúrate de tener un `.gitignore` apropiado:
   ```
   node_modules/
   __pycache__/
   .env
   .venv/
   dist/
   build/
   *.pyc
   .DS_Store
   ```

3. **Organización:** Mantén el código organizado por responsabilidad (separación de concerns)

4. **Documentación inline:** Si una función hace algo complejo, documéntala

5. **Manejo de errores:** Implementa manejo de errores apropiado, no dejes que la app crashee

---

## ⚠️ Nota importante

Recuerda que los jueces revisarán tu código. Aunque no tiene que ser perfecto, debe ser:
- ✅ Legible y bien organizado
- ✅ Funcional (que corra sin errores)
- ✅ Documentado (al menos lo básico)
- ✅ Reproducible (que otros puedan ejecutarlo)

No necesitas código de producción enterprise-grade, pero sí mostrar buenas prácticas y que entiendes lo que estás haciendo.

**¡Enfócate en un MVP funcional antes que en código perfecto!** 🚀
