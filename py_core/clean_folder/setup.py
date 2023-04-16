from setuptools import setup, find_namespace_packages


setup(
    name='clean_folder',
    version='0.0.1',
    description='Very useful code',
    url='https://github.com/icoderp/goit-python/blob/main/lesson6/new_sort.py',
    author='Ihor Voitiuk',
    author_email='flyingcircus@example.com',
    license='MIT',
    packages=find_namespace_packages(),
    entry_points={'console_scripts': [
        'clean-folder = clean_folder.clean:main_path']}
)
