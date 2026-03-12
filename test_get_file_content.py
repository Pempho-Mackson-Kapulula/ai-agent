from functions.get_file_content import get_file_content
import os
from config import MAX_CHARS


def test():
    result1= get_file_content("calculator", "main.py")
    print(len(result1))
    print(result1)
    result2= get_file_content("calculator", "pkg/calculator.py")
    print(len(result2))
    print(result2)
    result3= get_file_content("calculator", "/bin/cat")
    print(len(result3))
    print(result3)
    result4 = get_file_content("calculator", "pkg/does_not_exist.py") 
    print(len(result4))
    print(result4)
    
if __name__ == "__main__":
    test()