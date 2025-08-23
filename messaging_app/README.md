Messaging App API
A Django REST API for messaging functionality with JWT authentication, conversation management, and message filtering capabilities.

Quick Start with Docker Compose
The fastest way to get the application running is with Docker Compose:

Prerequisites
Docker Engine installed (Installation Guide)
Docker Compose installed (usually included with Docker Desktop)
Data Persistence
The application uses Docker volumes to ensure data persistence:

Database data: Stored in mysql_data volume (persists across container restarts)
Static files: Stored in static_volume volume
Media files: Stored in media_volume volume
These volumes are preserved even when containers are stopped. To completely remove data, use docker-compose down -v.

Prerequisites (Python)
Python 3.12+
PostgreSQL 17+
pip (Python package installer)
Installation Steps
Create a virtual environment:

Permissions
IsAuthenticated: Required for all API endpoints
IsParticipantOfConversation: Users must be participants to view/modify conversations
IsMessageOwnerOrReadOnly: Only message owners can edit/delete their messages
IsAdminUser: Required for admin interface access
API Endpoints
Token Authentication
Endpoint	Method	Description
/token/	POST	Obtain JWT token (access + refresh)
/token/refresh/	POST	Get new access token using refresh token
/token/verify/	POST	Verify a token
Users
Endpoint	Method	Description	Permissions
/users/	POST	Register new user	AllowAny
/users/me/	GET	Get current user's profile	IsAuthenticated
/users/{id}/	GET	Get user details	IsOwner or IsStaff
/users/{id}/	PATCH	Update user details	IsOwner or IsStaff
Conversations
Endpoint	Method	Description	Permissions
/conversations/	GET	List user's conversations	IsAuthenticated
/conversations/	POST	Create new conversation	IsAuthenticated
/conversations/{id}/	GET	Get conversation details	IsParticipant
/conversations/{id}/messages/	GET	List messages	IsParticipant
/conversations/{id}/messages/	POST	Send new message	IsParticipant
Messages
List Messages in a Conversation
GET /api/v1/conversations/{conversation_id}/messages/
urriculum.
