# sindeuda.ai
This is a backend base example for applications aiming to use a RAG approach.
This particular repo called "Sindeuda" was thought as a personal finance management appliaction to not 
only register transactions using natural language, but to ask for customized recomendations considering 
your current financial status, and transaction information.

## Usage
Calling the corresponding endpoints, you will be able to create a user with email and password. After that, you can create 
all bank accounts you want (card's information), categories to group all your transactions, (E.g., Restaurants, Utilities, Home, etc.).
Finally, using natural language, you will be able to register transactions that will be added automatically 
to your categories and corresponding cards/accounts previously created.

## Architecture
- The framework used to develop the API is FastAPI, the API models were generated using Pydantic. 
- The ORM chosen for database operations was SQLAlchemy where alembic is applied for migrations.
- DBMS selected to create the database was Postgres via docker image.

## Caveats
- This is not ready for production yet.
- Containers currently lie under the same docker network (spoecified on docker-compose.yml) to test API using Postman.
- This is under development, there are still missing endpoints to integrate with a functional frontend.