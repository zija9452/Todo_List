# Use an official Node runtime as a parent image
FROM node:18-alpine

# Set environment variables
ENV NODE_ENV=production

# Set working directory
WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm ci --only=production

# Copy project files
COPY . .

# Build the Next.js app
RUN npm run build

# Expose port
EXPOSE 3000

# Start the application
CMD ["npm", "start"]