from tkinter import INSERT

from project.plugs.log_tool import LogTool


class ShowTool(object):

    @classmethod
    def init(cls,ui):
        cls.ui = ui


    @classmethod
    def show(cls, content):
        LogTool.info(content)
        cls.ui.insert(INSERT, f"{content}\n")

