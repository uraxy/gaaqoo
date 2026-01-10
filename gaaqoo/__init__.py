from importlib.metadata import version, metadata

__version__ = version("gaaqoo")
__description__ = metadata("gaaqoo")["Summary"]
