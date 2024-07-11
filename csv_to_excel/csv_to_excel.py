import base64
import io
import pandas as pd




def lambda_handler(event, context):
    base64_data = event.get('body')
    file_name = event.get('filename')

    if not base64_data or not file_name:
        return {
            'statusCode': 400,
            'body': 'body or filename is missing'
        }

    try:
        # Decode base64 string
        csv_data = base64.b64decode(base64_data)
    except Exception as e:
        return {
            'statusCode': 400,
            'body': f'Error decoding base64 data: {e}'
        }

    try:
        # Parse CSV
        csv_io = io.StringIO(csv_data.decode('utf-8'))
        df = pd.read_csv(csv_io, delimiter=',', encoding='utf-8')
    except (pd.errors.ParserError, UnicodeDecodeError) as e:
        return {
            'statusCode': 400,
            'body': f'Error parsing CSV data: {e}'
        }

    try:
        # Convert to XLSX
        xlsx_io = io.BytesIO()
        df.to_excel(xlsx_io, index=False)
        xlsx_io.seek(0)  # Reset the buffer position to the beginning
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f'Error converting CSV to XLSX: {e}'
        }

    try:
        # Return XLSX as base64
        xlsx_base64 = base64.b64encode(xlsx_io.getvalue()).decode('utf-8')
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f'Error encoding XLSX to base64: {e}'
        }

    return {
        'statusCode': 200,
        'body': xlsx_base64,
        'filename': file_name
    }
