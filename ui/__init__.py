import configparser
import copy
import logging
import os
import os.path
import webbrowser

from nicegui import app, ui
from nicegui.events import ValueChangeEventArguments

import launchers.mc_java
import utils.fastgithub_launcher as fg_launcher

from .installers import *

__version__='0.0.3'
forecolor='#FFFFFF'
bgcolor='#ffffff'
firstlaunch=False
cwd=os.getcwd()
app.native.window_args['resizable'] = False
app.native.start_args['debug'] = False
app.add_static_files('/static',os.path.join(cwd, "static"))  # Use os.path.join instead of "+"
config = configparser.ConfigParser()
logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class LogElementHandler(logging.Handler):
    def __init__(self, element: ui.log, level: int = logging.NOTSET) -> None:
        self.element = element
        super().__init__(level)

    def emit(self, record: logging.LogRecord) -> None:
        try:
            msg = self.format(record)
            self.element.push(msg)
        except Exception:
            self.handleError(record)

class GameCard(ui.card):
    def set_game_name(self, game):
        self._game_name = copy.deepcopy(game)
        self.on("click", lambda: gamelabel.set_text('选定项目: '+self._game_name))

def set_background(color: str) -> None:
    ui.query('body').style(f'background-color: {color}')

def set_fgc(event: ValueChangeEventArguments):
    name = type(event.sender).__name__
    if f'{name}: {event.value}' == 'Radio: Grey':
        ui.colors(primary='#555')
        forecolor='#555'
        config.set('settings', 'forecolor', '#555')
        with open('lnxt.ini', 'w') as configfile:config.write(configfile)
    elif f'{name}: {event.value}' == 'Radio: Atlantic':
        ui.colors(primary='#3288AE')
        forecolor='#3288AE'
        config.set('settings', 'forecolor', '#3288AE')
        with open('lnxt.ini', 'w') as configfile:config.write(configfile)
    elif f'{name}: {event.value}' == 'Radio: Forest':
        ui.colors(primary='#346C48')
        forecolor='#346C48'
        config.set('settings', 'forecolor', '#346C48')
        with open('lnxt.ini', 'w') as configfile:config.write(configfile)
    elif f'{name}: {event.value}' == 'Radio: Deep Ocean':
        ui.colors(primary='#072A69')
        forecolor='#072A69'
        config.set('settings', 'forecolor', '#072A69')
        with open('lnxt.ini', 'w') as configfile:config.write(configfile)
    else:
        ui.colors()
        config.set('settings', 'forecolor', '#5898D4')
        with open('lnxt.ini', 'w') as configfile:config.write(configfile)

def set_bgc(event: ValueChangeEventArguments):
    name = type(event.sender).__name__
    if f'{name}: {event.value}' == 'Radio: Orange':
        set_background('#ffeedd')
        config.set('settings', 'bgcolor', '#ffeedd')
        with open('lnxt.ini', 'w') as configfile:config.write(configfile)
    else:
        set_background('#ffffff')
        config.set('settings', 'bgcolor', '#ffffff')
        with open('lnxt.ini', 'w') as configfile:config.write(configfile)

def select_game(game):
    logger.info('Game selected: '+game)
    game_selected=game
    config.set('games', 'game_selected', game)
    with open('lnxt.ini', 'w') as configfile:config.write(configfile)
    launch_bt.props(remove='disabled')
    launch_bt.set_text('启动 '+game)
    gamelabel.set_text('选定项目: '+game_selected)

if os.path.exists('lnxt.ini'):
    config.read('lnxt.ini')
    launchtime = int(config.get('general', 'launch'))
    forecolor = config.get('settings', 'forecolor')
    bgcolor = config.get('settings', 'bgcolor')
    if forecolor == '#555':
        fgc_name='Grey'
    elif forecolor == '#3288AE':
        fgc_name='Atlantic'
    elif forecolor == '#346C48':
        fgc_name='Forest'
    elif forecolor == '#072A69':
        fgc_name='Deep Ocean'
    else:
        fgc_name='Defalt'
    if bgcolor == '#ffeedd':
        bgc_name='Orange'
    else:
        bgc_name='Defalt'
    ui.colors(primary=forecolor)
    set_background(bgcolor)
    game_list= config.get('games', 'game_list').split(',')
    game_local= config.get('games', 'game_local').split(',')
    game_selected=config.get('games', 'game_selected')
    logger.info('Configuration file loaded.')
else:
    open('lnxt.ini', 'w').close()
    config['general'] = {
    "launch": '1'
    }
    config['settings'] = {
    "forecolor": '#5898D4',
    "bgcolor": "#ffffff"
    }
    config['games'] = {
    "game_list": 'MCSA Enchanted,MCSA Enchanted Light,MCSA Multiverse,Minecraft Java,Minecraft Bedrock,Genshin Impact',
    "game_local": 'None',
    "game_selected": 'None'
    }
    with open('lnxt.ini', 'w') as configfile:
        config.write(configfile)
    logger.info('New configuration file created.')
    fgc_name='Defalt'
    bgc_name='Defalt'
    game_list='MCSA Enchanted,MCSA Enchanted Light,MCSA Multiverse,Minecraft Java,Minecraft Bedrock,Genshin Impact'.split(',')
    game_local='None'
    game_selected='None'
    launchtime = 1

if game_selected == 'None':
    game_selected = '未指定'

if launchtime < 2:
    logger.info('First launch detected.')
    with ui.dialog() as dialog, ui.card():
        ui.label('欢迎!').style('color: #6E93D6; font-size: 200%; font-weight: 300')
        ui.label('LauncherNext 是一个基于 webUI 设计的轻量级应用启动器。')
        ui.label('只需要简单几步，我们就可以完成对启动器的初始化设置。')
        ui.label('单击"下一步"以继续。')
        with ui.row():
            ui.button('下一步')
            ui.button('跳过', on_click=dialog.close)
    dialog.open()
if launchtime % 2 == 0:
    fg_launcher.launch()
launchtime = launchtime + 1
config['general'] = {
    "launch": launchtime
    }
with open('lnxt.ini', 'w') as configfile:
    config.write(configfile)

logger.info('Initalization Complete.')

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
    log = ui.log(max_lines=10).classes('w-full')
    handler = LogElementHandler(log)
    logger.addHandler(handler)

with ui.page_sticky(position='bottom-right', x_offset=20, y_offset=20):
    if game_selected == '未指定':
        launch_bt=ui.button('未指定启动项').props('disabled')
    else:
        launch_bt=ui.button(text='启动 '+game_selected)

with ui.tab_panels(tabs, value='启动面板').classes('w-full'):
    with ui.tab_panel('启动面板'):
        ui.label('启动面板').style('color: #6E93D6; font-size: 200%; font-weight: 300')
        gamelabel=ui.label('选定项目: '+game_selected)
    with ui.tab_panel('产品库'):
        with ui.column():
            for game in game_list:
                with GameCard() as card:
                    card.set_game_name(game)
                    with ui.row():
                        onclick = lambda: gamelabel.set_text('选定项目: '+game)
                        l = ui.label(game)

    with ui.tab_panel('启动器设置'):
        ui.label('这里的设置会自动保存。')
        with ui.card():
            ui.label('LauncherNext').style('color: #6E93D6; font-size: 200%; font-weight: 300')
            with ui.column():
                ui.label('一个基于webUI和Python的轻量级启动器。')
                ui.label('当前版本：'+__version__)
                ui.label('由 DarkstarXD 和 Allen546 联合开发。')
                ui.separator()
                with ui.row():
                    ui.button('检查更新').props('disabled')
                    ui.button('许可与版权声明',on_click=lambda:webbrowser.open('https://github.com/ccjjfdyqlhy/LauncherNext/blob/main/LICENSE'))
                    ui.button('在 Github 上查看此项目',on_click=lambda:webbrowser.open('https://github.com/ccjjfdyqlhy/LauncherNext'))
        with ui.card():
            with ui.column():
                ui.label('账户').style('font-size: 150%; font-weight: 300')
                username = ui.input('用户名')
                password = ui.input('密码', password=True, password_toggle_button=True)
                ui.button('登录')
        with ui.card():
            ui.label('主题设置').style('font-size: 150%; font-weight: 300')
            ui.label('前景色设置')
            fgcradio=ui.radio(['Defalt','Atlantic','Forest','Deep Ocean','Grey'],value=fgc_name,on_change=set_fgc).props('inline')
            ui.label('背景色设置(Beta)')
            bgcradio=ui.radio(['Defalt','Orange'],value=bgc_name,on_change=set_bgc).props('inline')
        with ui.card():
            ui.label('实例设置').style('font-size: 150%; font-weight: 300')
            with ui.row():
                lb = ui.label("安装Java")
                lb.style('font-size:150%; margin-top:13px;')
                javaverin=ui.select(list(launchers.mc_java.JavaManager.versions.keys()), value="17")
                javaverin.style("margin-bottom: 15px;padding-right: 10px")
                ui.button('下载Java',on_click=get_java_installer_onclick(javaverin)).style("margin-top: 10px;")

app.on_disconnect(app.shutdown)
ui.context.client.on_disconnect(lambda: logger.removeHandler(handler))

def main():
    ui.run(native=True, window_size=(1280,720), title='LauncherNext 启动器', reload=False)