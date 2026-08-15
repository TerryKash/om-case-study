# ADD CODE HERE

FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install --production

COPY . .

EXPOSE 4567

CMD ["node", "index.js"]
