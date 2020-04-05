## File to learn about variables in python
## Declare a variable and intialize it
newvar=0
print(newvar)

## Re-declaring the variable works
newvar="new string value"
print(newvar)

## Let see type error
print("new string"+ str(123))

##Local vs Global variables
def function():
    global newvar
    newvar="new value"
    print(newvar)

## Calling the function
function()
print(newvar)

#deletes the definition of a variable
del newvar ## delete the definition

print(newvar)