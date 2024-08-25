import subprocess
import time
import threading
import configparser
import copy
import psutil
import logging
import os
import os.path
import webbrowser
import daemon
import sys

from nicegui import app, ui
from nicegui.events import ValueChangeEventArguments

import launchers.mc_java
import utils.fastgithub as fg_launcher

from .installers import *

__version__ = '0.0.5'
forecolor = '#FFFFFF'
bgcolor = '#ffffff'
firstlaunch = False
selected_game = None
cwd = os.getcwd()
app.native.window_args['resizable'] = False
app.native.start_args['debug'] = False
app.add_static_files('/static', os.path.join(cwd, "static"))
config = configparser.ConfigParser()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
show_notifications = True

def show_notification(message, type="success"):
    if show_notifications:
        ui.notify(message, type=type, position='bottom-right')

class LogElementHandler(logging.Handler):
    def __init__(self, element: ui.log, level: int = logging.NOTSET) -> None:
        self.element = element
        super().__init__(level)

    def emit(self, record: logging.LogRecord) -> None:
        try:
            msg = self.format(record)
            self.element.push(msg)

            # 根据日志级别显示不同类型的通知
            if record.levelno == logging.INFO:
                    show_notification(msg)
            elif record.levelno == logging.WARNING:
                show_notification(msg, "warning")
            elif record.levelno >= logging.ERROR:
                show_notification(msg, "negative")

        except Exception:
            self.handleError(record)


class GameCard(ui.card):
    def set_game_name(self, game):
        self._game_name = copy.deepcopy(game)
        self.on("click", lambda: select_game(self._game_name))


def ok(string):
    show_notification(string,type='positive')


def submit_instance():
    webbrowser.open('https://github.com/ccjjfdyqlhy/LauncherNext/labels/%E5%AE%9E%E4%BE%8B%E6%8A%95%E7%A8%BF')


def set_background(color: str) -> None:
    ui.query('body').style(f'background-color: {color}')


def set_fgc(event: ValueChangeEventArguments):
    name = type(event.sender).__name__
    if f'{name}: {event.value}' == 'Radio: Grey':
        ui.colors(primary='#555')
        forecolor = '#555'
        config.set('settings', 'forecolor', '#555')
        with open('lnxt.ini', 'w', encoding='utf-8-sig') as configfile: config.write(configfile)
    elif f'{name}: {event.value}' == 'Radio: Atlantic':
        ui.colors(primary='#3288AE')
        forecolor = '#3288AE'
        config.set('settings', 'forecolor', '#3288AE')
        with open('lnxt.ini', 'w', encoding='utf-8-sig') as configfile: config.write(configfile)
    elif f'{name}: {event.value}' == 'Radio: Forest':
        ui.colors(primary='#346C48')
        forecolor = '#346C48'
        config.set('settings', 'forecolor', '#346C48')
        with open('lnxt.ini', 'w', encoding='utf-8-sig') as configfile: config.write(configfile)
    elif f'{name}: {event.value}' == 'Radio: Deep Ocean':
        ui.colors(primary='#072A69')
        forecolor = '#072A69'
        config.set('settings', 'forecolor', '#072A69')
        with open('lnxt.ini', 'w', encoding='utf-8-sig') as configfile: config.write(configfile)
    else:
        ui.colors()
        config.set('settings', 'forecolor', '#5898D4')
        with open('lnxt.ini', 'w', encoding='utf-8-sig') as configfile: config.write(configfile)


def set_bgc(event: ValueChangeEventArguments):
    name = type(event.sender).__name__
    if f'{name}: {event.value}' == 'Radio: Orange':
        set_background('#ffeedd')
        config.set('settings', 'bgcolor', '#ffeedd')
        with open('lnxt.ini', 'w', encoding='utf-8-sig') as configfile: config.write(configfile)
    else:
        set_background('#ffffff')
        config.set('settings', 'bgcolor', '#ffffff')
        with open('lnxt.ini', 'w', encoding='utf-8-sig') as configfile: config.write(configfile)


def set_pyver():
    pyver = pyverin.value()


def select_game(game):
    global selected_game 
    logger.info(f'已选择实例: {game}')
    selected_game = game
    if os.path.exists(cwd+'\\apps\\'+game+'\\'+game+'.lnxt'):
        config.read(cwd+'\\apps\\'+game+'\\'+game+'.lnxt', encoding='utf-8-sig')
        apptype = config.get('app', 'class')
        logger.info(f'已获取 {game} 的应用程序类型: {apptype}')
    else:
        logger.warning('在默认实例文件夹中找不到文件; 正在使用应用程序文件夹')
        try:
            if os.path.exists(cwd+'\\apps\\'+game+'.lnxt'):
                config.read(cwd+'\\apps\\'+game+'.lnxt', encoding='utf-8-sig')
                apptype = config.get('app', 'class')
                logger.info(f'已获取 {game} 的应用程序类型: {apptype}')
            else:
                logger.error(f'找不到文件: {cwd}\\apps\\{game}.lnxt')
                apptype = 'unknown'
        except Exception as e:
            logger.error(f'读取配置文件时出错: {str(e)}')
            apptype = 'unknown'
    config.read('lnxt.ini', encoding='utf-8-sig')
    config.set('apps', 'game_selected', game)
    config.set('apps', 'type_selected', apptype)
    with open('lnxt.ini', 'w', encoding='utf-8-sig') as configfile: config.write(configfile)
    update_launch_button()
    gamelabel.set_text('选定项目: ' + selected_game)
    if apptype == 'exe':
        apptypedsp = 'Win32 可执行程序入口'
    elif apptype == 'jar':
        apptypedsp = '打包的 Java 应用程序'
    elif apptype == 'minecraft':
        apptypedsp = 'Minecraft 实例'
    elif apptype == 'py':
        apptypedsp = 'Python 实例'
    elif apptype == 'unknown':
        apptypedsp = '未知'
    else:
        apptypedsp = '尚未支持的类型 '+apptype
    typelabel.set_text('项目类型: ' + apptypedsp)


def update_launch_button():
    global selected_game
    if selected_game is None:
        launch_bt.props(remove='disabled')
        launch_bt.set_text('未指定启动项')
    else:
        launch_bt.props(remove='disabled')
        launch_bt.set_text('启动 ' + selected_game)


def launch_config(instance):
    if selected_game is None: 
        logger.error('未选择任何实例')
        return
    if os.path.exists(cwd + '\\apps\\' + instance + '.lnxt'):
            logger.info(f'正在读取 {instance}.lnxt')
            config.read(cwd + '\\apps\\' + instance + '.lnxt')
    else:
            logger.error('找不到 LauncherNext 应用程序配置文件。')
            logger.error('启动已终止。')
            return
    runtime = config.get('app', 'runtime')
    vcwd = config.get('app', 'vcwd')
    configexec = config.get('config', 'exec')
    try:
        daemon.exec(runtime+' '+configexec, vcwd)
        logger.info('已启动实例内置配置器。')
        ok('已启动实例内置配置器。')
    except FileNotFoundError:
        logger.error('找不到实例配置文件。')
        logger.error('启动已终止。')

def xlaunch(instance):
    if instance == None: logger.error('未选择任何实例');return
    if not os.path.exists(cwd + '\\apps\\' + instance):
        logger.warning('找不到实例文件夹，正从配置文件启动')
        isappfolder = False
    else:
        isappfolder = True
    logger.info(f'准备启动: {instance}')
    if isappfolder:
        if os.path.exists(cwd + '\\apps\\' + instance + '\\' + instance + '.lnxt'):
            logger.info(f'正在读取 {instance}.lnxt')
            config.read(cwd + '\\apps\\' + instance + '\\' + instance + '.lnxt')
        else:
            logger.error('找不到 LauncherNext 应用程序配置文件。')
            logger.error('启动已终止。')
            return
    else:
        if os.path.exists(cwd + '\\apps\\' + instance + '.lnxt'):
            logger.info(f'正在读取 {instance}.lnxt')
            config.read(cwd + '\\apps\\' + instance + '.lnxt')
        else:
            logger.error('找不到 LauncherNext 应用程序配置文件。')
            logger.error('启动已终止。')
            return
    appclass = config.get('app', 'class')
    if appclass == 'exe':
        appexec = config.get('app', 'exec')
    elif appclass == 'jar':
        appexec = 'java -jar ' + config.get('app', 'exec')
    elif appclass == 'minecraft':
        pass
        # TODO
    elif appclass == 'py':
        try:
            runtime = config.get('app', 'runtime')
            vcwd = config.get('app', 'vcwd')
            appexec = config.get('app', 'exec')
        except configparser.NoOptionError:
            logger.error('LauncherNext 应用程序配置文件缺少必需的选项。')
            return
        if runtime == '': runtime = 'python'
    elif appclass == 'unknown':
        logger.error('未知的应用程序类别。')
        logger.error('启动已终止。')
        return
    else:
        logger.error('尚不支持的应用程序类别。')
        logger.error('启动已终止。')
        return
    logger.info(f'正在启动 {instance}')
    try:
        if appclass == 'py':
            daemon.exec(runtime+' '+appexec, vcwd)
        else:
            daemon.exec(appexec)
        logger.info(f'{instance} 启动成功。')
        ok('启动完成。')
    except FileNotFoundError:
        logger.error('配置文件中实例可执行文件路径无效。')
        logger.error('启动已终止。')
        return

# --- 函数用于切换是否显示通知 ---
def toggle_notifications(event: ValueChangeEventArguments):
    global show_notifications
    show_notifications = event.value
    config.set('settings', 'show_notifications', str(show_notifications))
    with open('lnxt.ini', 'w', encoding='utf-8-sig') as configfile:
        config.write(configfile)


memory = psutil.virtual_memory()
mtotal = int((memory.total / 1024 ** 2) // 1024)
mused = int((memory.used / 1024 ** 2) // 1024)
mfree = mtotal - mused

if os.path.exists('lnxt.ini'):
    game_local,invalid_instances = daemon.scan_instances()
    if sys.platform == 'win32':
        installed_apps = ''
        #installed_apps = daemon.get_installed_list_win()
    else:
        installed_apps = ''
    config.read('lnxt.ini', encoding='utf-8-sig')
    config.set('apps', 'installed', installed_apps)
    config.set('apps', 'game_local', game_local)
    with open('lnxt.ini', 'w', encoding='utf-8-sig') as configfile:
        config.write(configfile)
    config.read('lnxt.ini', encoding='utf-8-sig')
    launchtime = int(config.get('general', 'launch'))
    forecolor = config.get('settings', 'forecolor')
    bgcolor = config.get('settings', 'bgcolor')

    # 读取是否显示通知的设置
    show_notifications = config.getboolean('settings', 'show_notifications', fallback=True)

    if forecolor == '#555':
        fgc_name = 'Grey'
    elif forecolor == '#3288AE':
        fgc_name = 'Atlantic'
    elif forecolor == '#346C48':
        fgc_name = 'Forest'
    elif forecolor == '#072A69':
        fgc_name = 'Deep Ocean'
    else:
        fgc_name = 'Defalt'
    if bgcolor == '#ffeedd':
        bgc_name = 'Orange'
    else:
        bgc_name = 'Defalt'
    ui.colors(primary=forecolor)
    set_background(bgcolor)
    installed_apps = config.get('apps', 'installed').split(',')
    game_list = config.get('apps', 'game_list').split(',')
    game_local = config.get('apps', 'game_local').split(',')

    # 读取上次选定的实例
    game_selected = config.get('apps', 'game_selected')
    type_selected = config.get('apps', 'type_selected')
    logger.info('已加载配置文件。')
else:
    if sys.platform == 'win32':
        installed_apps = ''
        #installed_apps = daemon.get_installed_list_win()
    else:
        installed_apps = ''
    game_local, invalid_instances = daemon.scan_instances()
    open('lnxt.ini', 'w', encoding='utf-8-sig').close()
    config['general'] = {
        "launch": '1'
    }
    config['settings'] = {
        "forecolor": '#5898D4',
        "bgcolor": "#ffffff",
        # 默认显示通知
        "show_notifications": "True"
    }
    config['apps'] = {
        "installed": installed_apps,
        "game_list": 'DSN,MCSA Enchanted,MCSA Enchanted Light,MCSA Multiverse,Minecraft Java,Minecraft Bedrock,Genshin Impact',
        "game_local": game_local,
        "game_selected": 'None',
        "type_selected": 'None'
    }
    with open('lnxt.ini', 'w', encoding='utf-8-sig') as configfile:
        config.write(configfile)
    logger.info('已创建新的配置文件。')
    fgc_name = 'Defalt'
    bgc_name = 'Defalt'
    installed_apps = installed_apps.split(',')
    game_list = 'DSN,MCSA Enchanted,MCSA Enchanted Light,MCSA Multiverse,Minecraft Java,Minecraft Bedrock,Genshin Impact'.split(',')
    game_local = game_local.split(',')
    game_selected = 'None'
    type_selected = 'None'
    launchtime = 1

# --- 初始化选定项 ---
if game_selected != 'None' and game_selected in game_list:
    selected_game = game_selected
    if type_selected == 'exe':
        apptypedsp = 'Win32 可执行程序入口'
    elif type_selected == 'jar':
        apptypedsp = '打包的 Java 应用程序'
    elif type_selected == 'minecraft':
        apptypedsp = 'Minecraft 实例'
    elif type_selected == 'py':
        apptypedsp = 'Python 实例'
    elif type_selected == 'unknown':
        apptypedsp = '未知类型'
    else:
        apptypedsp = '尚未支持的类型 '+type_selected
    selected_game_type = apptypedsp
else:
    selected_game = None 
    selected_game_type = None

if launchtime < 2:
    logger.info('检测到首次启动。')
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
    print('\nLauncherNext Interface ' + __version__ + '\n')
    if not daemon.is_alive('fastgithub.exe'):
        fg_launcher.launch()
    else:
        logger.info('FastGithub 已在运行。')
launchtime = launchtime + 1
config['general'] = {
    "launch": launchtime
}
with open('lnxt.ini', 'w', encoding='utf-8-sig') as configfile:
    config.write(configfile)
logger.info('初始化完成。')
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
    ui.linear_progress()
with ui.tab_panels(tabs, value='启动面板').classes('w-full'):
    with ui.tab_panel('启动面板'):
        ui.label('启动面板').style('color: #6E93D6; font-size: 200%; font-weight: 300')
        with ui.column():
            with ui.card():
                gamelabel = ui.label('选定项目: ' + str(selected_game or '未指定'))
                typelabel = ui.label('项目类型: ' + str(selected_game_type or '未指定'))
                ui.button('配置',on_click=lambda: launch_config(selected_game))
            with ui.card():
                ui.label('LauncherNext本地支持指南').style('font-size: 150%; font-weight: 300')
                ui.label('1、弄清楚你的项目是exe、jar、minecraft还是python项目。')
                ui.label('2、用Python为你的项目编写一个可交互的独立配置程序（之后会逐步支持更多语言），保存到你的实例文件夹下。')
                ui.label('3、书写<实例名>.lnxt文件。格式可以参考./examples/example.lnxt。')
                ui.label('4、你可以选择把lnxt文件直接放在启动器的apps文件夹下，也可以把lnxt文件放在你的实例文件夹下复制进启动器的apps文件夹。')
                ui.label('5、重新启动启动器。我们会自动适配你的实例，并将其添加到本地产品库。')
        with ui.card():
            ui.label('发布到LauncherNext').style('font-size: 150%; font-weight: 300')
            ui.label('想让你的项目被更多人发现吗？你可以选择发布到LauncherNext。这类产品会随更新推送到每位使用者的启动器中。')
            ui.label('1、确保你的项目支持多平台运行且开源。把你项目中可以从互联网下载的文件清单保存到你的实例文件夹下的required_files.list中，之后删除这些文件。确保现在你的实例文件夹中只有你原创或未公开的文件。')
            ui.label('2、按本地支持的格式书写<实例名>.lnxt文件后将其放进实例文件夹中。')
            ui.label('3、打包你的实例文件夹。将其上传到其GitHub仓库的Releases页面，并确保仓库是公开的。')
            ui.label('4、在 [产品库] 中转到投稿实例，点击 [新投稿] ，并填写相关信息。')
            ui.label('5、等待审核通过。')
            ui.label('6、审核通过后，你的实例将会出现在产品库的可用实例列表中。')
            ui.label('7、如果你更新了你的实例，只需更改lnxt文件和Release中的版本号，将其上传到其GitHub仓库。LauncherNext将自动将更新推送给每位使用者。')

    with ui.tab_panel('产品库'):
        with ui.column():
            with ui.row():
                with ui.column():
                    with ui.card():
                        ui.label(f'可用实例 ({len(game_list)})').style('font-size: 150%; font-weight: 300')
                        ui.label('下面列出了已经适配于LauncherNext且公开的的程序实例清单。')
                        ui.label('单击你要使用的项目，然后转到 [启动面板] 。')
                        for game in game_list:
                            with GameCard() as card:
                                card.set_game_name(game)
                                with ui.row():
                                    onclick = lambda game=game: gamelabel.set_text('选定项目: ' + game)
                                    ui.label(game)
                    with ui.card() as card:
                        ui.label(f'系统应用 ({len(installed_apps)})').style('font-size: 150%; font-weight: 300')
                        ui.label('这里呈现了LauncherNext扫描的你电脑上已经安装的应用程序。')
                        ui.label('由于其数量较多，我们不建议通过该列表启动它们。')
                        ui.label('系统运行时与驱动已剔除。')
                        systemappschk = ui.checkbox('查看系统应用', value=False)
                        for oapp in installed_apps:
                            with ui.card().bind_visibility_from(systemappschk, 'value'):
                                ui.label(oapp)
                with ui.column():
                    with ui.card():
                        ui.label('投稿实例').style('font-size: 150%; font-weight: 300')
                        ui.label('如果你的实例足够有应用价值且想要分享给其他人，')
                        ui.label('你可以在这里把自己的实例提交给LauncherNext的开发者。')
                        ui.label('请确保你的实例已经经过全平台测试并且已经按照启动面板上的要')
                        ui.label('求配置好。')
                        ui.button('新投稿', on_click=lambda: submit_instance())
                    with ui.card() as card:
                        ui.label(f'已安装 ({len(game_local)})').style('font-size: 150%; font-weight: 300')
                        ui.label('这是LauncherNext扫描到的安装在默认文件夹下的可用实例。')
                        ui.label('已经排除了启动器运行必须的依赖项和 '+str(invalid_instances)+' 个无法使用的损坏实例。')
                        if len(game_local) == 0:
                            with ui.card():
                                ui.label('你还没有安装任何实例 ~(￣▽￣)~*')
                        for game in game_local:
                            with ui.card():
                                ui.label(game)
    with ui.tab_panel('启动器设置'):
        ui.label('这里的设置会自动保存。')
        with ui.row():
            with ui.card():
                ui.label('LauncherNext').style('color: #6E93D6; font-size: 200%; font-weight: 300')
                with ui.column():
                    ui.label('基于webUI和Python的轻量级启动器，开源软件的自由流通平台。')
                    ui.label('版本 ' + __version__)
                    ui.label('由 DarkstarXD 和 Allen546 联合开发。')
                    ui.separator()
                    with ui.row():
                        ui.button('检查更新').props('disabled')
                        ui.button('许可与版权声明', on_click=lambda: webbrowser.open(
                            'https://github.com/ccjjfdyqlhy/LauncherNext/blob/main/LICENSE'))
                        ui.button('在 Github 上查看此项目',
                                  on_click=lambda: webbrowser.open('https://github.com/ccjjfdyqlhy/LauncherNext'))
            with ui.card():
                ui.label('登录').style('font-size: 150%; font-weight: 300')
                ui.label('使用GitHub账号登录到LauncherNext。')
                ui.chip('OAuth Login with GitHub', icon='launch', color='indigo-3')
        with ui.card():
            ui.label('个性化').style('font-size: 150%; font-weight: 300')
            ui.label('前景色设置')
            fgcradio = ui.radio(['Defalt', 'Atlantic', 'Forest', 'Deep Ocean', 'Grey'], value=fgc_name,
                                on_change=set_fgc).props('inline')
            ui.label('边框颜色设置')
            bgcradio = ui.radio(['Defalt', 'Orange'], value=bgc_name, on_change=set_bgc).props('inline')

        # --- 添加通知开关 ---
        with ui.card():
            ui.label('启动器设置').style('font-size: 150%; font-weight: 300')
            notification_switch = ui.switch('启用事件显示队列', value=show_notifications, on_change=toggle_notifications)

        with ui.card():
            ui.label('实例设置').style('font-size: 150%; font-weight: 300')
            ui.label('Python类').style('font-size: 125%')
            with ui.column():
                with ui.row():
                    pyverin = ui.input("默认Python运行时:")
                    ui.button('应用')
            ui.label('Minecraft类').style('font-size: 125%')
            with ui.row():
                ui.label("安装Java: ").style('margin-top:13px;')
                javaverin = ui.select(list(launchers.mc_java.JavaManager.versions.keys()), value="17").style(
                    "margin-bottom: 15px;padding-right: 10px")
                ui.button('下载Java', on_click=get_java_installer_onclick(javaverin)).style("margin-top: 10px;")
                ui.label("Java策略: ").style('margin-top:13px;')
                javarole = ui.select(['自动根据Minecraft版本选择Java'] + list(JavaManager.versions.keys()),
                                      value="自动根据Minecraft版本选择Java").style(
                    "margin-bottom: 15px;padding-right: 10px")
            with ui.row():
                ui.label("JVM内存分配: " + '总内存 ' + str(mtotal) + ' GB').style('margin-top:13px;')
                slider = ui.slider(min=1, max=mtotal, step=0.5, value=8)
                ui.number().bind_value(slider)
                ui.label('GB')

with ui.page_sticky(position='bottom-right', x_offset=20, y_offset=20):
    launch_bt = ui.button(
        on_click=lambda: xlaunch(selected_game)
    )
    update_launch_button() 
ui.context.client.on_disconnect(lambda: logger.removeHandler(handler))
def main():
    ui.run(port=8000, native=True, window_size=(1280, 720), title='LauncherNext Interface', reload=False)