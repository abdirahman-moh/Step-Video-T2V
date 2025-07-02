from setuptools import find_packages, setup
import subprocess
import re
import os


def get_cuda_version():
    try:
        nvcc_version = subprocess.check_output(["nvcc", "--version"], stderr=subprocess.DEVNULL).decode("utf-8")
        version_line = [line for line in nvcc_version.split("\n") if "release" in line]
        if not version_line:
            return "no_cuda"
        cuda_version = version_line[0].split(" ")[-2].replace(",", "")
        return "cu" + cuda_version.replace(".", "")
    except (subprocess.CalledProcessError, FileNotFoundError, IndexError) as e:
        print(f"Warning: Could not detect CUDA version: {e}")
        return "no_cuda"


def get_version_from_file(filepath):
    """Safely parse version from __version__.py file"""
    try:
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Version file not found: {filepath}")
        
        with open(filepath, "r") as f:
            content = f.read().strip()
        
        # Use regex to safely extract version string instead of eval()
        version_match = re.search(r'__version__\s*=\s*["\']([^"\']+)["\']', content)
        if version_match:
            return version_match.group(1)
        
        # Fallback: try to extract quoted string from the end of the file
        version_match = re.search(r'["\']([0-9]+\.[0-9]+\.[0-9]+(?:\.[a-zA-Z0-9]+)*)["\']', content)
        if version_match:
            return version_match.group(1)
        
        raise ValueError("Could not parse version from file content")
        
    except Exception as e:
        print(f"Error reading version file {filepath}: {e}")
        return "0.1.0"  # Default fallback version


if __name__ == "__main__":
    try:
        with open("README.md", "r", encoding="utf-8") as f:
            long_description = f.read()
    except (FileNotFoundError, UnicodeDecodeError) as e:
        print(f"Warning: Could not read README.md: {e}")
        long_description = "StepVideo - A 30B DiT based text to video and image generation model"
    
    # Fix: Use safe version parsing instead of eval()
    version = get_version_from_file("stepvideo/__version__.py")

    setup(
        name="stepvideo",
        author="Step-Video Team",
        packages=find_packages(),
        install_requires=[
            "torchvision==0.20",
            "torch==2.5.0",
            "accelerate>=1.0.0",
            "transformers>=4.39.1",
            "diffusers>=0.31.0",
            "sentencepiece>=0.1.99",
            "imageio>=2.37.0",
            "optimus==2.1",
            "numpy",
            "einops",
            "aiohttp",
            "asyncio",
            "flask",
            "flask_restful",
            "ffmpeg-python",
            "requests",
            "xfuser==0.4.2rc2"
        ],
        url="",
        description="A 30B DiT based text to video and image generation model",
        long_description=long_description,
        long_description_content_type="text/markdown",
        version=version,
        classifiers=[
            "Programming Language :: Python :: 3",
            "Operating System :: OS Independent",
        ],
        include_package_data=True,
        python_requires=">=3.10",
    )