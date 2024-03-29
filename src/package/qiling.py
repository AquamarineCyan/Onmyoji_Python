from ..utils.coordinate import RelativeCoor
from ..utils.decorator import log_function_call
from ..utils.event import event_thread
from ..utils.function import (
    check_click,
    check_finish_once,
    click,
    finish_random_left_right,
    get_coor_info,
    random_sleep
)
from ..utils.log import logger
from ..utils.mythread import WorkTimer
from .utils import Package


class QiLing(Package):
    """契灵"""
    scene_name = "契灵"
    resource_path = "qiling"
    resource_list: list = [
        "title",
        "start_tancha",
        "start_jieqi",
        "mingqizhaohuan",
        "queding",
    ]
    description = "次数为探查次数，选中“结契”按钮将在探查结束后自动挑战场上所有，地图最多支持刷出5只契灵，请提前在游戏内配置“结契设置”"

    @log_function_call
    def __init__(
        self,
        n: int = 0,
        _flag_tancha: bool = True,
        _flag_jieqi: bool = False,
        _stone_pokemon: str = None,
        _stone_numbers: int = 0,
    ) -> None:
        super().__init__(n)
        self._flag_tancha = _flag_tancha
        self._flag_jieqi = _flag_jieqi
        self._stone_pokemon = _stone_pokemon
        self._stone_numbers = _stone_numbers
        self._flag_finish: bool = False
        self._flag_timer_jieqi_finish: bool = True
        self._pokemon_address_count: int = 0
        self._stone_count: int = 0

    @log_function_call
    def fighting(self):
        _flag_first: bool = False
        while True:
            if event_thread.is_set():
                return
            if self._flag_finish:
                return
            if check_finish_once():
                _flag_first = True
                random_sleep(0.5, 0.8)
                finish_random_left_right()
            elif _flag_first:
                random_sleep(0.3, 0.5)
                return
            random_sleep(0.3, 0.5)

    @log_function_call
    def timer_start(self):
        coor = self.get_coor_info("start_tancha")
        if coor.is_effective:
            self._flag_finish = True

    @log_function_call
    def summon_pokemon(self):
        _pokemon_list = [
            RelativeCoor(160, 360),
            RelativeCoor(400, 360),
            RelativeCoor(650, 360),
            RelativeCoor(880, 360),
        ]
        if self._stone_pokemon == "镇墓兽":
            _pokemon_coor = _pokemon_list[3]
        for _ in range(self._stone_numbers - self._stone_count):
            check_click(f"{self.resource_path}/mingqizhaohuan")
            random_sleep()
            coor = self.get_coor_info("mingqizhaohuan")
            if coor.is_effective:
                logger.ui("场上最多5只契灵", "warn")
                return
            click(_pokemon_coor)
            random_sleep(0.4, 0.8)
            check_click(f"{self.resource_path}/queding")
            self._stone_count += 1
            logger.ui(f"已使用鸣契石数量: {self._stone_count}")
            random_sleep(3)

    @log_function_call
    def check_pokemon(self) -> bool:
        """判断5个契灵小图标的固定点位"""
        _pokemon_list = [
            RelativeCoor(220, 528),
            RelativeCoor(378, 485),
            RelativeCoor(635, 505),
            RelativeCoor(815, 484),
            RelativeCoor(935, 490),
        ]
        # 遍历5个固定点位
        for i in range(self._pokemon_address_count, 5):
            logger.info(f"_pokemon_address_count: {self._pokemon_address_count}")
            click(_pokemon_list[i])
            self._pokemon_address_count += 1
            random_sleep(2)
            coor = self.get_coor_info("start_jieqi")
            if coor.is_effective:
                return True
            else:
                continue
        return False

    @log_function_call
    def timer_jieqi_finish(self):
        coor = get_coor_info(f"{self.global_resource_path}/finish")
        if coor.is_zero:
            self._flag_timer_jieqi_finish = False

    @log_function_call
    def run_tancha(self):
        self.current_resource_list = [
            f"{self.resource_path}/title",
            f"{self.resource_path}/start_tancha",
        ]
        self.log_current_scene_list()

        while self.n < self.max:
            if event_thread.is_set():
                return
            scene, coor = self.check_scene_multiple_once()
            scene = self.scene_handle(scene)

            match scene:
                case "title":
                    logger.scene("契灵之境")
                case "start_tancha":
                    WorkTimer(5, self.timer_start).start()
                    click(coor)
                    random_sleep()
                    self.fighting()
                    self.done()
                    random_sleep(2, 4)
            if self._flag_finish:
                logger.ui("场上最多存在5只契灵，请及时清理")
                break

    @log_function_call
    def catch_pokemon(self):
        _n: int = 0
        self.current_resource_list = [
            f"{self.resource_path}/title",
            f"{self.resource_path}/start_jieqi",
        ]
        _flag_done_once: bool = False

        while _n <= 5:
            if event_thread.is_set():
                return
            scene, coor = self.check_scene_multiple_once()
            if scene is None:
                continue
            scene = self.scene_handle(scene)

            match scene:
                # 确保在探查界面点击契灵小图标
                case "title":
                    logger.scene("契灵之境")
                    if _flag_done_once:
                        _flag_done_once = False
                        _n += 1
                        logger.ui(f"结契第{_n}只成功")
                    if not self.check_pokemon():
                        break
                    random_sleep()
                    continue
                case "start_jieqi":
                    logger.scene("结契")
                    click(coor)
                    random_sleep(10)
                    _flag_first: bool = False
                    _timer = WorkTimer(2 * 60, self.timer_jieqi_finish)
                    _timer.start()

                    while True:
                        if not self._flag_timer_jieqi_finish:
                            # TODO 需要识别其他罗盘点击
                            logger.ui("没有足够的指定的罗盘", "warn")

                        if check_finish_once():
                            _flag_first = True
                            _timer.cancel()
                            random_sleep(0.5, 0.8)
                            finish_random_left_right()
                        elif _flag_first:
                            _flag_done_once = True
                            random_sleep(2)
                            break

    def run_jieqi(self):
        """结契"""
        while self._stone_count <= self._stone_numbers:
            self.summon_pokemon()
            self.catch_pokemon()

    def run(self):
        if self._flag_tancha:
            self.run_tancha()
        if self._flag_jieqi:
            self.run_jieqi()
