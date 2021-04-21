import string
import sys
import random
import subprocess
import urllib.request

import docker
import pymysql

from lid_ds.core import Scenario
from lid_ds.core.collector.json_file_store import JSONFileStorage
from lid_ds.core.image import StdinCommand, Image, ExecCommand, ChainImage
from lid_ds.sim import gen_schedule_wait_times
from lid_ds.utils.docker_utils import get_host_port, get_ip_address

warmup_time = int(sys.argv[1])
recording_time = int(sys.argv[2])
is_exploit = int(sys.argv[3])
do_exploit = True
if is_exploit < 1:
    do_exploit = False

total_duration = warmup_time + recording_time
exploit_time = random.randint(int(recording_time * .3), int(recording_time * .8))

min_user_count = 10
max_user_count = 25
user_count = random.randint(min_user_count, max_user_count)

wait_times = [gen_schedule_wait_times(total_duration) for _ in range(user_count)]


class Bruteforce_CWE_307(Scenario):
    victim_ip = ""

    def init_victim(self, container, logger):
        pass

    def wait_for_availability(self, container):
        try:
            self.victim_ip = get_ip_address(container)
            url = "http://" + self.victim_ip + "/private/index.html"
            print("checking... is victim ready?")
            with urllib.request.urlopen(url) as response:
                data = response.read().decode("utf8")
                if "Simple Web App" in data:
                    print("is ready...")
                    print("configuring and creating clients...")
                    return True
                else:
                    print("not ready yet...")
                    return False
        except Exception as error:
            print("not ready yet with error: " + str(error))
            return False


storage_services = [JSONFileStorage()]

post_freq = "20"

victim = Image("victim_bruteforce")
normal = Image("normal_bruteforce", command=StdinCommand(""), init_args="-ip ${victim} -post " + str(post_freq))
exploit = Image("exploit_bruteforce", command=StdinCommand(""), init_args="${victim}")

if do_exploit:
    scenario_normal = Bruteforce_CWE_307(
        victim=victim,
        normal=normal,
        exploit=exploit,
        wait_times=wait_times,
        warmup_time=warmup_time,
        recording_time=recording_time,
        storage_services=storage_services,
        exploit_start_time=exploit_time
    )
else:
    scenario_normal = Bruteforce_CWE_307(
        victim=victim,
        normal=normal,
        exploit=exploit,
        wait_times=wait_times,
        warmup_time=warmup_time,
        recording_time=recording_time,
        storage_services=storage_services,
    )

scenario_normal()
