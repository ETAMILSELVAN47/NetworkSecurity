from setuptools import find_packages,setup
from typing import List

HYPEN_E_DOT='-e .'

def get_requirements(file_path:str)->List[str]:
    '''
    This function will return the list of requirements
    '''
    try:
        with open(file=file_path,mode='r') as file:
            requirements=file.readlines()
            requirements=[req.strip() for req in requirements]
            requirements=[req.replace('\n','')for req in requirements]
            if HYPEN_E_DOT in requirements:
                requirements.remove(HYPEN_E_DOT)
        return requirements
    except Exception as e:
        pass



setup(
    name='Network Security',
    description=' Network Security ML Project',
    version="0.0.1",
    author="Tamilselvan",
    author_email="etamilselvan10@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements(file_path='requirements.txt')
)