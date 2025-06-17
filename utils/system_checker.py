"""System requirements checking utilities."""

import os
import sys
import shutil
import logging
import subprocess
from typing import Dict, Any, Optional
from pathlib import Path

logger = logging.getLogger(__name__)

class SystemChecker:
    """Checks system requirements and dependencies."""
    
    # Required commands and their minimum versions
    REQUIRED_COMMANDS = {
        "python": {
            "min_version": (3, 8),
            "command": "python --version",
            "description": "Python interpreter"
        },
        "manim": {
            "min_version": (0, 17, 0),
            "command": "manim --version",
            "description": "Manim library"
        },
        "ffmpeg": {
            "min_version": (4, 0, 0),
            "command": "ffmpeg -version",
            "description": "FFmpeg for video processing"
        }
    }
    
    # Required Python packages and their minimum versions
    REQUIRED_PACKAGES = {
        "manim": "0.17.0",
        "streamlit": "1.0.0",
        "groq": "0.3.0",
        "numpy": "1.20.0",
        "pillow": "8.0.0"
    }
    
    # Minimum system requirements
    MIN_REQUIREMENTS = {
        "cpu_cores": 2,
        "ram_gb": 4,
        "disk_space_gb": 1,
        "gpu_memory_gb": 2  # Optional
    }
    
    def __init__(self):
        """Initialize the system checker."""
        self.system_info = {}
        self.missing_requirements = []
        self.warnings = []
    
    @classmethod
    def get_system_info(cls) -> Dict[str, Any]:
        """Get system information and requirements status.
        
        Returns:
            Dictionary containing system information and requirements status
        """
        checker = cls()
        checker._check_python_version()
        checker._check_commands()
        checker._check_packages()
        checker._check_system_resources()
        
        return {
            "python_version": checker.system_info.get("python_version", "Unknown"),
            "manim_installed": checker.system_info.get("manim_installed", False),
            "ffmpeg_installed": checker.system_info.get("ffmpeg_installed", False),
            "required_packages": checker.system_info.get("required_packages", {}),
            "system_resources": checker.system_info.get("system_resources", {}),
            "missing_requirements": checker.missing_requirements,
            "warnings": checker.warnings
        }
    
    def _check_python_version(self) -> None:
        """Check Python version."""
        version = sys.version_info
        self.system_info["python_version"] = f"{version.major}.{version.minor}.{version.micro}"
        
        min_version = self.REQUIRED_COMMANDS["python"]["min_version"]
        if version < min_version:
            self.missing_requirements.append(
                f"Python {min_version[0]}.{min_version[1]} or higher required"
            )
    
    def _check_commands(self) -> None:
        """Check required command-line tools."""
        for cmd, info in self.REQUIRED_COMMANDS.items():
            if cmd == "python":
                continue  # Already checked
                
            try:
                result = subprocess.run(
                    info["command"].split(),
                    capture_output=True,
                    text=True
                )
                
                if result.returncode == 0:
                    version = self._parse_version(result.stdout)
                    min_version = info["min_version"]
                    
                    if version >= min_version:
                        self.system_info[f"{cmd}_installed"] = True
                        self.system_info[f"{cmd}_version"] = ".".join(map(str, version))
                    else:
                        self.missing_requirements.append(
                            f"{info['description']} version {'.'.join(map(str, min_version))} "
                            f"or higher required"
                        )
                else:
                    self.missing_requirements.append(
                        f"{info['description']} not found"
                    )
                    
            except Exception as e:
                logger.error(f"Error checking {cmd}: {e}")
                self.missing_requirements.append(
                    f"Error checking {info['description']}"
                )
    
    def _check_packages(self) -> None:
        """Check required Python packages."""
        import pkg_resources
        
        self.system_info["required_packages"] = {}
        
        for package, min_version in self.REQUIRED_PACKAGES.items():
            try:
                installed = pkg_resources.get_distribution(package)
                self.system_info["required_packages"][package] = {
                    "installed": True,
                    "version": installed.version
                }
                
                if installed.version < min_version:
                    self.missing_requirements.append(
                        f"{package} version {min_version} or higher required"
                    )
                    
            except pkg_resources.DistributionNotFound:
                self.system_info["required_packages"][package] = {
                    "installed": False,
                    "version": None
                }
                self.missing_requirements.append(f"{package} not installed")
    
    def _check_system_resources(self) -> None:
        """Check system resources."""
        import psutil
        
        self.system_info["system_resources"] = {}
        
        # CPU cores
        cpu_count = psutil.cpu_count(logical=False)
        self.system_info["system_resources"]["cpu_cores"] = cpu_count
        if cpu_count < self.MIN_REQUIREMENTS["cpu_cores"]:
            self.warnings.append(
                f"Low CPU cores: {cpu_count} (recommended: {self.MIN_REQUIREMENTS['cpu_cores']}+)"
            )
        
        # RAM
        ram_gb = psutil.virtual_memory().total / (1024 ** 3)
        self.system_info["system_resources"]["ram_gb"] = round(ram_gb, 1)
        if ram_gb < self.MIN_REQUIREMENTS["ram_gb"]:
            self.warnings.append(
                f"Low RAM: {round(ram_gb, 1)}GB (recommended: {self.MIN_REQUIREMENTS['ram_gb']}+GB)"
            )
        
        # Disk space
        disk_gb = psutil.disk_usage("/").free / (1024 ** 3)
        self.system_info["system_resources"]["disk_space_gb"] = round(disk_gb, 1)
        if disk_gb < self.MIN_REQUIREMENTS["disk_space_gb"]:
            self.warnings.append(
                f"Low disk space: {round(disk_gb, 1)}GB "
                f"(recommended: {self.MIN_REQUIREMENTS['disk_space_gb']}+GB)"
            )
        
        # GPU (optional)
        try:
            import torch
            if torch.cuda.is_available():
                gpu_memory = torch.cuda.get_device_properties(0).total_memory / (1024 ** 3)
                self.system_info["system_resources"]["gpu_memory_gb"] = round(gpu_memory, 1)
                if gpu_memory < self.MIN_REQUIREMENTS["gpu_memory_gb"]:
                    self.warnings.append(
                        f"Low GPU memory: {round(gpu_memory, 1)}GB "
                        f"(recommended: {self.MIN_REQUIREMENTS['gpu_memory_gb']}+GB)"
                    )
        except ImportError:
            self.system_info["system_resources"]["gpu_memory_gb"] = None
    
    @staticmethod
    def _parse_version(version_str: str) -> tuple:
        """Parse version string into tuple of integers."""
        import re
        version_match = re.search(r'(\d+\.\d+(?:\.\d+)?)', version_str)
        if version_match:
            return tuple(map(int, version_match.group(1).split('.')))
        return (0, 0, 0)
    
    @classmethod
    def check_requirements(cls) -> bool:
        """Check if all system requirements are met.
        
        Returns:
            True if all requirements are met, False otherwise
        """
        system_info = cls.get_system_info()
        return len(system_info["missing_requirements"]) == 0
    
    @classmethod
    def get_installation_guide(cls) -> str:
        """Get installation guide for missing requirements.
        
        Returns:
            Installation guide as a formatted string
        """
        system_info = cls.get_system_info()
        
        if not system_info["missing_requirements"]:
            return "All requirements are satisfied."
        
        guide = ["Installation Guide:"]
        
        # Python version
        if "Python" in str(system_info["missing_requirements"]):
            guide.extend([
                "\n1. Install Python:",
                "   - Download from https://www.python.org/downloads/",
                "   - Make sure to check 'Add Python to PATH' during installation"
            ])
        
        # Manim
        if not system_info["manim_installed"]:
            guide.extend([
                "\n2. Install Manim:",
                "   pip install manim",
                "   - For detailed installation, visit: https://docs.manim.community/",
                "   - Make sure to install system dependencies first"
            ])
        
        # FFmpeg
        if not system_info["ffmpeg_installed"]:
            guide.extend([
                "\n3. Install FFmpeg:",
                "   - Windows: Download from https://ffmpeg.org/download.html",
                "   - Linux: sudo apt-get install ffmpeg",
                "   - macOS: brew install ffmpeg"
            ])
        
        # Python packages
        missing_packages = [
            pkg for pkg, info in system_info["required_packages"].items()
            if not info["installed"]
        ]
        if missing_packages:
            guide.extend([
                "\n4. Install required Python packages:",
                f"   pip install {' '.join(missing_packages)}"
            ])
        
        return "\n".join(guide)