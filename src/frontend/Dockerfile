FROM node:20-alpine AS deps
WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm ci

FROM deps AS builder
WORKDIR /app
COPY . .

# Inject API base URL at build time (can be overridden with --build-arg)
ARG VITE_API_URL=http://localhost:8000
ENV VITE_API_URL=${VITE_API_URL}

# Build the production bundle
RUN npm run build

FROM node:20-alpine AS runner
WORKDIR /app

# Lightweight static file server
RUN npm install -g serve

# Copy built assets
COPY --from=builder /app/dist ./dist

EXPOSE 4173

CMD ["serve", "-s", "dist", "-l", "4173"]
