def returnSeconds(seconds):
    return f"%.2f"%(seconds)

def returnMinutes(seconds):
    return f"{int(seconds//60)}m %.2fs"%(seconds%60)

def returnHours(seconds):
    return f"{int(seconds//3600)}h {int((seconds%3600)//60)}m %.2fs"%((seconds%60))

def returnAuto(seconds):
    if seconds >= 3600:
        return returnHours(seconds)
    elif seconds >= 60:
        return returnMinutes(seconds)
    else:
        return returnSeconds(seconds)
