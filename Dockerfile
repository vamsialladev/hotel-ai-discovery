FROM python:3.12-slim
WORKDIR /app
COPY scripts/ scripts/
COPY docs/ docs/
COPY README.md .
# Prints the pricing scenarios; pass other flags after the image name, e.g. --properties 100 --scenarios
ENTRYPOINT ["python", "scripts/pricing.py"]
CMD ["--scenarios"]
