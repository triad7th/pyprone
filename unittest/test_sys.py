from pyprone.objects import PrSys

syscon = PrSys("Hello PrSyscon")
print(syscon.text)
syscon.text += "\nyay"
print(syscon.text)
