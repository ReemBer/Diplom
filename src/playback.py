import pygame


def play_music(music_file):
    """
    stream music with mixer.music module in blocking manner
    this will stream the sound from disk while playing
    """
    clock = pygame.time.Clock()
    try:
        pygame.mixer.music.load(music_file)
        print("Music file %s loaded!" % music_file)
    except pygame.error:
        print("File %s not found! (%s)" % (music_file, pygame.get_error()))
        return
    pygame.mixer.music.play()


def playback_midi_file(midi_file, freq=44100, bitsize=-16, channels=2, buffer=1024):
    pygame.mixer.init(freq, bitsize, channels, buffer)
    # optional volume 0 to 1.0
    pygame.mixer.music.set_volume(1.0)
    try:
        play_music(midi_file)
    except KeyboardInterrupt:
        # if user hits Ctrl/C then exit
        # (works only in console mode)
        pygame.mixer.music.fadeout(1000)
        pygame.mixer.music.stop()
        raise SystemExit


def play():
    playback_midi_file(
        './exp/default/results/inference/pianorolls/fake_x_hard_thresholding/fake_x_hard_thresholding_0.mid')


def pause_player():
    pygame.mixer.music.pause()


def resume_player():
    pygame.mixer.music.unpause()


def stop_player():
    pygame.mixer.music.stop()


if __name__ == '__main__':
    playback_midi_file(
        './exp/default/results/inference/pianorolls/fake_x_hard_thresholding/fake_x_hard_thresholding_0.mid')
