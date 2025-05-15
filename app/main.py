import os
print("📍 Running:", os.path.realpath(__file__))
def greet(name):
    print(f"Hello hallo, {name}!")

if __name__ == "__main__":
    name = "world"
    greet(name)
