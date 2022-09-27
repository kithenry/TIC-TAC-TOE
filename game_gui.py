import flet
from flet import (
    Page,
    Row,
    Column,
    Text,
    alignment,
    Container,
    padding,
    margin,
    OutlinedButton,
    ButtonStyle,
)
from flet.buttons import RoundedRectangleBorder
import base64
import game_logic


player_o = base64.b64encode(open("images/player_o.png", "rb").read()).decode("utf-8")
player_x = base64.b64encode(open("images/player_x.png", "rb").read()).decode("utf-8")


class Custom_Container(Container):
    def __init__(self, click, row=None, column=None, **kwargs):
        super().__init__(on_click=click)
        self.row = row
        self.column = column


class App:

    """Tic tac toe GUI"""

     def __init__(self, page: Page):
        self.xwins, self.owins, self.numdraws = 0, 0, 0
        self.page = page
        self.game = game_logic.Game(self)
        self.game_ended = False
        self.page.title = "TIC TAC TOE"
        self.row, self.col = None, None
        self.player_x = player_x
        self.player_o = player_o
        self.board_container = Column(width=600, height=600, spacing=5)
        self.main_container = Container(width=580, height=580)
        self.main_column = Column()
        self.row1, self.row2, self.row3 = Row(), Row(), Row()
        self.rows = [self.row1, self.row2, self.row3]
        self.row1_containers = [
            Custom_Container(self.change_image, row=0, column=0),
            Custom_Container(self.change_image, row=0, column=1),
            Custom_Container(self.change_image, row=0, column=2),
        ]
        self.row2_containers = [
            Custom_Container(self.change_image, row=1, column=0),
            Custom_Container(self.change_image, row=1, column=1),
            Custom_Container(self.change_image, row=1, column=2),
        ]
        self.row3_containers = [
            Custom_Container(self.change_image, row=2, column=0),
            Custom_Container(self.change_image, row=2, column=1),
            Custom_Container(self.change_image, row=2, column=2),
        ]
        self.row_containers = [
            self.row1_containers,
            self.row2_containers,
            self.row3_containers,
        ]
        self.board_dict = {
            0: {
                0: self.row1_containers[0],
                1: self.row1_containers[1],
                2: self.row1_containers[2],
            },
            1: {
                0: self.row2_containers[0],
                1: self.row2_containers[1],
                2: self.row2_containers[2],
            },
            2: {
                0: self.row3_containers[0],
                1: self.row3_containers[1],
                2: self.row3_containers[2],
            },
        }
        gamestats = [
            Text(f"HUMAN: {self.xwins}", font_family="Monospace", size=20),
            Text(f"DRAW: {self.numdraws}", font_family="Monospace", size=20),
            Text(f"AI: {self.owins}", font_family="Monospace", size=20),
        ]
        self.human_win_container = Container(
            content=gamestats[0], expand=True, alignment=alignment.center
        )
        self.draw_container = Container(
            content=gamestats[1], expand=True, alignment=alignment.center
        )
        self.ai_win_container = Container(
            content=gamestats[2], expand=True, alignment=alignment.center
        )
        self.win_stats_row = Row(
            spacing=36,
            alignment="center",
            controls=[
                self.human_win_container,
                self.draw_container,
                self.ai_win_container,
            ],
            vertical_alignment="center",
        )

        self.start_button = Container(
            content=OutlinedButton(
                text="New Game",
                style=ButtonStyle(shape={"": RoundedRectangleBorder(radius=2)}),
                on_click=self.new_game,
            ),
        )

        for row_container_array in self.row_containers:
            for row_container in row_container_array:
                row_container.padding = padding.all(0)
                row_container.alignment = alignment.Alignment(0, 0)
                row_container.horizontal_alignment = "center"
                row_container.bgcolor = "#34495e"
                row_container.margin = margin.all(1)
                row_container.height = 180
                row_container.width = 180
                row_container.expand = True

        for row, containers in zip(self.rows, self.row_containers):
            [row.controls.append(container) for container in containers]
            row.expand = True

        self.main_column.controls = self.rows
        self.main_column.wrap = False
        self.main_container.content = self.main_column
        self.main_container.padding = padding.all(1)
        self.main_container.margin = margin.all(1)
        self.main_container.bgcolor = "#475c6f"
        self.main_container.border_radius = 4
        self.main_container.alignment = alignment.Alignment(0, 0)
        self.main_container.horizontal_alignment = "center"
        self.board_container.controls = [
            self.main_container,
            self.win_stats_row,
            self.start_button,
        ]
        self.board_container.bgcolor = "#475c6f"
        self.board_container.alignment = "center"
        self.board_container.horizontal_alignment = "center"

        self.page.bgcolor = "#2d3d50"
        self.page.horizontal_alignment = "center"
        self.page.vertical_alignment = "center"
        self.page.add(self.board_container)
        self.game.play()

    def new_game(self):
            
        for i in range(3):
            for j in range(3):
                self.board_dict[i][j].image_src_base64 = None
                self.board_dict[i][j].update()
        self.game.player_turn = None
        self.game.initialize_game()
        self.game.play()

    def change_image(self, e):
        if (not self.game_ended) and (self.game.player_turn == "X"):
            e.control.image_src_base64 = self.player_x
            self.row, self.col = e.control.row, e.control.column
            e.control.update()
        elif self.game_ended:
            self.new_game()

    def update_winstats(self, state):
        if state == ".":
            self.numdraws += 1
            self.win_stats_row.controls[1].content.value = f"DRAW: {self.numdraws}"
            self.win_stats_row.controls[1].content.update()
        elif state == "X":
            self.xwins += 1
            self.win_stats_row.controls[0].content.value = f"HUMAN: {self.xwins}"
            self.win_stats_row.controls[0].update()
        elif state == "O":
            self.owins += 1
            self.win_stats_row.controls[2].content.value = f"AI: {self.owins}"
            self.win_stats_row.controls[2].update()

    def update_startbutton(self, new_text):
        self.start_button.content.text = new_text
        self.start_button.content.update()


if __name__ == "__main__":
    flet.app(target=App)
