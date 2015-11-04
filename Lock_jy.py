## Joshua You



#!/usr/bin/env python
import sys
import os.path
import gtk
import appindicator
import subprocess


I_ARMED_PATH = '/home/jshuay/Testing_Grounds/Lock.jy/res/icons/armed.png'
I_UNARMED_PATH = '/home/jshuay/Testing_Grounds/Lock.jy/res/icons/unarmed.png'
I_HOLD_PATH = '/home/jshuay/Testing_Grounds/Lock.jy/res/icons/hold.png'
S_KEY_PATH = '/home/jshuay/Testing_Grounds/Lock.jy/scripts/key.sh'
S_HOLD_PATH = '/home/jshuay/Testing_Grounds/Lock.jy/scripts/hold.sh'
F_HOLD_PATH = '/tmp/hold.jy'
F_LOCK_PATH = '/tmp/lock.jy'
F_UNLOCK_PATH = '/tmp/unlock.jy'


class Lock_jy:
    def __init__(self):
        status = appindicator.CATEGORY_APPLICATION_STATUS
        self.ind = appindicator.Indicator("debian-doc-menu",
                                          I_UNARMED_PATH,
                                          status)
        self.ind.set_status(appindicator.STATUS_ACTIVE)
        self.menu_setup()
        self.ind.set_menu(self.menu)
        self.isHold = False
        self.isArmed = False
        self.status_update()
        gtk.timeout_add(1000, self.status_update)

    def menu_setup(self):
        self.menu = gtk.Menu()

        self.hold_item = gtk.MenuItem("Hold")
        self.hold_item.connect("activate", self.hold)
        self.hold_item.show()
        self.menu.append(self.hold_item)

        self.quit_item = gtk.MenuItem("Quit")
        self.quit_item.connect("activate", self.quit)
        self.quit_item.show()
        self.menu.append(self.quit_item)

    def main(self):
        gtk.main()

    def hold(self, widget):
        if self.isHold:
            self.ind.set_icon(I_ARMED_PATH)
            self.hold_item.set_label("Hold")
            cmd = S_HOLD_PATH
            p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
            p.wait()
        else:
            self.ind.set_icon(I_HOLD_PATH)
            self.hold_item.set_label("Unhold")
            cmd = S_HOLD_PATH
            p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
            p.wait()
        self.isHold = not self.isHold

    def status_update(self):
        if os.path.isfile(F_HOLD_PATH) and not self.isHold:
            self.isHold = True
            self.ind.set_icon(I_HOLD_PATH)
            self.hold_item.set_label("Unhold")
        elif not os.path.isfile(F_HOLD_PATH) and self.isHold:
            self.isHold = False
            if self.isArmed:
                self.ind.set_icon(I_ARMED_PATH)
            else:
                self.ind.set_icon(I_UNARMED_PATH)
            self.hold_item.set_label("Hold")
        cmd = S_KEY_PATH
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        p.wait()
        if (os.path.isfile(F_LOCK_PATH) or
                os.path.isfile(F_UNLOCK_PATH)) and not self.isArmed:
            self.isArmed = True
            self.ind.set_icon(I_ARMED_PATH)
        elif not (os.path.isfile(F_LOCK_PATH) or
                  os.path.isfile(F_UNLOCK_PATH)) and self.isArmed:
            self.isArmed = False
            self.ind.set_icon(I_UNARMED_PATH)
        return True

    def quit(self, widget):
        if os.path.isfile(F_HOLD_PATH):
            os.remove(F_HOLD_PATH)
        if os.path.isfile(F_LOCK_PATH):
            os.remove(F_LOCK_PATH)
        if os.path.isfile(F_UNLOCK_PATH):
            os.remove(F_UNLOCK_PATH)
        sys.exit(0)

if __name__ == "__main__":
    indicator = Lock_jy()
    indicator.main()
