# src/frontend/Dockerfile

# --- ETAPA 1: CONSTRUCCIÓN ---
FROM node:20-alpine as build

WORKDIR /app

# 1. Rutas corregidas para encontrar los archivos
COPY src/frontend/package*.json ./
RUN npm install

COPY src/frontend/ .

# 2. Construimos la app (Genera la carpeta 'dist')
RUN npm run build

# --- ETAPA 2: SERVIDOR NGINX EN PUERTO 5173 ---
FROM nginx:alpine

# Copiamos los archivos construidos
COPY --from=build /app/dist /usr/share/nginx/html

# 3. Configuramos Nginx para escuchar en el 5173
RUN echo 'server { \
    listen 5173; \
    location / { \
        root /usr/share/nginx/html; \
        index index.html index.htm; \
        try_files $uri $uri/ /index.html; \
    } \
}' > /etc/nginx/conf.d/default.conf

# 4. Exponemos el puerto deseado
EXPOSE 5173

CMD ["nginx", "-g", "daemon off;"]