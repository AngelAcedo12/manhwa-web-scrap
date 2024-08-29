class convertTime:
    def __init__(self):
       pass

    def convert(self, time):
        minutes = time // 60
        seconds = time % 60
        hours = minutes // 60
        return f"{int(hours)}:{int(minutes)}:{int(seconds)}" if hours > 0 else f"{int(minutes)}:{int(seconds)}"