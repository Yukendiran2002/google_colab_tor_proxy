import subprocess

def runn_command(command):
    """Run a shell command."""
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing {command}: {e.stderr}")

def install_dependencies():
    """Update and install necessary packages."""
    runn_command("sudo apt update")
    runn_command("sudo apt install -y tor netcat curl privoxy")

def configure_tor():
    """Configure Tor settings."""
    torrc_config = [
        "ControlPort 9051",
        "CookieAuthentication 0",
        "HashedControlPassword 16:C55D891114CC4647600E6F2BE93DB9593CAD368F18C48F3FF9B03EE7D9",
        "UseEntryGuards 0",
        "NumEntryGuards 1",
         "NewCircuitPeriod 10",     
        "MaxCircuitDirtiness 10", 
        "AvoidDiskWrites 1"
    ]
    with open("/etc/tor/torrc", "a") as torrc:
        for line in torrc_config:
            torrc.write(line + "\n")

def configure_privoxy():
    """Configure Privoxy to route traffic through Tor."""
    privoxy_config = "forward-socks5t / 127.0.0.1:9050 .\n"
    with open("/etc/privoxy/config", "a") as privoxy:
        privoxy.write(privoxy_config)

def start_services():
    """Start Tor and Privoxy services."""
    runn_command("service tor start")
    runn_command("service privoxy start")

def check_services():
    """Check if services are running."""
    runn_command("service tor status")
    runn_command("privoxy --version")

def tor_proxy_setup():
    install_dependencies()
    configure_tor()
    configure_privoxy()
    start_services()
    check_services()
    print("Installation and configuration complete.")
    print("Tor and Privoxy are now running.")
    print("You can now use privoxy to route traffic through Tor via http://127.0.0.1:8118 or http://localhost:8118.")
