# Use Node 20 as base image
FROM node:20-slim

# Set working directory
WORKDIR /app

# Copy package definition files first to leverage Docker cache
COPY package.json package-lock.json* ./

# Install dependencies
RUN npm install

# Copy the rest of the application
COPY . .

# Expose Vite's default port
EXPOSE 5173

# Run the development server
# --host is handled in vite.config.ts, but explicit command is safer
CMD ["npm", "run", "dev", "--", "--host"]