from app import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)


class UserDevice(db.Model):
    __tablename__ = 'user_devices'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    device_id = db.Column(db.Integer, db.ForeignKey('devices.id'), nullable=False)
    user = db.relationship('User')
    device = db.relationship('Device', back_populates='user_devices')

class Device(db.Model):
    """
    Represents a device with an associated protection system.
    
    Attributes:
        id (int): The primary key of the device.
        name (str): The name of the device.
        protection_system (int): The foreign key referencing the associated protection system.
        protection_system_detail (ProtectionSystem): The relationship to the associated protection system.
    """
    __tablename__ = 'devices'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    protection_system = db.Column(db.Integer, db.ForeignKey('protection_systems.id'), nullable=False)
    protection_system_detail = db.relationship('ProtectionSystem', back_populates='devices')

class ProtectionSystem(db.Model):
    """
    Represents a protection system used by devices and content.
    
    Attributes:
        id (int): The primary key of the protection system.
        name (str): The name of the protection system.
        encryption_mode (str): The encryption mode used by the protection system.
        devices (list of Device): The list of devices using this protection system.
    """
    __tablename__ = 'protection_systems'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    encryption_mode = db.Column(db.String(50), nullable=False)
    devices = db.relationship('Device', back_populates='protection_system_detail')

class Content(db.Model):
    """
    Represents content with an encrypted payload and an associated protection system.
    
    Attributes:
        id (int): The primary key of the content.
        protection_system (int): The foreign key referencing the associated protection system.
        encryption_key (str): The encryption key used to encrypt the payload.
        encrypted_payload (str): The encrypted payload of the content.
        protection_system_detail (ProtectionSystem): The relationship to the associated protection system.
    """
    __tablename__ = 'contents'
    id = db.Column(db.Integer, primary_key=True)
    protection_system = db.Column(db.Integer, db.ForeignKey('protection_systems.id'), nullable=False)
    encryption_key = db.Column(db.String(255), nullable=False)
    encrypted_payload = db.Column(db.Text, nullable=False)
    protection_system_detail = db.relationship('ProtectionSystem')
