import threading
from subprocess import Popen, PIPE
from src import playback


class GuiController:

    @staticmethod
    def run_inference(onExit):
        def runInThread(onExit):
            proc = Popen("./scripts/run_inference.sh \"./exp/default/\" \"0\"", shell=True, stdout=PIPE)
            proc.wait()
            onExit.emit()
            return
        thread = threading.Thread(target=runInThread, args=(onExit,))
        thread.start()

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
