import unittest
from app import app, db
from app.models import Content, Device, ProtectionSystem
from flask import json

class TestRoutes(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        app.config.from_object('config.TestConfig')
        cls.client = app.test_client()
        cls.app = app
        cls.app_context = app.app_context()
        cls.app_context.push()
        db.create_all()
        
        cls.protection_system = ProtectionSystem(name='AES', encryption_mode='AES + ECB')
        db.session.add(cls.protection_system)
        db.session.commit()
        
        cls.device = Device(name='Device1', protection_system=cls.protection_system.id)
        db.session.add(cls.device)
        db.session.commit()
        
        cls.content_response = cls.client.post('/contents', headers={'Content-Type': 'application/json'}, data=json.dumps({
            "protection_system": cls.protection_system.id,
            "encryption_key": "p2iW1rL0WwjbkBFv6Er67Q==",
            "plaintext_payload": "This is a sample payload."
        }))
        cls.content_id = json.loads(cls.content_response.data)['id']

    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()

    def test_get_contents_with_data(self):
        response = self.client.get('/contents')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(len(data) > 0)

    def test_post_content(self):
        response = self.client.post('/contents',
                                    headers={'Content-Type': 'application/json'},
                                    data=json.dumps({
                                        "protection_system": self.protection_system.id,
                                        "encryption_key": "p2iW1rL0WwjbkBFv6Er67Q==",
                                        "plaintext_payload": "This is a sample payload."
                                    }))
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('id', data)
        self.assertEqual(data['protection_system'], self.protection_system.id)
        self.assertIn('encrypted_payload', data)

    def test_delete_content(self):
        post_response = self.client.post('/contents', headers={'Content-Type': 'application/json'}, data=json.dumps({
            "protection_system": self.protection_system.id,
            "encryption_key": "p2iW1rL0WwjbkBFv6Er67Q==",
            "plaintext_payload": "New sample payload."
        }))
        content_id = json.loads(post_response.data)['id']

        delete_response = self.client.delete(f'/contents/{content_id}')
        self.assertEqual(delete_response.status_code, 200)
        self.assertTrue(json.loads(delete_response.data)['result'])

        get_response = self.client.get(f'/contents/{content_id}')
        self.assertEqual(get_response.status_code, 404)

    def test_get_content_by_id(self):
        response = self.client.get(f'/contents/{self.content_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['id'], self.content_id)
        self.assertIn('encrypted_payload', data)

    def test_put_content(self):
        post_response = self.client.post('/contents', headers={'Content-Type': 'application/json'}, data=json.dumps({
            "protection_system": self.protection_system.id,
            "encryption_key": "p2iW1rL0WwjbkBFv6Er67Q==",
            "plaintext_payload": "Content to be updated."
        }))
        content_id = json.loads(post_response.data)['id']

        put_response = self.client.put(f'/contents/{content_id}', headers={'Content-Type': 'application/json'}, data=json.dumps({
            "protection_system": self.protection_system.id,
            "encryption_key": "p2iW1rL0WwjbkBFv6Er67Q==",
            "plaintext_payload": "Updated payload."
        }))
        self.assertEqual(put_response.status_code, 200)
        data = json.loads(put_response.data)
        self.assertEqual(data['id'], content_id)

        get_response = self.client.get(f'/contents/{content_id}')
        self.assertEqual(get_response.status_code, 200)
        parsed_get_response = json.loads(get_response.data)
        self.assertEqual(parsed_get_response['encrypted_payload'], 'PilZyCyLIZ1QHvqn7RJUpVCIWeujKIktCzn+1/t0+XA=')  # Adjust based on encryption

    def test_failed_decryption(self):
        self.content = Content(id=100, protection_system='1', encryption_key='invalid-key',encrypted_payload='invalid')
        db.session.add(self.content)
        db.session.commit()

        response = self.client.get(f'/contents/100')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Incorrect padding')
        self.client.delete(f'/contents/100')

if __name__ == '__main__':
    unittest.main()
