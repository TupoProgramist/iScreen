class Class1:
    def __init__(self):
        self.attribute1 = None

    def function1(self):
        print(f"Before function2: attribute1 = {self.attribute1}")
        self.function2()
        print(f"After function2: attribute1 = {self.attribute1}")
        # Further operations may overwrite or reset attribute1

    def function2(self):
        self.attribute1 = "Updated in function2"
        print(f"In function2: attribute1 = {self.attribute1}")

# Create an instance and call function1
obj = Class1()
obj.function1()
