services:
  streamlit:
    image: python:3.11-slim
    container_name: streamlit_app

    working_dir: /app

    ports:
      - "8501:8501"

    volumes:
      - ./app:/app
      - streamlit_uploads:/app/uploads

    command: >
      bash -c "
      pip install -r requirements.txt &&
      streamlit run app.py --server.address=0.0.0.0
      "

volumes:
  streamlit_uploads: