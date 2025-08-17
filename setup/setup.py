from setuptools import setup, find_packages

setup(
    name='rival-search-mcp',
    version='0.1.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    include_package_data=True,
    install_requires=[
        'httpx',
        'markdownify',
        'readabilipy',
        'protego',
        'pydantic',
        'requests',
        'torpy',
        'ipfshttpclient',
        'networkx',
        'joblib',
        'pillow',
        'pytesseract',
        'beautifulsoup4',
        'websockets',
        'cloudscraper',
    ],
    extras_require={
        'dev': ['pytest', 'ruff'],
    },
    entry_points={
        'console_scripts': [
            'rival-search-mcp = scripts.run_server:main',
        ],
    },
    author='Damion Rashford',
    description='Advanced MCP server for web retrieval, storage, and reasoning',
    long_description=open('../README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/damionr/rival-search-mcp',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.10',
)
