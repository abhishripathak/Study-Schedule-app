# Use official Node.js image
FROM node:18-slim

# Set environment variables
ENV NODE_ENV=production
ENV PORT=3000

# Set working directory
WORKDIR /app

# Install app dependencies
COPY package*.json ./
RUN npm install

# Copy the rest of the app
COPY . .

# Build the React app
RUN npm run build

# Use a lightweight web server to serve static files
FROM nginx:alpine
COPY --from=0 /app/build /usr/share/nginx/html

# Expose port
EXPOSE 3000

# Start nginx server
CMD ["nginx", "-g", "daemon off;"]
