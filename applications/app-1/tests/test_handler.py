import unittest
from unittest.mock import patch, MagicMock
import json
from app_1.handler import upload_list_in_chunks, lambda_handler


class TestS3Upload(unittest.TestCase):
    @patch('app_1.handler.boto3.client')
    @patch('app_1.handler.tempfile.NamedTemporaryFile')
    @patch('app_1.handler.os.remove')
    @patch('app_1.handler.os.path.getsize')
    def test_upload_list_in_chunks(self, mock_getsize, mock_remove, MockTempFile, MockS3Client):
        # Mock S3 client
        mock_s3_client = MagicMock()
        MockS3Client.return_value = mock_s3_client

        # Mock temp file creation
        mock_temp_file = MagicMock()
        mock_temp_file.name = 'mock_temp_file.txt'
        MockTempFile.return_value = mock_temp_file

        # Mock file size
        mock_getsize.return_value = 1024 * 100  # 100 KB

        data_list = list(range(1, 300))  # Example data
        bucket_name = 'test-bucket'
        s3_key = 'test/key/'
        base_file_name = 'test_file'
        aws_access_key_id = 'fake_access_key'
        aws_secret_access_key = 'fake_secret_key'

        upload_list_in_chunks(data_list, bucket_name, s3_key, base_file_name, aws_access_key_id, aws_secret_access_key)

        # Check if S3 client upload_file method was called with correct arguments
        self.assertEqual(mock_s3_client.upload_file.call_count, 2)  # Based on chunk size and data_list length

    @patch('app_1.handler.upload_list_in_chunks')
    @patch('app_1.handler.get_date')
    def test_lambda_handler(self, mock_get_date, mock_upload_list_in_chunks):
        # Mock the return value of get_date
        mock_get_date.return_value = '2024-08-09'

        # Mock the upload function
        mock_upload_list_in_chunks.return_value = None

        event = {}
        context = {}
        response = lambda_handler(event, context)

        # Check if upload_list_in_chunks was called
        mock_upload_list_in_chunks.assert_called()

        # Check response
        self.assertEqual(response['statusCode'], 200)
        self.assertEqual(json.loads(response['body']), 'Completed')


if __name__ == '__main__':
    unittest.main()
