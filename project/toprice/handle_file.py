import os
import re

from project.plugs.log_tool import LogTool
from project.plugs.show_tool import ShowTool


class HandleFile(object):
    """
    处理文件
    """

    def __init__(self, file_path):
        self.file_path = file_path.replace("file:///", "")  # 文件路径
        LogTool.info(f"路径为：{self.file_path}")
        self.content = None  # 文本内容
        pass

    def run(self):
        self._open_file()
        ret = []
        par_id = self._get_par_id()
        if par_id is None:
            return None
        ret.append(par_id)
        local = self._get_local()
        ret = ret + local
        par1 = self._get_par_1()
        ret.append(par1)
        par2 = self._get_par_2()
        ret.append(par2)
        par3 = self._get_par_3()
        ret = ret + par3
        return ret

    def _open_file(self):
        """
        打开文件操作
        :param file_path: 文件路径
        :return:
        """
        ShowTool.show("打开文件")
        f = None
        try:
            with open(os.path.abspath(self.file_path), 'r+', encoding='gbk') as f:
                self.content = f.read()
        except Exception as e:
            LogTool.error(f"打开文件出错;【{str(e)}】")
        finally:
            f.close() if f else None

    def _get_par_id(self):
        # pattern = re.compile(r'RUN.+?ID.+?([\d,.]+)')
        pattern = re.compile(r'Run.+?ID.+?([\d,.]+)')
        ret = pattern.findall(self.content)
        if ret:
            for r in ret:
                ShowTool.show("解析出id")
                return r
        return None

    def _get_local(self):
        """
        捞取local
        :param content:
        :return:
        """
        """
        * Location           : Nanchang
        * Meteo station      : Nanchang
        * Soil type          : Nanchang_Soil
        * Crop calendar      : Nanchang-Rice1
        * Substance          : A
        * Application scheme : A-4-2
        * Deposition scheme  : No
        * Irrigation scheme  : Surface_Auto
        *
        * End of PEARL REPORT: Header

        * PEARL REPORT: Leaching
        * Start date      :   01-Jan-1901
        * End date        :   31-Dec-1926
        * Target depth    :   1.00 m
        * Annual application to the crop at 10-Aug; dosage =     0.0500 kg.ha-1
        * Annual application to the crop at 17-Aug; dosage =     0.0500 kg.ha-1

        * Leaching summary for compound A
        """
        ret_list = []
        # pattern = re.compile(r'\*.+?Location.+?Leaching.+?summary')
        pattern = re.compile(r'\*.+?Location[\s\S]+?Leaching.+?summary')
        ret = pattern.findall(self.content)
        if ret:
            for r in ret:
                #  * Location           : Nanchang
                pattern1 = re.compile(r'\*.+?Location.+?:(.+?)<BR>')
                ret1 = pattern1.findall(r)
                if ret1:
                    for r1 in ret1:
                        ret_list.append(r1[6:])
                        break

                # * Substance          : A
                pattern2 = re.compile(r'\*.+?Substance.+?:(.+?)<BR>')
                ret2 = pattern2.findall(r)
                if ret2:
                    for r2 in ret2:
                        ret_list.append(r2[6:])
                        break

                # * Annual application to the crop at 10-Aug; dosage =     0.0500 kg.ha-1
                pattern3 = re.compile(r'crop.+?at(.+);.+?dosage')
                ret3 = pattern3.findall(r)
                if ret3:
                    for r3 in ret3:
                        ret_list.append(r3[6:])
                        break
                break

        return ret_list

    def _get_par_1(self):
        # The average concentration of 0333 closest to the 89th percentile is      0.019137 ug/L'
        pattern = re.compile(r'average.+?concentration.+?of.+?percentile.+?is.+?([\d,.]+).+?ug/L')
        ret = pattern.findall(self.content)
        if ret:
            for r in ret:
                return r
        return None

    def _get_par_2(self):
        # The 89 percentile peak concentration of 0333 in the pond is     21.787681 ug/L'
        pattern = re.compile(r'peak.+?concentration.+?of.+?pond.+?is.+?([\d,.]+).+?ug/L')
        ret = pattern.findall(self.content)
        if ret:
            for r in ret:
                return r
        return None

    def _get_par_3(self):
        # * Target  TWA period    Maximum TWA             TWA
        # * End of TOXSWA REPORT: Time weighted average exposure concentrations (TWA) water layer selected year
        pattern = re.compile(
            r'Target.+?TWA.+?period.+?Maximum.+?TWA[\s\S]+?substance.+?<BR>([\s\S]+?)\*.+?<BR>[\s\S]+?End.+?of.+?TOXSWA.+?REPORT')
        temp = pattern.findall(self.content)
        ret = []
        if temp:
            for r in temp:
                # TWA1d&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1.00&nbsp;&nbsp;&nbsp;&nbsp;31-Dec-1920-00h30&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;17.65 <BR>
                pattern1 = re.compile(r'.{7}(\d*\.\d*).{0,3}?<BR>')
                temp2 = pattern1.findall(r)
                for r2 in temp2:
                    ret.append(r2)
        return ret

# handleFile = HandleFile(r"C:\Users\snow\Desktop\原始数据\A-4-2.htm")
# handleFile.run()
