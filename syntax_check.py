def greet(userFav,name="orange", latsname="user",age=28):
    print(f"Hello {name} {latsname}, you are {age} years old! something you love most is {userFav}")

greet(latsname="nisha",userFav="Free Running")
greet("Free Running ","blue","nisha")

from fastapi import HTTPException
def check_res_of_error(num=10):
    if(num==10):
        return 10
    raise HTTPException(status_code=400,detail="only 10 allowed")

error_res=check_res_of_error(11)
