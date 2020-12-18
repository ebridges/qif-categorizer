import re
import wx
import wx.grid


class MyGrid(wx.grid.Grid):
    def __init__(self, parent, categories, uncategorized):
        wx.grid.Grid.__init__(self, parent)
        self.categories = categories
        self.uncategorized_transactions = uncategorized
        self.Bind(wx.grid.EVT_GRID_CELL_CHANGED, self.on_cell_change)

    def on_cell_change(self, evt):

        row = evt.GetRow()
        col = evt.GetCol()
        val = self.GetCellValue(row, col)
        regex = f'.*{val}.*'

        for cat in self.categories:
            c = cat.split(':')
            subcat = c[len(c) - 1]
            if re.match(regex, subcat, re.IGNORECASE):
                self.SetCellValue(row, col, cat)

    def lookup(self, instance, value):
        """
        Autocomplete example for reference
        """
        self.root.suggestion_text = ''
        val = value[value.rfind(' ') + 1 :]  # noqa: E203
        if not val:
            return
        try:
            word = [word for word in self.categories if word.startswith(val)][
                0
            ][
                len(val) :  # noqa: E203
            ]
            if not word:
                return
            self.root.suggestion_text = word
        except IndexError:
            print('Index Error.')


class CategorizerUIFrame(wx.Frame):
    def __init__(self, parent, categories, uncategorized):
        wx.Frame.__init__(self, parent)
        self.categories = categories
        self.uncategorized_transactions = uncategorized

        grid = MyGrid(self, categories, uncategorized)
        grid.CreateGrid(len(self.uncategorized_transactions), 5)

        row = 0
        for id, t in self.uncategorized_transactions.items():
            grid.SetCellValue(row, 0, str(t.date.date()))
            grid.SetReadOnly(row, 0)
            grid.SetCellValue(row, 1, str(t.payee))
            grid.SetReadOnly(row, 1)
            grid.SetCellValue(row, 2, str(t.amount))
            grid.SetCellAlignment(row, 2, wx.ALIGN_RIGHT, wx.ALIGN_CENTRE)
            grid.SetReadOnly(row, 2)
            grid.SetCellValue(row, 4, str(id))
            grid.SetReadOnly(row, 4)

            row = row + 1

        cat_width = 0
        for c in self.categories:
            cat_width = max(cat_width, len(str(c)))

        grid.AutoSizeColumn(0, setAsMin=True)
        grid.AutoSizeColumn(1, setAsMin=True)
        grid.AutoSizeColumn(2, setAsMin=True)
        grid.SetColSize(3, cat_width * 5)
        grid.AutoSizeColumn(4, setAsMin=True)
