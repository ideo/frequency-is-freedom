# Base image to use
FROM python:3.10-slim

# Expose port 8080
EXPOSE 8080

# Environment Variables
# ENV PROJECT_DIR /app
ENV PROJECT_DIR /app/
ENV PORT 8080
ENV HOST 0.0.0.0
ENV POETRY_VERSION=1.3.1

# Install pip
RUN python -m pip install --upgrade pip

# Install poetry
RUN pip install "poetry==${POETRY_VERSION}"

# Copy only requirements to cache them in docker layer
WORKDIR ${PROJECT_DIR}
COPY poetry.lock pyproject.toml ${PROJECT_DIR}

# Project initialization:
# RUN poetry install
# RUN poetry install --without dev
RUN poetry config virtualenvs.create false && poetry install --without dev

# Creating folders, and files for a project:
COPY . ${PROJECT_DIR}

# Run the application on port 8080
ENTRYPOINT poetry run streamlit run app.py --server.port=$PORT --server.address=$HOST