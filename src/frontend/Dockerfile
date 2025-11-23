# src/frontend/Dockerfile

# Etapa 1: Construcción
FROM node:18-alpine as build

WORKDIR /app

# Copiamos package.json y package-lock.json
COPY src/frontend/package*.json ./

# Instalamos dependencias
RUN npm install

# Copiamos el resto del código fuente del frontend
COPY src/frontend/ .

# Construimos la versión de producción
RUN npm run build

# Etapa 2: Servidor Web ligero (Nginx) para servir los archivos
FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
# (Si tu carpeta de salida es 'build' en vez de 'dist', cambia la línea de arriba)

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]