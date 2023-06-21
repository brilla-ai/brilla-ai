# NSMQ AI Web application

## Frontend

Frontend is using NextJS. To deploy the frontend locally, run the development server from `webapp/frontend`:

## Environment Variables

This project uses a few environment variables to connect to the backend. You can create a `.env.local` file in the `webapp/frontend` directory to set these variables. The following variables are required:
`BACKEND_VIDEOS_URL=http://localhost:5000/demo-videos/`
This is the URL to the backend videos. This is used to display and play the videos in the frontend.

### Testing

To run all tests in the frontend, run the following command from `webapp/frontend`:

```bash
npm run test
```

### Running

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

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
