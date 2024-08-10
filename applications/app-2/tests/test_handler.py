import unittest
from unittest.mock import patch, MagicMock
import json
from app_2.handler import delete_existing_s3_directory, lambda_handler


class TestS3Operations(unittest.TestCase):
    @patch('app_2.handler.boto3.client')
    def test_delete_existing_s3_directory(self, MockBoto3Client):
        # Mock S3 client
        mock_s3_client = MagicMock()
        MockBoto3Client.return_value = mock_s3_client

        # Mock response for list_objects_v2
        mock_s3_client.list_objects_v2.return_value = {
            'Contents': [
                {'Key': 'data/classification/period=2024-08-09/file1.txt'},
                {'Key': 'data/classification/period=2024-08-09/file2.txt'}
            ],
            'KeyCount': 2
        }

        bucket_name = 'test-bucket'
        s3_key = 'data/classification/period=2024-08-09/'

        delete_existing_s3_directory(mock_s3_client, bucket_name, s3_key)

        # Verify list_objects_v2 was called
        mock_s3_client.list_objects_v2.assert_called_once_with(Bucket=bucket_name, Prefix=s3_key)

        # Verify delete_objects was called with correct parameters
        expected_delete_params = {
            'Objects': [
                {'Key': 'data/classification/period=2024-08-09/file1.txt'},
                {'Key': 'data/classification/period=2024-08-09/file2.txt'}
            ]
        }
        mock_s3_client.delete_objects.assert_called_once_with(Bucket=bucket_name, Delete=expected_delete_params)

    @patch('app_2.handler.boto3.client')
    @patch('app_2.handler.get_date')
    def test_lambda_handler(self, mock_get_date, MockBoto3Client):
        # Mock get_date
        mock_get_date.return_value = '2024-08-09'

        # Mock S3 client
        mock_s3_client = MagicMock()
        MockBoto3Client.return_value = mock_s3_client

        event = {}
        context = {}
        response = lambda_handler(event, context)

        # Verify delete_existing_s3_directory was called
        s3_key = 'data/classification/period=2024-08-09/'
        mock_s3_client.list_objects_v2.assert_called_once_with(Bucket='dhananjayasamantasinghar', Prefix=s3_key)

        # Check response
        self.assertEqual(response['statusCode'], 200)
        self.assertEqual(json.loads(response['body']), 'Completed')


if __name__ == '__main__':
    unittest.main()
