# src/frontend/Dockerfile

# --- ETAPA 1: CONSTRUCCIÓN (BUILD) ---
FROM node:20-alpine as build

WORKDIR /app

# 1. Copiamos package.json desde src/frontend/
COPY package*.json ./

# variables de entorno (se pasan desde la EC2 en tiempo de build)
ARG VITE_GOOGLE_MAPS_API_KEY
ENV VITE_GOOGLE_MAPS_API_KEY=$VITE_GOOGLE_MAPS_API_KEY


# Instalamos dependencias
RUN npm install

# 2. Copiamos todo el código fuente del frontend
COPY . .

# Construimos la app (Al ser Vite, crea la carpeta 'dist')
RUN npm run build

# --- ETAPA 2: SERVIDOR (NGINX) ---
FROM nginx:alpine

# Copiamos la carpeta 'dist' generada
COPY --from=build /app/dist /usr/share/nginx/html

# Configuramos Nginx para escuchar en el puerto 5173
RUN echo 'server { \
    listen 5173; \
    location / { \
        root /usr/share/nginx/html; \
        index index.html index.htm; \
        try_files $uri $uri/ /index.html; \
    } \
}' > /etc/nginx/conf.d/default.conf

# Exponemos el puerto 5173
EXPOSE 5173

CMD ["nginx", "-g", "daemon off;"]