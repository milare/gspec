from gettext import gettext as _

import os
import gtk
import gedit
import webbrowser
import pygtk
import webkit
import re
import urllib


class BrowserPage(webkit.WebView):
    def __init__(self):
        webkit.WebView.__init__(self)


# Menu item example, insert a new item in the Tools menu
ui_str = """<ui>
  <menubar name="MenuBar">
    <menu name="ToolsMenu" action="Tools">
      <placeholder name="ToolsOps_2">
        <menuitem name="GSpec" action="GSpec"/>
      </placeholder>
    </menu>
  </menubar>
</ui>
"""
class GSpecWindowHelper:
    def __init__(self, plugin, window):
        self._window = window
        self._plugin = plugin
        self._browser = None
        # Insert menu items
        self._insert_menu()

    def deactivate(self):
        # Remove any installed menu items
        self._remove_menu()
        self._browser = None
        self._window = None
        self._plugin = None
        self._action_group = None

    def _insert_menu(self):

        # Get the GtkUIManager
        manager = self._window.get_ui_manager()

        actions = [
            ('GSpec', gtk.STOCK_EDIT, _('Run GSpec'), '<Alt>r', _("Run Spec File"), self.run_spec)
        ]
        # Create a new action group
        self._action_group = gtk.ActionGroup("GSpecPluginActions")
        self._action_group.add_actions(actions, self._window)

        # Insert the action group
        manager.insert_action_group(self._action_group, -1)

        # Merge the UI
        self._ui_id = manager.add_ui_from_string(ui_str)

    def _remove_menu(self):
        # Get the GtkUIManager
        manager = self._window.get_ui_manager()

        # Remove the ui
        manager.remove_ui(self._ui_id)

        # Remove the action group
        manager.remove_action_group(self._action_group)

        # Make sure the manager updates
        manager.ensure_update()


    def update_ui(self):
        self._action_group.set_sensitive(self._window.get_active_document() != None)


    # Menu activate handlers
    def run_spec(self, *args):


        #current_file = self._window.get_active_tab().get_document().get_uri()
        current_file = gedit.app_get_default().get_active_window().get_active_tab().get_document().get_uri()

        index = current_file.find("spec")

        root_path = current_file[7:index-1]

        print root_path
        cmd = "spec " + current_file[7:] + " --format html"

        retcode = os.popen(cmd)

        self._browser = BrowserPage()
        #self._browser.connect('navigation-requested', self.on_navigation_request)
        self._window = gtk.Window()
        self._window.set_type_hint(gtk.gdk.WINDOW_TYPE_HINT_DIALOG)
        self._window.resize(700,510)
        self._window.set_destroy_with_parent(True)
        self._window.add(self._browser)
        self._window.show_all()

        self._window.set_title("GSpec")

        #current_plugin_file = os.path.abspath( __file__ )
        #index = current_plugin_file.find("__init__")
        #f = open(current_plugin_file[:index-1]+"/results/result.html", 'r')


        self._browser.load_string(retcode.read(), "text/html", "utf-8", "about:")
#        os.remove(current_plugin_file[:index-1]+"/results/result.html")


class GSpecPlugin(gedit.Plugin):
    def __init__(self):
        gedit.Plugin.__init__(self)
        self._instances = {}

    def activate(self, window):
        self._instances[window] = GSpecWindowHelper(self, window)

    def deactivate(self, window):
        self._instances[window].deactivate()
        del self._instances[window]

