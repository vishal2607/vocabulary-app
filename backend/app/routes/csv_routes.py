"""CSV import/export API endpoints."""
from flask import Blueprint, request, jsonify, send_file
from app.database import SessionLocal
from app.services.vocabulary_service import VocabularyService
from app.routes.middleware import require_auth
from config.config import MAX_UPLOAD_SIZE, ALLOWED_EXTENSIONS
import logging
import io

logger = logging.getLogger(__name__)

csv_bp = Blueprint('csv', __name__)


def allowed_file(filename):
    """Check if file extension is allowed.
    
    Args:
        filename: Name of the file
    
    Returns:
        bool: True if extension is allowed
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@csv_bp.route('/upload', methods=['POST'])
@require_auth
def upload_csv(user):
    """Upload and import vocabulary entries from CSV file.
    
    POST /api/csv/upload
    Headers:
        Authorization: Bearer <token>
        Content-Type: multipart/form-data
    Form data:
        file: CSV file (required)
        encoding: Character encoding (optional, auto-detected if not provided)
    
    Response (200 OK):
        {
            "result": {
                "imported_count": int,
                "skipped_count": int,
                "error_count": int,
                "errors": ["string"]
            },
            "message": "string"
        }
    
    Response (400 Bad Request):
        {
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "string",
                "details": ["string"]
            }
        }
    """
    # Check if file is present in request
    if 'file' not in request.files:
        return jsonify({
            'error': {
                'code': 'VALIDATION_ERROR',
                'message': 'No file provided',
                'details': ['File field is required in multipart/form-data']
            }
        }), 400
    
    file = request.files['file']
    
    # Check if file is selected
    if file.filename == '':
        return jsonify({
            'error': {
                'code': 'VALIDATION_ERROR',
                'message': 'No file selected',
                'details': ['Please select a file to upload']
            }
        }), 400
    
    # Check file extension
    if not allowed_file(file.filename):
        return jsonify({
            'error': {
                'code': 'VALIDATION_ERROR',
                'message': 'Invalid file type',
                'details': [f'Allowed file types: {", ".join(ALLOWED_EXTENSIONS)}']
            }
        }), 400
    
    # Get optional encoding parameter
    encoding = request.form.get('encoding', None)
    
    db = SessionLocal()
    try:
        # Read file content
        file_content = file.read()
        
        # Check file size
        if len(file_content) > MAX_UPLOAD_SIZE:
            return jsonify({
                'error': {
                    'code': 'VALIDATION_ERROR',
                    'message': 'File too large',
                    'details': [f'Maximum file size: {MAX_UPLOAD_SIZE / (1024 * 1024):.1f}MB']
                }
            }), 400
        
        # Import CSV
        vocab_service = VocabularyService(db)
        import_result = vocab_service.import_from_csv(user.id, file_content, encoding)
        
        logger.info(
            f"User {user.username} imported CSV: "
            f"{import_result.imported_count} imported, "
            f"{import_result.skipped_count} skipped, "
            f"{import_result.error_count} errors"
        )
        
        # Determine response message
        if import_result.imported_count > 0:
            message = f"Successfully imported {import_result.imported_count} entries"
            if import_result.skipped_count > 0:
                message += f" ({import_result.skipped_count} skipped as duplicates)"
        elif import_result.error_count > 0:
            message = "CSV import failed with errors"
        else:
            message = "No entries were imported"
        
        return jsonify({
            'result': import_result.to_dict(),
            'message': message
        }), 200
        
    except Exception as e:
        logger.error(f"Error during CSV upload: {str(e)}")
        return jsonify({
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': 'An error occurred during CSV import',
                'details': [str(e)]
            }
        }), 500
    finally:
        db.close()


@csv_bp.route('/export', methods=['GET'])
@require_auth
def export_csv(user):
    """Export vocabulary entries to CSV file.
    
    GET /api/csv/export?ids=<comma-separated-ids>
    Headers:
        Authorization: Bearer <token>
    Query parameters:
        ids: Comma-separated list of entry IDs to export (optional)
             If not provided, exports all entries for the user
    
    Response (200 OK):
        CSV file download with Content-Type: text/csv
        Content-Disposition: attachment; filename="vocab_export_YYYY-MM-DD.csv"
    
    Response (400 Bad Request):
        {
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "string",
                "details": ["string"]
            }
        }
    """
    db = SessionLocal()
    try:
        vocab_service = VocabularyService(db)
        
        # Parse entry IDs if provided
        entry_ids = None
        ids_param = request.args.get('ids')
        
        if ids_param:
            try:
                entry_ids = [int(id_str.strip()) for id_str in ids_param.split(',')]
            except ValueError:
                return jsonify({
                    'error': {
                        'code': 'VALIDATION_ERROR',
                        'message': 'Invalid entry IDs',
                        'details': ['Entry IDs must be comma-separated integers']
                    }
                }), 400
        
        # Export to CSV
        csv_content = vocab_service.export_to_csv(user.id, entry_ids)
        
        # Generate filename
        filtered = entry_ids is not None
        filename = vocab_service.generate_export_filename(user.id, filtered)
        
        logger.info(f"User {user.username} exported vocabulary to CSV: {filename}")
        
        # Create file-like object from string
        csv_bytes = io.BytesIO(csv_content.encode('utf-8'))
        csv_bytes.seek(0)
        
        # Send file
        return send_file(
            csv_bytes,
            mimetype='text/csv',
            as_attachment=True,
            download_name=filename
        )
        
    except ValueError as e:
        return jsonify({
            'error': {
                'code': 'VALIDATION_ERROR',
                'message': str(e),
                'details': []
            }
        }), 400
    except Exception as e:
        logger.error(f"Error during CSV export: {str(e)}")
        return jsonify({
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': 'An error occurred during CSV export',
                'details': []
            }
        }), 500
    finally:
        db.close()
