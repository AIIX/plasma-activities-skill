"""
Plasma Activities Mycroft Skill. 
"""

import sys
import dbus
import re
from traceback import print_exc
from os.path import dirname
from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill, intent_handler
from mycroft.util.log import getLogger

__author__ = 'aix'

LOGGER = getLogger(__name__)


class ActivitiesPlasmaDesktopSkill(MycroftSkill):
    """
    Activities Skill Class.
    """

    def __init__(self):
        """
        Initialization
        """
        super(
            ActivitiesPlasmaDesktopSkill,
            self).__init__(
                name="ActivitiesPlasmaDesktopSkill")

    @intent_handler(IntentBuilder("ActivitiesKeywordIntent").require("ActivitiesCreateKeyword").build())
    def handle_activities_create_plasma_skill_intent(self, message):
        """
        Create Activities
        """
        utterance = message.data.get('utterance').lower()
        utterance = utterance.replace(
            message.data.get('ActivitiesCreateKeyword'), '')
        searchString = utterance
        speakword = searchString.lstrip(' ')

        bus = dbus.SessionBus()
        remote_object = bus.get_object(
            "org.kde.ActivityManager",
            "/ActivityManager/Activities")
        remote_object.AddActivity(
            speakword,
            dbus_interface="org.kde.ActivityManager.Activities")
        remote_object2 = bus.get_object("org.kde.plasmashell", "/PlasmaShell")
        remote_object2.toggleActivityManager(
            dbus_interface="org.kde.PlasmaShell")
        speakdlg = "New Activity {0} Has Been Created".format(speakword)
        self.speak(speakdlg)

    @intent_handler(IntentBuilder("ShowActivitiesIntent").require("ActivitiesShowKeyword").build())
    def handle_activities_show_plasma_skill_intent(self, message):
        """
        Show Activities
        """
        bus = dbus.SessionBus()
        remote_object2 = bus.get_object("org.kde.plasmashell", "/PlasmaShell")
        remote_object2.toggleActivityManager(dbus_interface="org.kde.PlasmaShell")

    @intent_handler(IntentBuilder("RemoveActivitiesIntent").require("ActivitiesRemoveKeyword").build())
    def handle_activities_remove_plasma_skill_intent(self, message):
        """
        Remove Activities
        """
        utterance = message.data.get('utterance').lower()
        utterance = utterance.replace(
            message.data.get('ActivitiesRemoveKeyword'), '')
        searchString = utterance.lower()
        speakword = searchString.lstrip(' ')
        actinfo = []
        bus = dbus.SessionBus()
        remote_object = bus.get_object(
            "org.kde.ActivityManager",
            "/ActivityManager/Activities")
        callback = remote_object.ListActivitiesWithInformation(
            dbus_interface="org.kde.ActivityManager.Activities")
        spkdlg = "Activity {0} has been removed".format(speakword)
        self.speak(spkdlg)
        for i in range(len(callback)):
            temp_callback = list(map(str, callback[i]))
            actinfo.append(temp_callback)
            actenum = actinfo[i][1]
            actgetid = actenum.lower()
            if(actgetid == speakword):
                actid = actinfo[i][0]
                self.removeactivity(actid)

    def removeactivity(self, activitieslist):
        """
        Remove Activities SubFunc
        """
        activityaddr = activitieslist
        bus = dbus.SessionBus()
        remote_object = bus.get_object(
            "org.kde.ActivityManager",
            "/ActivityManager/Activities")
        remote_object.RemoveActivity(
            activityaddr,
            dbus_interface="org.kde.ActivityManager.Activities")

    @intent_handler(IntentBuilder("StopActivitiesIntent").require("ActivitiesStopKeyword").build())
    def handle_activities_stop_plasma_skill_intent(self, message):
        """
        Stop Activities
        """
        utterance = message.data.get('utterance').lower()
        utterance = utterance.replace(
            message.data.get('ActivitiesStopKeyword'), '')
        searchString = utterance.lower()
        speakword = searchString.lstrip(' ')
        actinfo = []
        bus = dbus.SessionBus()
        remote_object = bus.get_object(
            "org.kde.ActivityManager",
            "/ActivityManager/Activities")
        callback = remote_object.ListActivitiesWithInformation(
            dbus_interface="org.kde.ActivityManager.Activities")
        spkdlg = "Activity {0} has been stopped".format(speakword)
        self.speak(spkdlg)
        for i in range(len(callback)):
            temp_callback = list(map(str, callback[i]))
            actinfo.append(temp_callback)
            actenum = actinfo[i][1]
            actgetid = actenum.lower()
            if(actgetid == speakword):
                actid = actinfo[i][0]
                self.stopactivity(actid)
                
    def stopactivity(self, activitieslist):
        """
        Stop Activities SubFunc
        """
        activityaddr = activitieslist
        bus = dbus.SessionBus()
        remote_object = bus.get_object(
            "org.kde.ActivityManager",
            "/ActivityManager/Activities")
        remote_object.StopActivity(
            activityaddr,
            dbus_interface="org.kde.ActivityManager.Activities")

    @intent_handler(IntentBuilder("SwitchActivitiesIntent").require("ActivitiesSwitchKeyword").build())
    def handle_activities_switch_plasma_skill_intent(self, message):
        """
        Switch Activities
        """
        utterance = message.data.get('utterance').lower()
        utterance = utterance.replace(
            message.data.get('ActivitiesSwitchKeyword'), '')
        searchString = utterance.lower()
        speakword = searchString.lstrip(' ')
        actinfo = []
        bus = dbus.SessionBus()
        remote_object = bus.get_object(
            "org.kde.ActivityManager",
            "/ActivityManager/Activities")
        callback = remote_object.ListActivitiesWithInformation(
            dbus_interface="org.kde.ActivityManager.Activities")
        self.speak_dialog(
            "activities.switch",
            data={'SwitchActivityName': speakword})
        for i in range(len(callback)):
            temp_callback = list(map(str, callback[i]))
            actinfo.append(temp_callback)
            actenum = actinfo[i][1]
            actgetid = actenum.lower()
            if(actgetid == speakword):
                actid = actinfo[i][0]
                self.switchtoactivity(actid)

    def switchtoactivity(self, activitieslist):
        """
        Switch Activities SubFunc
        """
        activityaddr = activitieslist
        bus = dbus.SessionBus()
        remote_object = bus.get_object(
            "org.kde.ActivityManager",
            "/ActivityManager/Activities")
        remote_object.SetCurrentActivity(
            activityaddr,
            dbus_interface="org.kde.ActivityManager.Activities")

    def stop(self):
        """
        Mycroft Stop Function
        """
        pass


def create_skill():
    """
    Mycroft Create Skill Function
    """
    return ActivitiesPlasmaDesktopSkill()
