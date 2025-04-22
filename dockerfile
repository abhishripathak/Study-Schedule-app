# Stage 1: Build React App
FROM node:18-slim AS build

# Set environment variables
ENV NODE_ENV=production
ENV PORT=3000

# Set working directory
WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm install

# Copy application code and build
COPY . .
RUN npm run build

# Stage 2: Serve with Nginx
FROM nginx:alpine

# Remove default nginx static assets
RUN rm -rf /usr/share/nginx/html/*

# Copy built assets from previous stage
COPY --from=build /app/build /usr/share/nginx/html

# Optional: Copy custom nginx config (if any)
# COPY nginx.conf /etc/nginx/nginx.conf

# Expose port 3000 (although Nginx default is 80)
EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
