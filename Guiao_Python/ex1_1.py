def list_lenght(list):
    if list:
        return 1 + list_lenght(list[1:])
    else:
        return 0


l = [1,2,3,4,5,6,7,8]
print(list_lenght(l))
