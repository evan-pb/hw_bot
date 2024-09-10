import fullbot as F

if __name__ == "__main__":
    while True:
        listener = F.keyboard.Listener(on_press=F.on_press)
        listener.start()
        listener.join()
