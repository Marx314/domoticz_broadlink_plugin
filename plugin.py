# Broadlink debugging
#
# Author: marx314
#
"""
<plugin key="Broadlink" name="Broadlink" author="marx314" version="1.0.0" wikilink="https://www.domoticz.com/wiki/Developing_a_Python_plugin" externallink="https://www.domoticz.com/wiki/Developing_a_Python_plugin">
    <description>
        <h2>Broadlink plugin</h2><br/>
    </description>
    <params>
        <param field="address" label="IP Address" width="200px" required="true" default="10.0.0.140"/>
        <param field="debug" label="debug" width="75px">
            <options>
                <option label="True" value="1"/>
                <option label="False" value="0"  default="0" />
            </options>
        </param>
    </params>
</plugin>
"""
import broadlink

if 'Parameters' not in globals():
    Parameters = {'Address': "10.0.0.140"}
if 'Devices' not in globals():
    Devices = {}

if '/opt/domoticz/' in __file__:
    import DomoticzEx
else:
    from fake_env import DomoticzEx


class BasePlugin:
    enabled = False
    ip = ""

    def __init__(self):
        DomoticzEx.Log(globals())
        return

    def hello(self):
        device = None
        while not device:
            try:
                device = broadlink.hello(self.ip)
                assert device.auth()
                device.ping()
            except Exception as e:
                device = None
                DomoticzEx.Log(e)
        return device

    def onStart(self):
        DomoticzEx.Log("onStart called")
        self.ip = Parameters['address']
        DomoticzEx.Log(Parameters['address'])
        if Parameters["debug"] != "0":
            DomoticzEx.Debugging(int(Parameters["debug"]))
            DumpConfigToLog()

        # if (not "Dimmer" in Devices):
        #    Domoticz.Unit(Name="Dimmer", Unit=2, TypeName="Dimmer", DeviceID="Dimmer").Create()

    def onStop(self):
        DomoticzEx.Log("onStop called")

    def onConnect(self, Connection, Status, Description):
        DomoticzEx.Log("onConnect called")
        self.hello()

    def onMessage(self, Connection, Data):
        DomoticzEx.Log("onMessage called")

    def onCommand(self, DeviceID, Unit, Command, Level, Color):
        DomoticzEx.Log("onCommand called for Device " + str(DeviceID) + " Unit " + str(Unit) + ": Parameter '" + str(
            Command) + "', Level: " + str(Level))

    def onNotification(self, Name, Subject, Text, Status, Priority, Sound, ImageFile):
        DomoticzEx.Log("Notification: " + Name + "," + Subject + "," + Text + "," + Status + "," + str(
            Priority) + "," + Sound + "," + ImageFile)

    def onDisconnect(self, Connection):
        DomoticzEx.Log("onDisconnect called")

    def onHeartbeat(self):
        DomoticzEx.Log("onHeartbeat called")


global _plugin
_plugin = BasePlugin()


def onStart():
    global _plugin
    _plugin.onStart()


def onStop():
    global _plugin
    _plugin.onStop()


def onConnect(Connection, Status, Description):
    global _plugin
    _plugin.onConnect(Connection, Status, Description)


def onMessage(Connection, Data):
    global _plugin
    _plugin.onMessage(Connection, Data)


def onCommand(DeviceID, Unit, Command, Level, Color):
    global _plugin
    _plugin.onCommand(DeviceID, Unit, Command, Level, Color)


def onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile):
    global _plugin
    _plugin.onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile)


def onDisconnect(Connection):
    global _plugin
    _plugin.onDisconnect(Connection)


def onHeartbeat():
    global _plugin
    _plugin.onHeartbeat()


# Generic helper functions
def DumpConfigToLog():
    for x in Parameters:
        if Parameters[x] != "":
            DomoticzEx.Debug("'" + x + "':'" + str(Parameters[x]) + "'")
    DomoticzEx.Debug("Device count: " + str(len(Devices)))
    for DeviceName in Devices:
        Device = Devices[DeviceName]
        DomoticzEx.Debug("Device ID:       '" + str(Device.DeviceID) + "'")
        DomoticzEx.Debug("--->Unit Count:      '" + str(len(Device.Units)) + "'")
        for UnitNo in Device.Units:
            Unit = Device.Units[UnitNo]
            DomoticzEx.Debug("--->Unit:           " + str(UnitNo))
            DomoticzEx.Debug("--->Unit Name:     '" + Unit.Name + "'")
            DomoticzEx.Debug("--->Unit nValue:    " + str(Unit.nValue))
            DomoticzEx.Debug("--->Unit sValue:   '" + Unit.sValue + "'")
            DomoticzEx.Debug("--->Unit LastLevel: " + str(Unit.LastLevel))
    return
