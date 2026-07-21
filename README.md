# WorkShip AI

## Project Overview

WorkShip AI is an enterprise-grade Software-as-a-Service (SaaS) platform designed to centralize knowledge management, incident intelligence, and team collaboration through artificial intelligence (specifically documentation search, incident tracking, and knowledge retrieval) within a secure, multi-tenant environment. By leveraging advanced AI capabilities—including semantic search, Retrieval-Augmented Generation (RAG), and an AI Copilot—WorkShip AI empowers organizations to transform unstructured institutional knowledge into actionable insights, reduce mean time to resolution (MTTR) for incidents, and enhance cross-functional decision making.

### Problem It Solves
Modern enterprises struggle with scattered knowledge silos, slow incident response times, and inefficient information retrieval. Employees waste hours searching across disconnected systems (Confluence, SharePoint, email, etc.) for critical information. WorkShip AI unifies these knowledge sources into a single, searchable repository with AI-powered context awareness, ensuring the right information is available at the right time.

### Key Features
- **Multi-Tenant Architecture**: Secure isolation between customer organizations (workspaces)
- **AI-Powered Semantic Search**: Natural language query understanding via sentence transformers and pgvector
- **AI Copilot**: Conversational interface for knowledge retrieval using Retrieval-Augmented Generation (RAG)
- **Incident Intelligence**: Structured incident tracking with severity levels, ownership, and post-mortem analysis
- **Document Management**: Full lifecycle handling of enterprise documents with metadata extraction
- **Role-Based Access Control (RBAC)**: Fine-grained permissions for CEO, Admin, Manager, Engineer, Employee, Viewer roles
- **Real-Time Dashboard**: Operational metrics and KPIs scoped to each-grained permissions for CEO, Admin, Manager, Engineer, Employee, Viewer roles
- **Real-Time Dashboard**: Operational metrics and KPIs scoped to each tenant
- **Dark Mode & Responsive UI**: Modern React-based interface with Theme UI
- **RESTful API**: Comprehensive backend API with OpenAPI documentation
- **Event-Driven Architecture**: Asynchronous processing for embeddings and notifications

### Technologies Used
- **Backend**: FastAPI (Python), SQLAlchemy ORM, Pydantic, Alembic
- **Database**: PostgreSQL with pgvector extension for vector similarity search
- **AI/ML**: Sentence Transformers (`all-MiniLM-L6-v2`) for document embeddings
- **Frontend**: React 18, TypeScript, Next.js 13+, Tailwind CSS, Headless UI
- **Authentication**: JWT (JSON Web Tokens) with refresh token rotation
- **Infrastructure**: Docker, Ubuntu-based containers, Gunicorn/Uvicorn workers
- **DevOps**: GitHub Actions, Render.com deployment, Sentry error tracking

### High-Level Architecture
```mermaid
graph TD
    A[Client Browser] -->|HTTPS/WSS| B(Load Balancer)
    B --> C[API Gateway]
    C --> D[Auth Service]
    C --> E[Document Service]
    C --> F[Incident Service]
    C --> G[Dashboard Service]
    C --> H[Copilot Service]
    D --> I[(PostgreSQL)]
    E --> I
    F --> I
    G --> I
    H --> I
    E --> J[(pgvector)]
    H --> J
    H --> K[Sentence Transformer Model]
    style I fill:#f9f,stroke:#333
    style J fill:#bbf,stroke:#333
    style K fill:#bfb,stroke:#333
```

## Project Architecture

### Backend Structure
```
backend/
│
├── app/
│   ├── api/                 # Route handlers and request validation
│   │   ├── auth.py          # Authentication endpoints (register, login, etc.)
│   │   ├── copilot.py       # AI Copilot query endpoint
│   │   ├── dashboard.py     # Dashboard metrics and analytics
│   │   ├── documents.py     # CRUD operations for documents
│   │   ├── employees.py     # Employee/user management
│   │   ├── health.py        # Health check endpoints
│   │   ├── incidents.py     # Incident tracking and simulation
│   │   ├── meetings.py      # Meeting scheduling and history
│   │   ├── router.py        # Main API router aggregation
│   │   ├── search.py        # Semantic search endpoints
│   │   ├── services.py      # Service dependency management
│   │   └── teams.py         # Team/org structure management
│   │
│   ├── core/                # Core configuration and utilities
│   │   ├── config.py        # Environment-based configuration (Pydantic Settings)
│   │   ├── exceptions.py    # Custom HTTP exception classes
│   │   ├── logging.py       # Structured logging setup
│   │   └── security.py      # Password hashing, JWT token handling
│   │
│   ├── models/              # SQLAlchemy ORM models
│   │   ├── __init__.py
│   │   ├── document.py      # Document metadata and content
│   │   ├── employee.py      # User accounts with role and workspace
│   │   ├── incident.py      # Incident tracking with severity/status
│   │   ├── log_entry.py     # Audit trail for system events
│   │   ├── meeting.py       # Scheduled meetings and attendees
│   │   ├── refresh_token.py # Refresh token storage and validation
│   │   ├── service.py       # Service catalog and ownership
│   │   ├── team.py          # Organizational teams and hierarchy
│   │   └── workspace.py     # Tenant isolation boundary
│   │
│   ├── repositories/        # Data access layer (repository pattern)
│   │   ├── __init__.py
│   │   ├── base.py          # Generic CRUD base class
│   │   ├── dashboard.py     # Aggregated queries for dashboard (FIXED: workspace-scoped)
│   │   ├── document.py      # Document queries with semantic search
│   │   ├── employee.py      # Employee queries with role filtering
│   │   ├── incident.py      # Incident queries with severity/status
│   │   ├── meeting.py       # Meeting queries with date filtering
│   │   ├── service.py       # Service queries with criticality filtering
│   │   └── team.py          # Team queries with name/search filtering
│   │
│   ├── services/            # Business logic layer
│   │   ├── __init__.py
│   │   ├── copilot.py       # AI Copilot service (FIXED: workspace injection)
│   │   ├── dashboard.py     # Dashboard aggregation service (FIXED: workspace injection)
│   │   ├── document_processing.py # Text normalization and metadata extraction
│   │   ├── document.py      # Document CRUD with embedding generation
│   │   ├── embedding.py     # Embedding generation and backfill service
│   │   ├── employee.py      # Employee creation/update with password hashing
│   │   ├── incident.py      # Incident lifecycle management
│   │   ├── meeting.py       # Meeting scheduling and updates
│   │   ├── service.py       # Service catalog management
│   │   └── team.py          # Team creation and hierarchy management
│   │
│   ├── schemas/             # Pydantic models for request/response validation
│   │   ├── __init__.py
│   │   ├── auth.py          # Registration, login, token models
│   │   ├── common.py        # Shared schemas (paginated responses, messages)
│   │   ├── copilot.py       # Copilot query/response schemas
│   │   ├── dashboard.py     # Dashboard response schemas
│   │   ├── document.py      # Document create/update/read schemas
│   │   ├── employee.py      # Employee create/update/read schemas
│   │   ├── incident.py      # Incident create/update/read schemas
│   │   ├── meeting.py       # Meeting create/update/read schemas
│   │   ├── search.py        # Search query and result schemas
│   │   ├── service.py       # Service create/update/read schemas
│   │   └── team.py          # Team create/update/read schemas
│   │
│   ├── dependencies/        # FastAPI dependency providers
│   │   └── deps.py          # Database session, current user, workspace resolution
│   │
│   ├── middleware/          # Custom HTTP middleware
│   │   └── (currently none, rate limiting in main.py)
│   │
│   └── utils/               # Utility functions
│       └── document_processing.py # Text cleaning, summarization, section splitting
│
├── alembic/                 # Database migration scripts
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
│       ├── ...              # Migration files (timestamped)
│
├── tests/                   # Test suite (not shown in context but implied)
│
├── requirements.txt         # Python package dependencies
├── main.py                  # FastAPI application entry point
├── backfill_embeddings.py   # CLI tool for generating missing document embeddings
├ ├── .env.example             # Template environment configuration
└── Dockerfile               # Container build instructions (implied)
```

### Frontend Structure
```
frontend/
│
├── src/
│   ├── components/          # Reusable UI components
│   │   ├── app-shell.tsx    # Main layout wrapper (sidebar, header)
│   │   ├── copilot-chat.tsx # AI Copilot chat interface
│   │   ├── logo.tsx         # Company logo component
│   │   ├── nav-item.tsx     # Sidebar navigation item
│   │   ├── navbar.tsx       # Responsive navigation bar
│   │   └── page-container.tsx # Page content container with padding
│   │   └── sidebar.tsx      # Collapsible sidebar navigation
│   │
│   ├── pages/               # Next.js pages (route components)
│   │   ├── app/
│   │   │   ├── company-sales/ # Sales analytics dashboard
│   │   │   │   └── page.tsx
│   │   │   ├── copilot/       # AI Copilot interface
│   │   │   │   └── page.tsx
│   │   │   ├── dashboard/     # Operational metrics dashboard
│   │   │   │   └── page.tsx
│   │   │   ├── incidents/     # Incident tracking and reporting
│   │   │   │   └── page.tsx
│   │   │   ├── knowledge/     # Knowledge base document library
│   │   │   │   └── page.tsx
│   │   │   ├── settings/      # User and workspace settings
│   │   │   │   └── page.tsx
│   │   │   └── page.tsx       # Landing page/homepage
│   │   │
│   │   ├── favicon.ico
│   │   ├── globals.css      # Global Tailwind CSS overrides
│   │   └── layout.tsx       # Root layout with providers
│   │
│   ├── hooks/               # Custom React hooks
│   │   ├── (examples: useAuth, useApi, useWorkspace)
│   │
│   ├── services/            # API service clients
│   │   ├── api.ts           # Centralized API client with interceptors
│   │   ├── authService.ts   # Authentication endpoint wrappers
│   │   ├── copilotService.ts # Copilot query handling
│   │   ├── dashboardService.ts # Dashboard metrics fetching
│   │   ├── documentService.ts # Document CRUD operations
│   │   ├── incidentService.ts # Incident tracking API
│   │   ├── meetingService.ts # Meeting scheduling API
│   │   ├── searchService.ts  # Semantic search interface
│   │   └── teamService.ts    # Team management API
│   │
│   ├── context/             # React context providers
│   │   ├── AuthContext.ts   # User authentication state
│   │   ├── ThemeContext.ts  # Dark/light mode toggle
│   │   └── WorkspaceContext.ts # Current tenant isolation
│   │
│   ├── layouts/             # Page layout wrappers
│   │   ├── AuthLayout.tsx   # Layout for login/register pages
│   │   └── DefaultLayout.tsx # Layout for authenticated pages
│   │
│   ├── assets/              # Static assets (images, icons, fonts)
│   │   ├── icons/
│   │   └── illustrations/
│   │
│   └── utils/               # Utility functions and constants
│       ├── apiConstants.ts  # API endpoint definitions
│   │   ├── dateUtils.ts     # Date formatting helpers
│   │   └── validation.ts    # Form validation schemas
│
├── public/                  # Static files served directly
│   ├── file.svg
│   ├── globe.svg
│   ├── logo.png
│   ├── next.svg
│   ├── vercel.svg
│   └── window.svg
│
├── package.json             # Node.js dependencies and scripts
├── next.config.ts           # Next.js configuration
├── tsconfig.json            # TypeScript configuration
├── postcss.config.mjs       # PostCSS/Tailwind configuration
├── eslint.config.mjs        # ESLint configuration
└── components.json          # Shadcn/UI component registry
```

### Backend Architecture Details

#### FastAPI Architecture & Request Flow
1. **Entry Point**: `main.py` creates the FastAPI application instance
2. **Lifespan Events**: Database connection initialization on startup
3. **Middleware Chain**:
   - CORS middleware (environment-configured origins)
   - Custom rate limiting middleware for `/auth/*` endpoints (5/minute/IP)
   - Built-in exception handling for 404/409 errors
4. **Routing**: `api/router.py` aggregates all feature routers
5. **Dependency Injection**: 
   - Database session via `get_db()` (yields SQLAlchemy Session)
   - Current user via `get_current_active_user()` (validates JWT, fetches Employee)
   - Current workspace via `get_current_workspace()` (returns Workspace from user.workspace_id)
   - Service layer dependencies inject db and workspace_id
6. **Request Processing**:
   - HTTP request received by FastAPI
   - Middleware executes (CORS, rate limiting)
   - Route handler validates request via Pydantic schemas
   - Dependencies resolved (db, user, workspace)
   - Service layer processes business logic
   - Repository layer executes database queries
   - Response serialized via Pydantic models and returned

#### Authentication Flow
```mermaid
sequenceDiagram
    participant Client as Browser
    participant API as FastAPI
    participant Auth as Auth Service
    participant DB as PostgreSQL

    Client->>API: POST /auth/register (email, password, name)
    API->>DB: Check email uniqueness per workspace
    alt Email exists
        DB-->>API: Conflict error
        API-->>Client: 400 Bad Request
    else Email available
        DB->>BCrypt: Hash password
        DB->>DB: Store employee record
        DB-->>API: Success
        API-->>Client: 201 Created (user data)
    end

    Client->>API: POST /auth/login (email, password)
    API->>DB: Find employee by email
    alt Employee not found OR password incorrect
        DB-->>API: Not found/null
        API-->>Client: 401 Unauthorized
    else Employee found AND password correct
        API->>Security: Create access token (JWT)
        API->>Security: Create refresh token (JWT)
        API->>DB: Store refresh token record
        DB-->>API: Success
        API-->>Client: 200 OK {access_token, refresh_token}
    end

    Client->>API: GET /protected-endpoint (Bearer <access_token>)
    API->>Security: Decode and validate JWT
    alt Token invalid/expired
        Security-->>API: JWTError
        API-->>Client: 401 Unauthorized
    else Token valid
        API->>DB: Fetch employee by token subject (user_id)
        alt Employee not found OR inactive
            DB-->>API: Not found/null
            API-->>Client: 404/400
        else Employee found AND active
            API->>Service: Process request with employee context
            Service->>Repository: Apply workspace_id filter
            Repository-->>Service: Tenant-scoped data
            Service-->>API: Processed result
            API-->>Client: 200 OK
        end
    end

    Client->>API: POST /auth/refresh-token (refresh_token)
    API->>DB: Find valid, non-revoked refresh token
    alt Token not found/expired/revoked
        DB-->>API: Null
        API-->>Client: 401/400
    else Token valid
        API->>Security: Create new access token
        API-->>Client: 200 OK {access_token, same refresh_token}
    end

    Client->>API: POST /auth/logout (refresh_token)
    API->>DB: Find refresh token for current user
    alt Token found
        DB->>DB: Mark token as revoked
        DB-->>API: Success
        API-->>Client: 200 OK {msg}
    else Token not found
        API-->>Client: 401 Unauthorized
    end
```

#### Repository Pattern
- **Purpose**: Abstract data access logic, provide tenant-scoped queries
- **Implementation**: Each entity has a repository class inheriting from `BaseRepository[Model]`
- **Tenancy Enforcement**: 
  - Repository methods accept optional `workspace_id` parameter
  - All queries include `.where(model.workspace_id == workspace_id)` when provided
  - Service layer ensures workspace_id is always passed from authenticated user
- **Key Files**: 
  - `backend/app/repositories/base.py`: Generic CRUD operations
  - Entity-specific repositories (document.py, employee.py, etc.)

#### Service Layer
- **Purpose**: Encapsulate business logic, coordinate repositories, handle transactions
- **Implementation**: 
  - Each entity has a service class (`DocumentService`, `EmployeeService`, etc.)
  - Services receive `db: Session` and `workspace_id: UUID` in constructor
  - Services delegate data access to repositories
  - Services handle validation, preprocessing (e.g., password hashing, document processing)
- **Key Files**: 
  - `backend/app/services/document.py`: Document creation with embedding generation
  - `backend/app/services/copilot.py`: AI Copilot query orchestration (FIXED)

#### JWT Authentication
- **Token Types**:
  - Access Token: Short-lived (30 minutes), contains `sub` (user ID)
  - Refresh Token: Long-lived (7 days), stored in database with expiration and revocation flag
- **Creation**: 
  - `security.create_access_token()` and `security.create_refresh_token()`
  - Uses HS256 algorithm with `SECRET_KEY` from environment
- **Validation**: 
  - `security.decode_token()` verifies signature and expiration
  - `deps.get_current_user()` extracts user ID from token and fetches employee
- **Security**: 
  - No sensitive data in tokens (only user ID)
  - Refresh tokens stored hashed in database (implied by security best practices)

#### Workspace Multi-Tenancy
- **Isolation Boundary**: `workspace_id` foreign key on all tenant-scoped tables
- **Enforcement Points**:
  1. **Database Schema**: `workspace_id` column with foreign key to `workspaces.id`
  2. **Repositories**: All queries filter by `workspace_id`
  3. **Services**: Constructor requires `workspace_id`, stored as instance variable
  4. **API Dependencies**: `get_current_workspace()` resolves from authenticated user
  5. **Dashboard/Copilot**: Fixed to properly scope queries (see Critical Fixes)
- **Workspace Model**: 
  - `company_name`: Display name of the organization
  - `slug`: Unique identifier for subdomain/path routing
  - `plan`: Subscription tier (free/pro/enterprise)
  - `logo`: Optional brand logo URL

#### AI Search Pipeline
graph LR
    A[Document Upload] --> B[Document Processing Service]
    B --> C[Clean & Normalize Text]
    C --> D[Extract Metadata (tags, summary)]
    D --> E[Generate Embedding]
    E --> F[Store Embedding in pgvector Column]
    F --> G[Document Available for Search]
    
    G --> H[Semantic Search Query]
    H --> I[Generate Query Embedding]
    I --> J[pgvector Cosine Similarity Search]
    J --> K[Return Documents + Similarity Scores]
    K --> L[RAG Context Assembly]
    L --> M[AI Copilot Response Generation]
    
    style E fill:#bfb,stroke:#333
    style I fill:#bfb,stroke:#333
    style J fill:#ff9,stroke:#333
```

#### Database Relationships
```mermaid
erDiagram
    WORKSPACE ||--o{ EMPLOYEE : "contains"
    WORKSPACE ||--o{ DOCUMENT : "owns"
    WORKSPACE ||--o{ INCIDENT : "owns"
    WORKSPACE ||--o{ MEETING : "owns"
    WORKSPACE ||--o{ SERVICE : "owns"
    WORKSPACE ||--o{ TEAM : "owns"
    
    EMPLOYEE ||--o{ TEAM : "belongs to"
    EMPLOYEE }o--|| EMPLOYEE : "manages"
    EMPLOYEE ||--o{ INCIDENT : "reports"
    EMPLOYEE ||--o{ MEETING : "attends"
    EMPLOYEE ||--o{ SERVICE : "owns"
    
    TEAM ||--o{ EMPLOYEE : "has members"
    TEAM ||--o{ SERVICE : "owns"
    TEAM ||--o{ INCIDENT : "owns"
    
    SERVICE ||--o{ INCIDENT : "related to"
    SERVICE }o--|| TEAM : "owned by"
    
    DOCUMENT }|..|{ INCIDENT : "references"
    DOCUMENT }|..|{ MEETING : "references"
    
    WORKSPACE {
        UUID id PK
        STRING company_name
        STRING slug UK
        STRING logo
        STRING plan
        TIMESTAMP created_at
        TIMESTAMP updated_at
    }
    EMPLOYEE {
        UUID id PK
        UUID workspace_id FK
        STRING first_name
        STRING last_name
        STRING full_name
        STRING email UK
        STRING password_hash
        STRING role
        BOOLEAN is_active
        STRING avatar
        STRING phone
        STRING department
        STRING job_title
        UUID manager_id FK
        UUID team_id FK
        TIMESTAMP last_login
        TIMESTAMP created_at
        TIMESTAMP updated_at
    }
    DOCUMENT {
        UUID id PK
        UUID workspace_id FK
        STRING title
        TEXT content
        STRING category
        STRING source
        STRING summary
        JSON tags
        INTEGER reading_time_minutes
        JSON sections
        JSON metadata
        VECTOR embedding
        TIMESTAMP created_at
        TIMESTAMP updated_at
    }
    INCIDENT {
        UUID id PK
        UUID workspace_id FK
        STRING title
        TEXT description
        STRING severity
        STRING status
        UUID service_id FK
        UUID owner_team_id FK
        TIMESTAMP created_at
        TIMESTAMP updated_at
    }
    MEETING {
        UUID id PK
        UUID workspace_id FK
        STRING title
        TEXT description
        DATE date
        TIME start_time
        TIME end_time
        JSON attendees
        TIMESTAMP created_at
        TIMESTAMP updated_at
    }
    SERVICE {
        UUID id PK
        UUID workspace_id FK
        STRING name
        STRING description
        STRING criticality
        UUID owner_team_id FK
        TIMESTAMP created_at
        TIMESTAMP updated_at
    }
    TEAM {
        UUID id PK
        UUID workspace_id FK
        STRING name
        STRING description
        TIMESTAMP created_at
        TIMESTAMP updated_at
    }
    REFRESH_TOKEN {
        UUID id PK
        UUID user_id FK
        STRING token
        TIMESTAMP expires_at
        BOOLEAN revoked
        TIMESTAMP created_at
    }
```

### Frontend Architecture Details

#### React Structure & Routing
- **Framework**: Next.js 13+ with App Router
- **Routing**: File-system based in `/src/app/` directory
  - `/app/page.tsx` → `/` (landing page)
  - `/app/dashboard/page.tsx` → `/dashboard`
  - `/app/copilot/page.tsx` → `/copilot`
  - etc.
- **Layouts**: 
  - Root layout (`src/app/layout.tsx`) provides global providers
  - Auth layout (`src/layouts/AuthLayout.tsx`) for login/register
  - Default layout (`src/layouts/DefaultLayout.tsx`) for authenticated pages

#### State Management
- **React Context**: 
  - `AuthContext`: Manages user authentication state (token, user profile)
  - `WorkspaceContext`: Stores current workspace information
  - `ThemeContext`: Tracks dark/light mode preference
- **Data Fetching**: 
  - Custom hooks (`useAuth`, useApi) handle API requests
  - SWR or React Query implied for caching and background updates
- **Form State**: React Hook Form with Zod validation implied

#### Authentication Flow
1. **Login**: 
   - User submits credentials to `/api/auth/login`
   - Receive JWT access/refresh tokens
   - Store access token in memory (or HTTP-only cookie implied)
   - Store refresh token in HTTP-only cookie or localStorage (security consideration)
   - Redirect to dashboard
2. **Token Refresh**: 
   - Background job or request interceptor detects expired access token
   - Use refresh token to get new access token via `/api/auth/refresh-token`
   - Update stored access token
3. **Logout**: 
   - Call `/api/auth/logout` with refresh token
   - Clear client-side tokens
   - Redirect to login page

#### API Communication
- **Base URL**: Defined in `src/utils/apiConstants.ts` (environment-dependent)
- **Client**: Centralized `api.ts` service with:
  - Automatic JWT attachment to requests
  - Response interceptors for error handling
  - Request/response logging (development)
  - Retry logic for transient failures
- **Endpoints**: Feature-specific services (documentService, incidentService, etc.) wrap API calls

#### Component Hierarchy
```mermaid
graph TD
    A[Next.js App] --> B[Root Layout]
    B --> C[ThemeContext.Provider]
    C --> D[AuthContext.Provider]
    D --> E[WorkspaceContext.Provider]
    E --> F[AppShell Component]
    F --> G[Navbar Component]
    F --> H[Sidebar Component]
    F --> I[PageContainer Component]
    I --> J[Route-specific Page]
    J --> K[Feature Components]
    K --> L[Reusable UI Elements]
    
    style B fill:#f9f,stroke:#333
    style C fill:#9f9,stroke:#333
    style D fill:#99f,stroke:#333
    style E fill:#f99,stroke:#333
```

#### Theme/Dark Mode
- **Implementation**: 
  - Tailwind CSS with dark mode class strategy
  - Theme context stores boolean (`isDark`)
  - Root `<html>` element gets `dark` class when `isDark=true`
  - Component classes use `dark:` prefixed variants
- **Persistence**: User preference stored in localStorage
- **Toggle**: Available in user settings or sidebar menu

#### Dashboard Architecture
- **Composition**: 
  - Multiple KPI cards (total employees, incidents, etc.)
  - Charts (incident trends, service status distribution)
  - Recent activity tables (incidents, meetings, documents)
- **Data Fetching**: 
  - Single `/api/dashboard` endpoint returns all required data
  - Backend performs aggregated queries (FIXED: now workspace-scoped)
  - Frontend renders loading states, error boundaries
- **Refresh**: 
  - Automatic refresh every 5 minutes
  - Manual refresh button available

### Database Schema Details

#### Tables Overview
| Table | Purpose | Primary Key | Foreign Keys |
|-------|---------|-------------|--------------|
| `workspaces` | Tenant isolation boundary | `id` | None |
| `employees` | User accounts within workspace | `id` | `workspace_id → workspaces.id`, `manager_id → employees.id`, `team_id → teams.id` |
| `documents` | Knowledge base documents | `id` | `workspace_id → workspaces.id` |
| `incidents` | Incident tracking and management | `id` | `workspace_id → workspaces.id`, `service_id → services.id`, `owner_team_id → teams.id` |
| `meetings` | Scheduled meetings and attendees | `id` | `workspace_id → workspaces.id` |
| `services` | Service catalog and ownership | `id` | `workspace_id → workspaces.id`, `owner_team_id → teams.id` |
| `teams` | Organizational team structure | `id` | `workspace_id → workspaces.id` |
| `refresh_token` | JWT refresh token storage | `id` | `user_id → employees.id` |
| `log_entry` | Audit trail for system events | `id` | None (system-wide) |

#### Key Constraints & Indexes
- **Unique Constraints**:
  - `employees`: `(workspace_id, email)` → prevents duplicate emails per workspace
  - `workspaces`: `slug` → ensures unique workspace identifiers
- **Indexes**:
  - `employees.email` → fast login lookup
  - `documents.workspace_id` → efficient workspace foreign key` → tenant-scoped queries
  - `incidents.workspace_id` → tenant-scoped queries
  - `pgvector` index on `documents.embedding` → efficient similarity search
- **Cascade Deletes**:
  - Not implemented explicitly; application handles cleanup via service layer
  - On workspace deletion: all related records should be deleted (cascading implied in service logic)

### Environment Variables

| Variable | Description | Required | Example |
|----------|-------------|----------|---------|
| `DATABASE_URL` | PostgreSQL connection string | Yes | `postgresql+psycopg://user:pass@host:5432/dbname` |
| `SECRET_KEY` | Secret for JWT signing (HS256) | Yes | `32+character-random-string` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Access token lifetime | No (default: 30) | `30` |
| `REFRESH_TOKEN_EXPIRE_DAYS` | Refresh token lifetime | No (default: 7) | `7` |
| `OPENAI_API_KEY` | OpenAI API key (for future LLM features) | No | `sk-...` |
| `SUPABASE_URL` | Supabase project URL (if using Supabase) | No | `https://xyz.supabase.co` |
| `SUPABASE_KEY` | Supabase anon/public key | No | `public-anon-key` |
| `BACKEND_CORS_ORIGINS` | Comma-separated list of allowed origins | No (secure default: same-origin) | `https://app.workshipai.com,https://staging.workshipai.com` |

> **Note**: Never commit actual secrets to version control. Use `.env.example` as template and manage secrets via platform-specific secret management (Render.com Environment Variables, Docker secrets, etc.)

## Installation Guide

### Prerequisites
- Python 3.11+
- Node.js 18+ and npm
- PostgreSQL 14+ with pgvector extension
- Git

### Backend Setup
```bash
# Clone repository
git clone https://github.com/your-org/workship-ai.git
cd workship-ai/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your actual values (SEE: Environment Variables section)

# Initialize database and run migrations
alembic upgrade head

# Start development server
uvicorn main:app --reload
```
Server will be available at `http://localhost:8000`

### Frontend Setup
```bash
cd ../frontend

# Install dependencies
npm install

# Set up environment variables (create .env.local)
# NEXT_PUBLIC_API_URL=http://localhost:8000
# NEXT_PUBLIC_BACKEND_URL=http://localhost:8000

# Start development server
npm run dev
```
Application will be available at `http://localhost:3000`

## Running the Project

### Backend
- **Development**: `uvicorn main:app --reload` (auto-reload on code changes)
- **Production**: `gunicorn main:app -k uvicorn.workers.UvicornWorker -w 4`
- **Database Migrations**: 
  - Create migration: `alembic revision --autogenerate -m "description"`
  - Apply migration: `alembic upgrade head`
  - Rollback: `alembic downgrade -1`

### Frontend
- **Development**: `npm run dev` (Next.js dev server with HMR)
- **Production Build**: `npm run build`
- **Production Start**: `npm start` (serves `.next` output)

### Database
- **PostgreSQL Requirements**:
  - Enable pgvector extension: `CREATE EXTENSION IF NOT EXISTS vector;`
  - Recommended settings: `shared_buffers=256MB`, `max_connections=100`
- **Connection Testing**:
  ```bash
  psql "$DATABASE_URL" -c "SELECT version();"
  ```

### API Documentation
- **Swagger UI**: Available at `http://localhost:8000/docs` when backend is running
- **ReDoc**: Available at `http://localhost:8000/redoc`

## Testing

### Backend Tests
```bash
# From backend directory
pytest  # Runs all tests
pytest -v  # Verbose output
pytest --cov=app  # With coverage report
```
Expected: All tests pass, coverage >80% for critical paths

### Frontend Tests
```bash
# From frontend directory
npm run test  # Runs Jest tests
npm run test:watch  # Watch mode
```
Expected: All tests pass

### Linting
```bash
# Backend
cd ../backend
flake8  # or ruff check

# Frontend
cd ../frontend
npm run lint  # ESLint
npx prettier --check .  # Prettier formatting
```
Expected: No lint errors

### Build Verification
```bash
# Frontend production build
cd ../frontend
npm run build
# Check for build errors
```
Expected: Successful build with optimized output

## Deployment Guide

### Render.com Deployment
1. **Create Services**:
   - **PostgreSQL Database**: 
     - Create new PostgreSQL instance
     - Enable pgvector extension in database settings
     - Note the internal database URL
   - **Backend Service**:
     - Connect to GitHub repository
     - Set build command: `pip install -r requirements.txt`
     - Set start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
     - Add environment variables from `.env` (DATABASE_URL, SECRET_KEY, etc.)
     - Enable auto-deploy from GitHub pushes
   - **Frontend Service**:
     - Connect to GitHub repository (frontend folder)
     - Set build command: `npm install && npm run build`
     - Set start command: `npm start`
     - Add environment variables: `NEXT_PUBLIC_API_URL=https://your-backend.onrender.com`
     - Enable auto-deploy

2. **Environment Variables** (Backend):
   ```
   DATABASE_URL=[PostgreSQL internal URL]
   SECRET_KEY=[32+ character random string]
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   REFRESH_TOKEN_EXPIRE_DAYS=7
   BACKEND_CORS_ORIGINS=https://your-frontend.onrender.com
   ```

3. **Database Initialization**:
   - First deploy will run `alembic upgrade head` via release script (add to backend `Dockerfile` or deploy script)
   - Alternatively, run migrations manually via Render shell

### Local Development with Docker
```bash
# Backend
docker build -t workship-backend -f Dockerfile.backend .
docker run -p 8000:8000 --env-file .env workship-backend

# Frontend
docker build -t workship-frontend -f Dockerfile.frontend .
docker run -p 3000:3000 -e NEXT_PUBLIC_API_URL=http://localhost:8000 workship-frontend
```

### Production Checklist
- [ ] SECRET_KEY set to strong random value (min 32 chars)
- [ ] BACKEND_CORS_ORIGINS set to actual frontend domains
- [ ] DATABASE_URL points to production PostgreSQL
- [ ] pgvector extension enabled in database
- [ ] Alembic migrations applied (`alembic upgrade head`)
- [ ] Backend running behind reverse proxy (NGINX/TRAEFIK) with SSL
- [ ] Rate limiting monitored and adjusted based on traffic
- [ ] Logging configured to external service (e.g., Datadog, Sentry)
- [ ] Health checks configured for load balancer
- [ ] Backup strategy for PostgreSQL implemented
- [ ] CDN configured for frontend assets
- [ ] Monitoring alerts for error rates and latency

## Troubleshooting

### Backend Not Starting
- **Symptom**: `uvicorn` fails to bind port or crashes on startup
- **Likely Causes**:
  - Port already in use: `lsof -i:8000` and kill process
  - Missing SECRET_KEY: Check environment variables
  - Database connection failure: Verify DATABASE_URL and pgvector extension
  - Missing dependencies: Run `pip install -r requirements.txt`
- **Fix**:
  ```bash
  # Check port
  lsof -i :8000
  kill -9 <PID>
  
  # Verify secrets
  echo $SECRET_KEY  # Should not be empty
  
  # Test database
  psql "$DATABASE_URL" -c "SELECT 1;"
  ```

### Database Connection Issues
- **Symptom**: SQLAlchemy errors on startup or during requests
- **Likely Causes**:
  - Incorrect DATABASE_URL format
  - Network/firewall blocking database access
  - pgvector extension not installed
  - Connection pool exhausted
- **Fix**:
  ```bash
  # Test connection
  psql "$DATABASE_URL" -c "SELECT extname FROM pg_extension WHERE extname='vector';"
  
  # If missing vector extension:
  psql "$DATABASE_URL" -c "CREATE EXTENSION IF NOT EXISTS vector;"
  
  # Check connection limits
  psql "$DATABASE_URL" -c "SELECT max_connections FROM pg_settings WHERE name='max_connections';"
  ```

### JWT Errors
- **Symptom**: 401 Unauthorized on valid credentials
- **Likely Causes**:
  - SECRET_KEY mismatch between token creation and validation
  - Token expiration (check system clock synchronization)
  - malformed Authorization header (missing `Bearer ` prefix)
- **Fix**:
  ```bash
  # Verify SECRET_KEY consistency across all instances
  # Check NTP synchronization
  # Inspect Authorization header in network tab
  ```

### CORS Issues
- **Symptom**: Browser blocks requests from frontend to backend
- **Likely Causes**:
  - BACKEND_CORS_ORIGINS not set or incorrect
  - Missing `Access-Control-Allow-Origin` header
  - Preflight OPTIONS request failing
- **Fix**:
  ```bash
  # Verify middleware is applied in main.py
  # Check actual origins sent in request
  # Temporarily set BACKEND_CORS_ORIGINS=* for testing (NOT for production)
  ```

### Migration Failures
- **Symptom**: `alembic upgrade head` fails with schema errors
- **Likely Causes**:
  - Model changes not reflected in migration
  - Database state mismatch (manual changes)
  - Missing dependencies in migration environment
- **Fix**:
  ```bash
  # Check migration history
  alembic history
  
  # If needed, recreate migration:
  alembic revision --autogenerate -m "fix schema"
  
  # Ensure env.py imports all models
  # Check DATABASE_URL points to correct database
  ```

### Search Endpoint Failures
- **Symptom**: Semantic search returns no results or errors
- **Likely Causes**:
  - Embeddings not generated for documents
  - pgvector extension not enabled
  - Embedding dimension mismatch
  - Workspace filtering too restrictive
- **Fix**:
  ```bash
  # Check embeddings exist
  psql "$DATABASE_URL" -c "SELECT COUNT(*) FROM documents WHERE embedding IS NOT NULL;"
  
  # Generate missing embeddings
  cd ../backend
  python backfill_embeddings.py --workspace-id <your-workspace-uuid>
  
  # Verify pgvector
  psql "$DATABASE_URL" -c "SELECT * FROM pg_extension WHERE extname='vector';"
  ```

### Render Deployment Issues
- **Symptom**: Service fails to deploy or health checks fail
- **Likely Causes**:
  - Missing environment variables in service settings
  - Buildpack incompatibility
  - Port binding failure (not using $PORT env var)
  - Database connection timeout during startup
- **Fix**:
  ```bash
  # Check Render deploy logs for specific error
  # Verify environment variables set in service dashboard
  # Ensure start command uses $PORT for backend
  # Add health check endpoint to backend (/health)
  ```

## Contributing Guide

### Branch Strategy
- `main`: Production-ready code (deployed to production)
- `develop`: Integration branch for next release
- `feature/*`: New features (branch from develop)
- `bugfix/*`: Bug fixes (branch from develop)
- `hotfix/*`: Production urgent fixes (branch from main)
- `release/*`: Release preparation (branch from develop)

### Commit Message Format
```
<type>(<scope>): <subject>

<body>

<footer>
```
**Types**: feat, fix, docs, style, refactor, test, chore, perf, ci  
**Examples**:
- `feat(auth): add refresh token rotation`
- `fix(dashboard): add workspace filtering to queries`
- `docs(api): document incident simulation endpoint`

### Pull Request Workflow
1. Fork repository
2. Create feature branch from `develop`
3. Make changes with corresponding tests
4. Push branch and open Pull Request against `develop`
5. Request review from maintainers
6. Address review comments
7. Maintainer squash-merges into `develop`
8. Release maintainer merges `develop` into `main` and tags version

### Coding Standards
- **Python**: 
  - Black formatting (line length 88)
  - Import ordering: standard library → third-party → local application
  - Type hints for all public functions
  - Docstrings for classes and methods (Google style)
- **JavaScript/TypeScript**:
  - ESLint with Airbnb base + plugin/react
  - Prettier formatting (semi: true, singleQuote: false)
  - TypeScript strict mode enabled
  - React hooks rules exhaustive-deps
- **General**:
  - No commented-out code
  - Meaningful variable and function names
  - Error handling for all I/O operations
  - Security-first mindset (input validation, output encoding)

### Folder Conventions
- **Backend**:
  - Keep service layer thin; complex logic in dedicated utilities
  - Repositories handle ONLY data access
  - Services handle business logic and transaction boundaries
  - API layer handles ONLY request/response validation and routing
- **Frontend**:
  - Components: PascalCase, single responsibility
  - Hooks: camelCase, prefixed with "use"
  - Services: camelCase, suffix "Service"
  - Context: PascalCase, suffix "Context"
  - Styles: Tailwind utility classes-first, custom CSS in `globals.css`

## Future Roadmap

### Q3 2026
- [ ] Google OAuth & Microsoft Azure AD integration
- [ ] Two-Factor Authentication (TOTP via Authy/Google Authenticator)
- [ ] Audit log export (CSV/JSON) for compliance
- [ ] Slack & Microsoft Teams notifications for critical incidents
- [ ] Document version history with diff viewing

### Q4 2026
- [ ] Billing & subscription management (Stripe integration)
- [ ] Advanced analytics dashboard (cohort retention, funnel analysis)
- [ ] AI-powered incident root cause analysis suggestions
- [ ] Mobile application (React Native) for iOS/Android

### 2027
- [ ] Real-time collaborative document editing
- [ ] Predictive analytics for incident forecasting
- [ ] Integration with SIEM tools (Splunk, Elasticsearch)
- [ ] On-premise deployment option for air-gapped networks
- [ ] Multilingual interface (i18n) with LTR/RTL support

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Copyright (c) 2026 WorkShip AI Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.

--- 
*Documentation last updated: 2026-07-20*  
*For questions or contributions, please open an issue or pull request on GitHub.*
