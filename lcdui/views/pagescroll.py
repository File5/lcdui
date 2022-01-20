from lcdui.event import EventType

from lcdui.views import View
from lcdui.views.layout import Layout
from lcdui.views.scrollbar import VScrollBar


class PageScrollLayout(View):
    def __init__(self, layout, scroll_bar=True, parent=None):
        super().__init__(parent)
        self.scroll_bar = scroll_bar
        w, h = self.parent.size
        if scroll_bar:
            w -= 1
        self.size = w, h

        self.pages = []
        rows = 0
        self.before_page_rows = []
        for page in layout:
            self.before_page_rows.append(rows)
            layout = Layout(page, self)
            self.pages.append(layout)
            rows += len(layout.layout)
        self.selected_page = 0
        self.scroll_bar_view = None
        if scroll_bar:
            self.scroll_bar_view = VScrollBar(rows, parent.size[1], parent=self)

    @property
    def page(self):
        return self.pages[self.selected_page]

    def print(self, canvas, final=False):
        w, h = self.parent.size
        if self.scroll_bar:
            w -= 1
        self.page.print(canvas.sub_canvas(w, h), final)
        if self.scroll_bar:
            canvas.position = (w, 0)
            self.scroll_bar_view.print(canvas.sub_canvas(1, h), final)

    def handle(self, event):
        focus_handled = self.page.handle(event)

        result = focus_handled
        if not focus_handled:
            # change the page
            if event.type == EventType.DOWN:
                if self.selected_page < len(self.pages) - 1:
                    self.selected_page += 1
                    result = True
            elif event.type == EventType.UP:
                if self.selected_page > 0:
                    self.selected_page -= 1
                    result = True

        if self.scroll_bar:
            # update scrollbar with new focus
            focus_pos = self.page.focus_grid._focus
            self.scroll_bar_view.value = self.before_page_rows[self.selected_page] + focus_pos[1]
        return result
