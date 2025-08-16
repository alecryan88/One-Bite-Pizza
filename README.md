# One Bite Pizza

One Bite Pizza is a Python application that fetches reviews from an API, processes them, and uploads the data to an AWS S3 bucket.

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd one_bite_pizza
   ```

2. **Install dependencies**:
   Make sure you have Python 3.x installed. Then, install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. **AWS Configuration**:
   Ensure you have AWS credentials configured. You can set them up using the AWS CLI:
   ```bash
   aws configure
   ```

## Usage

To run the application, use the following command:
```bash
python main.py --start_date YYYY-MM-DD [--end_date YYYY-MM-DD]
```
- `--start_date`: The start date for fetching reviews (required).
- `--end_date`: The end date for fetching reviews (optional, defaults to start date if not provided).

## Configuration

The application uses a `config.yml` file for configuration. Ensure this file is present in the root directory with the following structure:
```yaml
api:
  url: <API_URL>
  limit: <LIMIT>

aws:
  bucket_name: <BUCKET_NAME>
```

## Dependencies

- Python 3.x
- `requests`
- `boto3`
- `PyYAML`
- `argparse`

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -am 'Add new feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Create a new Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
