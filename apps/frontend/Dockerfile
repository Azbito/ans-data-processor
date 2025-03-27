FROM node:lts AS development
WORKDIR /app
COPY apps/frontend ./frontend
WORKDIR /app/frontend
RUN npm install
EXPOSE 5173
CMD ["npm", "run", "dev", "--", "--host"]
