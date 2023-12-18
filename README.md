# Introduction

The Company report generator is designed to facilitate companies in generating AI-driven reports based on their input data. This project enables users to submit their company details, goals and email through a web interface. The backend processes this information using Django and SuperAGI, an open-source project, to produce insightful reports, which are then emailed to the provided email. The workflow includes backend tasks managed by Celery, ensuring efficient and asynchronous handling of data processing.

# Features

- User Input Form: Collects company details, goals, and contact information.
- Django Backend: Stores user input in a database and triggers Celery tasks.
- Celery Tasks: Asynchronously handles SuperAGI agent runs, monitors completion, and processes generated reports.
- SuperAGI Integration: Utilizes a custom integration library for seamless communication with SuperAGI.
- Amazon S3 Integration: Stores resource files (e.g., reports) on Amazon S3 for easy access.
- PDF Conversion and Emailing: Converts reports to PDF and sends them to the provided email addresses.
- Organized Codebase: Follows best practices, including code organization and adherence to the three rules of simple design.


# Get it up and running

1. Setup for Superagi
    - Clone my [fork](https://github.com/aleric-cusher/SuperAGI.git) for superagi and checkout "custom_gru" branch.
    ```bash
    git clone https://github.com/aleric-cusher/SuperAGI.git
    cd SuperAGI
    git checkout custom_gru
    ```
    - Get openai api keys and add them to the config.yaml
    - Setup AmazonS3 for SuperAGI and add its details to the config.yaml file in SuperAGI.
    - Setup google search toolkit for SuperAGI. Follow the guide [here](https://superagi.com/docs/Toolkit/SuperAGI%20Toolkits/google_search/).
- After the setup the following fields in SuperAGI's config.yaml should be set
    - OPENAI_API_KEY: your-openai-api-key
    - STORAGE_TYPE: "S3"
    - BUCKET_NAME: "your-s3-bucket-name"
    - INSTAGRAM_TOOL_BUCKET_NAME: "your-s3-bucket-name"
    - AWS_ACCESS_KEY_ID: "your-aws-access-key-id"
    - AWS_SECRET_ACCESS_KEY: "your-aws-secret-access-key"
    - GOOGLE_API_KEY: your-google-api-key
    - SEARCH_ENGINE_ID: your-search-engine-id
2. Create custom docker networks
    ```bash
    docker network create gru_network
    docker network create super_network
    ```
3. Run SuperAGI
    - Navigate to the SuperAGI clone, base directory.
    - Run command:
    ```bash
    docker compose -f ./docker-compose-gru.yaml up -d --build
    ```
    - This takes 5 to 15 minutes to startup completely
- Get SuperAGI api key
    - Navigate to http://localhost:3000 in your browser
    - Go to Settings -> Api Keys -> Create Key
    - Enter a name for your api key then click create key.
    - Copy the displayed key, this is your SuperAGI api key.
4. Setup for report generator
    - Clone the current [repo](https://github.com/aleric-cusher/gru-report-workflow.git)
    ```bash
    git clone https://github.com/aleric-cusher/gru-report-workflow.git
    ```
    - Create a ".env" by renaming or copying the ".env.example" file in the base directory of the clone.
    - Fill out email server settings in .env, for quick testing checkout [mailtrap.io](https://mailtrap.io/)
    - Add your SuperAGI api key in the .env file.
    - Add AmazonS3 settings in the .env file.
5. Run report generator
    - Navigate to the clone of the current repository, base directory.
    - Run the following commands commands:
    ```bash
    docker compose -f ./gru/docker-compose.yaml up -d --build
    docker compose -f ./frontend/docker-compose.yaml up -d --build
    ```
6. After everything is up and running you can navigate to http://localhost:1573, to interact with the demo frontend.

# Generate a report for a company

After everything is up and running successfully, navigate to http://localhost:1573.
This will show a demo page.

On the top right click `Get Quote` button. This will open up a modal, enter in your company details, and your details and click submit.
After about 20-30 minutes a report will be emailed to the email address you enter.

# View logs for docker compose.

You can view the logs for SuperAGI by:
- Navigating to the SuperAGI clone and running the command:
```bash
docker compose -f ./docker-compose-gru.yaml logs -f backend celery
```

And for the gru logs:
- Navigating to the base directory of the current repo and running:
```bash
docker compose -f ./gru/docker-compose.yaml logs -f
```
