# Project Documentation

## 1. Introduction

### 1.1 Overview

This document provides detailed information about the project, including its purpose, architecture, setup, APIs, and development workflow.

### 1.2 Target Audience

* **Developers** – For understanding the technical implementation, APIs, and development processes.
* **Product Managers** – For understanding the product’s high-level functionality and user flows.

### 1.3 High-Level Architecture

(Include a diagram if necessary)

## 2. Getting Started

### 2.1 For Developers

#### 2.1.1 Prerequisites

Required software, dependencies, and versions.

* Python 3.8+
* Node 18+
* Git
* Virtual Environment Tools (e.g venv)
* Docker

#### 2.1.2 Setup & Installation

1.  Clone the project using <https://github.com/brilla-ai/brilla-ai.git>
2.  Change directory in `brilla-ai` folder
3.  Change directory into the `webapp` folder
4.  Run `docker compose up`
5.  Open browser and go to <http://localhost:3000/> to view frontend
6.  Open <http://localhost:8000/> in browser for backend docs

### 2.2 For Product Managers

* How to access the system.
* Key user workflows and features.

## 3. Project Structure

### 3.1 Codebase Overview

Description of key directories and files.

**Backend**

**Key Directories:**

* `alembic` – Database migrations using Alembic.
* `core` – Core configurations and settings.
* `databaseStore` – Database connection and query management.
* `helper` – Utility functions and reusable logic.
* `job` – Background jobs and task scheduling.
* `models` – Database models (ORM).
* `router` – API endpoints and routing.
* `services` – Business logic and service layer.
* `websocket` – WebSocket connections and real-time features.

**Key Files:**

* `main.py` – Entry point for the backend server.
* `database.py` – Handles database initialization.
* `requirements.txt` – Lists dependencies for the backend.
* `.gitignore` – Specifies files and directories to be ignored in version control.

**Frontend**

**Key Directories:**

* `apis` – API request handlers.
* `app` – Main application logic and state management.
* `assets/images` – Static assets like images.
* `components` – Reusable UI components.
* `lib` – Utility functions and shared logic.
* `mocks` – Mock data for testing.
* `public` – Static public files.
* `styles` – Global styles and theme definitions.
* `tests` & `tests-examples` – Unit and integration tests.

**Key Files:**

* `README.md` – Documentation for the frontend setup.
* `.gitignore` – Ignore rules for frontend files.
* `.eslintrc.json` – ESLint configuration for code linting.
* `components.json` – Likely a manifest for components.

## 4. Technologies & Dependencies

List of frameworks, libraries, and tools used.

**Backend**

* FastApi
* PostgreSql

**Frontend**

* React / Next js
* Playwright for testing

Justification for choices (brief for PMs).
