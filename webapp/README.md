# Brilla AI Web application

Latest Information on app deployment and setup can be found [here](./streamlitDemo/README.md)

## Frontend

Frontend is using NextJS. To deploy the frontend locally, run the development server from `webapp/frontend`:

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

![homepage](./frontend/public/homepage.png)

You can start editing the page by modifying `webapp/frontend/pages/index.tsx`. The page auto-updates as you edit the file.

## Backend

Backend is using NodeJS with a MongoDB Atlas cluster. To deploy the backend locally, run the development server from `webapp/backend`:

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
