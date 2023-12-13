FROM node:alpine

WORKDIR /app

COPY package.json .
RUN npm i

COPY . .

EXPOSE 1573

CMD [ "npm", "run", "dev" ]
