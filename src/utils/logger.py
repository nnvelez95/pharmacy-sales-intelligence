"""
Sistema de logging centralizado con formato estructurado.
"""
import logging
import sys
from pathlib import Path
from typing import Optional

from src.config import settings


def setup_logger(
    name: str,
    log_file: Optional[Path] = None,
    level: Optional[str] = None,
) -> logging.Logger:
    """
    Configura y retorna un logger con formato consistente.

    Args:
        name: Nombre del logger (usualmente __name__)
        log_file: Archivo de log opcional
        level: Nivel de log (DEBUG, INFO, WARNING, ERROR)

    Returns:
        Logger configurado

    Example:
        >>> logger = setup_logger(__name__)
        >>> logger.info("Procesando datos")
    """
    logger = logging.getLogger(name)
    log_level = getattr(logging, level or settings.log_level)
    logger.setLevel(log_level)

    # Evitar duplicación de handlers
    if logger.handlers:
        return logger

    # Formato estructurado
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Handler de consola
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Handler de archivo (opcional)
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
