import base64
import io
import pandas as pd


def lambda_handler(event, context):
    base64_data = event.get('body')
    file_name = event.get('filename')
    # Decode base64 string
    csv_data = base64.b64decode(base64_data)

    # Parse CSV
    csv_io = io.StringIO(csv_data.decode('utf-8'))
    df = pd.read_csv(csv_io, delimiter=',', encoding='utf-8')

    # Convert to XLSX
    xlsx_io = io.BytesIO()
    df.to_excel(xlsx_io, index=False)

    # Return XLSX as base64
    xlsx_base64 = base64.b64encode(xlsx_io.getvalue()).decode('utf-8')
    return {
        'statusCode': 200,
        'body': xlsx_base64,
        'filename': file_name  # Include the file name in the response
    }
