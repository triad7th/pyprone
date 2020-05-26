from pyprone.core import PrObj

obj = PrObj(f"obj{1:04}")
obj.log("Hello PrObj World!")

for i in range(1, 9999):
    obj = PrObj(f"obj{i:03}")
