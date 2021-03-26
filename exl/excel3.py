def useExcel():
    import pywintypes
    import win32com.client as win32

    # from point import Point
    # from field import Field

    useExcel = True
    try:
        excel = win32.GetActiveObject('Excel.Application')
        _ = excel.name
    except Exception as e:
        useExcel = False
        # print(e)
        print("Excel is unavailable")

    def possibles_str_repr(possible_values: list) -> str:
        txt = "1  2  3\n4  5  6\n7  8  9"
        if len(possible_values) == 0:
            return ""
        elif len(possible_values) == 9:
            return txt

        for x in "123456789":
            if int(x) not in possible_values:
                txt = txt.replace(str(x), " ")
        return txt

    def reprFieldInXl(field):
        if not useExcel:
            return
        try:
            excel.ScreenUpdating = False
            for pt in field.get_all_points():
                changeCellInXl(pt)
        finally:
            # print("excel.ScreenUpdating = True")
            excel.ScreenUpdating = True

    def changeCellInXl(pt):
        global useExcel
        if not useExcel: return
        # excel.ScreenUpdating = False
        if pt.value != 0:
            try:
                excel.run("set_value", pt.row, pt.column, pt.value, True)
            except pywintypes.com_error as e:
                print("Wintype error", e)
                useExcel = False
        else:
            possible = pt.possible_values
            if len(possible) == 1:
                print(f"Only one option ({possible[0]}) is valid for {pt}, but it is not marked to be a value")
                raise Exception("Something wrong")
            try:
                excel.run("set_value", pt.row, pt.column, possibles_str_repr(possible), True)
            except pywintypes.com_error as e:
                print("Wintype error", e)
                useExcel = False
