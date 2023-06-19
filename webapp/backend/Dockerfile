FROM node:16-alpine

WORKDIR /usr/src/app

RUN apk update && apk add && apk add ffmpeg && apk upgrade && apk add python3

COPY package*.json ./

RUN npm install

COPY . .

EXPOSE 5000

RUN npm run build

## CMD [ "node", "dist/src/index.js" ]
CMD npm run start
