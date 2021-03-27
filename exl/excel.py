import win32com.client as win32

from old.field_old import Field
from old.point_old import PointOld

excel = win32.GetActiveObject('Excel.Application')

useExcel = False


# b = excel.run("getPointByCoords", 1,9,True)
# print("Hello")
# excel.run("setPointPossibleVals",1,1, range(1,10,2),True)
# excel.run("setPointVal",1,1, 0,True)

def reprFieldInXl(field: Field):
    if not useExcel: return
    excel.ScreenUpdating = False
    for pt in field.get_all_points():
        changeCellInXl(pt)
    excel.ScreenUpdating = True


def changeCellInXl(pt: PointOld):
    if not useExcel: return
    excel.ScreenUpdating = False
    if pt.value != 0:
        excel.run("setPointVal", pt.row, pt.column, pt.value, False, pt.initial)
    excel.ScreenUpdating = True


def changePossibles(pt: PointOld):
    if not useExcel: return
    excel.run("setPointPossibleVals", pt.row, pt.column, pt.possible_values, False)


def initField():
    if not useExcel: return
    excel.ScreenUpdating = False
    excel.run("defineField")
    excel.ScreenUpdating = True
