# -*- coding: UTF-8 -*-
"""
Tencent is pleased to support the open source community by making GAutomator available.
Copyright (C) 2016 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at
http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" basis, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

"""
__author__ = 'minhuaxu wukenaihesos@gmail.com'

import os
from wpyscripts.tools.basic_operator import *
import wpyscripts.tools.traverse.travel as travel

logger = manager.get_testcase_logger()


def random_search_test():
    log_dir = os.environ.get("UPLOADDIR")
    if log_dir:
        log_dir = os.path.join(log_dir, "policy.log")
    else:
        log_dir = "policy.log"
    logger.info("run random search in testcase runner")
    travel.explore(log_dir, [], mode=0, max_num=3000)


def run():
    """
        begin of the test logic
    """
    try:
        nowStr = str(int(time.time()))
        import login_tester
        login_tester.main(nowStr, 2)
        time.sleep(5)
        import create_role_tester
        create_role_tester.create_role(nowStr)
        import tutorials_test
        tutorials_test.main()
        import battle_tester
        battle_tester.main()
    except Exception as e:
        traceback.print_exc()
        stack = traceback.format_exc()
        logger.error(stack)
        report.report(False, "Game Test", str(e))
    finally:
        report._report_total()
        report.screenshot()
