# ---------- Stage 1: build the React app ----------
FROM node:20-alpine AS build
WORKDIR /app

# Install dependencies first for better layer caching
COPY package*.json ./
RUN npm ci

COPY . .

# VITE_API_BASE_URL is baked in at build time (client-side env values are
# visible in the browser bundle -- never put secrets here)
ARG VITE_API_BASE_URL=/api/v1
ENV VITE_API_BASE_URL=$VITE_API_BASE_URL

RUN npm run build

# ---------- Stage 2: serve with a lightweight web server ----------
FROM nginx:1.27-alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf


EXPOSE 80
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD wget -qO- http://localhost:80/ || exit 1

CMD ["nginx", "-g", "daemon off;"]
