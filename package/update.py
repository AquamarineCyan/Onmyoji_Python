# update.py
"""
更新日志
"""

from mysignal import global_ms as ms


def update_record():
    """更新日志"""
    update = {
    '1.6.3':
'''新增
环境文件requirements.txt
清理日志
限时活动
组队日轮副本

优化
召唤功能结束
截图功能
窗口信息显示方式
个人突破刷新逻辑

修复
因呱太入侵导致的图像错位
更换pathlib库引发的错误''',
    '1.6.2':
'''新增 业原火副本
新增 道馆突破观战功能
优化 功能列表顺序
修复 初次使用无日志时写入报错''',

    '1.6.1':
'''新增 UI界面色彩显示
新增 组队永生之海副本
新增 更新窗口信息功能
优化 代码冗余''',

    '1.6':
'''新增 UI界面
新增 日志模块
优化 代码逻辑''',

    '1.5':
'''新增 百鬼夜行功能
新增 道馆突破功能
新增 御灵功能
新增 绘卷查分功能
新增 错误和异常判断处理
新增 部分注释说明
新增 输出界面的色彩直观表达
优化 功能选择的输入稳定性
优化 普通召唤的判定逻辑
优化 个人结界与寮结界的相互识别跳转
优化 文件处理的逻辑
适配 键入回车默认选择
适配 新版结算速度''',

    '1.4':
'''新增 个人结界功能
优化 图片素材存储''',

    '1.3':
'''新增 寮突破功能
优化 函数调用
优化 御魂组队情况''',

    '1.2':
'''新增 组队御魂功能''',

    '1.1':
'''新增 普通召唤功能'''
    }

    for key, value in update.items():
        ms.updateui_textBrowser_update.emit(str(key))
        ms.updateui_textBrowser_update.emit(str(value))
        ms.updateui_textBrowser_update.emit('')
