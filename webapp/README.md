# NSMQ AI Web application

## Frontend

Front end is using NextJS. To deploy it locally, run the development server from `webapp/frontend`:

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

![homepage](./frontend/public/homepage.png)

You can start editing the page by modifying `webapp/frontend/pages/index.tsx`. The page auto-updates as you edit the file.

## Backend

Backend is using NodeJS. To deploy it locally, run the development server from `webapp/backend`:

### Server

- Entry point for application: server.ts.

Run the following command to install node modules

```bash
npm install 
```

Use the following commands to start the server

```bash
npm run start
```

```bash
npm run watch
```

Visit <https://localhost:5000> with your browser to see the result.

### Testing

- Testing framework: Jasmine.

Run the following command to test application

```bash
npm run test
```

## Database

Coming soon
