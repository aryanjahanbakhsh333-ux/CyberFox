from datetime import datetime

from database import db
from device_fleet_model import ManagedDevice


def register_device(
    user_id,
    device_id,
    name,
    platform=None
):
    existing = ManagedDevice.query.filter_by(
        user_id=user_id,
        device_id=device_id
    ).first()

    if existing:
        existing.name = name
        existing.platform = platform
        existing.last_seen = datetime.utcnow()

        db.session.commit()

        return existing

    device = ManagedDevice(
        user_id=user_id,
        device_id=device_id,
        name=name,
        platform=platform,
        status="online",
        last_seen=datetime.utcnow()
    )

    db.session.add(device)
    db.session.commit()

    return device


def get_user_devices(user_id):
    return (
        ManagedDevice.query
        .filter_by(user_id=user_id)
        .order_by(
            ManagedDevice.created_at.desc()
        )
        .all()
    )


def serialize_device(device):
    return {
        "id": device.id,
        "device_id": device.device_id,
        "name": device.name,
        "platform": device.platform,
        "status": device.status,
        "last_seen": (
            device.last_seen.isoformat()
            if device.last_seen
            else None
        )
    }
