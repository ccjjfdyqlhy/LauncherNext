import os
import configparser
from nicegui import ui,app
from nicegui.events import ValueChangeEventArguments

__version__='0.0.3'
forecolor='#FFFFFF'
bgcolor='#ffffff'
cwd=os.getcwd()
app.native.window_args['resizable'] = False
app.native.start_args['debug'] = False
app.add_static_files('/static',cwd+'\\static')
config = configparser.ConfigParser()

def set_background(color: str) -> None:
    ui.query('body').style(f'background-color: {color}')

def set_fgc(event: ValueChangeEventArguments):
    name = type(event.sender).__name__
    if f'{name}: {event.value}' == 'Radio: Grey':
        ui.colors(primary='#555')
        forecolor='#555'
        config.set('settings', 'forecolor', '#555')
        with open('config.ini', 'w') as configfile:config.write(configfile)
    elif f'{name}: {event.value}' == 'Radio: Atlantic':
        ui.colors(primary='#3288AE')
        forecolor='#3288AE'
        config.set('settings', 'forecolor', '#3288AE')
        with open('config.ini', 'w') as configfile:config.write(configfile)
    elif f'{name}: {event.value}' == 'Radio: Forest':
        ui.colors(primary='#346C48')
        forecolor='#346C48'
        config.set('settings', 'forecolor', '#346C48')
        with open('config.ini', 'w') as configfile:config.write(configfile)
    elif f'{name}: {event.value}' == 'Radio: Deep Ocean':
        ui.colors(primary='#072A69')
        forecolor='#072A69'
        config.set('settings', 'forecolor', '#072A69')
        with open('config.ini', 'w') as configfile:config.write(configfile)
    else:
        ui.colors()
        config.set('settings', 'forecolor', '#5898D4')
        with open('config.ini', 'w') as configfile:config.write(configfile)

def set_bgc(event: ValueChangeEventArguments):
    name = type(event.sender).__name__
    if f'{name}: {event.value}' == 'Radio: Orange':
        set_background('#ffeedd')
        config.set('settings', 'bgcolor', '#ffeedd')
        with open('config.ini', 'w') as configfile:config.write(configfile)
    else:
        set_background('#ffffff')
        config.set('settings', 'bgcolor', '#ffffff')
        with open('config.ini', 'w') as configfile:config.write(configfile)

def select_game(game):
    print('[INFO] Game selected: '+game)
    game_selected=game
    config.set('games', 'game_selected', game)
    with open('config.ini', 'w') as configfile:config.write(configfile)
    launch_bt.props(remove='disabled')
    launch_bt.set_text('启动 '+game)
    gamelabel.set_text('选定项目: '+game_selected)

if os.path.exists('config.ini'):
    config.read('config.ini')
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
    print('[CONF] Configuration loaded.')
else:
    open('config.ini', 'w').close()
    config['settings'] = {
    "forecolor": '#5898D4',
    "bgcolor": "#ffffff"
    }
    config['games'] = {
    "game_list": 'MCSA Enchanted,MCSA Enchanted Light,MCSA Multiverse,Minecraft Java,Minecraft Bedrock,Genshin Impact',
    "game_local": 'None',
    "game_selected": 'None'
    }
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
    print('[CONF] New configuration file created.')
    fgc_name='Defalt'
    bgc_name='Defalt'
    game_list='MCSA Enchanted,MCSA Enchanted Light,MCSA Multiverse,Minecraft Java,Minecraft Bedrock,Genshin Impact'.split(',')
    game_local='None'
    game_selected='None'

if game_selected == 'None':
    game_selected = '未指定'

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
                with ui.card():
                    with ui.row():
                        ui.label(game)
    with ui.tab_panel('启动器设置'):
        ui.label('这里的设置会自动保存。')
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
        with ui.card():
            with ui.column():
                ui.label('账户').style('font-size: 150%; font-weight: 300')
                ui.input('用户名')
                ui.input('密码')
                ui.button('登录')
        with ui.card():
            ui.label('主题设置').style('font-size: 150%; font-weight: 300')
            ui.label('前景色设置')
            fgcradio=ui.radio(['Defalt','Atlantic','Forest','Deep Ocean','Grey'],value=fgc_name,on_change=set_fgc).props('inline')
            ui.label('背景色设置(Beta)')
            bgcradio=ui.radio(['Defalt','Orange'],value=bgc_name,on_change=set_bgc).props('inline')
        with ui.card():
            ui.label('实例设置').style('font-size: 150%; font-weight: 300')
            
app.on_disconnect(app.shutdown)
ui.run(native=True, window_size=(1280,720), title='LauncherNext 启动器', reload=False)