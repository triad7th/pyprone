from pyprone.objects import PrSys
from pyprone.commands import PrSysCmd

#app = QApplication([])

objects = {'syscon': PrSys("Test Syscon")}
syscon_cmd = PrSysCmd(objects)

syscon_cmd.command("cmd1")
print(objects['syscon'].text)
syscon_cmd.command("cmd2")
print(objects['syscon'].text)
syscon_cmd.command("cmd3")
print(objects['syscon'].text)
syscon_cmd.command("cmd4")
print(objects['syscon'].text)
syscon_cmd.command("cls")
print(objects['syscon'].text)
syscon_cmd.command("cmd5")
print(objects['syscon'].text)

#app.exec_()
