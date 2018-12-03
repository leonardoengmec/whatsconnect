from app.mac import mac, signals

@signals.command_received.connect
def handle(message):
    if message.command == "atualizarFoto":
        mac.set_profile_picture("/static/logo.jpg")
    