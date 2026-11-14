"""Detect whether Windows camera privacy settings block desktop apps.

Windows 10/11 store the "Camera access" and "Let desktop apps access your
camera" switches under CapabilityAccessManager\\ConsentStore\\webcam. A
value of "Deny" blocks the camera for this Python process even when the
hardware works, and OpenCV then simply fails to open the device.

Only reads the registry; never changes settings.
"""

import sys

_CONSENT_KEY = r"Software\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\webcam"

HELP_TEXT = (
    "Windows is blocking camera access for desktop apps. Open Settings > "
    "Privacy & security > Camera, turn on 'Camera access' and 'Let desktop "
    "apps access your camera', then press Retry. On a school-managed laptop "
    "these switches may be controlled by your school's IT administrator."
)


def _read_value(root, subkey):
    import winreg

    try:
        with winreg.OpenKey(root, subkey) as key:
            value, _ = winreg.QueryValueEx(key, "Value")
            return str(value)
    except OSError:
        return None


def camera_privacy_status():
    """Return ``{"blocked": bool | None, "reason": str | None}``.

    ``blocked`` is ``None`` on non-Windows systems or when the settings
    cannot be read (the check is then inconclusive, not a failure).
    """
    if not sys.platform.startswith("win"):
        return {"blocked": None, "reason": None}

    import winreg

    checks = [
        (winreg.HKEY_LOCAL_MACHINE, _CONSENT_KEY, "Camera access is turned off for this device"),
        (winreg.HKEY_CURRENT_USER, _CONSENT_KEY, "Camera access is turned off for your account"),
        (
            winreg.HKEY_CURRENT_USER,
            _CONSENT_KEY + r"\NonPackaged",
            "Desktop apps are not allowed to use the camera",
        ),
    ]

    seen_any = False
    for root, subkey, reason in checks:
        value = _read_value(root, subkey)
        if value is None:
            continue
        seen_any = True
        if value.lower() == "deny":
            return {"blocked": True, "reason": reason}

    return {"blocked": False if seen_any else None, "reason": None}
