# Return a list of users on this system

def get_users():
    # thanks, ~dan!
    users = []
    with open("/etc/passwd", "r") as f:
        for line in f:
            if "/bin/bash" in line:
                u = line.split(":")[0]  # Grab all text before first ':'
                users.append(u)
                
    return users