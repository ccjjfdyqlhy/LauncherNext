import os
import configparser
from nicegui import ui,app
from nicegui.events import ValueChangeEventArguments

__version__='0.0.3'
forecolor='#FFFFFF'
app.native.window_args['resizable'] = False
app.native.start_args['debug'] = False
app.add_static_files('/static', 'static')

cwd=os.getcwd()
game_name = 'MCSA Enchanted Light'
config = configparser.ConfigParser()

def set_background(color: str) -> None:
    ui.query('body').style(f'background-color: {color}')

def set_fgc(event: ValueChangeEventArguments):
    name = type(event.sender).__name__
    if f'{name}: {event.value}' == 'Radio: Grey':
        ui.colors(primary='#555')
        forecolor='#555'
        config.set('settings', 'forecolor', '#555')
    elif f'{name}: {event.value}' == 'Radio: Atlantic':
        ui.colors(primary='#3288AE')
        forecolor='#3288AE'
        config.set('settings', 'forecolor', '#3288AE')
    elif f'{name}: {event.value}' == 'Radio: Forest':
        ui.colors(primary='#346C48')
        forecolor='#346C48'
        config.set('settings', 'forecolor', '#346C48')
    elif f'{name}: {event.value}' == 'Radio: Deep Ocean':
        ui.colors(primary='#072A69')
        forecolor='#072A69'
        config.set('settings', 'forecolor', '#072A69')
    else:
        ui.colors()
        config.set('settings', 'forecolor', '#FFFFFF')

def set_bgc(event: ValueChangeEventArguments):
    name = type(event.sender).__name__
    if f'{name}: {event.value}' == 'Radio: Orange':
        set_background('#ffeedd')
        config.set('settings', 'bgcolor', '#ffeedd')
    else:
        set_background('#ffffff')
        config.set('settings', 'bgcolor', '#ffffff')


with ui.header().classes(replace='row items-center') as header:
    with ui.row():
        ui.label('\u00a0')
        ui.label('LNxt').style('color: #FFFFFF; font-size: 150%; font-weight: 500')
        ui.label('\u00a0')
    with ui.tabs() as tabs:
        ui.tab('启动面板')
        ui.tab('产品库')
        ui.tab('启动器设置')

with ui.left_drawer().classes('bg-blue-200') as left_drawer:
    ui.label('活跃线程').style('color: #3288AE; font-size: 150%; font-weight: 500')
    ui.label('没有正在进行的任务。').style('color: #3288AE;')

with ui.page_sticky(position='bottom-right', x_offset=20, y_offset=20):
    ui.button(text='启动 '+game_name)

with ui.tab_panels(tabs, value='启动面板').classes('w-full'):
    with ui.tab_panel('启动面板'):
        ui.label('启动面板').style('color: #6E93D6; font-size: 200%; font-weight: 300')
    with ui.tab_panel('产品库'):
        with ui.row():
            with ui.card():
                ui.image('static/game_icon/MCSA.png')
                with ui.card_section():
                    ui.label('MCSA Enchanted')
            with ui.card():
                ui.image('static/game_icon/genshin.png')
                with ui.card_section():
                    ui.label('原神')
            with ui.card():
                ui.image('static/game_icon/zzz.png')
                with ui.card_section():
                    ui.label('绝区零')
            with ui.card():
                ui.image('static/game_icon/star_rail.png')
                with ui.card_section():
                    ui.label('崩坏:星穹铁道')
            with ui.card():
                ui.image('static/game_icon/honkai3.png')
                with ui.card_section():
                    ui.label('崩坏3')
    with ui.tab_panel('启动器设置'):
        with ui.card():
            ui.label('LauncherNext').style('color: #6E93D6; font-size: 200%; font-weight: 300')
            with ui.column():
                ui.label('一个基于webUI和Python的轻量级启动器。')
                ui.label('当前版本：'+__version__)
                ui.label('由 DarkstarXD 独立开发。')
                ui.separator()
                with ui.row():
                    ui.button('检查更新')
                    ui.button('许可与版权声明')
                    ui.button('在 Github 上查看此项目')
        ui.label('\u00a0')
        with ui.card():
            ui.label('主题设置').style('font-size: 150%; font-weight: 300')
            ui.label('前景色设置')
            fgcradio=ui.radio(['Defalt','Atlantic','Forest','Deep Ocean','Grey'],value='Defalt',on_change=set_fgc).props('inline')
            ui.label('背景色设置(Beta)')
            bgcradio=ui.radio(['Defalt','Orange'],value='Defalt',on_change=set_bgc).props('inline')

if os.path.exists('config.ini'):
    config.read('config.ini')
    forecolor = config.get('settings', 'forecolor')
    bgcolor = config.get('settings', 'bgcolor')
    ui.colors(primary=forecolor)
    set_background(bgcolor)
def on_exit():
    config.set('settings', 'forecolor', forecolor)
    config.set('settings', 'bgcolor', bgcolor)
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
app.on_exit = on_exit

ui.run(native=True, window_size=(1280,720), title='LauncherNext 启动器')
