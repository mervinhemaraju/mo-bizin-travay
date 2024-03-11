# Build from AWS Lambda ECR image with Python 3.11
FROM public.ecr.aws/lambda/python:3.11

# Copy the requirements file
COPY requirements.txt ${LAMBDA_TASK_ROOT}

# Install the requirements
RUN pip install -r requirements.txt

# Copy the files to the lambda tasks root
COPY . ${LAMBDA_TASK_ROOT}

# Run the handler
CMD ["main.main"]