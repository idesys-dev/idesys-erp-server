from os import path


from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


def upload(creds, output_path, metadata_mime_type, media_mimetype):
    drive_service = build('drive', 'v3', credentials=creds)
    file_metadata = {
        'name': path.basename(output_path),
        'mimeType':metadata_mime_type
    }
    media = MediaFileUpload(output_path,
                            mimetype=media_mimetype,
                            resumable=True)
    file = drive_service.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='webViewLink').execute()
    return file.get('webViewLink')
