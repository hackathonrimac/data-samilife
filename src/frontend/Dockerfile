FROM node:20-alpine

WORKDIR /app

# Instalar dependencias base
COPY package*.json ./
RUN npm install

# Copiar el resto del código (que luego se montará en desarrollo)
COPY . .

EXPOSE 5173

# Ejecutar servidor de desarrollo de Vite con auto-reload (instala deps si cambian)
CMD ["sh", "-c", "npm install && npm run dev -- --host 0.0.0.0 --port 5173"]
