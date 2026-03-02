"""Custom exceptions for FreeLauncher"""


class FreeLauncherException(Exception):
    """Base exception for FreeLauncher"""
    pass


class ProfileException(FreeLauncherException):
    """Exception related to profile management"""
    pass


class ProfileNotFoundError(ProfileException):
    """Profile not found"""
    pass


class ProfileAlreadyExistsError(ProfileException):
    """Profile already exists"""
    pass


class InvalidProfileError(ProfileException):
    """Invalid profile data"""
    pass


class MinecraftException(FreeLauncherException):
    """Exception related to Minecraft operations"""
    pass


class MinecraftVersionNotFoundError(MinecraftException):
    """Minecraft version not found"""
    pass


class MinecraftLaunchError(MinecraftException):
    """Error launching Minecraft"""
    pass


class ModException(FreeLauncherException):
    """Exception related to mod management"""
    pass


class ConfigException(FreeLauncherException):
    """Exception related to configuration"""
    pass
