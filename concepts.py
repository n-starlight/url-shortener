# Iterators

# Iterator for looping over a sequence backwards
class Reverse:
    def __init__(self,data):
        self.data=data
        self.index=len(data)

    def __iter__(self):
        return self
    
    def __next__(self):
        if self.index==0:
            raise StopIteration
        self.index=self.index -1
        return self.data[self.index]
    

rev=Reverse('spam')
print(rev.__iter__())
for c in rev:
    print(c)



print("using generator : ------------")

# When a generator function is called, it returns an iterator- generator object instead of executing the body of the function immediately.
#Contains one or more yirld instead of return 
#Execution starts when one of generator's methods is called.
#At yield the execution suspends until next method called on generator
#At suspend all local state is retained, including the current bindings of local variables
def reverse(data):
    for index in range(len(data)-1,-1,-1):
        yield data[index]

for char in reverse('spam'):
    print(char)


def my_generator():
    print("First")
    yield 1
    print("Second")
    yield 2

gen = my_generator()  # Creates generator object, no execution yet
print(next(gen))      # Starts execution, prints "First", returns 1 to caller
print(next(gen))      # Resumes, prints "Second", returns 2

# When yield is encountered the function pauses and the value is sent to the caller.
# Execution can be resumed from that point using next() or in async case using await()


