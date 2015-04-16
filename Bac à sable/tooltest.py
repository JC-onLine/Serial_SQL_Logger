import wx
print "wxpython:   ",wx.__version__

tsize = (24,24)
class InputFrame(wx.Frame):
    def ToggleTest(self,event,init=False):
        if init:
            self.Test = False
        else:
            self.Test = not self.Test
        print "Test status = ",self.Test
        if self.Test:
            bmp =  wx.ArtProvider.GetBitmap(wx.ART_NEW, wx.ART_TOOLBAR, tsize)
            self.TestButton.SetNormalBitmap(bmp)
        else:
            bmp = wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_TOOLBAR, tsize)
            self.TestButton.SetNormalBitmap(bmp)
        self.toolbar.Realize()


    def __init__(self, parent):
        wx.Frame.__init__(self, parent=parent, title = "Test Toolbar",)
        topSizer = wx.BoxSizer(wx.VERTICAL)
        panel = wx.Panel(self)
        mainSizer = wx.BoxSizer(wx.HORIZONTAL)
        panel.SetSizer(mainSizer)
        self.GUPstat = wx.StaticText(panel, -1, "",size=(400,40))
        self.GUPstat.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))
        mainSizer.Add(self.GUPstat, 1)

        menubar = wx.MenuBar()
        self.toolbar = self.CreateToolBar()

        bmp = wx.ArtProvider.GetBitmap(wx.ART_COPY, wx.ART_TOOLBAR, tsize)
        self.TestButton = self.toolbar.AddLabelTool(2001, "Test", bmp)
        self.toolbar.Realize()
        self.ToggleTest(None,init=True)
        self.toolbar.Bind(wx.EVT_TOOL, self.ToggleTest)
        mainSizer.Fit(panel)
        self.Fit()
        self.Show(True)

app = wx.PySimpleApp()
frame = InputFrame(None)
frame.Show(True)
app.MainLoop()
