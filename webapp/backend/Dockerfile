FROM node:16-alpine

WORKDIR /usr/src/app

COPY package*.json ./

RUN npm install

## following 3 lines are for installing ffmepg
RUN apk update
RUN apk add
RUN apk add ffmpeg
RUN apk upgrade
RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools

COPY . .

EXPOSE 5000

RUN npm run build

## CMD [ "node", "dist/src/index.js" ]
CMD npm run start
