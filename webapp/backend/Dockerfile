FROM node:16-alpine

WORKDIR /usr/src/app

RUN apk update && apk add && apk add ffmpeg && apk upgrade
RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools

COPY package*.json ./

RUN npm install

COPY . .

EXPOSE 5000

RUN npm run build

## CMD [ "node", "dist/src/index.js" ]
CMD npm run start
