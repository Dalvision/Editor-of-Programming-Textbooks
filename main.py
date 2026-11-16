import flet as ft
import json

class Link:
	def __init__(self, rubric:int, text:str):
		self.rubric = rubric
		self.text = text

class Rubric:
	def __init__(self, number:int, text:str, links:list):
		self.number = number
		self.text = text
		self.links = [Link(**data) for data in links]

class Chapter:
    def __init__(self, number: int, title: str, description: str, rubrics: list):
        self.number = number
        self.title = title
        self.description = description
        self.rubrics = [Rubric(**data) for data in rubrics]


class Book:
	def __init__(self, name:str, author:str, chapters:list):
		self.name = name
		self.author = author
		self.chapters = [Chapter(**data) for data in chapters]


def main(page: ft.Page):

    def open_books():
        try:
            with open("book.json", "r", encoding="utf-8") as f:
                lib = json.load(f)
            return [Book(**data) for data in lib]
        except:
            raise ("Не удалось загрузить книгу")

    def create_menu_rubrics(target_rubric:int, rubrics:list):
        nonlocal panel_reading

        for i in rubrics:
            if i.number == target_rubric:
                formatted_text = i.text.replace("\t", "    ")
                page_text = ft.TextField(
                    value=formatted_text,
                    multiline=True,
                    read_only=True,
                    max_lines=25,
                    text_style=ft.TextStyle(font_family="Calibri"),
                )
                links = i.links
        
        menu_rubrics = ft.Container(
            content=ft.Column(
                controls=[
                ft.ElevatedButton(
                    text=i.text,
                    tooltip="Перейти",
                    on_click=lambda e, tr=i.rubric, rl=rubrics: create_menu_rubrics(tr, rl)) for i in links
                ],
                alignment=ft.MainAxisAlignment.START,
            ),
        )

        panel_reading = ft.Column([page_text, menu_rubrics], alignment=ft.MainAxisAlignment.CENTER)
        page.navigation_bar.selected_index = 1
        navigate(None)
        page.update()

    def create_chapter_card(title: str, description:str, rubrics:list):
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Column(
                        controls=[
                            ft.TextButton(
                                content=ft.Text(
                                    value=title,
                                    size=14,
                                    weight=ft.FontWeight.BOLD,
                                ),
                                tooltip="Читать",
                                style=ft.ButtonStyle(
                                    color={
                                        ft.ControlState.DEFAULT: ft.Colors.ON_SURFACE,
                                        ft.ControlState.HOVERED: ft.Colors.PRIMARY,
                                    },
                                    overlay_color=ft.Colors.TRANSPARENT,
                                    padding=0,
                                ),
                                on_click=lambda e, tr=1, rl=rubrics: create_menu_rubrics(tr, rl),
                            ),
                            ft.Text(description, size=11)
                        ],
                        spacing=2,
                        expand=True,
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=1,
            border_radius=12,
            expand=True,
        )

    def create_book_card(name: str, author: str, chapters: list):

        def open_or_close_menu(target_menu):
            target_menu.visible = not target_menu.visible
            page.update()

        menu = ft.Container(
            content=ft.Column(
                controls=[create_chapter_card(i.title, i.description, i.rubrics) for i in chapters]
            ),
            visible=False,
        )
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Column(
                        controls=[
                            ft.Text(name, size=16, weight=ft.FontWeight.BOLD),
                            ft.Text(author, size=13, color=ft.Colors.GREY_700),
                            menu
                        ],
                        spacing=2,
                        expand=True,
                    ),
                    ft.IconButton(
                        icon=ft.Icons.MENU,
                        on_click=lambda e, m=menu: open_or_close_menu(m),
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.START,
            ),
            padding=15,
            border=ft.border.all(1, ft.Colors.GREY_700),
            border_radius=12,
            expand=True,
        )

    """Переменные"""
    page.title = "Programmed Textbook"
    page.window.width = 600
    page.window.height = 800
    books = open_books()

    """Настройки"""

    """Навигация - панели"""
    def navigate(e):
        page.clean()
        index = page.navigation_bar.selected_index
        if index == 0:
            page.add(panel_books)
        elif index == 1:
            page.add(panel_reading)
        elif index == 2:
            page.add(panel_settings)

    panel_books = ft.Column([create_book_card(i.name, i.author, i.chapters) for i in books], alignment=ft.MainAxisAlignment.CENTER)
    panel_reading = ft.Column([], alignment=ft.MainAxisAlignment.CENTER)
    panel_settings = ft.Column([], alignment=ft.MainAxisAlignment.CENTER)

    page.navigation_bar = ft.NavigationBar(destinations=[
        ft.NavigationBarDestination(icon=ft.Icons.BOOKMARKS_OUTLINED, label='Книги'),
        ft.NavigationBarDestination(icon=ft.Icons.IMPORT_CONTACTS, label='Читать'),
        ft.NavigationBarDestination(icon=ft.Icons.SETTINGS, label='Опции')
    ], on_change=navigate)
    page.add(panel_books)

ft.app(target=main)