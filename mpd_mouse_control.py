from evdev import InputDevice
from select import select
import os
import mpd
import socket
import alsaaudio
import time
client = mpd.MPDClient(use_unicode=True)
dev = InputDevice('/dev/input/event2')
drop_lb_event = False
drop_rb_event = False

while True:
        r,w,x = select([dev], [], [])
        try:
                for event in dev.read():
                        client.connect("192.168.0.2", 6600)
                        if event.code == 8:
                                if 272 in dev.active_keys():
                                        drop_lb_event = True
                                        if (event.value > 0):
                                                client.seekcur("+5")
                                        else:
                                                client.seekcur("-5")
                                elif 273 in dev.active_keys():
                                        drop_rb_event = True
                                        if (event.value > 0):
                                                client.seekcur("+30")
                                        else:
                                                client.seekcur("-30")
                                else:
                                        mixer = alsaaudio.Mixer("PCM", **{"cardindex": 1})
                                        if (event.value > 0):
                                                mixer.setvolume(int(mixer.getvolume()[0])+2, -1)
                                        else:
                                                mixer.setvolume(int(mixer.getvolume()[0])-2, -1)
                        try:
                                if event.code == 272 and event.value == 0:
                                        if drop_lb_event:
                                                drop_lb_event = False
                                        else:
                                                client.previous()
                                if event.code == 273 and event.value == 0:
                                        if drop_rb_event:
                                                drop_rb_event = False
                                        else:
                                                client.next()
                                if event.code == 274 and event.value == 1:
                                        if client.status()["state"] == "stop":
                                                client.play()
                                        else:
                                                client.pause()
                                        os.system("/usr/sbin/qcontrol usbled off")
                                client.disconnect()
                        except mpd.ConnectionError, socket.error:
                                pass
        except IOError, OSError:
                time.sleep(5)
                dev = InputDevice('/dev/input/event2')
