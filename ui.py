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

game_name = 'MCSA Enchanted Light'
config = configparser.ConfigParser()

def set_background(color: str) -> None:
    ui.query('body').style(f'background-color: {color}')
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
    print('[CONF] Configuration loaded.')
else:
    open('config.ini', 'w').close()
    config['settings'] = {
    "forecolor": '#5898D4',
    "bgcolor": "#ffffff"
    }
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
    print('[CONF] New configuration file created.')
    fgc_name='Defalt'
    bgc_name='Defalt'

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
        with ui.column():
            with ui.card():
                ui.label('MCSA Enchanted')
            with ui.card():
                ui.label('原神')
            with ui.card():
                ui.label('绝区零')
            with ui.card():
                ui.label('崩坏:星穹铁道')
            with ui.card():
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