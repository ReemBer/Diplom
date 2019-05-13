from subprocess import Popen, PIPE
from src import playback


class GuiController:

    @staticmethod
    def run_inference(log_area):
        proc = Popen("./scripts/run_inference.sh \"./exp/default/\" \"0\"",
                     shell=True,
                     stdout=PIPE)
        # while True:
        #     line = proc.stdout.readline()
        #     if not line:
        #         break
        #     log_area.append(line)

    @staticmethod
    def play():
        playback.play()

    @staticmethod
    def pause():
        playback.pause_player()

    @staticmethod
    def resume():
        playback.resume_player()

    @staticmethod
    def stop():
        playback.stop_player()
