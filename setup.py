from setuptools import find_packages,setup
from typing import List
def get_requirements()->List[str]:
    """
    This function returns a list of requirements
    """
    requirements_lst:List[str]=[]
    try:
        with open("requirement.txt","r") as file:
            #Read lines from the file
            lines=file.readlines()
             # Remove newline characters and exclude '-e .' if present
            requirements=[line.strip() for line in lines if line.strip() and not line.startswith("-e")]
            return requirements
    except FileNotFoundError:
        print("requirements.txt file not found.")
    return requirements_lst
setup(
    name="Mlops_project",
    version="0.1.0",
    author="MMM",
    author_email="mannamodanmohan@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements(),
)