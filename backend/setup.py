from setuptools import setup, find_packages

setup(
    name="architector-llm-backend",
    version="1.0.0",
    description="Backend service for Architector-LLM",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.9",
    install_requires=[
        "flask>=3.0.0",
        "flask-cors>=4.0.0",
        "python-dotenv>=1.0.0",
        "requests>=2.31.0",
        "tree-sitter>=0.21.0",
    ],
)
